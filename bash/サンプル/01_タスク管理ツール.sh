#!/usr/bin/env bash
# ============================================================
# タスク管理ツール（TODOリスト）
# ============================================================
# 【学べる内容】
#   - 関数の定義と呼び出し
#   - case 文による分岐処理
#   - ファイルの読み書き（リダイレクト）
#   - 配列の操作
#   - 色付きターミナル出力（ANSIエスケープシーケンス）
#   - コマンドライン引数と対話型メニューの両対応
#
# 【実行方法】
#   chmod +x 01_タスク管理ツール.sh
#   ./01_タスク管理ツール.sh              # 対話型メニュー
#   ./01_タスク管理ツール.sh add "牛乳を買う"  # コマンドライン引数
#   ./01_タスク管理ツール.sh list
#   ./01_タスク管理ツール.sh done 1
#   ./01_タスク管理ツール.sh delete 1
# ============================================================
set -euo pipefail

# --- 色の定義 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# --- 設定 ---
TASK_FILE="${HOME}/.tasks.txt"

# タスクファイルが存在しなければ作成する
init_task_file() {
    if [[ ! -f "$TASK_FILE" ]]; then
        touch "$TASK_FILE"
        echo -e "${CYAN}タスクファイルを作成しました: ${TASK_FILE}${RESET}"
    fi
}

# タスクを追加する
add_task() {
    local task="$1"
    echo "[ ] ${task}" >> "$TASK_FILE"
    echo -e "${GREEN}追加しました:${RESET} ${task}"
}

# タスク一覧を表示する
list_tasks() {
    if [[ ! -s "$TASK_FILE" ]]; then
        echo -e "${YELLOW}タスクはありません。${RESET}"
        return
    fi
    echo -e "${BOLD}${BLUE}===== タスク一覧 =====${RESET}"
    local i=1
    while IFS= read -r line; do
        if [[ "$line" == "[x]"* ]]; then
            echo -e "  ${GREEN}${i}. ${line}${RESET}"
        else
            echo -e "  ${i}. ${line}"
        fi
        ((i++))
    done < "$TASK_FILE"
    echo -e "${BOLD}${BLUE}======================${RESET}"
    local total
    total=$(wc -l < "$TASK_FILE")
    local done_count
    done_count=$(grep -c '^\[x\]' "$TASK_FILE" || true)
    echo -e "  合計: ${total} 件 / 完了: ${done_count} 件"
}

# タスクを完了にする
complete_task() {
    local num="$1"
    local total
    total=$(wc -l < "$TASK_FILE")
    if [[ "$num" -lt 1 || "$num" -gt "$total" ]]; then
        echo -e "${RED}エラー: 無効な番号です (1〜${total})${RESET}"
        return 1
    fi
    # 指定行の [ ] を [x] に置換する
    sed -i "${num}s/^\[ \]/[x]/" "$TASK_FILE"
    local task
    task=$(sed -n "${num}p" "$TASK_FILE")
    echo -e "${GREEN}完了にしました:${RESET} ${task}"
}

# タスクを削除する
delete_task() {
    local num="$1"
    local total
    total=$(wc -l < "$TASK_FILE")
    if [[ "$num" -lt 1 || "$num" -gt "$total" ]]; then
        echo -e "${RED}エラー: 無効な番号です (1〜${total})${RESET}"
        return 1
    fi
    local task
    task=$(sed -n "${num}p" "$TASK_FILE")
    sed -i "${num}d" "$TASK_FILE"
    echo -e "${RED}削除しました:${RESET} ${task}"
}

# 対話型メニューを表示する
show_menu() {
    echo ""
    echo -e "${BOLD}${CYAN}--- タスク管理ツール ---${RESET}"
    echo "  1) タスクを追加"
    echo "  2) タスク一覧を表示"
    echo "  3) タスクを完了にする"
    echo "  4) タスクを削除する"
    echo "  5) 終了"
    echo -n "選択してください [1-5]: "
}

# 対話型モードのメインループ
interactive_mode() {
    while true; do
        show_menu
        read -r choice
        case "$choice" in
            1)
                echo -n "タスクの内容を入力: "
                read -r task
                if [[ -n "$task" ]]; then
                    add_task "$task"
                else
                    echo -e "${RED}タスクの内容が空です。${RESET}"
                fi
                ;;
            2) list_tasks ;;
            3)
                list_tasks
                echo -n "完了にする番号を入力: "
                read -r num
                if [[ "$num" =~ ^[0-9]+$ ]]; then
                    complete_task "$num"
                else
                    echo -e "${RED}数値を入力してください。${RESET}"
                fi
                ;;
            4)
                list_tasks
                echo -n "削除する番号を入力: "
                read -r num
                if [[ "$num" =~ ^[0-9]+$ ]]; then
                    delete_task "$num"
                else
                    echo -e "${RED}数値を入力してください。${RESET}"
                fi
                ;;
            5)
                echo -e "${CYAN}終了します。お疲れさまでした!${RESET}"
                exit 0
                ;;
            *)
                echo -e "${RED}無効な選択です。1〜5 を入力してください。${RESET}"
                ;;
        esac
    done
}

# --- メイン処理 ---
init_task_file

# コマンドライン引数がある場合はそちらを処理する
if [[ $# -gt 0 ]]; then
    command="$1"
    shift
    case "$command" in
        add)
            [[ $# -eq 0 ]] && { echo -e "${RED}使い方: $0 add \"タスク内容\"${RESET}"; exit 1; }
            add_task "$*"
            ;;
        list)   list_tasks ;;
        done)
            [[ $# -eq 0 ]] && { echo -e "${RED}使い方: $0 done <番号>${RESET}"; exit 1; }
            complete_task "$1"
            ;;
        delete)
            [[ $# -eq 0 ]] && { echo -e "${RED}使い方: $0 delete <番号>${RESET}"; exit 1; }
            delete_task "$1"
            ;;
        *)
            echo -e "${RED}不明なコマンド: ${command}${RESET}"
            echo "使い方: $0 {add|list|done|delete} [引数]"
            exit 1
            ;;
    esac
else
    # 引数がなければ対話型モードで起動する
    interactive_mode
fi
