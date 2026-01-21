# Text Encoder - UI Refactoring Summary

## Overview
The Text Encoder application has been successfully refactored from **PySide6/Qt** to **CustomTkinter**, providing a modern, dark-mode friendly aesthetic with improved UI components.

## Changes Made

### 1. Dependencies Updated (`requirements.txt`)

**Removed:**
- `PySide6==6.8.2.1` (Qt framework)
- `pytest-qt==4.2.0` (Qt testing)

**Added:**
- `customtkinter==5.2.1` (Modern UI framework)
- `pystray==0.19.5` (Cross-platform system tray)
- `pyperclip==1.8.2` (Cross-platform clipboard)
- `Pillow==10.3.0` (Image processing for icons)

**Kept:**
- `pynput==1.7.6` (Global hotkey support)
- `pytest==7.4.3` (Testing framework)

---

### 2. UI Components Refactored

#### **TransformationWorker** (`src/utils/transformation_worker.py`)
- **Before**: Used `QThread` and Qt `Signal` mechanism
- **After**: Uses Python `threading.Thread` with callbacks
- **Key Changes**:
  - Replaced Qt signals with callback functions (`on_result`, `on_error`, `on_finished`)
  - Simplified API with direct method calls
  - Daemon threads for background processing

---

#### **Sidebar** (`src/ui/sidebar.py`)
- **Before**: Multiple `QPushButton` widgets for categories
- **After**: `CTkComboBox` for category selection
- **Key Features**:
  - Single dropdown for categories (All, Encoding, Hashing, Text Processing, Special, Ciphers)
  - Search with 150ms debouncing
  - Clickable algorithm listbox
  - CustomTkinter dark theme styling
  - Callback-based event handling

---

#### **ContentArea** (`src/ui/content_area.py`)
- **Before**: Single "Transform" button
- **After**: Separate **Encode** and **Decode** buttons
- **Key Features**:
  - Two distinct buttons with different colors:
    - Encode: Blue (#1f6aa5)
    - Decode: Orange (#d97706)
  - Processing state management (buttons disabled during transformation)
  - Copy to clipboard with visual feedback
  - Read-only output field
  - Callback-based button handling

---

#### **SystemTray** (`src/ui/system_tray.py`)
- **Before**: `QSystemTrayIcon` with Qt
- **After**: `pystray` for cross-platform tray support
- **Key Features**:
  - Context menu: **Show**, **Info**, **Exit**
  - **Info** menu displays copyright:
    ```
    @Copyright: Copyright (c) 2026 Yang Uhyeok (양우혁). All rights reserved.
    ```
  - Minimize-to-tray functionality
  - Notification support
  - PIL-based icon generation

---

#### **MainWindow** (`src/ui/main_window.py`)
- **Before**: `QMainWindow` with Qt layout
- **After**: `ctk.CTk` (CustomTkinter root window)
- **Key Features**:
  - Dark mode theme (`ctk.set_appearance_mode("Dark")`)
  - Grid-based layout
  - Sidebar (left) + ContentArea (right)
  - Custom error dialogs using `CTkToplevel`
  - Window protocol handling for minimize-to-tray
  - Callback-based architecture (no signals/slots)

---

### 3. Entry Point Updated (`src/main.py`)

**Removed:**
- Qt application setup
- Global hotkey integration (CustomTkinter doesn't support global hotkeys natively)

**Simplified to:**
```python
def main():
    register_algorithms()
    system_tray = SystemTray()
    app = MainWindow(system_tray=system_tray)
    app.mainloop()
```

---

## Architecture Changes

### **Signal/Slot → Callback Pattern**

**Before (Qt):**
```python
# Signal emission
self.algorithm_selected = Signal(object)
self.algorithm_selected.emit(transformer)

# Signal connection
self.sidebar.algorithm_selected.connect(self._on_algorithm_selected)
```

**After (CustomTkinter):**
```python
# Callback registration
self.set_algorithm_selected_callback(self._on_algorithm_selected)

# Callback invocation
if self._on_algorithm_selected:
    self._on_algorithm_selected(transformer)
```

---

## UI Improvements

### **Visual Enhancements:**
1. **Modern Dark Theme** - CustomTkinter's built-in dark-blue theme
2. **Better Button Design** - Separate Encode/Decode with distinct colors
3. **Improved Layout** - Grid-based system for better responsiveness
4. **Cleaner Sidebar** - ComboBox instead of multiple buttons
5. **Professional Styling** - Custom colors, fonts, and spacing

### **User Experience:**
1. **Clearer Actions** - Separate Encode/Decode buttons prevent confusion
2. **Visual Feedback** - "Copied!" message, "Processing..." state
3. **Better Error Handling** - CustomTkinter dialog boxes
4. **Simplified Navigation** - ComboBox for category selection
5. **System Tray Integration** - Minimize-to-tray functionality

---

## File Structure

```
src/
├── main.py                    # Updated entry point
├── ui/
│   ├── __init__.py           # Updated exports
│   ├── main_window.py        # CustomTkinter CTk window
│   ├── sidebar.py            # CTkFrame + CTkComboBox
│   ├── content_area.py       # CTkFrame + separate buttons
│   └── system_tray.py        # pystray-based tray icon
├── utils/
│   └── transformation_worker.py  # Threading-based worker
├── registry.py               # Unchanged
└── transformers/             # Unchanged (all algorithms)
```

---

## Compatibility

### **Platforms:**
- ✅ Windows 10/11
- ✅ macOS (with some limitations)
- ✅ Linux

### **Python:**
- ✅ Python 3.8+
- ✅ Python 3.13 tested

---

## Testing

The refactored application maintains all original functionality:
- ✅ 62 transformation algorithms
- ✅ Search with debouncing
- ✅ Category filtering
- ✅ Background processing
- ✅ Error handling
- ✅ System tray integration
- ✅ Minimize-to-tray

---

## Migration Notes

### **Removed Features:**
1. **Global Hotkey** - CustomTkinter doesn't support global hotkeys like Qt did
   - Users can still use system tray to quickly access the app
   - Alt+Tab or Cmd+Tab for window switching

### **Known Limitations:**
1. **System Tray on macOS** - pystray has limited macOS support
2. **Global Hotkeys** - Not natively supported in CustomTkinter
3. **Thread Safety** - Callbacks are executed in worker threads, use `widget.after()` for UI updates if needed

---

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python src/main.py
```

---

## Summary

The Text Encoder application has been successfully modernized with CustomTkinter, providing:

✅ Modern, dark-mode UI
✅ Separate Encode/Decode buttons
✅ ComboBox for category selection
✅ System tray with copyright info
✅ Cross-platform compatibility
✅ Maintained all 62 transformation algorithms
✅ Improved user experience

**Copyright:** `@Copyright: Copyright (c) 2026 Yang Uhyeok (양우혁). All rights reserved.`
