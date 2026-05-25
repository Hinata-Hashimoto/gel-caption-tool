# GelAnnotator

A desktop application for semi-automatic annotation of gel electrophoresis images.  
ゲル電気泳動画像を半自動でアノテーションするデスクトップアプリです。慣れれば30秒で編集が終わります。


https://github.com/user-attachments/assets/5d3413db-3961-456e-9a16-19554abdc0c8


---

## Download / ダウンロード

Go to the [Releases page](https://github.com/Hinata-Hashimoto/gel-caption-tool/releases) and download the file for your OS.

[Releases ページ](https://github.com/Hinata-Hashimoto/gel-caption-tool/releases)からお使いの OS 用ファイルをダウンロードしてください。

| OS | File |
|----|------|
| Windows | `GelAnnotator.exe` |
| macOS | `GelAnnotator.app` (zip) |

> ### ⚠️ macOS: First Launch / 初回起動
>
> macOS will block the app because it is not signed with an Apple Developer certificate.
>
> 1. Double-click `GelAnnotator.app` (a warning dialog appears — that is expected).
> 2. Open **System Settings → Privacy & Security**, scroll down to the **Security** section.
> 3. You will see *"GelAnnotator was blocked…"* — click **"Open Anyway"**.
>
> ---
>
> macOS は署名のないアプリをブロックします。
>
> 1. `GelAnnotator.app` をダブルクリック（警告ダイアログが出ますが、完了を押せばOK）。
> 2. **システム設定 → プライバシーとセキュリティ** を開き、**セキュリティ** セクションまでスクロール。
> 3. *「"GelAnnotator" は開発元を確認できないため…」* という表示の横にある **「このまま開く」** をクリック。

---

## Features / 機能

- Load gel images (PNG, TIFF, JPEG)  
  ゲル画像の読み込み（PNG / TIFF / JPEG）
- Auto-fit ladder band positions from standard ladder data  
  標準ラダーデータから泳動距離を自動フィッティング
- Click-to-place well positions and band markers  
  クリックでウェル位置・バンドマーカーを配置
- Add sample names (manual input or CSV import)  
  サンプル名の入力（手動 / CSV インポート）
- Region labels (e.g. "insert", "vector")  
  領域ラベルの追加
- Rotate and crop image  
  画像の回転・トリミング
- White/black background toggle  
  白背景・黒背景の切り替え
- Export as **PNG** (≥300 DPI), **SVG**, or **PPTX**  
  **PNG**（300 DPI 以上）・**SVG**・**PPTX** でエクスポート
- Japanese / English UI toggle (restart required)  
  日本語 / English UI 切り替え（再起動が必要）

---

## Usage / 使い方

### 1. Open an image / 画像を開く

**File → Open Image** (or `Ctrl+O`)  
Select a gel image file (PNG, TIFF, JPEG).

**File → Open Image**（または `Ctrl+O`）でゲル画像ファイルを選択します。

---

### 2. Place ladder / ラダーを配置する

1. Select a ladder type from the dropdown in the sidebar.  
   サイドバーのドロップダウンでラダーの種類を選択します。
2. Click **Ladder Mode**, then click the gel image to place each ladder band from the top (largest) to the bottom (smallest).  
   **Ladder Mode** を押し、画像上でラダーバンドを上（大きい方）から順にクリックして配置します。
3. Use **Skip Band** (or`→`),to skip the ladder band.
   **このバンドをスキップ**（または`→`）でそのラダーバンドをスキップすることができます。

---

### 3. Set sample wells / ウェルを設定する

Enter the leftmost and rightmost lane X positions, set the number of wells, and click **Apply wells**.  
Or click **Pick by click** and click the first and last lane directly on the image.

左端・右端のレーン X 座標を入力してウェル数を設定し、**Apply wells** を押します。  
または **Pick by click** を押して画像上で直接クリックします。

---

### 4. Enter sample names / サンプル名を入力する

Type names in the text boxes in the sidebar, one per lane.  
Or use **File → Open CSV** to import names from a CSV file (one name per line).

サイドバーのテキストボックスに各レーンのサンプル名を入力します。  
CSV ファイル（1 行 1 サンプル名）を **File → Open CSV** で読み込むこともできます。

---

### 5. Add band markers / バンドマーカーを追加する

Click **Band Mode**, then click on the gel image at band positions.  
Click the same spot again to remove a marker.

**Band Mode** を押し、バンドの位置をクリックしてマーカーを追加します。  
`Control+z`で戻ることができます。

---

### 6. Add region labels / 領域ラベルを追加する

Click **Region Mode**, then drag across the gel image to define a region.  
Enter a label name in the dialog that appears.

**Region Mode** を押し、画像上でドラッグして領域を定義します。  
表示されるダイアログにラベル名を入力します。

---

### 7. Export / エクスポート

| Format | Menu | Notes |
|--------|------|-------|
| PNG | File → Export PNG (`Ctrl+S`) | ≥300 DPI, auto-upscaled |
| PPTX | File → Export PPTX (`Ctrl+Shift+S`) | Editable PowerPoint |
| SVG | File → Export SVG | Vector annotations + embedded image |

---

## Keyboard Shortcuts / キーボードショートカット

| Key | Action |
|-----|--------|
| `Ctrl+O` | Open image |
| `Ctrl+S` | Export PNG |
| `Ctrl+Shift+S` | Export PPTX |
| `Ctrl+Z` | Undo |
| `R` | Reset ladder |

---

## Build from Source / ソースからビルド

```bash
# Install dependencies
pip install pillow numpy python-pptx lxml

# Run directly
python main.py

# Build macOS .app
pyinstaller GelCaptionTool.spec --noconfirm

# Build Windows .exe (run on Windows)
pyinstaller GelCaptionTool_win.spec --noconfirm
```

### Requirements

- Python 3.9+
- Pillow
- numpy
- python-pptx
- lxml

---

## Author / 作者

Hinata Hashimoto  
[Homepage](https://sites.google.com/view/hinatahashimoto)
