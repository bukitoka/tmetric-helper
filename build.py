#!/usr/bin/env python3
"""Build script for creating standalone executable."""

import subprocess
import sys
from pathlib import Path


def build_executable():
    """Build standalone executable using PyInstaller."""
    print("Building TMetric Helper executable...")
    print("-" * 60)

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=tmetric-helper",
        "--onefile",  # Single executable file
        "--console",  # Console application
        "--clean",  # Clean PyInstaller cache
        "src/tmetric_helper/cli.py",
    ]

    print(f"Running: {' '.join(cmd)}")
    print("-" * 60)

    try:
        subprocess.run(cmd, check=True)
        print("\n" + "=" * 60)
        print("✓ Build successful!")
        print("=" * 60)
        print("\nExecutable location:")
        exe_path = Path("dist/tmetric-helper")
        if exe_path.exists():
            print(f"  {exe_path.absolute()}")
        else:
            print("  dist/tmetric-helper (Windows: dist/tmetric-helper.exe)")
        print("\nTo run:")
        print("  ./dist/tmetric-helper --help")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error code {e.returncode}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    build_executable()
