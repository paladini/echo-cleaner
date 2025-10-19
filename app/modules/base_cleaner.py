"""
Base Cleaner - Abstract base class for all cleaning modules
"""

from abc import ABC, abstractmethod
from typing import List, Dict
import os
import shutil
import subprocess


class BaseCleaner(ABC):
    """
    Abstract base class for all cleaning modules.
    Follows the Single Responsibility Principle.
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def scan(self) -> List[Dict]:
        """
        Scan and return items that can be cleaned.
        
        Returns:
            List of dictionaries with 'path', 'size', and optional metadata
        """
        pass
    
    @abstractmethod
    def clean(self, items: List[Dict]) -> int:
        """
        Clean the specified items.
        
        Args:
            items: List of items to clean (from scan results)
        
        Returns:
            Total size cleaned in bytes
        """
        pass
    
    def get_directory_size(self, path: str) -> int:
        """Calculate total size of a directory"""
        total_size = 0
        try:
            if os.path.isfile(path):
                return os.path.getsize(path)
            
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        continue
        except (OSError, FileNotFoundError):
            pass
        
        return total_size
    
    def safe_remove(self, path: str) -> bool:
        """Safely remove a file or directory"""
        try:
            if os.path.isfile(path):
                os.remove(path)
                return True
            elif os.path.isdir(path):
                shutil.rmtree(path)
                return True
        except (OSError, PermissionError) as e:
            print(f"Error removing {path}: {e}")
            return False
        
        return False
    
    def run_command(self, command: List[str], check: bool = False, use_sudo: bool = False) -> subprocess.CompletedProcess:
        """
        Safely run a shell command.
        
        Args:
            command: Command as list of strings
            check: Whether to raise exception on non-zero exit
            use_sudo: Whether to run with elevated privileges using pkexec
        
        Returns:
            CompletedProcess object
        """
        try:
            # If sudo is needed, prepend pkexec (graphical sudo alternative)
            if use_sudo:
                # Check if pkexec is available
                if shutil.which('pkexec'):
                    command = ['pkexec'] + command
                # Fallback to sudo if pkexec not available
                elif shutil.which('sudo'):
                    command = ['sudo', '-n'] + command  # -n = non-interactive
                else:
                    print(f"Warning: No privilege escalation tool available for: {' '.join(command)}")
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=check,
                timeout=60  # Increased timeout for sudo operations
            )
            return result
        except subprocess.TimeoutExpired:
            print(f"Command timed out: {' '.join(command)}")
            return subprocess.CompletedProcess(command, -1, '', 'Timeout')
        except Exception as e:
            print(f"Error running command: {e}")
            return subprocess.CompletedProcess(command, -1, '', str(e))
    
    def is_command_available(self, command: str) -> bool:
        """Check if a command is available in the system"""
        return shutil.which(command) is not None
