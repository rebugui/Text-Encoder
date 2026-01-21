# Application Icons Documentation

## Overview

The Text Encoder application uses custom-designed icons for different platforms. The icons are generated programmatically using Python's Pillow (PIL) library.

## Icon Design

### Visual Elements
- **Main Text**: "TE" (Text Encoder) in white, centered
- **Background**: Rounded rectangle with gradient blue background (#4285F4 to #2155D4)
- **Accent**: Small "< >" symbols at the bottom representing code/encoding
- **Shadow**: Subtle drop shadow for depth
- **Format**: RGBA with transparent background

### Sizes
- **Primary Size**: 256x256 pixels
- **ICO Multi-Size**: 16, 32, 48, 64, 128, 256 pixels (Windows)

## Generated Files

### 1. `assets/icon.ico` (Windows)
- **Format**: ICO with multiple sizes embedded
- **Sizes**: 16x16, 32x32, 48x48, 64x64, 128x128, 256x256
- **Usage**: Windows executable icon
- **File Size**: ~15KB
- **Configured in**: `build/encoder.spec`

### 2. `assets/icon.png` (macOS/Linux)
- **Format**: PNG
- **Size**: 256x256 pixels
- **Mode**: RGBA (transparent background)
- **Usage**: macOS and Linux application icons
- **File Size**: ~2.9KB

## Scripts

### 1. `scripts/generate_icons.py`
Main script to generate both icon files.

```bash
python scripts/generate_icons.py
```

**Features**:
- Creates both ICO and PNG files
- Generates icons at multiple sizes for Windows
- Uses system fonts when available, falls back to default
- Adds visual effects (shadows, rounded corners, text)

**Requirements**:
- Pillow (PIL) library

### 2. `scripts/verify_icons.py`
Verify that icon files exist and are valid.

```bash
python scripts/verify_icons.py
```

**Checks**:
- File existence
- Format validity
- Size information
- Embedded sizes (for ICO)
- Image mode

### 3. `scripts/preview_icons.py`
Preview the generated icons using system image viewer.

```bash
python scripts/preview_icons.py
```

**Features**:
- Opens PNG in default image viewer
- Opens ICO (256x256) in default image viewer
- Displays icon information

## Integration with PyInstaller

### Windows Build
The `build/encoder.spec` file references the Windows icon:

```python
exe = EXE(
    ...
    icon='assets/icon.ico',
    ...
)
```

### macOS/Linux Build
For macOS and Linux, the PNG icon can be referenced similarly or manually set as the application icon after build.

## Customization

### Modifying Icon Design

To customize the icon appearance, edit `scripts/generate_icons.py`:

1. **Colors**: Modify the color constants in `create_icon()`:
   ```python
   bg_color_top = (66, 133, 244, 255)    # Top background color
   bg_color_bottom = (33, 97, 212, 255)  # Bottom background color
   text_color = (255, 255, 255, 255)     # Text color
   ```

2. **Text**: Change the main text:
   ```python
   text = "TE"  # Change to your preferred text
   ```

3. **Size**: Adjust icon size when calling generation functions:
   ```python
   generate_ico(ico_path, size=512)  # Larger icon
   generate_png(png_path, size=512)
   ```

4. **Shapes**: Modify the rounded rectangle radius:
   ```python
   corner_radius = size // 6  # Adjust for more/less rounding
   ```

### Adding New Icon Sizes

To add new sizes, modify the `generate_ico()` function:

```python
sizes = [16, 32, 48, 64, 128, 256, 512]  # Add 512
```

## Troubleshooting

### Font Not Found
If custom fonts are not available, the script automatically falls back to the default font. This is normal behavior.

### Icons Not Appearing in Built Executable
1. Verify icons are generated: `python scripts/verify_icons.py`
2. Check `build/encoder.spec` has correct icon path
3. Ensure assets directory exists in build output
4. Rebuild with `--clean` flag

### Permission Errors
Ensure write permissions in the `assets/` directory:
```bash
# Linux/macOS
chmod +w assets/

# Windows: Run as Administrator if needed
```

## Requirements

### Python Dependencies
```bash
pip install pillow
```

### System Requirements
- Python 3.7+
- Pillow (PIL) library
- Write access to `assets/` directory

## File Structure

```
encoder/
├── assets/
│   ├── icon.ico          # Windows icon (multi-size)
│   └── icon.png          # macOS/Linux icon (256x256)
├── scripts/
│   ├── generate_icons.py # Icon generation script
│   ├── verify_icons.py   # Icon verification script
│   └── preview_icons.py  # Icon preview script
├── build/
│   └── encoder.spec      # PyInstaller configuration
└── docs/
    └── icons.md          # This documentation
```

## Best Practices

1. **Regenerate Before Build**: Always run `generate_icons.py` before building to ensure icons are up to date

2. **Version Control**: Consider whether to commit generated icons or regenerate them:
   - Commit if you want immediate availability
   - Regenerate if you want to track design changes in script

3. **Icon Sizes**: Include multiple sizes in ICO for best display quality across different Windows views

4. **Testing**: Use `verify_icons.py` after generation to ensure files are valid

5. **Backup**: Keep a backup of custom icon designs before modifying the generation script

## Future Enhancements

Possible improvements to the icon system:
- SVG support for vector-based icons
- Animated icons for loading states
- Platform-specific variations
- Dark/light theme variants
- Custom icon upload functionality
