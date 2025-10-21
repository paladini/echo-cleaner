# Build Tools Directory

This directory contains build-time tools that are **automatically downloaded** when needed.

## What's in here?

### `appimagetool-x86_64.AppImage`
- **Purpose**: Converts the application into a single `.AppImage` file for distribution
- **Downloaded from**: [AppImageKit Releases](https://github.com/AppImage/AppImageKit/releases)
- **Used by**: `make build-appimage` command
- **User impact**: NONE - end users don't need this tool, it's only for building releases

## Why is this separate?

- **Not part of the app**: These are build tools, not runtime dependencies
- **Not versioned**: Added to `.gitignore` to keep repository clean
- **Auto-downloaded**: The build script downloads automatically if missing
- **Clean separation**: Keeps project root organized

## How it works

When you run `make build-appimage`:

1. Script checks if `tools/appimagetool-x86_64.AppImage` exists
2. If not found, downloads it automatically (~8.4 MB)
3. Uses it to create the final `EchoCleaner-x86_64.AppImage`
4. The **final AppImage** is what users download and run

## Manual download (optional)

```bash
make download-tools
```

Or download manually:
```bash
mkdir -p tools
cd tools
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
```

## Clean up

To remove downloaded tools:
```bash
make clean-all
```

---

**Note for contributors**: You don't need to commit anything in this directory. It's automatically managed by the build system.
