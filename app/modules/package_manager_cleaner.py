"""
Package Manager Cleaner - Cleans package manager caches
"""

import os
from pathlib import Path
from typing import List, Dict
from .base_cleaner import BaseCleaner


class PackageManagerCleaner(BaseCleaner):
    """Cleans package manager caches (APT, DNF, Pacman, etc.)"""
    
    def __init__(self):
        super().__init__(
            name="Package Manager",
            description="Package manager cache files"
        )
    
    def scan(self) -> List[Dict]:
        """Scan for package manager caches"""
        items = []
        
        # APT cache (Debian/Ubuntu)
        if self.is_command_available('apt'):
            apt_cache = Path("/var/cache/apt/archives")
            if apt_cache.exists():
                size = self.get_directory_size(str(apt_cache))
                if size > 0:
                    items.append({
                        'path': str(apt_cache),
                        'name': 'APT Cache',
                        'size': size,
                        'type': 'apt_cache',
                        'requires_root': True
                    })
        
        # DNF/YUM cache (Fedora/RHEL)
        if self.is_command_available('dnf'):
            dnf_cache = Path("/var/cache/dnf")
            if dnf_cache.exists():
                size = self.get_directory_size(str(dnf_cache))
                if size > 0:
                    items.append({
                        'path': str(dnf_cache),
                        'name': 'DNF Cache',
                        'size': size,
                        'type': 'dnf_cache',
                        'requires_root': True
                    })
        
        # Pacman cache (Arch Linux)
        if self.is_command_available('pacman'):
            pacman_cache = Path("/var/cache/pacman/pkg")
            if pacman_cache.exists():
                size = self.get_directory_size(str(pacman_cache))
                if size > 0:
                    items.append({
                        'path': str(pacman_cache),
                        'name': 'Pacman Cache',
                        'size': size,
                        'type': 'pacman_cache',
                        'requires_root': True
                    })
        
        return items
    
    def clean(self, items: List[Dict]) -> int:
        """Clean package manager caches"""
        total_cleaned = 0
        
        for item in items:
            cache_type = item.get('type')
            size = item['size']
            
            # Use package manager commands for safe cleaning
            if cache_type == 'apt_cache':
                result = self.run_command(['apt-get', 'clean'])
                if result.returncode == 0:
                    total_cleaned += size
            
            elif cache_type == 'dnf_cache':
                result = self.run_command(['dnf', 'clean', 'all'])
                if result.returncode == 0:
                    total_cleaned += size
            
            elif cache_type == 'pacman_cache':
                result = self.run_command(['pacman', '-Sc', '--noconfirm'])
                if result.returncode == 0:
                    total_cleaned += size
        
        return total_cleaned
