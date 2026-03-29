#!/bin/bash
# ============================================================
# Vimコマンドクイズ
# ============================================================
# 学べる内容:
#   - Vimの基本コマンド（移動・編集・検索・保存）の知識確認
#   - 各コマンドの用途と使い分け
#   - 実践的なシナリオでのVimコマンド選択力
#
# 実行方法:
#   chmod +x 04_Vimコマンドクイズ.sh
#   ./04_Vimコマンドクイズ.sh
# ============================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
RESET='\033[0m'

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

section() { echo -e "\n${GREEN}========== $1 ==========${RESET}\n"; }
info()    { echo -e "${CYAN}[INFO]${RESET} $1"; }
run_cmd() { echo -e "${YELLOW}\$ $1${RESET}"; eval "$1"; }
pause()   { echo -e "\n${CYAN}[Enter を押して次へ進む]${RESET}"; read -r; }

SCORE=0
TOTAL=0

# クイズ出題関数
ask_quiz() {
    local question="$1"
    local opt_a="$2"
    local opt_b="$3"
    local opt_c="$4"
    local opt_d="$5"
    local answer="$6"
    local explanation="$7"

    TOTAL=$((TOTAL + 1))

    echo -e "${YELLOW}【問題 ${TOTAL}】${RESET}"
    echo "$question"
    echo ""
    echo "  a) $opt_a"
    echo "  b) $opt_b"
    echo "  c) $opt_c"
    echo "  d) $opt_d"
    echo ""
    read -rp "あなたの回答 [a/b/c/d]: " user_answer

    user_answer=$(echo "$user_answer" | tr '[:upper:]' '[:lower:]')

    if [[ "$user_answer" == "$answer" ]]; then
        echo -e "${GREEN}正解です！${RESET}"
        SCORE=$((SCORE + 1))
    else
        echo -e "${RED}不正解... 正解は ${answer}) です。${RESET}"
    fi
    echo -e "${CYAN}解説: ${explanation}${RESET}"
    echo ""
}

# ----------------------------------------------------------
section "Vimコマンドクイズへようこそ！"
info "Vimのコマンドに関する10問のクイズに挑戦しましょう。"
info "各問題に a〜d で回答してください。"
pause

# ----------------------------------------------------------
section "基本操作編"

ask_quiz \
    "ファイルを保存して終了するコマンドはどれですか？" \
    ":q!" \
    ":wq" \
    ":w" \
    ":e" \
    "b" \
    ":wq は write（保存）と quit（終了）を組み合わせたコマンドです。ZZ でも同じ操作ができます。"

ask_quiz \
    "挿入モードに入り、カーソルの「前」にテキストを入力するキーはどれですか？" \
    "a" \
    "o" \
    "i" \
    "s" \
    "c" \
    "i（insert）はカーソルの前に挿入します。a は後ろ、o は次の行、s はカーソル位置の文字を削除して挿入です。"

ask_quiz \
    "変更を保存せずにVimを強制終了するコマンドはどれですか？" \
    ":wq" \
    ":q" \
    ":x" \
    ":q!" \
    "d" \
    ":q! は変更を破棄して強制終了します。! を付けることで警告を無視します。"

pause

# ----------------------------------------------------------
section "移動コマンド編"

ask_quiz \
    "ファイルの末尾（最終行）に移動するコマンドはどれですか？" \
    "gg" \
    "G" \
    "0" \
    "\$" \
    "b" \
    "G はファイルの最終行に移動します。gg はファイルの先頭、0 は行頭、\$ は行末です。"

ask_quiz \
    "単語単位で前方に移動するコマンドはどれですか？" \
    "b" \
    "w" \
    "e" \
    "h" \
    "b" \
    "w（word）は次の単語の先頭へ、b（back）は前の単語の先頭へ、e（end）は単語の末尾へ移動します。"

ask_quiz \
    "10行目にジャンプするコマンドはどれですか？" \
    "10w" \
    "10j" \
    "10G" \
    "g10" \
    "c" \
    "数字+G で指定行にジャンプします。:10 でも同じ操作が可能です。"

pause

# ----------------------------------------------------------
section "編集コマンド編"

ask_quiz \
    "現在の行をまるごとコピー（ヤンク）するコマンドはどれですか？" \
    "dd" \
    "yy" \
    "pp" \
    "cc" \
    "b" \
    "yy は現在の行をヤンク（コピー）します。dd は削除、cc は変更（削除して挿入モード）、p は貼り付けです。"

ask_quiz \
    "直前の操作を取り消す（Undo）コマンドはどれですか？" \
    "Ctrl+z" \
    "u" \
    "r" \
    "." \
    "b" \
    "u（undo）で直前の操作を取り消します。Ctrl+r でやり直し（redo）ができます。"

pause

# ----------------------------------------------------------
section "検索・置換編"

ask_quiz \
    "ファイル全体で apple を orange に一括置換するコマンドはどれですか？" \
    ":%s/apple/orange/" \
    ":s/apple/orange/g" \
    ":%s/apple/orange/g" \
    ":/apple/orange/g" \
    "c" \
    ":%s/apple/orange/g は全行（%）に対して全出現箇所（g）を置換します。g がないと各行の最初の1つだけ置換されます。"

ask_quiz \
    "文字列 error を前方検索するコマンドはどれですか？" \
    "?error" \
    "/error" \
    ":find error" \
    ":search error" \
    "b" \
    "/pattern で前方検索、?pattern で後方検索です。n で次の候補、N で前の候補に移動します。"

pause

# ----------------------------------------------------------
section "結果発表"
echo ""
echo -e "${GREEN}============================================${RESET}"
echo -e "${GREEN}  クイズ結果: ${SCORE} / ${TOTAL} 問正解${RESET}"
echo -e "${GREEN}============================================${RESET}"
echo ""

if [[ $SCORE -eq $TOTAL ]]; then
    echo -e "${GREEN}パーフェクト！Vimマスターですね！${RESET}"
elif [[ $SCORE -ge 8 ]]; then
    echo -e "${GREEN}素晴らしい！Vimの基本をしっかり理解しています。${RESET}"
elif [[ $SCORE -ge 6 ]]; then
    echo -e "${YELLOW}良い成績です。もう少し練習すればマスターできます。${RESET}"
elif [[ $SCORE -ge 4 ]]; then
    echo -e "${YELLOW}基本は押さえています。苦手な分野を復習しましょう。${RESET}"
else
    echo -e "${CYAN}まだ学習中ですね。教材を読み直してから再挑戦しましょう！${RESET}"
fi

# 結果をファイルに保存
RESULT_FILE="$TMPDIR/quiz_result.txt"
cat > "$RESULT_FILE" <<EOF
Vimコマンドクイズ結果
=====================
日時: $(date '+%Y-%m-%d %H:%M:%S')
スコア: ${SCORE} / ${TOTAL}
正答率: $((SCORE * 100 / TOTAL))%
EOF

echo ""
info "結果は一時ファイルに保存されました。"
info "クイズ完了！一時ファイルは自動的に削除されます。"
