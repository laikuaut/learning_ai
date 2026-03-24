# 第1章：CSSの基本 ─ 演習問題

各問題には「ヒント」と「解答例」が用意されています。まずは自分で考えてから確認しましょう。

---

## 基本レベル（問題1〜4）

### 問題1：文字色と背景色を変える

以下のHTMLに対して、CSSを書いてください。

```html
<h1>こんにちは、CSS！</h1>
<p>CSSで見た目を変えてみましょう。</p>
```

**要件：**
- `<h1>` の文字色を `#2c3e50`（紺色）にする
- `<p>` の文字色を `#666666`（グレー）にする
- `<body>` の背景色を `#f5f5f5`（薄いグレー）にする

<details>
<summary>ヒント</summary>

- 文字色は `color` プロパティ
- 背景色は `background-color` プロパティ
- 要素セレクタ（タグ名）で指定します
</details>

<details>
<summary>解答例</summary>

```css
body {
  background-color: #f5f5f5;
}

h1 {
  color: #2c3e50;
}

p {
  color: #666666;
}
```
</details>

---

### 問題2：クラスセレクタを使ってスタイルを適用する

以下のHTMLに対して、指定されたスタイルを適用してください。

```html
<p class="important">この文章は重要です。</p>
<p>この文章は普通です。</p>
<p class="important">この文章も重要です。</p>
<p class="note">これは補足情報です。</p>
```

**要件：**
- `.important` クラス → 文字色を赤（`red`）、太字にする
- `.note` クラス → 文字色を `#888`、文字サイズを `14px`、イタリック体にする

<details>
<summary>ヒント</summary>

- 太字は `font-weight: bold;`
- イタリック体は `font-style: italic;`
- クラスセレクタは `.クラス名` で書きます
</details>

<details>
<summary>解答例</summary>

```css
.important {
  color: red;
  font-weight: bold;
}

.note {
  color: #888;
  font-size: 14px;
  font-style: italic;
}
```
</details>

---

### 問題3：リンクのスタイルを変更する

以下のHTMLのリンクにスタイルを適用してください。

```html
<nav>
  <a href="#">ホーム</a>
  <a href="#">サービス</a>
  <a href="#">お問い合わせ</a>
</nav>
```

**要件：**
- リンクの下線を消す
- 文字色を `#3498db`（青）にする
- 文字サイズを `18px` にする

<details>
<summary>ヒント</summary>

- 下線を消すには `text-decoration: none;`
- `nav` の中の `a` を対象にするには子孫セレクタ `nav a` を使います
</details>

<details>
<summary>解答例</summary>

```css
nav a {
  text-decoration: none;
  color: #3498db;
  font-size: 18px;
}
```
</details>

---

### 問題4：CSS変数を定義して使う

以下の要件に従い、CSS変数を使ってスタイルを書いてください。

```html
<h1>サイトのタイトル</h1>
<p>本文テキストがここに入ります。</p>
<a href="#">リンクテキスト</a>
```

**要件：**
- `:root` にCSS変数を定義する
  - `--primary-color`: `#e74c3c`（赤系）
  - `--text-color`: `#333333`
  - `--font-size-large`: `28px`
- `<h1>` に `--primary-color` と `--font-size-large` を適用
- `<p>` に `--text-color` を適用
- `<a>` に `--primary-color` を適用

<details>
<summary>ヒント</summary>

- CSS変数は `:root { --変数名: 値; }` で定義
- 使う時は `var(--変数名)` で参照
</details>

<details>
<summary>解答例</summary>

```css
:root {
  --primary-color: #e74c3c;
  --text-color: #333333;
  --font-size-large: 28px;
}

h1 {
  color: var(--primary-color);
  font-size: var(--font-size-large);
}

p {
  color: var(--text-color);
}

a {
  color: var(--primary-color);
}
```
</details>

---

## 応用レベル（問題5〜7）

### 問題5：複数のセレクタを組み合わせる

以下のHTMLに対して、指定のスタイルを適用してください。

```html
<header>
  <h1>サイトタイトル</h1>
  <p class="subtitle">サブタイトルです</p>
</header>
<main>
  <h2>セクション1</h2>
  <p>本文テキスト</p>
  <h2>セクション2</h2>
  <p class="highlight">重要なテキスト</p>
</main>
```

**要件：**
1. すべての `<h1>`, `<h2>` をまとめて `font-family: sans-serif` にする（グループセレクタ）
2. `header` 内の `<h1>` だけ文字色を白、背景色を `#2c3e50` にする（子孫セレクタ）
3. `header` 全体の背景色を `#2c3e50` にし、padding を `20px` にする
4. `.subtitle` の文字色を `#bdc3c7`（薄いグレー）にする
5. `main` 内の `.highlight` の背景色を `#ffffcc`（薄い黄色）にし、padding を `8px` にする

<details>
<summary>ヒント</summary>

- グループセレクタ：`h1, h2 { ... }`
- 子孫セレクタ：`header h1 { ... }`
- 組み合わせ：`main .highlight { ... }`
</details>

<details>
<summary>解答例</summary>

```css
h1, h2 {
  font-family: sans-serif;
}

header {
  background-color: #2c3e50;
  padding: 20px;
}

header h1 {
  color: white;
}

.subtitle {
  color: #bdc3c7;
}

main .highlight {
  background-color: #ffffcc;
  padding: 8px;
}
```
</details>

---

### 問題6：さまざまな色指定を使い分ける

以下のHTMLに対して、**指定された色形式で**スタイルを書いてください。

```html
<div class="box box-1">HEX指定</div>
<div class="box box-2">RGB指定</div>
<div class="box box-3">RGBA指定</div>
<div class="box box-4">HSL指定</div>
```

**要件：**
- `.box` 共通：padding `16px`、margin-bottom `8px`、文字色 白、border-radius `4px`
- `.box-1`：背景色を **HEX** で `#e74c3c` に
- `.box-2`：背景色を **RGB** で `rgb(46, 204, 113)` に
- `.box-3`：背景色を **RGBA** で `rgba(52, 152, 219, 0.7)` に
- `.box-4`：背景色を **HSL** で `hsl(280, 60%, 50%)` に

<details>
<summary>ヒント</summary>

- 共通スタイルは `.box` に書き、個別の色は `.box-1` 等に書きます
- HEX: `#RRGGBB`、RGB: `rgb(R, G, B)`、RGBA: `rgba(R, G, B, A)`、HSL: `hsl(H, S%, L%)`
</details>

<details>
<summary>解答例</summary>

```css
.box {
  padding: 16px;
  margin-bottom: 8px;
  color: white;
  border-radius: 4px;
}

.box-1 {
  background-color: #e74c3c;
}

.box-2 {
  background-color: rgb(46, 204, 113);
}

.box-3 {
  background-color: rgba(52, 152, 219, 0.7);
}

.box-4 {
  background-color: hsl(280, 60%, 50%);
}
```
</details>

---

### 問題7：外部スタイルシートの構成を考える

以下のHTMLファイルに対して、外部CSSファイル（`style.css`）を作成してください。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="style.css">
  <title>プロフィールページ</title>
</head>
<body>
  <div class="profile-card">
    <h1 class="name">山田太郎</h1>
    <p class="job">Webデベロッパー</p>
    <p class="bio">東京在住。Webサイト制作が好きです。趣味は読書とカフェ巡り。</p>
    <div class="links">
      <a href="#" class="link">Twitter</a>
      <a href="#" class="link">GitHub</a>
      <a href="#" class="link">Portfolio</a>
    </div>
  </div>
</body>
</html>
```

**要件：**
- `body`：背景色 `#ecf0f1`、フォント `sans-serif`
- `.profile-card`：背景色 白、padding `32px`、最大幅 `400px`、中央揃え（`margin: 40px auto`）、角丸 `12px`、影 `box-shadow: 0 2px 8px rgba(0,0,0,0.1)`
- `.name`：文字サイズ `24px`、色 `#2c3e50`、下余白（margin-bottom）`4px`
- `.job`：文字色 `#7f8c8d`、文字サイズ `14px`、上余白 `0`
- `.bio`：行の高さ `1.8`、文字色 `#555`
- `.link`：文字色 `#3498db`、下線なし、右余白（margin-right）`12px`

<details>
<summary>ヒント</summary>

- 中央揃えは `margin: 40px auto` で実現（左右がautoで中央になる）
- `box-shadow` は `水平 垂直 ぼかし 色` の順で指定
- `max-width` を使うと、画面が小さくなっても対応できます
</details>

<details>
<summary>解答例</summary>

```css
body {
  background-color: #ecf0f1;
  font-family: sans-serif;
}

.profile-card {
  background-color: white;
  padding: 32px;
  max-width: 400px;
  margin: 40px auto;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.name {
  font-size: 24px;
  color: #2c3e50;
  margin-bottom: 4px;
}

.job {
  color: #7f8c8d;
  font-size: 14px;
  margin-top: 0;
}

.bio {
  line-height: 1.8;
  color: #555;
}

.link {
  color: #3498db;
  text-decoration: none;
  margin-right: 12px;
}
```
</details>

---

## チャレンジレベル（問題8〜10）

### 問題8：CSSの優先順位を理解する

以下のHTMLとCSSが与えられたとき、各段落の文字色が何色になるか答えてください。

```html
<p id="special" class="highlight">テキストA</p>
<p class="highlight">テキストB</p>
<p style="color: purple;">テキストC</p>
<p class="highlight note">テキストD</p>
```

```css
p { color: black; }
.highlight { color: blue; }
.note { color: green; }
#special { color: red; }
```

**問い：** テキストA〜Dそれぞれの文字色は？

<details>
<summary>ヒント</summary>

優先順位（低→高）：
1. 要素セレクタ（`p`）
2. クラスセレクタ（`.highlight`, `.note`）
3. IDセレクタ（`#special`）
4. インラインスタイル（`style="..."`）

同じ優先度の場合は、後に書かれた方が適用されます。
</details>

<details>
<summary>解答例</summary>

| テキスト | 文字色 | 理由 |
|---------|--------|------|
| A | **赤（red）** | IDセレクタ `#special` が最も優先度が高い |
| B | **青（blue）** | クラス `.highlight` が要素セレクタ `p` より優先 |
| C | **紫（purple）** | インラインスタイルが最も優先度が高い |
| D | **緑（green）** | `.highlight` と `.note` は同じ優先度だが、`.note` の方がCSSで後に書かれている |
</details>

---

### 問題9：テーマ切り替え用のCSS変数設計

CSS変数を使って、「ライトテーマ」と「ダークテーマ」の2種類のスタイルを設計してください。

```html
<body class="light-theme">
  <div class="container">
    <h1>テーマ切り替え</h1>
    <p>CSS変数でテーマを管理します。</p>
    <a href="#">リンクテキスト</a>
  </div>
</body>
```

**要件：**
- `.light-theme` で以下の変数を定義：
  - `--bg-color`: `#ffffff`
  - `--text-color`: `#333333`
  - `--link-color`: `#3498db`
  - `--border-color`: `#dddddd`
- `.dark-theme` で以下の変数を定義：
  - `--bg-color`: `#1a1a2e`
  - `--text-color`: `#e0e0e0`
  - `--link-color`: `#64b5f6`
  - `--border-color`: `#444444`
- `.container`, `h1`, `p`, `a` のスタイルではすべて変数（`var()`）を使用する
- `.container`：背景色 `--bg-color`、border `1px solid var(--border-color)`、padding `24px`、最大幅 `600px`、中央揃え、角丸 `8px`

<details>
<summary>ヒント</summary>

- bodyのクラスを `light-theme` から `dark-theme` に変えるだけでテーマが変わる設計にします
- 各要素のスタイルでは色を直接指定せず、必ず `var(--変数名)` を使います
</details>

<details>
<summary>解答例</summary>

```css
.light-theme {
  --bg-color: #ffffff;
  --text-color: #333333;
  --link-color: #3498db;
  --border-color: #dddddd;
}

.dark-theme {
  --bg-color: #1a1a2e;
  --text-color: #e0e0e0;
  --link-color: #64b5f6;
  --border-color: #444444;
}

body {
  background-color: var(--bg-color);
  color: var(--text-color);
  font-family: sans-serif;
  margin: 0;
  padding: 20px;
}

.container {
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  padding: 24px;
  max-width: 600px;
  margin: 0 auto;
  border-radius: 8px;
}

h1 {
  color: var(--text-color);
}

p {
  color: var(--text-color);
  line-height: 1.6;
}

a {
  color: var(--link-color);
  text-decoration: none;
}
```

> bodyのクラスを `dark-theme` に変更するだけで、すべての色が切り替わります。
</details>

---

### 問題10：ミニプロジェクト ─ お知らせバナーを作る

以下の見た目のお知らせバナーをCSSで作成してください。

**完成イメージ：**
```
┌──────────────────────────────────────────────┐
│ ⚠ 重要なお知らせ                               │
│                                              │
│ システムメンテナンスのため、3月30日 0:00〜6:00 は    │
│ サービスを一時停止いたします。                      │
│                                              │
│                          [詳しくはこちら]        │
└──────────────────────────────────────────────┘
```

```html
<div class="notice">
  <h3 class="notice-title">⚠ 重要なお知らせ</h3>
  <p class="notice-text">
    システムメンテナンスのため、3月30日 0:00〜6:00 はサービスを一時停止いたします。
  </p>
  <div class="notice-action">
    <a href="#" class="notice-link">詳しくはこちら</a>
  </div>
</div>
```

**要件：**
- `.notice`：背景色 `#fff3cd`、枠線 左だけ `4px solid #ffc107`、padding `20px`、角丸 `4px`、最大幅 `600px`、影（`box-shadow: 0 1px 4px rgba(0,0,0,0.1)`）
- `.notice-title`：文字色 `#856404`、文字サイズ `18px`、余白 上は0 下は8px
- `.notice-text`：文字色 `#856404`、行の高さ `1.6`、余白 下は12px
- `.notice-action`：テキストを右揃え
- `.notice-link`：文字色 `#856404`、太字、下線あり

<details>
<summary>ヒント</summary>

- 左だけ枠線を付けるには `border-left: 4px solid #ffc107;`
- 他の枠線は `border: none;` で消すか、`border-left` だけ指定すればOK
- 右揃えは `text-align: right;`
</details>

<details>
<summary>解答例</summary>

```css
.notice {
  background-color: #fff3cd;
  border: none;
  border-left: 4px solid #ffc107;
  padding: 20px;
  border-radius: 4px;
  max-width: 600px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.notice-title {
  color: #856404;
  font-size: 18px;
  margin-top: 0;
  margin-bottom: 8px;
}

.notice-text {
  color: #856404;
  line-height: 1.6;
  margin-bottom: 12px;
}

.notice-action {
  text-align: right;
}

.notice-link {
  color: #856404;
  font-weight: bold;
  text-decoration: underline;
}
```
</details>

---

## 振り返り

| レベル | 問題 | 学んだこと |
|--------|------|-----------|
| 基本 | 1 | 文字色・背景色の指定 |
| 基本 | 2 | クラスセレクタ |
| 基本 | 3 | 子孫セレクタ、テキスト装飾 |
| 基本 | 4 | CSS変数（カスタムプロパティ） |
| 応用 | 5 | 複数セレクタの組み合わせ |
| 応用 | 6 | 色の指定方法（HEX / RGB / RGBA / HSL） |
| 応用 | 7 | 実践的なプロフィールカード |
| チャレンジ | 8 | CSSの優先順位（カスケード） |
| チャレンジ | 9 | CSS変数によるテーマ設計 |
| チャレンジ | 10 | 総合的なコンポーネント制作 |
