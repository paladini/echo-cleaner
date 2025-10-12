# Contributing to Echo Clear

Thank you for your interest in contributing to Echo Clear! 🎉

## Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/echo-clear.git
   cd echo-clear
   ```

3. **Set up the development environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Architecture Overview

Echo Clear follows a **layered architecture** based on SOLID principles:

### 1. Presentation Layer (`app/ui/`)
- Contains all UI components
- No business logic
- Emits signals for user actions

### 2. Service Layer (`app/services/`)
- Contains business logic
- Orchestrates cleaning operations
- UI-agnostic (could be used with CLI)

### 3. System Access Layer (`app/modules/`)
- Individual cleaning modules
- Each module has a single responsibility
- Extends `BaseCleaner` abstract class

## Adding a New Cleaner Module

To add a new cleaning module:

1. **Create a new file** in `app/modules/`:
   ```python
   """
   Your Cleaner - Description
   """
   
   from typing import List, Dict
   from .base_cleaner import BaseCleaner
   
   class YourCleaner(BaseCleaner):
       """Your cleaner description"""
       
       def __init__(self):
           super().__init__(
               name="Your Cleaner",
               description="What it cleans"
           )
       
       def scan(self) -> List[Dict]:
           """Scan for items to clean"""
           items = []
           # Your scan logic here
           return items
       
       def clean(self, items: List[Dict]) -> int:
           """Clean the items"""
           total_cleaned = 0
           # Your cleaning logic here
           return total_cleaned
   ```

2. **Register it** in `app/modules/__init__.py`:
   ```python
   from .your_cleaner import YourCleaner
   
   __all__ = [
       # ... existing cleaners ...
       'YourCleaner'
   ]
   ```

3. **Add it to the service** in `app/main.py`:
   ```python
   from modules import (
       # ... existing imports ...
       YourCleaner
   )
   
   # In setup_cleaners():
   self.service.register_cleaner(YourCleaner())
   ```

## Code Style

- Follow **PEP 8** style guide
- Use **type hints** where possible
- Write **docstrings** for all classes and methods
- Keep functions small and focused (SRP)

## Testing

Before submitting a PR:

1. Test your changes manually
2. Ensure no regressions in existing functionality
3. Test on different Linux distributions if possible

## Pull Request Process

1. Update the README.md if you add new features
2. Update the CHANGELOG.md with your changes
3. Ensure your code follows the project's code style
4. Write a clear PR description explaining your changes

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about architecture
- Help with development

Thank you for contributing! 🙌
