# 第7章：Vimの設定とカスタマイズ

## この章のゴール

- `.vimrc` の役割と場所を理解する
- 基本的な設定オプションを使いこなせる
- キーマッピングを設定できる
- カラースキームを変更できる
- ステータスラインをカスタマイズできる

---

## 1. .vimrc の基本

### .vimrc とは

`.vimrc` は Vim の設定ファイルです。Vim 起動時に自動的に読み込まれ、設定やキーマッピングが適用されます。

```
  設定ファイルの場所:

  Linux / macOS:  ~/.vimrc
  Windows:        ~/_vimrc または $HOME/_vimrc

  ※ Neovim の場合: ~/.config/nvim/init.vim
```

### .vimrc の作成と読み込み

```bash
# .vimrc を作成（またはVimで編集）
$ vim ~/.vimrc
```

```vim
" .vimrc の中身はVimコマンドそのものです
" " で始まる行はコメントです

" 設定を変更した後、Vimを再起動するか、以下で再読み込み
:source ~/.vimrc
" 省略形
:so %              " 現在編集中のファイルが .vimrc の場合
```

### ポイントまとめ

- `.vimrc` は `~/.vimrc` に配置します
- Vim コマンドをそのまま記述します
- `:source ~/.vimrc` で再読み込みできます

---

## 2. 基本的な設定オプション

### 表示に関する設定

```vim
" --- 行番号 ---
set number              " 行番号を表示
set relativenumber      " 相対行番号を表示（現在行からの距離）
" 両方設定すると、現在行は絶対行番号、他は相対行番号になる

" --- シンタックスハイライト ---
syntax on               " シンタックスハイライトを有効化
filetype plugin indent on  " ファイルタイプに応じたプラグインとインデントを有効化

" --- カーソル ---
set cursorline          " 現在行をハイライト
set showcmd             " 入力中のコマンドを右下に表示
set showmode            " 現在のモードを左下に表示

" --- 表示 ---
set wrap                " 長い行を折り返して表示
set linebreak           " 単語の途中で折り返さない
set scrolloff=5         " カーソルの上下に常に5行表示する
set sidescrolloff=5     " カーソルの左右に常に5列表示する
set signcolumn=yes      " サイン列を常に表示
```

### インデントに関する設定

```vim
" --- タブとインデント ---
set tabstop=4           " タブ文字の表示幅
set shiftwidth=4        " 自動インデントの幅
set softtabstop=4       " Tab キー押下時の挿入幅
set expandtab           " タブをスペースに変換
set autoindent          " 前の行のインデントを引き継ぐ
set smartindent         " 構文に応じた自動インデント
```

```
  tabstop と shiftwidth の違い:

  tabstop=4:     タブ文字の表示幅（既存のタブの見た目）
  shiftwidth=4:  >> や << でのインデント幅
  softtabstop=4: Tab キーを押した時に挿入される幅
  expandtab:     タブの代わりにスペースを挿入

  推奨: 4つとも同じ値に設定し、expandtab を有効にする
```

### 検索に関する設定

```vim
set hlsearch            " 検索結果をハイライト
set incsearch           " インクリメンタル検索（入力中にリアルタイム検索）
set ignorecase          " 検索で大小文字を区別しない
set smartcase           " 大文字が含まれる場合は区別する
```

### エンコーディングに関する設定

```vim
set encoding=utf-8           " Vim 内部のエンコーディング
set fileencoding=utf-8       " ファイル保存時のエンコーディング
set fileencodings=utf-8,cp932,euc-jp  " ファイル読み込み時の自動判定順
```

### その他の便利な設定

```vim
set clipboard=unnamedplus    " システムクリップボードと連携
set mouse=a                  " マウス操作を有効化
set wildmenu                 " コマンドライン補完を強化
set wildmode=longest:full,full  " 補完の動作設定
set history=1000             " コマンド履歴の保存数
set undofile                 " アンドゥ履歴をファイルに保存
set backup=no                " バックアップファイルを作成しない
set swapfile=no              " スワップファイルを作成しない
set hidden                   " バッファを保存せずに切り替え可能にする
set belloff=all              " ビープ音を無効化
set backspace=indent,eol,start  " バックスペースの動作を改善
```

### ポイントまとめ

- `set number` と `set relativenumber` で行番号を表示します
- `tabstop`/`shiftwidth`/`expandtab` でインデントを統一します
- `hlsearch`/`incsearch`/`smartcase` は検索の必須設定です
- `clipboard=unnamedplus` でシステムクリップボードと連携できます

---

## 3. キーマッピング

### マッピングの基本

```vim
" 構文: {モード}map {キー} {実行するコマンド}

" モード別のマッピングコマンド:
"   nmap  ← ノーマルモード
"   imap  ← 挿入モード
"   vmap  ← ビジュアルモード
"   cmap  ← コマンドラインモード
"   map   ← ノーマル + ビジュアル + オペレータ待機
```

### noremap の重要性

```vim
" map と noremap の違い:
"   map   ← 再帰的（マッピングの中でさらにマッピングが展開される）
"   noremap ← 非再帰的（安全、こちらを推奨）

" 常に noremap 系を使うことを推奨:
"   nnoremap  ← ノーマルモード（非再帰）
"   inoremap  ← 挿入モード（非再帰）
"   vnoremap  ← ビジュアルモード（非再帰）
"   cnoremap  ← コマンドラインモード（非再帰）
```

> **重要**: 特別な理由がない限り、常に `noremap` 系を使ってください。`map` 系はマッピングの連鎖で予期しない動作を引き起こすことがあります。

### Leader キー

Leader キーは、カスタムマッピングのプレフィックスとして使う特別なキーです。

```vim
" Leader キーの設定（スペースキーを推奨）
let mapleader = " "

" Leader キーを使ったマッピング例
nnoremap <Leader>w :w<CR>           " Space+w で保存
nnoremap <Leader>q :q<CR>           " Space+q で終了
nnoremap <Leader>e :Explore<CR>     " Space+e でファイルエクスプローラ
```

### 実用的なマッピング例

```vim
" --- ESC の代替 ---
inoremap jj <Esc>                   " jj で挿入モードを抜ける
inoremap jk <Esc>                   " jk で挿入モードを抜ける

" --- 検索ハイライトの解除 ---
nnoremap <Esc><Esc> :nohlsearch<CR> " ESC2回でハイライト消去

" --- ウィンドウ移動の簡略化 ---
nnoremap <C-h> <C-w>h              " Ctrl+h で左のウィンドウへ
nnoremap <C-j> <C-w>j              " Ctrl+j で下のウィンドウへ
nnoremap <C-k> <C-w>k              " Ctrl+k で上のウィンドウへ
nnoremap <C-l> <C-w>l              " Ctrl+l で右のウィンドウへ

" --- バッファ操作 ---
nnoremap <Leader>bn :bnext<CR>      " Space+bn で次のバッファ
nnoremap <Leader>bp :bprev<CR>      " Space+bp で前のバッファ
nnoremap <Leader>bd :bdelete<CR>    " Space+bd でバッファ削除

" --- 行の移動 ---
nnoremap <A-j> :m .+1<CR>==        " Alt+j で行を下に移動
nnoremap <A-k> :m .-2<CR>==        " Alt+k で行を上に移動
vnoremap <A-j> :m '>+1<CR>gv=gv    " ビジュアルモードで行を下に
vnoremap <A-k> :m '<-2<CR>gv=gv    " ビジュアルモードで行を上に

" --- ビジュアルモードでインデント後も選択を維持 ---
vnoremap > >gv
vnoremap < <gv

" --- Y を行末までヤンクに変更（D, C と統一） ---
nnoremap Y y$
```

### ポイントまとめ

- 必ず `noremap` 系（`nnoremap`, `inoremap` 等）を使いましょう
- Leader キーにはスペースキーを設定するのが人気です
- `jj` で ESC、`Ctrl+h/j/k/l` でウィンドウ移動は定番のマッピングです

---

## 4. カラースキームとシンタックスハイライト

### カラースキームの変更

```vim
" カラースキームを設定
colorscheme desert

" 背景の明暗を設定
set background=dark     " 暗い背景
set background=light    " 明るい背景

" 利用可能なカラースキームを確認
:colorscheme [Tab]      " Tab キーで候補を表示
```

### 組み込みカラースキーム

```vim
" Vim に標準で含まれるカラースキーム:
" default, blue, darkblue, delek, desert, elflord,
" evening, habamax, industry, koehler, lunaperche,
" morning, murphy, pablo, peachpuff, quiet, ron,
" shine, slate, torte, wildcharm, zaibatsu

" おすすめ:
colorscheme desert      " 暗い背景向け、見やすい
colorscheme slate       " 暗い背景向け、落ち着いた色合い
colorscheme industry    " 暗い背景向け、コントラスト高め
```

### ターミナルの色数設定

```vim
" 256色を有効化
set t_Co=256

" True Color（24ビットカラー）を有効化
if has('termguicolors')
  set termguicolors
endif
```

### ポイントまとめ

- `colorscheme 名前` でカラースキームを変更します
- `set background=dark/light` で背景の明暗を設定します
- 外部カラースキームはプラグインとしてインストールできます

---

## 5. ステータスラインの設定

### ステータスラインの有効化

```vim
set laststatus=2        " ステータスラインを常に表示
                        " 0: 表示しない
                        " 1: ウィンドウが2つ以上の時のみ
                        " 2: 常に表示
```

### ステータスラインのカスタマイズ

```vim
" statusline の書式
set statusline=%f       " ファイル名
set statusline+=%m      " 変更フラグ [+]
set statusline+=%r      " 読み取り専用フラグ [RO]
set statusline+=%h      " ヘルプフラグ [Help]
set statusline+=%=      " 左右の区切り（以降は右寄せ）
set statusline+=%y      " ファイルタイプ
set statusline+=\ [%{&encoding}]  " エンコーディング
set statusline+=\ [%l/%L]         " 現在行/全行数
set statusline+=\ [%c]            " カラム番号
set statusline+=\ [%p%%]          " ファイル内の位置（%）
```

### 実用的なステータスライン設定例

```vim
" シンプルだが情報量の多いステータスライン
set statusline=
set statusline+=\ %f                " ファイルパス
set statusline+=\ %m%r              " 変更・読取専用フラグ
set statusline+=%=                  " 右寄せ開始
set statusline+=\ %y                " ファイルタイプ
set statusline+=\ %{&encoding}      " エンコーディング
set statusline+=\ %l:%c             " 行:列
set statusline+=\ %p%%              " 位置（パーセント）
set statusline+=\                   " 末尾スペース
```

```
  表示例:
  ┌──────────────────────────────────────────────────────┐
  │  main.py [+]              [python] utf-8  42:10 65% │
  └──────────────────────────────────────────────────────┘
```

### ポイントまとめ

- `set laststatus=2` でステータスラインを常に表示します
- `statusline` でファイル名、行番号、エンコーディングなどを表示できます
- より高機能なステータスラインが必要なら lightline.vim や airline などのプラグインがあります

---

## 6. おすすめの初期設定テンプレート

以下は初心者向けの `.vimrc` テンプレートです。

```vim
" ============================================================
" 基本設定
" ============================================================
set nocompatible            " Vi互換モードを無効化
syntax on                   " シンタックスハイライト
filetype plugin indent on   " ファイルタイプ検出

" ============================================================
" 表示
" ============================================================
set number                  " 行番号
set relativenumber          " 相対行番号
set cursorline              " カーソル行ハイライト
set showcmd                 " 入力中のコマンドを表示
set showmode                " モードを表示
set laststatus=2            " ステータスライン常時表示
set scrolloff=5             " スクロール時の余白
set signcolumn=yes          " サイン列を常に表示
colorscheme desert          " カラースキーム
set background=dark         " 暗い背景

" ============================================================
" インデント
" ============================================================
set tabstop=4               " タブ幅
set shiftwidth=4            " インデント幅
set softtabstop=4           " Tab キーの挿入幅
set expandtab               " タブをスペースに変換
set autoindent              " 自動インデント
set smartindent             " スマートインデント

" ============================================================
" 検索
" ============================================================
set hlsearch                " 検索ハイライト
set incsearch               " インクリメンタル検索
set ignorecase              " 大小文字を区別しない
set smartcase               " 大文字を含む場合は区別する

" ============================================================
" エンコーディング
" ============================================================
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=utf-8,cp932,euc-jp

" ============================================================
" その他
" ============================================================
set hidden                  " バッファを保存せずに切り替え
set clipboard=unnamedplus   " システムクリップボード連携
set mouse=a                 " マウス有効
set wildmenu                " コマンド補完強化
set backspace=indent,eol,start  " BSの動作改善
set belloff=all             " ビープ音無効

" ============================================================
" キーマッピング
" ============================================================
let mapleader = " "

" jj で挿入モードを抜ける
inoremap jj <Esc>

" ESC2回で検索ハイライト消去
nnoremap <Esc><Esc> :nohlsearch<CR>

" ウィンドウ移動
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Y を行末までヤンクに変更
nnoremap Y y$

" ビジュアルモードでインデント後も選択を維持
vnoremap > >gv
vnoremap < <gv

" Leader + w で保存
nnoremap <Leader>w :w<CR>
" Leader + q で終了
nnoremap <Leader>q :q<CR>
```

### ポイントまとめ

- まずはシンプルな設定から始めて、徐々にカスタマイズしましょう
- 自分が理解できない設定は入れないようにしましょう
- `.vimrc` は Git で管理すると、環境移行が楽になります
