"""
Docker Cleaner - Cleans Docker artifacts
"""

import json
import re
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
        """Scan for Docker artifacts to clean - organized by subcategory"""
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
        for img in dangling_images:
            img['subcategory'] = 'Dangling Images'
        items.extend(dangling_images)
        
        # Find stopped containers
        stopped_containers = self._find_stopped_containers()
        for cont in stopped_containers:
            cont['subcategory'] = 'Stopped Containers'
        items.extend(stopped_containers)
        
        # Find unused volumes
        unused_volumes = self._find_unused_volumes()
        for vol in unused_volumes:
            vol['subcategory'] = 'Unused Volumes'
        items.extend(unused_volumes)
        
        # Build cache
        build_cache = self._get_build_cache_size()
        if build_cache:
            build_cache['subcategory'] = 'Build Cache'
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
                        # Parse size - Docker provides it in Size field
                        size_str = image.get('Size', '0B')
                        size_bytes = self._parse_docker_size(size_str)
                        
                        image_id = image.get('ID', 'unknown')[:12]
                        created = image.get('CreatedSince', 'unknown')
                        
                        items.append({
                            'path': image.get('ID'),
                            'name': f"Image {image_id}",
                            'size': size_bytes,
                            'type': 'docker_image',
                            'details': f"Created {created}"
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
                        
                        # Get actual size using docker ps with --size flag
                        size_result = self.run_command([
                            'docker', 'ps', '-a', '-s',
                            '--filter', f'id={container.get("ID")}',
                            '--format', '{{.Size}}'
                        ])
                        
                        size_bytes = 0
                        if size_result.returncode == 0 and size_result.stdout:
                            # Format is like "0B (virtual 1.23GB)"
                            size_str = size_result.stdout.strip().split('(')[0].strip()
                            size_bytes = self._parse_docker_size(size_str)
                        
                        items.append({
                            'path': container.get('ID'),
                            'name': container.get('Names', 'Unknown'),
                            'size': size_bytes,
                            'type': 'docker_container',
                            'details': f"Stopped • Status: {container.get('Status', 'Unknown')}"
                        })
                    except json.JSONDecodeError:
                        continue
        
        return items
    
    def _find_unused_volumes(self) -> List[Dict]:
        """Find unused Docker volumes with size detection"""
        items = []
        
        # Get all volumes with their sizes using docker system df -v
        df_result = self.run_command([
            'docker', 'system', 'df', '-v'
        ])
        
        # Parse volume sizes from docker system df -v
        # Format: VOLUME_NAME    LINKS    SIZE (columns aligned with lots of spaces)
        volume_sizes = {}
        if df_result.returncode == 0 and df_result.stdout:
            lines = df_result.stdout.strip().split('\n')
            in_volumes_section = False
            header_found = False
            
            for line in lines:
                # Find volumes section
                if 'Local Volumes space usage:' in line:
                    in_volumes_section = True
                    continue
                
                # Skip header line
                if in_volumes_section and 'VOLUME NAME' in line:
                    header_found = True
                    continue
                
                # Skip processing until we've seen the header
                if in_volumes_section and not header_found:
                    continue
                
                # Empty line after we've started processing data ends the section
                if in_volumes_section and header_found and not line.strip():
                    # Only break if we've already parsed some volumes
                    # (skip initial empty lines after header)
                    if volume_sizes:
                        break
                    else:
                        continue
                
                # Parse volume data line
                # The format has LOTS of whitespace between columns
                if in_volumes_section and header_found and line.strip():
                    # Split by whitespace and take last 2 elements as LINKS and SIZE
                    parts = line.split()
                    if len(parts) >= 3:
                        # Last part is SIZE, second-to-last is LINKS
                        size_str = parts[-1]
                        try:
                            links = int(parts[-2])
                            # Everything before last 2 elements is the volume name
                            vol_name = ' '.join(parts[:-2])
                            size_bytes = self._parse_docker_size(size_str)
                            volume_sizes[vol_name] = size_bytes
                        except ValueError:
                            # Second-to-last wasn't a number, skip this line
                            pass
        
        # Get dangling (unused) volumes
        result = self.run_command([
            'docker', 'volume', 'ls',
            '--filter', 'dangling=true',
            '--format', '{{.Name}}'
        ])
        
        if result.returncode == 0 and result.stdout:
            for volume_name in result.stdout.strip().split('\n'):
                if volume_name:
                    # Get size from the parsed volume_sizes dict
                    size_bytes = volume_sizes.get(volume_name, 0)
                    
                    # Add visual indicator for empty volumes
                    if size_bytes == 0:
                        details = "Empty volume • No data stored"
                    else:
                        details = "Unused volume"
                    
                    # Shorten volume name if too long for display
                    display_name = volume_name
                    if len(volume_name) > 64:
                        display_name = f"{volume_name[:32]}...{volume_name[-28:]}"
                    
                    items.append({
                        'path': volume_name,
                        'name': display_name,
                        'size': size_bytes,
                        'type': 'docker_volume',
                        'details': details
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
        if not size_str:
            return 0
            
        size_str = size_str.strip().upper()
        
        if size_str == '0B' or size_str == 'N/A':
            return 0
        
        # Remove any extra text (like "virtual" size info)
        size_str = size_str.split('(')[0].strip()
        
        units = {
            'TB': 1024 ** 4,
            'GB': 1024 ** 3,
            'MB': 1024 ** 2,
            'KB': 1024,
            'B': 1
        }
        
        # Try to find and parse the size with unit
        for unit, multiplier in units.items():
            if unit in size_str:
                try:
                    # Extract number, handling both "52.8MB" and "52.8 MB" formats
                    value_str = size_str.replace(unit, '').strip()
                    value = float(value_str)
                    return int(value * multiplier)
                except ValueError:
                    continue
        
        return 0
    
    def clean(self, items: List[Dict]) -> int:
        """Clean Docker artifacts"""
        total_cleaned = 0
        
        for item in items:
            item_type = item.get('type')
            size = item['size']
            path = item['path']
            
            if item_type == 'docker_image':
                # Try to remove image, if it fails due to conflict, force it
                result = self.run_command(['docker', 'rmi', path])
                if result.returncode != 0 and 'conflict' in result.stderr.lower():
                    # Image is being used by a stopped container, force removal
                    print(f"Image {path} in use, forcing removal...")
                    result = self.run_command(['docker', 'rmi', '-f', path])
                
                if result.returncode == 0:
                    total_cleaned += size
                else:
                    print(f"Failed to remove image {path}: {result.stderr}")
            
            elif item_type == 'docker_container':
                result = self.run_command(['docker', 'rm', path])
                if result.returncode == 0:
                    total_cleaned += size
                else:
                    print(f"Failed to remove container {path}: {result.stderr}")
            
            elif item_type == 'docker_volume':
                result = self.run_command(['docker', 'volume', 'rm', path])
                if result.returncode == 0:
                    total_cleaned += size
                else:
                    print(f"Failed to remove volume {path}: {result.stderr}")
            
            elif item_type == 'docker_build_cache':
                result = self.run_command(['docker', 'builder', 'prune', '-f'])
                if result.returncode == 0:
                    total_cleaned += size
                else:
                    print(f"Failed to clean build cache: {result.stderr}")
        
        return total_cleaned
