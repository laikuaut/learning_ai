# 第8章 演習：実践的な vimrc 構築

---

## 演習の目標

この演習では、以下のスキルを確認します。

- vimrc をセクションに分けて整理できる
- `has()` を使って OS やバージョンに応じた条件分岐を書ける
- vim-plug でプラグインを管理する設定を書ける
- 学んだ知識を組み合わせて完成度の高い vimrc を構築できる
- dotfiles として Git で管理する手順を理解している

---

## 基本問題

### 問題1：vimrc のセクション整理

以下の設定項目を、適切なセクションに分類して整理された vimrc を作成してください。

設定項目：
- `set number`
- `set encoding=utf-8`
- `set hlsearch`
- `set tabstop=4`
- `set nocompatible`
- `set expandtab`
- `syntax on`
- `set incsearch`
- `set shiftwidth=4`
- `set cursorline`
- `set smartcase`
- `let mapleader = " "`
- `nnoremap <Esc><Esc> :nohlsearch<CR>`

**期待される出力例：**

```vim
" ============================================================
" 基本設定
" ============================================================
" （該当する設定がここに入る）

" ============================================================
" 表示
" ============================================================
" （該当する設定がここに入る）

" （以下同様）
```

<details>
<summary>ヒント</summary>

- セクション例：基本設定、表示、インデント、検索、キーマッピング
- `nocompatible` と `encoding` は基本設定です
- `number` `cursorline` `syntax on` は表示です
- `tabstop` `expandtab` `shiftwidth` はインデントです

</details>

<details>
<summary>解答例</summary>

```vim
" ============================================================
" 基本設定
" ============================================================
set nocompatible              " Vi 互換モードを無効化
set encoding=utf-8            " 文字エンコーディング

" ============================================================
" 表示
" ============================================================
syntax on                     " シンタックスハイライト
set number                    " 行番号表示
set cursorline                " カーソル行ハイライト

" ============================================================
" インデント
" ============================================================
set tabstop=4                 " タブ幅
set shiftwidth=4              " インデント幅
set expandtab                 " タブをスペースに変換

" ============================================================
" 検索
" ============================================================
set hlsearch                  " 検索ハイライト
set incsearch                 " インクリメンタル検索
set smartcase                 " 大文字含む場合は区別

" ============================================================
" キーマッピング
" ============================================================
let mapleader = " "
" ESC 2回で検索ハイライト消去
nnoremap <Esc><Esc> :nohlsearch<CR>
```

</details>

---

### 問題2：環境判定の条件分岐

以下の要件を満たす条件分岐を vimrc に記述してください。

1. macOS の場合: クリップボードに `unnamed` を設定
2. Linux の場合: クリップボードに `unnamedplus` を設定
3. Windows の場合: シェルを `cmd.exe` に設定
4. GUI（GVim/MacVim）の場合: フォントを `Hack Nerd Font` サイズ 14 に設定
5. ripgrep がインストールされている場合: `grepprg` に設定

**期待される動作：**

```
環境に応じて適切な設定が自動的に適用される
```

<details>
<summary>ヒント</summary>

- `has('mac')` / `has('unix')` / `has('win32')` で OS を判定します
- `has('gui_running')` で GUI を判定します
- `executable('rg')` で ripgrep の存在を確認します

</details>

<details>
<summary>解答例</summary>

```vim
" OS 判定
if has('mac') || has('macunix')
  " macOS: unnamed でシステムクリップボードと連携
  set clipboard=unnamed
elseif has('win32') || has('win64')
  " Windows: シェルを cmd.exe に設定
  set clipboard=unnamed
  set shell=cmd.exe
elseif has('unix')
  " Linux: unnamedplus で X11 クリップボードと連携
  set clipboard=unnamedplus
endif

" GUI 判定
if has('gui_running')
  " GVim / MacVim の場合のフォント設定
  set guifont=Hack\ Nerd\ Font:h14
endif

" 外部ツール判定
if executable('rg')
  " ripgrep が使える場合は grepprg に設定
  set grepprg=rg\ --vimgrep\ --smart-case
  set grepformat=%f:%l:%c:%m
endif
```

</details>

---

### 問題3：vim-plug の基本設定

以下のプラグインを vim-plug で管理する設定を記述してください。

プラグイン一覧：
1. `tpope/vim-surround` - 囲み文字操作
2. `tpope/vim-commentary` - コメント切り替え
3. `airblade/vim-gitgutter` - Git 差分表示
4. `itchyny/lightline.vim` - ステータスライン
5. `fatih/vim-go` - Go 言語用（Go ファイルのみ読み込み）

また、lightline の基本的な設定も記述してください。

**期待される動作：**

```
:PlugInstall でプラグインがインストールされる
lightline によるステータスラインが表示される
```

<details>
<summary>ヒント</summary>

- `call plug#begin('~/.vim/plugged')` と `call plug#end()` で囲みます
- 遅延ロードには `{ 'for': 'ファイルタイプ' }` を使います
- lightline の設定は `g:lightline` 辞書変数で行います

</details>

<details>
<summary>解答例</summary>

```vim
" vim-plug によるプラグイン管理
call plug#begin('~/.vim/plugged')

" 囲み文字操作（cs'" で ' を " に変更など）
Plug 'tpope/vim-surround'

" gcc でコメント切り替え
Plug 'tpope/vim-commentary'

" Git の差分をサイン列に表示
Plug 'airblade/vim-gitgutter'

" 軽量なステータスライン
Plug 'itchyny/lightline.vim'

" Go 言語サポート（Go ファイルのみ遅延ロード）
Plug 'fatih/vim-go', { 'for': 'go' }

call plug#end()

" --- lightline の設定 ---
let g:lightline = {
  \ 'colorscheme': 'wombat',
  \ }
" lightline がモードを表示するので Vim 標準のモード表示は非表示にする
set laststatus=2
set noshowmode
```

</details>

---

## 応用問題

### 問題4：完成版 vimrc の構築

これまで学んだ知識を総動員して、以下の要件を全て満たす vimrc を作成してください。

要件：
1. 基本設定（`nocompatible`、`encoding`）
2. 表示（行番号ハイブリッド、`cursorline`、カラースキーム `desert`）
3. インデント（スペース4個、`expandtab`）
4. 検索（`hlsearch`、`incsearch`、`smartcase`）
5. キーマッピング（Leader はスペース、`jj` で Esc、`Esc Esc` で nohlsearch、ウィンドウ移動）
6. OS に応じたクリップボード設定
7. ファイルタイプ別インデント（Python: 4スペース、JavaScript: 2スペース）
8. カーソル位置復元の `autocmd`（`augroup` 使用）

**期待される動作：**

```
全ての設定が正しく動作し、環境に応じた設定が適用される
```

<details>
<summary>ヒント</summary>

- セクション分けして整理しましょう
- 全ての `autocmd` は `augroup` で囲みましょう
- `setlocal` をファイルタイプ別設定で使いましょう

</details>

<details>
<summary>解答例</summary>

```vim
" ============================================================
" 基本設定
" ============================================================
set nocompatible
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=utf-8,cp932,euc-jp

" ============================================================
" 表示
" ============================================================
syntax on
filetype plugin indent on
set number
set relativenumber
set cursorline
set showcmd
set laststatus=2
set scrolloff=5
set signcolumn=yes
colorscheme desert
set background=dark

" ============================================================
" インデント
" ============================================================
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set autoindent

" ============================================================
" 検索
" ============================================================
set hlsearch
set incsearch
set ignorecase
set smartcase

" ============================================================
" 操作
" ============================================================
set hidden
set mouse=a
set wildmenu
set backspace=indent,eol,start
set belloff=all

" ============================================================
" 環境別設定
" ============================================================
" OS に応じたクリップボード設定
if has('mac') || has('macunix')
  set clipboard=unnamed
elseif has('unix')
  set clipboard=unnamedplus
endif

" ============================================================
" キーマッピング
" ============================================================
let mapleader = " "

" jj で挿入モードを抜ける
inoremap jj <Esc>

" ESC 2回で検索ハイライト消去
nnoremap <Esc><Esc> :nohlsearch<CR>

" ウィンドウ移動
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Y を行末までヤンク
nnoremap Y y$

" Leader マッピング
nnoremap <Leader>w :w<CR>
nnoremap <Leader>q :q<CR>

" ============================================================
" autocmd
" ============================================================
" カーソル位置の復元
augroup RestoreCursor
  autocmd!
  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit'
    \ |   execute "normal! g`\""
    \ | endif
augroup END

" ファイルタイプ別インデント設定
augroup FileTypeIndent
  autocmd!
  " Python: 4スペース
  autocmd FileType python setlocal tabstop=4 shiftwidth=4 softtabstop=4 expandtab
  " JavaScript: 2スペース
  autocmd FileType javascript setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab
augroup END
```

</details>

---

### 問題5：dotfiles 管理の手順

vimrc を Git で dotfiles 管理するための手順を、実行するコマンドとともに記述してください。

要件：
1. `~/dotfiles` ディレクトリを作成
2. `~/.vimrc` を `~/dotfiles/vimrc` に移動
3. シンボリックリンクを作成
4. Git リポジトリとして初期化
5. `.gitignore` を作成（プラグインディレクトリとスワップファイルを除外）
6. 初回コミットを行う

**期待される出力例：**

```bash
# 各ステップのコマンドを記述
mkdir ~/dotfiles
# ...
```

<details>
<summary>ヒント</summary>

- `mv` でファイルを移動します
- `ln -s` でシンボリックリンクを作成します
- `.gitignore` に除外パターンを記述します

</details>

<details>
<summary>解答例</summary>

```bash
# 1. dotfiles ディレクトリを作成
mkdir ~/dotfiles

# 2. vimrc を移動
mv ~/.vimrc ~/dotfiles/vimrc

# 3. シンボリックリンクを作成
# -s: シンボリックリンク、-f: 既存ファイルを上書き
ln -sf ~/dotfiles/vimrc ~/.vimrc

# 4. Git リポジトリとして初期化
cd ~/dotfiles
git init

# 5. .gitignore を作成
cat > .gitignore << 'EOF'
# Vim プラグイン（vim-plug でインストールされるもの）
plugged/

# スワップファイル・バックアップファイル
*.swp
*.swo
*~
*.bak

# undo ファイル
undo/
EOF

# 6. 初回コミット
git add vimrc .gitignore
git commit -m "Initial dotfiles setup"
```

</details>

---

## チャレンジ問題

### 問題6：自己完結型 vimrc

以下の要件を全て満たす「自己完結型」の vimrc を作成してください。

要件：
1. vim-plug が未インストールの場合、自動でダウンロード・インストールする
2. プラグインが未インストールの場合、初回起動時に自動で `:PlugInstall` を実行する
3. プラグイン（最低3つ）を含む
4. 全ての設定を含む完全な vimrc（この1ファイルだけで環境が構築される）
5. Vim でも Neovim でも動作する

**期待される動作：**

```
新しい環境で ~/.vimrc にコピーするだけで、
Vim 起動時に自動でプラグインがインストールされ、
全ての設定が適用される
```

<details>
<summary>ヒント</summary>

- `empty(glob('~/.vim/autoload/plug.vim'))` で vim-plug の存在を確認できます
- `silent !curl ...` でダウンロードを実行できます
- `autocmd VimEnter` で起動時に `:PlugInstall` を実行できます
- Neovim 用のパスは `stdpath('data')` で取得できます

</details>

<details>
<summary>解答例</summary>

```vim
" ============================================================
"  自己完結型 vimrc
"  このファイルをコピーするだけで環境が構築されます
" ============================================================

" --- 基本設定 ---
set nocompatible
set encoding=utf-8
set fileencoding=utf-8

" --- vim-plug の自動インストール ---
" Neovim と Vim でパスが異なるので分岐
if has('nvim')
  let s:plug_path = stdpath('data') . '/site/autoload/plug.vim'
  let s:plugged_path = stdpath('data') . '/plugged'
else
  let s:plug_path = expand('~/.vim/autoload/plug.vim')
  let s:plugged_path = expand('~/.vim/plugged')
endif

" vim-plug が存在しない場合はダウンロード
if empty(glob(s:plug_path))
  " curl で vim-plug をダウンロード
  execute 'silent !curl -fLo ' . s:plug_path . ' --create-dirs '
    \ . 'https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  " 初回起動時にプラグインを自動インストール
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

" --- プラグイン ---
call plug#begin(s:plugged_path)

Plug 'tpope/vim-surround'           " 囲み文字操作
Plug 'tpope/vim-commentary'         " コメント切り替え
Plug 'itchyny/lightline.vim'        " ステータスライン

call plug#end()

" --- 表示 ---
syntax on
filetype plugin indent on
set number
set relativenumber
set cursorline
set laststatus=2
set noshowmode
set scrolloff=5
colorscheme desert
set background=dark

if has('termguicolors')
  set termguicolors
endif

" --- lightline ---
let g:lightline = { 'colorscheme': 'wombat' }

" --- インデント ---
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set autoindent

" --- 検索 ---
set hlsearch
set incsearch
set ignorecase
set smartcase

" --- 操作 ---
set hidden
set mouse=a
set wildmenu
set backspace=indent,eol,start
set belloff=all

" クリップボード
if has('mac')
  set clipboard=unnamed
elseif has('unix')
  set clipboard=unnamedplus
endif

" --- キーマッピング ---
let mapleader = " "
inoremap jj <Esc>
nnoremap <Esc><Esc> :nohlsearch<CR>
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l
nnoremap Y y$
nnoremap <Leader>w :w<CR>
nnoremap <Leader>q :q<CR>

" Neovim 固有
if has('nvim')
  set inccommand=split
  tnoremap <Esc> <C-\><C-n>
endif

" --- autocmd ---
augroup MyAutoCmd
  autocmd!
  " カーソル位置の復元
  autocmd BufReadPost *
    \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit'
    \ |   execute "normal! g`\""
    \ | endif
augroup END
```

</details>
