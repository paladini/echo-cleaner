# Echo Cleaner 🧹

![Dashboard Page - Scan Stats](docs/screenshots/dashboard.jpeg)

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

**Echo Cleaner** is a modern and efficient system cleaner for Linux, featuring an elegant and intuitive interface inspired by Apple's design philosophy. Designed for both regular users and developers, Echo Cleaner helps you reclaim disk space by intelligently identifying and removing:

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

## 🎬 Quick Start

**Download and run - it's that simple!**

```bash
# Download the latest release
wget https://github.com/paladini/echo-cleaner/releases/latest/download/EchoCleaner-1.2.0-x86_64.AppImage

# Make it executable
chmod +x EchoCleaner-1.2.0-x86_64.AppImage

# Run it!
./EchoCleaner-1.2.0-x86_64.AppImage
```

No installation required. No dependencies to manage. Just download and run.

## 🚀 Technologies

- **Python 3.10+**: Main language with excellent system integration
- **PySide6 (Qt 6)**: Professional GUI framework
- **Layered Architecture**: Based on SOLID principles
- **Threading**: Non-blocking background operations
- **Type Hints**: Modern, maintainable code
- **Make + pyproject.toml**: Robust dependency management
- **AppImage**: Universal Linux distribution format

## 📦 Installation

### AppImage (Recommended - No Installation!)

AppImage is a universal Linux application format that runs anywhere. No installation, no dependencies, no root required.

**1. Download**
```bash
wget https://github.com/paladini/echo-cleaner/releases/latest/download/EchoCleaner-1.2.0-x86_64.AppImage
```

**2. Make executable**
```bash
chmod +x EchoCleaner-1.2.0-x86_64.AppImage
```

**3. Run**
```bash
./EchoCleaner-1.2.0-x86_64.AppImage
```

That's it! The AppImage includes everything needed to run Echo Cleaner.

**Optional: Integrate with your system**

To add Echo Cleaner to your application menu:
```bash
# Move to a permanent location
mkdir -p ~/.local/bin
mv EchoCleaner-1.2.0-x86_64.AppImage ~/.local/bin/EchoCleaner.AppImage

# Make it available from anywhere
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Now you can launch it from your application menu or by typing `EchoCleaner.AppImage` in the terminal.

### From Source (For Developers)

If you want to contribute or modify the code:

```bash
git clone https://github.com/paladini/echo-cleaner.git
cd echo-cleaner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./echo-cleaner.py
```

## 🎮 Usage

### Running Echo Cleaner

**With AppImage:**
```bash
./EchoCleaner-1.2.0-x86_64.AppImage
```

**From source:**
```bash
./echo-cleaner.py
```

### How It Works

1. **Scan System** - Click the button to analyze your system
2. **Review Categories** - See what can be cleaned (System Cache, Docker, etc.)
3. **Select Items** - Choose what you want to remove
4. **Clean** - Click "Clean Selected" and confirm
5. **Done!** - View how much space you freed

### Tips

- 💡 Click category badges to select/deselect all items
- 💡 Hover over items to see detailed information
- 💡 Categories with no items show "All Clean!" message
- 💡 The app automatically rescans after cleaning

## 🏗️ Architecture

Echo Cleaner follows a **layered architecture** based on **SOLID principles**:

```
┌─────────────────────────────────────────┐
│      Presentation Layer (UI)            │  ← Qt Widgets, Signals
├─────────────────────────────────────────┤
│      Service Layer (Business Logic)     │  ← CleaningService
├─────────────────────────────────────────┤
│      Module Layer (System Access)       │  ← Individual Cleaners
└─────────────────────────────────────────┘
```

See [DEVELOPMENT.md](docs/guides/DEVELOPMENT.md) for details.

## 📁 Project Structure

```
echo-cleaner/
├── app/                    # Application source code
│   ├── models/            # Data models
│   ├── modules/           # Cleaning modules
│   ├── services/          # Business logic
│   └── ui/                # User interface
├── data/                  # Application metadata (FreeDesktop.org standards)
│   ├── icons/             # Application icons
│   ├── *.desktop          # Desktop entry
│   └── *.metainfo.xml     # AppStream metadata
├── dist/                  # Built packages (AppImages, checksums)
├── docs/                  # Documentation
│   ├── guides/            # Development and user guides
│   └── release-notes/     # Release documentation
├── scripts/               # Build and deployment scripts
└── tools/                 # External build tools
```

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

-  [Development Guide](docs/guides/DEVELOPMENT.md) - Architecture and development
- 🤝 [Contributing Guide](docs/guides/CONTRIBUTING.md) - How to contribute
- 📝 [Changelog](CHANGELOG.md) - Version history
- 📸 [Screenshots](docs/SCREENSHOTS.md) - Visual overview

## 🧪 Testing

If you're running from source, you can test the cleaning modules:

```bash
make test
```

This will show what would be cleaned without actually deleting anything.

## 🔒 Safety & Privacy

### What Echo Cleaner Does

- ✅ Scans standard cache/temp directories
- ✅ Shows what will be deleted before deleting
- ✅ Requires confirmation for destructive operations
- ✅ Handles errors gracefully

### What Echo Cleaner Does NOT Do

- ❌ Does not collect any data
- ❌ Does not connect to the internet
- ❌ Does not delete important files
- ❌ Does not modify configurations
- ❌ Does not access personal documents

All operations are **local only** and **fully transparent**.

## 🐛 Troubleshooting

### AppImage Won't Run

Make sure it's executable:
```bash
chmod +x EchoCleaner-1.2.0-x86_64.AppImage
```

If you get "FUSE" errors on older systems:
```bash
./EchoCleaner-1.2.0-x86_64.AppImage --appimage-extract-and-run
```

### Permission Errors During Cleaning

**For Docker operations:**
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

**For system package cache:**
- The app will automatically request sudo password when needed

### Missing Features

Some cleaning modules only appear if the related tools are installed:
- **Docker**: Requires Docker to be installed
- **Kubernetes**: Requires kubectl, minikube, or kind
- **Development Dependencies**: Only shows if cache directories exist

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](docs/guides/CONTRIBUTING.md) for details on how to contribute.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Fernando Paladini** - [github.com/paladini](https://github.com/paladini)
- Built with GitHub Copilot

## 🙏 Acknowledgments

- Qt/PySide6 team for the excellent GUI framework
- Linux community for inspiration and feedback
- All contributors who help improve Echo Cleaner

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/paladini/echo-cleaner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/paladini/echo-cleaner/discussions)

## ⭐ Star History

If you find Echo Cleaner useful, please consider giving it a star! ⭐

---

<p align="center">
  Made with ❤️ for the Linux community
</p>

<p align="center">
  <strong>Clean System • Happy Development • More Space</strong>
</p>
