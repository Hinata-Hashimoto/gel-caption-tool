# GelAnnotator
ゲル電気泳動画像を半自動でアノテーションするデスクトップアプリです。慣れれば30秒で編集が終わります。**releaseから最新バージョンをダウンロードしてください。windows版、Mac版両方あります。**
A desktop application for semi-automatic annotation of gel electrophoresis images.  

https://github.com/user-attachments/assets/5d3413db-3961-456e-9a16-19554abdc0c8


---

# GelAnnotator 操作ガイド / User Guide

電気泳動ゲル・ウェスタンブロット画像に、分子量マーカー・サンプル名・バンド位置・領域ラベルを素早く書き込んで、PNG / SVG / PPTXとして書き出すためのデスクトップツールです。macOS / Windows共通、インストール不要、キーボードショートカットは自由に変更できます。

A desktop tool for quickly labeling gel and Western blot images with molecular-weight ladders, sample names, band markers, and region labels, then exporting to PNG, SVG, or PPTX. Works on macOS and Windows, needs no install, and every keyboard shortcut is customizable.

---

# 日本語

## 目次

0. [インストールと初回起動](#00-インストールと初回起動)
1. [クイックスタート](#01-クイックスタート)
2. [画面の構成](#02-画面の構成)
3. [画像を開く・回転・保存](#03-画像を開く回転保存)
4. [4つの書き込みモード](#04-4つの書き込みモード)
5. [発光画像（WBモード）](#05-発光画像wbモード)
6. [ラダー（分子量マーカー）設定](#06-ラダー分子量マーカー設定)
7. [サンプルウェルとラベル](#07-サンプルウェルとラベル)
8. [書き出し（PNG / SVG / PPTX）](#08-書き出しpng--svg--pptx)
9. [元に戻す・言語設定](#09-元に戻す言語設定)
10. [キーボードショートカット](#10-キーボードショートカット)
11. [設定ファイルとヘルプ](#11-設定ファイルとヘルプ)

## 00. インストールと初回起動

### macOS

1. `GelAnnotator.app` をダウンロード（またはコピー）したフォルダに置きます。
2. 初回起動時、署名されていないアプリのため「"GelAnnotator"は、開発元を確認できないため開けません」という警告が出ます。これはmacOSの標準的な保護機能（Gatekeeper）によるもので、アプリ自体に問題があるわけではありません。
3. 次のいずれかの方法で開きます。
   - `GelAnnotator.app` を**右クリック（Controlキー＋クリック）**→「開く」→確認ダイアログで「開く」を選ぶ（初回のみ必要）。
   - それでも開けない場合: アップルメニュー →「システム設定」→「プライバシーとセキュリティ」を開き、下の方にある「"GelAnnotator"は確認できないため…」の横の **「このまま開く」** を押す。
   - 詳しい人向け: ターミナルで `xattr -cr /path/to/GelAnnotator.app` を実行してquarantine属性を外す方法もあります。
4. 一度許可すれば、次回からは通常どおりダブルクリックで起動できます。

### Windows

1. ダウンロードした `GelAnnotator.exe` をダブルクリックして起動します。
2. ダウンロード経路によっては「Windowsによって PC が保護されました」という表示（SmartScreen）が出ることがあります。その場合は「詳細情報」→「実行」を選べば起動できます。
3. 以降は通常どおり起動できます。

## 01. クイックスタート

初めて使うときの、画像を開いてから書き出すまでの一連の流れです。

1. **画像を開く** — ゲルの写真をウィンドウにドラッグ＆ドロップするか、`File > Open Image`（`Ctrl+O` または `Ctrl+N`）で画像ファイルを選びます。
2. **ラダーを置く** — サイドバーの「ラダー配置」を押してゲル上のマーカーバンドを上から順にクリックします。選んだラダー種別（例: 100bp DNA）のサイズが小さい方から順に割り当てられます。
3. **ウェルを設定する** — 「← → クリックで設定」で画像上の一番左と一番右のウェル位置をクリックするか、Left X / Right X に直接数値を入力します。
4. **サンプル名を入力する** — 「貼り付けで入力…」でExcelからコピーした名前を貼り付けるか、名前を入力せずに「ウェルを適用」を押すと 1, 2, 3… と自動で連番が入ります。
5. **必要に応じてバンドや領域を書き込む** — 「バンドマーカー」で注目バンドに赤丸を、「領域ラベル」で複数レーンをまとめて囲むラベルを追加します。
6. **書き出す** — PNG・SVG・PPTXのいずれかで保存します。PPTXはPowerPoint上でテキストや画像を個別に編集できます。

## 02. 画面の構成

左のサイドバーに全ての操作が並び、右側の黒いキャンバスに画像とアノテーションが表示されます。下の画面例は、ラダー・8つのサンプル名・バンドマーカー・領域ラベル「test1」を実際に配置した状態です。

![画面全体（日本語）](guide_images/ui_ja_full.png)

![サイドバー拡大（日本語）](guide_images/ui_ja_sidebar.png)

- **キャンバス上部の余白**にはサンプル名が縦書きで、**左側の余白**にはラダーのサイズラベルが表示されます。
- 画面下部には現在のモードに応じた操作ヒント（ステータス）が表示されます。
- 各ボタンの末尾の `[ ]` 内の文字は、現在そのボタンに割り当てられているショートカットキーです。「10. キーボードショートカット」で変更すると、ここの表示も自動的に更新されます。
- サイドバーの「モード」ボタン（ラダー配置・バンドマーカー・切り取り・領域ラベル）は、選択中のものが青くハイライトされます。

## 03. 画像を開く・回転・保存

| 操作 | 内容 |
|---|---|
| 画像を開く | `File > Open Image`、または画像ファイルをウィンドウにドラッグ＆ドロップ。PNG / JPEG / TIFF / BMPに対応。 |
| 16bit / 32bitのTIFF | 自動的に輝度の1〜99パーセンタイルでコントラストを引き伸ばし、白黒反転（発光シグナルが明るい→ゲル上で濃いバンドになるよう）して読み込みます。 |
| 回転 | 「↺ 左90°」「↻ 右90°」で90度単位で回転。既にアノテーションがある場合は確認ダイアログが出て、回転するとラダー・サンプル名・バンド・領域ラベルは全てクリアされます。 |
| 切り取り（Crop） | 「切り取り」モードにして、画像上をドラッグして矩形を選び、マウスを離すと即座に切り取られます。アノテーションの座標も自動調整されます。`Ctrl+Z`で元に戻せます。 |

## 04. 4つの書き込みモード

サイドバー上部の4つのボタンでモードを切り替えます。モード中はキャンバスをクリックして書き込みます。

| モード | 既定キー | 内容 |
|---|---|---|
| ラダー配置 | `L` | ゲル上のマーカーバンドを上から順にクリック。クリックするたびに、選択中のラダー種別のサイズが小さい方から順に割り当てられます。「このバンドをスキップ」で見えないバンドを飛ばせます。やり直す場合は「ラダーリセット」。 |
| バンドマーカー | `B` | 注目バンドをクリックすると赤丸が付きます。既存の赤丸の近くをクリックすると、その印を削除します。全消去は `Edit > Clear Band Markers`。 |
| 切り取り | `C` | 画像上をドラッグして矩形を選択し、マウスを離すとその場で切り取られます。4px未満の範囲は小さすぎるためキャンセルされます。 |
| 領域ラベル | `G` | 複数レーンをまとめて示すラベルです。範囲の左端・右端を2回クリックすると、ラベル名を入力するダイアログが出ます。 |

## 05. 発光画像（WBモード）

ウェスタンブロットなどで、可視光画像（メンブレン全体やマーカー）と発光画像を重ねて扱うための機能です。

- 先に通常の画像（可視光画像）を開いておく必要があります。
- `File > Open Luminescence Image (WB)` で発光画像を追加すると、WBモードが自動的に有効になります。
- 「WB画像切替」ボタン（`W`）で、可視光画像と発光画像の表示を切り替えられます。

## 06. ラダー（分子量マーカー）設定

**ラダー種別** — ドロップダウンから「100bp DNA」「1kb DNA」「Protein」の組み込みプリセットを選べます。それぞれのサイズリストに沿って、ラダー配置モードでクリックした順にサイズが割り当てられます。

**ラダーを編集** — 「ラダーを編集…」から、サイズのリストや単位（bp / kDa）を指定して自分のラダーを追加・リネーム・削除できます。追加したラダーはホームフォルダ内の設定ファイルに保存され、次回起動時も使えます（組み込みの3種類は上書きされません）。

**表示スタイルとリセット**

- **ラダーの線スタイル**: 「Full」は画像幅いっぱいの点線、「Short」は左余白だけの短い目盛り。
- **ラダーリセット**（`R`）: 配置したラダーをすべて消して最初からやり直します。
- **このバンドをスキップ**（`→`）: ゲル上で見えないバンドをクリックせずに1つ読み飛ばします。

## 07. サンプルウェルとラベル

**ウェル位置** — 「← → クリックで設定」（`S`）を押してから画像上で一番左・一番右のウェルを順にクリックすると、Left X / Right X に自動入力されます。もちろん数値を直接入力してもかまいません。「Wells」欄にウェルの数を入れると、その間を等間隔に並べます。

**サンプル名の入力**

- **CSV読み込み…**: CSVファイルの1行目をそのままサンプル名として読み込みます。
- **貼り付けで入力…**（`P`）: Excelの行をコピーしてそのまま貼り付けられます（タブ区切り・カンマ区切りの両方に対応、複数行もOK）。

> **名前を入力しなかった場合:** サンプル名を何も読み込まずに「ウェルを適用」を押すと、Wellsで指定した数だけ自動で 1, 2, 3, 4… と連番が入力されます。とりあえず位置だけ決めて後から名前を直したいときに便利です。

「ウェルを適用」（`A`）を押すと、読み込んだ（または自動生成した）名前がLeft X〜Right Xの間に等間隔で配置されます。「ウェルをクリア」で全消去できます。

**文字サイズ** — サンプル名・領域ラベルの文字サイズは「Font Size」の `−` / `+`（既定キー: `−` / `=`）で6〜36の範囲で調整できます。

## 08. 書き出し（PNG / SVG / PPTX）

| 形式 | 特徴 |
|---|---|
| PNG（`Ctrl+S`） | 300dpiのラスター画像。そのままレポートやスライドに貼り付けられます。 |
| PPTX（`Ctrl+Shift+S`） | PowerPointファイルとして書き出し。ゲル画像と、ラダー・サンプル名などのラベルがそれぞれ別の編集可能なテキストボックスになるので、PowerPoint側で文字や位置、フォントを自由に調整できます。 |
| SVG | ベクター形式。拡大しても文字や線が綺麗なままで、Illustratorなどでの編集にも向きます。 |

ファイル名の初期値は「元画像の更新日_元画像名_caption」の形式で自動提案されます。

## 09. 元に戻す・言語設定

- **元に戻す / やり直す**（`Ctrl+Z` / `Ctrl+Y`）: ラダー配置・バンド追加/削除・切り取り・回転・領域ラベルの追加など、ほとんどの操作を取り消せます。
- **表示言語**: `Language` メニューで日本語・Englishを切り替えられます。**切り替えには再起動が必要です。**

## 10. キーボードショートカット

既定のショートカットキー一覧です。英字キーは大文字・小文字（Shiftの有無）どちらでも反応します。

| 機能 | 既定キー |
|---|---|
| 画像を開く | `Ctrl+O` `Ctrl+N` |
| 元に戻す | `Ctrl+Z` |
| やり直す | `Ctrl+Y` |
| 通常モードに戻す | `Esc` |
| ラダーモード | `L` |
| バンドマーカーモード | `B` |
| 切り取りモード | `C` |
| 領域ラベルモード | `G` |
| ウェル位置をクリックで設定 | `S` |
| サンプル名を貼り付け | `P` |
| ウェルを適用 | `A` |
| フォントを大きく | `=` `+` |
| フォントを小さく | `−` |
| ラダーのバンドをスキップ | `→` |
| PNG書き出し | `Ctrl+S` |
| PPTX書き出し | `Ctrl+Shift+S` |
| WBモード切替 | `W` |
| ラダーをリセット | `R` |

![ショートカットキーの設定ダイアログ（日本語）](guide_images/ui_ja_shortcuts.png)

**ショートカットを変更する** — `Edit > Keyboard Shortcuts…` から変更できます。

1. **変更したい行を選ぶ** — 一覧で機能とキーの組み合わせを選択します。
2. **「変更…」または「追加…」を押す** — 編集ダイアログが開いたら、割り当てる機能を選び、そのまま目的のキーを押します（`Ctrl` / `Shift`との組み合わせも可）。「キーを入力…」ボタンは入力欄をリセットして待機状態に戻すためのものです。
3. **「適用」を押す** — 既に別の機能で使われているキーを選ぶとエラーになり、割り当てられません。
4. 変更内容は自動で保存され、サイドバーのボタン表示やメニューのショートカット表記もすぐに更新されます。「初期値に戻す」でいつでも既定の組み合わせに戻せます。

## 11. 設定ファイルとヘルプ

- **言語・ショートカット設定**は、ソースから起動した場合はアプリと同じフォルダの `config.json` に、配布版アプリ（.app / .exe）ではmacOSなら `~/Library/Application Support/GelCaptionTool/`、Windowsなら `%APPDATA%\GelCaptionTool\` 内の `config.json` に保存されます。
- **追加したラダー種別**は、ホームフォルダ直下の `.gel_caption_ladders.json` に保存されます。
- `Help` メニューからGitHubリポジトリと開発者のホームページを開けます。

---

# English

## Table of Contents

0. [Installation & First Launch](#00-installation--first-launch)
1. [Quick Start](#01-quick-start)
2. [Interface Overview](#02-interface-overview)
3. [Opening, Rotating & Cropping](#03-opening-rotating--cropping)
4. [The Four Modes](#04-the-four-modes)
5. [Luminescence (WB Mode)](#05-luminescence-wb-mode)
6. [Ladder Setup](#06-ladder-setup)
7. [Sample Wells & Labels](#07-sample-wells--labels)
8. [Exporting (PNG / SVG / PPTX)](#08-exporting-png--svg--pptx)
9. [Undo/Redo & Language](#09-undoredo--language)
10. [Keyboard Shortcuts](#10-keyboard-shortcuts)
11. [Config Files & Help](#11-config-files--help)

## 00. Installation & First Launch

### macOS

1. Place `GelAnnotator.app` wherever you downloaded or copied it.
2. On first launch, macOS shows "'GelAnnotator' cannot be opened because the developer cannot be verified." This is Gatekeeper, macOS's standard protection for unsigned apps — it doesn't mean anything is wrong with the app itself.
3. Open it with one of these:
   - **Right-click (or Control-click)** `GelAnnotator.app` → **Open** → confirm **Open** in the dialog (only needed the first time).
   - If that doesn't work: Apple menu → **System Settings** → **Privacy & Security**, scroll down to the "'GelAnnotator' was blocked..." message, and click **Open Anyway**.
   - For advanced users: run `xattr -cr /path/to/GelAnnotator.app` in Terminal to remove the quarantine flag.
4. Once approved, the app opens normally with a double-click from then on.

### Windows

1. Double-click the downloaded `GelAnnotator.exe` to launch it.
2. Depending on how it was downloaded, Windows may show "Windows protected your PC" (SmartScreen). If so, click **More info** → **Run anyway**.
3. After that, it launches normally.

## 01. Quick Start

The full path from opening an image to exporting a captioned figure.

1. **Open an image** — Drag a gel photo onto the window, or use `File > Open Image` (`Ctrl+O` or `Ctrl+N`).
2. **Place the ladder** — Click "Place Ladder" in the sidebar, then click each marker band top to bottom. Sizes from the selected ladder preset (e.g. 100bp DNA) are assigned smallest-first, in click order.
3. **Set the wells** — Click "Click to Set L/R", then click the leftmost and rightmost wells on the image — or type the X positions directly into Left X / Right X.
4. **Enter sample names** — Use "Paste Names…" to paste names copied from Excel, or just click "Apply Wells" with no names entered to auto-fill 1, 2, 3…
5. **Add bands or regions as needed** — Use "Band Marker" to flag bands of interest with a red dot, and "Region Label" to bracket several lanes under one label.
6. **Export** — Save as PNG, SVG, or PPTX. PPTX keeps every label as an editable text box in PowerPoint.

## 02. Interface Overview

Every control lives in the left sidebar; the dark canvas on the right shows the image and its annotations. The screenshot below shows a ladder, eight sample names, a band marker, and a region label ("test1") all placed.

![Full window (English)](guide_images/ui_en_full.png)

![Sidebar close-up (English)](guide_images/ui_en_sidebar.png)

- The **top margin** of the canvas carries vertical sample-name labels; the **left margin** carries ladder size labels.
- The status line at the bottom shows a hint for whatever mode is active.
- The `[ ]` suffix on a button shows the key currently assigned to it. Change it in "10. Keyboard Shortcuts" and the button updates automatically.
- The four mode buttons (Place Ladder, Band Marker, Crop, Region Label) highlight in blue while active.

## 03. Opening, Rotating & Cropping

| Action | Details |
|---|---|
| Open an image | `File > Open Image`, or drag a file onto the window. PNG, JPEG, TIFF and BMP are supported. |
| 16-/32-bit TIFF | Automatically contrast-stretched using the 1st–99th percentile of pixel intensity and inverted, so a bright luminescence signal becomes a dark band on a white background. |
| Rotate | "↺ CCW 90°" / "↻ CW 90°" rotate in 90° steps. If annotations exist you'll be asked to confirm, since rotating clears all ladder, sample, band and region annotations. |
| Crop | Switch to Crop mode, drag a rectangle over the image, and release to crop immediately — annotation positions are adjusted automatically. Press `Ctrl+Z` to undo. |

## 04. The Four Modes

The four buttons at the top of the sidebar switch modes; click on the canvas to place annotations while a mode is active.

| Mode | Default Key | Details |
|---|---|---|
| Place Ladder | `L` | Click each marker band top to bottom. Each click assigns the next size, smallest first, from the selected ladder preset. "Skip Band" advances past a band you can't see; "Reset Ladder" clears it all and starts over. |
| Band Marker | `B` | Click a band of interest to drop a red dot. Click near an existing dot to remove it. Clear them all from `Edit > Clear Band Markers`. |
| Crop | `C` | Drag a rectangle over the image; releasing the mouse crops immediately. Selections smaller than 4px are ignored as too small. |
| Region Label | `G` | For labeling a group of lanes together. Click the left edge, then the right edge of the span, then type the label text in the dialog that appears. |

## 05. Luminescence (WB Mode)

For Western blots: overlay a visible-light image (the membrane or marker lane) with a luminescence exposure.

- Open the normal (visible-light) image first.
- Then use `File > Open Luminescence Image (WB)` to add the luminescence exposure — WB mode turns on automatically.
- "Toggle WB" (`W`) switches the canvas between the visible-light and luminescence images.

## 06. Ladder Setup

**Ladder type** — Pick a built-in preset from the dropdown: 100bp DNA, 1kb DNA, or Protein. While in Place Ladder mode, each click assigns the preset's sizes in order, smallest first.

**Editing ladders** — "Edit Ladders…" lets you add, rename, or delete your own ladder presets, each with its own size list and unit (bp / kDa). Custom ladders are saved to a file in your home folder and persist across launches; the three built-in presets are never overwritten.

**Display & reset**

- **Ladder Line Style**: "Full" draws a dashed line across the whole image width; "Short" draws a short tick in the left margin only.
- **Reset Ladder** (`R`): clears every placed ladder band so you can start over.
- **Skip Band** (`→`): advances to the next size without clicking, for a band you can't actually see.

## 07. Sample Wells & Labels

**Well positions** — Click "Click to Set L/R" (`S`), then click the leftmost and rightmost wells on the image — this fills in Left X / Right X for you, though you can also type the values directly. The "Wells" field sets how many evenly-spaced labels are placed between them.

**Sample names**

- **Load CSV…**: reads the first row of a CSV file as the sample names.
- **Paste Names…** (`P`): paste rows copied straight from Excel (tab- or comma-separated, multiple rows are fine).

> **Leaving names blank:** click "Apply Wells" without loading any names, and the wells are automatically numbered 1, 2, 3, 4… up to the count in "Wells". Handy for positioning wells first and filling in real names later.

"Apply Wells" (`A`) places the loaded (or auto-numbered) names evenly between Left X and Right X. "Clear Wells" removes them all.

**Font size** — The text size for sample names and region labels is adjustable from 6 to 36 with the Font Size `−` / `+` buttons (default keys: `−` / `=`).

## 08. Exporting (PNG / SVG / PPTX)

| Format | Notes |
|---|---|
| PNG (`Ctrl+S`) | A 300dpi raster image, ready to drop straight into a report or slide. |
| PPTX (`Ctrl+Shift+S`) | A PowerPoint file where the gel image and every label (ladder sizes, sample names, etc.) are separate, fully editable text boxes — adjust text, position, or font directly in PowerPoint afterward. |
| SVG | A vector file that stays crisp at any zoom level, and opens cleanly in Illustrator or similar tools. |

The suggested filename follows the pattern "source-image-date_source-image-name_caption".

## 09. Undo/Redo & Language

- **Undo / Redo** (`Ctrl+Z` / `Ctrl+Y`): covers most actions — placing ladder bands, adding/removing band markers, cropping, rotating, adding region labels.
- **Display language**: switch between Japanese and English from the `Language` menu. **The change takes effect after restarting the app.**

## 10. Keyboard Shortcuts

The default shortcuts. Letter keys respond with or without Shift.

| Action | Default Key |
|---|---|
| Open Image | `Ctrl+O` `Ctrl+N` |
| Undo | `Ctrl+Z` |
| Redo | `Ctrl+Y` |
| Return to Normal Mode | `Esc` |
| Ladder Mode | `L` |
| Band Marker Mode | `B` |
| Crop Mode | `C` |
| Region Label Mode | `G` |
| Set Wells by Click | `S` |
| Paste Sample Names | `P` |
| Apply Wells | `A` |
| Larger Font | `=` `+` |
| Smaller Font | `−` |
| Skip Ladder Band | `→` |
| Export PNG | `Ctrl+S` |
| Export PPTX | `Ctrl+Shift+S` |
| Toggle WB Mode | `W` |
| Reset Ladder | `R` |

![Keyboard Shortcuts dialog (English)](guide_images/ui_en_shortcuts.png)

**Changing a shortcut** — Open `Edit > Keyboard Shortcuts…`.

1. **Pick a row** — Select the action/key pair you want to change.
2. **Click "Change…" or "Add…"** — In the dialog, choose the action, then just press the key you want to assign (`Ctrl` / `Shift` combinations work too). The "Capture Key…" button simply resets the field and refocuses the dialog if you need to try again.
3. **Click "Apply"** — A key already assigned to another action is rejected with an error instead of being applied.
4. Changes save automatically, and sidebar buttons and menu labels update immediately. "Reset to Defaults" restores the original set at any time.

## 11. Config Files & Help

- **Language and shortcut settings** are saved to `config.json` — next to the app's own files when run from source, or inside `~/Library/Application Support/GelCaptionTool/` (macOS) / `%APPDATA%\GelCaptionTool\` (Windows) for the packaged app.
- **Custom ladder presets** are saved to `.gel_caption_ladders.json` in your home folder.
- The `Help` menu links to the GitHub repository and the developer's homepage.


## Author / 作者

Hinata Hashimoto  
[Homepage](https://sites.google.com/view/hinatahashimoto)
