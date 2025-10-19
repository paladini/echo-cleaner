# Echo Clear - User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Interface Overview](#interface-overview)
4. [Using Echo Clear](#using-echo-clear)
5. [Cleaning Categories](#cleaning-categories)
6. [Advanced Usage](#advanced-usage)
7. [Safety & Privacy](#safety--privacy)
8. [FAQ](#faq)

## Introduction

Echo Clear is a modern system cleaner designed specifically for Linux. It helps you:

- 🔍 Identify reclaimable disk space
- 🧹 Clean system caches safely
- 🐳 Remove unused Docker artifacts
- 📦 Clean development dependency caches
- ⚡ Speed up your system

### Who is Echo Clear for?

- **Regular Users**: Clean system caches and free up space
- **Developers**: Remove Docker images, dependency caches, and build artifacts
- **DevOps Engineers**: Clean Kubernetes and container-related caches
- **Anyone**: Who wants a cleaner, faster Linux system

## Installation

See [QUICKSTART.md](QUICKSTART.md) for detailed installation instructions.

**Quick Install:**
```bash
./install.sh
```

## Interface Overview

### Main Window Layout

```
┌─────────────────────────────────────────────────┐
│  Sidebar       │  Content Area                  │
│  ──────────    │  ───────────────               │
│  Echo Clear    │  Dashboard                     │
│                │                                 │
│  CATEGORIES    │  ┌───────────────────────┐    │
│  □ Dashboard   │  │ Total Reclaimable     │    │
│  □ System      │  │ 2.5 GB                │    │
│  □ Docker      │  └───────────────────────┘    │
│  □ Dev Deps    │                                │
│                │  [Scan System] [Clean Now]    │
└─────────────────────────────────────────────────┘
```

### UI Elements

1. **Sidebar**
   - Application title
   - Category list
   - Version info

2. **Content Area**
   - Page title
   - Action buttons
   - Statistics cards
   - Progress indicators

3. **Action Buttons**
   - **Scan System**: Analyze your system
   - **Clean Now**: Remove selected items (enabled after scan)

## Using Echo Clear

### Step 1: Launch the Application

```bash
./echo-cleaner.py
```

The main window opens showing the Dashboard.

### Step 2: Scan Your System

1. Click the **"Scan System"** button
2. Watch the progress bar as Echo Clear analyzes your system
3. Wait for the scan to complete (usually 10-30 seconds)

During the scan, Echo Clear:
- Checks system cache directories
- Analyzes Docker artifacts
- Scans development caches
- Calculates total reclaimable space

### Step 3: Review Results

After scanning, the dashboard shows:

- **Total Reclaimable**: Total space that can be freed
- **Items Found**: Number of items that can be cleaned
- **Categories**: Number of categories with items

### Step 4: Clean Your System

1. Click the **"Clean Now"** button
2. A confirmation dialog appears showing:
   - Total space to be freed
   - Number of categories affected
   - Warning that this cannot be undone
3. Click **"Yes"** to proceed
4. Watch the progress as Echo Clear cleans your system
5. See the success message with results

### Step 5: Verify Results

After cleaning:
- Dashboard statistics reset to zero
- A success message shows:
  - Total space cleaned
  - Number of items removed

## Cleaning Categories

### System Cache

**What it cleans:**
- `~/.cache/*` - User application caches

**Safe to clean?** ✅ Yes, applications will recreate caches as needed

**Average savings:** 100 MB - 2 GB

---

### Trash

**What it cleans:**
- `~/.local/share/Trash/files/*` - Deleted files in trash

**Safe to clean?** ✅ Yes, but files cannot be recovered after

**Average savings:** 50 MB - 10 GB

---

### Logs

**What it cleans:**
- Log files older than 30 days
- `~/.xsession-errors`
- `~/.local/share/xorg/*.log`

**Safe to clean?** ✅ Yes, old logs are rarely needed

**Average savings:** 10 MB - 500 MB

---

### Package Manager

**What it cleans:**
- APT cache: `/var/cache/apt/archives`
- DNF cache: `/var/cache/dnf`
- Pacman cache: `/var/cache/pacman/pkg`

**Safe to clean?** ✅ Yes, packages can be re-downloaded if needed

**Average savings:** 100 MB - 5 GB

**Note:** Requires sudo for some operations

---

### Docker

**What it cleans:**
- Dangling images
- Stopped containers
- Unused volumes
- Build cache

**Safe to clean?** ✅ Yes, but only removes unused/stopped items

**Average savings:** 500 MB - 20 GB

**Requirements:**
- Docker installed
- User in `docker` group

**Check with:**
```bash
docker system df
```

---

### Kubernetes

**What it cleans:**
- Minikube cache
- kind cache
- kubectl cache
- Helm cache

**Safe to clean?** ✅ Yes, caches will regenerate

**Average savings:** 100 MB - 2 GB

---

### Dev Dependencies

**What it cleans:**
- npm cache (`~/.npm`)
- Yarn cache (`~/.yarn/cache`)
- pip cache (`~/.cache/pip`)
- Maven repository (`~/.m2/repository`)
- Gradle caches (`~/.gradle/caches`)
- Go modules (`~/go/pkg/mod`)
- Cargo registry (`~/.cargo/registry`)

**Safe to clean?** ✅ Yes, dependencies will be re-downloaded when needed

**Average savings:** 200 MB - 10 GB

## Advanced Usage

### Command Line Arguments

Echo Clear can be extended to support command-line arguments:

```bash
# Future feature: scan only
./echo-cleaner.py --scan-only

# Future feature: auto-clean
./echo-cleaner.py --auto-clean

# Future feature: dry run
./echo-cleaner.py --dry-run
```

### Configuration File

Future versions will support a configuration file (`~/.config/echo-cleaner/config.json`):

```json
{
  "scan_on_startup": false,
  "auto_clean_threshold_gb": 5,
  "exclude_paths": [
    "~/.cache/important-app"
  ],
  "log_age_days": 30
}
```

## Safety & Privacy

### What Echo Clear Does NOT Do

- ❌ Does not collect any data
- ❌ Does not connect to the internet
- ❌ Does not delete important system files
- ❌ Does not modify configurations
- ❌ Does not access personal files

### Safety Features

- ✅ **Confirmation dialogs**: Always asks before deleting
- ✅ **Safe paths only**: Only targets known cache/temp directories
- ✅ **No wildcards**: Uses explicit path operations
- ✅ **Error handling**: Gracefully handles permission errors
- ✅ **Read-only scanning**: Scan doesn't modify anything

### Privacy

- All operations are **local only**
- No telemetry or analytics
- No accounts required
- Open source - audit the code yourself!

## FAQ

### Q: Will Echo Clear make my system faster?

A: It can help by:
- Freeing up disk space
- Reducing disk I/O for cache lookups
- Cleaning up orphaned Docker containers

However, it's not a performance optimization tool.

### Q: How often should I run Echo Clear?

A: Recommended frequency:
- **Developers**: Weekly
- **Regular users**: Monthly
- **Servers**: As needed

### Q: Can I undo a clean operation?

A: No, files are permanently deleted. However, all cleaned items are caches that can be regenerated.

### Q: Is it safe to clean everything?

A: Yes! Echo Clear only targets:
- Cache directories
- Temporary files
- Unused Docker artifacts
- Old logs

It never touches:
- System files
- User documents
- Configuration files
- Active applications

### Q: Why does it need sudo for some operations?

A: Package manager caches (APT, DNF, Pacman) are in system directories that require root access.

You can run Echo Clear without sudo to clean user-level items only.

### Q: What if the scan finds nothing?

A: Great! Your system is already clean. Come back in a few days.

### Q: Does it work on all Linux distributions?

A: Yes! Echo Clear supports:
- Ubuntu / Debian (APT)
- Fedora / RHEL (DNF)
- Arch Linux (Pacman)
- Any Linux with standard cache locations

### Q: Can I select individual items to clean?

A: Currently, cleaning is category-based. Individual item selection is planned for v2.0.

### Q: How do I report a bug?

A: Open an issue on GitHub with:
- Your Linux distribution
- Echo Clear version
- Error message (if any)
- Steps to reproduce

## Support

- 📖 Documentation: [README.md](README.md)
- 🐛 Report bugs: [GitHub Issues](https://github.com/paladini/echo-cleaner/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/paladini/echo-cleaner/discussions)
- 🤝 Contribute: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Happy Cleaning!** 🧹✨
