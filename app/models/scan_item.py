"""
Scan Item Models - Data structures for scanned items
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ScanItem:
    """Represents a single scanned item"""
    
    name: str
    path: str
    size: int
    item_type: str
    details: str = ""
    subcategory: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for backward compatibility"""
        return {
            'name': self.name,
            'path': self.path,
            'size': self.size,
            'type': self.item_type,
            'details': self.details,
            'subcategory': self.subcategory,
            **self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ScanItem':
        """Create from dictionary"""
        return cls(
            name=data.get('name', 'Unknown'),
            path=data.get('path', ''),
            size=data.get('size', 0),
            item_type=data.get('type', 'unknown'),
            details=data.get('details', ''),
            subcategory=data.get('subcategory'),
            metadata={k: v for k, v in data.items() 
                     if k not in ['name', 'path', 'size', 'type', 'details', 'subcategory']}
        )


@dataclass
class SubcategoryGroup:
    """Represents a group of items within a subcategory"""
    
    name: str
    items: List[ScanItem]
    icon: str = "📂"
    description: str = ""
    
    @property
    def total_size(self) -> int:
        """Calculate total size of all items in this subcategory"""
        return sum(item.size for item in self.items)
    
    @property
    def item_count(self) -> int:
        """Get number of items in this subcategory"""
        return len(self.items)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'icon': self.icon,
            'description': self.description,
            'items': [item.to_dict() for item in self.items],
            'total_size': self.total_size,
            'item_count': self.item_count
        }
    
    @classmethod
    def group_items_by_subcategory(cls, items: List[Dict]) -> List['SubcategoryGroup']:
        """
        Group a list of items by their subcategory.
        Returns a list of SubcategoryGroup objects.
        """
        groups_dict = {}
        
        for item_data in items:
            scan_item = ScanItem.from_dict(item_data)
            subcat_name = scan_item.subcategory or 'General'
            
            if subcat_name not in groups_dict:
                groups_dict[subcat_name] = []
            
            groups_dict[subcat_name].append(scan_item)
        
        # Create SubcategoryGroup objects
        groups = []
        for subcat_name in sorted(groups_dict.keys()):
            group = cls(
                name=subcat_name,
                items=groups_dict[subcat_name]
            )
            groups.append(group)
        
        return groups
