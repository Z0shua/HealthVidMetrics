#!/usr/bin/env python3
"""
Test script for HealthVidMetrics core functionality
"""

import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def test_imports():
    print("Testing imports...")
    try:
        from healthvidmetrics import youtube_api, scoring, utils, export
        print("✓ Core modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Core module import failed: {e}")
        return False

def main():
    print("HealthVidMetrics Modular Test Suite")
    print("=" * 40)
    if test_imports():
        print("🎉 All core modules import successfully.")
    else:
        print("❌ Core module import failed.")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main()) 