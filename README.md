# Echo Clear 🧹

<p align="center">
  <strong>Intelligent System Cleaner for Linux</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/qt-6-green.svg" alt="Qt 6">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/status-beta-orange.svg" alt="Status: Beta">
</p>

---

## 📋 About

**Echo Clear** is a modern and efficient system cleaner for Linux, featuring an elegant and intuitive interface inspired by Apple's design philosophy. Designed for both regular users and developers, Echo Clear helps you reclaim disk space by intelligently identifying and removing:

- 💾 **System caches** and temporary files
- 🐳 **Docker artifacts** (images, containers, volumes)
- ☸️ **Kubernetes** local cluster caches
- 📦 **Development dependencies** (npm, pip, maven, gradle, cargo, go)
- 🗑️ **Trash** and old logs
- 📚 **Package manager** caches

## ✨ Features

- 🔍 **Intelligent Analysis**: Automatic scan that identifies reclaimable space by category
- 🎯 **Selective Cleaning**: Choose exactly what you want to clean
- 👁️ **Detailed Visualization**: See files before deleting them
- 🖥️ **System Cleaning**: Cache, logs, trash, and packages
- 🐳 **Developer Cleaning**: Docker, Kubernetes, npm, gradle, and more
- 🎨 **Elegant Interface**: Minimalist and modern design
- ⚡ **Fast & Efficient**: Background processing with real-time progress
- 🔒 **Safe Operations**: Confirmation dialogs and error handling
- 📊 **Visual Feedback**: Progress bars and statistics cards

## 🎬 Quick Demo

```bash
# Clone the repository
git clone https://github.com/paladini/echo-cleaner.git
cd echo-cleaner

# Install and run
make install
make run

# Or use AppImage (no installation)
make build-appimage
./EchoCleaner-x86_64.AppImage
```

## 🚀 Technologies

- **Python 3.10+**: Main language with excellent system integration
- **PySide6 (Qt 6)**: Professional GUI framework
- **Layered Architecture**: Based on SOLID principles
- **Threading**: Non-blocking background operations
- **Type Hints**: Modern, maintainable code
- **Make + pyproject.toml**: Robust dependency management
- **AppImage**: Universal Linux distribution format

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Optional: Docker (for Docker cleaning)
- Optional: kubectl, minikube, etc. (for Kubernetes cleaning)

### Method 1: Quick Install (Recommended)

```bash
cd echo-cleaner
./scripts/install.sh
```

The script will:
- ✅ Check Python version
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Make scripts executable

### Method 2: Using Make

```bash
cd echo-cleaner
make install
```

### Method 3: Manual Installation

```bash
cd echo-cleaner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Method 4: AppImage (No Installation Required)

Download the latest AppImage from releases and run:

```bash
chmod +x EchoCleaner-x86_64.AppImage
./EchoCleaner-x86_64.AppImage
```

Or build it yourself:

```bash
make build-appimage
./EchoCleaner-x86_64.AppImage
```

## 🎮 Usage

### Launch the Application

**Using Make:**
```bash
make run
```

**Using Python directly:**
```bash
./echo-cleaner.py
```

**Using AppImage:**
```bash
./EchoCleaner-x86_64.AppImage
```

### Developer Commands

```bash
make help           # Show all available commands
make install        # Install dependencies
make run            # Run the application
make build-appimage # Build AppImage for distribution
make clean          # Clean build artifacts
make test           # Run tests
make format         # Format code
make lint           # Lint code
```

### Basic Workflow

1. **Click "Scan System"** - Analyzes your system
2. **Review Results** - See what can be cleaned
3. **Click "Clean Now"** - Removes selected items
4. **Confirm** - Verify the operation
5. **Done!** - View cleaning results

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

## 🏗️ Architecture

Echo Clear follows a **layered architecture** based on **SOLID principles**:

```
┌─────────────────────────────────────────┐
│      Presentation Layer (UI)            │  ← Qt Widgets, Signals
├─────────────────────────────────────────┤
│      Service Layer (Business Logic)     │  ← CleaningService
├─────────────────────────────────────────┤
│      Module Layer (System Access)       │  ← Individual Cleaners
└─────────────────────────────────────────┘
```

### Key Principles

- **Single Responsibility**: Each module has one job
- **Open/Closed**: Extend by adding new cleaners
- **Dependency Inversion**: Depend on abstractions (BaseCleaner)

See [DEVELOPMENT.md](DEVELOPMENT.md) for architecture details.

## 🛠️ Cleaning Modules

### System Modules

| Module | Target | Requires Root | Avg Savings |
|--------|--------|---------------|-------------|
| **System Cache** | `~/.cache` | No | 100MB - 2GB |
| **Trash** | `~/.local/share/Trash` | No | 50MB - 10GB |
| **Logs** | Old log files (30+ days) | No | 10MB - 500MB |
| **Package Manager** | APT/DNF/Pacman cache | Yes | 100MB - 5GB |

### Developer Modules

| Module | Target | Requires | Avg Savings |
|--------|--------|----------|-------------|
| **Docker** | Images, containers, volumes | Docker | 500MB - 20GB |
| **Kubernetes** | Minikube, kind, kubectl cache | K8s tools | 100MB - 2GB |
| **npm/Yarn** | `~/.npm`, `~/.yarn/cache` | No | 200MB - 5GB |
| **pip** | `~/.cache/pip` | No | 50MB - 1GB |
| **Maven** | `~/.m2/repository` | No | 500MB - 10GB |
| **Gradle** | `~/.gradle/caches` | No | 200MB - 3GB |
| **Go** | `~/go/pkg/mod` | No | 100MB - 2GB |
| **Cargo** | `~/.cargo/registry` | No | 200MB - 5GB |

## 📚 Documentation

- 📖 [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- 📘 [User Guide](USER_GUIDE.md) - Comprehensive usage documentation
- 🔧 [Development Guide](DEVELOPMENT.md) - Architecture and development info
- 🤝 [Contributing Guide](CONTRIBUTING.md) - How to contribute
- 📝 [Changelog](CHANGELOG.md) - Version history

## 🧪 Testing

Run the test suite to verify all modules:

```bash
make test
```

This will:
- Test each cleaning module
- Show what would be cleaned
- Estimate space savings
- **Not delete anything** (dry run by default)

## 🔒 Safety & Privacy

### What Echo Clear Does

- ✅ Scans standard cache/temp directories
- ✅ Shows what will be deleted before deleting
- ✅ Requires confirmation for destructive operations
- ✅ Handles errors gracefully

### What Echo Clear Does NOT Do

- ❌ Does not collect any data
- ❌ Does not connect to the internet
- ❌ Does not delete important files
- ❌ Does not modify configurations
- ❌ Does not access personal documents

All operations are **local only** and **fully transparent**.

## 🐛 Troubleshooting

### Permission Errors

For Docker operations:
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

For package manager cleaning:
```bash
sudo python3 app/main.py
```

### Qt/UI Issues

Install Qt dependencies:
```bash
# Ubuntu/Debian
sudo apt install python3-pyqt6

# Fedora
sudo dnf install python3-qt6

# Arch
sudo pacman -S python-pyqt6
```

See [USER_GUIDE.md](USER_GUIDE.md) for more troubleshooting.

## �️ Roadmap

### v0.2.0 (Planned)
- [ ] Per-item selection in categories
- [ ] Detailed file list view
- [ ] Export scan results
- [ ] Custom exclusion lists

### v1.0.0 (Future)
- [ ] Scheduled automatic cleaning
- [ ] System tray integration
- [ ] CLI interface
- [ ] Configuration file support
- [ ] Undo functionality (where possible)
- [ ] Multi-language support
- [ ] Flatpak/Snap packages

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Code style guidelines
- How to add new cleaning modules
- Pull request process
- Development setup

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Echo Clear Team** - Initial work

## 🙏 Acknowledgments

- Qt/PySide6 team for the excellent GUI framework
- Linux community for inspiration and feedback
- All contributors who help improve Echo Clear

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/paladini/echo-cleaner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/paladini/echo-cleaner/discussions)
- **Email**: [Add email here]

## ⭐ Star History

If you find Echo Clear useful, please consider giving it a star! ⭐

---

<p align="center">
  Made with ❤️ for the Linux community
</p>

<p align="center">
  <strong>Clean System • Happy Development • More Space</strong>
</p>
