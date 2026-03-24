# 第4章：CSS Grid ─ 演習問題

各問題には「ヒント」と「解答例」が用意されています。まずは自分で考えてから確認しましょう。

---

## 基本レベル（問題1〜3）

### 問題1：基本的なグリッドを作る

以下のHTMLで、3列のグリッドを作成してください。

```html
<div class="grid">
  <div class="cell">1</div>
  <div class="cell">2</div>
  <div class="cell">3</div>
  <div class="cell">4</div>
  <div class="cell">5</div>
  <div class="cell">6</div>
</div>
```

**完成イメージ：**
```
┌────────┐ ┌────────┐ ┌────────┐
│   1    │ │   2    │ │   3    │
└────────┘ └────────┘ └────────┘
┌────────┐ ┌────────┐ ┌────────┐
│   4    │ │   5    │ │   6    │
└────────┘ └────────┘ └────────┘
```

**要件：**
- `.grid`：Gridレイアウト、3列の均等幅、間隔 `16px`
- `.cell`：背景色 `#3498db`、文字色 白、padding `24px`、テキスト中央揃え、角丸 `8px`

<details>
<summary>ヒント</summary>

- `display: grid` でGridを有効に
- `grid-template-columns: repeat(3, 1fr)` で3列の均等幅
- `gap` で間隔を設定
</details>

<details>
<summary>解答例</summary>

```css
.grid {
  /* Gridレイアウトを有効にする */
  display: grid;
  /* 3列を均等幅（1fr = 1分割）で作成 */
  grid-template-columns: repeat(3, 1fr);
  /* セル間の間隔 */
  gap: 16px;
}

.cell {
  background-color: #3498db;
  color: white;
  padding: 24px;
  text-align: center;
  border-radius: 8px;
}
```
</details>

---

### 問題2：列幅を指定してグリッドを作る

以下のHTMLで、サイドバー＋メインの2カラムレイアウトを作成してください。

```html
<div class="page-layout">
  <aside class="sidebar">サイドバー</aside>
  <main class="main-content">メインコンテンツ</main>
</div>
```

**完成イメージ：**
```
┌──────────┬─────────────────────────────┐
│          │                             │
│ サイド    │      メインコンテンツ         │
│ バー     │                             │
│          │                             │
└──────────┴─────────────────────────────┘
  250px            残りすべて
```

**要件：**
- `.page-layout`：Gridレイアウト、左列 `250px` 固定・右列は残り全部、間隔 `24px`、最小高さ `100vh`
- `.sidebar`：背景色 `#2c3e50`、文字色 白、padding `20px`
- `.main-content`：背景色 `#ecf0f1`、padding `20px`

<details>
<summary>ヒント</summary>

- `grid-template-columns: 250px 1fr` で左を固定幅、右を可変幅に
- `1fr` は残りのスペースをすべて使う単位
</details>

<details>
<summary>解答例</summary>

```css
.page-layout {
  display: grid;
  /* 左列250px固定、右列は残りのスペースすべて */
  grid-template-columns: 250px 1fr;
  gap: 24px;
  min-height: 100vh;
}

.sidebar {
  background-color: #2c3e50;
  color: white;
  padding: 20px;
}

.main-content {
  background-color: #ecf0f1;
  padding: 20px;
}
```
</details>

---

### 問題3：行と列の両方を指定する

以下のHTMLで、2行3列のグリッドを作成してください。

```html
<div class="dashboard">
  <div class="widget">ウィジェット1</div>
  <div class="widget">ウィジェット2</div>
  <div class="widget">ウィジェット3</div>
  <div class="widget">ウィジェット4</div>
  <div class="widget">ウィジェット5</div>
  <div class="widget">ウィジェット6</div>
</div>
```

**要件：**
- `.dashboard`：Gridレイアウト、3列均等幅、行の高さは1行目 `150px`・2行目 `200px`、間隔 `12px`、padding `12px`、背景色 `#f0f0f0`
- `.widget`：背景色 白、padding `16px`、角丸 `8px`、影 `0 2px 4px rgba(0,0,0,0.1)`

<details>
<summary>ヒント</summary>

- `grid-template-rows: 150px 200px` で行の高さを指定
- `grid-template-columns` と `grid-template-rows` を両方使って2次元のレイアウトを定義
</details>

<details>
<summary>解答例</summary>

```css
.dashboard {
  display: grid;
  /* 3列均等幅 */
  grid-template-columns: repeat(3, 1fr);
  /* 1行目150px、2行目200px */
  grid-template-rows: 150px 200px;
  gap: 12px;
  padding: 12px;
  background-color: #f0f0f0;
}

.widget {
  background-color: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```
</details>

---

## 応用レベル（問題4〜6）

### 問題4：グリッドエリアで名前付きレイアウト

以下のHTMLで、`grid-template-areas` を使ってページレイアウトを作成してください。

```html
<div class="page">
  <header class="page-header">ヘッダー</header>
  <nav class="page-nav">ナビゲーション</nav>
  <main class="page-main">メインコンテンツ</main>
  <aside class="page-aside">サイドバー</aside>
  <footer class="page-footer">フッター</footer>
</div>
```

**完成イメージ：**
```
┌──────────────────────────────────────┐
│              ヘッダー                  │
├──────┬──────────────────┬────────────┤
│ ナビ  │    メイン         │  サイド    │
│      │    コンテンツ      │  バー     │
├──────┴──────────────────┴────────────┤
│              フッター                  │
└──────────────────────────────────────┘
```

**要件：**
- `.page`：Gridレイアウト、エリア名を使って配置、間隔 `8px`、最小高さ `100vh`
  - 列: `150px 1fr 200px`
  - 行: `auto 1fr auto`
  - エリア定義:
    - 1行目: `"header header header"`
    - 2行目: `"nav main aside"`
    - 3行目: `"footer footer footer"`
- 各要素に `grid-area` で名前を割り当てる
- `.page-header`：背景色 `#2c3e50`、文字色 白、padding `16px`
- `.page-nav`：背景色 `#34495e`、文字色 白、padding `16px`
- `.page-main`：padding `20px`
- `.page-aside`：背景色 `#ecf0f1`、padding `16px`
- `.page-footer`：背景色 `#2c3e50`、文字色 白、padding `16px`、テキスト中央揃え

<details>
<summary>ヒント</summary>

- `grid-template-areas` は文字列で各行のエリア名を定義
- 各要素に `grid-area: エリア名` を指定して配置
- 同じ名前を繰り返すとその分のセルを結合して占有できる
</details>

<details>
<summary>解答例</summary>

```css
.page {
  display: grid;
  /* 列の幅を定義 */
  grid-template-columns: 150px 1fr 200px;
  /* 行の高さ: ヘッダー自動、メイン部分は残り全部、フッター自動 */
  grid-template-rows: auto 1fr auto;
  /* エリア名でレイアウトを視覚的に定義 */
  grid-template-areas:
    "header header header"
    "nav    main   aside"
    "footer footer footer";
  gap: 8px;
  min-height: 100vh;
}

/* 各要素にエリア名を割り当て */
.page-header { grid-area: header; }
.page-nav    { grid-area: nav; }
.page-main   { grid-area: main; }
.page-aside  { grid-area: aside; }
.page-footer { grid-area: footer; }

.page-header {
  background-color: #2c3e50;
  color: white;
  padding: 16px;
}

.page-nav {
  background-color: #34495e;
  color: white;
  padding: 16px;
}

.page-main {
  padding: 20px;
}

.page-aside {
  background-color: #ecf0f1;
  padding: 16px;
}

.page-footer {
  background-color: #2c3e50;
  color: white;
  padding: 16px;
  text-align: center;
}
```
</details>

---

### 問題5：セルの結合（span）

以下のHTMLで、特定のセルが複数のグリッドセルを占有するレイアウトを作成してください。

```html
<div class="grid-span">
  <div class="item item-featured">注目記事（2列占有）</div>
  <div class="item">記事2</div>
  <div class="item">記事3</div>
  <div class="item item-tall">記事4（2行占有）</div>
  <div class="item">記事5</div>
</div>
```

**完成イメージ：**
```
┌─────────────────────┬────────────┐
│    注目記事           │   記事2    │
│   （2列占有）         │            │
├───────────┬─────────┼────────────┤
│   記事3    │         │   記事5    │
│           │  記事4   │            │
│           │（2行占有）│            │
└───────────┴─────────┴────────────┘
```

**要件：**
- `.grid-span`：Gridレイアウト、3列均等幅、行の高さ `150px`、間隔 `12px`
- `.item`：背景色 `#3498db`、文字色 白、padding `20px`、角丸 `8px`
- `.item-featured`：2列にまたがる、背景色 `#e74c3c`
- `.item-tall`：2行にまたがる、背景色 `#2ecc71`

<details>
<summary>ヒント</summary>

- `grid-column: span 2` で2列にまたがる
- `grid-row: span 2` で2行にまたがる
- `span` キーワードで現在の位置からいくつ占有するか指定
</details>

<details>
<summary>解答例</summary>

```css
.grid-span {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  /* すべての行を150pxに（autoで内容に応じてもOK） */
  grid-auto-rows: 150px;
  gap: 12px;
}

.item {
  background-color: #3498db;
  color: white;
  padding: 20px;
  border-radius: 8px;
}

.item-featured {
  /* 2列にまたがる */
  grid-column: span 2;
  background-color: #e74c3c;
}

.item-tall {
  /* 2行にまたがる */
  grid-row: span 2;
  background-color: #2ecc71;
}
```
</details>

---

### 問題6：auto-fitとminmax()でレスポンシブグリッド

以下のHTMLで、画面幅に応じて列数が自動で変わるカードグリッドを作成してください。

```html
<div class="auto-grid">
  <div class="card">カード1</div>
  <div class="card">カード2</div>
  <div class="card">カード3</div>
  <div class="card">カード4</div>
  <div class="card">カード5</div>
  <div class="card">カード6</div>
  <div class="card">カード7</div>
  <div class="card">カード8</div>
</div>
```

**要件：**
- `.auto-grid`：Gridレイアウト、メディアクエリなしで列数が自動調整される、間隔 `16px`、padding `16px`
- `.card`：最小幅 `250px`、背景色 白、枠線 `1px solid #e0e0e0`、padding `20px`、角丸 `8px`、影 `0 2px 6px rgba(0,0,0,0.08)`

**動作イメージ：**
```
広い画面（4列）:  ┌───┐ ┌───┐ ┌───┐ ┌───┐
                 └───┘ └───┘ └───┘ └───┘

中程度（3列）:    ┌─────┐ ┌─────┐ ┌─────┐
                 └─────┘ └─────┘ └─────┘

狭い画面（1列）:  ┌─────────────────┐
                 └─────────────────┘
```

<details>
<summary>ヒント</summary>

- `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))` がポイント
- `auto-fit` は利用可能なスペースに応じて列数を自動調整
- `minmax(250px, 1fr)` は最小250px、最大は均等分割
</details>

<details>
<summary>解答例</summary>

```css
.auto-grid {
  display: grid;
  /* auto-fit: 列数を自動調整 */
  /* minmax(250px, 1fr): 各列は最小250px、最大は均等に分割 */
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  padding: 16px;
}

.card {
  background-color: white;
  border: 1px solid #e0e0e0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}
```
</details>

---

## チャレンジレベル（問題7〜8）

### 問題7：マガジン風レイアウト

以下のHTMLで、雑誌のようなレイアウトを作成してください。メイン記事が大きく、サブ記事が小さく並びます。

```html
<div class="magazine">
  <article class="article-main">
    <h2>メイン記事</h2>
    <p>これは一番目立つ位置に配置されるメイン記事です。</p>
  </article>
  <article class="article-sub">
    <h3>サブ記事1</h3>
    <p>短い説明テキスト</p>
  </article>
  <article class="article-sub">
    <h3>サブ記事2</h3>
    <p>短い説明テキスト</p>
  </article>
  <article class="article-sub">
    <h3>サブ記事3</h3>
    <p>短い説明テキスト</p>
  </article>
  <article class="article-sub">
    <h3>サブ記事4</h3>
    <p>短い説明テキスト</p>
  </article>
</div>
```

**完成イメージ：**
```
┌──────────────────────┬───────────┐
│                      │  サブ記事1  │
│     メイン記事         ├───────────┤
│    （2行2列占有）      │  サブ記事2  │
│                      │           │
├───────────┬──────────┴───────────┤
│  サブ記事3  │      サブ記事4        │
└───────────┴─────────────────────┘
```

**要件：**
- `.magazine`：Gridレイアウト、3列均等幅、行の高さ `180px`、間隔 `16px`
- `.article-main`：2列2行を占有、背景色 `#2c3e50`、文字色 白、padding `32px`、角丸 `12px`
- `.article-sub`：背景色 白、枠線 `1px solid #ddd`、padding `20px`、角丸 `8px`

<details>
<summary>ヒント</summary>

- `.article-main` に `grid-column: span 2` と `grid-row: span 2` を指定
- 残りの要素は自動配置される
</details>

<details>
<summary>解答例</summary>

```css
.magazine {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 180px;
  gap: 16px;
}

.article-main {
  /* 2列 x 2行を占有 */
  grid-column: span 2;
  grid-row: span 2;
  background-color: #2c3e50;
  color: white;
  padding: 32px;
  border-radius: 12px;
  /* Flexboxを併用して内部のテキスト配置 */
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.article-sub {
  background-color: white;
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
}

.article-main h2 {
  font-size: 24px;
  margin-bottom: 8px;
}

.article-sub h3 {
  font-size: 16px;
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 8px;
}

.article-sub p {
  font-size: 14px;
  color: #666;
  margin: 0;
}
```
</details>

---

### 問題8：ミニプロジェクト ─ ダッシュボードレイアウト

以下のHTMLで、管理画面風のダッシュボードを作成してください。

```html
<div class="dashboard-layout">
  <header class="dash-header">Dashboard</header>
  <nav class="dash-sidebar">
    <a href="#" class="dash-menu-item">概要</a>
    <a href="#" class="dash-menu-item">分析</a>
    <a href="#" class="dash-menu-item">ユーザー</a>
    <a href="#" class="dash-menu-item">設定</a>
  </nav>
  <main class="dash-main">
    <div class="stat-cards">
      <div class="stat-card">
        <div class="stat-number">1,234</div>
        <div class="stat-label">ユーザー数</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">567</div>
        <div class="stat-label">注文数</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">89%</div>
        <div class="stat-label">達成率</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">¥1.2M</div>
        <div class="stat-label">売上</div>
      </div>
    </div>
    <div class="chart-area">
      <p>グラフエリア（ここにチャートが入ります）</p>
    </div>
  </main>
</div>
```

**完成イメージ：**
```
┌──────────────────────────────────────────┐
│              Dashboard（ヘッダー）          │
├────────────┬─────────────────────────────┤
│  概要       │ ┌─────┐┌─────┐┌─────┐┌─────┐│
│  分析       │ │1,234││ 567 ││ 89% ││¥1.2M││
│  ユーザー   │ │ユーザ││注文数││達成率││ 売上 ││
│  設定       │ └─────┘└─────┘└─────┘└─────┘│
│            │ ┌───────────────────────────┐│
│            │ │    グラフエリア             ││
│            │ │                           ││
│            │ └───────────────────────────┘│
└────────────┴─────────────────────────────┘
```

**要件：**
- `.dashboard-layout`：Gridレイアウト、エリア名を使用、最小高さ `100vh`
  - 列: `220px 1fr`
  - 行: `60px 1fr`
  - エリア: `"header header"` / `"sidebar main"`
- `.dash-header`：背景色 `#1a1a2e`、文字色 白、padding `0 24px`、Flexbox で垂直中央揃え、文字サイズ `20px`、太字
- `.dash-sidebar`：背景色 `#16213e`、padding `20px 0`、Flexbox で縦方向に並べる
- `.dash-menu-item`：文字色 `#8892b0`、下線なし、padding `12px 24px`、文字サイズ `14px`
- `.dash-main`：背景色 `#f5f6fa`、padding `24px`
- `.stat-cards`：Gridレイアウト、4列均等幅、間隔 `16px`、margin-bottom `24px`
- `.stat-card`：背景色 白、padding `20px`、角丸 `12px`、影 `0 2px 8px rgba(0,0,0,0.06)`、テキスト中央揃え
- `.stat-number`：文字サイズ `28px`、太字、色 `#2c3e50`
- `.stat-label`：文字サイズ `13px`、色 `#999`、margin-top `4px`
- `.chart-area`：背景色 白、padding `24px`、角丸 `12px`、影 `0 2px 8px rgba(0,0,0,0.06)`、最小高さ `300px`

<details>
<summary>ヒント</summary>

- 外側の `.dashboard-layout` は `grid-template-areas` で大枠を定義
- 内側の `.stat-cards` にも別のGridを使う（Gridの入れ子）
- `grid-template-columns: repeat(4, 1fr)` で4列均等のカードを作成
</details>

<details>
<summary>解答例</summary>

```css
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
}

/* ===== 全体のGridレイアウト ===== */
.dashboard-layout {
  display: grid;
  grid-template-columns: 220px 1fr;
  grid-template-rows: 60px 1fr;
  grid-template-areas:
    "header  header"
    "sidebar main";
  min-height: 100vh;
}

/* ===== ヘッダー ===== */
.dash-header {
  grid-area: header;
  background-color: #1a1a2e;
  color: white;
  padding: 0 24px;
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
}

/* ===== サイドバー ===== */
.dash-sidebar {
  grid-area: sidebar;
  background-color: #16213e;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
}

.dash-menu-item {
  color: #8892b0;
  text-decoration: none;
  padding: 12px 24px;
  font-size: 14px;
}

/* ===== メインエリア ===== */
.dash-main {
  grid-area: main;
  background-color: #f5f6fa;
  padding: 24px;
}

/* ===== 統計カード（入れ子のGrid） ===== */
.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background-color: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  text-align: center;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #2c3e50;
}

.stat-label {
  font-size: 13px;
  color: #999;
  margin-top: 4px;
}

/* ===== グラフエリア ===== */
.chart-area {
  background-color: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  min-height: 300px;
}
```
</details>

---

## 振り返り

| レベル | 問題 | 学んだこと |
|--------|------|-----------|
| 基本 | 1 | display: grid と repeat() で基本グリッド |
| 基本 | 2 | 固定幅と可変幅（fr単位）の組み合わせ |
| 基本 | 3 | grid-template-rows で行の高さ指定 |
| 応用 | 4 | grid-template-areas による名前付きレイアウト |
| 応用 | 5 | grid-column: span / grid-row: span でセル結合 |
| 応用 | 6 | auto-fit と minmax() でレスポンシブ対応 |
| チャレンジ | 7 | spanを活用したマガジン風レイアウト |
| チャレンジ | 8 | Gridの入れ子でダッシュボード作成 |
