# 実践課題10：リファクタリング ─ レガシーvimrc ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第5章（キーマッピング）、第6章（autocmd）、第7章（関数とカスタムコマンド）
> **課題の種類**: リファクタリング
> **学習目標**: 「動くが保守しにくい」vimrcを、構造化された読みやすい設定に段階的に改善する力を養う

---

## 課題の説明

以下は数年間にわたって継ぎ足し続けた「レガシーvimrc」です。**正しく動作します**が、以下の問題を抱えています。

- 設定がカテゴリ分けされておらず散らばっている
- 同じ設定が重複して書かれている
- `augroup` で囲まれていない `autocmd` がある
- `nmap` / `imap`（再帰マッピング）が使われている
- `set` と `setlocal` が混在している
- コメントがほとんどない
- 似たような設定が何度もコピーされている

**このvimrcを段階的にリファクタリングしてください。**

### ゴール

1. **ステップ1**: セクション分けとコメント追加
2. **ステップ2**: 重複の除去と`noremap`への統一
3. **ステップ3**: `augroup` の整理と関数の導入

---

## リファクタリング対象のvimrc

以下を `legacy.vim` として保存してください。

```vim
set nocompatible
set number
nmap <C-s> :w<CR>
imap <C-s> <Esc>:w<CR>a
set tabstop=4
autocmd FileType python set tabstop=4
autocmd FileType python set shiftwidth=4
autocmd FileType python set expandtab
set shiftwidth=4
set expandtab
set incsearch
nmap <Leader>w :w<CR>
set hlsearch
set encoding=utf-8
autocmd FileType html set tabstop=2
autocmd FileType html set shiftwidth=2
autocmd FileType html set expandtab
set ignorecase
set smartcase
set cursorline
nmap j gj
nmap k gk
set softtabstop=4
autocmd FileType css set tabstop=2
autocmd FileType css set shiftwidth=2
autocmd FileType css set expandtab
set autoindent
nmap <C-h> <C-w>h
nmap <C-j> <C-w>j
nmap <C-k> <C-w>k
nmap <C-l> <C-w>l
set laststatus=2
autocmd FileType javascript set tabstop=2
autocmd FileType javascript set shiftwidth=2
autocmd FileType javascript set expandtab
syntax on
set background=dark
colorscheme desert
nmap <Leader>q :q<CR>
set backspace=indent,eol,start
autocmd FileType make set noexpandtab
autocmd FileType make set tabstop=8
autocmd FileType make set shiftwidth=8
set scrolloff=5
autocmd BufWritePre * %s/\s\+$//e
set ruler
set showcmd
nmap <Esc><Esc> :nohlsearch<CR>
set mouse=a
autocmd FileType python set colorcolumn=80
set belloff=all
set wrap
nmap <Leader>d :t.<CR>
```

---

## ステップガイド

<details>
<summary>ステップ1：セクション分けとコメント追加</summary>

まず、散らばった設定をカテゴリごとに並べ替えます。

### 分類の指針

| カテゴリ | 含まれる設定 |
|----------|-------------|
| 基本設定 | `nocompatible`, `encoding`, `backspace`, `hidden`, `belloff` |
| 表示設定 | `number`, `cursorline`, `laststatus`, `ruler`, `showcmd`, `wrap`, `scrolloff` |
| カラー | `syntax`, `background`, `colorscheme` |
| インデント | `tabstop`, `shiftwidth`, `softtabstop`, `expandtab`, `autoindent` |
| 検索 | `incsearch`, `hlsearch`, `ignorecase`, `smartcase` |
| キーマッピング | `nmap` / `nnoremap` 系 |
| ファイルタイプ | `autocmd FileType` 系 |
| 自動処理 | `autocmd BufWritePre` 系 |

同じ設定が複数箇所にある場合は1箇所にまとめます。

</details>

<details>
<summary>ステップ2：重複の除去とnoremapへの統一</summary>

### 2-1. 重複設定の除去

元のvimrcには以下の重複があります。

```vim
" デフォルト設定
set tabstop=4
set shiftwidth=4
set expandtab

" Python用（デフォルトと同じなので不要）
autocmd FileType python set tabstop=4
autocmd FileType python set shiftwidth=4
autocmd FileType python set expandtab
```

Pythonの設定はデフォルトと同じなので、Python固有の設定（`colorcolumn=80`）だけ残せば十分です。

### 2-2. `nmap` → `nnoremap` への変更

すべての `nmap` を `nnoremap` に、`imap` を `inoremap` に変更します。

```vim
" 修正前
nmap <C-s> :w<CR>
imap <C-s> <Esc>:w<CR>a
nmap j gj

" 修正後
nnoremap <C-s> :write<CR>
inoremap <C-s> <Esc>:write<CR>a
nnoremap j gj
```

### 2-3. 重複マッピングの整理

`<C-s>` と `<Leader>w` が両方保存に割り当てられています。どちらかに統一するか、意図的に両方残すかを判断します。

</details>

<details>
<summary>ステップ3：augroupの整理と関数の導入</summary>

### 3-1. autocmd をグループ化

```vim
" 修正前（augroupなし）
autocmd FileType html set tabstop=2
autocmd FileType css set tabstop=2
autocmd FileType javascript set tabstop=2
autocmd BufWritePre * %s/\s\+$//e

" 修正後
augroup FileTypeSettings
    autocmd!
    autocmd FileType html,css,javascript setlocal tabstop=2 shiftwidth=2 expandtab
    autocmd FileType make setlocal noexpandtab tabstop=8 shiftwidth=8
    autocmd FileType python setlocal colorcolumn=80
augroup END

augroup AutoCommands
    autocmd!
    autocmd BufWritePre * %s/\s\+$//e
augroup END
```

### 3-2. `set` → `setlocal` に修正

`autocmd` 内では `set` ではなく `setlocal` を使います。

### 3-3. 繰り返しを関数化

HTML/CSS/JavaScriptに同じインデント設定を繰り返す代わりに、カンマ区切りで1行にまとめるか、関数にします。

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け：セクション分け + noremap統一）</summary>

```vim
" ===========================================
" リファクタリング済みvimrc
" ===========================================

" --- 基本設定 ---
set nocompatible
set encoding=utf-8
set backspace=indent,eol,start
set belloff=all
set mouse=a

" --- 表示設定 ---
set number
set cursorline
set laststatus=2
set ruler
set showcmd
set scrolloff=5
set wrap
syntax on
set background=dark
colorscheme desert

" --- インデント ---
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set autoindent

" --- 検索 ---
set incsearch
set hlsearch
set ignorecase
set smartcase

" --- キーマッピング ---
let mapleader = "\<Space>"

nnoremap <Leader>w :write<CR>
nnoremap <Leader>q :quit<CR>
nnoremap <Leader>d :copy .<CR>
nnoremap <Esc><Esc> :nohlsearch<CR>

nnoremap j gj
nnoremap k gk

nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" --- ファイルタイプ別設定 ---
augroup FileTypeSettings
    autocmd!
    autocmd FileType html,css,javascript setlocal tabstop=2 shiftwidth=2 softtabstop=2
    autocmd FileType make setlocal noexpandtab tabstop=8 shiftwidth=8
    autocmd FileType python setlocal colorcolumn=80
augroup END

" --- 自動処理 ---
augroup AutoCommands
    autocmd!
    autocmd BufWritePre * %s/\s\+$//e
augroup END
```

**元のvimrcからの改善点**:
- カテゴリ別にセクション分け
- 重複設定を除去（元60行 → 約50行）
- `nmap` → `nnoremap` に統一
- `<C-s>` と `<Leader>w` の重複を解消（`<Leader>w` に統一）
- `autocmd` を `augroup` で囲み、`setlocal` を使用
- 同じインデント設定をカンマ区切りで1行に集約

</details>

<details>
<summary>解答例（改良版：関数導入と発展的な改善）</summary>

```vim
" ===========================================
" リファクタリング済みvimrc - 改良版
" ===========================================

" ==================== 基本設定 ====================
set nocompatible
set encoding=utf-8
scriptencoding utf-8
set fileencoding=utf-8
set backspace=indent,eol,start
set belloff=all
set mouse=a
set hidden                  " 未保存バッファの切替を許可
set autoread                " 外部変更の自動読込
set confirm                 " 未保存時に確認ダイアログ

" ==================== 表示設定 ====================
set number
set cursorline
set laststatus=2
set ruler
set showcmd
set scrolloff=5
set wrap
set linebreak
set showmatch

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

" ==================== キーマッピング ====================
let mapleader = "\<Space>"

" --- ファイル操作 ---
nnoremap <Leader>w :write<CR>
nnoremap <Leader>q :confirm quit<CR>

" --- 編集 ---
nnoremap <Leader>d :copy .<CR>
nnoremap <Esc><Esc> :nohlsearch<CR>
nnoremap Y y$

" --- 移動 ---
nnoremap <expr> j v:count == 0 ? 'gj' : 'j'
nnoremap <expr> k v:count == 0 ? 'gk' : 'k'

" --- ウィンドウ ---
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" --- ビジュアルモード ---
vnoremap < <gv
vnoremap > >gv

" ==================== ファイルタイプ別設定 ====================

" インデント設定ヘルパー
function! s:SetIndent(width, use_tabs) abort
    let &l:tabstop = a:width
    let &l:shiftwidth = a:width
    let &l:softtabstop = a:width
    let &l:expandtab = !a:use_tabs
endfunction

augroup vimrc_filetype
    autocmd!
    autocmd FileType html,css,javascript,json,yaml call s:SetIndent(2, 0)
    autocmd FileType make call s:SetIndent(8, 1)
    autocmd FileType python setlocal colorcolumn=80 textwidth=79
augroup END

" ==================== 自動処理 ====================

" 行末空白の削除（カーソル位置を保持）
function! s:TrimWhitespace() abort
    let l:save = winsaveview()
    keeppatterns %s/\s\+$//e
    call winrestview(l:save)
endfunction

augroup vimrc_autocmd
    autocmd!
    autocmd BufWritePre * call s:TrimWhitespace()

    " 前回の編集位置を復元
    autocmd BufReadPost *
        \ if line("'\"") >= 1 && line("'\"") <= line("$") && &filetype !~# 'commit' |
        \     execute "normal! g`\"" |
        \ endif
augroup END
```

**初心者向けとの違い**:

- `s:SetIndent()` 関数でインデント設定を抽象化
- `<expr>` マッピングでカウント指定時の動作を改善
- `s:TrimWhitespace()` で `keeppatterns` と `winsaveview` を使用
- `confirm quit` で安全な終了
- `hidden`, `autoread`, `confirm` で複数ファイル編集を快適に
- 前回の編集位置復元 autocmd を追加
- `vnoremap` によるインデント操作の改善

</details>

---

## リファクタリングのチェックリスト

リファクタリング後に以下をすべて確認しましょう。

- [ ] すべての `nmap`/`imap`/`vmap` が `noremap` 系に変わっているか
- [ ] 重複した設定が除去されているか
- [ ] `autocmd` がすべて `augroup` + `autocmd!` で囲まれているか
- [ ] `autocmd` 内で `setlocal` を使っているか（`set` ではなく）
- [ ] 設定がカテゴリ別にセクション分けされているか
- [ ] 各セクションにコメントがあるか
- [ ] 機能が元のvimrcと同一であるか（リグレッションなし）

---

## よくある間違い

| ミス | 正しい対応 | 説明 |
|------|-----------|------|
| リファクタリング中に機能を変えてしまう | 1ステップごとに動作確認 | リファクタリングは「動作を変えずに構造を改善」すること |
| `autocmd!` をグループの外に書く | `augroup` の直後に書く | グループ外だとグローバルな autocmd がすべて消える |
| `setlocal` にすべきところを `set` のまま | `autocmd` 内は必ず `setlocal` | バッファ固有にすべき設定がグローバルに影響する |
| デフォルトと同じ設定を残す | 思い切って削除 | 設定が多いほど読みにくく保守しにくい |
