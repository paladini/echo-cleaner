"""
Docker Cleaner - Cleans Docker artifacts
"""

import json
from typing import List, Dict
from .base_cleaner import BaseCleaner


class DockerCleaner(BaseCleaner):
    """Cleans Docker images, containers, and volumes"""
    
    def __init__(self):
        super().__init__(
            name="Docker",
            description="Docker images, containers, and volumes"
        )
    
    def scan(self) -> List[Dict]:
        """Scan for Docker artifacts to clean"""
        items = []
        
        # Check if Docker is available
        if not self.is_command_available('docker'):
            return items
        
        # Check if Docker daemon is running
        result = self.run_command(['docker', 'info'])
        if result.returncode != 0:
            return items
        
        # Find dangling images
        dangling_images = self._find_dangling_images()
        items.extend(dangling_images)
        
        # Find stopped containers
        stopped_containers = self._find_stopped_containers()
        items.extend(stopped_containers)
        
        # Find unused volumes
        unused_volumes = self._find_unused_volumes()
        items.extend(unused_volumes)
        
        # Build cache
        build_cache = self._get_build_cache_size()
        if build_cache:
            items.append(build_cache)
        
        return items
    
    def _find_dangling_images(self) -> List[Dict]:
        """Find dangling Docker images"""
        items = []
        
        result = self.run_command([
            'docker', 'images', 
            '--filter', 'dangling=true',
            '--format', '{{json .}}'
        ])
        
        if result.returncode == 0 and result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        image = json.loads(line)
                        # Parse size (e.g., "123MB" -> bytes)
                        size_str = image.get('Size', '0B')
                        size_bytes = self._parse_docker_size(size_str)
                        
                        items.append({
                            'path': image.get('ID'),
                            'name': f"Image {image.get('ID')[:12]}",
                            'size': size_bytes,
                            'type': 'docker_image',
                            'details': f"Dangling image"
                        })
                    except json.JSONDecodeError:
                        continue
        
        return items
    
    def _find_stopped_containers(self) -> List[Dict]:
        """Find stopped Docker containers"""
        items = []
        
        result = self.run_command([
            'docker', 'ps', '-a',
            '--filter', 'status=exited',
            '--format', '{{json .}}'
        ])
        
        if result.returncode == 0 and result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        container = json.loads(line)
                        size_str = container.get('Size', '0B')
                        size_bytes = self._parse_docker_size(size_str.split('(')[0].strip())
                        
                        items.append({
                            'path': container.get('ID'),
                            'name': container.get('Names', 'Unknown'),
                            'size': size_bytes,
                            'type': 'docker_container',
                            'details': f"Stopped container"
                        })
                    except json.JSONDecodeError:
                        continue
        
        return items
    
    def _find_unused_volumes(self) -> List[Dict]:
        """Find unused Docker volumes"""
        items = []
        
        result = self.run_command([
            'docker', 'volume', 'ls',
            '--filter', 'dangling=true',
            '--format', '{{.Name}}'
        ])
        
        if result.returncode == 0 and result.stdout:
            for volume_name in result.stdout.strip().split('\n'):
                if volume_name:
                    # Get volume size using inspect
                    inspect_result = self.run_command([
                        'docker', 'system', 'df', '-v',
                        '--format', '{{json .}}'
                    ])
                    
                    items.append({
                        'path': volume_name,
                        'name': volume_name,
                        'size': 0,  # Docker doesn't easily provide volume sizes
                        'type': 'docker_volume',
                        'details': f"Unused volume"
                    })
        
        return items
    
    def _get_build_cache_size(self) -> Dict:
        """Get Docker build cache size"""
        result = self.run_command(['docker', 'system', 'df', '--format', '{{json .}}'])
        
        if result.returncode == 0 and result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        data = json.loads(line)
                        if data.get('Type') == 'Build Cache':
                            size_str = data.get('Size', '0B')
                            size_bytes = self._parse_docker_size(size_str)
                            
                            if size_bytes > 0:
                                return {
                                    'path': 'build-cache',
                                    'name': 'Build Cache',
                                    'size': size_bytes,
                                    'type': 'docker_build_cache',
                                    'details': 'Docker build cache'
                                }
                    except json.JSONDecodeError:
                        continue
        
        return None
    
    def _parse_docker_size(self, size_str: str) -> int:
        """Parse Docker size string to bytes"""
        size_str = size_str.strip().upper()
        
        if not size_str or size_str == '0B':
            return 0
        
        units = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4
        }
        
        for unit, multiplier in units.items():
            if unit in size_str:
                try:
                    value = float(size_str.replace(unit, '').strip())
                    return int(value * multiplier)
                except ValueError:
                    return 0
        
        return 0
    
    def clean(self, items: List[Dict]) -> int:
        """Clean Docker artifacts"""
        total_cleaned = 0
        
        for item in items:
            item_type = item.get('type')
            size = item['size']
            path = item['path']
            
            if item_type == 'docker_image':
                result = self.run_command(['docker', 'rmi', path])
                if result.returncode == 0:
                    total_cleaned += size
            
            elif item_type == 'docker_container':
                result = self.run_command(['docker', 'rm', path])
                if result.returncode == 0:
                    total_cleaned += size
            
            elif item_type == 'docker_volume':
                result = self.run_command(['docker', 'volume', 'rm', path])
                if result.returncode == 0:
                    total_cleaned += size
            
            elif item_type == 'docker_build_cache':
                result = self.run_command(['docker', 'builder', 'prune', '-f'])
                if result.returncode == 0:
                    total_cleaned += size
        
        return total_cleaned
