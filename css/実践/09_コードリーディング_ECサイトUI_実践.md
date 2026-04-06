# 実践課題09：コードリーディング ─ ECサイトUI ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第1章〜第8章（全章）
> **課題の種類**: コードリーディング
> **学習目標**: 他者が書いたCSSを読み解き、レイアウトの仕組み・設計意図・改善点を理解する力を養う

---

## 課題の説明

以下のコードは「ECサイトの商品一覧ページ」です。
コードを読んで、後に続く **10個の設問** に答えてください。

**ブラウザで実際に表示して確認しても構いませんが、まずコードだけで挙動を想像してみましょう。**

---

## 読解対象コード

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ショップ - 商品一覧</title>
  <style>
    /* ===== リセット＆基本 ===== */
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    :root {
      --color-primary: #2563eb;
      --color-primary-dark: #1d4ed8;
      --color-bg: #f8fafc;
      --color-surface: #ffffff;
      --color-text: #1e293b;
      --color-text-muted: #64748b;
      --color-border: #e2e8f0;
      --color-danger: #ef4444;
      --color-success: #22c55e;
      --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
      --radius: 8px;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background-color: var(--color-bg);
      color: var(--color-text);
      line-height: 1.5;
    }

    /* ===== ヘッダー ===== */
    .header {
      background-color: var(--color-surface);
      border-bottom: 1px solid var(--color-border);
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .header-inner {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 24px;
      height: 64px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .logo {
      font-size: 20px;
      font-weight: 700;
      color: var(--color-primary);
    }

    .search-bar {
      flex: 1;
      max-width: 480px;
      margin: 0 32px;
      position: relative;
    }

    .search-bar input {
      width: 100%;
      padding: 8px 16px 8px 40px;
      border: 1px solid var(--color-border);
      border-radius: 24px;
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s;
    }

    .search-bar input:focus {
      border-color: var(--color-primary);
    }

    .search-bar::before {
      content: "🔍";
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 14px;
    }

    .cart-btn {
      position: relative;
      background: none;
      border: none;
      font-size: 24px;
      cursor: pointer;
    }

    .cart-count {
      position: absolute;
      top: -6px;
      right: -10px;
      background-color: var(--color-danger);
      color: #fff;
      font-size: 11px;
      font-weight: 700;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    /* ===== メインレイアウト ===== */
    .page {
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px;
      display: grid;
      grid-template-columns: 240px 1fr;
      gap: 32px;
    }

    /* ===== サイドバー（フィルタ） ===== */
    .filters {
      position: sticky;
      top: 88px;
      align-self: start;
    }

    .filter-group {
      margin-bottom: 24px;
    }

    .filter-group h3 {
      font-size: 14px;
      font-weight: 600;
      margin-bottom: 12px;
      color: var(--color-text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .filter-group label {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 6px 0;
      font-size: 14px;
      cursor: pointer;
    }

    .price-range {
      display: flex;
      gap: 8px;
      align-items: center;
    }

    .price-range input {
      width: 80px;
      padding: 6px 8px;
      border: 1px solid var(--color-border);
      border-radius: var(--radius);
      font-size: 13px;
    }

    /* ===== 商品グリッド ===== */
    .products-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }

    .products-header h2 {
      font-size: 20px;
    }

    .sort-select {
      padding: 6px 12px;
      border: 1px solid var(--color-border);
      border-radius: var(--radius);
      font-size: 13px;
      background-color: var(--color-surface);
    }

    .product-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 20px;
    }

    /* ===== 商品カード ===== */
    .product-card {
      background-color: var(--color-surface);
      border-radius: var(--radius);
      overflow: hidden;
      box-shadow: var(--shadow-sm);
      transition: box-shadow 0.2s, transform 0.2s;
    }

    .product-card:hover {
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
    }

    .product-image {
      width: 100%;
      aspect-ratio: 1 / 1;
      object-fit: cover;
      display: block;
    }

    .product-image-placeholder {
      width: 100%;
      aspect-ratio: 1 / 1;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 48px;
      background-color: #f1f5f9;
    }

    .product-body {
      padding: 16px;
    }

    .product-category {
      font-size: 11px;
      color: var(--color-text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .product-name {
      font-size: 15px;
      font-weight: 600;
      margin: 4px 0 8px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .product-price {
      display: flex;
      align-items: baseline;
      gap: 8px;
    }

    .current-price {
      font-size: 18px;
      font-weight: 700;
      color: var(--color-danger);
    }

    .original-price {
      font-size: 13px;
      color: var(--color-text-muted);
      text-decoration: line-through;
    }

    .product-rating {
      display: flex;
      align-items: center;
      gap: 4px;
      margin-top: 8px;
      font-size: 13px;
      color: var(--color-text-muted);
    }

    .stars {
      color: #f59e0b;
    }

    .product-actions {
      padding: 0 16px 16px;
    }

    .add-to-cart {
      width: 100%;
      padding: 10px;
      background-color: var(--color-primary);
      color: #fff;
      border: none;
      border-radius: var(--radius);
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: background-color 0.2s;
    }

    .add-to-cart:hover {
      background-color: var(--color-primary-dark);
    }

    .badge-sale {
      position: absolute;
      top: 12px;
      left: 12px;
      background-color: var(--color-danger);
      color: #fff;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 4px;
    }

    .product-card {
      position: relative;
    }

    /* ===== レスポンシブ ===== */
    @media (max-width: 768px) {
      .page {
        grid-template-columns: 1fr;
      }

      .filters {
        position: static;
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
      }

      .search-bar {
        display: none;
      }
    }
  </style>
</head>
<body>
  <header class="header">
    <div class="header-inner">
      <div class="logo">Shop</div>
      <div class="search-bar">
        <input type="text" placeholder="商品を検索...">
      </div>
      <button class="cart-btn">
        🛒
        <span class="cart-count">3</span>
      </button>
    </div>
  </header>

  <div class="page">
    <aside class="filters">
      <div class="filter-group">
        <h3>カテゴリ</h3>
        <label><input type="checkbox"> エレクトロニクス</label>
        <label><input type="checkbox"> ファッション</label>
        <label><input type="checkbox"> ホーム&キッチン</label>
        <label><input type="checkbox"> 書籍</label>
      </div>
      <div class="filter-group">
        <h3>価格帯</h3>
        <div class="price-range">
          <input type="number" placeholder="¥ 下限">
          <span>〜</span>
          <input type="number" placeholder="¥ 上限">
        </div>
      </div>
    </aside>

    <main>
      <div class="products-header">
        <h2>商品一覧 <small style="color: #64748b; font-weight: 400;">(24件)</small></h2>
        <select class="sort-select">
          <option>おすすめ順</option>
          <option>価格が安い順</option>
          <option>価格が高い順</option>
          <option>新着順</option>
        </select>
      </div>

      <div class="product-grid">
        <div class="product-card">
          <span class="badge-sale">-30%</span>
          <div class="product-image-placeholder">📱</div>
          <div class="product-body">
            <div class="product-category">エレクトロニクス</div>
            <h3 class="product-name">ワイヤレスイヤホン Pro</h3>
            <div class="product-price">
              <span class="current-price">¥6,980</span>
              <span class="original-price">¥9,980</span>
            </div>
            <div class="product-rating">
              <span class="stars">★★★★☆</span>
              <span>(128)</span>
            </div>
          </div>
          <div class="product-actions">
            <button class="add-to-cart">カートに追加</button>
          </div>
        </div>

        <div class="product-card">
          <div class="product-image-placeholder">👕</div>
          <div class="product-body">
            <div class="product-category">ファッション</div>
            <h3 class="product-name">オーガニックコットン Tシャツ</h3>
            <div class="product-price">
              <span class="current-price">¥3,480</span>
            </div>
            <div class="product-rating">
              <span class="stars">★★★★★</span>
              <span>(56)</span>
            </div>
          </div>
          <div class="product-actions">
            <button class="add-to-cart">カートに追加</button>
          </div>
        </div>

        <div class="product-card">
          <span class="badge-sale">-20%</span>
          <div class="product-image-placeholder">📚</div>
          <div class="product-body">
            <div class="product-category">書籍</div>
            <h3 class="product-name">CSS設計完全ガイド 実践で使えるテクニック集</h3>
            <div class="product-price">
              <span class="current-price">¥2,640</span>
              <span class="original-price">¥3,300</span>
            </div>
            <div class="product-rating">
              <span class="stars">★★★★☆</span>
              <span>(42)</span>
            </div>
          </div>
          <div class="product-actions">
            <button class="add-to-cart">カートに追加</button>
          </div>
        </div>

        <div class="product-card">
          <div class="product-image-placeholder">🏠</div>
          <div class="product-body">
            <div class="product-category">ホーム&キッチン</div>
            <h3 class="product-name">LED デスクライト</h3>
            <div class="product-price">
              <span class="current-price">¥4,980</span>
            </div>
            <div class="product-rating">
              <span class="stars">★★★☆☆</span>
              <span>(18)</span>
            </div>
          </div>
          <div class="product-actions">
            <button class="add-to-cart">カートに追加</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</body>
</html>
```

---

## 設問

### 設問1（基本理解）
`:root` で定義されているカスタムプロパティは何個ありますか？また、`--color-primary` の値が使われている箇所をすべて挙げてください。

### 設問2（基本理解）
`.header` に `position: sticky` が指定されています。これはどのような動作をしますか？`position: fixed` とどう違いますか？

### 設問3（レイアウト分析）
`.page` の Grid レイアウトはどのような構造ですか？列の幅はいくつですか？

### 設問4（レイアウト分析）
`.product-grid` で使われている `repeat(auto-fill, minmax(220px, 1fr))` はどのような動作をしますか？画面幅が 800px の場合、何列になるか計算してください（サイドバー240px + gap 32px + padding 48px を考慮）。

### 設問5（テクニック理解）
`.product-name` に指定されている `-webkit-line-clamp: 2` は何をするものですか？なぜ `overflow: hidden` と組み合わせて使われていますか？

### 設問6（テクニック理解）
`.search-bar::before` の疑似要素はどのように配置されていますか？`position: absolute` と `transform: translateY(-50%)` の組み合わせで何を実現していますか？

### 設問7（レスポンシブ分析）
768px以下の画面幅では、レイアウトはどのように変化しますか？具体的に変わる点を3つ挙げてください。

### 設問8（設計評価）
`.filters` に `position: sticky` と `align-self: start` が両方指定されています。なぜ `align-self: start` が必要なのですか？これがないとどうなりますか？

### 設問9（改善提案）
このコードにはアクセシビリティ（accessibility）の観点で改善すべき点があります。2つ以上指摘してください。

### 設問10（拡張設計）
このデザインに「商品をホバーしたときに『お気に入り』ハートボタンが右上に表示される」機能をCSSだけで追加するとしたら、どのようなセレクタとプロパティを使いますか？HTMLの変更箇所とCSSを書いてください。

---

## 解答例

<details>
<summary>設問1〜5の解答</summary>

### 設問1
**12個** のカスタムプロパティがあります（`--color-*` が8個、`--shadow-*` が2個、`--radius` が1個、計11個...正確に数えると11個です）。

`--color-primary` (`#2563eb`) が使われている箇所：
1. `.logo` の `color`
2. `.search-bar input:focus` の `border-color`
3. `.add-to-cart` の `background-color`

### 設問2
`position: sticky` は、通常のドキュメントフローに沿って配置されますが、スクロール時に `top: 0` の位置に「貼りつく」動作をします。

`position: fixed` との違い：
- `sticky` は親要素内でのみ固定され、親を超えてスクロールされると一緒に流れる
- `fixed` はビューポートに対して常に固定される
- `sticky` はスクロール前は通常の位置にいるため、他の要素のレイアウトに影響しない

### 設問3
`.page` は `grid-template-columns: 240px 1fr` で2列構成です。
- 左列（サイドバー）: 固定 240px
- 右列（メインコンテンツ）: 残りのスペースすべて（`1fr`）
- 列間のすき間: `gap: 32px`

### 設問4
`repeat(auto-fill, minmax(220px, 1fr))` は「最小220px、最大1frで列を自動的に埋める」動作をします。

計算：
- 画面幅 800px
- `padding: 24px * 2 = 48px` を引く → 752px
- サイドバー 240px + gap 32px を引く → 480px
- メインエリアで利用可能: 480px
- 480px / 220px = 2.18... → **2列** になります

### 設問5
`-webkit-line-clamp: 2` は、テキストを **2行で打ち切り**、超過分を省略記号（...）で表示するプロパティです。

`overflow: hidden` が必要な理由は、`-webkit-line-clamp` が効かないブラウザやフォールバックとして、テキストがボックスからはみ出さないようにするためです。`-webkit-box-orient: vertical` と `display: -webkit-box` も必須のセットです。

</details>

<details>
<summary>設問6〜10の解答</summary>

### 設問6
`.search-bar::before` は検索アイコンを配置する疑似要素です。

- `.search-bar` が `position: relative`（暗黙的な基準）
- `::before` に `position: absolute` で自由配置
- `left: 14px` で左端から14pxの位置
- `top: 50%` で上から50%の位置（要素の上端が中央に来る）
- `transform: translateY(-50%)` で要素自身の高さの半分だけ上にずらす

この「`top: 50%` + `transform: translateY(-50%)`」は **垂直中央揃え** の定番テクニックです。

### 設問7
768px以下で変わる点：

1. `.page` が `grid-template-columns: 1fr` になり、サイドバーとメインが **縦1列** になる
2. `.filters` が `position: static` になり、スクロール追従しなくなる。さらに `grid-template-columns: repeat(2, 1fr)` でフィルタ項目が **横2列** になる
3. `.search-bar` が `display: none` になり、検索バーが **非表示** になる

### 設問8
Grid コンテナの子要素はデフォルトで `align-self: stretch`（高さいっぱいに伸びる）です。

`align-self: start` がないと、`.filters` はメインコンテンツと同じ高さに引き伸ばされます。すると `position: sticky` の効果が失われます（要素自体がすでにコンテナいっぱいに広がっているため、スクロールで「貼りつく」ことがない）。

`align-self: start` で高さを内容分だけに制限することで、`sticky` が正常に機能します。

### 設問9
改善すべき点：

1. **検索バーに `<label>` がない** — `<input>` に `aria-label="商品を検索"` を追加すべきです。スクリーンリーダーが入力欄の目的を読み上げられません。
2. **カートボタンに `aria-label` がない** — 絵文字だけのボタンには `aria-label="カート（3件）"` を付けるべきです。
3. **色のコントラスト比が不十分な可能性** — `--color-text-muted: #64748b` は背景色 `#f8fafc` に対してWCAG AA基準を満たしているか検証が必要です。
4. **セール表示のバッジが視覚のみ** — スクリーンリーダー向けに `aria-label="30%オフ"` を設定すべきです。

### 設問10

HTMLの変更（各 `.product-card` 内に追加）:
```html
<button class="favorite-btn" aria-label="お気に入りに追加">♡</button>
```

CSSの追加:
```css
.favorite-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background-color: rgba(255, 255, 255, 0.9);
  font-size: 18px;
  cursor: pointer;
  opacity: 0;
  transform: scale(0.8);
  transition: opacity 0.2s, transform 0.2s;
  z-index: 1;
}

.product-card:hover .favorite-btn {
  opacity: 1;
  transform: scale(1);
}

.favorite-btn:hover {
  color: #ef4444;
  background-color: #ffffff;
}
```

ポイント：
- `.product-card` にはすでに `position: relative` が設定されているので、`absolute` で自由に配置できる
- `opacity: 0` で初期非表示、`:hover` で表示
- `transform: scale(0.8)` → `scale(1)` でポップイン演出を追加

</details>
