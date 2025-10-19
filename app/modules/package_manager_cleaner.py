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
                # Count only .deb files, not lock files and metadata
                size = self._count_package_files(apt_cache, "*.deb")
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
                # Count only .rpm files
                size = self._count_package_files(dnf_cache, "*.rpm")
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
                # Count only .pkg.tar.* files
                size = self._count_package_files(pacman_cache, "*.pkg.tar.*")
                if size > 0:
                    items.append({
                        'path': str(pacman_cache),
                        'name': 'Pacman Cache',
                        'size': size,
                        'type': 'pacman_cache',
                        'requires_root': True
                    })
        
        return items
    
    def _count_package_files(self, directory: Path, pattern: str) -> int:
        """Count size of package files matching pattern, ignoring metadata"""
        total_size = 0
        try:
            for file_path in directory.glob(pattern):
                if file_path.is_file():
                    try:
                        total_size += file_path.stat().st_size
                    except (OSError, PermissionError):
                        # If we can't read a file, try using sudo via du command
                        pass
        except (OSError, PermissionError):
            # If we can't list directory, try using du command with sudo
            # But for scan we don't want to prompt for sudo, so return 0
            pass
        
        return total_size
    
    def clean(self, items: List[Dict]) -> int:
        """Clean package manager caches - requires root privileges"""
        total_cleaned = 0
        
        for item in items:
            cache_type = item.get('type')
            size = item['size']
            
            # Use package manager commands for safe cleaning with elevated privileges
            if cache_type == 'apt_cache':
                result = self.run_command(['apt-get', 'clean'], use_sudo=True)
                if result.returncode == 0:
                    total_cleaned += size
                else:
                    print(f"APT clean failed: {result.stderr}")
            
            elif cache_type == 'dnf_cache':
                result = self.run_command(['dnf', 'clean', 'all'], use_sudo=True)
                if result.returncode == 0:
                    total_cleaned += size
                else:
                    print(f"DNF clean failed: {result.stderr}")
            
            elif cache_type == 'pacman_cache':
                result = self.run_command(['pacman', '-Sc', '--noconfirm'], use_sudo=True)
                if result.returncode == 0:
                    total_cleaned += size
                else:
                    print(f"Pacman clean failed: {result.stderr}")
        
        return total_cleaned
