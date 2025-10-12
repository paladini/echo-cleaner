"""
Echo Clear - Application Entry Point
"""

import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow
from services.cleaning_service import CleaningService
from modules import (
    SystemCacheCleaner,
    TrashCleaner,
    LogCleaner,
    PackageManagerCleaner,
    DockerCleaner,
    DevDependenciesCleaner,
    KubernetesCleaner
)


class EchoClearApp:
    """Main application controller"""
    
    def __init__(self):
        self.window = MainWindow()
        self.service = CleaningService()
        self.setup_cleaners()
        self.connect_signals()
    
    def setup_cleaners(self):
        """Register all cleaning modules"""
        self.service.register_cleaner(SystemCacheCleaner())
        self.service.register_cleaner(TrashCleaner())
        self.service.register_cleaner(LogCleaner())
        self.service.register_cleaner(PackageManagerCleaner())
        self.service.register_cleaner(DockerCleaner())
        self.service.register_cleaner(DevDependenciesCleaner())
        self.service.register_cleaner(KubernetesCleaner())
    
    def connect_signals(self):
        """Connect UI signals to service slots"""
        # UI to Service
        self.window.scan_requested.connect(self.on_scan_requested)
        self.window.clean_requested.connect(self.on_clean_requested)
        
        # Service to UI
        self.service.scan_started.connect(self.on_scan_started)
        self.service.scan_progress.connect(self.on_scan_progress)
        self.service.scan_completed.connect(self.on_scan_completed)
        self.service.scan_failed.connect(self.on_scan_failed)
        
        self.service.clean_started.connect(self.on_clean_started)
        self.service.clean_progress.connect(self.on_clean_progress)
        self.service.clean_completed.connect(self.on_clean_completed)
        self.service.clean_failed.connect(self.on_clean_failed)
    
    def on_scan_requested(self):
        """Handle scan request from UI"""
        self.service.start_scan()
    
    def on_scan_started(self):
        """Handle scan start"""
        self.window.enable_buttons(scan_enabled=False, clean_enabled=False)
        self.window.show_progress(visible=True)
        self.window.set_progress(0, "Starting scan...")
    
    def on_scan_progress(self, percentage, message):
        """Handle scan progress"""
        self.window.set_progress(percentage, message)
    
    def on_scan_completed(self, results):
        """Handle scan completion"""
        self.window.enable_buttons(scan_enabled=True)
        self.window.show_progress(visible=False)
        
        # Store results
        self.window.store_scan_results(results)
        
        # Update dashboard statistics
        total_size = results.get('total_size', 0)
        categories = results.get('categories', [])
        total_items = sum(len(cat.get('items', [])) for cat in categories)
        
        size_formatted = self.service.format_size(total_size)
        
        # Update dashboard
        self.window.update_dashboard_stats(size_formatted, total_items, len(categories))
        
        # Update category views with checkboxes
        category_name_map = {
            "System Cache": "System Cache",
            "Package Manager": "Package Manager",
            "Trash": "Trash",
            "Logs": "Logs",
            "Docker": "Docker",
            "Kubernetes": "Kubernetes",
            "Dev Dependencies": "Dev Dependencies"
        }
        
        for category in categories:
            cat_name = category.get('name')
            items = category.get('items', [])
            
            # Store cleaner reference for later
            category['cleaner_ref'] = category.get('cleaner')
            
            # Find matching UI category
            for ui_name, backend_name in category_name_map.items():
                if backend_name.lower() in cat_name.lower() or cat_name.lower() in backend_name.lower():
                    self.window.update_category_view(ui_name, items)
                    break
        
        # Show clean button if there's something to clean
        if total_size > 0:
            self.window.show_clean_button(visible=True)
            self.show_info_message(
                "Scan Complete",
                f"Found {size_formatted} of reclaimable space across {len(categories)} categories.\n\n"
                "Review and select items in each category, then click 'Clean Selected Items' on the Dashboard."
            )
        else:
            self.window.show_clean_button(visible=False)
            self.show_info_message(
                "Scan Complete",
                "Your system is already clean! No items found to clean."
            )
    
    def on_scan_failed(self, error_message):
        """Handle scan failure"""
        self.window.enable_buttons(scan_enabled=True)
        self.window.show_progress(visible=False)
        self.window.show_clean_button(visible=False)
        self.show_error_message("Scan Failed", f"An error occurred during scan:\n{error_message}")
    
    def on_clean_requested(self, selected_items_dict):
        """Handle clean request from UI with selected items"""
        # Get scan results to find cleaners
        results = self.window.scan_results
        if not results:
            self.show_warning_message("No Scan Results", "Please run a scan first.")
            return
        
        # Build categories with selected items only
        categories_to_clean = []
        total_size = 0
        total_items = 0
        
        # Map UI category names to backend category objects
        category_map = {}
        for category in results.get('categories', []):
            cat_name = category.get('name')
            category_map[cat_name] = category
        
        for ui_category_name, selected_items in selected_items_dict.items():
            # Find the matching backend category
            matched_category = None
            for backend_name, backend_category in category_map.items():
                if ui_category_name.lower() in backend_name.lower() or backend_name.lower() in ui_category_name.lower():
                    matched_category = backend_category
                    break
            
            if matched_category and selected_items:
                category_size = sum(item.get('size', 0) for item in selected_items)
                total_size += category_size
                total_items += len(selected_items)
                
                categories_to_clean.append({
                    'name': matched_category.get('name'),
                    'size': category_size,
                    'items': selected_items,
                    'cleaner': matched_category.get('cleaner')
                })
        
        if not categories_to_clean:
            self.show_warning_message("No Items Selected", "Please select at least one item to clean.")
            return
        
        # Confirm cleaning
        size_formatted = self.service.format_size(total_size)
        
        reply = QMessageBox.question(
            self.window,
            "Confirm Cleaning",
            f"This will clean:\n\n"
            f"• {total_items} selected items\n"
            f"• {size_formatted} of disk space\n"
            f"• Across {len(categories_to_clean)} categories\n\n"
            "This action cannot be undone. Continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.service.start_clean(categories_to_clean)
    
    def on_clean_started(self):
        """Handle clean start"""
        self.window.enable_buttons(scan_enabled=False)
        self.window.show_progress(visible=True)
        self.window.set_progress(0, "Starting cleaning...")
        self.window.show_clean_button(visible=False)
    
    def on_clean_progress(self, percentage, message):
        """Handle clean progress"""
        self.window.set_progress(percentage, message)
    
    def on_clean_completed(self, results):
        """Handle clean completion"""
        self.window.enable_buttons(scan_enabled=True)
        self.window.show_progress(visible=False)
        
        # Reset dashboard statistics
        self.window.update_dashboard_stats("0 B", 0, 0)
        
        # Clear all category views and selected items
        for category_name in self.window.category_views.keys():
            self.window.update_category_view(category_name, [])
        
        self.window.selected_items.clear()
        self.window.show_clean_button(visible=False)
        
        # Show success message
        total_cleaned = results.get('total_cleaned', 0)
        items_removed = results.get('items_removed', 0)
        size_formatted = self.service.format_size(total_cleaned)
        
        self.show_info_message(
            "Cleaning Complete! ✨",
            f"Successfully cleaned:\n\n"
            f"• {size_formatted} of disk space\n"
            f"• {items_removed} items removed\n\n"
            "Your system is now cleaner!"
        )
    
    def on_clean_failed(self, error_message):
        """Handle clean failure"""
        self.window.enable_buttons(scan_enabled=True)
        self.window.show_progress(visible=False)
        self.show_error_message("Cleaning Failed", f"An error occurred during cleaning:\n{error_message}")
    
    def show_info_message(self, title, message):
        """Show information message"""
        QMessageBox.information(self.window, title, message)
    
    def show_warning_message(self, title, message):
        """Show warning message"""
        QMessageBox.warning(self.window, title, message)
    
    def show_error_message(self, title, message):
        """Show error message"""
        QMessageBox.critical(self.window, title, message)
    
    def run(self):
        """Show the main window"""
        self.window.show()


def main():
    """Main application function"""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Echo Clear")
    app.setOrganizationName("Echo Clear Team")
    
    # Create and run Echo Clear
    echo_clear = EchoClearApp()
    echo_clear.run()
    
    # Execute event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
