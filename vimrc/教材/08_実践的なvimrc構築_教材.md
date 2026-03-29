# 第8章：実践的な vimrc 構築

## この章のゴール

- vimrc を整理されたセクション構成で書ける
- 条件分岐で OS やバージョンの違いに対応できる
- プラグインマネージャ（vim-plug）を使える
- dotfiles として Git で vimrc を管理できる
- Neovim への移行ポイントを理解する
- 完成度の高い vimrc テンプレートを構築できる

---

## 1. vimrc の構成と整理

### セクション分けのベストプラクティス

vimrc が長くなると読みづらくなります。セクションに分けてコメントで区切ることで、管理しやすくなります。

```vim
" ============================================================
" 基本設定
" ============================================================
set nocompatible
set encoding=utf-8
set fileencoding=utf-8

" ============================================================
" 表示
" ============================================================
syntax on
set number
set relativenumber
set cursorline

" ============================================================
" インデント
" ============================================================
set tabstop=4
set shiftwidth=4
set expandtab

" ============================================================
" 検索
" ============================================================
set hlsearch
set incsearch
set smartcase

" ============================================================
" キーマッピング
" ============================================================
let mapleader = " "
nnoremap <Esc><Esc> :nohlsearch<CR>

" ============================================================
" autocmd
" ============================================================
augroup MyAutoCmd
  autocmd!
  " ...
augroup END

" ============================================================
" プラグイン
" ============================================================
" ...
```

### 推奨するセクション順

```
  vimrc の推奨構成:

  1. 基本設定（encoding, nocompatible 等）
  2. プラグイン（vim-plug 等）
  3. 表示設定（行番号, カラースキーム等）
  4. インデント設定
  5. 検索設定
  6. その他のオプション
  7. キーマッピング
  8. autocmd / ファイルタイプ別設定
  9. プラグイン固有の設定

  ※ プラグインは早い段階で読み込む必要があるため、
    基本設定の直後に配置します。
```

### ポイントまとめ

- セクションごとにコメントで区切ると管理しやすくなります
- プラグインの読み込みは vimrc の前半に配置します
- 自分が理解できる設定だけを入れるのが重要です

---

## 2. 条件分岐による環境対応

### OS の判定

```vim
" OS を判定する
if has('mac') || has('macunix')
  " macOS 固有の設定
  set clipboard=unnamed
elseif has('win32') || has('win64')
  " Windows 固有の設定
  set clipboard=unnamed
  set shell=cmd.exe
elseif has('unix')
  " Linux 固有の設定
  set clipboard=unnamedplus
endif
```

### GUI の判定

```vim
" GVim / MacVim かどうかを判定
if has('gui_running')
  set guifont=Hack\ Nerd\ Font:h14
  set guioptions-=T         " ツールバーを非表示
  set guioptions-=m         " メニューバーを非表示
  set guioptions-=r         " 右スクロールバーを非表示
  set guioptions-=L         " 左スクロールバーを非表示
endif
```

### 機能の判定

```vim
" クリップボード機能があるか
if has('clipboard')
  set clipboard=unnamedplus
endif

" ターミナル機能があるか（Vim 8.1+）
if has('terminal')
  " ターミナル関連の設定
endif

" True Color に対応しているか
if has('termguicolors')
  set termguicolors
endif

" Vim のバージョン判定
if v:version >= 800
  " Vim 8.0 以降の設定
endif

" Neovim かどうか
if has('nvim')
  " Neovim 固有の設定
  set inccommand=split
endif
```

### executable() による外部コマンド判定

```vim
" ripgrep がインストールされているか
if executable('rg')
  set grepprg=rg\ --vimgrep\ --smart-case
  set grepformat=%f:%l:%c:%m
endif

" Python3 が利用可能か
if has('python3')
  " Python3 連携の設定
endif
```

### ポイントまとめ

- `has()` で OS、GUI、機能の有無を判定できます
- `executable()` で外部コマンドの存在を確認できます
- 条件分岐で環境に応じた設定を切り替えましょう

---

## 3. プラグインマネージャ入門

### vim-plug の基本

vim-plug は最も人気のあるプラグインマネージャの1つです。シンプルで高速な点が特徴です。

### vim-plug のインストール

```bash
# Unix / Linux / macOS
$ curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

# Neovim の場合
$ curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim \
    --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

### vimrc でのプラグイン宣言

```vim
" プラグインの開始（インストール先ディレクトリを指定）
call plug#begin('~/.vim/plugged')

" プラグインの宣言
Plug 'tpope/vim-sensible'           " 基本的なデフォルト設定
Plug 'tpope/vim-fugitive'           " Git 連携
Plug 'tpope/vim-surround'           " 囲み文字の操作
Plug 'tpope/vim-commentary'         " コメントの切り替え
Plug 'airblade/vim-gitgutter'       " Git の差分表示
Plug 'itchyny/lightline.vim'        " ステータスライン

" プラグインの終了
call plug#end()
```

### プラグインのインストールと管理

```vim
" Vim 内でコマンドを実行
:PlugInstall          " 宣言したプラグインをインストール
:PlugUpdate           " プラグインを更新
:PlugClean            " 不要なプラグインを削除
:PlugStatus           " プラグインの状態を表示
:PlugUpgrade          " vim-plug 自体を更新
```

```
  :PlugInstall の実行画面:

  ┌─ vim-plug ─────────────────────────────────┐
  │ Updated!  vim-sensible                     │
  │ Updated!  vim-fugitive                     │
  │ Updated!  vim-surround                     │
  │ Updated!  vim-commentary                   │
  │ Updated!  vim-gitgutter                    │
  │ Updated!  lightline.vim                    │
  │                                            │
  │ Finishing ... Done!                        │
  └────────────────────────────────────────────┘
```

### 条件付きプラグイン

```vim
call plug#begin('~/.vim/plugged')

" 特定の条件でのみ読み込むプラグイン
Plug 'neoclide/coc.nvim', {'branch': 'release'}  " 特定のブランチ

" 特定のファイルタイプでのみ読み込み
Plug 'fatih/vim-go', { 'for': 'go' }
Plug 'rust-lang/rust.vim', { 'for': 'rust' }

" コマンド実行時にのみ読み込み（遅延ロード）
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'

call plug#end()
```

### 他のプラグインマネージャ

```
  ┌──────────────────┬──────────────────────────────────┐
  │ マネージャ       │ 特徴                             │
  ├──────────────────┼──────────────────────────────────┤
  │ vim-plug         │ シンプル、高速、最も人気          │
  │ dein.vim         │ 日本人開発、遅延ロードが強力     │
  │ Vundle           │ 古参、シンプルだが開発停止気味   │
  │ packer.nvim      │ Neovim 用、Lua で設定            │
  │ lazy.nvim        │ Neovim 用、最新で高速            │
  └──────────────────┴──────────────────────────────────┘
```

### ポイントまとめ

- vim-plug が最もシンプルで推奨されるプラグインマネージャです
- `call plug#begin()` と `call plug#end()` の間にプラグインを宣言します
- `:PlugInstall` でインストール、`:PlugUpdate` で更新します

---

## 4. よく使われるプラグイン紹介

### ファイラ（ファイルエクスプローラ）

```vim
" NERDTree: 最も有名なファイルツリー
Plug 'preservim/nerdtree'

" NERDTree の設定例
nnoremap <Leader>e :NERDTreeToggle<CR>
let NERDTreeShowHidden=1            " 隠しファイルを表示
```

```vim
" fern.vim: 軽量で高速なファイラ
Plug 'lambdalisue/fern.vim'

" fern の設定例
nnoremap <Leader>e :Fern . -drawer -toggle<CR>
```

### ファジーファインダ

```vim
" fzf.vim: 高速なあいまい検索
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'

" fzf の設定例
nnoremap <Leader>f :Files<CR>       " ファイル検索
nnoremap <Leader>g :Rg<CR>          " テキスト検索
nnoremap <Leader>b :Buffers<CR>     " バッファ検索
```

### 補完

```vim
" coc.nvim: Language Server Protocol (LSP) クライアント
Plug 'neoclide/coc.nvim', {'branch': 'release'}
```

### ステータスライン

```vim
" lightline.vim: 軽量なステータスライン
Plug 'itchyny/lightline.vim'

" lightline の設定例
let g:lightline = {
  \ 'colorscheme': 'wombat',
  \ }
set laststatus=2
set noshowmode                      " モード表示はlightlineに任せる
```

### Git 連携

```vim
" vim-fugitive: Vim 内で Git 操作
Plug 'tpope/vim-fugitive'

" vim-gitgutter: 差分をサイン列に表示
Plug 'airblade/vim-gitgutter'
```

### その他の定番プラグイン

```vim
Plug 'tpope/vim-surround'           " 囲み文字の操作（cs'" で ' → " に変更）
Plug 'tpope/vim-commentary'         " gcc でコメント切り替え
Plug 'tpope/vim-repeat'             " . でプラグインの操作も繰り返し
Plug 'jiangmiao/auto-pairs'         " 括弧の自動補完
Plug 'machakann/vim-highlightedyank' " ヤンク範囲をハイライト表示
```

### ポイントまとめ

- まずは必要最小限のプラグインから始めましょう
- プラグインを入れすぎると起動が遅くなります
- 各プラグインの README を読んで設定を理解しましょう

---

## 5. dotfiles 管理

### Git で vimrc を管理する

vimrc を Git で管理すると、バックアップや環境移行が容易になります。

```bash
# dotfiles ディレクトリを作成
$ mkdir ~/dotfiles
$ cd ~/dotfiles

# vimrc を移動
$ mv ~/.vimrc ~/dotfiles/vimrc

# シンボリックリンクを作成
$ ln -s ~/dotfiles/vimrc ~/.vimrc

# Git リポジトリとして初期化
$ git init
$ git add vimrc
$ git commit -m "Initial vimrc"
```

### ディレクトリ構造の例

```
  ~/dotfiles/
  ├── vimrc                  ← メインの設定ファイル
  ├── vim/
  │   ├── ftplugin/
  │   │   ├── python.vim
  │   │   ├── javascript.vim
  │   │   └── go.vim
  │   └── after/
  │       └── plugin/
  ├── bashrc
  ├── tmux.conf
  ├── gitconfig
  ├── install.sh             ← セットアップスクリプト
  └── README.md
```

### セットアップスクリプトの例

```bash
#!/bin/bash
# install.sh - dotfiles のセットアップ

DOTFILES_DIR="$HOME/dotfiles"

# シンボリックリンクを作成
ln -sf "$DOTFILES_DIR/vimrc" "$HOME/.vimrc"
ln -sf "$DOTFILES_DIR/vim" "$HOME/.vim"

# vim-plug のインストール
if [ ! -f "$HOME/.vim/autoload/plug.vim" ]; then
  curl -fLo "$HOME/.vim/autoload/plug.vim" --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
fi

# Vim プラグインのインストール
vim +PlugInstall +qall

echo "dotfiles のセットアップが完了しました"
```

### ~/.vim/vimrc を使う方法

Vim 8.0 以降では、`~/.vim/vimrc` が認識されます。この方法なら `~/.vim/` ディレクトリごと Git 管理できます。

```
  ~/.vim/
  ├── vimrc               ← 設定ファイル（~/.vimrc の代わり）
  ├── autoload/
  │   └── plug.vim
  ├── plugged/             ← プラグイン（.gitignore で除外）
  ├── ftplugin/
  │   ├── python.vim
  │   └── javascript.vim
  └── .gitignore
```

```bash
# .gitignore の例
plugged/
*.swp
*.swo
*~
```

### ポイントまとめ

- dotfiles を Git で管理すると環境移行が楽になります
- シンボリックリンクで元の場所から参照させます
- `~/.vim/vimrc`（Vim 8.0+）ならディレクトリごと管理できます

---

## 6. Neovim への移行

### Neovim とは

Neovim は Vim のフォーク（fork）で、よりモダンな機能と Lua スクリプティングをサポートしています。

### 設定ファイルの違い

```
  ┌──────────────┬────────────────────────────────┐
  │ Vim          │ Neovim                         │
  ├──────────────┼────────────────────────────────┤
  │ ~/.vimrc     │ ~/.config/nvim/init.vim         │
  │              │ ~/.config/nvim/init.lua（Lua）  │
  │ ~/.vim/      │ ~/.config/nvim/                 │
  └──────────────┴────────────────────────────────┘
```

### Vim の vimrc を Neovim でも使う

```vim
" ~/.config/nvim/init.vim に以下を記述すると ~/.vimrc を読み込める
set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
source ~/.vimrc
```

### Neovim 固有の設定

```vim
if has('nvim')
  " 置換のリアルタイムプレビュー
  set inccommand=split

  " ターミナルモードからの脱出
  tnoremap <Esc> <C-\><C-n>

  " True Color（Neovim ではデフォルトでサポート）
  set termguicolors
endif
```

### init.lua（Lua での設定）

Neovim では Lua で設定を書くこともできます。

```lua
-- ~/.config/nvim/init.lua の例

-- 基本設定
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true
vim.opt.hlsearch = true
vim.opt.incsearch = true
vim.opt.smartcase = true
vim.opt.ignorecase = true

-- キーマッピング
vim.g.mapleader = " "
vim.keymap.set('n', '<Esc><Esc>', ':nohlsearch<CR>')
vim.keymap.set('i', 'jj', '<Esc>')
```

### ポイントまとめ

- Neovim の設定ファイルは `~/.config/nvim/init.vim` です
- 既存の vimrc を `source` で読み込むこともできます
- Neovim では Lua による設定（init.lua）も選択できます
- `has('nvim')` で Neovim 固有の設定を分岐させましょう

---

## 7. 完成版 vimrc テンプレート

### 初心者向けテンプレート

プラグインなしで動作する、シンプルだが実用的な vimrc です。

```vim
" ============================================================
"  初心者向け vimrc テンプレート
"  そのままコピーして ~/.vimrc に保存してください
" ============================================================

" --- 基本設定 ---
set nocompatible                " Vi 互換モードを無効化
set encoding=utf-8              " 文字エンコーディング
set fileencoding=utf-8          " ファイル保存時のエンコーディング
set fileencodings=utf-8,cp932,euc-jp  " 読み込み時の自動判定

" --- 表示 ---
syntax on                       " シンタックスハイライト
filetype plugin indent on       " ファイルタイプ検出
set number                      " 行番号表示
set cursorline                  " カーソル行ハイライト
set showcmd                     " 入力中のコマンドを表示
set showmode                    " 現在のモードを表示
set laststatus=2                " ステータスライン常時表示
set scrolloff=5                 " スクロール時の余白行数
set signcolumn=yes              " サイン列を常に表示
colorscheme desert              " カラースキーム
set background=dark             " 暗い背景

" --- インデント ---
set tabstop=4                   " タブ幅
set shiftwidth=4                " インデント幅
set softtabstop=4               " Tab キーの挿入幅
set expandtab                   " タブをスペースに変換
set autoindent                  " 自動インデント

" --- 検索 ---
set hlsearch                    " 検索ハイライト
set incsearch                   " インクリメンタル検索
set ignorecase                  " 大小文字を区別しない
set smartcase                   " 大文字含む場合は区別

" --- 操作 ---
set hidden                      " バッファを保存せずに切り替え
set clipboard=unnamedplus       " システムクリップボード連携
set mouse=a                     " マウス有効
set wildmenu                    " コマンド補完強化
set backspace=indent,eol,start  " BS の動作改善
set belloff=all                 " ビープ音無効

" --- キーマッピング ---
let mapleader = " "

" jj で挿入モードを抜ける
inoremap jj <Esc>

" ESC 2回で検索ハイライト消去
nnoremap <Esc><Esc> :nohlsearch<CR>

" ウィンドウ移動を Ctrl + h/j/k/l で
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Y を行末までヤンクに変更
nnoremap Y y$

" Leader + w で保存
nnoremap <Leader>w :w<CR>

" Leader + q で終了
nnoremap <Leader>q :q<CR>
```

### 中級者向けテンプレート

プラグイン管理と高度な設定を含む vimrc です。

```vim
" ============================================================
"  中級者向け vimrc テンプレート
" ============================================================

" --- 基本設定 ---
set nocompatible
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=utf-8,cp932,euc-jp

" --- vim-plug によるプラグイン管理 ---
" インストール: curl -fLo ~/.vim/autoload/plug.vim --create-dirs
"   https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
" 初回は :PlugInstall を実行してください

call plug#begin('~/.vim/plugged')

Plug 'tpope/vim-sensible'               " 基本設定
Plug 'tpope/vim-surround'               " 囲み文字操作
Plug 'tpope/vim-commentary'             " コメント切り替え
Plug 'tpope/vim-fugitive'               " Git 連携
Plug 'airblade/vim-gitgutter'           " Git 差分表示
Plug 'itchyny/lightline.vim'            " ステータスライン
Plug 'preservim/nerdtree'               " ファイルツリー
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'                 " ファジーファインダ
Plug 'machakann/vim-highlightedyank'    " ヤンク範囲ハイライト
Plug 'jiangmiao/auto-pairs'             " 括弧自動補完

call plug#end()

" --- 表示 ---
syntax on
filetype plugin indent on
set number
set relativenumber
set cursorline
set showcmd
set laststatus=2
set noshowmode                           " lightline があるので非表示
set scrolloff=5
set sidescrolloff=5
set signcolumn=yes
set termguicolors
colorscheme desert
set background=dark

" --- ステータスライン（lightline）---
let g:lightline = {
  \ 'colorscheme': 'wombat',
  \ 'active': {
  \   'left': [ [ 'mode', 'paste' ],
  \             [ 'gitbranch', 'readonly', 'filename', 'modified' ] ]
  \ },
  \ 'component_function': {
  \   'gitbranch': 'FugitiveHead',
  \ },
  \ }

" --- インデント ---
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set autoindent
set smartindent

" --- 検索 ---
set hlsearch
set incsearch
set ignorecase
set smartcase

" --- grep ---
if executable('rg')
  set grepprg=rg\ --vimgrep\ --smart-case
  set grepformat=%f:%l:%c:%m
endif

" --- 不可視文字 ---
set list
set listchars=tab:▸\ ,trail:·,extends:❯,precedes:❮

" --- 操作 ---
set hidden
set clipboard=unnamedplus
set mouse=a
set wildmenu
set wildmode=longest:full,full
set backspace=indent,eol,start
set belloff=all
set undofile
set undodir=~/.vim/undo

" --- キーマッピング ---
let mapleader = " "

inoremap jj <Esc>
nnoremap <Esc><Esc> :nohlsearch<CR>

" ウィンドウ移動
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Y を行末までヤンク
nnoremap Y y$

" ビジュアルモードでインデント後も選択を維持
vnoremap > >gv
vnoremap < <gv

" 行の移動
nnoremap <A-j> :m .+1<CR>==
nnoremap <A-k> :m .-2<CR>==
vnoremap <A-j> :m '>+1<CR>gv=gv
vnoremap <A-k> :m '<-2<CR>gv=gv

" 検索時に画面中央に表示
nnoremap n nzzzv
nnoremap N Nzzzv

" Leader マッピング
nnoremap <Leader>w :w<CR>
nnoremap <Leader>q :q<CR>
nnoremap <Leader>e :NERDTreeToggle<CR>
nnoremap <Leader>f :Files<CR>
nnoremap <Leader>g :Rg<CR>
nnoremap <Leader>b :Buffers<CR>

" quickfix ナビゲーション
nnoremap ]q :cnext<CR>
nnoremap [q :cprev<CR>

" --- autocmd ---
augroup MyAutoCmd
  autocmd!
  " カーソル位置を復元
  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit'
    \ |   execute "normal! g`\""
    \ | endif

  " 末尾空白を自動削除
  autocmd BufWritePre * if &ft != 'markdown' | :%s/\s\+$//e | endif

  " grep 後に quickfix を自動で開く
  autocmd QuickFixCmdPost *grep* cwindow
augroup END

" --- ファイルタイプ別設定 ---
augroup FileTypeSettings
  autocmd!
  autocmd FileType python setlocal tabstop=4 shiftwidth=4 expandtab textwidth=79
  autocmd FileType javascript,typescript setlocal tabstop=2 shiftwidth=2 expandtab
  autocmd FileType html,css setlocal tabstop=2 shiftwidth=2 expandtab
  autocmd FileType go setlocal tabstop=4 shiftwidth=4 noexpandtab
  autocmd FileType make setlocal noexpandtab
  autocmd FileType vim setlocal tabstop=2 shiftwidth=2 expandtab
augroup END

" --- undo ディレクトリの作成 ---
if !isdirectory(expand('~/.vim/undo'))
  call mkdir(expand('~/.vim/undo'), 'p')
endif
```

### ポイントまとめ

- 初心者はプラグインなしのシンプルな vimrc から始めましょう
- 慣れてきたらプラグインを少しずつ追加していきます
- 自分が理解できない設定は入れないことが大切です
- vimrc は Git で管理し、定期的に見直しましょう
