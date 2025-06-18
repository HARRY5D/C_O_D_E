#!/usr/bin/env python3
"""
Test script to identify import issues
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from real_data_processor import RealDataProcessor
    print("✅ Successfully imported RealDataProcessor")
    
    # Test instantiation
    processor = RealDataProcessor()
    print("✅ Successfully created RealDataProcessor instance")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    print(f"Files in src directory:")
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    if os.path.exists(src_dir):
        print(os.listdir(src_dir))
    else:
        print("❌ src directory not found")

except Exception as e:
    print(f"❌ Other Error: {e}")
    import traceback
    traceback.print_exc()
