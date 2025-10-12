"""
Kubernetes Cleaner - Cleans local Kubernetes caches
"""

from pathlib import Path
from typing import List, Dict
from .base_cleaner import BaseCleaner


class KubernetesCleaner(BaseCleaner):
    """Cleans Kubernetes local cluster caches (minikube, kind, etc.)"""
    
    def __init__(self):
        super().__init__(
            name="Kubernetes",
            description="Local Kubernetes cluster caches"
        )
    
    def scan(self) -> List[Dict]:
        """Scan for Kubernetes caches"""
        items = []
        
        home = Path.home()
        
        # Minikube cache
        minikube_cache = home / ".minikube" / "cache"
        if minikube_cache.exists():
            size = self.get_directory_size(str(minikube_cache))
            if size > 0:
                items.append({
                    'path': str(minikube_cache),
                    'name': 'Minikube Cache',
                    'size': size,
                    'type': 'minikube_cache'
                })
        
        # kind cache
        kind_cache = home / ".kind"
        if kind_cache.exists():
            size = self.get_directory_size(str(kind_cache))
            if size > 0:
                items.append({
                    'path': str(kind_cache),
                    'name': 'kind Cache',
                    'size': size,
                    'type': 'kind_cache'
                })
        
        # kubectl cache
        kubectl_cache = home / ".kube" / "cache"
        if kubectl_cache.exists():
            size = self.get_directory_size(str(kubectl_cache))
            if size > 0:
                items.append({
                    'path': str(kubectl_cache),
                    'name': 'kubectl Cache',
                    'size': size,
                    'type': 'kubectl_cache'
                })
        
        # Helm cache
        helm_cache = home / ".cache" / "helm"
        if helm_cache.exists():
            size = self.get_directory_size(str(helm_cache))
            if size > 0:
                items.append({
                    'path': str(helm_cache),
                    'name': 'Helm Cache',
                    'size': size,
                    'type': 'helm_cache'
                })
        
        return items
    
    def clean(self, items: List[Dict]) -> int:
        """Clean Kubernetes caches"""
        total_cleaned = 0
        
        for item in items:
            path = item['path']
            size = item['size']
            
            if self.safe_remove(path):
                total_cleaned += size
        
        return total_cleaned
