# 実践課題03：Flexboxナビゲーション ★2

> **難易度**: ★★☆☆☆（基礎）
> **前提知識**: 第1章（CSSの基本）、第3章（Flexbox）
> **課題の種類**: ミニプロジェクト
> **学習目標**: Flexboxの `justify-content`・`align-items`・`gap` を使い、実用的なナビゲーションバーを作る

---

## 完成イメージ

```
┌──────────────────────────────────────────────────┐
│  🏠 MyApp     ホーム  機能  料金  ブログ   [ログイン] │
│  ← ロゴ       ← ナビリンク →        ← ボタン →     │
└──────────────────────────────────────────────────┘

※ ロゴが左端、ナビリンクが中央付近、ログインボタンが右端に配置される
```

---

## 課題の要件

1. ナビゲーションバーを画面上部に固定表示する
2. ロゴを左端に配置する
3. ナビリンクを中央に配置する
4. ログインボタンを右端に配置する
5. リンクにホバー時のスタイル変化を付ける
6. 適切な高さ・余白・背景色を設定する

---

## ステップガイド

<details>
<summary>ステップ1：HTML構造を作る</summary>

ナビバーの中を3つのグループに分けます。

```html
<nav class="navbar">
  <div class="nav-logo">MyApp</div>
  <ul class="nav-links">
    <li><a href="#">ホーム</a></li>
    <li><a href="#">機能</a></li>
    <li><a href="#">料金</a></li>
    <li><a href="#">ブログ</a></li>
  </ul>
  <div class="nav-auth">
    <a href="#" class="btn-login">ログイン</a>
  </div>
</nav>
```

</details>

<details>
<summary>ステップ2：Flexboxで配置する</summary>

`nav` を Flexコンテナにし、`justify-content: space-between` で左・中央・右に分離します。

```css
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

リンクリストも Flex にして横並びにします。

```css
.nav-links {
  display: flex;
  list-style: none;
  gap: 24px;
}
```

</details>

<details>
<summary>ステップ3：固定ヘッダーにする</summary>

`position: fixed` でスクロールしても追従するようにします。

```css
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
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
  <title>ナビゲーションバー</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: sans-serif;
      padding-top: 64px; /* ナビバーの高さ分だけ余白 */
      color: #333333;
    }

    /* --- ナビバー --- */
    .navbar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 64px;
      background-color: #ffffff;
      border-bottom: 1px solid #e0e0e0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 32px;
      z-index: 100;
    }

    /* --- ロゴ --- */
    .nav-logo {
      font-size: 20px;
      font-weight: bold;
      color: #4a90d9;
    }

    /* --- ナビリンク --- */
    .nav-links {
      display: flex;
      list-style: none;
      gap: 32px;
    }

    .nav-links a {
      text-decoration: none;
      color: #555555;
      font-size: 14px;
      padding: 8px 0;
    }

    .nav-links a:hover {
      color: #4a90d9;
      border-bottom: 2px solid #4a90d9;
    }

    /* --- ログインボタン --- */
    .btn-login {
      text-decoration: none;
      color: #ffffff;
      background-color: #4a90d9;
      padding: 8px 20px;
      border-radius: 6px;
      font-size: 14px;
    }

    .btn-login:hover {
      background-color: #3a7bc8;
    }

    /* --- メインコンテンツ（動作確認用） --- */
    .content {
      max-width: 800px;
      margin: 40px auto;
      padding: 0 20px;
    }

    .content section {
      margin-bottom: 40px;
    }

    .content h2 {
      margin-bottom: 16px;
    }

    .content p {
      line-height: 1.8;
      color: #666666;
    }
  </style>
</head>
<body>
  <nav class="navbar">
    <div class="nav-logo">MyApp</div>
    <ul class="nav-links">
      <li><a href="#home">ホーム</a></li>
      <li><a href="#features">機能</a></li>
      <li><a href="#pricing">料金</a></li>
      <li><a href="#blog">ブログ</a></li>
    </ul>
    <div class="nav-auth">
      <a href="#" class="btn-login">ログイン</a>
    </div>
  </nav>

  <div class="content">
    <section id="home">
      <h2>ホーム</h2>
      <p>ここにメインコンテンツが入ります。スクロールしてナビゲーションバーが固定されることを確認してください。</p>
    </section>
    <section id="features">
      <h2>機能</h2>
      <p>ここに機能の説明が入ります。長いテキストを入れてスクロールできるようにしましょう。</p>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
    </section>
    <section id="pricing">
      <h2>料金</h2>
      <p>ここに料金プランの説明が入ります。</p>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
    </section>
    <section id="blog">
      <h2>ブログ</h2>
      <p>ここにブログの記事一覧が入ります。</p>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
    </section>
  </div>
</body>
</html>
```

</details>

<details>
<summary>解答例（改良版 ─ スクロール時に影が出る＆アクティブ状態付き）</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ナビゲーションバー（改良版）</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: "Helvetica Neue", Arial, sans-serif;
      padding-top: 64px;
      color: #333333;
      background-color: #fafafa;
    }

    /* --- ナビバー --- */
    .navbar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: 64px;
      background-color: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid rgba(0, 0, 0, 0.06);
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 40px;
      z-index: 100;
      transition: box-shadow 0.3s;
    }

    /* --- ロゴ --- */
    .nav-logo {
      font-size: 22px;
      font-weight: 800;
      background: linear-gradient(135deg, #667eea, #764ba2);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    /* --- ナビリンク --- */
    .nav-links {
      display: flex;
      list-style: none;
      gap: 8px;
    }

    .nav-links a {
      text-decoration: none;
      color: #666666;
      font-size: 14px;
      font-weight: 500;
      padding: 8px 16px;
      border-radius: 6px;
      transition: color 0.2s, background-color 0.2s;
    }

    .nav-links a:hover {
      color: #333333;
      background-color: #f0f0f0;
    }

    .nav-links a.active {
      color: #667eea;
      background-color: #eef0ff;
    }

    /* --- 認証ボタン --- */
    .nav-auth {
      display: flex;
      gap: 12px;
      align-items: center;
    }

    .btn-ghost {
      text-decoration: none;
      color: #666666;
      font-size: 14px;
      font-weight: 500;
      padding: 8px 16px;
      border-radius: 6px;
      transition: color 0.2s;
    }

    .btn-ghost:hover {
      color: #333333;
    }

    .btn-primary {
      text-decoration: none;
      color: #ffffff;
      background: linear-gradient(135deg, #667eea, #764ba2);
      padding: 8px 20px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 600;
      transition: opacity 0.2s;
    }

    .btn-primary:hover {
      opacity: 0.9;
    }

    /* --- メインコンテンツ --- */
    .content {
      max-width: 800px;
      margin: 40px auto;
      padding: 0 20px;
    }

    .content section {
      background: #ffffff;
      border-radius: 12px;
      padding: 32px;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    }

    .content h2 {
      margin-bottom: 16px;
      font-size: 20px;
    }

    .content p {
      line-height: 1.8;
      color: #666666;
      margin-bottom: 12px;
    }
  </style>
</head>
<body>
  <nav class="navbar">
    <div class="nav-logo">MyApp</div>
    <ul class="nav-links">
      <li><a href="#home" class="active">ホーム</a></li>
      <li><a href="#features">機能</a></li>
      <li><a href="#pricing">料金</a></li>
      <li><a href="#blog">ブログ</a></li>
    </ul>
    <div class="nav-auth">
      <a href="#" class="btn-ghost">ログイン</a>
      <a href="#" class="btn-primary">無料で始める</a>
    </div>
  </nav>

  <div class="content">
    <section id="home">
      <h2>ホーム</h2>
      <p>ここにメインコンテンツが入ります。スクロールしてナビゲーションバーが固定されることを確認してください。</p>
    </section>
    <section id="features">
      <h2>機能</h2>
      <p>ここに機能の説明が入ります。長いテキストを入れてスクロールできるようにしましょう。</p>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
    </section>
    <section id="pricing">
      <h2>料金</h2>
      <p>ここに料金プランの説明が入ります。</p>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
    </section>
    <section id="blog">
      <h2>ブログ</h2>
      <p>ここにブログの記事一覧が入ります。</p>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
    </section>
  </div>
</body>
</html>
```

**初心者向けとの違い:**
- `backdrop-filter: blur()` で背景がすりガラス風になる（モダンなUIでよく使われるテクニック）
- アクティブ（現在のページ）リンクを `background-color` で強調
- リンクのホバー時に背景色を付けるピル型デザイン
- ロゴにグラデーションテキストを適用
- ゴーストボタン（枠なし）とプライマリボタンの2種を使い分け

</details>
