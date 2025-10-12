#!/usr/bin/env python3
"""
Echo Clear - Project Validator
Validates the project structure and dependencies
"""

import os
import sys
from pathlib import Path


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def check(condition, message):
    if condition:
        print(f"{Colors.GREEN}✓{Colors.END} {message}")
        return True
    else:
        print(f"{Colors.RED}✗{Colors.END} {message}")
        return False


def validate_structure():
    """Validate project structure"""
    print_header("Project Structure Validation")
    
    required_dirs = [
        'app',
        'app/ui',
        'app/services',
        'app/modules',
        'app/assets',
        'screenshots',
    ]
    
    required_files = [
        'app/__init__.py',
        'app/main.py',
        'app/ui/__init__.py',
        'app/ui/main_window.py',
        'app/services/__init__.py',
        'app/services/cleaning_service.py',
        'app/modules/__init__.py',
        'app/modules/base_cleaner.py',
        'app/modules/system_cache_cleaner.py',
        'app/modules/trash_cleaner.py',
        'app/modules/log_cleaner.py',
        'app/modules/package_manager_cleaner.py',
        'app/modules/docker_cleaner.py',
        'app/modules/dev_dependencies_cleaner.py',
        'app/modules/kubernetes_cleaner.py',
        'requirements.txt',
        'README.md',
        'LICENSE',
        'install.sh',
        'uninstall.sh',
        'echo-clear.py',
        'test.py',
    ]
    
    all_ok = True
    
    # Check directories
    print(f"{Colors.BOLD}Directories:{Colors.END}")
    for dir_path in required_dirs:
        exists = Path(dir_path).is_dir()
        check(exists, f"Directory: {dir_path}")
        all_ok = all_ok and exists
    
    print(f"\n{Colors.BOLD}Files:{Colors.END}")
    for file_path in required_files:
        exists = Path(file_path).is_file()
        check(exists, f"File: {file_path}")
        all_ok = all_ok and exists
    
    return all_ok


def validate_python():
    """Validate Python version and imports"""
    print_header("Python Environment Validation")
    
    all_ok = True
    
    # Check Python version
    version = sys.version_info
    version_ok = version >= (3, 10)
    check(version_ok, f"Python version: {version.major}.{version.minor}.{version.micro}")
    all_ok = all_ok and version_ok
    
    # Check imports
    print(f"\n{Colors.BOLD}Required Modules:{Colors.END}")
    
    modules = [
        ('PySide6', 'PySide6'),
        ('psutil', 'psutil'),
        ('humanize', 'humanize'),
    ]
    
    for module_name, import_name in modules:
        try:
            __import__(import_name)
            check(True, f"Module: {module_name}")
        except ImportError:
            check(False, f"Module: {module_name} (not installed)")
            all_ok = False
    
    return all_ok


def validate_executables():
    """Validate executable permissions"""
    print_header("Executable Permissions Validation")
    
    executables = [
        'install.sh',
        'uninstall.sh',
        'echo-clear.py',
        'test.py',
    ]
    
    all_ok = True
    
    for exe in executables:
        path = Path(exe)
        if path.exists():
            executable = os.access(path, os.X_OK)
            check(executable, f"Executable: {exe}")
            all_ok = all_ok and executable
        else:
            check(False, f"File missing: {exe}")
            all_ok = False
    
    return all_ok


def validate_documentation():
    """Validate documentation files"""
    print_header("Documentation Validation")
    
    docs = [
        'README.md',
        'QUICKSTART.md',
        'USER_GUIDE.md',
        'DEVELOPMENT.md',
        'CONTRIBUTING.md',
        'CHANGELOG.md',
        'LICENSE',
        'PROJECT_SUMMARY.md',
    ]
    
    all_ok = True
    
    for doc in docs:
        exists = Path(doc).is_file()
        check(exists, f"Documentation: {doc}")
        all_ok = all_ok and exists
    
    return all_ok


def print_summary(results):
    """Print validation summary"""
    print_header("Validation Summary")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"{Colors.BOLD}Total Checks:{Colors.END} {total}")
    print(f"{Colors.GREEN}{Colors.BOLD}Passed:{Colors.END} {passed}")
    if failed > 0:
        print(f"{Colors.RED}{Colors.BOLD}Failed:{Colors.END} {failed}")
    
    print()
    
    if failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All validations passed!{Colors.END}")
        print(f"{Colors.GREEN}Echo Clear is ready to use.{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Some validations failed.{Colors.END}")
        print(f"{Colors.YELLOW}Please fix the issues above.{Colors.END}")
        return False


def main():
    """Main validation function"""
    print(f"""
{Colors.BOLD}{Colors.BLUE}╔════════════════════════════════════════════════════════════╗
║                                                            ║
║               ECHO CLEAR - PROJECT VALIDATOR               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝{Colors.END}
""")
    
    # Run validations
    results = {
        'structure': validate_structure(),
        'python': validate_python(),
        'executables': validate_executables(),
        'documentation': validate_documentation(),
    }
    
    # Print summary
    success = print_summary(results)
    
    print(f"\n{Colors.BOLD}Next Steps:{Colors.END}")
    if success:
        print("1. Run: ./echo-clear.py")
        print("2. Click 'Scan System'")
        print("3. Review results")
        print("4. Click 'Clean Now'")
        print("\nFor more info, see: QUICKSTART.md")
    else:
        print("1. Fix the issues listed above")
        print("2. Run this validator again")
        print("3. See QUICKSTART.md for installation help")
    
    print()
    
    return 0 if success else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Validation interrupted by user{Colors.END}")
        sys.exit(1)
