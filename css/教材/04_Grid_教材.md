# 第4章：CSS Grid

## この章で学ぶこと

- CSS Gridとは何か
- Gridコンテナとアイテム
- 行と列の定義（grid-template-columns / rows）
- fr単位
- gap（間隔）
- アイテムの配置（grid-column / grid-row）
- grid-template-areas（名前付きエリア）
- レスポンシブなGridレイアウト
- FlexboxとGridの使い分け

---

## 1. CSS Gridとは？

**CSS Grid** は、Webページを「行（横）と列（縦）」の格子状に分割してレイアウトする仕組みです。

```
Flexbox → 1次元レイアウト（横 or 縦のどちらか）
Grid    → 2次元レイアウト（横 と 縦の両方を同時に制御）
```

### 使い方の基本

親要素に `display: grid` を指定し、行と列を定義します。

```html
<div class="grid-container">
  <div class="item">1</div>
  <div class="item">2</div>
  <div class="item">3</div>
  <div class="item">4</div>
  <div class="item">5</div>
  <div class="item">6</div>
</div>
```

```css
.grid-container {
  display: grid;
  grid-template-columns: 200px 200px 200px;  /* 3列（各200px） */
  grid-template-rows: 100px 100px;            /* 2行（各100px） */
  gap: 16px;
}
```

```
┌──────┐ ┌──────┐ ┌──────┐
│  1   │ │  2   │ │  3   │  ← 1行目（100px）
└──────┘ └──────┘ └──────┘
┌──────┐ ┌──────┐ ┌──────┐
│  4   │ │  5   │ │  6   │  ← 2行目（100px）
└──────┘ └──────┘ └──────┘
 200px    200px    200px
```

---

## 2. Gridの用語

```
          列1(column)  列2       列3
         ←─────────→←─────→←─────────→
    行1  ┌──────────┬───────┬──────────┐  ─┬─
(row)    │          │       │          │   │
         │   セル   │  セル  │   セル    │   │
         │          │       │          │   │
         ├──────────┼───────┼──────────┤  ─┤
    行2  │          │       │          │   │
         │   セル   │  セル  │   セル    │   │
         │          │       │          │   │
         └──────────┴───────┴──────────┘  ─┘
         ↑          ↑       ↑          ↑
       ライン1    ライン2  ライン3    ライン4
       (line)
```

| 用語 | 説明 |
|------|------|
| **Gridコンテナ** | `display: grid` を指定した親要素 |
| **Gridアイテム** | Gridコンテナの直接の子要素 |
| **セル** | 行と列が交わる1つのマス |
| **トラック** | 1つの行全体、または1つの列全体 |
| **ライン** | 行や列の区切り線（番号が振られる） |
| **エリア** | 複数のセルをまとめた範囲 |

---

## 3. grid-template-columns / rows（列と行の定義）

### 固定サイズで指定

```css
.container {
  display: grid;
  grid-template-columns: 200px 300px 200px;  /* 3列 */
  grid-template-rows: 100px 150px;           /* 2行 */
}
```

### fr単位（余ったスペースを分け合う）

**fr（fraction）** はGridで使える特別な単位で、余ったスペースを比率で分配します。

```css
.container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;  /* 3列を均等に分割 */
}
```

```
┌──────────┬──────────┬──────────┐
│   1fr    │   1fr    │   1fr    │
│  (33%)   │  (33%)   │  (33%)   │
└──────────┴──────────┴──────────┘
```

比率を変えることもできます。

```css
grid-template-columns: 1fr 2fr 1fr;  /* 1:2:1 の比率 */
```

```
┌──────┬────────────┬──────┐
│ 1fr  │    2fr     │ 1fr  │
│(25%) │   (50%)    │(25%) │
└──────┴────────────┴──────┘
```

### 固定値とfrの組み合わせ

```css
grid-template-columns: 250px 1fr;  /* 左250px固定、右は残り全部 */
```

```
┌──────────┬──────────────────────┐
│  250px   │        1fr           │
│ (固定)    │    (残り全部)         │
└──────────┴──────────────────────┘
```

### repeat() で繰り返し

同じ指定を繰り返す場合に便利です。

```css
grid-template-columns: repeat(3, 1fr);        /* 1fr 1fr 1fr と同じ */
grid-template-columns: repeat(4, 200px);      /* 200px × 4列 */
grid-template-columns: repeat(3, 1fr 2fr);    /* 1fr 2fr 1fr 2fr 1fr 2fr（6列） */
```

### minmax() で最小値と最大値

```css
grid-template-columns: repeat(3, minmax(200px, 1fr));
/* 各列は最小200px、最大は均等分割 */
```

---

## 4. gap（間隔）

Flexboxと同じく `gap` で間隔を指定します。

```css
.container {
  display: grid;
  gap: 16px;               /* 行間と列間の両方 */
  gap: 20px 16px;          /* 行間20px、列間16px */
  row-gap: 20px;           /* 行間のみ */
  column-gap: 16px;        /* 列間のみ */
}
```

---

## 5. アイテムの配置（grid-column / grid-row）

アイテムをどの位置に配置するか、ライン番号で指定できます。

### ライン番号を理解する

3列のGridの場合、列のライン番号は 1, 2, 3, 4 です。

```
  ライン1  ライン2  ライン3  ライン4
    ↓       ↓       ↓       ↓
    │ 列1   │ 列2   │ 列3   │
    │       │       │       │
```

### grid-column / grid-row の使い方

```css
.item-a {
  grid-column: 1 / 3;  /* 列ライン1から3まで（2列分） */
  grid-row: 1 / 2;     /* 行ライン1から2まで（1行分） */
}
```

```
  1       2       3       4
  ┌───────────────┬───────┐
  │     A         │       │  ← Aが2列分を占める
  ├───────┬───────┼───────┤
  │       │       │       │
  └───────┴───────┴───────┘
```

### span で指定

ライン番号の代わりに「いくつ分」で指定できます。

```css
.item-a {
  grid-column: span 2;  /* 2列分 */
  grid-row: span 3;     /* 3行分 */
}
```

### 実例：ダッシュボード風レイアウト

```css
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: auto auto auto;
  gap: 16px;
}

.header {
  grid-column: 1 / -1;    /* -1は最後のラインを意味する（全列を使う） */
}

.sidebar {
  grid-column: 1 / 2;     /* 1列目 */
  grid-row: 2 / 4;        /* 2行目から3行目まで */
}

.main {
  grid-column: 2 / -1;    /* 2列目から最後まで */
}

.widget {
  grid-column: 2 / 4;     /* 2列目から3列目 */
}
```

---

## 6. grid-template-areas（名前付きエリア）

セルに名前を付けて、直感的にレイアウトを定義できます。**初心者に特におすすめ**の方法です。

### 基本的な使い方

```css
.container {
  display: grid;
  grid-template-columns: 250px 1fr;
  grid-template-rows: 60px 1fr 50px;
  grid-template-areas:
    "header  header"
    "sidebar main"
    "footer  footer";
  gap: 16px;
  min-height: 100vh;
}

.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }
```

```html
<div class="container">
  <header class="header">ヘッダー</header>
  <aside class="sidebar">サイドバー</aside>
  <main class="main">メインコンテンツ</main>
  <footer class="footer">フッター</footer>
</div>
```

```
┌───────────────────────────────┐
│           header              │  60px
├──────────┬────────────────────┤
│          │                    │
│ sidebar  │       main         │  1fr
│          │                    │
├──────────┴────────────────────┤
│           footer              │  50px
└───────────────────────────────┘
   250px          1fr
```

### 空白セルの指定

空のセルには `.`（ドット）を使います。

```css
grid-template-areas:
  "header header header"
  "sidebar main ."
  "footer footer footer";
```

### grid-template-areas のルール

1. すべての行で同じ列数を指定する
2. エリアは長方形でなければならない（L字型などはNG）
3. 空のセルは `.` で表す
4. 各アイテムに `grid-area: エリア名` を指定する

---

## 7. 暗黙的なGrid（auto-fill / auto-fit）

アイテムの数が不明な場合、自動的に列数を調整するレスポンシブなGridを作れます。

### auto-fill

```css
.container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}
```

→ 各アイテムは最小250px。画面幅に応じて列数が自動で変わります。

```
画面が広い場合：
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│  1   │ │  2   │ │  3   │ │  4   │
└──────┘ └──────┘ └──────┘ └──────┘

画面が狭い場合：
┌──────────┐ ┌──────────┐
│    1     │ │    2     │
└──────────┘ └──────────┘
┌──────────┐ ┌──────────┐
│    3     │ │    4     │
└──────────┘ └──────────┘
```

### auto-fill と auto-fit の違い

- **auto-fill**：空のトラック（列）を保持する
- **auto-fit**：空のトラックを潰して、アイテムを広げる

> アイテムが少ない場合に違いが出ます。多くの場合は `auto-fit` が使いやすいです。

```css
/* アイテムが画面幅いっぱいに広がってほしい場合 */
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
```

---

## 8. 配置の微調整

### justify-items / align-items

セル内でのアイテムの配置を制御します。

```css
.container {
  display: grid;
  justify-items: center;   /* 水平方向に中央 */
  align-items: center;     /* 垂直方向に中央 */
}
```

### place-items（ショートハンド）

```css
.container {
  place-items: center;           /* align-items と justify-items を同時に指定 */
  place-items: center stretch;   /* align / justify */
}
```

### justify-content / align-content

Grid全体の配置を制御します（コンテナにスペースが余っている場合）。

```css
.container {
  display: grid;
  justify-content: center;     /* Grid全体を水平方向の中央に */
  align-content: center;       /* Grid全体を垂直方向の中央に */
}
```

---

## 9. よくあるGridレイアウトパターン

### パターン1：ホーリーグレイルレイアウト

Webサイトで最もよく見る構成です。

```css
.page {
  display: grid;
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header header"
    "left   main   right"
    "footer footer footer";
  min-height: 100vh;
  gap: 16px;
}

.header { grid-area: header; }
.left   { grid-area: left; }
.main   { grid-area: main; }
.right  { grid-area: right; }
.footer { grid-area: footer; }
```

### パターン2：写真ギャラリー

```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 8px;
}

.gallery img {
  width: 100%;
  height: 200px;
  object-fit: cover;       /* 画像の比率を保ちながらサイズに合わせる */
  border-radius: 4px;
}
```

### パターン3：特徴セクション（2×3 グリッド）

```css
.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  padding: 40px;
}

.feature-card {
  text-align: center;
  padding: 24px;
  border: 1px solid #eee;
  border-radius: 8px;
}
```

```
┌──────────┐ ┌──────────┐ ┌──────────┐
│ 特徴 1    │ │ 特徴 2    │ │ 特徴 3    │
└──────────┘ └──────────┘ └──────────┘
┌──────────┐ ┌──────────┐ ┌──────────┐
│ 特徴 4    │ │ 特徴 5    │ │ 特徴 6    │
└──────────┘ └──────────┘ └──────────┘
```

### パターン4：マガジン風レイアウト

```css
.magazine {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: 200px 200px;
  gap: 16px;
}

.feature-article {
  grid-column: span 2;
  grid-row: span 2;     /* 大きな記事：2列×2行 */
}

.sub-article {
  grid-column: span 1;
  grid-row: span 1;     /* 小さな記事：1列×1行 */
}
```

```
┌──────────────┬───────┐
│              │  記事2 │
│  特集記事     ├───────┤
│              │  記事3 │
└──────────────┴───────┘
```

---

## 10. FlexboxとGridの使い分け

| 特徴 | Flexbox | Grid |
|------|---------|------|
| 次元 | 1次元（横 or 縦） | 2次元（横 と 縦） |
| 得意なこと | 要素を1列に並べる | ページ全体のレイアウト |
| アイテム数 | 不定でもOK | 定まっている方が扱いやすい |
| 代表的な用途 | ナビバー、ボタン群、カードの横並び | ページ構成、ギャラリー、ダッシュボード |

### 判断の目安

- **横か縦の一方向だけ** → **Flexbox**
- **行と列の両方を制御したい** → **Grid**
- **ナビバー、ツールバー** → **Flexbox**
- **ページ全体の骨格** → **Grid**
- **カードの繰り返し** → **Grid**（auto-fit）か **Flexbox**（flex-wrap）

> 実務ではFlexboxとGridを組み合わせて使います。ページ全体の構成をGridで作り、各パーツの中身をFlexboxで並べる、というのがよくあるパターンです。

---

## Gridプロパティ早見表

### コンテナに指定するプロパティ

| プロパティ | 説明 | 例 |
|-----------|------|-----|
| `display` | Gridを有効化 | `grid` |
| `grid-template-columns` | 列の定義 | `1fr 1fr 1fr` |
| `grid-template-rows` | 行の定義 | `auto 1fr auto` |
| `grid-template-areas` | エリアの名前付け | `"header header"` |
| `gap` | 間隔 | `16px` |
| `justify-items` | セル内の水平配置 | `center` |
| `align-items` | セル内の垂直配置 | `center` |
| `justify-content` | Grid全体の水平配置 | `center` |
| `align-content` | Grid全体の垂直配置 | `center` |

### アイテムに指定するプロパティ

| プロパティ | 説明 | 例 |
|-----------|------|-----|
| `grid-column` | 列の配置 | `1 / 3` or `span 2` |
| `grid-row` | 行の配置 | `1 / 3` or `span 2` |
| `grid-area` | エリア名の指定 | `header` |
| `justify-self` | 個別の水平配置 | `center` |
| `align-self` | 個別の垂直配置 | `center` |

---

## まとめ

| 項目 | 要点 |
|------|------|
| Gridの開始 | 親に `display: grid` を指定 |
| 列の定義 | `grid-template-columns` で列数と幅を指定 |
| fr単位 | 余ったスペースを比率で分配する便利な単位 |
| repeat() | 同じ指定の繰り返しを簡潔に書ける |
| エリア指定 | `grid-template-areas` で直感的にレイアウト定義 |
| レスポンシブ | `auto-fit` + `minmax()` で自動調整 |
| Flexboxとの使い分け | 1次元→Flexbox、2次元→Grid |

---

---

## 動作サンプル

この章の内容を実際に動かして確認できるサンプルファイルを用意しています。

**ファイル：** `../サンプル/04_Grid.html`

ブラウザで開いて、Gridレイアウトの各パターンを確認しましょう。

---

次の章では「レスポンシブデザイン」を学びます。画面サイズに応じてレイアウトを切り替える方法を、メディアクエリやモバイルファーストの考え方とともに解説します。
