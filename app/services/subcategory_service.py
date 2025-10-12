"""
Subcategory Service - Business logic for managing subcategorized items
Follows Single Responsibility Principle
"""

from typing import List, Dict, Optional
from collections import defaultdict


class SubcategoryService:
    """
    Service for organizing and managing items by subcategory.
    This service is framework-agnostic and can be used by any UI layer.
    """
    
    @staticmethod
    def group_items_by_subcategory(items: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Group items by their 'subcategory' field.
        Returns a dictionary mapping subcategory names to lists of items.
        """
        grouped = defaultdict(list)
        
        for item in items:
            subcategory = item.get('subcategory', 'General')
            grouped[subcategory].append(item)
        
        return dict(grouped)
    
    @staticmethod
    def has_subcategories(items: List[Dict]) -> bool:
        """
        Check if items have meaningful subcategories.
        Returns True if there are multiple subcategories or if items explicitly define subcategories.
        """
        if not items:
            return False
        
        subcategories = set(item.get('subcategory') for item in items if item.get('subcategory'))
        return len(subcategories) > 1
    
    @staticmethod
    def get_subcategory_summary(items: List[Dict], subcategory_name: str) -> Dict:
        """
        Get summary statistics for a specific subcategory.
        Returns dict with item_count, total_size, etc.
        """
        subcategory_items = [
            item for item in items 
            if item.get('subcategory') == subcategory_name
        ]
        
        total_size = sum(item.get('size', 0) for item in subcategory_items)
        
        return {
            'name': subcategory_name,
            'item_count': len(subcategory_items),
            'total_size': total_size,
            'items': subcategory_items
        }
    
    @staticmethod
    def calculate_total_size(items: List[Dict]) -> int:
        """Calculate total size of all items"""
        return sum(item.get('size', 0) for item in items)
    
    @staticmethod
    def filter_selected_items(items_dict: Dict[int, Dict]) -> List[Dict]:
        """
        Filter items dictionary to get only selected items.
        Expects dict format: {idx: {'selected': bool, 'data': dict}}
        """
        return [
            item_info['data'] 
            for item_info in items_dict.values() 
            if item_info.get('selected', False)
        ]
