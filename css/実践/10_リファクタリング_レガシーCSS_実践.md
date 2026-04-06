# 実践課題10：リファクタリング ─ レガシーCSS ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第1章〜第4章（基本・ボックスモデル・Flexbox・Grid）、第7章（カスタムプロパティ）
> **課題の種類**: リファクタリング
> **学習目標**: 古い書き方や冗長なCSSを読み解き、モダンなCSS（Flexbox・Grid・カスタムプロパティ）で書き直す力を養う

---

## 課題の説明

以下のCSSは「社内ポータルサイトのダッシュボード」です。**正しく動作します**が、以下の問題を抱えています。

- `float` を使った古いレイアウト手法
- `clearfix` ハック
- 同じ色コードやフォントサイズの繰り返し（マジックナンバー）
- 深いセレクタのネスト
- `!important` の乱用
- レスポンシブ対応がない

**このCSSを段階的にリファクタリングしてください。**

### ゴール

1. **ステップ1**: `float` を Flexbox / Grid に置き換える
2. **ステップ2**: 繰り返しの値をカスタムプロパティにまとめる
3. **ステップ3**: セレクタを整理し、`!important` を削除する
4. **ステップ4**: レスポンシブ対応を追加する

---

## リファクタリング対象のコード

以下を `dashboard_legacy.html` として保存してください。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>ダッシュボード（レガシー版）</title>
  <style>
    /* === レガシーCSS === */
    /* 問題1: 同じ色コードが何度も登場する */
    body {
      margin: 0;
      padding: 0;
      font-family: Arial, sans-serif;
      background-color: #f5f5f5;
      color: #333333;
    }

    /* clearfix ハック（float解除用） */
    .clearfix::after {
      content: "";
      display: table;
      clear: both;
    }

    /* === ヘッダー === */
    .header {
      background-color: #2c3e50;
      color: #ffffff;
      height: 60px;
      line-height: 60px;
      padding: 0 20px;
    }

    /* 問題2: 深すぎるセレクタ */
    .header .header-inner .logo {
      float: left;
      font-size: 20px;
      font-weight: bold;
    }

    .header .header-inner .nav {
      float: right;
    }

    .header .header-inner .nav ul {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    .header .header-inner .nav ul li {
      float: left;
      margin-left: 20px;
    }

    .header .header-inner .nav ul li a {
      color: #ffffff;
      text-decoration: none;
      font-size: 14px;
    }

    /* === コンテンツエリア === */
    .content {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }

    /* === 統計カード === */
    /* 問題3: floatレイアウト */
    .stats-row {
      margin: 0 -10px;
    }

    .stat-card {
      float: left;
      width: 25%;
      padding: 0 10px;
      margin-bottom: 20px;
    }

    .stat-card-inner {
      background-color: #ffffff;
      border-radius: 8px;
      padding: 20px;
      /* 問題4: box-shadow のマジックナンバー */
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .stat-card-inner .stat-value {
      font-size: 32px;
      font-weight: bold;
      color: #2c3e50;
    }

    .stat-card-inner .stat-label {
      font-size: 14px;
      color: #888888;
      margin-top: 4px;
    }

    /* 問題5: !important の乱用 */
    .stat-card-inner.accent-blue .stat-value {
      color: #3498db !important;
    }

    .stat-card-inner.accent-green .stat-value {
      color: #27ae60 !important;
    }

    .stat-card-inner.accent-orange .stat-value {
      color: #f39c12 !important;
    }

    .stat-card-inner.accent-red .stat-value {
      color: #e74c3c !important;
    }

    /* === メインとサイドバー === */
    /* 問題6: float レイアウト */
    .main-area {
      float: left;
      width: 70%;
      padding-right: 20px;
    }

    .sidebar {
      float: left;
      width: 30%;
    }

    /* === テーブル === */
    .panel {
      background-color: #ffffff;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .panel .panel-title {
      font-size: 18px;
      font-weight: bold;
      color: #2c3e50;
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid #eeeeee;
    }

    .data-table {
      width: 100%;
      border-collapse: collapse;
    }

    .data-table th {
      text-align: left;
      padding: 10px 8px;
      font-size: 12px;
      color: #888888;
      border-bottom: 2px solid #eeeeee;
      text-transform: uppercase;
    }

    .data-table td {
      padding: 10px 8px;
      font-size: 14px;
      border-bottom: 1px solid #f5f5f5;
    }

    /* 問題7: 状態によるスタイルが冗長 */
    .status-badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: bold;
    }

    .status-badge.status-active {
      background-color: #d4edda;
      color: #155724;
    }

    .status-badge.status-pending {
      background-color: #fff3cd;
      color: #856404;
    }

    .status-badge.status-inactive {
      background-color: #f8d7da;
      color: #721c24;
    }

    /* === サイドバーウィジェット === */
    .widget-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }

    .widget-list li {
      padding: 12px 0;
      border-bottom: 1px solid #f0f0f0;
      font-size: 14px;
      color: #555555;
    }

    .widget-list li:last-child {
      border-bottom: none;
    }

    .widget-list li .widget-count {
      float: right;
      background-color: #3498db;
      color: #ffffff;
      font-size: 12px;
      padding: 2px 8px;
      border-radius: 10px;
    }
  </style>
</head>
<body>
  <header class="header">
    <div class="header-inner clearfix">
      <div class="logo">Dashboard</div>
      <nav class="nav">
        <ul>
          <li><a href="#">ホーム</a></li>
          <li><a href="#">レポート</a></li>
          <li><a href="#">設定</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <div class="content clearfix">
    <!-- 統計カード -->
    <div class="stats-row clearfix">
      <div class="stat-card">
        <div class="stat-card-inner accent-blue">
          <div class="stat-value">1,234</div>
          <div class="stat-label">ユーザー数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-card-inner accent-green">
          <div class="stat-value">567</div>
          <div class="stat-label">新規登録（今月）</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-card-inner accent-orange">
          <div class="stat-value">89%</div>
          <div class="stat-label">稼働率</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-card-inner accent-red">
          <div class="stat-value">12</div>
          <div class="stat-label">未対応チケット</div>
        </div>
      </div>
    </div>

    <!-- メイン + サイドバー -->
    <div class="main-area">
      <div class="panel">
        <h2 class="panel-title">最近のアクティビティ</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>ユーザー</th>
              <th>アクション</th>
              <th>日時</th>
              <th>ステータス</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>田中太郎</td>
              <td>ログイン</td>
              <td>2024-03-15 09:30</td>
              <td><span class="status-badge status-active">アクティブ</span></td>
            </tr>
            <tr>
              <td>佐藤花子</td>
              <td>レポート作成</td>
              <td>2024-03-15 10:15</td>
              <td><span class="status-badge status-pending">保留中</span></td>
            </tr>
            <tr>
              <td>鈴木一郎</td>
              <td>ファイルアップロード</td>
              <td>2024-03-14 16:45</td>
              <td><span class="status-badge status-inactive">非アクティブ</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <aside class="sidebar">
      <div class="panel">
        <h2 class="panel-title">お知らせ</h2>
        <ul class="widget-list">
          <li>システムメンテナンスのお知らせ <span class="widget-count">新着</span></li>
          <li>新機能リリースのご案内 <span class="widget-count">3</span></li>
          <li>セキュリティアップデート <span class="widget-count">1</span></li>
        </ul>
      </div>
    </aside>
  </div>
</body>
</html>
```

---

## ステップガイド

<details>
<summary>ステップ1：float を Flexbox / Grid に置き換える</summary>

以下の3箇所で `float` が使われています。それぞれ最適な方法で置き換えましょう。

1. **ヘッダー** (`float: left/right`) → `display: flex` + `justify-content: space-between`
2. **統計カード** (`float: left; width: 25%`) → `display: grid` + `grid-template-columns: repeat(4, 1fr)`
3. **メイン+サイドバー** (`float: left; width: 70%/30%`) → `display: grid` + `grid-template-columns: 1fr 300px`

また、`clearfix` クラスと `.clearfix::after` のCSSは不要になるので削除します。

</details>

<details>
<summary>ステップ2：カスタムプロパティにまとめる</summary>

繰り返されている値を洗い出します。

```
#2c3e50 → 3回使われている → --color-heading
#ffffff → 多数 → --color-surface
#888888 → 2回 → --color-text-muted
#f5f5f5 → 2回 → --color-bg
0 2px 4px rgba(0,0,0,0.1) → 2回 → --shadow
```

`:root` にまとめ、`var()` で参照します。

</details>

<details>
<summary>ステップ3：セレクタ整理と !important 削除</summary>

深すぎるセレクタ `.header .header-inner .nav ul li a` は `.nav-link` のような1クラスに変更します。

`!important` は詳細度の問題で使われていたので、セレクタの詳細度を調整すれば不要になります。

</details>

<details>
<summary>ステップ4：レスポンシブ対応を追加</summary>

```css
@media (max-width: 1024px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: 1fr;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け ─ 段階的にリファクタリング）</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ダッシュボード（リファクタリング版）</title>
  <style>
    /* ステップ2: カスタムプロパティ */
    :root {
      --color-bg: #f5f5f5;
      --color-surface: #ffffff;
      --color-text: #333333;
      --color-text-muted: #888888;
      --color-heading: #2c3e50;
      --color-primary: #3498db;
      --color-border: #eeeeee;
      --shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      --radius: 8px;
    }

    /* ステップ3: リセット */
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: Arial, sans-serif;
      background-color: var(--color-bg);
      color: var(--color-text);
    }

    /* clearfix は不要になったので削除 */

    /* ステップ1: ヘッダーを Flexbox に */
    .header {
      background-color: var(--color-heading);
      color: #ffffff;
      height: 60px;
      padding: 0 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .logo {
      font-size: 20px;
      font-weight: bold;
    }

    /* ステップ3: セレクタを浅くする */
    .nav ul {
      list-style: none;
      display: flex;
      gap: 20px;
    }

    .nav a {
      color: #ffffff;
      text-decoration: none;
      font-size: 14px;
    }

    .content {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }

    /* ステップ1: 統計カードを Grid に */
    .stats-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      margin-bottom: 20px;
    }

    /* float や width は不要になった */
    .stat-card-inner {
      background-color: var(--color-surface);
      border-radius: var(--radius);
      padding: 20px;
      box-shadow: var(--shadow);
    }

    .stat-value {
      font-size: 32px;
      font-weight: bold;
      color: var(--color-heading);
    }

    .stat-label {
      font-size: 14px;
      color: var(--color-text-muted);
      margin-top: 4px;
    }

    /* ステップ3: !important を削除 */
    .accent-blue .stat-value  { color: #3498db; }
    .accent-green .stat-value { color: #27ae60; }
    .accent-orange .stat-value { color: #f39c12; }
    .accent-red .stat-value   { color: #e74c3c; }

    /* ステップ1: メイン+サイドバーを Grid に */
    .content-grid {
      display: grid;
      grid-template-columns: 1fr 300px;
      gap: 20px;
    }

    .panel {
      background-color: var(--color-surface);
      border-radius: var(--radius);
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: var(--shadow);
    }

    .panel-title {
      font-size: 18px;
      font-weight: bold;
      color: var(--color-heading);
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--color-border);
    }

    .data-table {
      width: 100%;
      border-collapse: collapse;
    }

    .data-table th {
      text-align: left;
      padding: 10px 8px;
      font-size: 12px;
      color: var(--color-text-muted);
      border-bottom: 2px solid var(--color-border);
      text-transform: uppercase;
    }

    .data-table td {
      padding: 10px 8px;
      font-size: 14px;
      border-bottom: 1px solid var(--color-bg);
    }

    .status-badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: bold;
    }

    .status-active   { background-color: #d4edda; color: #155724; }
    .status-pending  { background-color: #fff3cd; color: #856404; }
    .status-inactive { background-color: #f8d7da; color: #721c24; }

    .widget-list {
      list-style: none;
    }

    .widget-list li {
      padding: 12px 0;
      border-bottom: 1px solid #f0f0f0;
      font-size: 14px;
      color: #555555;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .widget-list li:last-child {
      border-bottom: none;
    }

    .widget-count {
      background-color: var(--color-primary);
      color: #ffffff;
      font-size: 12px;
      padding: 2px 8px;
      border-radius: 10px;
    }

    /* ステップ4: レスポンシブ対応 */
    @media (max-width: 1024px) {
      .stats-row {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    @media (max-width: 768px) {
      .stats-row {
        grid-template-columns: 1fr;
      }

      .content-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <header class="header">
    <div class="logo">Dashboard</div>
    <nav class="nav">
      <ul>
        <li><a href="#">ホーム</a></li>
        <li><a href="#">レポート</a></li>
        <li><a href="#">設定</a></li>
      </ul>
    </nav>
  </header>

  <div class="content">
    <div class="stats-row">
      <div class="stat-card-inner accent-blue">
        <div class="stat-value">1,234</div>
        <div class="stat-label">ユーザー数</div>
      </div>
      <div class="stat-card-inner accent-green">
        <div class="stat-value">567</div>
        <div class="stat-label">新規登録（今月）</div>
      </div>
      <div class="stat-card-inner accent-orange">
        <div class="stat-value">89%</div>
        <div class="stat-label">稼働率</div>
      </div>
      <div class="stat-card-inner accent-red">
        <div class="stat-value">12</div>
        <div class="stat-label">未対応チケット</div>
      </div>
    </div>

    <div class="content-grid">
      <main>
        <div class="panel">
          <h2 class="panel-title">最近のアクティビティ</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>ユーザー</th>
                <th>アクション</th>
                <th>日時</th>
                <th>ステータス</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>田中太郎</td>
                <td>ログイン</td>
                <td>2024-03-15 09:30</td>
                <td><span class="status-badge status-active">アクティブ</span></td>
              </tr>
              <tr>
                <td>佐藤花子</td>
                <td>レポート作成</td>
                <td>2024-03-15 10:15</td>
                <td><span class="status-badge status-pending">保留中</span></td>
              </tr>
              <tr>
                <td>鈴木一郎</td>
                <td>ファイルアップロード</td>
                <td>2024-03-14 16:45</td>
                <td><span class="status-badge status-inactive">非アクティブ</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </main>

      <aside>
        <div class="panel">
          <h2 class="panel-title">お知らせ</h2>
          <ul class="widget-list">
            <li>システムメンテナンスのお知らせ <span class="widget-count">新着</span></li>
            <li>新機能リリースのご案内 <span class="widget-count">3</span></li>
            <li>セキュリティアップデート <span class="widget-count">1</span></li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</body>
</html>
```

</details>

<details>
<summary>改善ポイントの解説</summary>

### 変更点のまとめ

| 改善項目 | Before（レガシー） | After（モダン） |
|---|---|---|
| レイアウト | `float` + `clearfix` | Flexbox / Grid |
| 色の管理 | ハードコーディング | カスタムプロパティ |
| セレクタ | `.header .header-inner .nav ul li a` | `.nav a` |
| 詳細度制御 | `!important` | セレクタの調整 |
| レスポンシブ | なし | メディアクエリ追加 |
| HTML構造 | `.stat-card` > `.stat-card-inner` の二重構造 | `.stat-card-inner` 1つに統合 |
| リスト項目の配置 | `float: right` | `display: flex` + `justify-content: space-between` |

### なぜ float を避けるべきか

- `float` は本来テキストの回り込み用であり、レイアウト用途はハック
- `clearfix` が必要になるなど、余分なコードが増える
- 垂直方向の中央揃えが困難
- Flexbox や Grid のほうが意図が明確で、保守しやすい

### なぜ !important を避けるべきか

- CSSの詳細度（specificity）の仕組みを無視する「最終手段」
- 一度使い始めると、上書きに `!important` が必要になる悪循環に陥る
- セレクタの詳細度を適切に設計すれば不要

</details>
