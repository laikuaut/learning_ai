# 第1章 演習：vimrcの基本と仕組み

## 演習の目標

- `.vimrc` ファイルの場所と役割を理解できる
- `set` コマンドと `let` コマンドの使い分けができる
- 設定の確認・変更・再読み込みが自力でできる
- vimrc 内のコメントの書き方を正しく使える

---

## 基本問題

### 問題1：.vimrc ファイルの作成と配置

自分の環境で `.vimrc` ファイルを作成し、以下の設定を記述してください。

1. 行番号を表示する
2. シンタックスハイライトを有効にする
3. それぞれの設定行にコメントで説明を付ける

**期待される .vimrc の内容：**
```vim
" 行番号を表示する
set number

" シンタックスハイライトを有効にする
syntax on
```

<details>
<summary>ヒント</summary>

- `.vimrc` はホームディレクトリに作成します（`~/.vimrc`）
- Vim のコメントは `"` （ダブルクォーテーション）で始めます
- ターミナルで `vim ~/.vimrc` を実行して編集できます

</details>

<details>
<summary>解答例</summary>

```bash
# ターミナルで .vimrc を作成・編集する
vim ~/.vimrc
```

```vim
" .vimrc - Vim設定ファイル
" 作成日: 2026-03-29

" 行番号を表示する
set number

" シンタックスハイライトを有効にする
syntax on
```

```
" Vim のコメントは「"」で始めます
" 行頭に「"」を置くとその行全体がコメントになります
" インラインコメントも可能ですが、set コマンドの後ろに置く場合は注意が必要です
```

</details>

---

### 問題2：設定の確認コマンド

Vim のコマンドラインモードで、以下の情報を確認するコマンドをそれぞれ答えてください。

1. `number` オプションが現在有効かどうかを確認する
2. `tabstop` の現在の値を確認する
3. `number` に関連する全オプションの現在値を一覧表示する

**期待される操作と出力例：**
```
:set number?
  → number  （有効の場合）
  → nonumber （無効の場合）

:set tabstop?
  → tabstop=8  （デフォルト値）

:verbose set number?
  → number
  →   Last set from ~/.vimrc line 5
```

<details>
<summary>ヒント</summary>

- `set オプション名?` で現在の値を確認できます
- `:verbose` を前置すると、その設定がどのファイルの何行目で設定されたかも表示されます

</details>

<details>
<summary>解答例</summary>

```vim
" 1. number オプションの有効/無効を確認
:set number?

" 2. tabstop の現在値を確認
:set tabstop?

" 3. verbose を付けて設定元ファイルも表示
:verbose set number?

" 補足：すべてのオプションの現在値を一覧表示する場合
:set

" デフォルトから変更されたオプションだけ表示する場合
:set!
```

</details>

---

### 問題3：source コマンドによる再読み込み

`.vimrc` を編集した後、Vim を再起動せずに設定を反映させる方法を2つ答えてください。また、それぞれの違いを説明してください。

**期待される回答：**
```
方法1: :source ~/.vimrc
方法2: :so %  （.vimrc を開いている場合）

違い:
- :source ~/.vimrc はどのバッファからでも実行できる
- :so % は現在開いているファイルを読み込むため、.vimrc を編集中の場合に便利
```

<details>
<summary>ヒント</summary>

- `source`（省略形 `so`）コマンドは指定したファイルを Vim スクリプトとして実行します
- `%` は現在編集中のファイルのパスを表す特殊記号です

</details>

<details>
<summary>解答例</summary>

```vim
" 方法1：フルパスを指定して再読み込み
" どのバッファを開いていても使える汎用的な方法です
:source ~/.vimrc

" 方法2：現在のファイル（%）を再読み込み
" .vimrc 自体を編集しているときに使える便利な方法です
:so %

" 注意点：
" - source はファイル全体を再実行するため、
"   autocmd が重複登録される可能性があります
" - augroup を使って autocmd を管理するのがベストプラクティスです
" - 例：
"   augroup MyAutoCmd
"     autocmd!
"     autocmd FileType python setlocal tabstop=4
"   augroup END
```

</details>

---

## 応用問題

### 問題4：set コマンドと let コマンドの使い分け

以下の設定を `set` と `let` のどちらで書くべきか判断し、正しい記述を答えてください。

1. タブ幅を 4 に設定する
2. `mapleader` を スペースキーに設定する
3. 行を折り返さない設定にする
4. グローバル変数 `g:loaded_netrw` に `1` を代入する

**期待される .vimrc の記述：**
```vim
set tabstop=4
let mapleader = " "
set nowrap
let g:loaded_netrw = 1
```

<details>
<summary>ヒント</summary>

- `set` は Vim の組み込みオプション（`:help options` で一覧できるもの）に使います
- `let` は変数への代入に使います（`g:` はグローバル変数のプレフィックスです）
- `mapleader` は特殊な変数で、`let` を使って設定します

</details>

<details>
<summary>解答例</summary>

```vim
" 1. tabstop はVim組み込みオプションなので set を使う
set tabstop=4

" 2. mapleader は変数なので let を使う
" スペースキーをリーダーキーにするのは現代的なベストプラクティスです
let mapleader = " "

" 3. wrap はVim組み込みオプションなので set を使う
" ブール値オプションを無効にするには「no」を前置します
set nowrap

" 4. g:loaded_netrw はグローバル変数なので let を使う
" この変数を1にすると、デフォルトのファイルブラウザ netrw の読み込みを無効化できます
let g:loaded_netrw = 1

" 使い分けの原則：
" - set  → :help 'オプション名' で出てくるVimのオプション
" - let  → それ以外の変数（g:, b:, s:, l: などのスコープ付き変数を含む）
```

</details>

---

### 問題5：設定のトグルと一時的な変更

以下の操作を行うコマンドを答えてください。

1. 行番号の表示・非表示をワンコマンドでトグルする
2. 現在のバッファだけで `wrap` を有効にする（グローバル設定は変えない）
3. `.vimrc` に、`F2` キーで行番号表示をトグルするキーマッピングを書く

**期待される操作と .vimrc の記述：**
```
1. :set number!

2. :setlocal wrap

3. nnoremap <F2> :set number!<CR>
```

<details>
<summary>ヒント</summary>

- ブール値オプションの末尾に `!` を付けると、有効/無効がトグルされます
- `setlocal` は現在のバッファ/ウィンドウだけに設定を適用します
- `nnoremap` はノーマルモードの再帰しないキーマッピングです
- `<CR>` はエンターキーを意味します

</details>

<details>
<summary>解答例</summary>

```vim
" 1. number オプションのトグル
" 「!」を末尾に付けると有効 ↔ 無効が切り替わります
:set number!

" 2. 現在のバッファだけに wrap を適用
" setlocal はバッファローカルな設定変更です
" 他のバッファには影響しません
:setlocal wrap

" 3. .vimrc に記述するキーマッピング
" ノーマルモードで F2 を押すと行番号の表示/非表示が切り替わります
nnoremap <F2> :set number!<CR>

" 補足：相対行番号も一緒にトグルしたい場合
nnoremap <F2> :set number! relativenumber!<CR>
```

</details>

---

### 問題6：条件付き設定

以下の要件を満たす `.vimrc` の記述を作成してください。

- GUI版Vim（gVim）の場合のみフォントを設定する
- ターミナル版Vimの場合のみ、256色カラーを有効にする

**期待される .vimrc の記述：**
```vim
if has('gui_running')
  set guifont=Monospace\ 12
else
  set t_Co=256
endif
```

<details>
<summary>ヒント</summary>

- `has()` 関数で Vim の機能を検査できます
- `has('gui_running')` は GUI 版で起動している場合に `1` を返します
- GUIフォント名のスペースはバックスラッシュでエスケープします

</details>

<details>
<summary>解答例</summary>

```vim
" GUI版とターミナル版で設定を切り替える
if has('gui_running')
  " GUI版Vim（gVim）の場合
  " guifont でフォントを指定します
  " スペースは \ でエスケープが必要です
  set guifont=Monospace\ 12
else
  " ターミナル版Vimの場合
  " t_Co でターミナルの色数を指定します
  set t_Co=256
endif

" 補足：OS ごとにフォントを変えたい場合の例
if has('gui_running')
  if has('win32')
    set guifont=Consolas:h11
  elseif has('mac')
    set guifont=Menlo:h12
  else
    set guifont=Monospace\ 12
  endif
endif
```

</details>

---

## チャレンジ問題

### 問題7：整理された .vimrc テンプレートの作成

以下の要件をすべて満たす `.vimrc` を作成してください。

**要件：**
1. ファイル冒頭にコメントで作成者名・作成日・概要を書く
2. セクションをコメントで区切る（基本設定 / 表示設定 / 検索設定）
3. 基本設定：`nocompatible`、`encoding=utf-8`、`fileencoding=utf-8`
4. 表示設定：行番号表示、カーソル行ハイライト、シンタックスハイライト
5. 検索設定：インクリメンタルサーチ、検索ハイライト、大文字小文字スマート判定
6. リーダーキーをスペースに設定
7. `source` で再読み込みしても `autocmd` が重複しないようにする

**期待される .vimrc の構成：**
```vim
" =============================================================================
" .vimrc
" Author: Your Name
" Created: 2026-03-29
" Description: Vim基本設定ファイル
" =============================================================================

" --- 基本設定 ---
...

" --- 表示設定 ---
...

" --- 検索設定 ---
...

" --- autocmd ---
augroup MyAutoCmd
  autocmd!
  ...
augroup END
```

<details>
<summary>ヒント</summary>

- `nocompatible` は vi 互換モードを無効にし、Vim の全機能を使えるようにします
- `augroup` と `autocmd!` を組み合わせると、再読み込み時に autocmd が重複登録されるのを防げます
- セクションを視覚的に分けると可読性が大幅に向上します

</details>

<details>
<summary>解答例</summary>

```vim
" =============================================================================
" .vimrc
" Author: Your Name
" Created: 2026-03-29
" Description: Vim基本設定ファイル
" =============================================================================

" --- 基本設定 ---
" vi 互換モードを無効にする（Vim の全機能を使うために必須）
set nocompatible

" 文字エンコーディングを UTF-8 に設定
set encoding=utf-8
set fileencoding=utf-8

" リーダーキーをスペースに設定
" 多くのモダンな Vim 設定で推奨されている設定です
let mapleader = " "

" --- 表示設定 ---
" 行番号を表示する
set number

" カーソル行をハイライトする
set cursorline

" シンタックスハイライトを有効にする
syntax on

" --- 検索設定 ---
" インクリメンタルサーチ（入力中にリアルタイムで検索）
set incsearch

" 検索結果をハイライト
set hlsearch

" 大文字小文字を区別しない（ただし大文字を含む場合は区別する）
set ignorecase
set smartcase

" --- autocmd ---
" augroup で囲み、autocmd! でクリアすることで
" source による再読み込み時の重複登録を防止します
augroup MyAutoCmd
  autocmd!
  " 例：Python ファイルを開いたらタブ幅を4に設定
  autocmd FileType python setlocal tabstop=4 shiftwidth=4 expandtab
augroup END
```

</details>
