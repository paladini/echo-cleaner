#!/usr/bin/env python3
"""
Echo Clear - Test Suite
Simple manual testing script for Echo Clear modules
"""

import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from modules import (
    SystemCacheCleaner,
    TrashCleaner,
    LogCleaner,
    PackageManagerCleaner,
    DockerCleaner,
    DevDependenciesCleaner,
    KubernetesCleaner
)


def format_size(bytes_size):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def test_cleaner(cleaner, dry_run=True):
    """Test a single cleaner module"""
    print(f"\n{'='*60}")
    print(f"Testing: {cleaner.name}")
    print(f"Description: {cleaner.description}")
    print(f"{'='*60}")
    
    try:
        print("\n🔍 Scanning...")
        items = cleaner.scan()
        
        if not items:
            print("✅ No items found (system is clean)")
            return
        
        print(f"\n📊 Found {len(items)} items:")
        
        total_size = 0
        for i, item in enumerate(items[:10], 1):  # Show first 10
            size = item.get('size', 0)
            total_size += size
            name = item.get('name', 'Unknown')
            item_type = item.get('type', 'unknown')
            
            print(f"  {i}. {name}")
            print(f"     Size: {format_size(size)}")
            print(f"     Type: {item_type}")
            if 'requires_root' in item:
                print(f"     ⚠️  Requires root access")
            print()
        
        if len(items) > 10:
            remaining = len(items) - 10
            remaining_size = sum(item.get('size', 0) for item in items[10:])
            total_size += remaining_size
            print(f"  ... and {remaining} more items ({format_size(remaining_size)})")
        
        print(f"\n💾 Total reclaimable space: {format_size(total_size)}")
        
        if dry_run:
            print("\n⚠️  DRY RUN MODE - No files will be deleted")
        else:
            print("\n⚠️  CLEANING MODE - Files will be deleted!")
            response = input("Continue? (yes/NO): ")
            if response.lower() == 'yes':
                print("\n🧹 Cleaning...")
                cleaned_size = cleaner.clean(items)
                print(f"✅ Cleaned {format_size(cleaned_size)}")
            else:
                print("❌ Cleaning cancelled")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main test function"""
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║               ECHO CLEAR - TEST SUITE                      ║
║                                                            ║
║  This script tests all cleaning modules without actually  ║
║  deleting anything (dry run mode by default).             ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""")
    
    # Ask for mode
    print("Select test mode:")
    print("1. Dry Run (scan only, no deletion)")
    print("2. Full Test (includes cleaning - DANGEROUS!)")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    dry_run = choice != '2'
    
    if not dry_run:
        print("\n⚠️  WARNING: Full test mode will DELETE files!")
        print("⚠️  This should only be used in a test environment!")
        confirm = input("Type 'I UNDERSTAND' to continue: ")
        if confirm != "I UNDERSTAND":
            print("Test cancelled.")
            return
    
    # Create cleaner instances
    cleaners = [
        SystemCacheCleaner(),
        TrashCleaner(),
        LogCleaner(),
        PackageManagerCleaner(),
        DockerCleaner(),
        DevDependenciesCleaner(),
        KubernetesCleaner()
    ]
    
    # Test each cleaner
    for cleaner in cleaners:
        test_cleaner(cleaner, dry_run=dry_run)
        
        if cleaner != cleaners[-1]:  # Not the last one
            input("\nPress Enter to continue to next cleaner...")
    
    print(f"\n{'='*60}")
    print("✅ All tests completed!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
