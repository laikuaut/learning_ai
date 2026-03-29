#!/usr/bin/env bash
# ============================================================
# インタラクティブクイズゲーム（Bash/Linux 知識編）
# ============================================================
# 【学べる内容】
#   - 配列（通常配列・連想配列）の活用
#   - select 文による選択肢メニュー
#   - read コマンドのオプション（-t でタイムアウト、-r で安全入力）
#   - 条件分岐（if, case）
#   - 算術演算（$(( )) による計算）
#   - ANSIエスケープシーケンスによる色付き出力
#
# 【実行方法】
#   chmod +x 04_インタラクティブクイズゲーム.sh
#   ./04_インタラクティブクイズゲーム.sh
# ============================================================
set -euo pipefail

# --- 色の定義 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# --- 設定 ---
TIME_LIMIT=15       # 1問あたりの制限時間（秒）
TOTAL_QUESTIONS=5   # 出題数

# --- スコア管理 ---
score=0
answered=0
correct_list=()
wrong_list=()

# 区切り線を表示する
separator() {
    printf '%50s\n' '' | tr ' ' '-'
}

# タイトル画面を表示する
show_title() {
    clear 2>/dev/null || true
    echo -e "${BOLD}${CYAN}"
    echo "  ╔══════════════════════════════════════╗"
    echo "  ║   Bash / Linux クイズゲーム          ║"
    echo "  ║                                      ║"
    echo "  ║   制限時間: ${TIME_LIMIT}秒 / 全${TOTAL_QUESTIONS}問           ║"
    echo "  ╚══════════════════════════════════════╝"
    echo -e "${RESET}"
    echo ""
    echo -n "Enter キーを押してスタート..."
    read -r
}

# =====================================================
# 問題データ（配列で管理）
# 形式: "問題文|選択肢A|選択肢B|選択肢C|選択肢D|正解番号"
# =====================================================
questions=(
    "ファイルの中身を表示するコマンドはどれですか？|cat|mkdir|rm|chmod|1"
    "カレントディレクトリを表示するコマンドはどれですか？|ls|pwd|cd|whoami|2"
    "ファイルの権限を変更するコマンドはどれですか？|chown|mv|chmod|grep|3"
    "テキストファイルからパターンを検索するコマンドはどれですか？|find|grep|sed|awk|2"
    "ディレクトリを再帰的に削除するオプションはどれですか？|rm -f|rm -i|rm -r|rm -v|3"
    "パイプの役割として正しいのはどれですか？|ファイルを削除する|コマンドの出力を別のコマンドの入力に渡す|変数を定義する|プロセスを終了する|2"
    "Bashスクリプトの1行目に書くシバン（shebang）はどれですか？|#!/bin/sh|#!/usr/bin/env bash|#!/usr/bin/python|#!bash|2"
    "環境変数 HOME が示すものはどれですか？|現在のディレクトリ|ユーザーのホームディレクトリ|ルートディレクトリ|一時ディレクトリ|2"
    "ファイルの行数を数えるコマンドはどれですか？|wc -l|wc -w|wc -c|wc -m|1"
    "標準エラー出力のファイルディスクリプタ番号はどれですか？|0|1|2|3|3"
    "Bashで変数に値を代入する正しい書き方はどれですか？|name = value|name =value|name= value|name=value|4"
    "コマンドの実行結果を変数に入れる書き方はどれですか？|var=\$(command)|var=command|var={command}|var=[command]|1"
    "ファイルが存在するか確認する test コマンドのオプションはどれですか？|-d|-f|-r|-x|2"
    "プロセスを強制終了するシグナルはどれですか？|SIGHUP|SIGINT|SIGKILL|SIGTERM|3"
    "直前のコマンドの終了ステータスを参照する特殊変数はどれですか？|\$#|\$@|\$?|\$!|3"
)

# 問題をシャッフルする（Fisher-Yatesアルゴリズム）
shuffle_questions() {
    local n=${#questions[@]}
    for ((i = n - 1; i > 0; i--)); do
        local j=$((RANDOM % (i + 1)))
        local tmp="${questions[$i]}"
        questions[$i]="${questions[$j]}"
        questions[$j]="$tmp"
    done
}

# 1問を出題して結果を返す
ask_question() {
    local q_data="$1"
    local q_num="$2"

    # パイプ区切りでデータを分割する
    IFS='|' read -r question opt_a opt_b opt_c opt_d correct_num <<< "$q_data"

    echo ""
    echo -e "${BOLD}${YELLOW}【第${q_num}問】${RESET}"
    echo -e "  ${question}"
    echo ""
    echo -e "    ${CYAN}1)${RESET} ${opt_a}"
    echo -e "    ${CYAN}2)${RESET} ${opt_b}"
    echo -e "    ${CYAN}3)${RESET} ${opt_c}"
    echo -e "    ${CYAN}4)${RESET} ${opt_d}"
    echo ""

    # 制限時間付きで入力を受け付ける
    local answer=""
    echo -ne "  回答を入力してください (1-4) [${TIME_LIMIT}秒以内]: "
    if ! read -r -t "$TIME_LIMIT" answer; then
        echo ""
        echo -e "  ${RED}時間切れです！${RESET}"
        wrong_list+=("Q${q_num}: ${question} -> 正解は ${correct_num})")
        return 1
    fi

    # 回答を判定する
    if [[ "$answer" == "$correct_num" ]]; then
        echo -e "  ${GREEN}正解です！${RESET}"
        correct_list+=("Q${q_num}: ${question}")
        return 0
    else
        echo -e "  ${RED}不正解... 正解は ${correct_num}) でした。${RESET}"
        wrong_list+=("Q${q_num}: ${question} -> 正解は ${correct_num})")
        return 1
    fi
}

# 結果サマリーを表示する
show_results() {
    echo ""
    echo ""
    echo -e "${BOLD}${CYAN}╔══════════════════════════════════════╗${RESET}"
    echo -e "${BOLD}${CYAN}║         結果発表                     ║${RESET}"
    echo -e "${BOLD}${CYAN}╚══════════════════════════════════════╝${RESET}"
    echo ""

    # スコアの表示
    local pct=0
    if [[ $answered -gt 0 ]]; then
        pct=$(( score * 100 / answered ))
    fi
    printf "  スコア : %d / %d 問正解 (%d%%)\n" "$score" "$answered" "$pct"

    # スコアバーを表示する
    local bar=""
    local filled=$(( pct / 5 ))
    for ((i = 0; i < 20; i++)); do
        if [[ $i -lt $filled ]]; then
            bar+="█"
        else
            bar+="░"
        fi
    done
    echo -e "  成績   : [${bar}] ${pct}%"
    echo ""

    # 評価メッセージを表示する
    if [[ $pct -ge 80 ]]; then
        echo -e "  ${GREEN}${BOLD}素晴らしい！ Bash マスターへの道を歩んでいます！${RESET}"
    elif [[ $pct -ge 60 ]]; then
        echo -e "  ${YELLOW}${BOLD}なかなかの成績です！ もう少しで上級者です。${RESET}"
    elif [[ $pct -ge 40 ]]; then
        echo -e "  ${YELLOW}惜しい！ 復習すればもっと伸びます。${RESET}"
    else
        echo -e "  ${RED}まだまだこれから！ 教材を読み直してみましょう。${RESET}"
    fi
    echo ""

    # 正解した問題を表示する
    if [[ ${#correct_list[@]} -gt 0 ]]; then
        echo -e "  ${GREEN}--- 正解した問題 ---${RESET}"
        for item in "${correct_list[@]}"; do
            echo -e "    ${GREEN}○${RESET} ${item}"
        done
    fi

    # 間違えた問題を表示する
    if [[ ${#wrong_list[@]} -gt 0 ]]; then
        echo -e "  ${RED}--- 間違えた / 時間切れの問題 ---${RESET}"
        for item in "${wrong_list[@]}"; do
            echo -e "    ${RED}×${RESET} ${item}"
        done
    fi
    echo ""
    separator
}

# --- メイン処理 ---
show_title
shuffle_questions

echo ""
echo -e "${BOLD}それではクイズを始めます！${RESET}"
separator

for ((i = 0; i < TOTAL_QUESTIONS && i < ${#questions[@]}; i++)); do
    answered=$((answered + 1))
    if ask_question "${questions[$i]}" "$((i + 1))"; then
        score=$((score + 1))
    fi
    separator
done

show_results
echo -e "${CYAN}お疲れさまでした！${RESET}"
