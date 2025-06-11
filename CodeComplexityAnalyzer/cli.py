#!/usr/bin/env python3
"""
Command Line Interface entry point for Code Complexity Analyzer.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from interfaces.cli import cli
    if __name__ == '__main__':
        cli()
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
