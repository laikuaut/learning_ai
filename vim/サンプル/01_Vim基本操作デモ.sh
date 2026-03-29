#!/bin/bash
# ============================================================
# Vim基本操作デモ
# ============================================================
# 学べる内容:
#   - Vimのexモード（vim -e / ex）を使ったファイル操作
#   - ファイルの作成・テキスト追加・保存・表示
#   - Vimの基本的なモード概念（ノーマル・挿入・コマンド）
#   - exコマンドによるスクリプト的なVim操作
#
# 実行方法:
#   chmod +x 01_Vim基本操作デモ.sh
#   ./01_Vim基本操作デモ.sh
# ============================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

section() { echo -e "\n${GREEN}========== $1 ==========${RESET}\n"; }
info()    { echo -e "${CYAN}[INFO]${RESET} $1"; }
run_cmd() { echo -e "${YELLOW}\$ $1${RESET}"; eval "$1"; }
pause()   { echo -e "\n${CYAN}[Enter を押して次へ進む]${RESET}"; read -r; }

# ----------------------------------------------------------
section "1. Vimのモード概念"
info "Vimには主に3つのモードがあります:"
echo "  ノーマルモード : カーソル移動・コマンド実行（起動時のモード）"
echo "  挿入モード     : テキスト入力（i, a, o で切替）"
echo "  コマンドモード : ファイル保存・終了・検索（: で切替）"
echo ""
info "このデモでは ex モード（コマンドモードのスクリプト版）を使って操作します。"
pause

# ----------------------------------------------------------
section "2. exモードでファイルを作成"
TARGET="$TMPDIR/sample.txt"
info "ex コマンドでファイルを作成し、テキストを挿入します。"
info "対象ファイル: $TARGET"
echo ""

run_cmd "ex -s '$TARGET' <<'SCRIPT'
i
こんにちは、Vimの世界へようこそ！
これはexモードで作成したファイルです。
Vimはテキスト編集の強力なツールです。
.
wq
SCRIPT"

echo ""
info "作成されたファイルの内容:"
run_cmd "cat -n '$TARGET'"
pause

# ----------------------------------------------------------
section "3. テキストの追加（append）"
info "既存ファイルの末尾にテキストを追加します。"

run_cmd "ex -s '$TARGET' <<'SCRIPT'
\$a
--- 追記ここから ---
4行目: exの a コマンドで末尾に追加しました。
5行目: wq で保存して終了します。
.
wq
SCRIPT"

echo ""
info "追記後のファイル内容:"
run_cmd "cat -n '$TARGET'"
pause

# ----------------------------------------------------------
section "4. 特定行の編集"
info "2行目を別のテキストに置き換えます。"

run_cmd "ex -s '$TARGET' <<'SCRIPT'
2s/.*/2行目を書き換えました！（:s コマンド使用）/
wq
SCRIPT"

echo ""
info "編集後のファイル内容:"
run_cmd "cat -n '$TARGET'"
pause

# ----------------------------------------------------------
section "5. 行の削除とコピー"
info "3行目を削除し、1行目をコピーして末尾に貼り付けます。"

run_cmd "ex -s '$TARGET' <<'SCRIPT'
3d
1t\$
wq
SCRIPT"

echo ""
info "操作後のファイル内容:"
run_cmd "cat -n '$TARGET'"
pause

# ----------------------------------------------------------
section "6. 複数ファイルの一括作成"
info "exモードを使って複数ファイルを一括で作成します。"

for i in 1 2 3; do
  F="$TMPDIR/file${i}.txt"
  ex -s "$F" <<SCRIPT
i
ファイル${i}の内容です。
作成日時: $(date '+%Y-%m-%d %H:%M:%S')
.
wq
SCRIPT
  info "作成: file${i}.txt"
done

echo ""
info "作成されたファイル一覧:"
run_cmd "ls -la '$TMPDIR'/"
pause

# ----------------------------------------------------------
section "まとめ"
echo "このデモで学んだこと:"
echo "  1. ex -s でVimをスクリプト的に操作できる"
echo "  2. i（挿入）, a（追加）, s（置換）, d（削除）, t（コピー）"
echo "  3. wq で保存終了、q! で保存せず終了"
echo "  4. Vimのコマンドはシェルスクリプトに組み込める"
echo ""
info "デモ完了！一時ファイルは自動的に削除されます。"
