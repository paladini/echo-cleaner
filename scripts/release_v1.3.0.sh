#!/bin/bash
# Release Script for Echo Cleaner v1.3.0

set -e

echo "🚀 Echo Cleaner v1.3.0 Release Process"
echo "========================================"
echo ""

# 1. Verify we're on main branch
echo "📋 Step 1: Checking git branch..."
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ]; then
    echo "❌ Error: Not on main branch (current: $BRANCH)"
    echo "   Run: git checkout main"
    exit 1
fi
echo "✅ On main branch"
echo ""

# 2. Check for uncommitted changes
echo "📋 Step 2: Checking for uncommitted changes..."
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  You have uncommitted changes. Commit them first:"
    echo ""
    git status --short
    echo ""
    read -p "Do you want to commit these changes now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "chore: prepare v1.3.0 release"
        echo "✅ Changes committed"
    else
        echo "❌ Aborting release. Please commit changes first."
        exit 1
    fi
else
    echo "✅ No uncommitted changes"
fi
echo ""

# 3. Create and push git tag
echo "📋 Step 3: Creating git tag v1.3.0..."
if git rev-parse v1.3.0 >/dev/null 2>&1; then
    echo "⚠️  Tag v1.3.0 already exists"
    read -p "Do you want to delete and recreate it? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -d v1.3.0
        git push origin :refs/tags/v1.3.0 2>/dev/null || true
        echo "✅ Old tag deleted"
    else
        echo "❌ Aborting release"
        exit 1
    fi
fi

git tag -a v1.3.0 -m "Release v1.3.0 - Code Refactoring & Bug Fixes"
echo "✅ Tag created locally"
echo ""

# 4. Push to GitHub
echo "📋 Step 4: Pushing to GitHub..."
git push origin main
git push origin v1.3.0
echo "✅ Pushed to GitHub"
echo ""

# 5. Display GitHub CLI command for creating release
echo "📋 Step 5: Create GitHub Release"
echo ""
echo "Run the following command to create the release:"
echo ""
echo "gh release create v1.3.0 \\"
echo "  --title \"Echo Cleaner v1.3.0 - Code Refactoring & Bug Fixes\" \\"
echo "  --notes-file RELEASE_NOTES_v1.3.0.md \\"
echo "  dist/EchoCleaner-1.3.0-x86_64.AppImage \\"
echo "  dist/EchoCleaner-1.3.0-x86_64.AppImage.sha256"
echo ""
echo "Or manually:"
echo "1. Go to: https://github.com/paladini/echo-cleaner/releases/new"
echo "2. Tag: v1.3.0"
echo "3. Title: Echo Cleaner v1.3.0 - Code Refactoring & Bug Fixes"
echo "4. Description: Copy from RELEASE_NOTES_v1.3.0.md"
echo "5. Attach files:"
echo "   - dist/EchoCleaner-1.3.0-x86_64.AppImage (1.4M)"
echo "   - dist/EchoCleaner-1.3.0-x86_64.AppImage.sha256"
echo ""

# 6. Display release info
echo "📦 Release Info"
echo "==============="
echo "Version: 1.3.0"
echo "Date: $(date +%Y-%m-%d)"
echo "AppImage: dist/EchoCleaner-1.3.0-x86_64.AppImage"
echo "Size: 1.4M"
echo "SHA256: 30bbee616d177ed50b831ed83ce1ad695a0eb8307eed79e2a2e28d2e4e8379bc"
echo ""
echo "✅ Release preparation complete!"
echo ""
echo "🎉 Next steps:"
echo "   1. Create GitHub release (command shown above)"
echo "   2. Verify release page on GitHub"
echo "   3. Test download and installation"
echo "   4. Announce on social media (optional)"
