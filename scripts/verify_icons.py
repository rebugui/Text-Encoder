#!/usr/bin/env python3
"""
Verify that icon files exist and are valid.

This script checks the generated icon files and displays their properties.
"""

import os
from PIL import Image


def verify_icon_file(filepath, expected_format):
    """Verify a single icon file."""
    if not os.path.exists(filepath):
        print(f"[X] {filepath} does not exist!")
        return False

    try:
        img = Image.open(filepath)
        print(f"[OK] {os.path.basename(filepath)}:")
        print(f"  Format: {img.format}")
        print(f"  Size: {img.size}")
        print(f"  Mode: {img.mode}")

        if img.format == 'ICO':
            sizes = img.info.get('sizes', set())
            print(f"  Embedded sizes: {sorted(sizes)}")

        return True
    except Exception as e:
        print(f"[X] Error reading {filepath}: {e}")
        return False


def main():
    """Verify all icon files."""
    print("Verifying application icons...\n")

    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    assets_dir = os.path.join(project_root, 'assets')

    # Check assets directory
    if not os.path.exists(assets_dir):
        print(f"[X] Assets directory does not exist: {assets_dir}")
        return

    print(f"Assets directory: {assets_dir}\n")

    # Verify icons
    all_ok = True

    # Windows ICO
    ico_path = os.path.join(assets_dir, 'icon.ico')
    if not verify_icon_file(ico_path, 'ICO'):
        all_ok = False
    print()

    # PNG for macOS/Linux
    png_path = os.path.join(assets_dir, 'icon.png')
    if not verify_icon_file(png_path, 'PNG'):
        all_ok = False
    print()

    if all_ok:
        print("[OK] All icon files are valid!")
    else:
        print("[X] Some icon files are missing or invalid!")
        print("\nRun: python scripts/generate_icons.py")

    return all_ok


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
