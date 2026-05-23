import json
import os
import sys
import platform
from pathlib import Path


def _config_path() -> Path:
    if getattr(sys, 'frozen', False):
        # PyInstaller bundle: write to user data dir (bundle itself may be read-only)
        if platform.system() == "Windows":
            base = Path(os.environ.get("APPDATA", Path.home()))
        elif platform.system() == "Darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path.home() / ".config"
        d = base / "GelCaptionTool"
        d.mkdir(parents=True, exist_ok=True)
        return d / "config.json"
    return Path(__file__).parent / "config.json"


_CONFIG_PATH = _config_path()
_LANG = "en"


def load_lang():
    global _LANG
    try:
        cfg = json.loads(_CONFIG_PATH.read_text())
        _LANG = cfg.get("lang", "en")
    except Exception:
        _LANG = "en"


def save_lang(lang: str):
    global _LANG
    _LANG = lang
    try:
        cfg = {}
        try:
            cfg = json.loads(_CONFIG_PATH.read_text())
        except Exception:
            pass
        cfg["lang"] = lang
        _CONFIG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
    except Exception:
        pass


def get_lang() -> str:
    return _LANG


# (Japanese, English)
_S: dict[str, tuple[str, str]] = {
    # Menu - File
    "menu_file":            ("ファイル", "File"),
    "menu_open_image":      ("画像を開く…", "Open Image…"),
    "menu_open_lumi":       ("発光画像を開く（WBモード）…", "Open Luminescence Image (WB)…"),
    "menu_export_png":      ("PNG書き出し…", "Export PNG…"),
    "menu_export_pptx":     ("PPTX書き出し…", "Export PPTX…"),
    "menu_quit":            ("終了", "Quit"),
    # Menu - Edit
    "menu_edit":            ("編集", "Edit"),
    "menu_undo":            ("元に戻す", "Undo"),
    "menu_reset_ladder":    ("ラダーをリセット", "Reset Ladder"),
    "menu_clear_wells":     ("ウェルラベルをクリア", "Clear Well Labels"),
    "menu_clear_bands":     ("バンドマーカーをクリア", "Clear Band Markers"),
    # Menu - Language
    "menu_language":        ("言語", "Language"),
    "lang_japanese":        ("日本語", "Japanese"),
    "lang_english":         ("英語", "English"),
    "lang_restart_title":   ("再起動が必要", "Restart Required"),
    "lang_restart_msg":     ("言語を変更しました。アプリを再起動してください。",
                             "Language changed. Please restart the app."),
    # Sidebar sections
    "sec_mode":             ("モード切替", "Mode"),
    "sec_transform":        ("画像変換", "Transform"),
    "sec_ladder_type":      ("ラダー種別", "Ladder Type"),
    "sec_ladder_style":     ("ラダー線スタイル", "Ladder Line Style"),
    "sec_wells":            ("サンプルウェル", "Sample Wells"),
    "sec_font":             ("文字サイズ", "Font Size"),
    "sec_export":           ("書き出し", "Export"),
    # Sidebar buttons
    "btn_ladder_mode":      ("ラダー配置  [L]", "Place Ladder  [L]"),
    "btn_band_mode":        ("バンドマーカー  [B]", "Band Marker  [B]"),
    "btn_crop_mode":        ("切り取り  [C]", "Crop  [C]"),
    "btn_region_mode":      ("領域ラベル  [G]", "Region Label  [G]"),
    "btn_rotate_ccw":       ("↺ 左90°", "↺ CCW 90°"),
    "btn_rotate_cw":        ("↻ 右90°", "↻ CW 90°"),
    "btn_toggle_wb":        ("WB画像切替  [W]", "Toggle WB  [W]"),
    "btn_edit_ladders":     ("ラダーを編集…", "Edit Ladders…"),
    "btn_reset_ladder":     ("ラダーリセット  [R]", "Reset Ladder  [R]"),
    "btn_skip_band":        ("このバンドをスキップ  [→]", "Skip Band  [→]"),
    "btn_pick_wells":       ("← → クリックで設定 [S]", "Click to Set L/R  [S]"),
    "btn_load_csv":         ("CSV読み込み…", "Load CSV…"),
    "btn_paste_names":      ("貼り付けで入力… [P]", "Paste Names…  [P]"),
    "btn_apply_wells":      ("ウェルを適用 [A]", "Apply Wells  [A]"),
    "btn_clear_wells":      ("ウェルをクリア", "Clear Wells"),
    "btn_export_png":       ("PNG書き出し… [Ctrl+S]", "Export PNG…  [Ctrl+S]"),
    "btn_export_pptx":      ("PPTX書き出し… [⇧S]", "Export PPTX…  [⇧S]"),
    "btn_apply":            ("適用", "Apply"),
    "btn_cancel":           ("キャンセル", "Cancel"),
    "btn_new":              ("＋ 新規", "+ New"),
    "btn_delete":           ("削除", "Delete"),
    "btn_save_entry":       ("この内容で保存", "Save"),
    "btn_close_save":       ("閉じる（保存）", "Close (Save)"),
    # Labels
    "lbl_left_x":           ("左端X", "Left X"),
    "lbl_right_x":          ("右端X", "Right X"),
    "lbl_num_wells":        ("ウェル数", "Wells"),
    "lbl_line_full":        ("全体", "Full"),
    "lbl_line_short":       ("短め", "Short"),
    "lbl_name":             ("名前:", "Name:"),
    "lbl_unit":             ("単位:", "Unit:"),
    "lbl_sizes":            ("バンドサイズ\n(カンマ区切り):", "Band Sizes\n(comma-separated):"),
    # Dialog titles
    "dlg_open_image":       ("画像を開く", "Open Image"),
    "dlg_open_lumi":        ("発光画像を開く（WBモード）", "Open Luminescence Image (WB)"),
    "dlg_export_png":       ("PNG書き出し", "Export PNG"),
    "dlg_export_pptx":      ("PPTX書き出し", "Export PPTX"),
    "dlg_load_csv":         ("サンプルCSVを読み込む", "Load Sample CSV"),
    "dlg_paste_names":      ("サンプル名を貼り付け", "Paste Sample Names"),
    "dlg_region_label":     ("領域ラベル", "Region Label"),
    "dlg_edit_ladders":     ("ラダー種別を編集", "Edit Ladder Types"),
    "dlg_ladder_list":      ("ラダー一覧", "Ladder List"),
    "dlg_ladder_detail":    ("詳細編集", "Edit"),
    # File type labels
    "ft_image":             ("画像ファイル", "Image Files"),
    "ft_all":               ("すべてのファイル", "All Files"),
    "ft_csv":               ("CSV", "CSV"),
    # Dialog content
    "paste_hint":           ("Excelなどからコピーしたセルを貼り付けてください。\n（タブ区切り・カンマ区切り・改行区切りを自動判定）",
                             "Paste cells copied from Excel etc.\n(Tab, comma, or newline-separated)"),
    "region_prompt":        ("領域の名前を入力してください:", "Enter region name:"),
    # Error / warning titles
    "err_title":            ("エラー", "Error"),
    "warn_title":           ("警告", "Warning"),
    "confirm_title":        ("確認", "Confirm"),
    # Warnings / errors
    "warn_no_name":         ("名前を入力してください", "Please enter a name"),
    "err_sizes":            ("サイズは数値のカンマ区切りで入力してください（例: 0.5, 1.0, 1.5）",
                             "Enter numeric sizes separated by commas (e.g. 0.5, 1.0, 1.5)"),
    "warn_no_sizes":        ("サイズを1つ以上入力してください", "Enter at least one size"),
    "warn_min_ladder":      ("最低1つのラダーが必要です", "At least one ladder is required"),
    "confirm_delete_ladder": ("「{name}」を削除しますか？", "Delete '{name}'?"),
    "paste_no_names":       ("名前が見つかりませんでした", "No names found"),
    # Status messages
    "msg_canvas_hint":      ("ファイル > 画像を開く  または  Ctrl+O",
                             "File > Open Image  or  Ctrl+O"),
    "msg_no_image":         ("画像を先に開いてください", "Please open an image first"),
    "msg_open_visible_first": ("先に可視光画像を開いてください。", "Please open a visible image first."),
    "msg_wb_inactive":      ("WBモード無効（発光画像を読み込んでください）",
                             "WB mode inactive (load a luminescence image first)"),
    "msg_rotated":          ("画像を回転しました（Ctrl+Z で元に戻せます）",
                             "Image rotated (Ctrl+Z to undo)"),
    "msg_rotate_confirm":   ("回転するとアノテーションがすべてクリアされます。続けますか？",
                             "Rotation will clear all annotations. Continue?"),
    "msg_ladder_reset":     ("ラダーアノテーションをリセットしました", "Ladder annotations reset"),
    "msg_wells_applied":    ("{n} ウェルラベルを配置しました", "{n} well labels placed"),
    "msg_wells_cleared":    ("ウェルラベルをクリアしました", "Well labels cleared"),
    "msg_bands_cleared":    ("バンドマーカーをクリアしました", "Band markers cleared"),
    "msg_region_added":     ("領域「{name}」を追加しました", "Region '{name}' added"),
    "msg_load_complete":    ("読み込み完了: {name}", "Loaded: {name}"),
    "msg_wb_active":        ("WBモード有効 — 発光: {name}  |  W キーで切替",
                             "WB mode active — lumi: {name}  |  W to toggle"),
    "msg_lumi_image":       ("発光画像", "Luminescence"),
    "msg_visible_image":    ("可視光画像", "Visible"),
    "msg_showing":          ("表示中: {label}", "Showing: {label}"),
    "msg_export_png_done":  ("PNG書き出し完了: {name}", "PNG exported: {name}"),
    "msg_export_pptx_done": ("PPTX書き出し完了: {name}", "PPTX exported: {name}"),
    "msg_csv_loaded":       ("{n} サンプル名を読み込みました", "{n} sample names loaded"),
    "msg_no_csv":           ("CSVを先に読み込んでください", "Please load a CSV first"),
    "msg_set_right":        ("右端X = {x} に設定しました", "Right X = {x} set"),
    "msg_set_left":         ("左端X = {x}。次に右端をクリックしてください",
                             "Left X = {x}. Now click the right edge"),
    "msg_pick_left":        ("左端ウェルをクリックしてください", "Click the left well"),
    "msg_crop_done":        ("切り取り完了。Ctrl+Z で元に戻せます。", "Crop done. Ctrl+Z to undo."),
    "msg_band_deleted":     ("バンドマーカーを削除しました（Ctrl+Z で元に戻せます）",
                             "Band marker removed (Ctrl+Z to undo)"),
    "msg_region_click2":    ("2点目（右端）をクリックしてください", "Click the 2nd point (right edge)"),
    "msg_open_error":       ("画像を開けませんでした:\n{exc}", "Could not open image:\n{exc}"),
    "msg_export_error":     ("書き出し失敗:\n{exc}", "Export failed:\n{exc}"),
    "msg_csv_error":        ("CSV読み込みエラー:\n{exc}", "CSV load error:\n{exc}"),
    "msg_input_error":      ("左端X・右端X・ウェル数を正しく入力してください",
                             "Enter valid Left X, Right X, and well count"),
    "msg_wells_min1":       ("ウェル数は1以上にしてください", "Well count must be at least 1"),
    # Mode hints
    "hint_normal":          ("通常モード", "Normal mode"),
    "hint_ladder":          ("ラダーモード：バンドを下から順にクリック",
                             "Ladder mode: click bands from bottom to top"),
    "hint_band":            ("バンドマーカー：目的バンドをクリック（赤点）",
                             "Band marker: click target band (red dot)"),
    "hint_crop":            ("切り取り：ドラッグして選択 → マウスを離すと即確定（Ctrl+Z で元に戻せます）",
                             "Crop: drag to select → release to confirm (Ctrl+Z to undo)"),
    "hint_region":          ("領域モード：左端をクリック → 右端をクリック → 名前を入力",
                             "Region mode: click left edge → right edge → enter name"),
    # SVG export
    "menu_export_svg":      ("SVG書き出し…", "Export SVG…"),
    "btn_export_svg":       ("SVG書き出し…", "Export SVG…"),
    "dlg_export_svg":       ("SVG書き出し", "Export SVG"),
    "msg_export_svg_done":  ("SVG書き出し完了: {name}", "SVG exported: {name}"),
    # Help menu
    "menu_help":            ("ヘルプ", "Help"),
    "help_github":          ("GitHubページ", "GitHub Page"),
    "help_homepage":        ("制作者のホームページ", "Author's Homepage"),
    # main.py error
    "err_no_tkinter":       (
        "エラー: tkinter が見つかりません。\n"
        "  conda 環境ではなく、以下のいずれかで実行してください:\n"
        "    /opt/homebrew/bin/python3 main.py   (Homebrew Python / macOS)\n"
        "    python3 main.py                     (tkinter 入りの Python)\n"
        "  または launch.sh を使ってください: bash launch.sh",
        "Error: tkinter not found.\n"
        "  Please run with one of the following:\n"
        "    /opt/homebrew/bin/python3 main.py   (Homebrew Python / macOS)\n"
        "    python3 main.py                     (Python with tkinter)\n"
        "  Or use launch.sh: bash launch.sh",
    ),
}


def t(key: str, **kwargs) -> str:
    pair = _S.get(key)
    if pair is None:
        return key
    s = pair[1] if _LANG == "en" else pair[0]
    if kwargs:
        s = s.format(**kwargs)
    return s


load_lang()
