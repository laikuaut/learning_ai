# 第7章 演習：Vimの設定とカスタマイズ

---

## 基本問題

### 問題1: 基本的なset設定

以下の各要件を満たす Vim の設定コマンドを答えてください。

a) 行番号を表示する
b) タブ文字をスペース4つに変換する
c) 検索結果をハイライト表示する

<details>
<summary>解答</summary>

```vim
" a) 行番号を表示する
set number

" b) タブ文字をスペース4つに変換する（3つの設定が必要）
set tabstop=4
set shiftwidth=4
set expandtab

" c) 検索結果をハイライト表示する
set hlsearch
```

- `set number` は絶対行番号、`set relativenumber` は相対行番号です
- `expandtab` がないとタブ文字がそのまま挿入されます
- `hlsearch` のハイライトは `:nohlsearch` で一時的に消せます

</details>

---

### 問題2: キーマッピングの設定

以下の各要件を満たすキーマッピングを `.vimrc` に記述してください。

a) ノーマルモードで `<Space>w` を押すと保存（`:w`）する
b) 挿入モードで `jj` を押すと ESC する
c) ノーマルモードで `<Space>q` を押すと終了（`:q`）する

<details>
<summary>解答</summary>

```vim
" Leader キーの設定（a と c で使用）
let mapleader = " "

" a) Space+w で保存
nnoremap <Leader>w :w<CR>

" b) jj で ESC
inoremap jj <Esc>

" c) Space+q で終了
nnoremap <Leader>q :q<CR>
```

- `nnoremap` はノーマルモード用の非再帰マッピングです
- `inoremap` は挿入モード用の非再帰マッピングです
- `<CR>` は Enter キーを意味します
- 常に `noremap` 系を使い、`map` 系は避けましょう

</details>

---

### 問題3: カラースキームの変更

以下の操作を行うコマンドを答えてください。

a) 現在利用可能なカラースキームを確認する方法
b) カラースキームを `desert` に変更するコマンド
c) 背景を暗い色に設定するコマンド

<details>
<summary>解答</summary>

```vim
" a) 利用可能なカラースキームを確認
:colorscheme [Tab キーを押して候補を表示]
" または
:echo globpath(&rtp, 'colors/*.vim')

" b) カラースキームを desert に変更
:colorscheme desert

" c) 背景を暗い色に設定
:set background=dark
```

- Tab キーで補完候補を表示するには `set wildmenu` が設定されている必要があります
- `.vimrc` に記述する場合は `:` を省いて `colorscheme desert` と書きます
- `background` は `dark` と `light` の2種類です

</details>

---

## 応用問題

### 問題4: 実用的なキーマッピングの作成

以下の要件を満たすキーマッピングを作成してください。

a) ノーマルモードで `Ctrl+h/j/k/l` でウィンドウ間を移動する
b) ビジュアルモードで `>` や `<` を押した後も選択状態を維持する
c) ノーマルモードで ESC を2回押すと検索ハイライトを消す

<details>
<summary>ヒント</summary>

- ウィンドウ移動は `<C-w>h` 等で行いますが、これを `<C-h>` だけで実行したい
- ビジュアルモードでインデント後に `gv` で再選択できます
- `:nohlsearch` で検索ハイライトを消せます

</details>

<details>
<summary>解答</summary>

```vim
" a) Ctrl+h/j/k/l でウィンドウ移動
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" b) インデント後も選択を維持
vnoremap > >gv
vnoremap < <gv

" c) ESC2回でハイライト消去
nnoremap <Esc><Esc> :nohlsearch<CR>
```

- `<C-h>` は `Ctrl+h` を意味します
- `>gv` は「インデントしてから再選択」という意味です
- これらは多くの Vim ユーザーが使っている定番マッピングです

</details>

---

### 問題5: ステータスラインの設定

以下の情報を表示するステータスラインを設定してください。

表示したい情報（左側）：
- ファイル名
- 変更フラグ（未保存なら [+] を表示）

表示したい情報（右側）：
- ファイルタイプ
- 行番号:列番号
- ファイル内の位置（パーセント）

期待される表示例：
```
 main.py [+]                          [python] 42:10 65%
```

<details>
<summary>ヒント</summary>

- `%f` はファイル名、`%m` は変更フラグです
- `%=` は左右の区切り（右寄せ開始）です
- `%y` はファイルタイプ、`%l` は行番号、`%c` は列番号、`%p` はパーセントです

</details>

<details>
<summary>解答</summary>

```vim
" ステータスラインを常に表示
set laststatus=2

" ステータスラインの内容を設定
set statusline=
set statusline+=\ %f              " ファイル名
set statusline+=\ %m              " 変更フラグ [+]
set statusline+=%=                " 右寄せ開始
set statusline+=\ %y              " ファイルタイプ [python]
set statusline+=\ %l:%c           " 行番号:列番号
set statusline+=\ %p%%            " パーセント（%% でリテラルの % を表示）
set statusline+=\                 " 末尾スペース
```

- `set laststatus=2` がないとステータスラインが表示されません
- `%=` を境に左寄せと右寄せが分かれます
- `%%` で `%` の文字そのものを表示します
- `\ ` でスペースを挿入しています

</details>

---

## チャレンジ問題

### 問題6: 自分だけの .vimrc を作成

以下の要件を満たす `.vimrc` を一から作成してください。

要件:
1. 行番号（相対行番号）を表示
2. タブをスペース2つに設定
3. 検索のインクリメンタル検索と smartcase を有効化
4. シンタックスハイライトを有効化
5. Leader キーをスペースに設定
6. `jk` で ESC するマッピング
7. Leader+s で保存するマッピング
8. ウィンドウ移動を Ctrl+h/j/k/l に設定
9. カラースキームを `slate` に設定
10. クリップボードをシステムと連携

<details>
<summary>解答</summary>

```vim
" ============================================================
" 基本設定
" ============================================================
set nocompatible
syntax on
filetype plugin indent on

" ============================================================
" 表示
" ============================================================
set number
set relativenumber
set cursorline
set showcmd
set laststatus=2
colorscheme slate
set background=dark

" ============================================================
" インデント（スペース2つ）
" ============================================================
set tabstop=2
set shiftwidth=2
set softtabstop=2
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
" その他
" ============================================================
set encoding=utf-8
set clipboard=unnamedplus
set hidden
set mouse=a
set backspace=indent,eol,start
set belloff=all

" ============================================================
" キーマッピング
" ============================================================
let mapleader = " "

" jk で ESC
inoremap jk <Esc>

" Leader+s で保存
nnoremap <Leader>s :w<CR>

" ウィンドウ移動
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" 検索ハイライト消去
nnoremap <Esc><Esc> :nohlsearch<CR>

" Y を行末までヤンクに変更
nnoremap Y y$

" ビジュアルモードでインデント後も選択維持
vnoremap > >gv
vnoremap < <gv
```

- 設定はカテゴリごとにコメントで区切ると見やすくなります
- 自分が理解できない設定は入れないようにしましょう
- `.vimrc` は Git リポジトリで管理するとバックアップや環境移行が楽です
- 設定は少しずつ追加していくのがおすすめです

</details>
