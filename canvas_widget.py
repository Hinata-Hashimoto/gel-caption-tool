import tkinter as tk
from PIL import Image, ImageTk
from ladder_data import LADDERS, LADDER_UNITS
from annotation_model import AppState, LadderAnnotation, RegionAnnotation
from i18n import t

LEFT_MARGIN = 90    # canvas pixels reserved on the left for ladder labels
TOP_MARGIN = 110    # canvas pixels reserved on the top for sample names
BAND_RADIUS = 3     # canvas pixels, radius of the red dot marker


class GelCanvas(tk.Frame):
    def __init__(self, parent, state: AppState, on_status=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.state = state
        self.on_status = on_status or (lambda msg: None)
        self.mode = "NORMAL"

        self._scale = 1.0
        self._photo = None  # keep reference to prevent GC

        # Crop interaction state
        self._crop_start = None
        self._crop_rect_id = None
        self._crop_end = None

        # Well-position picking
        self.pick_callback = None   # callable(x_img, mode)

        # Region annotation: two-click, then app shows name dialog
        self.region_callback = None  # callable(x_start, x_end)
        self._region_x1 = None

        # Called by app to sync mode buttons after automatic crop-on-release
        self.on_crop_done = None  # callable()

        self._build()

    def _build(self):
        self._canvas = tk.Canvas(self, bg="#2a2a2a", cursor="crosshair", highlightthickness=0)
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind("<Button-1>", self._on_click)
        self._canvas.bind("<B1-Motion>", self._on_drag)
        self._canvas.bind("<ButtonRelease-1>", self._on_release)
        self._canvas.bind("<Configure>", lambda e: self.refresh())

    # ── public API ────────────────────────────────────────────────────────────

    def set_mode(self, mode: str):
        self.mode = mode
        self._crop_start = None
        self._crop_end = None
        self._region_x1 = None
        if self._crop_rect_id:
            self._canvas.delete(self._crop_rect_id)
            self._crop_rect_id = None
        if mode not in ("PICK_LEFT", "PICK_RIGHT"):
            self.pick_callback = None
        if mode != "REGION":
            self.region_callback = None

    def refresh(self):
        if self.state.image_visible is None:
            self._canvas.delete("all")
            self._canvas.create_text(
                self._canvas.winfo_width() // 2,
                self._canvas.winfo_height() // 2,
                text=t("msg_canvas_hint"),
                fill="#666666", font=("Helvetica", 14)
            )
            return
        self._render_image()
        self._draw_annotations()

    def confirm_crop(self):
        if self._crop_start is None or self._crop_end is None:
            return

        x0_c, y0_c = self._crop_start
        x1_c, y1_c = self._crop_end

        # Normalise rect
        lx, rx = sorted([x0_c, x1_c])
        ty, by = sorted([y0_c, y1_c])

        img = self.state.image_visible
        iw, ih = img.size
        x0 = max(0, int(self._c2ix(lx)))
        y0 = max(0, int(self._c2iy(ty)))
        x1 = min(iw, int(self._c2ix(rx)))
        y1 = min(ih, int(self._c2iy(by)))

        if x1 - x0 < 4 or y1 - y0 < 4:
            self.on_status("Crop region too small, cancelled.")
            return

        self.state.push_undo('crop')

        box = (x0, y0, x1, y1)
        self.state.image_visible = img.crop(box)
        if self.state.image_lumi is not None:
            self.state.image_lumi = self.state.image_lumi.crop(box)

        # Adjust annotation coordinates
        for a in self.state.ladder_annotations:
            a.y_img -= y0
        for a in self.state.sample_annotations:
            a.x_img -= x0
        self.state.ladder_annotations = [
            a for a in self.state.ladder_annotations if 0 <= a.y_img <= (y1 - y0)
        ]
        self.state.sample_annotations = [
            a for a in self.state.sample_annotations if 0 <= a.x_img <= (x1 - x0)
        ]
        self.state.band_markers = [
            (bx - x0, by - y0)
            for bx, by in self.state.band_markers
            if x0 <= bx <= x1 and y0 <= by <= y1
        ]
        self.state.region_annotations = [
            RegionAnnotation(
                x_start=max(0, r.x_start - x0),
                x_end=min(x1 - x0, r.x_end - x0),
                name=r.name
            )
            for r in self.state.region_annotations
            if r.x_end >= x0 and r.x_start <= x1
        ]

        self._crop_start = None
        self._crop_end = None
        if self._crop_rect_id:
            self._canvas.delete(self._crop_rect_id)
            self._crop_rect_id = None

        self.mode = "NORMAL"
        self.refresh()
        self.on_status(t("msg_crop_done"))
        if self.on_crop_done:
            self.on_crop_done()

    # ── rendering ─────────────────────────────────────────────────────────────

    def _render_image(self):
        img = self.state.current_image()
        if img is None:
            return

        cw = self._canvas.winfo_width() - LEFT_MARGIN
        ch = self._canvas.winfo_height() - TOP_MARGIN
        if cw <= 0 or ch <= 0:
            return

        iw, ih = img.size
        self._scale = min(cw / iw, ch / ih)

        dw = max(1, int(iw * self._scale))
        dh = max(1, int(ih * self._scale))

        resized = img.resize((dw, dh), Image.LANCZOS)
        self._photo = ImageTk.PhotoImage(resized)

        self._canvas.delete("all")
        self._canvas.create_image(LEFT_MARGIN, TOP_MARGIN, anchor=tk.NW, image=self._photo, tags="img")

        # Draw margins background
        self._canvas.create_rectangle(0, 0, LEFT_MARGIN, self._canvas.winfo_height(),
                                       fill="#1e1e1e", outline="")
        self._canvas.create_rectangle(0, 0, self._canvas.winfo_width(), TOP_MARGIN,
                                       fill="#1e1e1e", outline="")

    def _draw_annotations(self):
        img = self.state.image_visible
        if img is None:
            return
        iw = img.size[0]
        img_right_c = LEFT_MARGIN + int(iw * self._scale)

        # Ladder annotations
        SHORT_TICK_C = 25  # canvas pixels, length of short tick in the margin
        for ann in self.state.ladder_annotations:
            if ann.skipped:
                continue
            yc = self._iy2c(ann.y_img)
            if self.state.ladder_line_style == "full":
                x_start, x_end = LEFT_MARGIN, img_right_c
                label_x = LEFT_MARGIN - 6
            else:
                x_start, x_end = LEFT_MARGIN - SHORT_TICK_C, LEFT_MARGIN
                label_x = LEFT_MARGIN - SHORT_TICK_C - 4
            self._canvas.create_line(
                x_start, yc, x_end, yc,
                fill="#ffffff", dash=(4, 4), width=1, tags="annot"
            )
            size_str = str(int(ann.size)) if ann.size == int(ann.size) else str(ann.size)
            label = f"{size_str} {ann.unit}"
            self._canvas.create_text(
                label_x, yc,
                text=label, anchor=tk.E,
                fill="#ffffff", font=("Helvetica", 9, "bold"), tags="annot"
            )

        # Sample name annotations
        for ann in self.state.sample_annotations:
            xc = self._ix2c(ann.x_img)
            # Tick from top margin to image edge
            self._canvas.create_line(xc, TOP_MARGIN - 4, xc, TOP_MARGIN, fill="#aaaaaa", tags="annot")
            try:
                fs = self.state.sample_font_size
                self._canvas.create_text(
                    xc, TOP_MARGIN * 3 // 4,
                    text=ann.name, anchor=tk.CENTER,
                    fill="#ffffff", font=("Helvetica", fs),
                    angle=90, tags="annot"
                )
            except tk.TclError:
                self._canvas.create_text(
                    xc, TOP_MARGIN * 3 // 4,
                    text=ann.name[:8], anchor=tk.CENTER,
                    fill="#ffffff", font=("Helvetica", self.state.sample_font_size), tags="annot"
                )

        # Region annotations
        REGION_BAR_Y = TOP_MARGIN // 5
        for reg in self.state.region_annotations:
            x1c = self._ix2c(reg.x_start)
            x2c = self._ix2c(reg.x_end)
            self._canvas.create_line(x1c, REGION_BAR_Y, x2c, REGION_BAR_Y,
                                     fill="#ffffff", width=1, tags="annot")
            xmid = (x1c + x2c) / 2
            self._canvas.create_text(
                xmid, REGION_BAR_Y - 2, text=reg.name, anchor=tk.S,
                fill="#ffffff", font=("Helvetica", self.state.sample_font_size), tags="annot"
            )

        # Band markers
        r = BAND_RADIUS
        for xb, yb in self.state.band_markers:
            xc = self._ix2c(xb)
            yc = self._iy2c(yb)
            self._canvas.create_oval(
                xc - r, yc - r, xc + r, yc + r,
                fill="red", outline="red", tags="annot"
            )

    # ── event handlers ────────────────────────────────────────────────────────

    def _on_click(self, event):
        self._canvas.focus_set()  # grab keyboard focus so keybindings work
        if self.state.image_visible is None:
            return

        xc, yc = event.x, event.y
        xi = self._c2ix(xc)
        yi = self._c2iy(yc)
        iw, ih = self.state.image_visible.size

        if self.mode in ("PICK_LEFT", "PICK_RIGHT"):
            if 0 <= xi <= iw and self.pick_callback:
                picked_mode = self.mode
                cb = self.pick_callback
                self.pick_callback = None
                self.mode = "NORMAL"
                cb(xi, picked_mode)
            return

        if self.mode == "LADDER":
            if 0 <= yi <= ih:
                self._place_ladder(yi)

        elif self.mode == "BAND":
            if 0 <= xi <= iw and 0 <= yi <= ih:
                # Click near an existing marker → remove it
                threshold = max(10, BAND_RADIUS * 3) / self._scale
                for i, (bx, by) in enumerate(self.state.band_markers):
                    if ((xi - bx) ** 2 + (yi - by) ** 2) ** 0.5 < threshold:
                        self.state.undo_history.append(
                            {'type': 'band_delete', 'data': (i, (bx, by))}
                        )
                        self.state.band_markers.pop(i)
                        self._draw_annotations()
                        self.on_status(t("msg_band_deleted"))
                        return
                # Otherwise add a new marker
                self.state.push_undo('band')
                self.state.band_markers.append((xi, yi))
                self._draw_annotations()

        elif self.mode == "REGION":
            if 0 <= xi <= iw:
                if self._region_x1 is None:
                    self._region_x1 = xi
                    self.on_status(t("msg_region_click2"))
                else:
                    x1, x2 = sorted([self._region_x1, xi])
                    self._region_x1 = None
                    cb = self.region_callback
                    self.region_callback = None
                    self.mode = "NORMAL"
                    if cb:
                        cb(x1, x2)

        elif self.mode == "CROP":
            self._crop_start = (xc, yc)
            self._crop_end = None

    def _on_drag(self, event):
        if self.mode == "CROP" and self._crop_start:
            if self._crop_rect_id:
                self._canvas.delete(self._crop_rect_id)
            x0, y0 = self._crop_start
            self._crop_rect_id = self._canvas.create_rectangle(
                x0, y0, event.x, event.y,
                outline="#ffff00", width=2, dash=(4, 4), tags="crop_rect"
            )

    def _on_release(self, event):
        if self.mode == "CROP" and self._crop_start:
            self._crop_end = (event.x, event.y)
            self.confirm_crop()  # apply immediately; Ctrl+Z to undo

    # ── helpers ───────────────────────────────────────────────────────────────

    def _ix2c(self, x_img: float) -> float:
        return x_img * self._scale + LEFT_MARGIN

    def _iy2c(self, y_img: float) -> float:
        return y_img * self._scale + TOP_MARGIN

    def _c2ix(self, xc: float) -> float:
        return (xc - LEFT_MARGIN) / self._scale if self._scale else 0

    def _c2iy(self, yc: float) -> float:
        return (yc - TOP_MARGIN) / self._scale if self._scale else 0

    def skip_ladder(self):
        sizes = LADDERS[self.state.ladder_type]
        unit = LADDER_UNITS[self.state.ladder_type]
        idx = len(self.state.ladder_annotations)
        if idx >= len(sizes):
            self.on_status(f"All {len(sizes)} ladder bands placed. Press R to reset.")
            return
        self.state.push_undo('ladder')
        self.state.ladder_annotations.append(
            LadderAnnotation(y_img=-1, size=sizes[idx], unit=unit, skipped=True)
        )
        size_str = str(int(sizes[idx])) if sizes[idx] == int(sizes[idx]) else str(sizes[idx])
        self.on_status(f"Ladder: {size_str} {unit} skipped ({idx + 1}/{len(sizes)})")

    def _place_ladder(self, y_img: float):
        sizes = LADDERS[self.state.ladder_type]
        unit = LADDER_UNITS[self.state.ladder_type]
        idx = len(self.state.ladder_annotations)
        if idx >= len(sizes):
            self.on_status(f"All {len(sizes)} ladder bands placed. Press R to reset.")
            return
        self.state.push_undo('ladder')
        self.state.ladder_annotations.append(LadderAnnotation(y_img=y_img, size=sizes[idx], unit=unit))
        self._draw_annotations()
        size_str = str(int(sizes[idx])) if sizes[idx] == int(sizes[idx]) else str(sizes[idx])
        self.on_status(f"Ladder: {size_str} {unit} placed ({idx + 1}/{len(sizes)})")
