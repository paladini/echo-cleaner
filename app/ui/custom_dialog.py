"""
Custom Dialog - Beautiful macOS-style dialogs
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor


class CustomDialog(QDialog):
    """Beautiful custom dialog with macOS-inspired design"""
    
    def __init__(self, parent=None, title="", message="", icon_type="info"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedWidth(480)
        
        # Remove window frame for custom look
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setup_ui(title, message, icon_type)
    
    def setup_ui(self, title, message, icon_type):
        """Setup the dialog UI"""
        # Main container with rounded corners
        container = QFrame(self)
        container.setObjectName("dialogContainer")
        
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        # Icon
        icon_label = QLabel()
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_emoji = self.get_icon_emoji(icon_type)
        icon_label.setText(icon_emoji)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 36px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.1),
                    stop:1 rgba(255, 255, 255, 0.05));
                border-radius: 24px;
                padding: 0px;
            }
        """)
        header_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("dialogTitle")
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label, 1)
        
        main_layout.addLayout(header_layout)
        
        # Message
        message_label = QLabel(message)
        message_label.setObjectName("dialogMessage")
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        main_layout.addWidget(message_label)
        
        # Button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_button = QPushButton("Got it!")
        ok_button.setObjectName("dialogButton")
        ok_button.setCursor(Qt.PointingHandCursor)
        ok_button.setFixedSize(140, 40)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        main_layout.addLayout(button_layout)
        
        # Set the container as the main widget
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(container)
        
        self.apply_styles()
    
    def get_icon_emoji(self, icon_type):
        """Get emoji icon based on type"""
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "sparkles": "✨",
            "search": "🔍"
        }
        return icons.get(icon_type, "ℹ️")
    
    def apply_styles(self):
        """Apply custom styles"""
        self.setStyleSheet("""
            #dialogContainer {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff,
                    stop:1 #f8f9fa);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 16px;
            }
            
            #dialogTitle {
                font-size: 22px;
                font-weight: 600;
                color: #1a1a1a;
                padding: 0px;
            }
            
            #dialogMessage {
                font-size: 14px;
                color: #4a4a4a;
                line-height: 1.6;
                padding: 8px 0px;
            }
            
            #dialogButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007AFF,
                    stop:1 #0051D5);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 24px;
            }
            
            #dialogButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0051D5,
                    stop:1 #003DA5);
            }
            
            #dialogButton:pressed {
                background: #003DA5;
            }
        """)


class ConfirmDialog(QDialog):
    """Beautiful confirmation dialog with Yes/No options"""
    
    def __init__(self, parent=None, title="", message="", icon_type="warning"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedWidth(480)
        
        # Remove window frame for custom look
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setup_ui(title, message, icon_type)
    
    def setup_ui(self, title, message, icon_type):
        """Setup the dialog UI"""
        # Main container with rounded corners
        container = QFrame(self)
        container.setObjectName("dialogContainer")
        
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        # Icon
        icon_label = QLabel()
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_emoji = self.get_icon_emoji(icon_type)
        icon_label.setText(icon_emoji)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 36px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 165, 0, 0.15),
                    stop:1 rgba(255, 165, 0, 0.05));
                border-radius: 24px;
                padding: 0px;
            }
        """)
        header_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("dialogTitle")
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label, 1)
        
        main_layout.addLayout(header_layout)
        
        # Message
        message_label = QLabel(message)
        message_label.setObjectName("dialogMessage")
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        main_layout.addWidget(message_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("cancelButton")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.setFixedSize(120, 40)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        confirm_button = QPushButton("Continue")
        confirm_button.setObjectName("confirmButton")
        confirm_button.setCursor(Qt.PointingHandCursor)
        confirm_button.setFixedSize(120, 40)
        confirm_button.clicked.connect(self.accept)
        button_layout.addWidget(confirm_button)
        
        main_layout.addLayout(button_layout)
        
        # Set the container as the main widget
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(container)
        
        self.apply_styles()
    
    def get_icon_emoji(self, icon_type):
        """Get emoji icon based on type"""
        icons = {
            "warning": "⚠️",
            "question": "❓",
            "danger": "🚨"
        }
        return icons.get(icon_type, "❓")
    
    def apply_styles(self):
        """Apply custom styles"""
        self.setStyleSheet("""
            #dialogContainer {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff,
                    stop:1 #f8f9fa);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 16px;
            }
            
            #dialogTitle {
                font-size: 22px;
                font-weight: 600;
                color: #1a1a1a;
                padding: 0px;
            }
            
            #dialogMessage {
                font-size: 14px;
                color: #4a4a4a;
                line-height: 1.6;
                padding: 8px 0px;
            }
            
            #cancelButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f5f5f5,
                    stop:1 #e8e8e8);
                color: #333333;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                font-size: 14px;
                font-weight: 500;
                padding: 0px 20px;
            }
            
            #cancelButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e8e8e8,
                    stop:1 #d8d8d8);
            }
            
            #cancelButton:pressed {
                background: #d8d8d8;
            }
            
            #confirmButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FF3B30,
                    stop:1 #D32F2F);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
                padding: 0px 20px;
            }
            
            #confirmButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #D32F2F,
                    stop:1 #B71C1C);
            }
            
            #confirmButton:pressed {
                background: #B71C1C;
            }
        """)
