#!/usr/bin/env python3
"""
Preview the generated application icons.

This script displays the generated icons using PIL's default viewer.
Note: On some systems, this may open an external image viewer.
"""

import os
from PIL import Image


def preview_icons():
    """Display the generated icons."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    assets_dir = os.path.join(project_root, 'assets')

    # Check if icons exist
    ico_path = os.path.join(assets_dir, 'icon.ico')
    png_path = os.path.join(assets_dir, 'icon.png')

    if not os.path.exists(ico_path) or not os.path.exists(png_path):
        print("Icon files not found. Please run: python scripts/generate_icons.py")
        return

    print("Opening icon previews...")
    print("Note: Close the preview windows to continue.\n")

    # Display PNG (most compatible)
    try:
        print("Displaying PNG icon...")
        img = Image.open(png_path)
        img.show()
        print(f"  Size: {img.size}, Format: PNG")
    except Exception as e:
        print(f"  Error displaying PNG: {e}")

    # Display ICO with its multiple sizes
    try:
        print("\nDisplaying ICO icon (256x256)...")
        img = Image.open(ico_path)
        img.show()
        print(f"  Size: {img.size}, Format: ICO")
        print(f"  Embedded sizes: {sorted(img.info.get('sizes', set()))}")
    except Exception as e:
        print(f"  Error displaying ICO: {e}")

    print("\nPreview complete!")


if __name__ == '__main__':
    preview_icons()
