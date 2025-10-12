# Screenshots directory

This directory will contain application screenshots for documentation.

To add screenshots:

1. Take screenshots of the application
2. Save them with descriptive names:
   - `dashboard.png` - Main dashboard view
   - `scanning.png` - Scan in progress
   - `scan-results.png` - Scan completed
   - `confirmation.png` - Clean confirmation dialog
   - `success.png` - Clean success message
   - `categories.png` - Category selection (future)

3. Update SCREENSHOTS.md with the actual images
4. Optimize images for web (keep under 500KB each)

Recommended tools:
- **GNOME Screenshot**: `gnome-screenshot -a`
- **Flameshot**: `flameshot gui`
- **Spectacle** (KDE): `spectacle`

Image optimization:
```bash
# Using ImageMagick
mogrify -resize 1200x -quality 85 *.png

# Using optipng
optipng -o7 *.png
```
