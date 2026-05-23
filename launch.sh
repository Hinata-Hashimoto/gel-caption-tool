#!/bin/bash
# Gel Caption Tool 起動スクリプト
# tkinter に対応した Python を自動検出して起動します

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# tkinter が使える Python を探す
CANDIDATES=(
    "/opt/homebrew/bin/python3"
    "/usr/local/bin/python3"
    "$(pyenv which python3 2>/dev/null)"
    "/usr/bin/python3"
    "python3"
)

for PY in "${CANDIDATES[@]}"; do
    if [ -z "$PY" ]; then continue; fi
    if "$PY" -c "import tkinter, PIL, pptx" 2>/dev/null; then
        echo "使用する Python: $PY"
        cd "$SCRIPT_DIR" && exec "$PY" main.py "$@"
    fi
done

echo "エラー: tkinter + Pillow + python-pptx が揃った Python が見つかりませんでした。"
echo "以下を実行してから再試行してください:"
echo "  /opt/homebrew/bin/pip3 install --break-system-packages Pillow python-pptx"
exit 1
