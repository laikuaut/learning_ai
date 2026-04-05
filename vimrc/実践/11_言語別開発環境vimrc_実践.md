# 実践課題11：言語別開発環境vimrc ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第8章（全章の知識を総合的に活用）
> **課題の種類**: ミニプロジェクト（総合設計）
> **学習目標**: 複数のプログラミング言語に対応した開発環境をvimrc一つで構築する。関数・autocmd・キーマッピングを組み合わせて、実務で使えるレベルの設定を自力で設計・実装する

---

## 完成イメージ

ファイルを開くだけで、言語に最適化された開発環境が自動構成されます。

```
┌──────────────────────────────────────────────────────────────┐
│  NORMAL │ main.py [+] │  master │ python │ utf-8 │ 42/150:15 │
├──────────────────────────────────────────────────────────────┤
│  1 │ import os                                               │
│  2 │ import sys                                              │
│  3 │ from pathlib import Path                                │
│  4 │                                                         │
│  5 │ def process_file(filepath: str) -> dict:                │
│  6 │ ····"""ファイルを処理して結果を返す"""                   │
│  7 │ ····result = {}                                         │
│  8 │ ····with open(filepath) as f:                           │
│  9 │ ········for line in f:                                  │
│ 10 │ ············result[line.strip()] = True                 │
│ 11 │ ····return result                                       │
│                                      ↑ 4スペースインデント   │
│ ──────────────────────────── 80列目ガイド ────────────────    │
│                                                              │
│  <F5> 実行  <Leader>r 実行  <Leader>b ビルド                 │
│  <Leader>t テスト  <Leader>l リント                          │
└──────────────────────────────────────────────────────────────┘
```

---

## 課題の要件

### 必須要件

1. **共通基盤**（全言語共通）
   - Leader キー、基本表示、検索、操作性の設定
   - カスタムステータスライン（モード・ファイル名・ファイルタイプ・位置情報）
   - 保存時の自動行末空白削除

2. **言語別設定**（最低4言語）
   - Python: 4スペース、80列ガイド、`<F5>` で実行
   - JavaScript/TypeScript: 2スペース、100列ガイド
   - HTML/CSS: 2スペース
   - Makefile: タブ文字
   - Shell script: 4スペース、`<F5>` で実行
   - (追加言語は任意)

3. **言語別キーマッピング**
   - `<Leader>r` または `<F5>` でファイルを実行（Python, Shell）
   - `<Leader>b` でビルド（コンパイル言語対応）
   - `<Leader>t` でテスト実行

4. **便利機能**
   - 前回の編集位置を復元
   - プロジェクトルートへの自動 `lcd`
   - テンプレート自動挿入（新規ファイル作成時）

5. **コード品質**
   - すべての関数に `s:` プレフィックスと `abort` を付ける
   - すべての `autocmd` を `augroup` で管理
   - すべてのマッピングは `noremap` 系
   - 適切なコメントとセクション分け

---

## ステップガイド

<details>
<summary>ステップ1：共通基盤を構築する</summary>

まず全言語共通の設定を書きます。

```vim
" ===========================================
" Language Development Environment
" ===========================================

" ==================== 基本設定 ====================
set nocompatible
set encoding=utf-8
scriptencoding utf-8
set fileencodings=utf-8,cp932,euc-jp
set fileformats=unix,dos,mac
set hidden
set autoread
set nobackup noswapfile
set undofile
set undodir=~/.vim/undo
set backspace=indent,eol,start
set belloff=all
set mouse=a
set confirm

" ==================== 表示設定 ====================
set number relativenumber
set cursorline
set laststatus=2
set noshowmode
set ruler showcmd
set scrolloff=8
set showmatch matchtime=1
set display=lastline
set ambiwidth=double

syntax enable
set background=dark
colorscheme desert

" ==================== インデント ====================
set tabstop=4 shiftwidth=4 softtabstop=4
set expandtab
set autoindent smartindent
set shiftround
filetype plugin indent on

" ==================== 検索 ====================
set incsearch hlsearch
set ignorecase smartcase
set wrapscan

" ==================== 不可視文字 ====================
set list
set listchars=tab:▸\ ,trail:·,extends:»,precedes:«
```

</details>

<details>
<summary>ステップ2：ステータスラインを構築する</summary>

```vim
" ==================== ステータスライン ====================
function! s:GetMode() abort
    let l:mode_map = {
        \ 'n': 'NORMAL', 'i': 'INSERT', 'v': 'VISUAL',
        \ 'V': 'V-LINE', "\<C-v>": 'V-BLOCK',
        \ 'R': 'REPLACE', 'c': 'COMMAND', 't': 'TERMINAL',
        \ }
    return get(l:mode_map, mode(), mode())
endfunction

set statusline=
set statusline+=\ %{s:GetMode()}
set statusline+=\ │\ %f\ %m%r
set statusline+=\ │\ %Y
set statusline+=\ │\ %{&fileencoding}
set statusline+=%=
set statusline+=\ %l/%L:%c
set statusline+=\ │\ %p%%\ 
```

</details>

<details>
<summary>ステップ3：共通キーマッピングを定義する</summary>

```vim
" ==================== キーマッピング ====================
let mapleader = "\<Space>"

" --- ファイル操作 ---
nnoremap <Leader>w :write<CR>
nnoremap <Leader>q :confirm quit<CR>

" --- 移動 ---
nnoremap <expr> j v:count == 0 ? 'gj' : 'j'
nnoremap <expr> k v:count == 0 ? 'gk' : 'k'
nnoremap H ^
nnoremap L $
nnoremap <C-d> <C-d>zz
nnoremap <C-u> <C-u>zz
nnoremap n nzzzv
nnoremap N Nzzzv

" --- 編集 ---
nnoremap <Leader>d :copy .<CR>
nnoremap Y y$
nnoremap x "_x

" --- 検索 ---
nnoremap <Esc><Esc> :nohlsearch<CR>

" --- ウィンドウ ---
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" --- 挿入モード ---
inoremap jj <Esc>
inoremap <C-a> <Home>
inoremap <C-e> <End>

" --- ビジュアルモード ---
vnoremap < <gv
vnoremap > >gv
```

</details>

<details>
<summary>ステップ4：言語別設定と実行機能を実装する</summary>

```vim
" ==================== 言語別設定 ====================

" インデント設定ヘルパー
function! s:SetIndent(width, use_tabs) abort
    let &l:tabstop = a:width
    let &l:shiftwidth = a:width
    let &l:softtabstop = a:width
    let &l:expandtab = !a:use_tabs
endfunction

" ファイル実行関数
function! s:RunFile() abort
    write
    let l:ft = &filetype
    let l:file = expand('%')

    if l:ft ==# 'python'
        execute '!python3 ' . shellescape(l:file)
    elseif l:ft ==# 'sh' || l:ft ==# 'bash'
        execute '!bash ' . shellescape(l:file)
    elseif l:ft ==# 'javascript'
        execute '!node ' . shellescape(l:file)
    elseif l:ft ==# 'typescript'
        execute '!npx ts-node ' . shellescape(l:file)
    elseif l:ft ==# 'go'
        execute '!go run ' . shellescape(l:file)
    elseif l:ft ==# 'rust'
        execute '!cargo run'
    elseif l:ft ==# 'c'
        execute '!gcc -o %:r ' . shellescape(l:file) . ' && ./%:r'
    else
        echo "実行方法が未定義: " . l:ft
    endif
endfunction

" テスト実行関数
function! s:RunTest() abort
    write
    let l:ft = &filetype

    if l:ft ==# 'python'
        execute '!python3 -m pytest -v'
    elseif l:ft ==# 'javascript' || l:ft ==# 'typescript'
        execute '!npm test'
    elseif l:ft ==# 'go'
        execute '!go test ./...'
    elseif l:ft ==# 'rust'
        execute '!cargo test'
    else
        echo "テスト方法が未定義: " . l:ft
    endif
endfunction

" 実行・テストのマッピング
nnoremap <F5> :call <SID>RunFile()<CR>
nnoremap <Leader>r :call <SID>RunFile()<CR>
nnoremap <Leader>t :call <SID>RunTest()<CR>

" --- ファイルタイプ別の詳細設定 ---
augroup vimrc_filetype
    autocmd!

    " Python
    autocmd FileType python call s:SetIndent(4, 0)
    autocmd FileType python setlocal colorcolumn=80 textwidth=79
    autocmd FileType python setlocal formatoptions+=r

    " Web系
    autocmd FileType html,css,scss,vue call s:SetIndent(2, 0)
    autocmd FileType javascript,typescript,json call s:SetIndent(2, 0)
    autocmd FileType javascript,typescript setlocal colorcolumn=100

    " Makefile
    autocmd FileType make call s:SetIndent(8, 1)

    " Shell
    autocmd FileType sh,bash,zsh call s:SetIndent(4, 0)
    autocmd FileType sh,bash,zsh setlocal colorcolumn=80

    " Go
    autocmd FileType go call s:SetIndent(4, 1)

    " Markdown
    autocmd FileType markdown call s:SetIndent(2, 0)
    autocmd FileType markdown setlocal wrap linebreak spell spelllang=en,cjk

    " Git commit
    autocmd FileType gitcommit setlocal spell spelllang=en,cjk textwidth=72

    " YAML
    autocmd FileType yaml call s:SetIndent(2, 0)
    autocmd FileType yaml setlocal cursorcolumn
augroup END
```

</details>

<details>
<summary>ステップ5：便利機能を追加する</summary>

```vim
" ==================== 自動処理 ====================

" 行末空白の安全な削除
function! s:TrimWhitespace() abort
    if &filetype ==# 'markdown'
        return
    endif
    let l:save = winsaveview()
    keeppatterns %s/\s\+$//e
    call winrestview(l:save)
endfunction

" プロジェクトルートに移動
function! s:CdProjectRoot() abort
    let l:markers = ['.git', 'Makefile', 'package.json', 'Cargo.toml',
        \ 'go.mod', 'pyproject.toml', 'setup.py']
    let l:dir = expand('%:p:h')
    while l:dir !=# '/' && l:dir !=# ''
        for l:marker in l:markers
            if isdirectory(l:dir . '/' . l:marker) ||
                \ filereadable(l:dir . '/' . l:marker)
                execute 'lcd' fnameescape(l:dir)
                return
            endif
        endfor
        let l:dir = fnamemodify(l:dir, ':h')
    endwhile
endfunction

" テンプレート挿入
function! s:InsertTemplate() abort
    let l:ft = &filetype
    if l:ft ==# 'python' && line('$') == 1 && getline(1) ==# ''
        call setline(1, ['#!/usr/bin/env python3', '"""', 'Description.',
            \ '"""', '', ''])
        call cursor(3, 1)
    elseif l:ft ==# 'sh' && line('$') == 1 && getline(1) ==# ''
        call setline(1, ['#!/bin/bash', 'set -euo pipefail', '', ''])
        call cursor(4, 1)
    endif
endfunction

augroup vimrc_autocmd
    autocmd!

    " 保存時に行末空白を削除
    autocmd BufWritePre * call s:TrimWhitespace()

    " 前回の編集位置を復元
    autocmd BufReadPost *
        \ if line("'\"") >= 1 && line("'\"") <= line("$") && &filetype !~# 'commit' |
        \     execute "normal! g`\"" |
        \ endif

    " プロジェクトルートに自動移動
    autocmd BufEnter * call s:CdProjectRoot()

    " 新規ファイルにテンプレート挿入
    autocmd BufNewFile *.py,*.sh call s:InsertTemplate()

    " undoディレクトリの自動作成
    if !isdirectory(expand('~/.vim/undo'))
        call mkdir(expand('~/.vim/undo'), 'p')
    endif
augroup END

" ==================== カスタムコマンド ====================
command! TrimWhitespace call s:TrimWhitespace()
command! CdRoot call s:CdProjectRoot()
command! CopyPath let @+ = expand('%:p')
command! CopyRelPath let @+ = expand('%')
```

</details>

---

## 解答例

<details>
<summary>解答例（完成版：全機能統合）</summary>

上記のステップ1〜5をすべて結合し、さらにモード別のステータスライン色変更を加えた完成版です。

```vim
" ===========================================
" Language Development Environment - vimrc
" ===========================================

" {{{ 1. 基本設定
set nocompatible
set encoding=utf-8
scriptencoding utf-8
set fileencodings=utf-8,cp932,euc-jp
set fileformats=unix,dos,mac
set hidden autoread
set nobackup noswapfile
set undofile undodir=~/.vim/undo
set backspace=indent,eol,start
set belloff=all
set mouse=a
set confirm
set history=500
" }}}

" {{{ 2. 表示設定
set number relativenumber
set cursorline
set laststatus=2 noshowmode
set ruler showcmd
set scrolloff=8 sidescrolloff=8
set showmatch matchtime=1
set display=lastline
set ambiwidth=double
set pumheight=10

syntax enable
set background=dark
colorscheme desert

set list
set listchars=tab:▸\ ,trail:·,extends:»,precedes:«
" }}}

" {{{ 3. インデント
set tabstop=4 shiftwidth=4 softtabstop=4
set expandtab autoindent smartindent shiftround
filetype plugin indent on
" }}}

" {{{ 4. 検索
set incsearch hlsearch
set ignorecase smartcase wrapscan
if executable('rg')
    set grepprg=rg\ --vimgrep\ --smart-case
    set grepformat=%f:%l:%c:%m
endif
" }}}

" {{{ 5. ステータスライン
function! s:GetMode() abort
    let l:m = {'n':'NORMAL','i':'INSERT','v':'VISUAL','V':'V-LINE',
        \ "\<C-v>":'V-BLOCK','R':'REPLACE','c':'COMMAND','t':'TERMINAL'}
    return get(l:m, mode(), mode())
endfunction

set statusline=\ %{<SID>GetMode()}\ │\ %f\ %m%r\ │\ %Y\ │\ %{&fenc}%=\ %l/%L:%c\ │\ %p%%\ 

augroup vimrc_statuscolor
    autocmd!
    autocmd InsertEnter * hi StatusLine ctermbg=blue ctermfg=white
    autocmd InsertLeave * hi StatusLine ctermbg=darkgreen ctermfg=white
augroup END
hi StatusLine ctermbg=darkgreen ctermfg=white
" }}}

" {{{ 6. キーマッピング
let mapleader = "\<Space>"

nnoremap <Leader>w :write<CR>
nnoremap <Leader>q :confirm quit<CR>
nnoremap <Leader>d :copy .<CR>
nnoremap <Leader>o o<Esc>k
nnoremap <Leader>O O<Esc>j
nnoremap Y y$
nnoremap x "_x
nnoremap <Esc><Esc> :nohlsearch<CR>

nnoremap <expr> j v:count == 0 ? 'gj' : 'j'
nnoremap <expr> k v:count == 0 ? 'gk' : 'k'
nnoremap H ^
nnoremap L $
nnoremap <C-d> <C-d>zz
nnoremap <C-u> <C-u>zz
nnoremap n nzzzv
nnoremap N Nzzzv

nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

nnoremap <Leader>bn :bnext<CR>
nnoremap <Leader>bp :bprevious<CR>
nnoremap <Leader>bd :bdelete<CR>

inoremap jj <Esc>
inoremap <C-a> <Home>
inoremap <C-e> <End>

vnoremap < <gv
vnoremap > >gv
vnoremap J :move '>+1<CR>gv=gv
vnoremap K :move '<-2<CR>gv=gv
" }}}

" {{{ 7. 言語別設定
function! s:SetIndent(width, use_tabs) abort
    let &l:tabstop = a:width
    let &l:shiftwidth = a:width
    let &l:softtabstop = a:width
    let &l:expandtab = !a:use_tabs
endfunction

function! s:RunFile() abort
    write
    let l:runners = {
        \ 'python': 'python3', 'sh': 'bash', 'bash': 'bash',
        \ 'javascript': 'node', 'typescript': 'npx ts-node',
        \ 'go': 'go run', 'ruby': 'ruby', 'perl': 'perl',
        \ }
    let l:ft = &filetype
    if l:ft ==# 'c'
        execute '!gcc -o %:r ' . shellescape(expand('%')) . ' && ./%:r'
    elseif l:ft ==# 'rust'
        execute '!cargo run'
    elseif has_key(l:runners, l:ft)
        execute '!' . l:runners[l:ft] . ' ' . shellescape(expand('%'))
    else
        echo '実行方法が未定義: ' . l:ft
    endif
endfunction

function! s:RunTest() abort
    write
    let l:testers = {
        \ 'python': 'python3 -m pytest -v',
        \ 'javascript': 'npm test', 'typescript': 'npm test',
        \ 'go': 'go test ./...', 'rust': 'cargo test',
        \ }
    let l:cmd = get(l:testers, &filetype, '')
    if l:cmd !=# ''
        execute '!' . l:cmd
    else
        echo 'テスト方法が未定義: ' . &filetype
    endif
endfunction

nnoremap <F5> :call <SID>RunFile()<CR>
nnoremap <Leader>r :call <SID>RunFile()<CR>
nnoremap <Leader>t :call <SID>RunTest()<CR>

augroup vimrc_filetype
    autocmd!
    autocmd FileType python call s:SetIndent(4, 0)
    autocmd FileType python setlocal colorcolumn=80 textwidth=79
    autocmd FileType html,css,scss,vue call s:SetIndent(2, 0)
    autocmd FileType javascript,typescript,json,yaml call s:SetIndent(2, 0)
    autocmd FileType javascript,typescript setlocal colorcolumn=100
    autocmd FileType make call s:SetIndent(8, 1)
    autocmd FileType sh,bash,zsh call s:SetIndent(4, 0)
    autocmd FileType sh,bash,zsh setlocal colorcolumn=80
    autocmd FileType go call s:SetIndent(4, 1)
    autocmd FileType markdown call s:SetIndent(2, 0)
    autocmd FileType markdown setlocal wrap linebreak spell spelllang=en,cjk
    autocmd FileType gitcommit setlocal spell spelllang=en,cjk textwidth=72
augroup END
" }}}

" {{{ 8. 自動処理
function! s:TrimWhitespace() abort
    if &filetype ==# 'markdown' | return | endif
    let l:save = winsaveview()
    keeppatterns %s/\s\+$//e
    call winrestview(l:save)
endfunction

function! s:CdProjectRoot() abort
    let l:markers = ['.git', 'Makefile', 'package.json', 'Cargo.toml',
        \ 'go.mod', 'pyproject.toml']
    let l:dir = expand('%:p:h')
    while l:dir !=# '/' && l:dir !=# ''
        for l:m in l:markers
            if isdirectory(l:dir.'/'.l:m) || filereadable(l:dir.'/'.l:m)
                execute 'lcd' fnameescape(l:dir)
                return
            endif
        endfor
        let l:dir = fnamemodify(l:dir, ':h')
    endwhile
endfunction

function! s:InsertTemplate() abort
    if line('$') != 1 || getline(1) !=# '' | return | endif
    let l:templates = {
        \ 'python': ['#!/usr/bin/env python3', '"""', 'Description.', '"""', '', ''],
        \ 'sh':     ['#!/bin/bash', 'set -euo pipefail', '', ''],
        \ }
    let l:tmpl = get(l:templates, &filetype, [])
    if !empty(l:tmpl)
        call setline(1, l:tmpl)
        call cursor(len(l:tmpl), 1)
    endif
endfunction

augroup vimrc_autocmd
    autocmd!
    autocmd BufWritePre * call s:TrimWhitespace()
    autocmd BufReadPost *
        \ if line("'\"") >= 1 && line("'\"") <= line("$") && &ft !~# 'commit' |
        \     exe "normal! g`\"" | endif
    autocmd BufEnter * call s:CdProjectRoot()
    autocmd BufNewFile *.py,*.sh call s:InsertTemplate()
augroup END

" undoディレクトリの作成
if !isdirectory(expand('~/.vim/undo'))
    call mkdir(expand('~/.vim/undo'), 'p')
endif
" }}}

" {{{ 9. カスタムコマンド
command! TrimWhitespace call s:TrimWhitespace()
command! CdRoot call s:CdProjectRoot()
command! CopyPath let @+ = expand('%:p')
command! CopyRelPath let @+ = expand('%')
" }}}
```

</details>

---

## 評価チェックリスト

完成したvimrcが以下を満たしているか確認しましょう。

### 機能面
- [ ] 4言語以上のインデント設定が正しく動作する
- [ ] `<F5>` でPython/Shellファイルが実行できる
- [ ] `<Leader>t` でテストが実行できる
- [ ] ステータスラインにモード・ファイル名・タイプ・位置が表示される
- [ ] 保存時に行末空白が自動削除される
- [ ] 前回の編集位置が復元される

### コード品質
- [ ] すべての関数に `s:` と `abort` が付いている
- [ ] すべての `autocmd` が `augroup` で管理されている
- [ ] すべてのマッピングが `noremap` 系
- [ ] `autocmd` 内で `setlocal` を使用している
- [ ] セクション分けとコメントが適切

### テスト方法
- [ ] `vim -u your_vimrc.vim test.py` — Pythonファイルの設定確認
- [ ] `vim -u your_vimrc.vim test.html` — HTMLファイルのインデント確認
- [ ] `vim -u your_vimrc.vim Makefile` — タブ文字が使われることの確認
- [ ] `:set tabstop?` で各言語の設定値を確認
- [ ] `:verbose nmap <Leader>r` でマッピングの確認
