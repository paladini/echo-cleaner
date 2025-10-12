"""
Log Cleaner - Manages system log files
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
from .base_cleaner import BaseCleaner


class LogCleaner(BaseCleaner):
    """Cleans old log files"""
    
    def __init__(self, days_old: int = 30):
        super().__init__(
            name="Logs",
            description=f"Log files older than {days_old} days"
        )
        self.days_old = days_old
    
    def scan(self) -> List[Dict]:
        """Scan for old log files"""
        items = []
        
        # User log directories
        log_paths = [
            Path.home() / ".local" / "share" / "xorg",
            Path.home() / ".xsession-errors"
        ]
        
        cutoff_date = datetime.now() - timedelta(days=self.days_old)
        
        for log_path in log_paths:
            if log_path.is_file():
                # Single log file
                try:
                    mtime = datetime.fromtimestamp(log_path.stat().st_mtime)
                    if mtime < cutoff_date:
                        size = log_path.stat().st_size
                        items.append({
                            'path': str(log_path),
                            'name': log_path.name,
                            'size': size,
                            'type': 'log_file',
                            'modified': mtime.strftime('%Y-%m-%d')
                        })
                except (OSError, PermissionError):
                    pass
            
            elif log_path.is_dir():
                # Log directory
                try:
                    for log_file in log_path.rglob("*.log*"):
                        if log_file.is_file():
                            try:
                                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                                if mtime < cutoff_date:
                                    size = log_file.stat().st_size
                                    items.append({
                                        'path': str(log_file),
                                        'name': log_file.name,
                                        'size': size,
                                        'type': 'log_file',
                                        'modified': mtime.strftime('%Y-%m-%d')
                                    })
                            except (OSError, PermissionError):
                                continue
                except (OSError, PermissionError):
                    pass
        
        return items
    
    def clean(self, items: List[Dict]) -> int:
        """Clean old log files"""
        total_cleaned = 0
        
        for item in items:
            path = item['path']
            size = item['size']
            
            if self.safe_remove(path):
                total_cleaned += size
        
        return total_cleaned
