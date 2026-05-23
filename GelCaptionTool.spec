# -*- mode: python ; coding: utf-8 -*-
# macOS build → produces dist/GelCaptionTool.app
# Run: pyinstaller GelCaptionTool.spec --noconfirm
#
# Icon: place app_icon.icns in this directory before building.
# To create it from a PNG: python3 make_icons.py your_icon.png

import os
_icon = 'app_icon.icns' if os.path.exists('app_icon.icns') else None

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

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GelCaptionTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=_icon,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GelCaptionTool',
)
app = BUNDLE(
    coll,
    name='GelAnnotator.app',
    icon=_icon,
    bundle_identifier='jp.ac.aizawalab.GelCaptionTool',
    info_plist={
        'NSHighResolutionCapable': True,
        'CFBundleShortVersionString': '1.0.0',
    },
)
