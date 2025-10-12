"""
Subcategory Widget - Reusable component for displaying subcategorized items
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QCheckBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from typing import List, Dict, Callable


class SubcategoryHeaderWidget(QFrame):
    """Reusable subcategory header widget"""
    
    def __init__(self, name: str, item_count: int, icon: str = "📂", parent=None):
        super().__init__(parent)
        self.setObjectName("subcategoryHeader")
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)
        
        self._setup_ui(name, item_count, icon)
    
    def _setup_ui(self, name: str, item_count: int, icon: str):
        """Setup the header UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(12)
        
        # Icon and name
        name_label = QLabel(f"{icon} {name}")
        name_label.setObjectName("subcategoryName")
        name_font = QFont("Inter", 12, QFont.DemiBold)
        name_label.setFont(name_font)
        layout.addWidget(name_label)
        
        layout.addStretch()
        
        # Item count badge
        count_text = f"{item_count} item" if item_count == 1 else f"{item_count} items"
        count_label = QLabel(count_text)
        count_label.setObjectName("subcategoryCount")
        count_label.setAlignment(Qt.AlignCenter)
        count_font = QFont("Inter", 10, QFont.Medium)
        count_label.setFont(count_font)
        count_label.setFixedHeight(24)
        count_label.setMinimumWidth(65)
        layout.addWidget(count_label)


class ItemCheckboxWidget(QFrame):
    """Reusable item checkbox widget following Single Responsibility Principle"""
    
    selection_changed = Signal(bool)  # Emits when checkbox state changes
    
    def __init__(self, item_data: Dict, item_id: str, parent=None):
        super().__init__(parent)
        self.item_data = item_data
        self.item_id = item_id
        self.setObjectName("itemCheckboxFrame")
        self.setMinimumHeight(65)
        self.setMaximumHeight(65)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the item UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(12)
        
        # Checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setObjectName(f"checkbox_{self.item_id}")
        self.checkbox.setChecked(True)  # Selected by default
        self.checkbox.setCursor(Qt.PointingHandCursor)
        self.checkbox.stateChanged.connect(
            lambda state: self.selection_changed.emit(state == Qt.Checked)
        )
        layout.addWidget(self.checkbox)
        
        # Item info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        # Name
        name = self.item_data.get('name', 'Unknown')
        name_label = QLabel(name)
        name_label.setObjectName("itemName")
        name_label.setWordWrap(False)
        name_font = QFont("Inter", 11, QFont.Medium)
        name_label.setFont(name_font)
        info_layout.addWidget(name_label)
        
        # Details
        details_label = self._create_details_label()
        info_layout.addWidget(details_label)
        
        layout.addLayout(info_layout, 1)
    
    def _create_details_label(self) -> QLabel:
        """Create the details label with size and path info"""
        size = self.item_data.get('size', 0)
        size_str = self._format_size(size)
        path = self.item_data.get('path', '')
        details_text = self.item_data.get('details', '')
        
        # Build details string
        parts = [size_str]
        if details_text:
            parts.append(details_text)
        elif path and len(path) < 100:
            parts.append(path)
        
        details_label = QLabel(" • ".join(parts))
        details_label.setObjectName("itemDetails")
        details_label.setWordWrap(False)
        details_font = QFont("Inter", 9)
        details_label.setFont(details_font)
        
        return details_label
    
    def _format_size(self, size_bytes: int) -> str:
        """Format size in bytes to human-readable string"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                if unit == 'B':
                    return f"{int(size_bytes)} {unit}"
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def is_selected(self) -> bool:
        """Check if item is selected"""
        return self.checkbox.isChecked()
    
    def set_selected(self, selected: bool):
        """Set selection state"""
        self.checkbox.setChecked(selected)


class SubcategoryGroupWidget(QWidget):
    """
    Reusable widget for displaying a group of items under a subcategory.
    Follows Open/Closed Principle - open for extension, closed for modification.
    """
    
    def __init__(self, subcategory_name: str, items: List[Dict], 
                 category_name: str, item_id_generator: Callable[[int], str],
                 parent=None):
        super().__init__(parent)
        self.subcategory_name = subcategory_name
        self.items = items
        self.category_name = category_name
        self.item_id_generator = item_id_generator
        self.item_widgets = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the group UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Add header
        header = SubcategoryHeaderWidget(self.subcategory_name, len(self.items))
        layout.addWidget(header)
        
        # Add items
        for idx, item_data in enumerate(self.items):
            item_id = self.item_id_generator(idx)
            item_widget = ItemCheckboxWidget(item_data, item_id)
            self.item_widgets.append(item_widget)
            layout.addWidget(item_widget)
        
        # Add spacing after group
        spacing = QWidget()
        spacing.setFixedHeight(10)
        layout.addWidget(spacing)
    
    def get_selected_items(self) -> List[Dict]:
        """Get all selected items in this subcategory"""
        return [
            widget.item_data 
            for widget in self.item_widgets 
            if widget.is_selected()
        ]
    
    def select_all(self, selected: bool = True):
        """Select or deselect all items in this subcategory"""
        for widget in self.item_widgets:
            widget.set_selected(selected)
