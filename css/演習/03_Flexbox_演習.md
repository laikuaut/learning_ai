# 第3章：Flexbox ─ 演習問題

各問題には「ヒント」と「解答例」が用意されています。まずは自分で考えてから確認しましょう。

---

## 基本レベル（問題1〜4）

### 問題1：要素を横に並べる

以下のHTMLで、3つのボックスを横に並べてください。

```html
<div class="container">
  <div class="box">A</div>
  <div class="box">B</div>
  <div class="box">C</div>
</div>
```

**要件：**
- `.container`：Flexboxを有効にする
- `.box`：幅 `100px`、高さ `100px`、背景色 `#3498db`、文字色 白、テキスト中央揃え、行の高さ `100px`（垂直中央揃え用）

<details>
<summary>ヒント</summary>

- 親要素に `display: flex` を指定するだけで子要素は横に並びます
- `line-height` を `height` と同じ値にすると、1行のテキストが垂直中央に揃います
</details>

<details>
<summary>解答例</summary>

```css
.container {
  display: flex;
}

.box {
  width: 100px;
  height: 100px;
  background-color: #3498db;
  color: white;
  text-align: center;
  line-height: 100px;
}
```
</details>

---

### 問題2：要素を中央に配置する

以下のHTMLで、ボックスを画面の上下左右の中央に配置してください。

```html
<div class="center-container">
  <div class="center-box">中央</div>
</div>
```

**要件：**
- `.center-container`：画面の高さいっぱい（`100vh`）、Flexboxで上下左右の中央揃え
- `.center-box`：幅 `200px`、高さ `200px`、背景色 `#e74c3c`、文字色 白、テキスト中央揃え、行の高さ `200px`、角丸 `12px`

<details>
<summary>ヒント</summary>

- 水平中央：`justify-content: center`
- 垂直中央：`align-items: center`
- 画面全体の高さ：`height: 100vh`
</details>

<details>
<summary>解答例</summary>

```css
.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.center-box {
  width: 200px;
  height: 200px;
  background-color: #e74c3c;
  color: white;
  text-align: center;
  line-height: 200px;
  border-radius: 12px;
}
```
</details>

---

### 問題3：justify-contentの各値を試す

以下のHTMLに対して、指定された配置をそれぞれ実現してください。

```html
<div class="row row-start">
  <div class="item">1</div><div class="item">2</div><div class="item">3</div>
</div>
<div class="row row-center">
  <div class="item">1</div><div class="item">2</div><div class="item">3</div>
</div>
<div class="row row-between">
  <div class="item">1</div><div class="item">2</div><div class="item">3</div>
</div>
<div class="row row-evenly">
  <div class="item">1</div><div class="item">2</div><div class="item">3</div>
</div>
```

**要件：**
- `.row` 共通：`display: flex`、padding `8px`、背景色 `#ecf0f1`、margin-bottom `8px`
- `.item` 共通：幅 `60px`、高さ `60px`、背景色 `#2ecc71`、文字色 白、テキスト中央揃え、行の高さ `60px`、角丸 `4px`
- `.row-start`：先頭に寄せる
- `.row-center`：中央に寄せる
- `.row-between`：両端に寄せて間を均等に
- `.row-evenly`：すべての間隔を均等に

<details>
<summary>ヒント</summary>

- `flex-start` / `center` / `space-between` / `space-evenly` を使い分けます
</details>

<details>
<summary>解答例</summary>

```css
.row {
  display: flex;
  padding: 8px;
  background-color: #ecf0f1;
  margin-bottom: 8px;
}

.item {
  width: 60px;
  height: 60px;
  background-color: #2ecc71;
  color: white;
  text-align: center;
  line-height: 60px;
  border-radius: 4px;
}

.row-start {
  justify-content: flex-start;
}

.row-center {
  justify-content: center;
}

.row-between {
  justify-content: space-between;
}

.row-evenly {
  justify-content: space-evenly;
}
```
</details>

---

### 問題4：gapで間隔を付ける

以下のHTMLで、アイテム間に均等な間隔を付けてください。

```html
<div class="tag-list">
  <span class="tag">HTML</span>
  <span class="tag">CSS</span>
  <span class="tag">JavaScript</span>
  <span class="tag">React</span>
  <span class="tag">Node.js</span>
</div>
```

**要件：**
- `.tag-list`：Flexbox、折り返しあり、間隔 `8px`
- `.tag`：背景色 `#e8f4fd`、文字色 `#2980b9`、padding `6px 14px`、角丸 `20px`、文字サイズ `14px`

<details>
<summary>ヒント</summary>

- `flex-wrap: wrap` で折り返し
- `gap: 8px` でアイテム間の余白を設定
</details>

<details>
<summary>解答例</summary>

```css
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background-color: #e8f4fd;
  color: #2980b9;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 14px;
}
```
</details>

---

## 応用レベル（問題5〜7）

### 問題5：ナビゲーションバーを作る

以下のHTMLで、ロゴを左、リンクを右に配置するナビゲーションバーを作ってください。

```html
<nav class="navbar">
  <div class="logo">MyApp</div>
  <div class="nav-links">
    <a href="#" class="nav-link">ホーム</a>
    <a href="#" class="nav-link">機能</a>
    <a href="#" class="nav-link">料金</a>
    <a href="#" class="nav-link">お問い合わせ</a>
  </div>
</nav>
```

**完成イメージ：**
```
┌────────────────────────────────────────────────┐
│ MyApp                    ホーム 機能 料金 お問い合わせ │
└────────────────────────────────────────────────┘
```

**要件：**
- `.navbar`：Flexbox、`space-between` で両端配置、垂直中央揃え、padding `12px 24px`、背景色 `#2c3e50`
- `.logo`：文字色 白、文字サイズ `20px`、太字
- `.nav-links`：Flexbox、間隔 `20px`
- `.nav-link`：文字色 `#ecf0f1`、下線なし、文字サイズ `15px`

<details>
<summary>ヒント</summary>

- 親の `.navbar` に `justify-content: space-between` でロゴとリンクが左右に分かれます
- `.nav-links` も `display: flex` にして、リンクを横に並べます
- `align-items: center` で垂直中央揃え
</details>

<details>
<summary>解答例</summary>

```css
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background-color: #2c3e50;
}

.logo {
  color: white;
  font-size: 20px;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: #ecf0f1;
  text-decoration: none;
  font-size: 15px;
}
```
</details>

---

### 問題6：サイドバー + メインコンテンツのレイアウト

以下のHTMLで、サイドバーとメインコンテンツを横に並べてください。

```html
<div class="layout">
  <aside class="sidebar">
    <h3>メニュー</h3>
    <ul>
      <li>ダッシュボード</li>
      <li>プロフィール</li>
      <li>設定</li>
    </ul>
  </aside>
  <main class="main">
    <h1>メインコンテンツ</h1>
    <p>ここにメインの内容が表示されます。サイドバーは固定幅で、メインコンテンツは残りの幅をすべて使います。</p>
  </main>
</div>
```

**要件：**
- `.layout`：Flexbox、間隔 `24px`、最小高さ `100vh`
- `.sidebar`：幅 `250px` 固定（伸びない、縮まない）、背景色 `#34495e`、文字色 白、padding `20px`
- `.main`：残りのスペースをすべて使う、padding `20px`

<details>
<summary>ヒント</summary>

- サイドバーの固定幅は `flex: 0 0 250px`（伸びない / 縮まない / 250px固定）
- メインの可変幅は `flex: 1`（残りを全部使う）
</details>

<details>
<summary>解答例</summary>

```css
.layout {
  display: flex;
  gap: 24px;
  min-height: 100vh;
}

.sidebar {
  flex: 0 0 250px;
  background-color: #34495e;
  color: white;
  padding: 20px;
}

.main {
  flex: 1;
  padding: 20px;
}
```
</details>

---

### 問題7：カードを均等に並べる

以下のHTMLで、カードを折り返しながら均等に並べてください。

```html
<div class="card-grid">
  <div class="card">カード1</div>
  <div class="card">カード2</div>
  <div class="card">カード3</div>
  <div class="card">カード4</div>
  <div class="card">カード5</div>
  <div class="card">カード6</div>
</div>
```

**要件：**
- `.card-grid`：Flexbox、折り返しあり、間隔 `16px`
- `.card`：最小幅 `250px` で余りスペースを均等に分け合う、padding `24px`、背景色 白、枠線 `1px solid #ddd`、角丸 `8px`

**完成イメージ（画面が広い場合）：**
```
┌──────────┐ ┌──────────┐ ┌──────────┐
│ カード1    │ │ カード2    │ │ カード3    │
└──────────┘ └──────────┘ └──────────┘
┌──────────┐ ┌──────────┐ ┌──────────┐
│ カード4    │ │ カード5    │ │ カード6    │
└──────────┘ └──────────┘ └──────────┘
```

<details>
<summary>ヒント</summary>

- `flex: 1 1 250px` は「最小250px、余ったスペースを均等に分け合う」という意味
- `flex-wrap: wrap` で折り返し
</details>

<details>
<summary>解答例</summary>

```css
.card-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.card {
  flex: 1 1 250px;
  padding: 24px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 8px;
}
```
</details>

---

## チャレンジレベル（問題8〜10）

### 問題8：フッターを画面下部に固定する

コンテンツが少なくても、フッターを常に画面の下部に表示されるようにしてください。

```html
<body>
  <header class="header">ヘッダー</header>
  <main class="content">
    <p>コンテンツが少ないページです。</p>
  </main>
  <footer class="footer">フッター</footer>
</body>
```

**要件：**
- `body`：Flexboxを使って縦方向に並べる、最小高さ `100vh`、margin `0`
- `.header`：背景色 `#2c3e50`、文字色 白、padding `16px`
- `.content`：残りのスペースをすべて使う、padding `24px`
- `.footer`：背景色 `#2c3e50`、文字色 白、padding `16px`、テキスト中央揃え

<details>
<summary>ヒント</summary>

- `body` に `display: flex` と `flex-direction: column` を指定
- `min-height: 100vh` で画面の高さいっぱいに
- `.content` に `flex: 1` で余ったスペースを埋めると、フッターが押し下げられます
</details>

<details>
<summary>解答例</summary>

```css
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin: 0;
}

.header {
  background-color: #2c3e50;
  color: white;
  padding: 16px;
}

.content {
  flex: 1;
  padding: 24px;
}

.footer {
  background-color: #2c3e50;
  color: white;
  padding: 16px;
  text-align: center;
}
```
</details>

---

### 問題9：複雑なカードレイアウト

以下のHTMLで、画像とテキストが横に並ぶカードを作ってください。

```html
<div class="article-card">
  <div class="article-image"></div>
  <div class="article-body">
    <span class="article-category">テクノロジー</span>
    <h2 class="article-title">FlexboxでWebレイアウトが劇的に変わる</h2>
    <p class="article-excerpt">Flexboxを使えば、従来のfloatベースのレイアウトよりも簡単に、柔軟なデザインが実現できます。</p>
    <div class="article-footer">
      <span class="article-author">山田太郎</span>
      <span class="article-date">2026年3月24日</span>
    </div>
  </div>
</div>
```

**完成イメージ：**
```
┌────────────┬──────────────────────────────┐
│            │ テクノロジー                    │
│            │                              │
│   [画像]   │ Flexboxで Webレイアウトが       │
│            │ 劇的に変わる                    │
│            │                              │
│            │ Flexboxを使えば...             │
│            │                              │
│            │ 山田太郎          2026年3月24日  │
└────────────┴──────────────────────────────┘
```

**要件：**
- `.article-card`：Flexbox、最大幅 `700px`、背景色 白、枠線 `1px solid #e0e0e0`、角丸 `12px`、overflow hidden
- `.article-image`：幅 `200px` 固定（伸びない / 縮まない）、最小高さ `200px`、背景色 `#bdc3c7`
- `.article-body`：`flex: 1`、padding `20px`、Flexboxで縦方向に並べる
- `.article-category`：背景色 `#e74c3c`、文字色 白、padding `4px 10px`、角丸 `4px`、文字サイズ `12px`、太字、`align-self: flex-start`
- `.article-title`：文字サイズ `18px`、色 `#2c3e50`、margin上 `12px` 下 `8px`
- `.article-excerpt`：文字サイズ `14px`、色 `#666`、行の高さ `1.6`、`flex: 1`（残りのスペースを埋める）
- `.article-footer`：Flexbox、`space-between`、文字サイズ `13px`、色 `#999`

<details>
<summary>ヒント</summary>

- `.article-card` は横方向のFlex（デフォルト）
- `.article-body` は縦方向のFlex（`flex-direction: column`）
- `.article-excerpt` に `flex: 1` を使うと、日付のフッターが下に押される
- `align-self: flex-start` でカテゴリタグの幅をコンテンツ幅だけにする
</details>

<details>
<summary>解答例</summary>

```css
*, *::before, *::after {
  box-sizing: border-box;
}

.article-card {
  display: flex;
  max-width: 700px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
}

.article-image {
  flex: 0 0 200px;
  min-height: 200px;
  background-color: #bdc3c7;
}

.article-body {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.article-category {
  background-color: #e74c3c;
  color: white;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  align-self: flex-start;
}

.article-title {
  font-size: 18px;
  color: #2c3e50;
  margin-top: 12px;
  margin-bottom: 8px;
}

.article-excerpt {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  flex: 1;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #999;
}
```
</details>

---

### 問題10：ミニプロジェクト ─ ツールバーを作る

以下の見た目のツールバーを作成してください。

**完成イメージ：**
```
┌──────────────────────────────────────────────────────────┐
│ [ロゴ]  ホーム  探す  通知    〈─ 伸びるスペース ─〉   [検索]  [設定] │
└──────────────────────────────────────────────────────────┘
```

左側にロゴとナビリンク、右側にアクションボタンが配置されます。

```html
<div class="toolbar">
  <div class="toolbar-left">
    <span class="toolbar-logo">Logo</span>
    <a href="#" class="toolbar-link">ホーム</a>
    <a href="#" class="toolbar-link">探す</a>
    <a href="#" class="toolbar-link">通知</a>
  </div>
  <div class="toolbar-spacer"></div>
  <div class="toolbar-right">
    <button class="toolbar-btn">検索</button>
    <button class="toolbar-btn toolbar-btn-primary">設定</button>
  </div>
</div>
```

**要件：**
- `.toolbar`：Flexbox、垂直中央揃え、padding `8px 16px`、背景色 `#1a1a2e`、gap `8px`
- `.toolbar-left`：Flexbox、垂直中央揃え、gap `16px`
- `.toolbar-logo`：文字色 `#e94560`、文字サイズ `20px`、太字
- `.toolbar-link`：文字色 `#eee`、下線なし、文字サイズ `14px`
- `.toolbar-spacer`：`flex: 1`（残りスペースを全部埋める）
- `.toolbar-right`：Flexbox、gap `8px`
- `.toolbar-btn`：背景色 `transparent`、文字色 `#eee`、枠線 `1px solid #555`、padding `6px 16px`、角丸 `4px`、文字サイズ `14px`、cursor pointer
- `.toolbar-btn-primary`：背景色 `#e94560`、枠線色も `#e94560`

<details>
<summary>ヒント</summary>

- `.toolbar-spacer` に `flex: 1` を使うと、左側と右側の間にある空きスペースをすべて埋めます
- これにより左のグループと右のグループが自然に離れます
- ボタンの `cursor: pointer` はマウスホバー時に指カーソルにする設定です
</details>

<details>
<summary>解答例</summary>

```css
*, *::before, *::after {
  box-sizing: border-box;
}

.toolbar {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  background-color: #1a1a2e;
  gap: 8px;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.toolbar-logo {
  color: #e94560;
  font-size: 20px;
  font-weight: bold;
}

.toolbar-link {
  color: #eee;
  text-decoration: none;
  font-size: 14px;
}

.toolbar-spacer {
  flex: 1;
}

.toolbar-right {
  display: flex;
  gap: 8px;
}

.toolbar-btn {
  background-color: transparent;
  color: #eee;
  border: 1px solid #555;
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.toolbar-btn-primary {
  background-color: #e94560;
  border-color: #e94560;
}
```
</details>

---

## 振り返り

| レベル | 問題 | 学んだこと |
|--------|------|-----------|
| 基本 | 1 | display: flex で横並び |
| 基本 | 2 | 上下左右の中央揃え |
| 基本 | 3 | justify-content の各値 |
| 基本 | 4 | flex-wrap と gap |
| 応用 | 5 | space-between でナビバー |
| 応用 | 6 | サイドバー＋メインの2カラムレイアウト |
| 応用 | 7 | flex-wrap でカードグリッド |
| チャレンジ | 8 | flex-direction: column でフッター固定 |
| チャレンジ | 9 | ネストされたFlexboxでカードレイアウト |
| チャレンジ | 10 | スペーサーを使ったツールバー |
