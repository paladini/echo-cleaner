# Development Guide

## 📦 Quick Start

### Install Dependencies

```bash
# Using make (recommended)
make install

# Or using pip directly
pip install -r requirements.txt
```

### Run the Application

```bash
# Using make
make run

# Or directly
python3 echo-clear.py
```

### Available Commands (like npm scripts)

```bash
make help           # Show all available commands
make install        # Install dependencies
make run            # Run the application
make build-appimage # Build AppImage for distribution
make clean          # Clean build artifacts
make test           # Run tests
make format         # Format code with black
make lint           # Lint code with flake8
```

### Dependency Management

This project uses **`pyproject.toml`** (Python's equivalent to `package.json`):

| Node.js          | Python                    |
|------------------|---------------------------|
| `package.json`   | `pyproject.toml`          |
| `npm install`    | `make install`            |
| `npm run build`  | `make build-appimage`     |
| `npm run clean`  | `make clean`              |
| `npm test`       | `make test`               |

## Project Structure

```
echo-clear/
├── app/
│   ├── ui/                    # Presentation Layer
│   │   ├── __init__.py
│   │   └── main_window.py     # Main window UI
│   ├── services/              # Service Layer (Business Logic)
│   │   ├── __init__.py
│   │   └── cleaning_service.py
│   ├── modules/               # System Access Layer
│   │   ├── __init__.py
│   │   ├── base_cleaner.py    # Abstract base class
│   │   ├── system_cache_cleaner.py
│   │   ├── trash_cleaner.py
│   │   ├── log_cleaner.py
│   │   ├── package_manager_cleaner.py
│   │   ├── docker_cleaner.py
│   │   ├── dev_dependencies_cleaner.py
│   │   └── kubernetes_cleaner.py
│   ├── assets/                # Icons, fonts, etc.
│   ├── __init__.py
│   └── main.py                # Entry point
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

## Architecture Principles

### SOLID Principles

1. **Single Responsibility Principle (SRP)**
   - Each cleaner module has one job
   - UI only handles presentation
   - Service only handles business logic

2. **Open/Closed Principle (OCP)**
   - Extend functionality by adding new cleaners
   - No need to modify existing code

3. **Liskov Substitution Principle (LSP)**
   - All cleaners extend `BaseCleaner`
   - Can be used interchangeably

4. **Interface Segregation Principle (ISP)**
   - Simple, focused interfaces
   - `scan()` and `clean()` methods

5. **Dependency Inversion Principle (DIP)**
   - Depend on abstractions (`BaseCleaner`)
   - Not on concrete implementations

## Signal-Slot Communication

Echo Cleaner uses Qt's signal-slot mechanism for communication:

```
UI Layer (MainWindow)
    ↓ (signals)
Service Layer (CleaningService)
    ↓ (orchestrates)
Module Layer (Cleaners)
    ↑ (results)
Service Layer
    ↑ (signals)
UI Layer (updates display)
```

## Threading Model

- **Main Thread**: UI operations
- **Worker Threads**: Scan and clean operations
- **QThread**: Used for background tasks
- **Signals**: Thread-safe communication

## Adding New Features

### Adding a UI Component

1. Modify `app/ui/main_window.py`
2. Use Qt Style Sheets for styling
3. Emit signals for user actions
4. Connect to service layer

### Adding a New Cleaner

See `CONTRIBUTING.md` for detailed instructions.

### Modifying the Service Layer

The `CleaningService` orchestrates all operations:
- Manages cleaner registration
- Handles threading
- Emits progress signals
- Formats results

## Testing

### Manual Testing Checklist

- [ ] UI loads without errors
- [ ] Scan completes successfully
- [ ] Progress bar updates correctly
- [ ] Statistics display correctly
- [ ] Clean operation works
- [ ] Confirmation dialogs appear
- [ ] Error handling works
- [ ] No memory leaks (long-running tests)

### Testing Individual Cleaners

```python
from modules import SystemCacheCleaner

cleaner = SystemCacheCleaner()
items = cleaner.scan()
print(f"Found {len(items)} items")

# Don't run clean() during testing!
```

## Performance Considerations

- Use `QThread` for long-running operations
- Avoid blocking the UI thread
- Calculate sizes efficiently
- Use generators for large datasets where possible

## Security Considerations

- Never execute user input as commands
- Use `subprocess.run()` with explicit arguments
- Check permissions before deleting
- Validate paths before operations
- Provide clear warnings for destructive operations

## Future Enhancements

Ideas for v2.0:
- [ ] Schedule automatic cleaning
- [ ] Custom exclusion lists
- [ ] Dry-run mode
- [ ] Detailed per-item selection
- [ ] System tray integration
- [ ] Command-line interface
- [ ] Configuration file
- [ ] Undo functionality (where possible)
- [ ] Flatpak/Snap packaging
- [ ] Multi-language support

## Resources

- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Qt Style Sheets](https://doc.qt.io/qt-6/stylesheet-reference.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
