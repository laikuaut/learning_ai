# 第3章：Flexbox

## この章で学ぶこと

- Flexboxとは何か
- Flexコンテナとアイテム
- 主軸と交差軸
- 配置（justify-content / align-items / align-self）
- 折り返し（flex-wrap）
- flex プロパティ（grow / shrink / basis）
- gap プロパティ
- よくあるレイアウトパターン

---

## 1. Flexboxとは？

**Flexbox（フレキシブルボックス）** は、要素を柔軟に並べるためのレイアウト方法です。

従来は `float` や `inline-block` を使って苦労していた横並びレイアウトが、Flexboxを使うと簡単に実現できます。

### 使い方の基本

親要素に `display: flex` を指定するだけです。

```html
<div class="container">
  <div class="item">A</div>
  <div class="item">B</div>
  <div class="item">C</div>
</div>
```

```css
.container {
  display: flex;
}
```

これだけで子要素が横に並びます。

```
【display: flex を指定する前】
┌─────────┐
│    A    │
└─────────┘
┌─────────┐
│    B    │
└─────────┘
┌─────────┐
│    C    │
└─────────┘

【display: flex を指定した後】
┌────┐ ┌────┐ ┌────┐
│ A  │ │ B  │ │ C  │
└────┘ └────┘ └────┘
```

---

## 2. Flexコンテナと Flexアイテム

| 用語 | 説明 |
|------|------|
| **Flexコンテナ** | `display: flex` を指定した親要素 |
| **Flexアイテム** | Flexコンテナの直接の子要素 |

```html
<div class="container">    <!-- Flexコンテナ -->
  <div class="item">A</div>  <!-- Flexアイテム -->
  <div class="item">B</div>  <!-- Flexアイテム -->
  <div class="item">C</div>  <!-- Flexアイテム -->
</div>
```

> **重要：** Flexの設定は「コンテナに指定するもの」と「アイテムに指定するもの」に分かれます。

---

## 3. 主軸と交差軸

Flexboxには2つの軸があります。

```
flex-direction: row（デフォルト）の場合

  主軸（main axis）→ → → → →
  ┌────┐ ┌────┐ ┌────┐
  │ A  │ │ B  │ │ C  │    ↓ 交差軸
  └────┘ └────┘ └────┘    ↓（cross axis）


flex-direction: column の場合

  ↓ 主軸（main axis）
  ↓
  ┌─────────┐
  │    A    │  → 交差軸（cross axis）
  └─────────┘
  ┌─────────┐
  │    B    │
  └─────────┘
  ┌─────────┐
  │    C    │
  └─────────┘
```

---

## 4. flex-direction（並ぶ方向）

**コンテナに指定**します。

```css
.container {
  display: flex;
  flex-direction: row;             /* 横並び（デフォルト） */
  flex-direction: row-reverse;     /* 横並び（逆順） */
  flex-direction: column;          /* 縦並び */
  flex-direction: column-reverse;  /* 縦並び（逆順） */
}
```

| 値 | 並び方 |
|----|--------|
| `row` | 左 → 右（デフォルト） |
| `row-reverse` | 右 → 左 |
| `column` | 上 → 下 |
| `column-reverse` | 下 → 上 |

---

## 5. justify-content（主軸方向の配置）

**コンテナに指定**します。主軸方向のアイテムの配置を決めます。

```css
.container {
  display: flex;
  justify-content: flex-start;      /* 先頭に寄せる（デフォルト） */
}
```

### 各値の配置イメージ

```
flex-start（デフォルト）
┌────┬────┬────┬─────────────────┐
│ A  │ B  │ C  │                 │
└────┴────┴────┴─────────────────┘

flex-end
┌─────────────────┬────┬────┬────┐
│                 │ A  │ B  │ C  │
└─────────────────┴────┴────┴────┘

center
┌───────┬────┬────┬────┬───────┐
│       │ A  │ B  │ C  │       │
└───────┴────┴────┴────┴───────┘

space-between
┌────┬──────────┬──────────┬────┐
│ A  │          │          │ C  │
└────┘    B     └──────────┘────┘
（両端に寄せ、間を均等に空ける）

space-around
┌──┬────┬──┬────┬──┬────┬──┐
│  │ A  │  │ B  │  │ C  │  │
└──┴────┴──┴────┴──┴────┴──┘
（各アイテムの左右に均等な余白）

space-evenly
┌───┬────┬───┬────┬───┬────┬───┐
│   │ A  │   │ B  │   │ C  │   │
└───┴────┴───┴────┴───┴────┴───┘
（すべての間隔が均等）
```

### justify-content まとめ

| 値 | 説明 |
|----|------|
| `flex-start` | 先頭に寄せる（デフォルト） |
| `flex-end` | 末尾に寄せる |
| `center` | 中央に寄せる |
| `space-between` | 両端に寄せ、間を均等に |
| `space-around` | 各アイテムの両側に均等な余白 |
| `space-evenly` | すべての間隔を均等に |

---

## 6. align-items（交差軸方向の配置）

**コンテナに指定**します。交差軸方向のアイテムの配置を決めます。

```css
.container {
  display: flex;
  height: 300px;
  align-items: stretch;     /* 高さいっぱいに伸ばす（デフォルト） */
}
```

### 各値の配置イメージ（flex-direction: row の場合）

```
stretch（デフォルト）
┌────────────────────────┐
│┌────┐ ┌────┐ ┌────┐   │
││ A  │ │ B  │ │ C  │   │
││    │ │    │ │    │   │
│└────┘ └────┘ └────┘   │
└────────────────────────┘
（コンテナの高さいっぱいに伸びる）

flex-start
┌────────────────────────┐
│┌────┐ ┌────┐ ┌────┐   │
│└────┘ └────┘ └────┘   │
│                        │
│                        │
└────────────────────────┘

center
┌────────────────────────┐
│                        │
│┌────┐ ┌────┐ ┌────┐   │
│└────┘ └────┘ └────┘   │
│                        │
└────────────────────────┘

flex-end
┌────────────────────────┐
│                        │
│                        │
│┌────┐ ┌────┐ ┌────┐   │
│└────┘ └────┘ └────┘   │
└────────────────────────┘
```

### 上下左右の中央揃え（最も使うパターン）

```css
.container {
  display: flex;
  justify-content: center;   /* 水平方向に中央 */
  align-items: center;       /* 垂直方向に中央 */
  height: 100vh;             /* 画面の高さいっぱい */
}
```

> これだけで完璧な中央揃えが実現できます。Flexbox以前はこれが非常に難しかったのです！

---

## 7. align-self（個別のアイテムの配置）

**アイテムに指定**します。`align-items` を上書きして、特定のアイテムだけ配置を変えられます。

```css
.container {
  display: flex;
  align-items: flex-start;
}

.item-special {
  align-self: flex-end;   /* この要素だけ下に配置 */
}
```

---

## 8. flex-wrap（折り返し）

**コンテナに指定**します。アイテムがコンテナからはみ出す場合の動作を制御します。

```css
.container {
  display: flex;
  flex-wrap: nowrap;   /* 折り返さない（デフォルト・アイテムが縮む） */
  flex-wrap: wrap;     /* 折り返す */
}
```

```
nowrap（デフォルト）
┌────┬────┬────┬────┬────┐
│ A  │ B  │ C  │ D  │ E  │  ← 全部1行に無理やり収める
└────┴────┴────┴────┴────┘

wrap
┌────┬────┬────┐
│ A  │ B  │ C  │
└────┴────┴────┘
┌────┬────┐
│ D  │ E  │
└────┴────┘
```

---

## 9. gap（アイテム間の余白）

**コンテナに指定**します。アイテム同士の間隔を簡単に設定できます。

```css
.container {
  display: flex;
  gap: 16px;               /* 上下左右の間隔 */
  gap: 20px 16px;          /* 行間 列間 */
  row-gap: 20px;           /* 行間のみ */
  column-gap: 16px;        /* 列間のみ */
}
```

> **メリット：** marginと違い、最初と最後のアイテムに余計な余白が付きません。

---

## 10. flex プロパティ（アイテムのサイズ制御）

**アイテムに指定**します。アイテムの伸縮を制御します。

### 10.1 flex-grow（伸びる比率）

余ったスペースをアイテムが占める比率を指定します。

```css
.item-a { flex-grow: 1; }  /* 1の割合で伸びる */
.item-b { flex-grow: 2; }  /* 2の割合で伸びる */
.item-c { flex-grow: 1; }  /* 1の割合で伸びる */
```

```
┌──────┬────────────┬──────┐
│  A   │     B      │  C   │
│ (1)  │    (2)     │ (1)  │
└──────┴────────────┴──────┘
  25%       50%        25%
```

### 10.2 flex-shrink（縮む比率）

スペースが足りない場合に縮む比率を指定します。

```css
.item { flex-shrink: 1; }     /* 均等に縮む（デフォルト） */
.item-fixed { flex-shrink: 0; } /* 縮まない */
```

### 10.3 flex-basis（基本サイズ）

伸縮前の基本サイズを指定します。

```css
.item { flex-basis: 200px; }   /* 基本幅200px */
.item { flex-basis: auto; }    /* コンテンツに合わせる（デフォルト） */
```

### 10.4 flex ショートハンド

```css
.item {
  flex: 1;           /* flex-grow: 1, flex-shrink: 1, flex-basis: 0% */
  flex: 0 0 200px;   /* 伸びない、縮まない、幅200px固定 */
  flex: 1 1 auto;    /* 伸びる、縮む、基本はコンテンツ幅 */
}
```

### よく使う flex パターン

| 書き方 | 意味 |
|--------|------|
| `flex: 1` | 余った幅を均等に分け合う |
| `flex: 0 0 auto` | 伸びも縮みもしない（コンテンツ幅のまま） |
| `flex: 0 0 200px` | 200px固定 |
| `flex: 1 1 0%` | 均等な幅に分割（`flex: 1` と同じ） |

---

## 11. order（表示順序）

**アイテムに指定**します。HTMLの順番を変えずに、表示順序を変更できます。

```css
.item-a { order: 2; }
.item-b { order: 1; }
.item-c { order: 3; }
```

→ 表示順は B → A → C になります（デフォルトのorderは0）。

---

## 12. よくあるレイアウトパターン

### パターン1：ナビゲーションバー

```html
<nav class="navbar">
  <div class="logo">サイト名</div>
  <ul class="nav-links">
    <li><a href="#">ホーム</a></li>
    <li><a href="#">サービス</a></li>
    <li><a href="#">お問い合わせ</a></li>
  </ul>
</nav>
```

```css
.navbar {
  display: flex;
  justify-content: space-between;  /* ロゴとリンクを両端に */
  align-items: center;
  padding: 16px 24px;
  background-color: #333;
  color: white;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 24px;
  margin: 0;
  padding: 0;
}
```

```
┌──────────────────────────────────────┐
│ サイト名          ホーム サービス お問い合わせ │
└──────────────────────────────────────┘
```

### パターン2：カードの横並び

```css
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.card {
  flex: 1 1 300px;    /* 最小300px、余裕があれば伸びる */
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
```

### パターン3：サイドバー + メインコンテンツ

```css
.layout {
  display: flex;
  gap: 24px;
}

.sidebar {
  flex: 0 0 250px;   /* 250px固定 */
}

.main-content {
  flex: 1;            /* 残りのスペースを全部使う */
}
```

```
┌──────────┬──────────────────────┐
│          │                      │
│ sidebar  │    main-content      │
│ (250px)  │    (残りの幅)         │
│          │                      │
└──────────┴──────────────────────┘
```

### パターン4：フッターを画面下部に固定

```css
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;   /* メインコンテンツが伸びて残りのスペースを埋める */
}

footer {
  /* flex: 0のまま（コンテンツ分だけ） */
}
```

---

## Flexboxプロパティ早見表

### コンテナに指定するプロパティ

| プロパティ | 値 | デフォルト |
|-----------|-----|---------|
| `display` | `flex` | ─ |
| `flex-direction` | `row` / `column` / `row-reverse` / `column-reverse` | `row` |
| `justify-content` | `flex-start` / `center` / `flex-end` / `space-between` / `space-around` / `space-evenly` | `flex-start` |
| `align-items` | `stretch` / `flex-start` / `center` / `flex-end` / `baseline` | `stretch` |
| `flex-wrap` | `nowrap` / `wrap` | `nowrap` |
| `gap` | 長さ（例：`16px`） | `0` |
| `align-content` | `flex-start` / `center` / `space-between` など | `stretch` |

### アイテムに指定するプロパティ

| プロパティ | 値 | デフォルト |
|-----------|-----|---------|
| `flex` | `grow shrink basis` | `0 1 auto` |
| `flex-grow` | 数値 | `0` |
| `flex-shrink` | 数値 | `1` |
| `flex-basis` | 長さ / `auto` | `auto` |
| `align-self` | `auto` / `flex-start` / `center` / `flex-end` / `stretch` | `auto` |
| `order` | 数値 | `0` |

---

## まとめ

| 項目 | 要点 |
|------|------|
| Flexboxの開始 | 親に `display: flex` を指定するだけ |
| 方向 | `flex-direction` で横（row）か縦（column）を指定 |
| 主軸の配置 | `justify-content` で中央揃え・均等配置など |
| 交差軸の配置 | `align-items` で上下方向の位置を調整 |
| 中央揃え | `justify-content: center` + `align-items: center` |
| 折り返し | `flex-wrap: wrap` で複数行に |
| 間隔 | `gap` でアイテム間の余白を指定 |
| 伸縮 | `flex: 1` で余ったスペースを埋める |

---

---

## 動作サンプル

この章の内容を実際に動かして確認できるサンプルファイルを用意しています。

**ファイル：** `../サンプル/03_Flexbox.html`

ブラウザで開いて、Flexboxの各プロパティの動作を確認しましょう。

---

次の章では「CSS Grid」を学びます。Flexboxが1次元（横 or 縦）のレイアウトに強いのに対し、Gridは2次元（横 と 縦）のレイアウトに最適です。
