"""
Dev Dependencies Cleaner - Cleans language-specific caches
"""

from pathlib import Path
from typing import List, Dict
from .base_cleaner import BaseCleaner


class DevDependenciesCleaner(BaseCleaner):
    """Cleans development dependency caches (npm, pip, maven, gradle, etc.)"""
    
    def __init__(self):
        super().__init__(
            name="Dev Dependencies",
            description="Language dependency caches (npm, pip, maven, gradle)"
        )
    
    def scan(self) -> List[Dict]:
        """Scan for development dependency caches"""
        items = []
        
        home = Path.home()
        
        # npm cache
        npm_cache = home / ".npm"
        if npm_cache.exists():
            size = self.get_directory_size(str(npm_cache))
            if size > 0:
                items.append({
                    'path': str(npm_cache),
                    'name': 'npm Cache',
                    'size': size,
                    'type': 'npm_cache'
                })
        
        # Yarn cache
        yarn_cache = home / ".yarn" / "cache"
        if yarn_cache.exists():
            size = self.get_directory_size(str(yarn_cache))
            if size > 0:
                items.append({
                    'path': str(yarn_cache),
                    'name': 'Yarn Cache',
                    'size': size,
                    'type': 'yarn_cache'
                })
        
        # pip cache
        pip_cache = home / ".cache" / "pip"
        if pip_cache.exists():
            size = self.get_directory_size(str(pip_cache))
            if size > 0:
                items.append({
                    'path': str(pip_cache),
                    'name': 'pip Cache',
                    'size': size,
                    'type': 'pip_cache'
                })
        
        # Maven cache
        maven_cache = home / ".m2" / "repository"
        if maven_cache.exists():
            size = self.get_directory_size(str(maven_cache))
            if size > 0:
                items.append({
                    'path': str(maven_cache),
                    'name': 'Maven Repository',
                    'size': size,
                    'type': 'maven_cache'
                })
        
        # Gradle cache
        gradle_cache = home / ".gradle" / "caches"
        if gradle_cache.exists():
            size = self.get_directory_size(str(gradle_cache))
            if size > 0:
                items.append({
                    'path': str(gradle_cache),
                    'name': 'Gradle Caches',
                    'size': size,
                    'type': 'gradle_cache'
                })
        
        # Go module cache
        go_cache = home / "go" / "pkg" / "mod"
        if go_cache.exists():
            size = self.get_directory_size(str(go_cache))
            if size > 0:
                items.append({
                    'path': str(go_cache),
                    'name': 'Go Modules',
                    'size': size,
                    'type': 'go_cache'
                })
        
        # Rust cargo cache
        cargo_cache = home / ".cargo" / "registry"
        if cargo_cache.exists():
            size = self.get_directory_size(str(cargo_cache))
            if size > 0:
                items.append({
                    'path': str(cargo_cache),
                    'name': 'Cargo Registry',
                    'size': size,
                    'type': 'cargo_cache'
                })
        
        return items
    
    def clean(self, items: List[Dict]) -> int:
        """Clean development caches"""
        total_cleaned = 0
        
        for item in items:
            path = item['path']
            size = item['size']
            cache_type = item.get('type')
            
            # Use package manager commands when available
            if cache_type == 'npm_cache' and self.is_command_available('npm'):
                result = self.run_command(['npm', 'cache', 'clean', '--force'])
                if result.returncode == 0:
                    total_cleaned += size
            
            elif cache_type == 'yarn_cache' and self.is_command_available('yarn'):
                result = self.run_command(['yarn', 'cache', 'clean'])
                if result.returncode == 0:
                    total_cleaned += size
            
            elif cache_type == 'pip_cache' and self.is_command_available('pip'):
                result = self.run_command(['pip', 'cache', 'purge'])
                if result.returncode == 0:
                    total_cleaned += size
            
            elif cache_type == 'gradle_cache' and self.is_command_available('gradle'):
                result = self.run_command(['gradle', 'cleanBuildCache'])
                if result.returncode == 0:
                    total_cleaned += size
            
            elif cache_type == 'go_cache' and self.is_command_available('go'):
                result = self.run_command(['go', 'clean', '-modcache'])
                if result.returncode == 0:
                    total_cleaned += size
            
            elif cache_type == 'cargo_cache' and self.is_command_available('cargo'):
                # Cargo doesn't have a clean command, remove manually
                if self.safe_remove(path):
                    total_cleaned += size
            
            else:
                # Fallback to manual removal
                if self.safe_remove(path):
                    total_cleaned += size
        
        return total_cleaned
