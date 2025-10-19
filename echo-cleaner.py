#!/usr/bin/env python3
"""
Echo Cleaner Launcher Script
"""

import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from main import main

if __name__ == "__main__":
    main()
