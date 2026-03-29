#!/bin/bash
# =============================================================================
# 学べる内容：
#   - Vimの基本的なキーマッピングとその意味
#   - vimrc設定の各オプションの役割
#   - map と noremap の違い
#   - Leader キーの概念
#   - autocmd や augroup の使い方
#
# 実行方法：
#   chmod +x 03_キーマッピングクイズ.sh
#   ./03_キーマッピングクイズ.sh
# =============================================================================

# --- 色付き出力用 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# スコア管理
score=0
total=0

# =============================================================================
# クイズ出題関数
# =============================================================================

ask_question() {
    local question="$1"
    local opt_a="$2"
    local opt_b="$3"
    local opt_c="$4"
    local opt_d="$5"
    local correct="$6"
    local explanation="$7"

    ((total++))

    echo ""
    echo -e "${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}  問題 ${total}${RESET}"
    echo -e "${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""
    echo -e "  ${question}"
    echo ""
    echo -e "  ${BOLD}A)${RESET} ${opt_a}"
    echo -e "  ${BOLD}B)${RESET} ${opt_b}"
    echo -e "  ${BOLD}C)${RESET} ${opt_c}"
    echo -e "  ${BOLD}D)${RESET} ${opt_d}"
    echo ""

    while true; do
        read -rp "  あなたの回答 [A/B/C/D]: " answer
        answer=$(echo "$answer" | tr '[:lower:]' '[:upper:]')
        if [[ "$answer" =~ ^[ABCD]$ ]]; then
            break
        fi
        echo -e "  ${RED}A, B, C, D のいずれかを入力してください${RESET}"
    done

    if [ "$answer" = "$correct" ]; then
        echo ""
        echo -e "  ${GREEN}${BOLD}◎ 正解！${RESET}"
        ((score++))
    else
        echo ""
        echo -e "  ${RED}${BOLD}✗ 不正解... 正解は ${correct} です${RESET}"
    fi

    echo ""
    echo -e "  ${CYAN}【解説】${RESET}"
    echo -e "  ${explanation}"
    echo ""

    read -rp "  [Enter] で次の問題へ..."
}

# =============================================================================
# メイン
# =============================================================================

clear 2>/dev/null || true

echo -e "${BOLD}${YELLOW}"
echo "  ╔═══════════════════════════════════════════════╗"
echo "  ║                                               ║"
echo "  ║   Vim / vimrc キーマッピングクイズ            ║"
echo "  ║                                               ║"
echo "  ║   全10問であなたのVim知識を試しましょう！     ║"
echo "  ║                                               ║"
echo "  ╚═══════════════════════════════════════════════╝"
echo -e "${RESET}"
echo ""
read -rp "  [Enter] でクイズ開始..."

# --- 問題1 ---
ask_question \
    "vimrcで 'set nocompatible' は何を意味しますか？" \
    "Vimを互換モードで起動する" \
    "Vi互換モードを無効にし、Vimの拡張機能を有効にする" \
    "プラグインの互換性チェックを無効にする" \
    "古いバージョンのvimrcとの互換性を保つ" \
    "B" \
    "nocompatible は Vi互換モードを無効にする設定です。
  これにより、Vimが持つ多くの拡張機能（ビジュアルモード、
  複数アンドゥ等）が使えるようになります。現代のvimrcでは
  必ず設定すべき項目です。"

# --- 問題2 ---
ask_question \
    "'nnoremap' と 'nmap' の最も重要な違いは何ですか？" \
    "nnoremap はノーマルモード専用、nmap は全モード対応" \
    "nnoremap は再帰的マッピング、nmap は非再帰的マッピング" \
    "nnoremap は非再帰的マッピング、nmap は再帰的マッピング" \
    "機能的な違いはなく、単なるエイリアス" \
    "C" \
    "nnoremap は「非再帰的（non-recursive）」マッピングです。
  マッピング先のキーがさらに別のマッピングに展開されることを
  防ぎます。nmap は再帰的なので、予期しない動作の原因になります。
  特別な理由がない限り、常に noremap 系を使いましょう。"

# --- 問題3 ---
ask_question \
    "'let mapleader = \"\\\\<Space>\"' は何を設定していますか？" \
    "スペースキーを無効化する" \
    "スペースキーをリーダーキーに設定する" \
    "スペースキーでファイルを保存する" \
    "スペースキーで検索を開始する" \
    "B" \
    "Leader キーは、カスタムキーマッピングの接頭辞として使う
  特別なキーです。デフォルトは \\ ですが、スペースキーに
  変更すると、<Leader>w や <Leader>q のようなマッピングが
  押しやすくなります。"

# --- 問題4 ---
ask_question \
    "'set expandtab' の効果は何ですか？" \
    "タブ文字の表示幅を変更する" \
    "タブキーを押した時にスペースを挿入する" \
    "タブキーを無効化する" \
    "既存のタブ文字をスペースに自動変換する" \
    "B" \
    "expandtab を設定すると、Tab キーを押した際にタブ文字（\\t）
  の代わりにスペース文字が挿入されます。多くのプロジェクトで
  スペースインデントが標準なので、設定しておくと便利です。
  なお、既存のタブ変換には :retab コマンドを使います。"

# --- 問題5 ---
ask_question \
    "autocmd を augroup で囲む理由は何ですか？" \
    "autocmd の実行速度を向上させるため" \
    "autocmd にエラーハンドリングを追加するため" \
    "vimrc 再読み込み時に autocmd の重複登録を防ぐため" \
    "autocmd を特定のファイルタイプでのみ有効にするため" \
    "C" \
    ":source ~/.vimrc でvimrcを再読み込みすると、autocmd が
  重複して登録され、同じ処理が複数回実行されてしまいます。
  augroup で囲み、先頭に autocmd! を書くことで、
  再読み込み時にグループ内のautocmdがリセットされます。"

# --- 問題6 ---
ask_question \
    "'inoremap jj <Esc>' はどのような動作をしますか？" \
    "ノーマルモードで jj を押すとEscと同じ動作をする" \
    "挿入モードで jj を素早く入力するとノーマルモードに戻る" \
    "ビジュアルモードで jj を押すと選択を解除する" \
    "コマンドモードで jj を押すとキャンセルする" \
    "B" \
    "inoremap は挿入モード（Insert mode）用の非再帰マッピングです。
  jj という文字列は通常のテキストではほぼ出現しないため、
  Escキーの代替として人気のあるマッピングです。
  ホームポジションから手を動かさずにモードを切り替えられます。"

# --- 問題7 ---
ask_question \
    "'set hlsearch' と 'set incsearch' の組み合わせは？" \
    "検索結果のハイライト + インクリメンタル検索" \
    "検索履歴の保存 + 逆方向検索" \
    "正規表現検索 + 大文字小文字無視" \
    "複数ファイル検索 + 置換確認" \
    "A" \
    "hlsearch は検索にマッチした全箇所をハイライト表示します。
  incsearch は検索文字の入力中にリアルタイムで最初のマッチに
  ジャンプします。この2つの組み合わせで、検索体験が大幅に
  向上します。:nohlsearch でハイライトを消せます。"

# --- 問題8 ---
ask_question \
    "'set wildmenu' は何を有効にしますか？" \
    "ファイルブラウザを開く" \
    "コマンドラインでのTab補完を視覚的に表示する" \
    "自動保存機能を有効にする" \
    "ワイルドカード検索を有効にする" \
    "B" \
    "wildmenu を有効にすると、コマンドライン（:）でTabキーを
  押した際に、候補が画面下部にビジュアルに表示されます。
  wildmode=list:longest,full と組み合わせると、最長一致で
  補完しつつ、さらにTabを押すと候補を切り替えられます。"

# --- 問題9 ---
ask_question \
    "'set scrolloff=5' はどのような効果がありますか？" \
    "5行ずつスクロールする" \
    "カーソル位置から上下5行を常に表示する（余白を確保）" \
    "5秒後に自動スクロールする" \
    "最大5つのウィンドウまでスクロールを同期する" \
    "B" \
    "scrolloff はカーソルの上下に常に表示される最小行数を指定します。
  5 に設定すると、カーソルが画面端から5行以内に来ると
  自動的にスクロールします。文脈を常に把握できるので
  コードの読みやすさが向上します。999にすると常に画面中央になります。"

# --- 問題10 ---
ask_question \
    "以下のvimrc設定のうち、セキュリティリスクがあるものはどれですか？" \
    "set number（行番号表示）" \
    "set modeline（ファイル内のVim設定を実行）" \
    "set cursorline（カーソル行ハイライト）" \
    "set laststatus=2（ステータスライン常時表示）" \
    "B" \
    "modeline はファイルの先頭や末尾に書かれたVimの設定行
  （例: /* vim: set ts=4 : */）を自動実行する機能です。
  悪意あるファイルに危険なコマンドが仕込まれる可能性があるため、
  セキュリティリスクがあります。nomodeline で無効にできます。"

# =============================================================================
# 結果表示
# =============================================================================

clear 2>/dev/null || true

echo ""
echo -e "${BOLD}${YELLOW}"
echo "  ╔═══════════════════════════════════════════════╗"
echo "  ║                                               ║"
echo "  ║            クイズ結果                         ║"
echo "  ║                                               ║"
echo "  ╚═══════════════════════════════════════════════╝"
echo -e "${RESET}"
echo ""
echo -e "  ${BOLD}正解数: ${score} / ${total}${RESET}"
echo ""

# スコアに応じたバーグラフ表示
bar_width=30
filled=$((score * bar_width / total))
empty=$((bar_width - filled))
bar=$(printf "%${filled}s" | tr ' ' '█')
bar_empty=$(printf "%${empty}s" | tr ' ' '░')

percentage=$((score * 100 / total))
echo -e "  [${GREEN}${bar}${RESET}${bar_empty}] ${percentage}%"
echo ""

# 評価メッセージ
if [ "$score" -eq "$total" ]; then
    echo -e "  ${GREEN}${BOLD}★★★ パーフェクト！素晴らしいVim知識です！ ★★★${RESET}"
    echo ""
    echo -e "  あなたはVimの達人です。vimrcを自在にカスタマイズできるでしょう。"
elif [ "$score" -ge 8 ]; then
    echo -e "  ${GREEN}${BOLD}★★ 優秀！よくVimを理解しています ★★${RESET}"
    echo ""
    echo -e "  基本的な知識はしっかり身についています。"
    echo -e "  間違えた問題を復習して、さらにスキルアップしましょう。"
elif [ "$score" -ge 6 ]; then
    echo -e "  ${YELLOW}${BOLD}★ 合格ライン！基本は押さえています${RESET}"
    echo ""
    echo -e "  基礎知識はありますが、まだ学ぶべきことがあります。"
    echo -e "  vimrcの教材を読み返して理解を深めましょう。"
elif [ "$score" -ge 4 ]; then
    echo -e "  ${YELLOW}もう少し！vimrcの基本を復習しましょう${RESET}"
    echo ""
    echo -e "  Vimの設定に関する理解をさらに深める必要があります。"
    echo -e "  教材を読み、実際にvimrcを編集してみましょう。"
else
    echo -e "  ${RED}まだまだこれから！一緒に学んでいきましょう${RESET}"
    echo ""
    echo -e "  Vimの設定はたくさんありますが、一つずつ覚えれば大丈夫です。"
    echo -e "  まずは基本的な設定から始めてみましょう。"
fi

echo ""
echo -e "  ${CYAN}ヒント: このクイズを何度も受けて満点を目指しましょう！${RESET}"
echo ""
