# 実践課題12：チーム共有vimrc設計 ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第8章（全章の知識を総合的に活用）
> **課題の種類**: 設計課題（総合設計）
> **学習目標**: チームで共有可能なvimrcのフレームワークを設計する。ポータビリティ・個人カスタマイズの余地・ドキュメント性を考慮した実務レベルの設計力を養う

---

## 完成イメージ

```
プロジェクトリポジトリ:
┌─────────────────────────────────────────────┐
│  .vim/                                      │
│  ├── vimrc.shared        ← チーム共通設定   │
│  ├── vimrc.local.sample  ← 個人設定の雛形   │
│  └── ftplugin/           ← 言語別設定       │
│      ├── python.vim                         │
│      ├── javascript.vim                     │
│      └── html.vim                           │
│                                             │
│  各メンバーの ~/.vimrc:                      │
│  ┌──────────────────────────────────┐       │
│  │ " 共通設定を読み込み             │       │
│  │ source ~/project/.vim/vimrc.shared│      │
│  │                                   │       │
│  │ " 個人設定                        │       │
│  │ colorscheme slate                 │       │
│  │ set relativenumber                │       │
│  └──────────────────────────────────┘       │
└─────────────────────────────────────────────┘
```

---

## 課題の要件

### 設計要件

1. **チーム共通設定ファイル**（`vimrc.shared`）
   - プロジェクトのコーディング規約に合ったインデント・フォーマット設定
   - チーム全員が使う共通のキーマッピング
   - ファイルタイプ別設定
   - 環境に依存しない安全な設定（`if has()`, `if executable()` で条件分岐）

2. **個人設定の分離**（`vimrc.local` の仕組み）
   - 共通設定の後に個人設定を読み込む仕組み
   - 個人設定で共通設定の一部を上書きできる
   - `.gitignore` に `vimrc.local` を登録（個人設定はバージョン管理しない）

3. **言語別設定の分離**（`ftplugin/` ディレクトリ）
   - 言語ごとに独立したファイルにする
   - 共通のパターンを関数化

4. **ドキュメント性**
   - 各設定の意図をコメントで説明
   - 新メンバーが読んで理解できるREADME的なヘッダー
   - サンプルの `vimrc.local` を提供

5. **安全性とポータビリティ**
   - OS差異の吸収（Linux/macOS/Windows）
   - Vimバージョン差異の吸収
   - 外部ツール（ripgrep等）のオプショナル対応

---

## ステップガイド

<details>
<summary>ステップ1：ディレクトリ構造の設計</summary>

```
.vim/
├── vimrc.shared           # チーム共通設定（メインファイル）
├── vimrc.local.sample     # 個人設定のサンプル
├── ftplugin/              # 言語別設定
│   ├── python.vim
│   ├── javascript.vim
│   ├── typescript.vim
│   ├── html.vim
│   ├── css.vim
│   ├── make.vim
│   └── markdown.vim
└── autoload/              # ユーティリティ関数
    └── shared.vim
```

この構造のメリット:
- `vimrc.shared` を `source` するだけでチーム設定が適用される
- `ftplugin/` は Vim が自動で読み込む仕組みを利用できる
- `autoload/` は関数が呼ばれたときだけ読み込まれるので効率的

</details>

<details>
<summary>ステップ2：共通設定ファイル（vimrc.shared）の作成</summary>

```vim
" ===========================================
" チーム共通vimrc
" ===========================================
"
" 使い方:
"   ~/.vimrc に以下を追加してください:
"     source /path/to/project/.vim/vimrc.shared
"
" 個人カスタマイズ:
"   vimrc.local.sample を参考に .vim/vimrc.local を作成してください。
"   vimrc.local は .gitignore に含まれており、リポジトリには反映されません。
"
" ===========================================

" --- 多重読み込み防止 ---
if exists('g:loaded_shared_vimrc')
    finish
endif
let g:loaded_shared_vimrc = 1

" --- このファイルのディレクトリを取得 ---
let s:vimrc_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

" ==================== 基本設定 ====================
set nocompatible
set encoding=utf-8
scriptencoding utf-8
set fileencodings=utf-8,cp932,euc-jp
set hidden autoread
set backspace=indent,eol,start
set belloff=all
set confirm
set history=500

" バックアップ・スワップ
set nobackup noswapfile
if has('persistent_undo')
    set undofile
    let &undodir = s:vimrc_dir . '/undo'
    if !isdirectory(&undodir)
        call mkdir(&undodir, 'p')
    endif
endif

" ==================== 表示設定 ====================
set number
set cursorline
set laststatus=2
set ruler showcmd
set scrolloff=5
set showmatch matchtime=1
set display=lastline

" 日本語環境の対応
if has('multi_byte')
    set ambiwidth=double
endif

syntax enable
set background=dark

" desertが使えれば適用（他の環境でエラーにならないように）
try
    colorscheme desert
catch
endtry

" ==================== プロジェクト規約：インデント ====================
" プロジェクトの規約: デフォルト4スペース
set tabstop=4 shiftwidth=4 softtabstop=4
set expandtab
set autoindent smartindent shiftround
filetype plugin indent on

" ==================== 不可視文字の表示 ====================
set list
if has('multi_byte')
    set listchars=tab:▸\ ,trail:·,extends:»,precedes:«
else
    set listchars=tab:>\ ,trail:.,extends:>,precedes:<
endif

" ==================== 検索 ====================
set incsearch hlsearch
set ignorecase smartcase wrapscan

" ripgrepが使えれば高速検索に
if executable('rg')
    set grepprg=rg\ --vimgrep\ --smart-case
    set grepformat=%f:%l:%c:%m
endif

" ==================== キーマッピング ====================
" チーム共通のLeaderキー
let mapleader = "\<Space>"

" --- チーム標準マッピング ---
" ファイル保存
nnoremap <Leader>w :write<CR>

" 検索ハイライト解除
nnoremap <Esc><Esc> :nohlsearch<CR>

" 表示行移動
nnoremap <expr> j v:count == 0 ? 'gj' : 'j'
nnoremap <expr> k v:count == 0 ? 'gk' : 'k'

" ウィンドウ間移動
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" ビジュアルモードのインデント
vnoremap < <gv
vnoremap > >gv

" ==================== 自動処理 ====================

" 行末空白の安全な削除
function! shared#TrimWhitespace() abort
    if &filetype ==# 'markdown' || &filetype ==# 'diff'
        return
    endif
    let l:save = winsaveview()
    keeppatterns %s/\s\+$//e
    call winrestview(l:save)
endfunction

augroup shared_autocmd
    autocmd!

    " 保存時に行末空白を削除
    autocmd BufWritePre * call shared#TrimWhitespace()

    " 前回の編集位置を復元
    autocmd BufReadPost *
        \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit' |
        \     exe "normal! g`\"" | endif
augroup END

" ==================== ftpluginの読み込み ====================
" このプロジェクト独自のftpluginディレクトリを追加
let &runtimepath = s:vimrc_dir . ',' . &runtimepath

" ==================== 個人設定の読み込み ====================
" vimrc.local が存在すれば読み込む
let s:local_vimrc = s:vimrc_dir . '/vimrc.local'
if filereadable(s:local_vimrc)
    execute 'source' s:local_vimrc
endif
```

</details>

<details>
<summary>ステップ3：言語別設定（ftplugin/）の作成</summary>

### ftplugin/python.vim

```vim
" Python用設定（プロジェクト規約）
" PEP 8 準拠: 4スペース、80文字制限

if exists('b:did_ftplugin_shared')
    finish
endif
let b:did_ftplugin_shared = 1

setlocal tabstop=4 shiftwidth=4 softtabstop=4 expandtab
setlocal colorcolumn=80
setlocal textwidth=79
setlocal formatoptions+=r

" 実行マッピング（バッファローカル）
nnoremap <buffer> <F5> :write<CR>:!python3 %<CR>
nnoremap <buffer> <LocalLeader>r :write<CR>:!python3 %<CR>
nnoremap <buffer> <LocalLeader>t :write<CR>:!python3 -m pytest -v<CR>
```

### ftplugin/javascript.vim

```vim
" JavaScript用設定（プロジェクト規約）
" 2スペースインデント

if exists('b:did_ftplugin_shared')
    finish
endif
let b:did_ftplugin_shared = 1

setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab
setlocal colorcolumn=100

nnoremap <buffer> <F5> :write<CR>:!node %<CR>
nnoremap <buffer> <LocalLeader>t :write<CR>:!npm test<CR>
```

### ftplugin/html.vim

```vim
" HTML用設定
" 2スペースインデント

if exists('b:did_ftplugin_shared')
    finish
endif
let b:did_ftplugin_shared = 1

setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab
```

### ftplugin/make.vim

```vim
" Makefile用設定
" タブ文字必須

if exists('b:did_ftplugin_shared')
    finish
endif
let b:did_ftplugin_shared = 1

setlocal noexpandtab tabstop=8 shiftwidth=8
```

### ftplugin/markdown.vim

```vim
" Markdown用設定

if exists('b:did_ftplugin_shared')
    finish
endif
let b:did_ftplugin_shared = 1

setlocal tabstop=2 shiftwidth=2 softtabstop=2 expandtab
setlocal wrap linebreak
setlocal spell spelllang=en,cjk
setlocal conceallevel=0
```

</details>

<details>
<summary>ステップ4：個人設定のサンプル（vimrc.local.sample）</summary>

```vim
" ===========================================
" 個人設定サンプル（vimrc.local.sample）
" ===========================================
"
" このファイルを .vim/vimrc.local にコピーして
" 個人の好みに合わせてカスタマイズしてください。
"
" vimrc.local は .gitignore に含まれているので
" リポジトリには反映されません。
"
" ===========================================

" --- カラースキーム ---
" 好みに合わせて変更してください
" colorscheme slate
" colorscheme elflord

" --- 相対行番号 ---
" 好みに応じて有効化
" set relativenumber

" --- フォントサイズ（GUI Vim使用時）---
" if has('gui_running')
"     set guifont=Consolas:h12
" endif

" --- 追加のキーマッピング ---
" inoremap jj <Esc>
" nnoremap <Leader>q :confirm quit<CR>

" --- マウスの無効化 ---
" マウスを使いたくない場合
" set mouse=

" --- 個人的な追加autocmd ---
" augroup local_autocmd
"     autocmd!
"     " ここに個人的なautocmdを追加
" augroup END
```

</details>

<details>
<summary>ステップ5：安全性とポータビリティの強化</summary>

以下のパターンを `vimrc.shared` に組み込みます。

```vim
" --- OS判定 ---
let s:is_windows = has('win32') || has('win64')
let s:is_mac = has('mac') || has('macunix')
let s:is_linux = has('unix') && !has('macunix')

" --- OS別のパス区切り ---
let s:sep = s:is_windows ? '\' : '/'

" --- クリップボード設定（OS別）---
if has('clipboard')
    if s:is_mac
        set clipboard=unnamed           " macOS: pbcopy連携
    else
        set clipboard=unnamedplus       " Linux: xclip連携
    endif
endif

" --- Vimバージョン分岐 ---
" TextYankPost はVim 8.0.1394+ で使用可能
if exists('##TextYankPost')
    augroup shared_yank_highlight
        autocmd!
        autocmd TextYankPost * silent! lua vim.highlight.on_yank({timeout=200})
    augroup END
endif

" --- 外部ツールの条件付き設定 ---
" ripgrep
if executable('rg')
    set grepprg=rg\ --vimgrep\ --smart-case
    set grepformat=%f:%l:%c:%m
endif

" --- ターミナル機能（Vim 8.1+ のみ）---
if has('terminal')
    nnoremap <Leader>tt :terminal<CR>
    tnoremap <Esc><Esc> <C-\><C-n>

    augroup shared_terminal
        autocmd!
        autocmd TerminalOpen * setlocal nonumber norelativenumber
    augroup END
endif
```

</details>

---

## 解答例

<details>
<summary>解答例（完成版：全ファイル）</summary>

### .vim/vimrc.shared（完成版）

```vim
" ===========================================
" チーム共通vimrc - 完成版
" ===========================================
" 使い方: ~/.vimrc に source /path/to/.vim/vimrc.shared を追加
" 個人設定: vimrc.local.sample を参考に vimrc.local を作成
" ===========================================

if exists('g:loaded_shared_vimrc')
    finish
endif
let g:loaded_shared_vimrc = 1

let s:vimrc_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
let s:is_windows = has('win32') || has('win64')

" {{{ 基本設定
set nocompatible encoding=utf-8
scriptencoding utf-8
set fileencodings=utf-8,cp932,euc-jp
set fileformats=unix,dos,mac
set hidden autoread confirm
set backspace=indent,eol,start
set belloff=all
set history=500
set nobackup noswapfile
if has('persistent_undo')
    set undofile
    let &undodir = s:vimrc_dir . '/undo'
    if !isdirectory(&undodir) | call mkdir(&undodir, 'p') | endif
endif
" }}}

" {{{ 表示設定
set number cursorline
set laststatus=2 ruler showcmd
set scrolloff=5 showmatch matchtime=1
set display=lastline
if has('multi_byte') | set ambiwidth=double | endif
syntax enable
set background=dark
try | colorscheme desert | catch | endtry
set list
if has('multi_byte')
    set listchars=tab:▸\ ,trail:·,extends:»,precedes:«
else
    set listchars=tab:>\ ,trail:.,extends:>,precedes:<
endif
" }}}

" {{{ インデント（プロジェクト規約: 4スペース）
set tabstop=4 shiftwidth=4 softtabstop=4
set expandtab autoindent smartindent shiftround
filetype plugin indent on
" }}}

" {{{ 検索
set incsearch hlsearch ignorecase smartcase wrapscan
if executable('rg')
    set grepprg=rg\ --vimgrep\ --smart-case
    set grepformat=%f:%l:%c:%m
endif
" }}}

" {{{ クリップボード
if has('clipboard')
    if has('mac') || has('macunix')
        set clipboard=unnamed
    else
        set clipboard=unnamedplus
    endif
endif
" }}}

" {{{ キーマッピング
let mapleader = "\<Space>"
let maplocalleader = ","

nnoremap <Leader>w :write<CR>
nnoremap <Esc><Esc> :nohlsearch<CR>
nnoremap <expr> j v:count == 0 ? 'gj' : 'j'
nnoremap <expr> k v:count == 0 ? 'gk' : 'k'
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l
vnoremap < <gv
vnoremap > >gv

if has('terminal')
    nnoremap <Leader>tt :terminal<CR>
    tnoremap <Esc><Esc> <C-\><C-n>
endif
" }}}

" {{{ 自動処理
function! shared#TrimWhitespace() abort
    if &ft ==# 'markdown' || &ft ==# 'diff' | return | endif
    let l:save = winsaveview()
    keeppatterns %s/\s\+$//e
    call winrestview(l:save)
endfunction

augroup shared_autocmd
    autocmd!
    autocmd BufWritePre * call shared#TrimWhitespace()
    autocmd BufReadPost *
        \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit' |
        \     exe "normal! g`\"" | endif
    if has('terminal')
        autocmd TerminalOpen * setlocal nonumber norelativenumber
    endif
augroup END
" }}}

" {{{ runtimepath と個人設定
let &runtimepath = s:vimrc_dir . ',' . &runtimepath
let s:local_vimrc = s:vimrc_dir . '/vimrc.local'
if filereadable(s:local_vimrc)
    execute 'source' s:local_vimrc
endif
" }}}
```

</details>

---

## 設計判断のポイント

この課題で考慮すべき設計判断をまとめます。

### 何を共通設定にし、何を個人設定にするか

| 共通設定に含めるべき | 個人設定に委ねるべき |
|------|------|
| プロジェクトのコーディング規約（インデント幅など） | カラースキーム |
| チーム標準のキーマッピング（`<Leader>w` 等） | `relativenumber` の有無 |
| ファイルタイプ別の設定 | 挿入モードの `jj` → Esc |
| 行末空白の自動削除 | マウスの有効/無効 |
| 検索のデフォルト設定 | フォントや GUI 設定 |

### 設計の原則

1. **最小限の共通設定**: 全員に必要なものだけ共通化。好みの問題は個人設定に
2. **上書き可能**: `vimrc.local` で共通設定の値を変更できる構造に
3. **安全第一**: 環境依存の機能は `if has()` / `if executable()` で保護
4. **多重読み込み防止**: `g:loaded_shared_vimrc` で二重実行を防止
5. **ドキュメント**: 新メンバーがファイルを読むだけでセットアップできること

---

## 評価チェックリスト

### 構造面
- [ ] 共通設定・個人設定・言語別設定が分離されている
- [ ] `vimrc.local` の読み込み機構がある
- [ ] `ftplugin/` で言語別設定が独立ファイルになっている
- [ ] 多重読み込み防止（`g:loaded_*`）がある

### ポータビリティ
- [ ] OS差異を `has()` で吸収している
- [ ] Vimバージョン差異を条件分岐で吸収している
- [ ] 外部ツールは `executable()` でチェックしている
- [ ] マルチバイト文字の有無を考慮している

### ドキュメント性
- [ ] ファイルの冒頭に使い方が書かれている
- [ ] 各セクションにコメントがある
- [ ] `vimrc.local.sample` が提供されている
- [ ] 設定の意図（なぜそうするか）がコメントで説明されている

### コード品質
- [ ] すべてのマッピングが `noremap` 系
- [ ] すべての `autocmd` が `augroup` で管理されている
- [ ] `ftplugin` 内で `setlocal` を使用している
- [ ] `ftplugin` に多重読み込み防止がある
