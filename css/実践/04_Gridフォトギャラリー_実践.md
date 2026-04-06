# 実践課題04：Gridフォトギャラリー ★2

> **難易度**: ★★☆☆☆（基礎）
> **前提知識**: 第1章（CSSの基本）、第4章（Grid）
> **課題の種類**: ミニプロジェクト
> **学習目標**: CSS Gridの `grid-template-columns`・`grid-row`・`grid-column`・`gap` を使って、不規則なレイアウトのギャラリーを作る

---

## 完成イメージ

```
┌──────────────┬───────┐
│              │       │
│   大きい写真  │  写真2 │
│   （2列分）   │       │
│              ├───────┤
│              │  写真3 │
├───────┬──────┴───────┤
│ 写真4  │    写真5     │
│       │  （2列分）    │
├───────┴──────┬───────┤
│   写真6      │ 写真7  │
└──────────────┴───────┘
```

写真の代わりに背景色のボックスを使い、ホバーするとオーバーレイ（overlay）が表示されます。

---

## 課題の要件

1. CSS Grid を使ってギャラリーレイアウトを組む
2. 一部のアイテムは2列または2行にまたがらせる
3. `gap` で均等な溝を設ける
4. 各アイテムに背景色（写真の代わり）と番号テキストを表示する
5. ホバー時にオーバーレイ（半透明の暗い膜＋テキスト）を表示する

---

## ステップガイド

<details>
<summary>ステップ1：Grid コンテナを作る</summary>

3列のグリッドを定義します。

```css
.gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
```

</details>

<details>
<summary>ステップ2：特定アイテムを複数セルにまたがらせる</summary>

```css
.item-1 {
  grid-column: 1 / 3;  /* 1列目から3列目の手前まで＝2列分 */
  grid-row: 1 / 3;     /* 2行分 */
}
```

</details>

<details>
<summary>ステップ3：ホバーオーバーレイを作る</summary>

`position: relative` と `::after` 疑似要素（pseudo-element）を組み合わせます。

```css
.item {
  position: relative;
  overflow: hidden;
}

.item::after {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.3s;
}

.item:hover::after {
  opacity: 1;
}
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>フォトギャラリー</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: sans-serif;
      background-color: #1a1a1a;
      padding: 32px;
      color: #ffffff;
    }

    h1 {
      text-align: center;
      margin-bottom: 24px;
      font-size: 24px;
    }

    /* --- ギャラリー --- */
    .gallery {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      max-width: 800px;
      margin: 0 auto;
    }

    /* --- アイテム共通 --- */
    .item {
      background-color: #333333;
      border-radius: 8px;
      min-height: 180px;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 18px;
      color: #ffffff;
      position: relative;
      overflow: hidden;
      cursor: pointer;
    }

    /* --- 個別の背景色 --- */
    .item-1 { background-color: #e74c3c; }
    .item-2 { background-color: #3498db; }
    .item-3 { background-color: #2ecc71; }
    .item-4 { background-color: #f39c12; }
    .item-5 { background-color: #9b59b6; }
    .item-6 { background-color: #1abc9c; }
    .item-7 { background-color: #e67e22; }

    /* --- 複数セルにまたがるアイテム --- */
    .item-1 {
      grid-column: 1 / 3;
      grid-row: 1 / 3;
      min-height: 372px;  /* (180 * 2) + gap(12) */
    }

    .item-5 {
      grid-column: 2 / 4;
    }

    /* --- ホバーオーバーレイ --- */
    .item::after {
      content: "クリックで拡大";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 14px;
      opacity: 0;
      transition: opacity 0.3s;
    }

    .item:hover::after {
      opacity: 1;
    }
  </style>
</head>
<body>
  <h1>フォトギャラリー</h1>
  <div class="gallery">
    <div class="item item-1">Photo 1</div>
    <div class="item item-2">Photo 2</div>
    <div class="item item-3">Photo 3</div>
    <div class="item item-4">Photo 4</div>
    <div class="item item-5">Photo 5</div>
    <div class="item item-6">Photo 6</div>
    <div class="item item-7">Photo 7</div>
  </div>
</body>
</html>
```

</details>

<details>
<summary>解答例（改良版 ─ ホバー時ズームイン演出付き）</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>フォトギャラリー（改良版）</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: "Helvetica Neue", Arial, sans-serif;
      background-color: #111111;
      padding: 40px 32px;
      color: #ffffff;
    }

    h1 {
      text-align: center;
      margin-bottom: 8px;
      font-size: 28px;
      font-weight: 300;
      letter-spacing: 4px;
      text-transform: uppercase;
    }

    .subtitle {
      text-align: center;
      color: #888888;
      font-size: 14px;
      margin-bottom: 40px;
    }

    .gallery {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-auto-rows: 200px;
      gap: 8px;
      max-width: 900px;
      margin: 0 auto;
    }

    .item {
      border-radius: 4px;
      position: relative;
      overflow: hidden;
      cursor: pointer;
    }

    /* 背景色をグラデーションで表現 */
    .item-1 { background: linear-gradient(135deg, #e74c3c, #c0392b); }
    .item-2 { background: linear-gradient(135deg, #3498db, #2980b9); }
    .item-3 { background: linear-gradient(135deg, #2ecc71, #27ae60); }
    .item-4 { background: linear-gradient(135deg, #f39c12, #e67e22); }
    .item-5 { background: linear-gradient(135deg, #9b59b6, #8e44ad); }
    .item-6 { background: linear-gradient(135deg, #1abc9c, #16a085); }
    .item-7 { background: linear-gradient(135deg, #e67e22, #d35400); }

    /* グリッド配置 */
    .item-1 {
      grid-column: 1 / 3;
      grid-row: 1 / 3;
    }

    .item-5 {
      grid-column: 2 / 4;
    }

    /* ズームイン背景（疑似要素で背景レイヤーを作る） */
    .item::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: inherit;
      transition: transform 0.4s ease;
      z-index: 0;
    }

    .item:hover::before {
      transform: scale(1.1);
    }

    /* テキストオーバーレイ */
    .item-label {
      position: relative;
      z-index: 2;
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding: 16px;
    }

    .item-label .item-title {
      font-size: 16px;
      font-weight: 600;
      transform: translateY(8px);
      opacity: 0;
      transition: transform 0.3s, opacity 0.3s;
    }

    .item-label .item-desc {
      font-size: 12px;
      color: rgba(255, 255, 255, 0.7);
      transform: translateY(8px);
      opacity: 0;
      transition: transform 0.3s 0.05s, opacity 0.3s 0.05s;
    }

    .item:hover .item-title,
    .item:hover .item-desc {
      transform: translateY(0);
      opacity: 1;
    }

    /* 暗くするオーバーレイ */
    .item::after {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(to top, rgba(0,0,0,0.6) 0%, transparent 60%);
      opacity: 0;
      transition: opacity 0.3s;
      z-index: 1;
    }

    .item:hover::after {
      opacity: 1;
    }
  </style>
</head>
<body>
  <h1>Gallery</h1>
  <p class="subtitle">ホバーして詳細を確認してください</p>

  <div class="gallery">
    <div class="item item-1">
      <div class="item-label">
        <div class="item-title">風景写真</div>
        <div class="item-desc">2024年 春の風景コレクション</div>
      </div>
    </div>
    <div class="item item-2">
      <div class="item-label">
        <div class="item-title">海</div>
        <div class="item-desc">夏の海辺シリーズ</div>
      </div>
    </div>
    <div class="item item-3">
      <div class="item-label">
        <div class="item-title">森</div>
        <div class="item-desc">新緑の季節</div>
      </div>
    </div>
    <div class="item item-4">
      <div class="item-label">
        <div class="item-title">夕焼け</div>
        <div class="item-desc">黄金色の空</div>
      </div>
    </div>
    <div class="item item-5">
      <div class="item-label">
        <div class="item-title">夜景</div>
        <div class="item-desc">都市のイルミネーション</div>
      </div>
    </div>
    <div class="item item-6">
      <div class="item-label">
        <div class="item-title">花</div>
        <div class="item-desc">マクロ撮影</div>
      </div>
    </div>
    <div class="item item-7">
      <div class="item-label">
        <div class="item-title">山</div>
        <div class="item-desc">秋の紅葉シーズン</div>
      </div>
    </div>
  </div>
</body>
</html>
```

**初心者向けとの違い:**
- `::before` 疑似要素で背景レイヤーを分離し、ホバー時にズームインする演出
- 下からグラデーションで暗くなるオーバーレイ（写真サイトでよく見るパターン）
- テキストがホバー時に下からスライドインするアニメーション
- `transition-delay` で要素ごとに微妙な時差を付けて高級感を演出
- `grid-auto-rows` で行の高さを明示し、レイアウト崩れを防止

</details>
