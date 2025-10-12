"""
Main Window UI Component
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QListWidget, QListWidgetItem,
    QFrame, QProgressBar, QStackedWidget, QCheckBox, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class MainWindow(QMainWindow):
    """Main window for Echo Clear"""
    
    # Signals
    scan_requested = Signal()
    clean_requested = Signal(dict)  # Pass selected items
    
    def __init__(self):
        super().__init__()
        self.scan_results = None
        self.selected_items = {}
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
        
        # Logo/Title
        title = QLabel("Echo Clear")
        title.setObjectName("appTitle")
        title_font = QFont("Inter", 24, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("System Cleaner")
        subtitle.setObjectName("appSubtitle")
        subtitle_font = QFont("Inter", 12)
        subtitle.setFont(subtitle_font)
        layout.addWidget(subtitle)
        
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
            ("⚙️", "Settings")
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
        
        # Settings view (index 8)
        settings = self.create_settings_view()
        self.stacked_widget.addWidget(settings)
        
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
        
        # Clean button (hidden by default, shown after scan)
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
            
            #appSubtitle {
                color: #86868b;
                margin-bottom: 0px;
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
                    stop:0 rgba(0, 122, 255, 0.1),
                    stop:1 rgba(0, 122, 255, 0.03));
                border-left: 4px solid #007aff;
                border-radius: 10px;
                margin: 10px 0px 6px 0px;
            }
            
            #subcategoryName {
                color: #1d1d1f;
                font-weight: 600;
            }
            
            #subcategoryCount {
                color: #007aff;
                background-color: rgba(0, 122, 255, 0.15);
                padding: 6px 16px;
                border-radius: 14px;
                font-weight: 500;
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
            "Settings"
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
        
        # Header with title and select all button
        header_layout = QHBoxLayout()
        
        items_label = QLabel("Items to Clean")
        items_label.setObjectName("welcomeTitle")
        items_label_font = QFont("Inter", 16, QFont.Medium)
        items_label.setFont(items_label_font)
        header_layout.addWidget(items_label)
        
        header_layout.addStretch()
        
        # Select All / Deselect All button
        select_all_btn = QPushButton("Select All")
        select_all_btn.setObjectName(f"selectAllBtn_{category_name}")
        select_all_btn.setMinimumSize(120, 35)
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
    
    def create_settings_view(self):
        """Create settings view"""
        view = QFrame()
        view.setObjectName("settingsView")
        
        layout = QVBoxLayout(view)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(25)
        
        # Title
        title = QLabel("Settings")
        title.setObjectName("welcomeTitle")
        title_font = QFont("Inter", 20, QFont.Medium)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Description
        description = QLabel(
            "Settings and preferences will be available in a future version."
        )
        description.setObjectName("description")
        description.setWordWrap(True)
        desc_font = QFont("Inter", 11)
        description.setFont(desc_font)
        layout.addWidget(description)
        
        layout.addStretch()
        
        return view
    
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
        """Update a category view with scan results - organized by subcategory"""
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
        else:
            info_label.setVisible(False)
            
            # Group items by subcategory
            subcategories = {}
            for item_data in items:
                subcat = item_data.get('subcategory', 'General')
                if subcat not in subcategories:
                    subcategories[subcat] = []
                subcategories[subcat].append(item_data)
            
            # If only one subcategory (or no subcategories), show items directly
            if len(subcategories) <= 1:
                idx = 0
                for item_data in items:
                    item_widget = self.create_item_checkbox(category_name, idx, item_data)
                    layout.addWidget(item_widget)
                    
                    # Select by default
                    self.selected_items[category_name][idx] = {
                        'selected': True,
                        'data': item_data
                    }
                    idx += 1
            else:
                # Show subcategory headers and items
                idx = 0
                for subcat_name in sorted(subcategories.keys()):
                    subcat_items = subcategories[subcat_name]
                    
                    # Subcategory header
                    subcat_header = self.create_subcategory_header(subcat_name, len(subcat_items))
                    layout.addWidget(subcat_header)
                    
                    # Items in subcategory
                    for item_data in subcat_items:
                        item_widget = self.create_item_checkbox(category_name, idx, item_data)
                        layout.addWidget(item_widget)
                        
                        # Select by default
                        self.selected_items[category_name][idx] = {
                            'selected': True,
                            'data': item_data
                        }
                        idx += 1
                    
                    # Add spacing between subcategories
                    spacing_widget = QWidget()
                    spacing_widget.setFixedHeight(10)
                    layout.addWidget(spacing_widget)
            
            layout.addStretch()
        
        self.update_selection_summary()
    
    def create_subcategory_header(self, subcat_name, item_count):
        """Create a subcategory header widget"""
        header_frame = QFrame()
        header_frame.setObjectName("subcategoryHeader")
        header_frame.setMinimumHeight(50)
        header_frame.setMaximumHeight(50)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(18, 12, 18, 12)
        
        # Icon and name
        name_label = QLabel(f"📂 {subcat_name}")
        name_label.setObjectName("subcategoryName")
        name_font = QFont("Inter", 14, QFont.DemiBold)
        name_label.setFont(name_font)
        header_layout.addWidget(name_label)
        
        header_layout.addStretch()
        
        # Item count badge
        count_text = f"{item_count} item" if item_count == 1 else f"{item_count} items"
        count_label = QLabel(count_text)
        count_label.setObjectName("subcategoryCount")
        count_font = QFont("Inter", 12, QFont.Medium)
        count_label.setFont(count_font)
        header_layout.addWidget(count_label)
        
        return header_frame
    
    def create_item_checkbox(self, category_name, item_idx, item_data):
        """Create a checkbox item widget"""
        item_frame = QFrame()
        item_frame.setObjectName("itemCheckboxFrame")
        item_frame.setMinimumHeight(70)
        item_frame.setMaximumHeight(100)
        
        item_layout = QHBoxLayout(item_frame)
        item_layout.setContentsMargins(15, 12, 15, 12)
        
        # Checkbox
        checkbox = QCheckBox()
        checkbox.setObjectName(f"checkbox_{category_name}_{item_idx}")
        checkbox.setChecked(True)  # Selected by default
        checkbox.setCursor(Qt.PointingHandCursor)
        checkbox.stateChanged.connect(lambda state: self.on_item_selection_changed(category_name, item_idx, state == Qt.Checked))
        item_layout.addWidget(checkbox)
        
        # Item info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        name = item_data.get('name', 'Unknown')
        name_label = QLabel(name)
        name_label.setObjectName("itemName")
        name_label.setWordWrap(False)
        name_font = QFont("Inter", 12, QFont.Medium)
        name_label.setFont(name_font)
        info_layout.addWidget(name_label)
        
        # Details
        size = item_data.get('size', 0)
        size_str = self.format_size(size)
        path = item_data.get('path', '')
        
        details_label = QLabel(f"{size_str}")
        if path and len(path) < 100:
            details_label.setText(f"{size_str} • {path}")
        
        details_label.setObjectName("itemDetails")
        details_label.setWordWrap(False)
        details_font = QFont("Inter", 10)
        details_label.setFont(details_font)
        info_layout.addWidget(details_label)
        
        item_layout.addLayout(info_layout, 1)
        
        return item_frame
    
    def on_item_selection_changed(self, category_name, item_idx, is_checked):
        """Handle individual item selection change"""
        if category_name in self.selected_items and item_idx in self.selected_items[category_name]:
            self.selected_items[category_name][item_idx]['selected'] = is_checked
            self.update_selection_summary()
    
    def toggle_select_all(self, category_name):
        """Toggle select all items in a category"""
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
        )
        
        # Toggle all
        new_state = not all_selected
        
        for item_idx in self.selected_items[category_name]:
            self.selected_items[category_name][item_idx]['selected'] = new_state
            
            # Update checkbox UI
            checkbox = items_container.findChild(QCheckBox, f"checkbox_{category_name}_{item_idx}")
            if checkbox:
                checkbox.setChecked(new_state)
        
        # Update button text
        select_all_btn = view.findChild(QPushButton, f"selectAllBtn_{category_name}")
        if select_all_btn:
            select_all_btn.setText("Deselect All" if new_state else "Select All")
        
        self.update_selection_summary()
    
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
