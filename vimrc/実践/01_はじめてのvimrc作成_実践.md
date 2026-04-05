# 実践課題01：はじめてのvimrc作成 ★1

> **難易度**: ★☆☆☆☆（入門）
> **前提知識**: 第1章（vimrcの基本と仕組み）、第2章（表示とエディタの基本設定）
> **課題の種類**: ミニプロジェクト
> **学習目標**: vimrcファイルを一から作成し、基本的な `set` オプションで快適な表示環境を構築する

---

## 完成イメージ

```
" ===========================================
" My First vimrc
" ===========================================

" --- 基本設定 ---
set nocompatible
set encoding=utf-8
set fileencoding=utf-8

" --- 表示設定 ---
set number
set cursorline
set showmatch
set laststatus=2
set ruler

" --- 操作性 ---
set backspace=indent,eol,start
set whichwrap=b,s,h,l,<,>,[,]
set scrolloff=5

" --- ビープ音の無効化 ---
set belloff=all
```

Vimでこのvimrcを読み込むと、以下のような画面になります。

```
┌──────────────────────────────────────────┐
│  1 #include <stdio.h>                    │
│  2                                       │
│  3 int main(void) {          ← 行番号   │
│  4     printf("Hello!\n");   が表示      │
│  5     return 0;                         │
│  6 }                                     │
│  ─────────────────────── ← カーソル行    │
│  ~ ~ ~ ~                    がハイライト │
│                                          │
│ [ファイル名]    5行目, 10列目  ← ルーラー │
└──────────────────────────────────────────┘
```

---

## 課題の要件

1. vimrcファイルを新規作成する
2. Vi互換モードを無効にする（`nocompatible`）
3. エンコーディングをUTF-8に設定する
4. 行番号を表示する
5. カーソル行をハイライトする
6. 対応する括弧を強調表示する
7. ステータスラインを常に表示する
8. `backspace` キーの動作を直感的にする
9. スクロール時に上下に余白を持たせる
10. ビープ音を無効化する

---

## ステップガイド

<details>
<summary>ステップ1：ファイルの作成とVi互換モードの無効化</summary>

新しいファイルを作成し、まずコメントとVi互換モードの無効化を書きます。

```vim
" ===========================================
" My First vimrc
" ===========================================

" Vi互換モードを無効にする（Vim独自機能を有効化）
set nocompatible
```

**ポイント**: Vimでは `"` がコメントの開始記号です。設定の意図をコメントで残す習慣をつけましょう。

</details>

<details>
<summary>ステップ2：エンコーディングの設定</summary>

日本語を正しく扱うためにエンコーディングを設定します。

```vim
" --- エンコーディング ---
set encoding=utf-8       " Vim内部のエンコーディング
set fileencoding=utf-8   " 保存時のエンコーディング
```

`encoding` はVimの内部処理用、`fileencoding` はファイル書き込み時の文字コードです。

</details>

<details>
<summary>ステップ3：表示設定を追加する</summary>

エディタの見た目を整える設定を追加します。

```vim
" --- 表示設定 ---
set number          " 行番号を表示
set cursorline      " カーソル行をハイライト
set showmatch       " 対応する括弧を一瞬ハイライト
set laststatus=2    " ステータスラインを常に表示
set ruler           " カーソル位置を右下に表示
```

- `number` は左端に行番号を表示します
- `cursorline` は現在のカーソルがある行を目立たせます
- `showmatch` は `)`、`}`、`]` を入力したとき、対応する開き括弧を一瞬ハイライトします

</details>

<details>
<summary>ステップ4：操作性の改善</summary>

```vim
" --- 操作性 ---
set backspace=indent,eol,start  " BSキーでインデント・改行・挿入開始前を削除可能に
set whichwrap=b,s,h,l,<,>,[,]  " 行頭・行末で前後の行に移動可能に
set scrolloff=5                 " スクロール時に上下5行の余白を確保
```

- `backspace` を設定しないと、挿入モードで `Backspace` の動作が制限されることがあります
- `scrolloff` は画面端に到達する前にスクロールを始めるので、周辺のコードが常に見えます

</details>

<details>
<summary>ステップ5：ビープ音の無効化</summary>

```vim
" --- ビープ音の無効化 ---
set belloff=all
```

`belloff=all` はすべてのビープ音を無効化します。視覚ベル（`visualbell`）に切り替える方法もあります。

```vim
" 視覚ベルを使う場合（画面がフラッシュする）
" set visualbell
" set t_vb=
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```vim
" ===========================================
" My First vimrc
" ===========================================

" --- 基本設定 ---
set nocompatible
set encoding=utf-8
set fileencoding=utf-8

" --- 表示設定 ---
set number
set cursorline
set showmatch
set laststatus=2
set ruler

" --- 操作性 ---
set backspace=indent,eol,start
set whichwrap=b,s,h,l,<,>,[,]
set scrolloff=5

" --- ビープ音の無効化 ---
set belloff=all
```

</details>

<details>
<summary>解答例（改良版：より詳細なコメント付き）</summary>

```vim
" ===========================================
" My First vimrc - 改良版
" 作成日: 2024-XX-XX
" ===========================================

" ------------------------------------------
" 基本設定
" ------------------------------------------
" Vi互換モードを無効にしてVimの全機能を使えるようにする
set nocompatible

" 文字エンコーディング
set encoding=utf-8        " Vim内部で使用するエンコーディング
set fileencoding=utf-8    " ファイル保存時のエンコーディング
set fileencodings=utf-8,cp932,euc-jp  " 読み込み時の自動判定順序

" ------------------------------------------
" 表示設定
" ------------------------------------------
set number                " 行番号を表示する
set cursorline            " カーソル行をハイライトする
set showmatch             " 対応する括弧を強調表示する
set matchtime=1           " showmatchの表示時間（0.1秒単位）
set laststatus=2          " ステータスラインを常に表示する
set ruler                 " カーソル位置情報を表示する
set title                 " ウィンドウタイトルにファイル名を表示
set showcmd               " 入力中のコマンドを右下に表示
set cmdheight=2           " コマンドラインの高さを2行に

" ------------------------------------------
" 操作性
" ------------------------------------------
set backspace=indent,eol,start  " BSキーの挙動を直感的にする
set whichwrap=b,s,h,l,<,>,[,]  " 行末から次の行頭へ移動可能に
set scrolloff=5                 " スクロール時に上下5行の余白を確保
set sidescrolloff=10            " 横スクロール時にも余白を確保
set mouse=a                     " マウス操作を有効にする

" ------------------------------------------
" その他
" ------------------------------------------
set belloff=all           " すべてのビープ音を無効化
set history=200           " コマンド履歴を200件保持
set confirm               " 未保存時に確認ダイアログを表示
```

**初心者向けとの違い**:

- `fileencodings` で日本語ファイル（cp932, euc-jp）の自動判定を追加
- `matchtime` で括弧ハイライトの表示時間を短く設定
- `title`, `showcmd`, `cmdheight` で情報表示を強化
- `sidescrolloff`, `mouse` で操作性をさらに向上
- `history`, `confirm` で作業の安全性を向上

</details>

---

## よくある間違い

| ミス | 正しい書き方 | 説明 |
|------|-------------|------|
| `set nonumber` と書くつもりで `set no number` | `set nonumber`（スペースなし） | `no` プレフィックスはオプション名と直結 |
| `set encoding utf-8` | `set encoding=utf-8` | 値の設定には `=` が必要 |
| `# コメント` | `" コメント` | Vimのコメントは `"` で始める |
| `set backspace=all` | `set backspace=indent,eol,start` | `all` は無効な値 |
