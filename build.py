#!/usr/bin/env python3
"""
Build script to create executable from main.py
"""
import subprocess
import sys
import os

def build_executable():
    """Build the executable using PyInstaller"""
    
    # PyInstaller command
    cmd = [
        "poetry", "run", "pyinstaller",
        "--onefile",                    # Create a single executable file
        "--windowed",                   # Hide console window (for GUI apps)
        "--name", "why-turn-on-computer", # Name of the executable
        "--add-data", "purpose.txt:.",  # Include purpose.txt file
        "main.py"                       # Main script
    ]
    
    print("Building executable...")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(f"Executable created at: dist/why-turn-on-computer")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)