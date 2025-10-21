# Changelog

All notable changes to Echo Cleaner will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-10-20

### Added
- ✨ **Empty State UI**: Beautiful "All Clean!" message when categories have no items to clean
- 🎨 **Contextual Header Buttons**: "Scan System" on Dashboard, "Clean Selected" on category pages
- 🏷️ **Smart Selection Badge**: Shows "✓ X selected • YYY MB" in header on category pages
- 🖱️ **Clickable Category Badges**: Click "All Selected" badge to toggle all items in a category
- 🔄 **Hover Text Feedback**: Badge changes text on hover ("All selected" → "Deselect All")
- 📱 **Adaptive UI**: Headers and badges automatically hide when categories are empty

### Changed
- 🎯 **Removed Clutter**: Eliminated awkward "deselect all" toggle button from dashboard
- 🎨 **Improved Badge Design**: Elegant gradients with state-based colors (green/blue for different states)
- 📐 **Better Layout**: Contextual elements appear only when needed
- ⚡ **Smoother Interactions**: Enhanced hover effects and visual feedback
- 🖼️ **Empty State Design**: Centered layout with emoji icon, title, and friendly message

### Fixed
- 🐛 **Badge Size Display**: Fixed "0 Bytes" showing in selection badge
- 🐛 **Broom Emoji on Dashboard**: Removed unwanted icon appearing after first scan
- 🐛 **Hover Effects**: Improved badge hover states with proper styling

### UI/UX Improvements
- 🎭 **State-Based Styling**: Different colors for "all selected", "none selected", and "partial selection"
- 💚 **Green Theme**: Primary actions use elegant green gradients (#34C759 → #30B350)
- 💙 **Blue Accent**: Partial selections use blue gradient for visual distinction
- 🎯 **Intuitive Interactions**: All actions have clear visual feedback
- 📦 **Hidden Elements**: Selection controls hide on empty categories and Dashboard/About pages

### Technical
- 🏗️ **Component Refactoring**: Improved separation of concerns in UI code
- 🔧 **Event Handling**: Enhanced hover and click event management
- 📊 **State Management**: Better tracking of selection states across categories
- 🎨 **CSS Organization**: Cleaner stylesheet structure with state selectors

## [1.1.0] - 2025-10-19

### Added
- 🎨 **New Professional Logo**: Replaced emoji placeholder with high-quality PNG logo (1024x1024)
- 🔒 **Sudo/pkexec Integration**: Automatic privilege escalation for operations requiring root access
- 📊 **Improved Package Manager Cleaning**: Now counts only actual package files (.deb, .rpm, .pkg.tar.*), ignoring metadata
- 🐳 **Enhanced Docker Cleaning**: Force removal of images in use by stopped containers
- 🔄 **Auto Re-scan After Cleaning**: Automatically scans system after cleaning to show updated state

### Changed
- 📏 **Larger Logo Display**: Increased logo size from 70x70 to 120x120 pixels for better visibility
- 🎯 **Removed Logo Border**: Cleaner appearance without background frame and border
- 📱 **High DPI Support**: Logo now scales properly on Retina and high-resolution displays
- ⚠️ **Better Error Handling**: Failed cleaning operations are tracked and reported to user
- 📝 **Improved Messaging**: Contextual messages for full success, partial success, or failure scenarios

### Fixed
- 🐛 **Package Manager Cache**: Fixed scan showing files after successful cleaning (was counting lock files)
- 🐛 **Docker Image Removal**: Fixed dangling images not being removed when used by stopped containers
- 🐛 **Dashboard Reset**: Fixed dashboard zeroing after cleaning - now shows updated scan results
- 🔧 **Permission Handling**: Proper detection and handling of operations requiring admin privileges

### Documentation
- 📖 **SUDO_PERMISSIONS.md**: New guide explaining privilege requirements and usage
- 📁 **Assets Directory**: New organized structure for application resources
- 📝 **Updated README**: Renamed from "Echo Clear" to "Echo Cleaner" throughout all documentation

## [1.0.0] - 2025-10-12

### Added
- Initial release of Echo Cleaner
- Modern Qt-based UI with Apple-inspired design
- System cleaning modules:
  - System Cache Cleaner
  - Trash Cleaner
  - Log Cleaner
  - Package Manager Cleaner (APT, DNF, Pacman)
- Developer cleaning modules:
  - Docker Cleaner (images, containers, volumes, build cache)
  - Kubernetes Cleaner (minikube, kind, kubectl, helm)
  - Dev Dependencies Cleaner (npm, yarn, pip, maven, gradle, go, cargo)
- Intelligent system scan
- Real-time progress tracking
- Layered architecture based on SOLID principles
- Background threading for non-blocking operations
- Human-readable size formatting
- Confirmation dialogs for destructive operations

### Features
- 🔍 **Smart Scanning**: Automatically detects reclaimable space
- 🎯 **Selective Cleaning**: Choose what to clean
- 👁️ **Detailed View**: See what will be deleted
- 🎨 **Beautiful UI**: Minimalist, Apple-inspired design
- ⚡ **Fast & Efficient**: Background processing
- 🐳 **Developer-Friendly**: Cleans Docker, K8s, and language caches

[1.2.0]: https://github.com/paladini/echo-cleaner/releases/tag/v1.2.0
[1.1.0]: https://github.com/paladini/echo-cleaner/releases/tag/v1.1.0
[1.0.0]: https://github.com/paladini/echo-cleaner/releases/tag/v1.0.0
