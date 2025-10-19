# Echo Clear - Quick Start Guide

## 🚀 Installation

### Method 1: Automated Installation (Recommended)

```bash
cd echo-cleaner
./install.sh
```

### Method 2: Manual Installation

```bash
cd echo-cleaner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Running Echo Clear

### Option 1: Direct Launch
```bash
./echo-cleaner.py
```

### Option 2: Python Command
```bash
python3 app/main.py
```

### Option 3: From Virtual Environment
```bash
source .venv/bin/activate
python app/main.py
```

## 📖 Basic Usage

1. **Launch the application**
   - The main window will open with a beautiful, clean interface

2. **Scan your system**
   - Click the "Scan System" button
   - Wait for the analysis to complete
   - View the results in the dashboard

3. **Review what will be cleaned**
   - See the total reclaimable space
   - View the number of items found
   - Check which categories have items

4. **Clean your system**
   - Click the "Clean Now" button
   - Confirm the operation
   - Wait for cleaning to complete

## 🧹 What Gets Cleaned

### System Category
- ✅ User cache files (`~/.cache`)
- ✅ System trash
- ✅ Old log files (30+ days)
- ✅ Package manager caches (APT/DNF/Pacman)

### Developer Category
- ✅ Docker images (dangling)
- ✅ Docker containers (stopped)
- ✅ Docker volumes (unused)
- ✅ Docker build cache
- ✅ Kubernetes caches (minikube, kind, kubectl, helm)
- ✅ npm cache
- ✅ Yarn cache
- ✅ pip cache
- ✅ Maven repository
- ✅ Gradle caches
- ✅ Go module cache
- ✅ Rust cargo registry

## ⚠️ Important Notes

### Safety
- ✅ **Safe to use**: Echo Clear only removes cache and temporary files
- ⚠️ **Confirmation required**: You'll be asked before anything is deleted
- 🔒 **No system files**: Won't touch system-critical files

### Permissions
- Some operations (like package manager cleaning) may require sudo
- Docker operations require you to be in the `docker` group
- User cache cleaning works without special permissions

### Best Practices
- 🔍 **Scan first**: Always scan before cleaning
- 📊 **Review results**: Check what will be deleted
- 💾 **Backup important data**: While Echo Clear is safe, backups are always good
- 🔄 **Regular cleaning**: Run weekly or monthly for best results

## 🐛 Troubleshooting

### Application won't start
```bash
# Check Python version
python3 --version  # Should be 3.10+

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Scan finds nothing
- This is normal if your system is already clean!
- Try again after a few days of use

### Permission errors
```bash
# For Docker operations, add yourself to docker group
sudo usermod -aG docker $USER
# Then log out and back in

# For package manager operations, run with sudo
sudo python3 app/main.py
```

### UI looks wrong
- Make sure you have Qt dependencies installed
- On Ubuntu/Debian: `sudo apt install python3-pyqt6`
- On Fedora: `sudo dnf install python3-qt6`

## 📚 Learn More

- [README.md](README.md) - Full documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [DEVELOPMENT.md](DEVELOPMENT.md) - Architecture details

## 🆘 Getting Help

- **Issues**: [GitHub Issues](https://github.com/paladini/echo-cleaner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/paladini/echo-cleaner/discussions)

## 🗑️ Uninstallation

```bash
./uninstall.sh
```

Or manually:
```bash
rm -rf .venv
rm -rf __pycache__
```

---

**Enjoy your cleaner system!** ✨
