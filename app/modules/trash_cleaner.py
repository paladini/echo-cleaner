"""
Trash Cleaner - Empties the system trash
"""

import os
from pathlib import Path
from typing import List, Dict
from .base_cleaner import BaseCleaner


class TrashCleaner(BaseCleaner):
    """Cleans user trash directory"""
    
    def __init__(self):
        super().__init__(
            name="Trash",
            description="Empty trash bin"
        )
    
    def scan(self) -> List[Dict]:
        """Scan trash directory"""
        items = []
        
        # Standard trash locations
        trash_paths = [
            Path.home() / ".local" / "share" / "Trash" / "files",
            Path.home() / ".Trash"
        ]
        
        for trash_path in trash_paths:
            if trash_path.exists():
                try:
                    for item in trash_path.iterdir():
                        size = self.get_directory_size(str(item))
                        if size > 0:
                            items.append({
                                'path': str(item),
                                'name': item.name,
                                'size': size,
                                'type': 'trash_item'
                            })
                except PermissionError:
                    pass
        
        return items
    
    def clean(self, items: List[Dict]) -> int:
        """Clean trash items"""
        total_cleaned = 0
        
        for item in items:
            path = item['path']
            size = item['size']
            
            if self.safe_remove(path):
                total_cleaned += size
        
        return total_cleaned
