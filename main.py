import sys

try:
    import tkinter as tk
except ModuleNotFoundError:
    from i18n import t
    print(t("err_no_tkinter"))
    sys.exit(1)

try:
    from tkinterdnd2 import TkinterDnD
    _HAS_DND = True
except ImportError:
    _HAS_DND = False

from app import GelCaptionApp

if __name__ == "__main__":
    root = TkinterDnD.Tk() if _HAS_DND else tk.Tk()
    GelCaptionApp(root)
    root.mainloop()
