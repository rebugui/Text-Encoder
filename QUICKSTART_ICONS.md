# Quick Start Guide - Icon Generation

## Generate Icons
```bash
python scripts/generate_icons.py
```

## Verify Icons
```bash
python scripts/verify_icons.py
```

## Preview Icons
```bash
python scripts/preview_icons.py
```

## Build Application
```bash
# Windows
pyinstaller build/encoder.spec --clean --onefile

# macOS
pyinstaller build/encoder.spec --clean --onefile --windowed

# Linux
pyinstaller build/encoder.spec --clean --onefile
```

## Generated Files
- `assets/icon.ico` - Windows icon (multi-size: 16, 32, 48, 64, 128, 256)
- `assets/icon.png` - macOS/Linux icon (256x256)

## Documentation
- See `docs/icons.md` for detailed documentation
- See `docs/icon_implementation_summary.md` for implementation details
