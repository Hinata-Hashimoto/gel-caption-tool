import sys

try:
    import tkinter as tk
except ModuleNotFoundError:
    from i18n import t
    print(t("err_no_tkinter"))
    sys.exit(1)

from app import GelCaptionApp

if __name__ == "__main__":
    root = tk.Tk()
    GelCaptionApp(root)
    root.mainloop()
