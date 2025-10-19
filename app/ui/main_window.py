"""
Main Window UI Component
"""

from typing import List, Dict
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QListWidget, QListWidgetItem,
    QFrame, QProgressBar, QStackedWidget, QCheckBox, QScrollArea, QApplication
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from .subcategory_widget import SubcategoryGroupWidget, ItemCheckboxWidget
from services.subcategory_service import SubcategoryService


class MainWindow(QMainWindow):
    """Main window for Echo Clear"""
    
    # Signals
    scan_requested = Signal()
    clean_requested = Signal(dict)  # Pass selected items
    
    def __init__(self):
        super().__init__()
        self.scan_results = None
        self.selected_items = {}
        self.subcategory_service = SubcategoryService()
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """Initialize the main window interface"""
        # Window settings
        self.setWindowTitle("Echo Clear - Intelligent System Cleaner")
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
        
        # Logo/Icon placeholder
        logo_container = QFrame()
        logo_container.setObjectName("logoContainer")
        logo_container.setFixedSize(80, 80)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignCenter)
        
        # Logo icon (using emoji as placeholder until you add a real icon)
        logo_icon = QLabel("✨")
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_icon.setStyleSheet("font-size: 48px;")
        logo_layout.addWidget(logo_icon)
        
        layout.addWidget(logo_container, 0, Qt.AlignHCenter)
        layout.addSpacing(10)
        
        # App Title
        title = QLabel("Echo Clear")
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
        version = QLabel("v0.1.0")
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
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        self.page_title = QLabel("Dashboard")
        self.page_title.setObjectName("pageTitle")
        title_font = QFont("Inter", 28, QFont.Bold)
        self.page_title.setFont(title_font)
        layout.addWidget(self.page_title)
        
        layout.addStretch()
        
        # Action buttons
        self.scan_button = QPushButton("🔍 Scan System")
        self.scan_button.setObjectName("scanButton")
        self.scan_button.setMinimumSize(160, 50)
        scan_font = QFont("Inter", 13, QFont.Medium)
        self.scan_button.setFont(scan_font)
        self.scan_button.setCursor(Qt.PointingHandCursor)
        self.scan_button.clicked.connect(self.scan_requested.emit)
        layout.addWidget(self.scan_button)
        
        return header
    
    def create_dashboard(self):
        """Create the dashboard view"""
        dashboard = QFrame()
        dashboard.setObjectName("dashboard")
        
        layout = QVBoxLayout(dashboard)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(25)
        
        # Welcome message
        welcome = QLabel("Welcome to Echo Clear")
        welcome.setObjectName("welcomeTitle")
        welcome_font = QFont("Inter", 20, QFont.Medium)
        welcome.setFont(welcome_font)
        layout.addWidget(welcome)
        
        description = QLabel(
            "Echo Clear helps you reclaim disk space by cleaning system cache, "
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
        
        # Action buttons container (Clean + Select/Deselect All)
        buttons_container = QWidget()
        buttons_layout = QVBoxLayout(buttons_container)
        buttons_layout.setSpacing(15)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        # Clean button (hidden by default, shown after scan)
        self.clean_button = QPushButton("🧹 Clean Selected Items")
        self.clean_button.setObjectName("cleanButton")
        self.clean_button.setMinimumSize(200, 60)
        clean_font = QFont("Inter", 15, QFont.Bold)
        self.clean_button.setFont(clean_font)
        self.clean_button.setCursor(Qt.PointingHandCursor)
        self.clean_button.setVisible(False)
        self.clean_button.clicked.connect(self.on_clean_button_clicked)
        buttons_layout.addWidget(self.clean_button, alignment=Qt.AlignCenter)
        
        # Toggle selection button (hidden by default, shown after scan)
        self.toggle_selection_button = QPushButton("☑️ Deselect All Items")
        self.toggle_selection_button.setObjectName("toggleSelectionButton")
        self.toggle_selection_button.setMinimumSize(180, 40)
        toggle_font = QFont("Inter", 12)
        self.toggle_selection_button.setFont(toggle_font)
        self.toggle_selection_button.setCursor(Qt.PointingHandCursor)
        self.toggle_selection_button.setVisible(False)
        self.toggle_selection_button.clicked.connect(self.on_toggle_all_selection)
        buttons_layout.addWidget(self.toggle_selection_button, alignment=Qt.AlignCenter)
        
        layout.addWidget(buttons_container)
        
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
            
            #logoContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 122, 255, 0.08),
                    stop:1 rgba(0, 122, 255, 0.02));
                border: 2px solid #e5e5e7;
                border-radius: 16px;
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
            
            #toggleSelectionButton, #selectAllButton, #deselectAllButton {
                background-color: #f5f5f7;
                color: #1d1d1f;
                border: 1px solid #d2d2d7;
                border-radius: 10px;
                padding: 10px 24px;
                font-weight: 500;
            }
            
            #toggleSelectionButton:hover, #selectAllButton:hover, #deselectAllButton:hover {
                background-color: #e8e8ed;
                border-color: #007aff;
            }
            
            #toggleSelectionButton:pressed, #selectAllButton:pressed, #deselectAllButton:pressed {
                background-color: #d2d2d7;
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
            
            QPushButton[objectName^="selectAllBtn_"] {
                background-color: #f5f5f7;
                color: #007aff;
                border: 1px solid #e5e5e7;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 11px;
                font-weight: 600;
            }
            
            QPushButton[objectName^="selectAllBtn_"]:hover {
                background-color: #e8e8ed;
                border-color: #007aff;
            }
            
            QPushButton[objectName^="selectAllBtn_"]:pressed {
                background-color: #d2d2d7;
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
        
        # Header with title, selection badge and button
        header_layout = QHBoxLayout()
        
        # Title
        items_label = QLabel("Items to Clean")
        items_label.setObjectName("welcomeTitle")
        items_label_font = QFont("Inter", 16, QFont.Medium)
        items_label.setFont(items_label_font)
        header_layout.addWidget(items_label)
        
        # Selection status badge
        selection_badge = QLabel("")
        selection_badge.setObjectName(f"selectionBadge_{category_name}")
        selection_badge.setVisible(False)
        badge_font = QFont("Inter", 11, QFont.Medium)
        selection_badge.setFont(badge_font)
        header_layout.addWidget(selection_badge)
        
        header_layout.addStretch()
        
        # Select All / Deselect All button
        select_all_btn = QPushButton("Select All")
        select_all_btn.setObjectName(f"selectAllBtn_{category_name}")
        select_all_btn.setMinimumSize(140, 38)
        select_all_btn.setCursor(Qt.PointingHandCursor)
        select_all_btn.clicked.connect(lambda: self.toggle_select_all(category_name))
        header_layout.addWidget(select_all_btn)
        
        layout.addLayout(header_layout)
        
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
        
        # Info label
        info_label = QLabel("Run a scan to see items in this category")
        info_label.setObjectName(f"infoLabel_{category_name}")
        info_font = QFont("Inter", 10)
        info_label.setFont(info_font)
        layout.addWidget(info_label)
        
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
        version_label = QLabel("Version 0.1.0")
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
        info_label = view.findChild(QLabel, f"infoLabel_{category_name}")
        
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
            info_label.setText("✓ No items found - this category is clean!")
            info_label.setVisible(True)
            # Hide badge when no items
            selection_badge = view.findChild(QLabel, f"selectionBadge_{category_name}")
            if selection_badge:
                selection_badge.setVisible(False)
        else:
            info_label.setVisible(False)
            
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
        """Update button text and badge for a specific category"""
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
        
        # Update button text
        select_all_btn = view.findChild(QPushButton, f"selectAllBtn_{category_name}")
        if select_all_btn:
            if selected_count == total_items:
                select_all_btn.setText("☑️ Deselect All")
            elif selected_count == 0:
                select_all_btn.setText("☐ Select All")
            else:
                select_all_btn.setText("☑️ Deselect All")  # Default action when partial
        
        # Update selection badge
        selection_badge = view.findChild(QLabel, f"selectionBadge_{category_name}")
        if selection_badge:
            # Always update badge visibility and content
            if selected_count == total_items:
                # All selected - green badge
                selection_badge.setText("✓ All selected")
                selection_badge.setStyleSheet("""
                    QLabel {
                        background-color: #34C759;
                        color: white;
                        padding: 4px 12px;
                        border-radius: 12px;
                        font-weight: 500;
                    }
                """)
                selection_badge.setVisible(True)
            elif selected_count == 0:
                # None selected - gray badge
                selection_badge.setText("None selected")
                selection_badge.setStyleSheet("""
                    QLabel {
                        background-color: #8E8E93;
                        color: white;
                        padding: 4px 12px;
                        border-radius: 12px;
                        font-weight: 500;
                    }
                """)
                selection_badge.setVisible(True)
            else:
                # Partial selection - blue badge
                selection_badge.setText(f"{selected_count}/{total_items} selected")
                selection_badge.setStyleSheet("""
                    QLabel {
                        background-color: #007AFF;
                        color: white;
                        padding: 4px 12px;
                        border-radius: 12px;
                        font-weight: 500;
                    }
                """)
                selection_badge.setVisible(True)
            
            # Force widget update with proper size recalculation
            selection_badge.adjustSize()  # Recalculate size based on new text
            selection_badge.update()
            selection_badge.repaint()
            QApplication.processEvents()  # Process all pending events
    
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
        
        # Update toggle button text
        self.update_toggle_button_text()
    
    def update_toggle_button_text(self):
        """Update toggle button text based on current selection state"""
        total_items = 0
        selected_items = 0
        
        for category_items in self.selected_items.values():
            for item in category_items.values():
                total_items += 1
                if item['selected']:
                    selected_items += 1
        
        if selected_items == 0:
            # All deselected - show "Select All"
            self.toggle_selection_button.setText("☑️ Select All Items")
            self.toggle_selection_button.setObjectName("selectAllButton")
        elif selected_items == total_items:
            # All selected - show "Deselect All"
            self.toggle_selection_button.setText("☐ Deselect All Items")
            self.toggle_selection_button.setObjectName("deselectAllButton")
        else:
            # Partially selected - show "Deselect All" (default action)
            self.toggle_selection_button.setText("☐ Deselect All Items")
            self.toggle_selection_button.setObjectName("deselectAllButton")
        
        # Reapply styles
        self.toggle_selection_button.style().unpolish(self.toggle_selection_button)
        self.toggle_selection_button.style().polish(self.toggle_selection_button)
    
    def on_toggle_all_selection(self):
        """Toggle all items selection across all categories"""
        # Check current state
        total_items = 0
        selected_items = 0
        
        for category_items in self.selected_items.values():
            for item in category_items.values():
                total_items += 1
                if item['selected']:
                    selected_items += 1
        
        # Decide action: if all selected, deselect all. Otherwise, select all
        new_state = (selected_items == 0)
        
        # Apply to all items
        for category_name, category_items in self.selected_items.items():
            for item_idx in category_items.keys():
                self.selected_items[category_name][item_idx]['selected'] = new_state
        
        # Update all checkboxes in UI
        self._update_all_checkboxes(new_state)
        
        # Update visuals for all categories
        for category_name in self.selected_items.keys():
            self.update_category_selection_visuals(category_name)
        
        # Update summary
        self.update_selection_summary()
    
    def _update_all_checkboxes(self, checked: bool):
        """Update all checkbox widgets to match the new state"""
        # Find all ItemCheckboxWidget instances and update them
        for category_name, view in self.category_views.items():
            # Find all checkbox widgets in the view
            items_container = view.findChild(QWidget, f"itemsContainer_{category_name}")
            if items_container:
                checkboxes = items_container.findChildren(QCheckBox)
                for checkbox in checkboxes:
                    if checkbox.objectName().startswith("checkbox_"):
                        checkbox.blockSignals(True)  # Prevent signal spam
                        checkbox.setChecked(checked)
                        checkbox.blockSignals(False)
    
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
        """Show or hide the clean button and toggle selection button on dashboard"""
        self.clean_button.setVisible(visible)
        self.toggle_selection_button.setVisible(visible)
        if visible:
            self.update_selection_summary()
            self.update_toggle_button_text()
        else:
            self.selected_summary.setVisible(False)
    
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
