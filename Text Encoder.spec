# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

# Cross-platform paths
main_script = 'src/main.py'
assets_dir = 'assets'

# Platform-specific icon
if sys.platform == 'win32':
    icon_path = 'assets/icon.ico'
else:
    icon_path = 'assets/icon.png'

# Collect all customtkinter data and binaries
customtkinter_datas, customtkinter_binaries, customtkinter_hiddenimports = collect_all('customtkinter')

# Collect pystray
pystray_datas, pystray_binaries, pystray_hiddenimports = collect_all('pystray')

# Collect pynput
pynput_datas, pynput_binaries, pynput_hiddenimports = collect_all('pynput')

a = Analysis(
    [main_script],
    pathex=['src'],
    binaries=customtkinter_binaries + pystray_binaries + pynput_binaries,
    datas=[
        (assets_dir, 'assets'),
        *customtkinter_datas,
        *pystray_datas,
        *pynput_datas,
    ],
    hiddenimports=[
        'ui.main_window',
        'ui.system_tray',
        'ui.sidebar',
        'ui.content_area',
        'hotkey.global_hotkey',
        'registry',
        'transformers.encoding',
        'transformers.ascii_encoding',
        'transformers.hashing',
        'transformers.text_processing',
        'transformers.special',
        'transformers.special_formats',
        'transformers.ciphers',
        'utils.transformation_worker',
        *customtkinter_hiddenimports,
        *pystray_hiddenimports,
        *pynput_hiddenimports,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Text Encoder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
