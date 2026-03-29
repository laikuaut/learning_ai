#!/bin/bash
# =============================================================================
# 学べる内容：
#   - vimrcに含めるべき推奨設定
#   - よくある間違いやアンチパターン
#   - map vs noremap の違い
#   - augroup の重要性
#   - 設定の重複チェック
#
# 実行方法：
#   chmod +x 02_vimrcバリデータ.sh
#   ./02_vimrcバリデータ.sh                  # ~/.vimrc をチェック
#   ./02_vimrcバリデータ.sh /path/to/vimrc   # 指定ファイルをチェック
# =============================================================================

# --- 色付き出力用 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# カウンター
warnings=0
errors=0
info_count=0

warn() {
    echo -e "  ${YELLOW}⚠ 警告:${RESET} $1"
    ((warnings++))
}

error() {
    echo -e "  ${RED}✗ エラー:${RESET} $1"
    ((errors++))
}

ok() {
    echo -e "  ${GREEN}✓ OK:${RESET} $1"
}

info() {
    echo -e "  ${CYAN}ℹ 情報:${RESET} $1"
    ((info_count++))
}

# =============================================================================
# 対象ファイルの決定
# =============================================================================

VIMRC_FILE="${1:-$HOME/.vimrc}"

echo -e "${BOLD}=============================================${RESET}"
echo -e "${BOLD}  vimrc バリデータ${RESET}"
echo -e "${BOLD}=============================================${RESET}"
echo ""

if [ ! -f "$VIMRC_FILE" ]; then
    echo -e "${RED}エラー: ファイルが見つかりません: ${VIMRC_FILE}${RESET}"
    echo ""
    echo "使い方:"
    echo "  $0                  # ~/.vimrc をチェック"
    echo "  $0 /path/to/vimrc   # 指定ファイルをチェック"
    exit 1
fi

echo -e "チェック対象: ${CYAN}${VIMRC_FILE}${RESET}"
total_lines=$(wc -l < "$VIMRC_FILE")
echo -e "総行数: ${total_lines} 行"
echo ""

# コメントと空行を除いた有効行数
effective_lines=$(grep -cvE '^\s*"|^\s*$' "$VIMRC_FILE" 2>/dev/null || echo 0)
echo -e "有効な設定行数: ${effective_lines} 行"
echo ""

# =============================================================================
# チェック1: 基本的な推奨設定の存在確認
# =============================================================================

echo -e "${BOLD}【チェック1】基本的な推奨設定${RESET}"

# nocompatible
if grep -qE '^\s*set\s+nocompatible' "$VIMRC_FILE"; then
    ok "set nocompatible が設定されています"
else
    warn "set nocompatible が見つかりません"
    info "  → Vi互換モードを無効にし、Vimの全機能を使えるようにします"
fi

# encoding
if grep -qE '^\s*set\s+encoding=utf-8' "$VIMRC_FILE"; then
    ok "encoding=utf-8 が設定されています"
else
    warn "set encoding=utf-8 が見つかりません"
    info "  → 文字化けを防ぐためにUTF-8を推奨します"
fi

# filetype
if grep -qE '^\s*filetype\s+plugin\s+indent\s+on' "$VIMRC_FILE"; then
    ok "filetype plugin indent on が設定されています"
else
    if grep -qE '^\s*filetype\s+' "$VIMRC_FILE"; then
        warn "filetype の設定が不完全な可能性があります"
        info "  → 'filetype plugin indent on' で全機能を有効にすることを推奨します"
    else
        warn "filetype の設定が見つかりません"
        info "  → 'filetype plugin indent on' を追加してファイルタイプ別設定を有効にしましょう"
    fi
fi

# syntax
if grep -qE '^\s*syntax\s+(enable|on)' "$VIMRC_FILE"; then
    ok "シンタックスハイライトが有効化されています"
else
    warn "syntax enable/on が見つかりません"
    info "  → シンタックスハイライトはコード可読性を大幅に向上させます"
fi

# backspace
if grep -qE '^\s*set\s+backspace=' "$VIMRC_FILE"; then
    ok "backspace が設定されています"
else
    warn "set backspace=indent,eol,start が見つかりません"
    info "  → バックスペースが期待通りに動作しない場合があります"
fi

echo ""

# =============================================================================
# チェック2: map vs noremap
# =============================================================================

echo -e "${BOLD}【チェック2】キーマッピングの安全性${RESET}"

# map（noremap以外の）を使っている行を検出
# ただし noremap, unmap, mapclear は除外
map_lines=$(grep -nE '^\s*(n|v|i|x|s|o|c|t)?map\s+' "$VIMRC_FILE" | grep -vE 'noremap|unmap|mapclear' 2>/dev/null)

if [ -n "$map_lines" ]; then
    warn "map（再帰マッピング）が使用されています。noremap の使用を推奨します："
    while IFS= read -r line; do
        echo -e "    ${YELLOW}行 ${line}${RESET}"
    done <<< "$map_lines"
    info "  → map はマッピングが連鎖的に展開され予期しない動作を引き起こす可能性があります"
    info "  → 特別な理由がない限り noremap（nnoremap, inoremap 等）を使いましょう"
else
    ok "再帰マッピング（map）は検出されませんでした"
fi

echo ""

# =============================================================================
# チェック3: autocmd と augroup
# =============================================================================

echo -e "${BOLD}【チェック3】autocmd の安全性${RESET}"

autocmd_count=$(grep -cE '^\s*autocmd\s+' "$VIMRC_FILE" 2>/dev/null || echo 0)
augroup_count=$(grep -cE '^\s*augroup\s+' "$VIMRC_FILE" 2>/dev/null || echo 0)

if [ "$autocmd_count" -gt 0 ]; then
    info "autocmd が ${autocmd_count} 件見つかりました"

    if [ "$augroup_count" -eq 0 ]; then
        warn "autocmd が augroup で囲まれていない可能性があります"
        info "  → vimrcを再読み込みするたびに autocmd が重複登録されます"
        info "  → 以下のように augroup で囲み、autocmd! でリセットしましょう："
        info ""
        info "    augroup MyGroup"
        info "      autocmd!"
        info "      autocmd FileType python setlocal ..."
        info "    augroup END"
    else
        # augroup 内に autocmd! があるか確認
        if grep -qE '^\s*autocmd!' "$VIMRC_FILE"; then
            ok "augroup 内で autocmd! によるリセットが行われています"
        else
            warn "augroup はありますが autocmd! （リセット）が見つかりません"
            info "  → augroup の先頭に autocmd! を追加して重複登録を防ぎましょう"
        fi
    fi
else
    info "autocmd は使用されていません"
fi

echo ""

# =============================================================================
# チェック4: 設定の重複
# =============================================================================

echo -e "${BOLD}【チェック4】設定の重複チェック${RESET}"

# 'set xxx' 形式の設定を抽出して重複を検出
duplicates=$(grep -oE '^\s*set\s+\S+' "$VIMRC_FILE" | \
    sed 's/^\s*set\s\+//' | \
    sed 's/=.*//' | \
    sed 's/^no//' | \
    sort | uniq -d)

if [ -n "$duplicates" ]; then
    warn "以下の設定が複数回定義されています："
    while IFS= read -r setting; do
        if [ -n "$setting" ]; then
            # 該当行を表示
            lines=$(grep -nE "^\s*set\s+(no)?${setting}" "$VIMRC_FILE" | head -5)
            echo -e "    ${YELLOW}${setting}:${RESET}"
            while IFS= read -r l; do
                echo "      行 $l"
            done <<< "$lines"
        fi
    done <<< "$duplicates"
    info "  → 後に書かれた設定が優先されます。意図的でなければ整理しましょう"
else
    ok "設定の重複は検出されませんでした"
fi

echo ""

# =============================================================================
# チェック5: 非推奨・危険な設定
# =============================================================================

echo -e "${BOLD}【チェック5】非推奨・注意が必要な設定${RESET}"

# compatible
if grep -qE '^\s*set\s+compatible\b' "$VIMRC_FILE"; then
    error "set compatible が設定されています！"
    info "  → Vi互換モードはVimの多くの機能を無効にします"
fi

# modeline（セキュリティリスク）
if grep -qE '^\s*set\s+modeline\b' "$VIMRC_FILE"; then
    warn "set modeline が有効になっています"
    info "  → 悪意あるファイルによるコード実行のリスクがあります"
    info "  → 信頼できるファイルのみを扱う場合は問題ありません"
fi

# exrc（セキュリティリスク）
if grep -qE '^\s*set\s+exrc\b' "$VIMRC_FILE"; then
    warn "set exrc が有効になっています"
    info "  → カレントディレクトリの .vimrc を読み込むため、セキュリティリスクがあります"
    info "  → 使用する場合は set secure も合わせて設定してください"
fi

# 非常に大きな scrolloff
scrolloff_val=$(grep -oE '^\s*set\s+scrolloff=\d+' "$VIMRC_FILE" | grep -oE '[0-9]+' | tail -1)
if [ -n "$scrolloff_val" ] && [ "$scrolloff_val" -gt 999 ]; then
    info "scrolloff=${scrolloff_val} が設定されています（カーソルが常に画面中央）"
fi

echo ""

# =============================================================================
# チェック6: インデント設定の整合性
# =============================================================================

echo -e "${BOLD}【チェック6】インデント設定の整合性${RESET}"

has_expandtab=$(grep -qE '^\s*set\s+expandtab' "$VIMRC_FILE" && echo "yes" || echo "no")
has_noexpandtab=$(grep -qE '^\s*set\s+noexpandtab' "$VIMRC_FILE" && echo "yes" || echo "no")

tabstop_val=$(grep -oE '^\s*set\s+tabstop=\d+' "$VIMRC_FILE" | grep -oE '[0-9]+' | tail -1)
shiftwidth_val=$(grep -oE '^\s*set\s+shiftwidth=\d+' "$VIMRC_FILE" | grep -oE '[0-9]+' | tail -1)
softtabstop_val=$(grep -oE '^\s*set\s+softtabstop=\d+' "$VIMRC_FILE" | grep -oE '[0-9]+' | tail -1)

if [ "$has_expandtab" = "yes" ] && [ "$has_noexpandtab" = "yes" ]; then
    warn "expandtab と noexpandtab の両方が設定されています（後者が優先されます）"
fi

if [ -n "$tabstop_val" ] && [ -n "$shiftwidth_val" ]; then
    if [ "$tabstop_val" != "$shiftwidth_val" ]; then
        warn "tabstop(${tabstop_val}) と shiftwidth(${shiftwidth_val}) の値が異なります"
        info "  → 意図的でなければ揃えることを推奨します"
    else
        ok "tabstop と shiftwidth の値が一致しています (${tabstop_val})"
    fi
fi

if [ -n "$softtabstop_val" ] && [ -n "$tabstop_val" ]; then
    if [ "$softtabstop_val" != "$tabstop_val" ]; then
        info "softtabstop(${softtabstop_val}) と tabstop(${tabstop_val}) の値が異なります"
    fi
fi

echo ""

# =============================================================================
# チェック7: Leader キー設定
# =============================================================================

echo -e "${BOLD}【チェック7】Leaderキー設定${RESET}"

if grep -qE '^\s*let\s+mapleader' "$VIMRC_FILE"; then
    leader_val=$(grep -oE "let\s+mapleader\s*=\s*\S+" "$VIMRC_FILE" | tail -1)
    ok "Leaderキーが設定されています: ${leader_val}"
else
    info "Leaderキーは設定されていません（デフォルト: \\）"
    info "  → スペースキーをLeaderにすると便利です: let mapleader = \"\\<Space>\""
fi

echo ""

# =============================================================================
# サマリー
# =============================================================================

echo -e "${BOLD}=============================================${RESET}"
echo -e "${BOLD}  チェック結果サマリー${RESET}"
echo -e "${BOLD}=============================================${RESET}"

if [ "$errors" -gt 0 ]; then
    echo -e "  ${RED}エラー:   ${errors} 件${RESET}"
fi
if [ "$warnings" -gt 0 ]; then
    echo -e "  ${YELLOW}警告:     ${warnings} 件${RESET}"
fi
echo -e "  ${CYAN}情報:     ${info_count} 件${RESET}"
echo ""

if [ "$errors" -eq 0 ] && [ "$warnings" -eq 0 ]; then
    echo -e "  ${GREEN}${BOLD}素晴らしい！問題は検出されませんでした。${RESET}"
elif [ "$errors" -eq 0 ] && [ "$warnings" -le 2 ]; then
    echo -e "  ${GREEN}概ね良好です。警告の内容を確認してみてください。${RESET}"
else
    echo -e "  ${YELLOW}いくつかの改善点があります。上記のメッセージを参考に修正しましょう。${RESET}"
fi

echo ""
