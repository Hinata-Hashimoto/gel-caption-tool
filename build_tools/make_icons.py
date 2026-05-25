#!/usr/bin/env python3
"""
Generate app_icon.icns (macOS) and app_icon.ico (Windows)
from a single square PNG.

Usage:
    python3 make_icons.py <source.png>

The source PNG should be at least 1024x1024 px and square.
Output files are written to the same directory as this script.
"""

import sys
import subprocess
import shutil
from pathlib import Path


def make_icns(src: Path, out_dir: Path):
    iconset = out_dir / "app_icon.iconset"
    iconset.mkdir(exist_ok=True)

    # Required sizes for macOS .icns
    entries = [
        ("icon_16x16.png",       16),
        ("icon_16x16@2x.png",    32),
        ("icon_32x32.png",       32),
        ("icon_32x32@2x.png",    64),
        ("icon_128x128.png",    128),
        ("icon_128x128@2x.png", 256),
        ("icon_256x256.png",    256),
        ("icon_256x256@2x.png", 512),
        ("icon_512x512.png",    512),
        ("icon_512x512@2x.png",1024),
    ]
    for fname, size in entries:
        subprocess.run(
            ["sips", "-z", str(size), str(size), str(src),
             "--out", str(iconset / fname)],
            check=True, capture_output=True,
        )

    dest = out_dir / "app_icon.icns"
    subprocess.run(["iconutil", "-c", "icns", str(iconset), "-o", str(dest)],
                   check=True)
    shutil.rmtree(iconset)
    print(f"✓ {dest}")


def make_ico(src: Path, out_dir: Path):
    from PIL import Image
    img = Image.open(src).convert("RGBA")
    dest = out_dir / "app_icon.ico"
    img.save(str(dest), format="ICO",
             sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
    print(f"✓ {dest}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    src = Path(sys.argv[1])
    if not src.exists():
        print(f"Error: {src} not found")
        sys.exit(1)

    out_dir = Path(__file__).parent
    import platform

    if platform.system() == "Darwin":
        if shutil.which("sips") and shutil.which("iconutil"):
            make_icns(src, out_dir)
        else:
            print("sips/iconutil not found — skipping .icns")

    try:
        make_ico(src, out_dir)
    except ImportError:
        print("Pillow not installed — skipping .ico")
        print("  pip install Pillow")

    print("\nNext steps:")
    print("  Mac .app : pyinstaller GelCaptionTool.spec --noconfirm")
    print("  Win .exe : push to GitHub → Actions builds it automatically")
