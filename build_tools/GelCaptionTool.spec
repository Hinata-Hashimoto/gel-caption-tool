# -*- mode: python ; coding: utf-8 -*-
# macOS build → produces dist/GelCaptionTool.app
# Run from project root: pyinstaller build_tools/GelCaptionTool.spec --noconfirm
#
# Icon: place app_icon.icns in assets/ before building.
# To create it from a PNG: python3 build_tools/make_icons.py your_icon.png

import os
_root = os.path.dirname(SPECPATH)
_icon_path = os.path.join(_root, 'assets', 'app_icon.icns')
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
        'tkinterdnd2',
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
