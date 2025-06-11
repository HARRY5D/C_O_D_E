#!/usr/bin/env python3
"""
Streamlit Web Application entry point for Code Complexity Analyzer.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from interfaces.web_app import main

if __name__ == '__main__':
    main()
