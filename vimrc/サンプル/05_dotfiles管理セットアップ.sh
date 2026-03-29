#!/bin/bash
# =============================================================================
# 学べる内容：
#   - dotfiles管理の基本的な考え方とメリット
#   - シンボリックリンクによる設定ファイル管理
#   - Gitを使ったdotfilesのバージョン管理
#   - 複数マシン間での設定共有の方法
#
# 実行方法：
#   chmod +x 05_dotfiles管理セットアップ.sh
#
#   # ドライランモード（デフォルト）- 実行されるコマンドを表示するだけ
#   ./05_dotfiles管理セットアップ.sh
#
#   # 実際に実行する場合（--execute オプション）
#   ./05_dotfiles管理セットアップ.sh --execute
# =============================================================================

# --- 色付き出力用 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# --- モード判定 ---
DRY_RUN=true
if [ "$1" = "--execute" ] || [ "$1" = "-x" ]; then
    DRY_RUN=false
fi

# --- ヘルパー関数 ---

# コマンドを表示し、実行モードなら実行する
run_cmd() {
    local cmd="$1"
    if $DRY_RUN; then
        echo -e "    ${CYAN}[ドライラン]${RESET} $cmd"
    else
        echo -e "    ${GREEN}[実行]${RESET} $cmd"
        eval "$cmd"
        if [ $? -ne 0 ]; then
            echo -e "    ${RED}[エラー] コマンドが失敗しました${RESET}"
            return 1
        fi
    fi
}

# 確認プロンプト
confirm() {
    local message="$1"
    echo ""
    echo -e "  ${BOLD}${message}${RESET}"

    if $DRY_RUN; then
        echo -e "  ${CYAN}（ドライランモード: 自動で「はい」として続行）${RESET}"
        return 0
    fi

    while true; do
        read -rp "  続行しますか？ [y/n]: " answer
        case "$answer" in
            [Yy]|[Yy][Ee][Ss]) return 0 ;;
            [Nn]|[Nn][Oo]) return 1 ;;
            *) echo -e "  ${RED}y または n を入力してください${RESET}" ;;
        esac
    done
}

section_header() {
    echo ""
    echo -e "${BOLD}${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}${YELLOW}  $1${RESET}"
    echo -e "${BOLD}${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
}

# =============================================================================
# メイン処理
# =============================================================================

DOTFILES_DIR="$HOME/dotfiles"

echo -e "${BOLD}"
echo "  ╔═══════════════════════════════════════════════╗"
echo "  ║                                               ║"
echo "  ║   dotfiles 管理セットアップ                   ║"
echo "  ║   vimrc をバージョン管理しましょう            ║"
echo "  ║                                               ║"
echo "  ╚═══════════════════════════════════════════════╝"
echo -e "${RESET}"

if $DRY_RUN; then
    echo -e "  ${CYAN}${BOLD}※ ドライランモード（実際のファイル操作は行いません）${RESET}"
    echo -e "  ${CYAN}  実行する場合は --execute オプションを付けてください：${RESET}"
    echo -e "  ${CYAN}  $0 --execute${RESET}"
else
    echo -e "  ${RED}${BOLD}※ 実行モード（実際にファイル操作を行います）${RESET}"
fi

echo ""
echo -e "  ${BOLD}dotfiles管理とは？${RESET}"
echo ""
echo "  Linuxの設定ファイル（.vimrc, .bashrc 等）は「ドットファイル」と"
echo "  呼ばれます。これらをGitで管理することで："
echo ""
echo "    1. 設定の変更履歴を記録できる"
echo "    2. 複数のマシンで同じ設定を使える"
echo "    3. 設定を壊しても簡単に元に戻せる"
echo "    4. GitHubで他の人と設定を共有できる"
echo ""

# =============================================================================
# ステップ1: dotfilesディレクトリの作成
# =============================================================================

section_header "ステップ1: dotfiles ディレクトリの作成"
echo ""
echo "  設定ファイルを集約するディレクトリを作成します。"
echo -e "  場所: ${CYAN}${DOTFILES_DIR}${RESET}"
echo ""

if [ -d "$DOTFILES_DIR" ]; then
    echo -e "  ${YELLOW}注意: ${DOTFILES_DIR} は既に存在します${RESET}"
else
    if confirm "~/dotfiles ディレクトリを作成しますか？"; then
        run_cmd "mkdir -p \"${DOTFILES_DIR}\""
        echo ""
        echo -e "  ${GREEN}ディレクトリ構成の説明：${RESET}"
        echo "    ~/dotfiles/"
        echo "    ├── .vimrc          # Vim設定"
        echo "    ├── .bashrc         # Bash設定（将来）"
        echo "    ├── .gitconfig      # Git設定（将来）"
        echo "    └── setup.sh        # セットアップスクリプト（将来）"
    else
        echo -e "  ${YELLOW}スキップしました${RESET}"
    fi
fi

# =============================================================================
# ステップ2: .vimrc の移動
# =============================================================================

section_header "ステップ2: .vimrc を dotfiles に移動"
echo ""
echo "  ホームディレクトリの .vimrc を dotfiles ディレクトリに移動します。"
echo ""

VIMRC_SRC="$HOME/.vimrc"
VIMRC_DST="$DOTFILES_DIR/.vimrc"

if [ -f "$VIMRC_SRC" ]; then
    if [ -L "$VIMRC_SRC" ]; then
        link_target=$(readlink -f "$VIMRC_SRC")
        echo -e "  ${YELLOW}注意: ~/.vimrc は既にシンボリックリンクです${RESET}"
        echo -e "  リンク先: ${CYAN}${link_target}${RESET}"
    else
        echo -e "  現在の ~/.vimrc のサイズ: $(wc -c < "$VIMRC_SRC") バイト"
        echo -e "  行数: $(wc -l < "$VIMRC_SRC") 行"
        echo ""

        if confirm ".vimrc を ${DOTFILES_DIR} に移動しますか？"; then
            echo ""
            echo "  以下の操作を実行します："
            echo "    1. ~/.vimrc のバックアップを作成"
            echo "    2. ~/.vimrc を ~/dotfiles/.vimrc に移動"
            echo ""

            # バックアップ作成
            backup_name=".vimrc.backup.$(date +%Y%m%d_%H%M%S)"
            run_cmd "cp \"${VIMRC_SRC}\" \"${HOME}/${backup_name}\""
            echo -e "    ${GREEN}→ バックアップ: ~/${backup_name}${RESET}"
            echo ""

            # 移動
            run_cmd "mv \"${VIMRC_SRC}\" \"${VIMRC_DST}\""
        else
            echo -e "  ${YELLOW}スキップしました${RESET}"
        fi
    fi
else
    echo -e "  ${YELLOW}~/.vimrc が見つかりません${RESET}"
    echo ""

    if confirm "サンプルの .vimrc を作成しますか？"; then
        echo ""
        echo "  サンプルvimrcを作成します："
        echo ""

        if $DRY_RUN; then
            echo -e "    ${CYAN}[ドライラン]${RESET} 以下の内容で ${VIMRC_DST} を作成："
            echo '    " 基本設定'
            echo '    set nocompatible'
            echo '    filetype plugin indent on'
            echo '    syntax enable'
            echo '    set encoding=utf-8'
            echo '    set number'
            echo '    set expandtab'
            echo '    set tabstop=4'
            echo '    set shiftwidth=4'
        else
            cat > "$VIMRC_DST" << 'SAMPLE_VIMRC'
" =============================================================================
" .vimrc - 基本設定
" =============================================================================

" 基本
set nocompatible
filetype plugin indent on
syntax enable
set encoding=utf-8
set fileencoding=utf-8
set backspace=indent,eol,start

" インデント
set expandtab
set tabstop=4
set shiftwidth=4
set softtabstop=4
set autoindent

" 表示
set number
set cursorline
set laststatus=2
set showcmd
set showmatch

" 検索
set hlsearch
set incsearch
set ignorecase
set smartcase

" 操作性
set wildmenu
set hidden
set scrolloff=5
set belloff=all
SAMPLE_VIMRC
            echo -e "    ${GREEN}[実行]${RESET} サンプルvimrcを作成しました"
        fi
    else
        echo -e "  ${YELLOW}スキップしました${RESET}"
    fi
fi

# =============================================================================
# ステップ3: シンボリックリンクの作成
# =============================================================================

section_header "ステップ3: シンボリックリンクの作成"
echo ""
echo "  dotfiles ディレクトリの .vimrc へのシンボリックリンクを"
echo "  ホームディレクトリに作成します。"
echo ""
echo "  シンボリックリンクとは？"
echo "    ファイルへの「ショートカット」のようなものです。"
echo "    ~/dotfiles/.vimrc を実体として、~/.vimrc はリンクになります。"
echo ""
echo "    ~/.vimrc  --->  ~/dotfiles/.vimrc（実体）"
echo ""

if confirm "シンボリックリンクを作成しますか？"; then
    # 既存の ~/.vimrc がある場合（シンボリックリンクでない）
    if [ -f "$VIMRC_SRC" ] && [ ! -L "$VIMRC_SRC" ]; then
        echo ""
        echo -e "  ${YELLOW}注意: ~/.vimrc が既に存在します（通常ファイル）${RESET}"
        echo -e "  先にステップ2で移動してください"
    else
        run_cmd "ln -sf \"${VIMRC_DST}\" \"${VIMRC_SRC}\""
        echo ""
        echo -e "  ${GREEN}リンクが作成されました：${RESET}"
        echo -e "    ${VIMRC_SRC} -> ${VIMRC_DST}"
    fi
else
    echo -e "  ${YELLOW}スキップしました${RESET}"
fi

# =============================================================================
# ステップ4: Git リポジトリの初期化
# =============================================================================

section_header "ステップ4: Git リポジトリの初期化"
echo ""
echo "  dotfiles ディレクトリを Git リポジトリとして初期化します。"
echo "  これにより設定ファイルの変更履歴を管理できます。"
echo ""

if [ -d "${DOTFILES_DIR}/.git" ]; then
    echo -e "  ${YELLOW}注意: 既にGitリポジトリです${RESET}"
    if ! $DRY_RUN; then
        echo -e "  最新のコミット:"
        git -C "$DOTFILES_DIR" log --oneline -3 2>/dev/null || echo "    （コミットなし）"
    fi
else
    if confirm "Git リポジトリを初期化しますか？"; then
        run_cmd "git -C \"${DOTFILES_DIR}\" init"
        echo ""

        # .gitignore の作成
        echo "  .gitignore も作成します（秘密情報を含むファイルを除外）："
        echo ""

        if $DRY_RUN; then
            echo -e "    ${CYAN}[ドライラン]${RESET} 以下の内容で ${DOTFILES_DIR}/.gitignore を作成："
            echo "    # 秘密情報を含む可能性のあるファイル"
            echo "    *.pem"
            echo "    *.key"
            echo "    .ssh/"
            echo "    # OS固有のファイル"
            echo "    .DS_Store"
            echo "    Thumbs.db"
        else
            cat > "${DOTFILES_DIR}/.gitignore" << 'GITIGNORE'
# 秘密情報を含む可能性のあるファイル
*.pem
*.key
.ssh/

# OS固有のファイル
.DS_Store
Thumbs.db

# エディタのバックアップファイル
*~
*.swp
*.swo
GITIGNORE
            echo -e "    ${GREEN}[実行]${RESET} .gitignore を作成しました"
        fi
    else
        echo -e "  ${YELLOW}スキップしました${RESET}"
    fi
fi

# =============================================================================
# ステップ5: 初回コミット
# =============================================================================

section_header "ステップ5: 初回コミット"
echo ""
echo "  現在のdotfilesの状態をGitに記録（コミット）します。"
echo ""

if confirm "初回コミットを作成しますか？"; then
    run_cmd "git -C \"${DOTFILES_DIR}\" add -A"
    run_cmd "git -C \"${DOTFILES_DIR}\" commit -m 'Initial commit: dotfiles管理を開始'"
    echo ""

    if ! $DRY_RUN && [ -d "${DOTFILES_DIR}/.git" ]; then
        echo -e "  ${GREEN}コミット完了！${RESET}"
        echo ""
        echo "  コミット履歴："
        git -C "$DOTFILES_DIR" log --oneline 2>/dev/null || true
    fi
else
    echo -e "  ${YELLOW}スキップしました${RESET}"
fi

# =============================================================================
# 完了メッセージと次のステップ
# =============================================================================

echo ""
echo -e "${BOLD}${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${BOLD}${YELLOW}  セットアップ完了${RESET}"
echo -e "${BOLD}${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""

if $DRY_RUN; then
    echo -e "  ${CYAN}${BOLD}ドライランモードのため、実際の操作は行われていません。${RESET}"
    echo ""
    echo -e "  実際にセットアップを実行するには："
    echo -e "    ${GREEN}$0 --execute${RESET}"
    echo ""
fi

echo -e "  ${BOLD}作成されたファイル構成：${RESET}"
echo ""
echo "    ~/dotfiles/"
echo "    ├── .git/           # Gitリポジトリ"
echo "    ├── .gitignore      # 除外設定"
echo "    └── .vimrc          # Vim設定（実体）"
echo ""
echo "    ~/.vimrc -> ~/dotfiles/.vimrc  （シンボリックリンク）"
echo ""
echo -e "  ${BOLD}次のステップ：${RESET}"
echo ""
echo "    1. vimrcを編集してカスタマイズ"
echo "       vim ~/dotfiles/.vimrc"
echo ""
echo "    2. 変更をコミット"
echo "       cd ~/dotfiles && git add -A && git commit -m '設定を変更'"
echo ""
echo "    3. GitHub にプッシュ（オプション）"
echo "       git remote add origin https://github.com/ユーザー名/dotfiles.git"
echo "       git push -u origin main"
echo ""
echo "    4. 別のマシンで設定を復元"
echo "       git clone https://github.com/ユーザー名/dotfiles.git ~/dotfiles"
echo "       ln -sf ~/dotfiles/.vimrc ~/.vimrc"
echo ""
echo -e "  ${CYAN}ヒント: .bashrc や .gitconfig なども同様に管理できます！${RESET}"
echo ""
