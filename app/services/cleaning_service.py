"""
Cleaning Service - Core Business Logic
"""

from PySide6.QtCore import QObject, Signal, QThread
from typing import Dict, List
import humanize


class ScanWorker(QThread):
    """Worker thread for scanning system"""
    
    progress = Signal(int, str)  # percentage, status message
    finished = Signal(dict)  # scan results
    error = Signal(str)  # error message
    
    def __init__(self, cleaners):
        super().__init__()
        self.cleaners = cleaners
    
    def run(self):
        """Execute scan in background thread"""
        try:
            results = {
                'total_size': 0,
                'categories': []
            }
            
            total_cleaners = len(self.cleaners)
            
            for idx, cleaner in enumerate(self.cleaners):
                # Update progress
                progress_pct = int((idx / total_cleaners) * 100)
                self.progress.emit(progress_pct, f"Scanning {cleaner.name}...")
                
                # Scan cleaner
                items = cleaner.scan()
                
                if items:
                    category_size = sum(item.get('size', 0) for item in items)
                    results['total_size'] += category_size
                    results['categories'].append({
                        'name': cleaner.name,
                        'size': category_size,
                        'items': items,
                        'cleaner': cleaner
                    })
            
            self.progress.emit(100, "Scan complete!")
            self.finished.emit(results)
            
        except Exception as e:
            self.error.emit(str(e))


class CleanWorker(QThread):
    """Worker thread for cleaning"""
    
    progress = Signal(int, str)  # percentage, status message
    finished = Signal(dict)  # cleaning results
    error = Signal(str)  # error message
    
    def __init__(self, selected_categories):
        super().__init__()
        self.selected_categories = selected_categories
    
    def run(self):
        """Execute cleaning in background thread"""
        try:
            results = {
                'total_cleaned': 0,
                'items_removed': 0,
                'categories_cleaned': []
            }
            
            total_categories = len(self.selected_categories)
            
            for idx, category in enumerate(self.selected_categories):
                # Update progress
                progress_pct = int((idx / total_categories) * 100)
                self.progress.emit(progress_pct, f"Cleaning {category['name']}...")
                
                # Clean category
                cleaner = category['cleaner']
                items_to_clean = category['items']
                
                cleaned_size = cleaner.clean(items_to_clean)
                
                results['total_cleaned'] += cleaned_size
                results['items_removed'] += len(items_to_clean)
                results['categories_cleaned'].append(category['name'])
            
            self.progress.emit(100, "Cleaning complete!")
            self.finished.emit(results)
            
        except Exception as e:
            self.error.emit(str(e))


class CleaningService(QObject):
    """
    Service layer for managing cleaning operations.
    Orchestrates the different cleaning modules.
    """
    
    # Signals for UI communication
    scan_started = Signal()
    scan_progress = Signal(int, str)  # percentage, status message
    scan_completed = Signal(dict)  # scan results
    scan_failed = Signal(str)  # error message
    
    clean_started = Signal()
    clean_progress = Signal(int, str)  # percentage, status message
    clean_completed = Signal(dict)  # cleaning results
    clean_failed = Signal(str)  # error message
    
    def __init__(self):
        super().__init__()
        self.cleaners = []
        self.scan_results = None
        self.scan_worker = None
        self.clean_worker = None
    
    def register_cleaner(self, cleaner):
        """Register a cleaning module"""
        self.cleaners.append(cleaner)
    
    def start_scan(self):
        """Start system scan in background thread"""
        if self.scan_worker and self.scan_worker.isRunning():
            return  # Already scanning
        
        self.scan_started.emit()
        
        # Create and start worker thread
        self.scan_worker = ScanWorker(self.cleaners)
        self.scan_worker.progress.connect(self.scan_progress.emit)
        self.scan_worker.finished.connect(self._on_scan_finished)
        self.scan_worker.error.connect(self._on_scan_error)
        self.scan_worker.start()
    
    def _on_scan_finished(self, results):
        """Handle scan completion"""
        self.scan_results = results
        self.scan_completed.emit(results)
    
    def _on_scan_error(self, error_msg):
        """Handle scan error"""
        self.scan_failed.emit(error_msg)
    
    def start_clean(self, selected_categories):
        """Start cleaning process in background thread"""
        if self.clean_worker and self.clean_worker.isRunning():
            return  # Already cleaning
        
        if not selected_categories:
            self.clean_failed.emit("No categories selected for cleaning")
            return
        
        self.clean_started.emit()
        
        # Create and start worker thread
        self.clean_worker = CleanWorker(selected_categories)
        self.clean_worker.progress.connect(self.clean_progress.emit)
        self.clean_worker.finished.connect(self._on_clean_finished)
        self.clean_worker.error.connect(self._on_clean_error)
        self.clean_worker.start()
    
    def _on_clean_finished(self, results):
        """Handle cleaning completion"""
        self.clean_completed.emit(results)
        # Clear scan results after cleaning
        self.scan_results = None
    
    def _on_clean_error(self, error_msg):
        """Handle cleaning error"""
        self.clean_failed.emit(error_msg)
    
    def get_scan_results(self):
        """Get the last scan results"""
        return self.scan_results
    
    def format_size(self, size_bytes):
        """Format size in human-readable format"""
        return humanize.naturalsize(size_bytes, binary=True)
