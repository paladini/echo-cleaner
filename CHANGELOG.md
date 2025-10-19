# Changelog

All notable changes to Echo Clear will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-12

### Added
- Initial release of Echo Clear
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

[0.1.0]: https://github.com/paladini/echo-cleaner/releases/tag/v0.1.0
