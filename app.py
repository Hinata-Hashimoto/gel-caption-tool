import copy
import csv
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from PIL import Image

from annotation_model import AppState, SampleAnnotation
from canvas_widget import GelCanvas
from ladder_data import LADDERS
from i18n import t, save_lang, get_lang

GITHUB_URL   = "https://github.com/Hinata-Hashimoto/gel-caption-tool"
HOMEPAGE_URL = "https://sites.google.com/view/hinatahashimoto"

# ── Sidebar colour constants (light theme → black text) ───────────────────────
SBG   = "#f4f4f4"   # sidebar background
S_FG  = "#333333"   # section header text
L_FG  = "#111111"   # label / button text
B_BG  = "#e2e2e2"   # button background
B_ACT = "#c8c8c8"   # button active background
B_SEL = "#0055bb"   # selected-mode button background


class GelCaptionApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("GelAnnotator")
        self.root.geometry("1200x760")
        self.root.minsize(800, 560)

        self.state = AppState()
        self._csv_names: list[str] = []
        self._source_path: str = ""

        self._build_menu()
        self._build_ui()
        self._bind_keys()

    # ── menu ──────────────────────────────────────────────────────────────────

    def _build_menu(self):
        mb = tk.Menu(self.root)

        fm = tk.Menu(mb, tearoff=0)
        fm.add_command(label=t("menu_open_image"), command=self._open_image, accelerator="Ctrl+O")
        fm.add_command(label=t("menu_open_lumi"), command=self._open_lumi)
        fm.add_separator()
        fm.add_command(label=t("menu_export_png"), command=self._export_png, accelerator="Ctrl+S")
        fm.add_command(label=t("menu_export_pptx"), command=self._export_pptx, accelerator="Ctrl+Shift+S")
        fm.add_command(label=t("menu_export_svg"), command=self._export_svg)
        fm.add_separator()
        fm.add_command(label=t("menu_quit"), command=self.root.quit)
        mb.add_cascade(label=t("menu_file"), menu=fm)

        em = tk.Menu(mb, tearoff=0)
        em.add_command(label=t("menu_undo"), command=self._undo, accelerator="Ctrl+Z")
        em.add_command(label=t("menu_reset_ladder"), command=self._reset_ladder, accelerator="R")
        em.add_command(label=t("menu_clear_wells"), command=self._clear_wells)
        em.add_command(label=t("menu_clear_bands"), command=self._clear_bands)
        mb.add_cascade(label=t("menu_edit"), menu=em)

        lm = tk.Menu(mb, tearoff=0)
        lm.add_command(label="日本語", command=lambda: self._set_lang("ja"))
        lm.add_command(label="English", command=lambda: self._set_lang("en"))
        mb.add_cascade(label=t("menu_language"), menu=lm)

        hm = tk.Menu(mb, tearoff=0)
        hm.add_command(label=t("help_github"),   command=lambda: webbrowser.open(GITHUB_URL))
        hm.add_command(label=t("help_homepage"), command=lambda: webbrowser.open(HOMEPAGE_URL))
        mb.add_cascade(label=t("menu_help"), menu=hm)

        self.root.config(menu=mb)

    # ── UI layout ─────────────────────────────────────────────────────────────

    def _build_ui(self):
        self._status_var = tk.StringVar()  # kept for internal use, not displayed

        main = tk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True)

        # Left sidebar
        self._sb_frame = tk.Frame(main, width=200, bg=SBG)
        self._sb_frame.pack(side=tk.LEFT, fill=tk.Y)
        self._sb_frame.pack_propagate(False)

        self._build_sidebar(self._sb_frame)

        # Image canvas
        canvas_frame = tk.Frame(main, bg="#2a2a2a")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.gel_canvas = GelCanvas(canvas_frame, self.state,
                                    on_status=self._set_status, bg="#2a2a2a")
        self.gel_canvas.pack(fill=tk.BOTH, expand=True)
        self.gel_canvas.on_crop_done = lambda: self._sync_mode_btns("NORMAL")

    def _build_sidebar(self, p):

        def section(text):
            tk.Label(p, text=text, bg=SBG, fg=S_FG,
                     font=("Helvetica", 7, "bold")).pack(pady=(4, 1))

        def sep():
            tk.Frame(p, height=1, bg="#cccccc").pack(fill=tk.X, padx=8, pady=2)

        def btn(text, cmd, width=18):
            b = tk.Button(p, text=text, command=cmd,
                          bg=B_BG, fg=L_FG, relief=tk.GROOVE,
                          padx=2, pady=1, width=width, cursor="hand2",
                          activebackground=B_ACT, activeforeground=L_FG,
                          font=("Helvetica", 8))
            b.pack(padx=5, pady=1)
            return b

        # ── Mode buttons ──────────────────────────────────────────────────────
        section(t("sec_mode"))
        self._btn_ladder = btn(t("btn_ladder_mode"), lambda: self._set_mode("LADDER"))
        self._btn_band   = btn(t("btn_band_mode"),   lambda: self._set_mode("BAND"))
        self._btn_crop   = btn(t("btn_crop_mode"),   lambda: self._set_mode("CROP"))
        self._btn_region = btn(t("btn_region_mode"), self._set_mode_region)

        # ── Rotate ───────────────────────────────────────────────────────────────
        sep()
        section(t("sec_transform"))

        # 90° rotation
        rrow = tk.Frame(p, bg=SBG)
        rrow.pack(fill=tk.X, padx=5, pady=1)
        for label, ccw in [(t("btn_rotate_ccw"), True), (t("btn_rotate_cw"), False)]:
            tk.Button(rrow, text=label, command=lambda c=ccw: self._rotate_image(ccw=c),
                      bg=B_BG, fg=L_FG, relief=tk.GROOVE, font=("Helvetica", 8),
                      cursor="hand2", activebackground=B_ACT,
                      padx=3, pady=1).pack(side=tk.LEFT, expand=True, fill=tk.X)

        sep()
        btn(t("btn_toggle_wb"), self._toggle_wb)

        # ── Ladder type ───────────────────────────────────────────────────────
        sep()
        section(t("sec_ladder_type"))
        self._ladder_var = tk.StringVar(value="100bp DNA")
        self._ladder_combo = ttk.Combobox(p, textvariable=self._ladder_var,
                                          values=list(LADDERS.keys()), state="readonly", width=18)
        self._ladder_combo.pack(padx=5, pady=2)
        self._ladder_combo.bind("<<ComboboxSelected>>",
                                lambda e: setattr(self.state, 'ladder_type', self._ladder_var.get()))

        btn(t("btn_edit_ladders"),  self._edit_ladders)
        btn(t("btn_reset_ladder"),  self._reset_ladder)
        btn(t("btn_skip_band"),     self._skip_ladder)

        # Ladder line style
        section(t("sec_ladder_style"))
        self._line_style_var = tk.StringVar(value="short")
        row_ls = tk.Frame(p, bg=SBG)
        row_ls.pack(fill=tk.X, padx=6, pady=1)
        for val, label in [("full", t("lbl_line_full")), ("short", t("lbl_line_short"))]:
            tk.Radiobutton(
                row_ls, text=label, variable=self._line_style_var,
                value=val, bg=SBG, fg=L_FG, activebackground=SBG,
                selectcolor=SBG, font=("Helvetica", 8),
                command=self._apply_line_style
            ).pack(side=tk.LEFT, padx=2)

        # ── Sample wells ──────────────────────────────────────────────────────
        sep()
        section(t("sec_wells"))

        self._left_x_var  = tk.StringVar(value="0")
        self._right_x_var = tk.StringVar(value="0")
        self._num_wells_var = tk.StringVar(value="2")

        # Left / Right X — manual entry
        for label, var in [
            (t("lbl_left_x"),  self._left_x_var),
            (t("lbl_right_x"), self._right_x_var),
        ]:
            row = tk.Frame(p, bg=SBG)
            row.pack(fill=tk.X, padx=6, pady=1)
            tk.Label(row, text=label, bg=SBG, fg=L_FG,
                     width=4, anchor=tk.W, font=("Helvetica", 8)).pack(side=tk.LEFT)
            tk.Entry(row, textvariable=var, width=9,
                     font=("Helvetica", 8)).pack(side=tk.LEFT, padx=2)

        btn(t("btn_pick_wells"), self._pick_wells_by_click)

        # Num wells
        row3 = tk.Frame(p, bg=SBG)
        row3.pack(fill=tk.X, padx=6, pady=1)
        tk.Label(row3, text=t("lbl_num_wells"), bg=SBG, fg=L_FG,
                 width=5, anchor=tk.W, font=("Helvetica", 8)).pack(side=tk.LEFT)
        tk.Entry(row3, textvariable=self._num_wells_var, width=5,
                 font=("Helvetica", 8)).pack(side=tk.LEFT, padx=2)

        # Font size control
        section(t("sec_font"))
        self._font_size_var = tk.StringVar(value="10")
        frow = tk.Frame(p, bg=SBG)
        frow.pack(padx=5, pady=1)
        tk.Button(frow, text="－ [−]", command=self._font_smaller,
                  bg=B_BG, fg=L_FG, relief=tk.GROOVE,
                  font=("Helvetica", 8), cursor="hand2",
                  activebackground=B_ACT, padx=4, pady=1).pack(side=tk.LEFT)
        tk.Label(frow, textvariable=self._font_size_var, bg=SBG, fg=L_FG,
                 font=("Helvetica", 8), width=3, anchor=tk.CENTER).pack(side=tk.LEFT)
        tk.Button(frow, text="＋ [=]", command=self._font_larger,
                  bg=B_BG, fg=L_FG, relief=tk.GROOVE,
                  font=("Helvetica", 8), cursor="hand2",
                  activebackground=B_ACT, padx=4, pady=1).pack(side=tk.LEFT)

        sep()
        btn(t("btn_load_csv"),    self._load_csv)
        btn(t("btn_paste_names"), self._paste_names)
        btn(t("btn_apply_wells"), self._apply_wells)
        btn(t("btn_clear_wells"), self._clear_wells)

        # ── Export ────────────────────────────────────────────────────────────
        sep()
        section(t("sec_export"))
        btn(t("btn_export_png"),  self._export_png)
        btn(t("btn_export_pptx"), self._export_pptx)
        btn(t("btn_export_svg"),  self._export_svg)

        # Mode button references (for highlighting active mode)
        self._mode_btns = {
            "LADDER": self._btn_ladder,
            "BAND":   self._btn_band,
            "CROP":   self._btn_crop,
            "REGION": self._btn_region,
        }

    # ── key bindings ──────────────────────────────────────────────────────────

    def _bind_keys(self):
        for key, fn in [
            ("<Control-o>", self._open_image),
            ("<Control-z>", self._undo),
            ("<Return>",    self._on_enter),
            ("<Escape>",    lambda e: self._set_mode("NORMAL")),
        ]:
            self.root.bind(key, lambda e, f=fn: f())

        for key, mode in [
            ("<l>", "LADDER"), ("<L>", "LADDER"),
            ("<b>", "BAND"),   ("<B>", "BAND"),
            ("<c>", "CROP"),   ("<C>", "CROP"),
        ]:
            self.root.bind(key, lambda e, m=mode: self._set_mode(m))

        for key in ("<s>", "<S>"):
            self.root.bind(key, lambda e: self._pick_wells_by_click())
        for key in ("<p>", "<P>"):
            self.root.bind(key, lambda e: self._paste_names())
        for key in ("<a>", "<A>"):
            self.root.bind(key, lambda e: self._apply_wells())
        self.root.bind("<equal>", lambda e: self._font_larger())
        self.root.bind("<plus>",  lambda e: self._font_larger())
        self.root.bind("<minus>", lambda e: self._font_smaller())
        for key in ("<g>", "<G>"):
            self.root.bind(key, lambda e: self._set_mode_region())
        self.root.bind("<Right>", lambda e: self._skip_ladder())
        self.root.bind("<Control-s>", lambda e: self._export_png())
        self.root.bind("<Control-S>", lambda e: self._export_pptx())

        for key in ("<w>", "<W>"):
            self.root.bind(key, lambda e: self._toggle_wb())
        for key in ("<r>", "<R>"):
            self.root.bind(key, lambda e: self._reset_ladder())

    # ── mode management ───────────────────────────────────────────────────────

    def _sync_mode_btns(self, mode: str):
        for m, b in self._mode_btns.items():
            if m == mode:
                b.config(bg=B_SEL, fg="white", activebackground="#0044aa")
            else:
                b.config(bg=B_BG, fg=L_FG, activebackground=B_ACT)

    def _set_mode(self, mode: str):
        self.gel_canvas.set_mode(mode)
        self._sync_mode_btns(mode)
        hints = {
            "NORMAL": t("hint_normal"),
            "LADDER": t("hint_ladder"),
            "BAND":   t("hint_band"),
            "CROP":   t("hint_crop"),
            "REGION": t("hint_region"),
        }
        self._set_status(hints.get(mode, ""))

    def _on_enter(self):
        pass  # crop is now applied on mouse release

    def _set_mode_region(self):
        if self.state.image_visible is None:
            return
        self.gel_canvas.region_callback = self._on_region_pick
        self._set_mode("REGION")

    def _on_region_pick(self, x1: float, x2: float):
        from tkinter import simpledialog
        from annotation_model import RegionAnnotation
        name = simpledialog.askstring(t("dlg_region_label"), t("region_prompt"), parent=self.root)
        self._sync_mode_btns("NORMAL")
        if name and name.strip():
            self.state.push_undo('region')
            self.state.region_annotations.append(RegionAnnotation(x_start=x1, x_end=x2, name=name.strip()))
            self.gel_canvas.refresh()
            self._set_status(t("msg_region_added", name=name.strip()))

    # ── file operations ───────────────────────────────────────────────────────

    @staticmethod
    def _load_image(path: str) -> Image.Image:
        """Open any image and return an 8-bit RGB PIL Image.
        16-bit / 32-bit images are normalised with 1–99 percentile stretch."""
        img = Image.open(path)
        if img.mode in ("I;16", "I;16B", "I;16L", "I", "F"):
            arr = np.array(img).astype(np.float32)
            lo, hi = np.percentile(arr, 1), np.percentile(arr, 99)
            if hi > lo:
                arr = (arr - lo) / (hi - lo) * 255.0
            arr = np.clip(arr, 0, 255).astype(np.uint8)
            arr = 255 - arr  # invert: bright signal → dark bands on white background
            return Image.fromarray(arr, mode="L").convert("RGB")
        return img.convert("RGB")

    def _open_image(self):
        path = filedialog.askopenfilename(
            title=t("dlg_open_image"),
            filetypes=[(t("ft_image"), "*.png *.jpg *.jpeg *.tif *.tiff *.bmp"),
                       (t("ft_all"), "*.*")]
        )
        if not path:
            return
        try:
            img = self._load_image(path)
            self.state.image_visible = img
            self.state.image_lumi = None
            self.state.wb_mode = False
            self.state.show_lumi = False
            self.state.ladder_annotations.clear()
            self.state.sample_annotations.clear()
            self.state.band_markers.clear()
            self.state.undo_history.clear()
            self._source_path = path
            self.root.after(50, self.gel_canvas.refresh)
            self._set_status(t("msg_load_complete", name=path.split('/')[-1]))
        except Exception as exc:
            messagebox.showerror(t("err_title"), t("msg_open_error", exc=exc))

    def _open_lumi(self):
        path = filedialog.askopenfilename(
            title=t("dlg_open_lumi"),
            filetypes=[(t("ft_image"), "*.png *.jpg *.jpeg *.tif *.tiff *.bmp"),
                       (t("ft_all"), "*.*")]
        )
        if not path:
            return
        if self.state.image_visible is None:
            messagebox.showwarning(t("warn_title"), t("msg_open_visible_first"))
            return
        try:
            img = self._load_image(path)
            self.state.image_lumi = img
            self.state.wb_mode = True
            self._set_status(t("msg_wb_active", name=path.split('/')[-1]))
        except Exception as exc:
            messagebox.showerror(t("err_title"), t("msg_open_error", exc=exc))

    def _rotate_image(self, ccw: bool):
        if self.state.image_visible is None:
            return
        has_annot = (self.state.ladder_annotations or
                     self.state.sample_annotations or
                     self.state.band_markers or
                     self.state.region_annotations)
        if has_annot:
            if not messagebox.askyesno(t("confirm_title"), t("msg_rotate_confirm")):
                return
        self.state.push_undo('rotate')
        direction = Image.ROTATE_90 if ccw else Image.ROTATE_270
        self.state.image_visible = self.state.image_visible.transpose(direction)
        if self.state.image_lumi is not None:
            self.state.image_lumi = self.state.image_lumi.transpose(direction)
        self.state.ladder_annotations.clear()
        self.state.sample_annotations.clear()
        self.state.band_markers.clear()
        self.state.region_annotations.clear()
        self.gel_canvas.refresh()
        self._set_status(t("msg_rotated"))

    def _toggle_wb(self):
        if not self.state.wb_mode or self.state.image_lumi is None:
            self._set_status(t("msg_wb_inactive"))
            return
        self.state.show_lumi = not self.state.show_lumi
        label = t("msg_lumi_image") if self.state.show_lumi else t("msg_visible_image")
        self._set_status(t("msg_showing", label=label))
        self.gel_canvas.refresh()

    # ── ladder ────────────────────────────────────────────────────────────────

    def _edit_ladders(self):
        import ladder_data as ld

        # Work on a local copy; apply only on close
        ladders_copy = copy.deepcopy(ld.LADDERS)
        units_copy   = copy.deepcopy(ld.LADDER_UNITS)

        dlg = tk.Toplevel(self.root)
        dlg.title(t("dlg_edit_ladders"))
        dlg.geometry("530x300")
        dlg.resizable(True, True)
        dlg.transient(self.root)
        dlg.grab_set()

        # ── Left: listbox ────────────────────────────────────────────
        left = tk.Frame(dlg, padx=8, pady=8)
        left.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(left, text=t("dlg_ladder_list"), font=("Helvetica", 10, "bold")).pack(anchor=tk.W)

        lb_wrap = tk.Frame(left)
        lb_wrap.pack(fill=tk.BOTH, expand=True)
        lb = tk.Listbox(lb_wrap, width=14, height=10,
                        selectmode=tk.SINGLE, exportselection=False)
        sb = tk.Scrollbar(lb_wrap, orient=tk.VERTICAL, command=lb.yview)
        lb.config(yscrollcommand=sb.set)
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        btn_row = tk.Frame(left)
        btn_row.pack(fill=tk.X, pady=(4, 0))
        tk.Button(btn_row, text=t("btn_new"), width=6,
                  command=lambda: new_entry()).pack(side=tk.LEFT)
        tk.Button(btn_row, text=t("btn_delete"), width=5,
                  command=lambda: delete_entry()).pack(side=tk.LEFT, padx=4)

        # ── Right: edit fields ───────────────────────────────────────
        right = tk.Frame(dlg, padx=10, pady=8)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(right, text=t("dlg_ladder_detail"), font=("Helvetica", 10, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 6))

        name_var  = tk.StringVar()
        unit_var  = tk.StringVar(value="bp")
        sizes_var = tk.StringVar()

        tk.Label(right, text=t("lbl_name")).grid(row=1, column=0, sticky=tk.W)
        tk.Entry(right, textvariable=name_var, width=24).grid(
            row=1, column=1, sticky=tk.EW, pady=2)

        tk.Label(right, text=t("lbl_unit")).grid(row=2, column=0, sticky=tk.W)
        urow = tk.Frame(right)
        urow.grid(row=2, column=1, sticky=tk.W, pady=2)
        tk.Radiobutton(urow, text="bp",  variable=unit_var, value="bp" ).pack(side=tk.LEFT)
        tk.Radiobutton(urow, text="kDa", variable=unit_var, value="kDa").pack(side=tk.LEFT)

        tk.Label(right, text=t("lbl_sizes"), justify=tk.LEFT).grid(
            row=3, column=0, sticky=tk.NW, pady=(8, 0))
        tk.Entry(right, textvariable=sizes_var, width=28).grid(
            row=3, column=1, sticky=tk.EW, pady=(8, 0))

        right.columnconfigure(1, weight=1)
        tk.Button(right, text=t("btn_save_entry"), command=lambda: save_entry()).grid(
            row=4, column=1, sticky=tk.E, pady=(12, 0))

        # ── State ────────────────────────────────────────────────────
        _sel = [None]  # currently selected ladder name

        def refresh_list(select_name=None):
            lb.delete(0, tk.END)
            for name in ladders_copy:
                lb.insert(tk.END, name)
            if select_name and select_name in ladders_copy:
                idx = list(ladders_copy.keys()).index(select_name)
                lb.selection_set(idx)
                lb.see(idx)
                load_entry(select_name)

        def load_entry(name):
            _sel[0] = name
            name_var.set(name)
            unit_var.set(units_copy.get(name, "bp"))
            sizes_var.set(", ".join(str(s) for s in ladders_copy.get(name, [])))

        def on_select(event=None):
            sel = lb.curselection()
            if sel:
                load_entry(lb.get(sel[0]))

        def save_entry():
            new_name = name_var.get().strip()
            if not new_name:
                messagebox.showwarning(t("warn_title"), t("warn_no_name"), parent=dlg)
                return
            try:
                def _parse_size(s):
                    v = float(s)
                    return int(v) if v == int(v) else v
                sizes = [_parse_size(s.strip()) for s in sizes_var.get().split(",") if s.strip()]
            except ValueError:
                messagebox.showerror(t("err_title"), t("err_sizes"), parent=dlg)
                return
            if not sizes:
                messagebox.showwarning(t("warn_title"), t("warn_no_sizes"), parent=dlg)
                return

            old_name = _sel[0]
            if old_name and old_name != new_name and old_name in ladders_copy:
                # Rename in-place (preserve order)
                keys = list(ladders_copy.keys())
                idx  = keys.index(old_name)
                items = [(k, v) for k, v in ladders_copy.items() if k != old_name]
                items.insert(idx, (new_name, sizes))
                ladders_copy.clear()
                ladders_copy.update(items)
                del units_copy[old_name]
            else:
                ladders_copy[new_name] = sizes
            units_copy[new_name] = unit_var.get()
            _sel[0] = new_name
            refresh_list(new_name)

        def new_entry():
            _sel[0] = None
            name_var.set("")
            unit_var.set("bp")
            sizes_var.set("")
            lb.selection_clear(0, tk.END)

        def delete_entry():
            sel = lb.curselection()
            if not sel:
                return
            name = lb.get(sel[0])
            if len(ladders_copy) <= 1:
                messagebox.showwarning(t("warn_title"), t("warn_min_ladder"), parent=dlg)
                return
            if not messagebox.askyesno(t("confirm_title"), t("confirm_delete_ladder", name=name), parent=dlg):
                return
            del ladders_copy[name]
            del units_copy[name]
            _sel[0] = None
            name_var.set(""); sizes_var.set("")
            refresh_list()

        def apply_and_close():
            ld.LADDERS.clear()
            ld.LADDERS.update(ladders_copy)
            ld.LADDER_UNITS.clear()
            ld.LADDER_UNITS.update(units_copy)
            ld.save_ladders()
            self._ladder_combo['values'] = list(ld.LADDERS.keys())
            if self.state.ladder_type not in ld.LADDERS:
                first = next(iter(ld.LADDERS))
                self.state.ladder_type = first
                self._ladder_var.set(first)
            dlg.destroy()

        lb.bind("<<ListboxSelect>>", on_select)
        dlg.protocol("WM_DELETE_WINDOW", apply_and_close)

        refresh_list(next(iter(ladders_copy), None))

        tk.Button(dlg, text=t("btn_close_save"), command=apply_and_close).pack(
            side=tk.BOTTOM, pady=8)

    def _font_larger(self):
        self.state.sample_font_size = min(36, self.state.sample_font_size + 1)
        self._font_size_var.set(str(self.state.sample_font_size))
        self.gel_canvas.refresh()

    def _font_smaller(self):
        self.state.sample_font_size = max(6, self.state.sample_font_size - 1)
        self._font_size_var.set(str(self.state.sample_font_size))
        self.gel_canvas.refresh()

    def _apply_line_style(self):
        self.state.ladder_line_style = self._line_style_var.get()
        self.gel_canvas.refresh()

    def _reset_ladder(self):
        self.state.ladder_annotations.clear()
        self.state.undo_history = [
            a for a in self.state.undo_history if a['type'] != 'ladder'
        ]
        self.gel_canvas.refresh()
        self._set_status(t("msg_ladder_reset"))

    def _skip_ladder(self):
        self.gel_canvas.skip_ladder()

    # ── sample wells ──────────────────────────────────────────────────────────

    def _pick_wells_by_click(self):
        if self.state.image_visible is None:
            messagebox.showwarning(t("warn_title"), t("msg_no_image"))
            return

        def on_right(x_img, _mode):
            self._right_x_var.set(str(int(x_img)))
            self._set_status(t("msg_set_right", x=int(x_img)))

        def on_left(x_img, _mode):
            self._left_x_var.set(str(int(x_img)))
            self._set_status(t("msg_set_left", x=int(x_img)))
            self.gel_canvas.pick_callback = on_right
            self.gel_canvas.mode = "PICK_RIGHT"

        self.gel_canvas.pick_callback = on_left
        self.gel_canvas.mode = "PICK_LEFT"
        self._set_status(t("msg_pick_left"))

    def _paste_names(self):
        dlg = tk.Toplevel(self.root)
        dlg.title(t("dlg_paste_names"))
        dlg.geometry("420x220")
        dlg.resizable(True, True)
        dlg.transient(self.root)
        dlg.grab_set()

        tk.Label(dlg, text=t("paste_hint"),
                 font=("Helvetica", 10), justify=tk.LEFT).pack(padx=12, pady=(10, 2), anchor=tk.W)

        txt = tk.Text(dlg, height=6, font=("Helvetica", 10))
        txt.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)
        txt.focus_set()

        def apply():
            raw = txt.get("1.0", tk.END)
            names = []
            for line in raw.splitlines():
                if '\t' in line:
                    parts = line.split('\t')
                else:
                    parts = line.split(',')
                for p in parts:
                    p = p.strip()
                    if p:
                        names.append(p)
            if not names:
                messagebox.showwarning(t("warn_title"), t("paste_no_names"), parent=dlg)
                return
            self._csv_names = names
            self._num_wells_var.set(str(len(names)))
            self._set_status(t("msg_csv_loaded", n=len(names)))
            dlg.destroy()

        btn_row = tk.Frame(dlg)
        btn_row.pack(fill=tk.X, padx=12, pady=(0, 10))
        tk.Button(btn_row, text=t("btn_cancel"), command=dlg.destroy,
                  font=("Helvetica", 10)).pack(side=tk.RIGHT, padx=4)
        tk.Button(btn_row, text=t("btn_apply"), command=apply,
                  font=("Helvetica", 10), default=tk.ACTIVE).pack(side=tk.RIGHT)
        dlg.bind("<Return>", lambda e: apply())
        dlg.bind("<Escape>", lambda e: dlg.destroy())

    def _load_csv(self):
        path = filedialog.askopenfilename(
            title=t("dlg_load_csv"),
            filetypes=[(t("ft_csv"), "*.csv"), (t("ft_all"), "*.*")]
        )
        if not path:
            return
        try:
            with open(path, newline='', encoding='utf-8-sig') as f:
                rows = list(csv.reader(f))
            if not rows:
                messagebox.showwarning(t("warn_title"), "CSV is empty")
                return
            self._csv_names = [c.strip() for c in rows[0] if c.strip()]
            self._num_wells_var.set(str(len(self._csv_names)))
            self._set_status(t("msg_csv_loaded", n=len(self._csv_names)))
        except Exception as exc:
            messagebox.showerror(t("err_title"), t("msg_csv_error", exc=exc))

    def _apply_wells(self):
        if not self._csv_names:
            messagebox.showwarning(t("warn_title"), t("msg_no_csv"))
            return
        if self.state.image_visible is None:
            messagebox.showwarning(t("warn_title"), t("msg_no_image"))
            return
        try:
            left_x = float(self._left_x_var.get())
            right_x = float(self._right_x_var.get())
            n = int(self._num_wells_var.get())
        except ValueError:
            messagebox.showerror(t("err_title"), t("msg_input_error"))
            return
        if n < 1:
            messagebox.showerror(t("err_title"), t("msg_wells_min1"))
            return
        names = self._csv_names[:n]
        self.state.sample_annotations = []
        for i, name in enumerate(names):
            x = left_x if n == 1 else left_x + i * (right_x - left_x) / (n - 1)
            self.state.sample_annotations.append(SampleAnnotation(x_img=x, name=name))
        self.gel_canvas.refresh()
        self._set_status(t("msg_wells_applied", n=len(names)))

    def _clear_wells(self):
        self.state.sample_annotations.clear()
        self.gel_canvas.refresh()
        self._set_status(t("msg_wells_cleared"))

    def _clear_bands(self):
        self.state.band_markers.clear()
        self.gel_canvas.refresh()
        self._set_status(t("msg_bands_cleared"))

    # ── undo ──────────────────────────────────────────────────────────────────

    def _undo(self):
        msg = self.state.undo()
        self.gel_canvas.refresh()
        if msg:
            self._set_status(msg)

    # ── export ────────────────────────────────────────────────────────────────

    def _default_export_name(self) -> str:
        if not self._source_path:
            return "caption"
        from pathlib import Path
        from datetime import datetime
        p = Path(self._source_path)
        try:
            date_str = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y%m%d")
        except Exception:
            from datetime import date
            date_str = date.today().strftime("%Y%m%d")
        return f"{date_str}_{p.stem}_caption"

    def _export_png(self):
        if self.state.image_visible is None:
            messagebox.showwarning(t("warn_title"), t("msg_no_image"))
            return
        path = filedialog.asksaveasfilename(
            title=t("dlg_export_png"),
            initialfile=self._default_export_name(),
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("TIFF", "*.tif")]
        )
        if not path:
            return
        try:
            from exporter import export_png
            export_png(self.state, path)
            self._set_status(t("msg_export_png_done", name=path.split('/')[-1]))
        except Exception as exc:
            messagebox.showerror(t("err_title"), t("msg_export_error", exc=exc))

    def _export_pptx(self):
        if self.state.image_visible is None:
            messagebox.showwarning(t("warn_title"), t("msg_no_image"))
            return
        path = filedialog.asksaveasfilename(
            title=t("dlg_export_pptx"),
            initialfile=self._default_export_name(),
            defaultextension=".pptx",
            filetypes=[("PowerPoint", "*.pptx")]
        )
        if not path:
            return
        try:
            from exporter import export_pptx
            export_pptx(self.state, path)
            self._set_status(t("msg_export_pptx_done", name=path.split('/')[-1]))
        except Exception as exc:
            messagebox.showerror(t("err_title"), t("msg_export_error", exc=exc))

    def _export_svg(self):
        if self.state.image_visible is None:
            messagebox.showwarning(t("warn_title"), t("msg_no_image"))
            return
        path = filedialog.asksaveasfilename(
            title=t("dlg_export_svg"),
            initialfile=self._default_export_name(),
            defaultextension=".svg",
            filetypes=[("SVG", "*.svg")]
        )
        if not path:
            return
        try:
            from exporter import export_svg
            export_svg(self.state, path)
            self._set_status(t("msg_export_svg_done", name=path.split('/')[-1]))
        except Exception as exc:
            messagebox.showerror(t("err_title"), t("msg_export_error", exc=exc))

    # ── language ──────────────────────────────────────────────────────────────

    def _set_lang(self, lang: str):
        save_lang(lang)
        messagebox.showinfo(t("lang_restart_title"), t("lang_restart_msg"))

    # ── helpers ───────────────────────────────────────────────────────────────

    def _set_status(self, msg: str):
        self._status_var.set(msg)
