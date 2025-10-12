"""
System Cache Cleaner - Cleans user and system caches
"""

import os
from pathlib import Path
from typing import List, Dict
from .base_cleaner import BaseCleaner


class SystemCacheCleaner(BaseCleaner):
    """Cleans system and user cache directories"""
    
    def __init__(self):
        super().__init__(
            name="System Cache",
            description="User cache files (~/.cache)"
        )
    
    def scan(self) -> List[Dict]:
        """Scan for cache directories and files"""
        items = []
        
        # User cache directory
        user_cache = Path.home() / ".cache"
        
        if user_cache.exists():
            # Scan subdirectories in .cache
            try:
                for cache_dir in user_cache.iterdir():
                    if cache_dir.is_dir():
                        size = self.get_directory_size(str(cache_dir))
                        if size > 0:
                            items.append({
                                'path': str(cache_dir),
                                'name': cache_dir.name,
                                'size': size,
                                'type': 'directory'
                            })
            except PermissionError:
                pass
        
        return items
    
    def clean(self, items: List[Dict]) -> int:
        """Clean the specified cache items"""
        total_cleaned = 0
        
        for item in items:
            path = item['path']
            size = item['size']
            
            if self.safe_remove(path):
                total_cleaned += size
        
        return total_cleaned
