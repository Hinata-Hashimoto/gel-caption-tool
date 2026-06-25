# -*- mode: python ; coding: utf-8 -*-
# Windows build → produces dist/GelCaptionTool.exe (single file)
# Run on a Windows machine: pyinstaller build_tools/GelCaptionTool_win.spec --noconfirm
# Or use GitHub Actions: push to GitHub and the workflow builds it automatically.
#
# Icon: place app_icon.ico in assets/ before building.
# To create it from a PNG: python3 build_tools/make_icons.py your_icon.png

import os
_root = os.path.dirname(SPECPATH)
_icon_path = os.path.join(_root, 'assets', 'app_icon.ico')
_icon = _icon_path if os.path.exists(_icon_path) else None

a = Analysis(
    [os.path.join(_root, 'main.py')],
    pathex=[_root],
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
