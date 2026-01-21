# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

# Cross-platform paths
main_script = 'src/main.py'
assets_dir = 'assets'

# Platform-specific icon
if sys.platform == 'win32':
    icon_path = 'assets/icon.ico'
else:
    icon_path = 'assets/icon.png'

a = Analysis(
    [main_script],
    pathex=['src'],
    binaries=[],
    datas=[(assets_dir, 'assets')],
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
        'utils.transformation_worker'
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
