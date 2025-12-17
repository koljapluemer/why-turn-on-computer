#!/usr/bin/env python3
"""
Build script to create executables for why and why-done commands
"""
import subprocess
import sys


def build_executable(script_name: str, exe_name: str) -> bool:
    """Build executable using PyInstaller."""
    cmd = [
        "uv", "run", "pyinstaller",
        "--onefile",                    # Create a single executable file
        "--console",                    # Show console window (for terminal apps)
        "--name", exe_name,             # Name of the executable
        script_name                     # Main script
    ]

    print(f"Building {exe_name}...")
    print(f"Running: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ Build successful: dist/{exe_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False


def main():
    print("Building Why Turn On Computer executables...\n")

    success = True
    success &= build_executable("why.py", "why")
    success &= build_executable("why_done.py", "why-done")

    if success:
        print("\n✓ All builds successful!")
        print("Executables created in dist/")
        print("\nNext steps:")
        print("  1. Run: bash install.sh")
        print("  2. Or manually add aliases to your shell config")
    else:
        print("\n✗ Some builds failed")
        sys.exit(1)


if __name__ == "__main__":
    main()