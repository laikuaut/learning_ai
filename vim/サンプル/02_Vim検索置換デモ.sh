#!/bin/bash
# ============================================================
# Vim検索置換デモ
# ============================================================
# 学べる内容:
#   - Vimの検索・置換コマンド（:%s/old/new/g）
#   - 正規表現を使ったパターンマッチング
#   - :g（global）コマンドによる行操作
#   - 実用的な検索置換パターン
#
# 実行方法:
#   chmod +x 02_Vim検索置換デモ.sh
#   ./02_Vim検索置換デモ.sh
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

# サンプルファイルの準備
SAMPLE="$TMPDIR/sample.txt"
cat > "$SAMPLE" <<'EOF'
プロジェクト報告書
作成日: 2026-01-15
担当者: 田中太郎

1. 概要
本プロジェクトはWebアプリケーションの開発です。
フレームワークにはReactを使用しています。
バックエンドはpythonで構築しました。
データベースはmysqlを採用しています。

2. 進捗状況
TODO: ログイン機能の実装
TODO: ユーザー管理画面の作成
DONE: トップページのデザイン
DONE: APIの基本設計
TODO: テストの作成

3. メモ
email: tanaka@example.com
tel: 090-1234-5678
url: http://example.com/project
EOF

# ----------------------------------------------------------
section "1. サンプルファイルの確認"
info "以下のテキストファイルに対して検索・置換を行います。"
run_cmd "cat -n '$SAMPLE'"
pause

# ----------------------------------------------------------
section "2. 基本的な置換 :%s/old/new/g"
info "python → Python に置換します（大文字修正）。"
info "コマンド: :%s/python/Python/g"

cp "$SAMPLE" "$TMPDIR/work.txt"
ex -s "$TMPDIR/work.txt" <<'SCRIPT'
%s/python/Python/g
wq
SCRIPT

echo ""
info "置換結果（該当行）:"
run_cmd "grep -n 'Python' '$TMPDIR/work.txt'"
pause

# ----------------------------------------------------------
section "3. 大文字小文字を無視した置換（\\c フラグ）"
info "mysql → MySQL に統一します（大文字小文字を無視してマッチ）。"
info "コマンド: :%s/\\\\cmysql/MySQL/g"

cp "$SAMPLE" "$TMPDIR/work.txt"
ex -s "$TMPDIR/work.txt" <<'SCRIPT'
%s/\cmysql/MySQL/g
wq
SCRIPT

echo ""
info "置換結果（該当行）:"
run_cmd "grep -n 'MySQL' '$TMPDIR/work.txt'"
pause

# ----------------------------------------------------------
section "4. 正規表現による置換"
info "日付形式を YYYY-MM-DD → YYYY年MM月DD日 に変換します。"
info "コマンド: :%s/\\\\(\\\\d\\\\{4\\\\}\\\\)-\\\\(\\\\d\\\\{2\\\\}\\\\)-\\\\(\\\\d\\\\{2\\\\}\\\\)/\\\\1年\\\\2月\\\\3日/g"

cp "$SAMPLE" "$TMPDIR/work.txt"
ex -s "$TMPDIR/work.txt" <<'SCRIPT'
%s/\(\d\{4\}\)-\(\d\{2\}\)-\(\d\{2\}\)/\1年\2月\3日/g
wq
SCRIPT

echo ""
info "置換結果（該当行）:"
run_cmd "grep -n '年' '$TMPDIR/work.txt'"
pause

# ----------------------------------------------------------
section "5. :g（global）コマンドで行を操作"
info "TODO の行だけを抽出して新しいファイルに書き出します。"
info "コマンド: :g/TODO/w >> todo.txt"

TODO_FILE="$TMPDIR/todo.txt"
ex -s "$SAMPLE" <<SCRIPT
g/TODO/.w >> $TODO_FILE
q
SCRIPT

echo ""
info "抽出されたTODO一覧:"
run_cmd "cat -n '$TODO_FILE'"
pause

# ----------------------------------------------------------
section "6. :g コマンドで行を削除"
info "DONE の行を削除して未完了タスクだけ残します。"

cp "$SAMPLE" "$TMPDIR/work.txt"
ex -s "$TMPDIR/work.txt" <<'SCRIPT'
g/DONE/d
wq
SCRIPT

echo ""
info "DONE行を削除した結果:"
run_cmd "cat -n '$TMPDIR/work.txt'"
pause

# ----------------------------------------------------------
section "7. 複数パターンの一括置換"
info "複数の置換を一度に実行します。"

cp "$SAMPLE" "$TMPDIR/work.txt"
ex -s "$TMPDIR/work.txt" <<'SCRIPT'
%s/TODO/【未完了】/g
%s/DONE/【完了】/g
%s/田中太郎/山田花子/g
wq
SCRIPT

echo ""
info "一括置換の結果:"
run_cmd "cat -n '$TMPDIR/work.txt'"
pause

# ----------------------------------------------------------
section "まとめ"
echo "このデモで学んだ検索・置換コマンド:"
echo "  :%s/old/new/g     … ファイル全体で置換"
echo "  :%s/\\\\cold/new/g  … 大文字小文字を無視して置換"
echo "  :%s/\\\\(pat\\\\)/\\\\1/ … 正規表現のグループ参照"
echo "  :g/pattern/d      … パターンに一致する行を削除"
echo "  :g/pattern/.w >>  … パターンに一致する行を書き出し"
echo ""
info "デモ完了！一時ファイルは自動的に削除されます。"
