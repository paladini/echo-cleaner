# Distribution Directory

This directory contains built packages ready for distribution.

## Contents

- `*.AppImage` - Portable Linux executables
- `*.sha256` - SHA256 checksums for verification

## AppImages

AppImages are automatically placed here by the build script:
```bash
./scripts/build_appimage.sh
```

Naming format: `EchoCleaner-{VERSION}-x86_64.AppImage`

Example:
- `EchoCleaner-1.2.0-x86_64.AppImage`
- `EchoCleaner-1.2.0-x86_64.AppImage.sha256`

## Verification

To verify an AppImage download:
```bash
sha256sum -c EchoCleaner-1.2.0-x86_64.AppImage.sha256
```

## Git

AppImages are gitignored and should be distributed via:
- GitHub Releases
- Direct downloads
- Package managers

Do not commit AppImages to the repository.
