# Assets Directory

This directory contains application resources such as images, icons, and other media files.

## Files

- **logo.png** - Application logo displayed in the sidebar (70x70px scaled)
- **icon.png** - Application icon used for AppImage and desktop entries (256x256px recommended)

## Usage

The logo is automatically loaded by the main window UI component. If the file is not found, it falls back to an emoji placeholder (✨).

## Adding New Assets

1. Place image files in this directory
2. Reference them in code using relative paths from the `app` directory
3. For AppImage builds, ensure icons are properly sized (256x256px for best compatibility)
