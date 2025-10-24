"""
Main Window UI Component
"""

import os
from pathlib import Path
from typing import List, Dict
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QListWidget, QListWidgetItem,
    QFrame, QProgressBar, QStackedWidget, QCheckBox, QScrollArea, QApplication,
    QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QFont, QPixmap
from .subcategory_widget import SubcategoryGroupWidget, ItemCheckboxWidget
from services.subcategory_service import SubcategoryService


class MainWindow(QMainWindow):
    """Main window for Echo Cleaner"""
    
    # Signals
    scan_requested = Signal()
    clean_requested = Signal(dict)  # Pass selected items
    
    def __init__(self):
        super().__init__()
        self.scan_results = None
        self.selected_items = {}
        self.current_category = None  # Track current category for header clean button
        self.subcategory_service = SubcategoryService()
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """Initialize the main window interface"""
        # Window settings
        self.setWindowTitle("Echo Cleaner - Intelligent System Cleaner")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left sidebar (categories)
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Right content area
        self.content_area = self.create_content_area()
        main_layout.addWidget(self.content_area, 1)
        
        # Ensure clean button is hidden on Dashboard at startup
        if hasattr(self, 'header_clean_button'):
            self.header_clean_button.setVisible(False)
        
        # Center window on screen
        self.center_on_screen()
    
    def create_sidebar(self):
        """Create the left sidebar with categories"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 30, 20, 20)
        layout.setSpacing(10)
        
        # Logo/Icon - Direct QLabel without frame
        logo_icon = QLabel()
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_icon.setScaledContents(False)  # Don't scale contents, we'll do it manually
        
        # Get path to logo image
        assets_dir = Path(__file__).parent.parent / "assets"
        logo_path = assets_dir / "logo.png"
        
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            # Use device pixel ratio for high DPI displays
            device_ratio = self.devicePixelRatio()
            # Scale to a larger size for better quality (120x120 logical pixels)
            scaled_pixmap = pixmap.scaled(
                int(120 * device_ratio), 
                int(120 * device_ratio), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            scaled_pixmap.setDevicePixelRatio(device_ratio)
            logo_icon.setPixmap(scaled_pixmap)
            logo_icon.setFixedSize(120, 120)
        else:
            # Fallback to emoji if logo not found
            logo_icon.setText("✨")
            logo_icon.setStyleSheet("font-size: 64px;")
            logo_icon.setFixedSize(120, 120)
        
        layout.addWidget(logo_icon, 0, Qt.AlignHCenter)
        layout.addSpacing(10)
        
        # App Title
        title = QLabel("Echo Cleaner")
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont("Inter", 24, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Categories list
        categories_label = QLabel("CATEGORIES")
        categories_label.setObjectName("sectionLabel")
        categories_label_font = QFont("Inter", 10, QFont.Bold)
        categories_label.setFont(categories_label_font)
        layout.addWidget(categories_label)
        
        layout.addSpacing(5)
        
        self.categories_list = QListWidget()
        self.categories_list.setObjectName("categoriesList")
        self.categories_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.categories_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.categories_list.setFocusPolicy(Qt.NoFocus)
        
        # Add categories
        categories = [
            ("🏠", "Dashboard"),
            ("💾", "System Cache"),
            ("📦", "Package Manager"),
            ("🗑️", "Trash"),
            ("📝", "Logs"),
            ("🐳", "Docker"),
            ("☸️", "Kubernetes"),
            ("📚", "Dev Dependencies"),
            ("ℹ️", "About")
        ]
        
        for icon, name in categories:
            item = QListWidgetItem(f"{icon}  {name}")
            item.setFont(QFont("Inter", 11))
            self.categories_list.addItem(item)
        
        # Set Dashboard as default
        self.categories_list.setCurrentRow(0)
        
        # Connect category selection
        self.categories_list.currentRowChanged.connect(self.on_category_changed)
        
        layout.addWidget(self.categories_list, 1)  # Give it stretch priority
        
        layout.addSpacing(10)
        
        # Version info
        version = QLabel("v1.3.0")
        version.setObjectName("versionLabel")
        version_font = QFont("Inter", 9)
        version.setFont(version_font)
        layout.addWidget(version)
        
        return sidebar
    
    def create_content_area(self):
        """Create the right content area"""
        content = QFrame()
        content.setObjectName("contentArea")
        
        layout = QVBoxLayout(content)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("stackedWidget")
        
        # Dashboard view (index 0)
        dashboard = self.create_dashboard()
        self.stacked_widget.addWidget(dashboard)
        
        # Category views (indices 1-7)
        self.category_views = {}
        for category_name in ["System Cache", "Package Manager", "Trash", "Logs", "Docker", "Kubernetes", "Dev Dependencies"]:
            view = self.create_category_view(category_name)
            self.stacked_widget.addWidget(view)
            self.category_views[category_name] = view
        
        # About view (index 8)
        about = self.create_about_view()
        self.stacked_widget.addWidget(about)
        
        layout.addWidget(self.stacked_widget, 1)
        
        return content
    
    def create_header(self):
        """Create the header with title and action buttons"""
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(75)  # Fixed height to prevent jumping
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignVCenter)  # Center items vertically
        
        # Title
        self.page_title = QLabel("Dashboard")
        self.page_title.setObjectName("pageTitle")
        title_font = QFont("Inter", 28, QFont.Bold)
        self.page_title.setFont(title_font)
        layout.addWidget(self.page_title)
        
        # Selection summary badge (hidden by default)
        self.header_selection_badge = QLabel("")
        self.header_selection_badge.setObjectName("headerSelectionBadge")
        self.header_selection_badge.setVisible(False)
        self.header_selection_badge.setFixedHeight(40)  # Fixed height to prevent jumping
        self.header_selection_badge.setAlignment(Qt.AlignCenter)  # Center text
        badge_font = QFont("Inter", 11, QFont.Medium)
        self.header_selection_badge.setFont(badge_font)
        layout.addWidget(self.header_selection_badge)
        
        layout.addStretch()
        
        # Scan button (visible only on Dashboard)
        self.scan_button = QPushButton("🔍 Scan System")
        self.scan_button.setObjectName("scanButton")
        self.scan_button.setMinimumHeight(48)  # Minimum height, can grow if needed
        self.scan_button.setMinimumWidth(170)  # Minimum width for text
        scan_font = QFont("Inter", 13, QFont.Medium)
        self.scan_button.setFont(scan_font)
        self.scan_button.setCursor(Qt.PointingHandCursor)
        self.scan_button.clicked.connect(self.scan_requested.emit)
        layout.addWidget(self.scan_button)
        
        # Clean button for category pages (starts hidden)
        self.header_clean_button = QPushButton("🧹 Clean Selected")
        self.header_clean_button.setObjectName("headerCleanButton")
        self.header_clean_button.setMinimumHeight(48)  # Minimum height, can grow if needed
        self.header_clean_button.setMinimumWidth(190)  # Minimum width for text
        clean_font = QFont("Inter", 13, QFont.Medium)
        self.header_clean_button.setFont(clean_font)
        self.header_clean_button.setCursor(Qt.PointingHandCursor)
        self.header_clean_button.setVisible(False)  # Start hidden on Dashboard
        self.header_clean_button.clicked.connect(self.on_header_clean_clicked)
        layout.addWidget(self.header_clean_button)
        
        return header
    
    def create_dashboard(self):
        """Create the dashboard view"""
        dashboard = QFrame()
        dashboard.setObjectName("dashboard")
        
        layout = QVBoxLayout(dashboard)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(25)
        
        # Welcome message
        layout.addSpacing(20)
        
        # Welcome message
        welcome = QLabel("Welcome to Echo Cleaner")
        welcome.setObjectName("welcomeTitle")
        welcome_font = QFont("Inter", 20, QFont.Medium)
        welcome.setFont(welcome_font)
        layout.addWidget(welcome)
        
        description = QLabel(
            "Echo Cleaner helps you reclaim disk space by cleaning system cache, "
            "unused packages, and development artifacts. Click 'Scan System' to begin."
        )
        description.setObjectName("description")
        description.setWordWrap(True)
        desc_font = QFont("Inter", 11)
        description.setFont(desc_font)
        layout.addWidget(description)
        
        layout.addSpacing(20)
        
        # Stats cards container
        stats_frame = QFrame()
        stats_frame.setObjectName("statsContainer")
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(20)
        
        # Total space card
        total_card = self.create_stat_card("Total Reclaimable", "0 B", "💾")
        stats_layout.addWidget(total_card)
        
        # Items found card
        items_card = self.create_stat_card("Items Found", "0", "📦")
        stats_layout.addWidget(items_card)
        
        # Categories card
        categories_card = self.create_stat_card("Categories", "0", "📊")
        stats_layout.addWidget(categories_card)
        
        layout.addWidget(stats_frame)
        
        layout.addSpacing(20)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status message
        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        status_font = QFont("Inter", 10)
        self.status_label.setFont(status_font)
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)
        
        layout.addSpacing(20)
        
        # Clean button (hidden by default, shown after scan)
        # Now using a more elegant single-button design
        self.clean_button = QPushButton("🧹 Clean Selected Items")
        self.clean_button.setObjectName("cleanButton")
        self.clean_button.setMinimumSize(200, 60)
        clean_font = QFont("Inter", 15, QFont.Bold)
        self.clean_button.setFont(clean_font)
        self.clean_button.setCursor(Qt.PointingHandCursor)
        self.clean_button.setVisible(False)
        self.clean_button.clicked.connect(self.on_clean_button_clicked)
        layout.addWidget(self.clean_button, alignment=Qt.AlignCenter)
        
        # Selected items summary
        self.selected_summary = QLabel("")
        self.selected_summary.setObjectName("selectedSummary")
        summary_font = QFont("Inter", 11)
        self.selected_summary.setFont(summary_font)
        self.selected_summary.setVisible(False)
        self.selected_summary.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.selected_summary, alignment=Qt.AlignCenter)
        
        layout.addStretch()
        
        return dashboard
    
    def create_stat_card(self, title, value, icon):
        """Create a statistics card"""
        card = QFrame()
        card.setObjectName("statCard")
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)
        
        # Icon and title row
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setObjectName("cardIcon")
        icon_font = QFont("Inter", 24)
        icon_label.setFont(icon_font)
        header_layout.addWidget(icon_label)
        
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("cardValue")
        value_font = QFont("Inter", 28, QFont.Bold)
        value_label.setFont(value_font)
        layout.addWidget(value_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        title_font = QFont("Inter", 11)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        return card
    
    def apply_styles(self):
        """Apply custom styles to the window"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f7;
            }
            
            /* Sidebar */
            #sidebar {
                background-color: #ffffff;
                border-right: 1px solid #e5e5e7;
            }
            
            #appTitle {
                color: #1d1d1f;
                margin-bottom: 5px;
            }
            
            #sectionLabel {
                color: #86868b;
                letter-spacing: 0.5px;
                margin-top: 10px;
                margin-bottom: 5px;
            }
            
            #categoriesList {
                background-color: transparent;
                border: none;
                outline: none;
            }
            
            #categoriesList::item {
                padding: 12px 15px;
                border-radius: 8px;
                color: #1d1d1f;
                margin: 2px 0px;
            }
            
            #categoriesList::item:selected {
                background-color: #007aff;
                color: #ffffff;
            }
            
            #categoriesList::item:hover:!selected {
                background-color: #f5f5f7;
            }
            
            #versionLabel {
                color: #86868b;
                margin-top: 10px;
            }
            
            /* Content Area */
            #contentArea {
                background-color: #f5f5f7;
            }
            
            #pageTitle {
                color: #1d1d1f;
            }
            
            /* Buttons */
            #scanButton {
                background-color: #e8e8ed;
                color: #1d1d1f;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-weight: 500;
                text-align: center;
            }
            
            #scanButton:hover {
                background-color: #d2d2d7;
            }
            
            #scanButton:pressed {
                background-color: #c7c7cc;
            }
            
            #scanButton:disabled {
                background-color: #f5f5f7;
                color: #86868b;
            }
            
            #cleanButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007aff, stop:1 #0051d5);
                color: #ffffff;
                border: none;
                border-radius: 15px;
                padding: 15px 30px;
                font-weight: 700;
                text-align: center;
            }
            
            #cleanButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0051d5, stop:1 #004ab8);
            }
            
            #cleanButton:pressed {
                background: #004ab8;
            }
            
            #cleanButton:disabled {
                background-color: #e8e8ed;
                color: #86868b;
            }
            
            /* Header selection badge */
            #headerSelectionBadge {
                background-color: rgba(0, 122, 255, 0.1);
                color: #007aff;
                border: 1px solid rgba(0, 122, 255, 0.2);
                border-radius: 12px;
                padding: 6px 16px;
                margin-left: 12px;
                font-weight: 600;
            }
            
            /* Header clean button (for category pages) */
            #headerCleanButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34c759, stop:1 #2da94b);
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-weight: 600;
                text-align: center;
            }
            
            #headerCleanButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2da94b, stop:1 #268f3f);
            }
            
            #headerCleanButton:pressed {
                background: #268f3f;
            }
            
            #headerCleanButton:disabled {
                background-color: #e8e8ed;
                color: #86868b;
            }
            
            #selectedSummary {
                color: #424245;
                margin-top: 10px;
            }
            
            /* Scroll Area */
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            
            QScrollBar:vertical {
                border: none;
                background-color: #f5f5f7;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #c7c7cc;
                border-radius: 5px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #a8a8ad;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            
            /* Item Checkbox Frame */
            #itemCheckboxFrame {
                background-color: #ffffff;
                border: 1px solid #e5e5e7;
                border-radius: 10px;
                margin: 2px 0px;
            }
            
            #itemCheckboxFrame:hover {
                background-color: #f9f9f9;
                border-color: #007aff;
            }
            
            #subcategoryHeader {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 122, 255, 0.06),
                    stop:1 rgba(0, 122, 255, 0.01));
                border-left: 2px solid #007aff;
                border-radius: 6px;
                margin: 6px 0px 3px 0px;
            }
            
            #subcategoryName {
                color: #1d1d1f;
                font-weight: 600;
                font-size: 12px;
            }
            
            #subcategoryCount {
                color: #ffffff;
                background-color: #007aff;
                padding: 3px 10px;
                border-radius: 12px;
                font-weight: 500;
                font-size: 10px;
                min-width: 65px;
                max-height: 24px;
            }
            
            #itemName {
                color: #1d1d1f;
            }
            
            #itemDetails {
                color: #86868b;
            }
            
            QCheckBox {
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                border-radius: 6px;
                border: 2px solid #d2d2d7;
                background-color: #ffffff;
            }
            
            QCheckBox::indicator:hover {
                border-color: #007aff;
            }
            
            QCheckBox::indicator:checked {
                background-color: #007aff;
                border-color: #007aff;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }
            
            /* Clickable selection badges - elegant green style with smooth transitions */
            QPushButton[objectName^="selectionBadge_"] {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #34C759, stop:1 #30B350);
                color: white;
                border: none;
                border-radius: 14px;
                padding: 10px 18px;
                font-weight: 600;
                text-align: left;
            }
            
            QPushButton[objectName^="selectionBadge_"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #28A745, stop:1 #259D3F);
            }
            
            QPushButton[objectName^="selectionBadge_"]:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1F8A37, stop:1 #1C7D32);
            }
            
            /* Different states for visual feedback */
            QPushButton[objectName^="selectionBadge_"][selectionState="none"] {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #F8F9FA, stop:1 #E9ECEF);
                color: #34C759;
                border: 2px solid #34C759;
            }
            
            QPushButton[objectName^="selectionBadge_"][selectionState="none"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #34C759, stop:1 #30B350);
                color: white;
                border: 2px solid #34C759;
            }
            
            QPushButton[objectName^="selectionBadge_"][selectionState="partial"] {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #007AFF, stop:1 #0051D5);
                color: white;
            }
            
            QPushButton[objectName^="selectionBadge_"][selectionState="partial"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0051D5, stop:1 #004AB8);
            }
            
            /* Dashboard */
            #welcomeTitle {
                color: #1d1d1f;
            }
            
            #description {
                color: #424245;
                line-height: 1.6;
            }
            
            #statsContainer {
                background-color: transparent;
            }
            
            #statCard {
                background-color: #ffffff;
                border-radius: 16px;
                border: 1px solid #e5e5e7;
                min-width: 200px;
            }
            
            #cardIcon {
                color: #86868b;
            }
            
            #cardValue {
                color: #1d1d1f;
            }
            
            #cardTitle {
                color: #86868b;
            }
            
            /* Progress Bar */
            #progressBar {
                border: none;
                border-radius: 4px;
                background-color: #e8e8ed;
            }
            
            #progressBar::chunk {
                background-color: #007aff;
                border-radius: 4px;
            }
            
            #statusLabel {
                color: #424245;
            }
            
            /* About Page */
            #aboutView {
                background-color: #f5f5f7;
            }
            
            #aboutVersion {
                color: #86868b;
                font-weight: 500;
                letter-spacing: 0.3px;
            }
            
            #aboutDescCard {
                background-color: #ffffff;
                border: 1px solid #e5e5e7;
                border-radius: 18px;
            }
            
            #aboutDescription {
                color: #1d1d1f;
                line-height: 1.55;
            }
            
            #aboutCreatorTitle {
                color: #86868b;
                letter-spacing: 1.5px;
                font-weight: 600;
            }
            
            #aboutCreatorName {
                color: #1d1d1f;
                letter-spacing: -0.3px;
            }
            
            #aboutCreatorSubtitle {
                color: #6e6e73;
                line-height: 1.5;
            }
            
            #aboutGithubButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d2f, stop:1 #1d1d1f);
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 14px 28px;
                text-align: center;
            }
            
            #aboutGithubButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3d3d3f, stop:1 #2d2d2f);
            }
            
            #aboutGithubButton:pressed {
                background: #1d1d1f;
            }
            
            #aboutSponsorButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff3b82, stop:1 #ff2d72);
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 14px 28px;
                text-align: center;
            }
            
            #aboutSponsorButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff5596, stop:1 #ff3b82);
            }
            
            #aboutSponsorButton:pressed {
                background: #ff2d72;
            }
            
            #aboutFooterNote {
                color: #86868b;
                line-height: 1.5;
            }
            
            /* Empty State */
            #emptyStateIcon {
                color: #86868b;
            }
            
            #emptyStateTitle {
                color: #1d1d1f;
            }
            
            #emptyStateMessage {
                color: #6e6e73;
                line-height: 1.6;
            }
        """)
    
    def center_on_screen(self):
        """Center the window on screen"""
        screen_geometry = self.screen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
    
    def on_category_changed(self, index):
        """Handle category selection change"""
        if index < 0:
            return
        
        # Update page title based on category
        category_names = [
            "Dashboard",
            "System Cache",
            "Package Manager",
            "Trash",
            "Logs",
            "Docker",
            "Kubernetes",
            "Dev Dependencies",
            "About"
        ]
        
        if index < len(category_names):
            self.page_title.setText(category_names[index])
            self.stacked_widget.setCurrentIndex(index)
            
            # Store current category for clean button functionality
            self.current_category = category_names[index] if index > 0 and index < 8 else None
            
            # Show/hide appropriate header button based on page
            if index == 0:  # Dashboard
                self.scan_button.setVisible(True)
                self.header_clean_button.setVisible(False)  # Hide on dashboard
                self.header_selection_badge.setVisible(False)  # Hide badge on dashboard
            elif index == 8:  # About page
                self.scan_button.setVisible(False)
                self.header_clean_button.setVisible(False)  # Hide on about
                self.header_selection_badge.setVisible(False)  # Hide badge on about
            else:  # Category pages
                self.scan_button.setVisible(False)
                # Clean button visibility will be updated by update_category_clean_buttons()
                self.update_header_clean_button_visibility()
                # Badge visibility will be updated by update_header_selection_badge()
                self.update_header_selection_badge()
    
    def create_category_view(self, category_name):
        """Create a category detail view"""
        view = QFrame()
        view.setObjectName("categoryView")
        
        layout = QVBoxLayout(view)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(25)
        
        # Description
        description = QLabel(self.get_category_description(category_name))
        description.setObjectName("description")
        description.setWordWrap(True)
        desc_font = QFont("Inter", 11)
        description.setFont(desc_font)
        layout.addWidget(description)
        
        layout.addSpacing(10)
        
        # Header with title and clickable selection badge
        header_layout = QHBoxLayout()
        header_widget = QWidget()
        header_widget.setObjectName(f"itemsHeader_{category_name}")
        header_widget.setFixedHeight(55)  # Fixed height to prevent jumping
        header_widget.setLayout(header_layout)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setAlignment(Qt.AlignVCenter)  # Center items vertically
        
        # Title
        items_label = QLabel("Items to Clean")
        items_label.setObjectName("welcomeTitle")
        items_label_font = QFont("Inter", 16, QFont.Medium)
        items_label.setFont(items_label_font)
        header_layout.addWidget(items_label)
        
        # Clickable selection status badge (replaces Select All button)
        selection_badge = QPushButton("")
        selection_badge.setObjectName(f"selectionBadge_{category_name}")
        selection_badge.setVisible(False)
        selection_badge.setCursor(Qt.PointingHandCursor)
        selection_badge.setAutoDefault(False)
        selection_badge.setDefault(False)
        selection_badge.setFocusPolicy(Qt.NoFocus)  # Remove focus rectangle
        selection_badge.setMinimumWidth(160)  # Wide enough for "☐ Deselect All"
        selection_badge.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)  # Fixed width, flexible height
        badge_font = QFont("Inter", 11, QFont.Medium)
        selection_badge.setFont(badge_font)
        selection_badge.clicked.connect(lambda: self.toggle_select_all(category_name))
        
        # Install event filter for hover text change
        selection_badge.installEventFilter(self)
        
        header_layout.addWidget(selection_badge)
        
        header_layout.addStretch()
        
        layout.addWidget(header_widget)
        
        # Scroll area for items
        scroll_area = QScrollArea()
        scroll_area.setObjectName(f"scrollArea_{category_name}")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Items container inside scroll area
        items_container = QWidget()
        items_container.setObjectName(f"itemsContainer_{category_name}")
        items_layout = QVBoxLayout(items_container)
        items_layout.setContentsMargins(0, 0, 0, 0)
        items_layout.setSpacing(8)
        items_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(items_container)
        layout.addWidget(scroll_area, 1)
        
        # Empty state widget (hidden by default, shown when no items)
        empty_state = QWidget()
        empty_state.setObjectName(f"emptyState_{category_name}")
        empty_state.setVisible(False)
        empty_state_layout = QVBoxLayout(empty_state)
        empty_state_layout.setContentsMargins(40, 60, 40, 60)
        empty_state_layout.setSpacing(15)
        empty_state_layout.setAlignment(Qt.AlignCenter)
        
        # Icon
        empty_icon = QLabel("✨")
        empty_icon.setObjectName("emptyStateIcon")
        empty_icon.setAlignment(Qt.AlignCenter)
        empty_icon_font = QFont("Inter", 48)
        empty_icon.setFont(empty_icon_font)
        empty_state_layout.addWidget(empty_icon)
        
        # Title
        empty_title = QLabel("All Clean!")
        empty_title.setObjectName("emptyStateTitle")
        empty_title.setAlignment(Qt.AlignCenter)
        empty_title_font = QFont("Inter", 18, QFont.Bold)
        empty_title.setFont(empty_title_font)
        empty_state_layout.addWidget(empty_title)
        
        # Message
        empty_message = QLabel("No items found in this category.\nYour system is already optimized here.")
        empty_message.setObjectName("emptyStateMessage")
        empty_message.setAlignment(Qt.AlignCenter)
        empty_message.setWordWrap(True)
        empty_message_font = QFont("Inter", 12)
        empty_message.setFont(empty_message_font)
        empty_state_layout.addWidget(empty_message)
        
        layout.addWidget(empty_state)
        
        return view
    
    def create_about_view(self):
        """Create about view - elegant and modern"""
        view = QFrame()
        view.setObjectName("aboutView")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(60, 45, 60, 45)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        # Versão
        version_label = QLabel("Version 1.3.0")
        version_label.setObjectName("aboutVersion")
        version_label.setAlignment(Qt.AlignCenter)
        version_font = QFont("Inter", 12)
        version_label.setFont(version_font)
        layout.addWidget(version_label, 0, Qt.AlignHCenter)
        layout.addSpacing(28)
        
        # Card de descrição
        desc_card = QFrame()
        desc_card.setObjectName("aboutDescCard")
        desc_card.setMaximumWidth(520)
        desc_layout = QVBoxLayout(desc_card)
        desc_layout.setContentsMargins(30, 22, 30, 22)
        desc_layout.setSpacing(0)
        
        description = QLabel("An intelligent system cleaner for Linux, designed to help you reclaim disk space with style and efficiency.")
        description.setObjectName("aboutDescription")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        desc_font = QFont("Inter", 13)
        description.setFont(desc_font)
        desc_layout.addWidget(description)
        
        layout.addWidget(desc_card, 0, Qt.AlignHCenter)
        layout.addSpacing(32)
        
        # Seção do criador
        creator_title = QLabel("CREATED BY")
        creator_title.setObjectName("aboutCreatorTitle")
        creator_title.setAlignment(Qt.AlignCenter)
        creator_title_font = QFont("Inter", 9, QFont.Bold)
        creator_title.setFont(creator_title_font)
        layout.addWidget(creator_title, 0, Qt.AlignHCenter)
        
        layout.addSpacing(8)
        
        creator_name = QLabel("Fernando Paladini")
        creator_name.setObjectName("aboutCreatorName")
        creator_name.setAlignment(Qt.AlignCenter)
        creator_name_font = QFont("Inter", 20, QFont.Bold)
        creator_name.setFont(creator_name_font)
        layout.addWidget(creator_name, 0, Qt.AlignHCenter)
        
        layout.addSpacing(6)
        
        creator_subtitle = QLabel("Building powerful Linux applications through Vibe Coding")
        creator_subtitle.setObjectName("aboutCreatorSubtitle")
        creator_subtitle.setAlignment(Qt.AlignCenter)
        creator_subtitle.setWordWrap(True)
        creator_subtitle_font = QFont("Inter", 12)
        creator_subtitle.setFont(creator_subtitle_font)
        layout.addWidget(creator_subtitle)
        
        layout.addSpacing(32)
        
        # Botões de ação (apenas 2)
        buttons_container = QWidget()
        buttons_container.setMaximumWidth(340)
        buttons_layout = QVBoxLayout(buttons_container)
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        github_button = QPushButton("⭐  Star on GitHub")
        github_button.setObjectName("aboutGithubButton")
        github_button.setFixedHeight(46)
        github_button.setCursor(Qt.PointingHandCursor)
        github_font = QFont("Inter", 13, QFont.DemiBold)
        github_button.setFont(github_font)
        github_button.clicked.connect(lambda: self.open_url("https://github.com/paladini/echo-cleaner"))
        buttons_layout.addWidget(github_button)
        
        sponsor_button = QPushButton("💖  Sponsor this Project")
        sponsor_button.setObjectName("aboutSponsorButton")
        sponsor_button.setFixedHeight(46)
        sponsor_button.setCursor(Qt.PointingHandCursor)
        sponsor_font = QFont("Inter", 13, QFont.DemiBold)
        sponsor_button.setFont(sponsor_font)
        sponsor_button.clicked.connect(lambda: self.open_url("https://github.com/sponsors/paladini"))
        buttons_layout.addWidget(sponsor_button)
        
        layout.addWidget(buttons_container, 0, Qt.AlignHCenter)
        layout.addSpacing(24)
        
        # Nota de rodapé
        footer_note = QLabel("Can't sponsor? A star is just as meaningful ⭐")
        footer_note.setObjectName("aboutFooterNote")
        footer_note.setAlignment(Qt.AlignCenter)
        footer_note.setWordWrap(True)
        footer_font = QFont("Inter", 11)
        footer_note.setFont(footer_font)
        layout.addWidget(footer_note)
        
        layout.addSpacing(45)
        
        scroll.setWidget(content)
        
        main_layout = QVBoxLayout(view)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
        return view
    
    def open_url(self, url):
        """Open URL in default browser"""
        import webbrowser
        webbrowser.open(url)
    
    def get_category_description(self, category_name):
        """Get description for a category"""
        descriptions = {
            "System Cache": "Clean user cache files from ~/.cache. These files are automatically recreated by applications as needed.",
            "Package Manager": "Clean package manager caches (APT, DNF, Pacman). These are downloaded packages that can be re-downloaded if needed.",
            "Trash": "Empty your trash bin. Files will be permanently deleted and cannot be recovered.",
            "Logs": "Remove old log files (older than 30 days). Recent logs are kept for troubleshooting.",
            "Docker": "Clean Docker artifacts including dangling images, stopped containers, unused volumes, and build cache.",
            "Kubernetes": "Clean local Kubernetes cluster caches from minikube, kind, kubectl, and helm.",
            "Dev Dependencies": "Clean development dependency caches (npm, yarn, pip, maven, gradle, go, cargo). Dependencies will be re-downloaded when needed."
        }
        return descriptions.get(category_name, "Scan your system to see what can be cleaned in this category.")
    
    def update_dashboard_stats(self, total_size, items_count, categories_count):
        """Update dashboard statistics"""
        dashboard = self.stacked_widget.widget(0)
        stats_container = dashboard.findChild(QFrame, "statsContainer")
        
        if stats_container:
            cards = stats_container.findChildren(QFrame, "statCard")
            if len(cards) >= 3:
                # Update Total Reclaimable
                value_labels = cards[0].findChildren(QLabel, "cardValue")
                if value_labels:
                    value_labels[0].setText(total_size)
                
                # Update Items Found
                value_labels = cards[1].findChildren(QLabel, "cardValue")
                if value_labels:
                    value_labels[0].setText(str(items_count))
                
                # Update Categories
                value_labels = cards[2].findChildren(QLabel, "cardValue")
                if value_labels:
                    value_labels[0].setText(str(categories_count))
    
    def update_category_view(self, category_name, items):
        """Update a category view with scan results - using new component architecture"""
        if category_name not in self.category_views:
            return
        
        view = self.category_views[category_name]
        items_container = view.findChild(QWidget, f"itemsContainer_{category_name}")
        empty_state = view.findChild(QWidget, f"emptyState_{category_name}")
        scroll_area = view.findChild(QScrollArea, f"scrollArea_{category_name}")
        items_header = view.findChild(QWidget, f"itemsHeader_{category_name}")
        
        if not items_container:
            return
        
        # Clear existing items
        layout = items_container.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Initialize selected items for this category
        if category_name not in self.selected_items:
            self.selected_items[category_name] = {}
        
        if not items:
            # Show empty state, hide items container and header
            if empty_state:
                empty_state.setVisible(True)
            if scroll_area:
                scroll_area.setVisible(False)
            if items_header:
                items_header.setVisible(False)
            
            # Hide badge when no items
            selection_badge = view.findChild(QPushButton, f"selectionBadge_{category_name}")
            if selection_badge:
                selection_badge.setVisible(False)
        else:
            # Hide empty state, show items container and header
            if empty_state:
                empty_state.setVisible(False)
            if scroll_area:
                scroll_area.setVisible(True)
            if items_header:
                items_header.setVisible(True)
            
            # Check if items have subcategories using the service
            if self.subcategory_service.has_subcategories(items):
                # Render with subcategory groups
                self._render_with_subcategories(category_name, items, layout)
            else:
                # Render without subcategories (legacy mode)
                self._render_without_subcategories(category_name, items, layout)
            
            layout.addStretch()
            
            # Force initial update of category visuals after rendering
            self.update_category_selection_visuals(category_name)
        
        self.update_selection_summary()
    
    def _render_with_subcategories(self, category_name: str, items: List[Dict], layout):
        """Render items organized by subcategories using new components"""
        grouped_items = self.subcategory_service.group_items_by_subcategory(items)
        
        idx = 0
        for subcat_name in sorted(grouped_items.keys()):
            subcat_items = grouped_items[subcat_name]
            
            # Create subcategory group widget
            def make_id_generator(base_idx):
                return lambda item_idx: f"{category_name}_{base_idx + item_idx}"
            
            group_widget = SubcategoryGroupWidget(
                subcategory_name=subcat_name,
                items=subcat_items,
                category_name=category_name,
                item_id_generator=make_id_generator(idx)
            )
            
            # Connect selection changes and store items
            for item_idx, item_widget in enumerate(group_widget.item_widgets):
                global_idx = idx + item_idx
                self.selected_items[category_name][global_idx] = {
                    'selected': True,
                    'data': item_widget.item_data
                }
                
                # Connect signal with proper closure to capture global_idx by value
                def make_callback(cat, gidx):
                    return lambda checked: self._on_item_selection_changed_new(cat, gidx, checked)
                
                item_widget.selection_changed.connect(make_callback(category_name, global_idx))
            
            layout.addWidget(group_widget)
            idx += len(subcat_items)
    
    def _render_without_subcategories(self, category_name: str, items: List[Dict], layout):
        """Render items without subcategory grouping (legacy mode)"""
        for idx, item_data in enumerate(items):
            item_id = f"{category_name}_{idx}"
            item_widget = ItemCheckboxWidget(item_data, item_id)
            
            # Store selection state
            self.selected_items[category_name][idx] = {
                'selected': True,
                'data': item_data
            }
            
            # Connect selection change - use a factory function to capture idx by value
            def make_callback(cat, item_idx):
                return lambda checked: self._on_item_selection_changed_new(cat, item_idx, checked)
            
            item_widget.selection_changed.connect(make_callback(category_name, idx))
            
            layout.addWidget(item_widget)
    
    def _on_item_selection_changed_new(self, category_name: str, item_idx: int, is_checked: bool):
        """Handle item selection change from new components"""
        if category_name not in self.selected_items:
            return
            
        if item_idx not in self.selected_items[category_name]:
            return
        
        # Update selection state
        self.selected_items[category_name][item_idx]['selected'] = is_checked
        
        # Force immediate visual update
        self.update_category_selection_visuals(category_name)
        self.update_selection_summary()
        
        # Force Qt to process pending events and update the UI
        QApplication.processEvents()
        
        # Force the view to repaint
        if category_name in self.category_views:
            view = self.category_views[category_name]
            view.update()
            view.repaint()
    
    # Legacy methods - kept for backward compatibility if needed
    # These are now replaced by SubcategoryGroupWidget and ItemCheckboxWidget
    
    def on_item_selection_changed(self, category_name, item_idx, is_checked):
        """Legacy method - redirects to new implementation"""
        self._on_item_selection_changed_new(category_name, item_idx, is_checked)
    
    def toggle_select_all(self, category_name):
        """Toggle select all items in a category with visual feedback"""
        if category_name not in self.selected_items:
            return
        
        view = self.category_views[category_name]
        items_container = view.findChild(QWidget, f"itemsContainer_{category_name}")
        
        if not items_container:
            return
        
        # Check if all are currently selected
        all_selected = all(
            item['selected'] 
            for item in self.selected_items[category_name].values()
            if item  # Skip None values
        )
        
        # Toggle all: if all selected, deselect. Otherwise, select all.
        new_state = not all_selected
        
        # Update internal state
        for item_idx in self.selected_items[category_name]:
            self.selected_items[category_name][item_idx]['selected'] = new_state
        
        # Update all checkbox widgets in the UI
        checkboxes = items_container.findChildren(QCheckBox)
        for checkbox in checkboxes:
            if checkbox.objectName().startswith(f"checkbox_{category_name}_"):
                checkbox.blockSignals(True)  # Prevent signal spam
                checkbox.setChecked(new_state)
                checkbox.blockSignals(False)
        
        # Force immediate update of category visuals
        self.update_category_selection_visuals(category_name)
        self.update_selection_summary()
    
    def update_category_selection_visuals(self, category_name):
        """Update clickable badge for a specific category"""
        if category_name not in self.selected_items or category_name not in self.category_views:
            return
        
        view = self.category_views[category_name]
        
        # Count selected items
        total_items = len(self.selected_items[category_name])
        if total_items == 0:
            return
            
        selected_count = sum(
            1 for item in self.selected_items[category_name].values() 
            if item['selected']
        )
        
        # Update clickable selection badge (now a button)
        selection_badge = view.findChild(QPushButton, f"selectionBadge_{category_name}")
        if selection_badge:
            # Store state as property for hover effect
            selection_badge.setProperty("selectionState", 
                "all" if selected_count == total_items 
                else "none" if selected_count == 0 
                else "partial")
            selection_badge.setProperty("selectedCount", selected_count)
            selection_badge.setProperty("totalItems", total_items)
            
            # Set text based on state
            if selected_count == total_items:
                # All selected - show "All selected" normally, "Deselect All" on hover
                selection_badge.setText("✓ All selected")
                selection_badge.setToolTip("Click to deselect all items")
            elif selected_count == 0:
                # None selected - show "Select All"
                selection_badge.setText("☐ Select All")
                selection_badge.setToolTip("Click to select all items")
            else:
                # Partial selection - show count, "Deselect All" on hover
                selection_badge.setText(f"✓ {selected_count}/{total_items} selected")
                selection_badge.setToolTip("Click to deselect all items")
            
            selection_badge.setVisible(True)
            
            # Force style update without resizing
            selection_badge.style().unpolish(selection_badge)
            selection_badge.style().polish(selection_badge)
            selection_badge.update()
    
    def update_selection_summary(self):
        """Update the selection summary on dashboard"""
        total_size = 0
        total_items = 0
        
        for category_items in self.selected_items.values():
            for item in category_items.values():
                if item['selected']:
                    total_items += 1
                    total_size += item['data'].get('size', 0)
        
        if total_items > 0:
            size_str = self.format_size(total_size)
            self.selected_summary.setText(
                f"Selected: {total_items} items • {size_str}"
            )
            self.selected_summary.setVisible(True)
            self.clean_button.setEnabled(True)
        else:
            self.selected_summary.setText("No items selected")
            self.selected_summary.setVisible(True)
            self.clean_button.setEnabled(False)
        
        # Update header badge and category buttons
        self.update_header_selection_badge()
        self.update_category_clean_buttons()
    
    def update_header_selection_badge(self):
        """Update the header selection badge with selected items summary"""
        # Don't show badge on Dashboard (index 0) or About (index 8)
        current_index = self.stacked_widget.currentIndex()
        if current_index == 0 or current_index == 8:
            self.header_selection_badge.setVisible(False)
            return
        
        total_items = 0
        selected_items = 0
        selected_size = 0
        
        for category_items in self.selected_items.values():
            for item in category_items.values():
                total_items += 1
                if item['selected']:
                    selected_items += 1
                    # Get size from the item data
                    item_data = item.get('data', {})
                    selected_size += item_data.get('size', 0)
        
        if selected_items == 0:
            self.header_selection_badge.setVisible(False)
        else:
            from humanize import naturalsize
            size_str = naturalsize(selected_size, binary=True)
            self.header_selection_badge.setText(f"✓ {selected_items} selected • {size_str}")
            self.header_selection_badge.setVisible(True)
    
    def update_category_clean_buttons(self):
        """Update header clean button visibility based on current category"""
        # This method is now simpler - just update the header clean button
        self.update_header_clean_button_visibility()
    
    def update_header_clean_button_visibility(self):
        """Update the header clean button visibility for current category"""
        # Only show on category pages (not Dashboard or About)
        current_index = self.stacked_widget.currentIndex()
        
        # Dashboard = 0, About = 8, Categories = 1-7
        if current_index == 0 or current_index == 8:
            self.header_clean_button.setVisible(False)
            return
        
        # Check if current category has selected items
        if hasattr(self, 'current_category') and self.current_category:
            selected_count = 0
            if self.current_category in self.selected_items:
                for item in self.selected_items[self.current_category].values():
                    if item['selected']:
                        selected_count += 1
            
            self.header_clean_button.setVisible(selected_count > 0)
        else:
            self.header_clean_button.setVisible(False)
    
    def on_header_clean_clicked(self):
        """Handle header clean button click - cleans current category"""
        if not hasattr(self, 'current_category') or not self.current_category:
            return
        
        # Build selected items dict for current category only
        selected_for_cleaning = {}
        
        if self.current_category in self.selected_items:
            selected_items = []
            for item_data in self.selected_items[self.current_category].values():
                if item_data['selected']:
                    selected_items.append(item_data['data'])
            
            if selected_items:
                selected_for_cleaning[self.current_category] = selected_items
        
        if selected_for_cleaning:
            self.clean_requested.emit(selected_for_cleaning)
    
    def on_clean_button_clicked(self):
        """Handle clean button click"""
        # Build selected items dict
        selected_for_cleaning = {}
        
        for category_name, items in self.selected_items.items():
            selected_items = []
            for item_data in items.values():
                if item_data['selected']:
                    selected_items.append(item_data['data'])
            
            if selected_items:
                selected_for_cleaning[category_name] = selected_items
        
        if selected_for_cleaning:
            self.clean_requested.emit(selected_for_cleaning)
    
    def show_clean_button(self, visible=True):
        """Show or hide the clean button on dashboard"""
        self.clean_button.setVisible(visible)
        if visible:
            self.update_selection_summary()
            self.update_header_selection_badge()
            self.update_category_clean_buttons()
        else:
            self.selected_summary.setVisible(False)
            self.header_selection_badge.setVisible(False)
    
    def format_size(self, size_bytes):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def show_progress(self, visible=True):
        """Show or hide progress indicators"""
        self.progress_bar.setVisible(visible)
        self.status_label.setVisible(visible)
    
    def set_progress(self, percentage, message):
        """Update progress bar and message"""
        self.progress_bar.setValue(percentage)
        self.status_label.setText(message)
    
    def enable_buttons(self, scan_enabled=True, clean_enabled=False):
        """Enable or disable action buttons"""
        self.scan_button.setEnabled(scan_enabled)
        # Clean button visibility controlled separately
    
    def store_scan_results(self, results):
        """Store scan results for later use"""
        self.scan_results = results
    
    def eventFilter(self, obj, event):
        """Event filter for hover effects on selection badges"""
        # Check if this is a selection badge button
        if isinstance(obj, QPushButton) and obj.objectName().startswith("selectionBadge_"):
            state = obj.property("selectionState")
            selected_count = obj.property("selectedCount") or 0
            total_items = obj.property("totalItems") or 0
            
            if event.type() == QEvent.Enter:  # Mouse enters
                # Change text to show action on hover
                if state == "all":
                    obj.setText("☐ Deselect All")
                elif state == "none":
                    obj.setText("☑️ Select All")
                elif state == "partial":
                    obj.setText("☐ Deselect All")
                
                # Update style only, no resize
                obj.style().unpolish(obj)
                obj.style().polish(obj)
                    
            elif event.type() == QEvent.Leave:  # Mouse leaves
                # Restore original text
                if state == "all":
                    obj.setText("✓ All selected")
                elif state == "none":
                    obj.setText("☐ Select All")
                elif state == "partial":
                    obj.setText(f"✓ {selected_count}/{total_items} selected")
                
                # Update style only, no resize
                obj.style().unpolish(obj)
                obj.style().polish(obj)
        
        # Call base class implementation
        return super().eventFilter(obj, event)
