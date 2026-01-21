#!/usr/bin/env python3
"""
Application Icon Generator for Text Encoder

Generates icon files for different platforms:
- icon.ico (Windows) - 256x256
- icon.png (macOS/Linux) - 256x256

Design: Simple text encoder themed icon with "TE" text
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_icon(size=256):
    """
    Create a simple icon with 'TE' text on a rounded square background.

    Args:
        size: Icon size in pixels (default: 256)

    Returns:
        PIL.Image: The generated icon image
    """
    # Create a new image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Define colors
    # Gradient-like background using two tones of blue
    bg_color_top = (66, 133, 244, 255)    # Bright blue
    bg_color_bottom = (33, 97, 212, 255)  # Darker blue
    text_color = (255, 255, 255, 255)     # White

    # Draw rounded rectangle background
    corner_radius = size // 6
    margin = size // 16

    # Simple rounded rectangle
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=corner_radius,
        fill=bg_color_bottom
    )

    # Try to load a nice font, fall back to default if not available
    try:
        # Try to use Arial or similar system font
        font_size = size // 2
        font = ImageFont.truetype("arial.ttf", font_size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", size // 2)
        except (OSError, IOError):
            # Use default font if custom fonts are not available
            font = ImageFont.load_default()

    # Draw "TE" text centered
    text = "TE"
    try:
        # Get text bounding box for newer Pillow versions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        # Fallback for older Pillow versions
        text_width, text_height = draw.textsize(text, font=font)

    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2

    # Add a subtle shadow effect
    shadow_offset = size // 64
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text,
              font=font, fill=(0, 0, 0, 100))

    # Draw main text
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    # Add small decorative element (like code brackets)
    bracket_font_size = size // 8
    try:
        bracket_font = ImageFont.truetype("arial.ttf", bracket_font_size)
    except (OSError, IOError):
        try:
            bracket_font = ImageFont.truetype("DejaVuSans.ttf", bracket_font_size)
        except (OSError, IOError):
            bracket_font = ImageFont.load_default()

    # Draw angle brackets at bottom
    bracket_text = "< >"
    try:
        bbox = draw.textbbox((0, 0), bracket_text, font=bracket_font)
        bracket_width = bbox[2] - bbox[0]
    except AttributeError:
        bracket_width = draw.textsize(bracket_text, font=bracket_font)[0]

    bracket_x = (size - bracket_width) // 2
    bracket_y = size - (size // 5)

    draw.text((bracket_x, bracket_y), bracket_text,
              font=bracket_font, fill=(255, 255, 255, 180))

    return img


def generate_ico(output_path, size=256):
    """
    Generate Windows .ico file with multiple sizes embedded.

    Args:
        output_path: Path where the .ico file will be saved
        size: Maximum icon size in pixels
    """
    # Create icons at multiple sizes
    sizes = [16, 32, 48, 64, 128, 256]
    img_sizes = [create_icon(s) for s in sizes]

    # Save the largest image with all sizes embedded
    img_sizes[-1].save(
        output_path,
        format='ICO',
        sizes=[(s, s) for s in sizes]
    )
    print(f"Created: {output_path} (with sizes: {sizes})")


def generate_png(output_path, size=256):
    """
    Generate PNG file for macOS/Linux.

    Args:
        output_path: Path where the .png file will be saved
        size: Icon size in pixels
    """
    img = create_icon(size)
    img.save(output_path, format='PNG')
    print(f"Created: {output_path}")


def main():
    """Generate all icon files."""
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    assets_dir = os.path.join(project_root, 'assets')

    # Create assets directory if it doesn't exist
    os.makedirs(assets_dir, exist_ok=True)

    # Generate icons
    print("Generating application icons...")
    print(f"Assets directory: {assets_dir}")

    # Windows ICO
    ico_path = os.path.join(assets_dir, 'icon.ico')
    generate_ico(ico_path)

    # PNG for macOS/Linux
    png_path = os.path.join(assets_dir, 'icon.png')
    generate_png(png_path)

    print("\nIcon generation completed successfully!")
    print(f"Files created in: {assets_dir}")
    print(f"  - icon.ico (Windows)")
    print(f"  - icon.png (macOS/Linux)")


if __name__ == '__main__':
    main()
