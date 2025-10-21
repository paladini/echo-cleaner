# Data Directory

This directory contains application metadata and assets following FreeDesktop.org standards.

## Structure

```
data/
├── icons/                                  # Application icons
│   └── hicolor/                           # Icon theme directory
│       ├── 256x256/apps/                  # 256x256 PNG icons
│       │   └── io.github.paladini.EchoCleaner.png
│       └── scalable/apps/                 # SVG icons (optional)
│           └── io.github.paladini.EchoCleaner.svg
├── io.github.paladini.EchoCleaner.desktop      # Desktop entry file
└── io.github.paladini.EchoCleaner.metainfo.xml # AppStream metadata
```

## Files

### Desktop Entry (`*.desktop`)
- Defines how the application appears in application menus
- Follows [Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/latest/)
- Used by all desktop environments (GNOME, KDE, Xfce, etc.)

### AppStream Metadata (`*.metainfo.xml`)
- Provides rich metadata for software centers
- Includes descriptions, screenshots, release notes
- Required for Flathub and Snap Store
- Follows [AppStream Specification](https://www.freedesktop.org/software/appstream/docs/)

### Icons
- **Format**: PNG (256x256) is required, SVG is optional but recommended
- **Naming**: Must match the application ID (`io.github.paladini.EchoCleaner`)
- **Location**: Follows XDG Icon Theme Specification

## Application ID

The reverse-DNS application ID is: **`io.github.paladini.EchoCleaner`**

This ID is used consistently across:
- Desktop file name
- Icon file name
- AppStream metadata file name
- Internal application identification

## Standards Compliance

All files in this directory follow these standards:
- [FreeDesktop.org Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/latest/)
- [FreeDesktop.org Icon Theme Specification](https://specifications.freedesktop.org/icon-theme-spec/latest/)
- [AppStream Specification](https://www.freedesktop.org/software/appstream/docs/)
- [Flatpak Manifest Guidelines](https://docs.flatpak.org/en/latest/manifests.html)

## Usage

These files are automatically copied during the build process:
- AppImage: Embedded in the `.AppDir` structure
- Flatpak/Snap: Installed to system directories
- System Install: Copied to `/usr/share/` directories
