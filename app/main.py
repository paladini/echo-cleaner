"""
Echo Cleaner - Application Entry Point
"""

import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow
from ui.custom_dialog import CustomDialog, ConfirmDialog
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
            self.show_custom_dialog(
                "Scan Complete! 🔍",
                f"Found <b>{size_formatted}</b> of reclaimable space across <b>{len(categories)} categories</b>.<br><br>"
                "<b>Next steps:</b><br>"
                "• Review and select items in each category<br>"
                "• Click 'Clean Selected Items' when ready<br><br>"
                "<span style='color: #86868b;'>All items are selected by default for your convenience.</span>",
                icon_type="search"
            )
        else:
            self.window.show_clean_button(visible=False)
            self.show_custom_dialog(
                "Scan Complete! ✨",
                "Your system is already clean!\n\nNo items found that need cleaning.",
                icon_type="success"
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
        
        dialog = ConfirmDialog(
            self.window,
            "Confirm Cleaning",
            f"This will permanently delete:\n\n"
            f"• <b>{total_items}</b> selected items\n"
            f"• <b>{size_formatted}</b> of disk space\n"
            f"• Across <b>{len(categories_to_clean)}</b> categories\n\n"
            "⚠️ This action cannot be undone. Are you sure?",
            icon_type="warning"
        )
        
        if dialog.exec() == ConfirmDialog.Accepted:
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
        # Show success message
        total_cleaned = results.get('total_cleaned', 0)
        items_removed = results.get('items_removed', 0)
        failed_items = results.get('failed_items', [])
        size_formatted = self.service.format_size(total_cleaned)
        
        # Build message based on results
        if total_cleaned > 0 and not failed_items:
            # Full success
            message = (
                f"<b>Successfully cleaned:</b>\n\n"
                f"✓ <b>{size_formatted}</b> of disk space freed\n"
                f"✓ <b>{items_removed}</b> items removed\n\n"
                "<i>Refreshing system state...</i>"
            )
            icon = "success"
        elif total_cleaned > 0 and failed_items:
            # Partial success
            failed_categories = ", ".join([item['category'] for item in failed_items])
            message = (
                f"<b>Partially cleaned:</b>\n\n"
                f"✓ <b>{size_formatted}</b> of disk space freed\n"
                f"✓ <b>{items_removed}</b> items removed\n\n"
                f"⚠️ Some items couldn't be cleaned:\n"
                f"<i>{failed_categories}</i>\n\n"
                "<b>Tip:</b> Items marked with 🔒 require admin privileges.\n"
                "Run the app with sudo or pkexec for full access.\n\n"
                "<i>Refreshing system state...</i>"
            )
            icon = "warning"
        else:
            # Nothing cleaned
            message = (
                "⚠️ <b>No items were cleaned</b>\n\n"
                "This usually happens when:\n"
                "• Items require admin privileges (look for 🔒)\n"
                "• Files were already removed by another process\n\n"
                "<b>Tip:</b> Try running with:\n"
                "<code>pkexec echo-cleaner</code>\n\n"
                "<i>Refreshing system state...</i>"
            )
            icon = "warning"
        
        self.show_custom_dialog(
            "Cleaning Complete! ✨",
            message,
            icon_type=icon
        )
        
        # Automatically trigger a new scan to show updated state
        # This ensures the dashboard reflects what's still available to clean
        self.service.start_scan()
    
    def on_clean_failed(self, error_message):
        """Handle clean failure"""
        self.window.enable_buttons(scan_enabled=True)
        self.window.show_progress(visible=False)
        self.show_error_message("Cleaning Failed", f"An error occurred during cleaning:\n{error_message}")
    
    def show_custom_dialog(self, title, message, icon_type="info"):
        """Show custom styled dialog"""
        dialog = CustomDialog(self.window, title, message, icon_type)
        dialog.exec()
    
    def show_info_message(self, title, message):
        """Show information message (legacy fallback)"""
        self.show_custom_dialog(title, message, "info")
    
    def show_warning_message(self, title, message):
        """Show warning message"""
        dialog = CustomDialog(self.window, title, message, icon_type="warning")
        dialog.exec()
    
    def show_error_message(self, title, message):
        """Show error message"""
        dialog = CustomDialog(self.window, title, message, icon_type="error")
        dialog.exec()
    
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
    app.setApplicationName("Echo Cleaner")
    app.setOrganizationName("Echo Cleaner Team")
    
    # Create and run Echo Cleaner
    echo_clear = EchoClearApp()
    echo_clear.run()
    
    # Execute event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
