# -*- mode: python ; coding: utf-8 -*-
# Windows build → produces dist/GelCaptionTool.exe (single file)
# Run on a Windows machine: pyinstaller GelCaptionTool_win.spec --noconfirm
# Or use GitHub Actions: push to GitHub and the workflow builds it automatically.
#
# Icon: place app_icon.ico in this directory before building.
# To create it from a PNG: python3 make_icons.py your_icon.png

import os
_icon = 'app_icon.ico' if os.path.exists('app_icon.ico') else None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PIL._tkinter_finder',
        'numpy',
        'pptx',
        'pptx.util',
        'pptx.dml.color',
        'pptx.enum.text',
        'pptx.enum.shapes',
        'pptx.oxml.ns',
        'lxml',
        'lxml.etree',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

# Single-file exe: binaries and datas go directly into EXE (no COLLECT)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GelAnnotator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=_icon,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
