# System Tray Integration

## Overview

Text Encoder application includes system tray integration allowing users to minimize the application to the system tray instead of closing it completely.

## Features

### 1. Minimize to System Tray
- When clicking the X button on the main window, the application minimizes to the system tray instead of closing
- A notification appears confirming the minimization
- The application continues running in the background

### 2. Restore Window
- **Double-click** the tray icon to restore the main window
- Or right-click and select "Show" from the context menu
- The window is brought to front and activated

### 3. Context Menu

Right-clicking the tray icon shows a context menu with three options:

#### Show
- Restores and activates the main window
- Same as double-clicking the icon

#### Info
- Displays an about dialog with application information:
  - Application name
  - Description
  - Version
  - Platform information

#### Exit
- Properly closes the application
- Hides the tray icon
- Quits the application

## Icon Support

### Platform-Specific Icons

The application tries to load custom icons from the `assets` directory:

**Windows:**
- Path: `assets/icon.ico`
- Format: ICO file
- Recommended size: 16x16, 32x32, 48x48 (multiple sizes in one file)

**macOS/Linux:**
- Path: `assets/icon.png`
- Format: PNG file
- Recommended size: 32x32 or 48x48 pixels

### Fallback Icon

If no custom icon is found, the application uses Qt's standard `SP_ComputerIcon` as a fallback, ensuring the system tray always has an icon.

## Implementation Details

### Files

1. **`src/ui/system_tray.py`** - SystemTray class
   - Creates and manages the system tray icon
   - Handles context menu creation
   - Provides signals for window restoration and application exit
   - Shows balloon notifications

2. **`src/ui/main_window.py`** - MainWindow integration
   - Accepts system_tray parameter in constructor
   - Overrides `closeEvent` to minimize to tray instead of closing
   - Implements `_restore_from_tray()` and `_exit_from_tray()` methods

3. **`src/main.py`** - Application initialization
   - Creates SystemTray instance
   - Passes it to MainWindow

### Key Features

#### Signal/Slot Architecture

```python
# SystemTray signals
show_requested = Signal()  # Emitted when Show is clicked
exit_requested = Signal()  # Emitted when Exit is clicked

# MainWindow connections
system_tray.show_requested.connect(window._restore_from_tray)
system_tray.exit_requested.connect(window._exit_from_tray)
```

#### Cross-Platform Detection

```python
# Check if system tray is available
if QSystemTrayIcon.isSystemTrayAvailable():
    # Create and show tray icon
else:
    # Fall back to normal window behavior
```

#### Icon Loading

```python
# Platform-specific icon paths
if sys.platform == "win32":
    icon_file = assets_dir / "icon.ico"
else:
    icon_file = assets_dir / "icon.png"

# Fallback to standard Qt icon
if not icon_file.exists():
    icon = app.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
```

## Adding Custom Icons

### Option 1: Use Existing Icon

Place your icon files in the `assets` directory:
- `assets/icon.ico` for Windows
- `assets/icon.png` for macOS/Linux

### Option 2: Create Simple Icons

#### Using Online Tools
- [icoconvert.com](https://icoconvert.com/) - Create ICO files from PNG
- [favicon.io](https://favicon.io/) - Generate icons from text or images

#### Using Python (PIL/Pillow)

```python
from PIL import Image

# Open PNG file
img = Image.open("icon.png")

# Save as ICO (Windows)
img.save("icon.ico", format="ICO", sizes=[(16,16), (32,32), (48,48)])
```

## Testing

Run the test script to verify system tray functionality:

```bash
python test_system_tray.py
```

Or run the main application:

```bash
python src/main.py
```

### Test Checklist

- [ ] Application starts with tray icon visible
- [ ] Closing window with X button minimizes to tray
- [ ] Notification appears when minimizing to tray
- [ ] Double-clicking tray icon restores window
- [ ] Right-click shows context menu (Show, Info, Exit)
- [ ] Show menu item restores window
- [ ] Info menu item shows about dialog
- [ ] Exit menu item closes application
- [ ] Custom icon displays correctly (if provided)
- [ ] Fallback icon displays if no custom icon

## Troubleshooting

### Tray Icon Not Showing

**Problem:** Tray icon doesn't appear in the system tray

**Solutions:**
1. Check if system tray is supported on your platform
2. Verify icon file exists and is valid format
3. Check application console for warning messages
4. On Windows: Ensure "Show hidden icons" is enabled in taskbar settings

### Notification Not Appearing

**Problem:** Balloon notifications don't show

**Solutions:**
1. Check if `QSystemTrayIcon.supportsMessages()` returns True
2. Verify OS notification settings are enabled
3. Some Linux distributions may not support balloon notifications

### Window Won't Close

**Problem:** Clicking Exit doesn't close the application

**Solutions:**
1. Check console for error messages
2. Verify signal connections are properly set up
3. Try closing via window's X button (should minimize to tray)

## Platform-Specific Notes

### Windows
- Full system tray support
- Balloon notifications supported
- ICO format recommended for best quality

### macOS
- System tray supported (called "Menu Bar" on macOS)
- Notifications may appear as OS X notifications
- PNG format recommended

### Linux
- System tray support varies by desktop environment
- Some distributions require system tray applet/indicator
- PNG format recommended
- Balloon notifications may not work on all distributions

## Future Enhancements

Possible improvements for future versions:

1. **Custom Notifications**: Add notification settings (enable/disable, duration)
2. **Minimize on Startup**: Option to start minimized to tray
3. **Tray Icon Animation**: Animated icon during processing
4. **Quick Actions**: Add common transformations to tray menu
5. **Icon Themes**: Support for multiple icon themes
6. **Status Indicator**: Show current algorithm or processing status in tray
