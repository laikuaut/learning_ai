# 第6章：セマンティックHTML

## この章のゴール
- セマンティックHTMLの概念と、なぜ重要かを理解する
- header / nav / main / section / article / aside / footer の使い分けを習得する
- 適切なランドマーク要素を使ってページの構造を設計できる
- WAI-ARIA の基礎（role, aria-label, aria-hidden 等）を理解し、適切に使えるようになる
- アクセシビリティと SEO の両方に配慮したHTMLを書けるようになる

---

## 6.1 セマンティックHTMLとは

「セマンティック」とは「意味のある」という意味です。セマンティックHTMLとは、**コンテンツの意味や役割を適切に表現するHTML要素を使うこと**を指します。

### 非セマンティック vs セマンティック

```html
<!-- 非セマンティック：divとspanだけで構築 -->
<div id="header">
  <div id="nav">
    <div class="nav-item"><a href="/">ホーム</a></div>
    <div class="nav-item"><a href="/about">概要</a></div>
  </div>
</div>
<div id="main">
  <div class="article">
    <div class="article-title">記事タイトル</div>
    <div class="article-body">記事本文...</div>
  </div>
</div>
<div id="footer">
  <div class="copyright">Copyright 2024</div>
</div>

<!-- セマンティック：意味のある要素を使用 -->
<header>
  <nav>
    <ul>
      <li><a href="/">ホーム</a></li>
      <li><a href="/about">概要</a></li>
    </ul>
  </nav>
</header>
<main>
  <article>
    <h2>記事タイトル</h2>
    <p>記事本文...</p>
  </article>
</main>
<footer>
  <p><small>Copyright 2024</small></p>
</footer>
```

### セマンティックHTMLのメリット

| メリット | 説明 |
|---|---|
| **アクセシビリティ** | スクリーンリーダーが構造を正しく伝えられる |
| **SEO** | 検索エンジンがコンテンツの役割を理解しやすい |
| **保守性** | コードを読むだけで構造が把握できる |
| **機械可読性** | ブラウザの「リーダーモード」等が正しく機能する |
| **一貫性** | 開発者間で共通の構造パターンが使える |

---

## 6.2 ページ構造の全体像

典型的なWebページは以下のような構造になります。

```
+-----------------------------------------------+
|  <header>                                     |
|    サイトロゴ、サイトタイトル                    |
|    <nav> メインナビゲーション </nav>            |
|  </header>                                    |
+-----------------------------------------------+
|  <main>                                       |
|  +-------------------------+ +-----------+    |
|  | <article>               | | <aside>   |    |
|  |   <section>             | |  サイド    |    |
|  |     コンテンツ...        | |  バー     |    |
|  |   </section>            | |           |    |
|  |   <section>             | |           |    |
|  |     コンテンツ...        | |           |    |
|  |   </section>            | |           |    |
|  | </article>              | |           |    |
|  +-------------------------+ +-----------+    |
|  </main>                                      |
+-----------------------------------------------+
|  <footer>                                     |
|    コピーライト、リンク集                       |
|  </footer>                                    |
+-----------------------------------------------+
```

---

## 6.3 header要素

`<header>` は導入的なコンテンツやナビゲーションのグループを表します。

```html
<!-- ページ全体のヘッダー -->
<header>
  <h1>My Website</h1>
  <nav>
    <ul>
      <li><a href="/">ホーム</a></li>
      <li><a href="/blog">ブログ</a></li>
      <li><a href="/contact">お問い合わせ</a></li>
    </ul>
  </nav>
</header>

<!-- 記事のヘッダー -->
<article>
  <header>
    <h2>記事のタイトル</h2>
    <p>投稿日：<time datetime="2024-03-15">2024年3月15日</time></p>
    <p>著者：田中太郎</p>
  </header>
  <p>記事の本文...</p>
</article>
```

### headerの特徴
- ページ全体のヘッダーにも、article / section 内のヘッダーにも使える
- 1つのページに**複数の `<header>` を配置**してよい
- `<header>` の中に `<header>` や `<footer>` を入れることはできない

---

## 6.4 nav要素

`<nav>` はナビゲーションリンクのセクションを表します。

```html
<!-- メインナビゲーション -->
<nav aria-label="メインナビゲーション">
  <ul>
    <li><a href="/">ホーム</a></li>
    <li><a href="/products">製品</a></li>
    <li><a href="/about">会社概要</a></li>
    <li><a href="/contact">お問い合わせ</a></li>
  </ul>
</nav>

<!-- パンくずリスト -->
<nav aria-label="パンくずリスト">
  <ol>
    <li><a href="/">ホーム</a></li>
    <li><a href="/products">製品</a></li>
    <li aria-current="page">製品A</li>
  </ol>
</nav>

<!-- ページ内目次 -->
<nav aria-label="目次">
  <h2>目次</h2>
  <ul>
    <li><a href="#section1">セクション1</a></li>
    <li><a href="#section2">セクション2</a></li>
    <li><a href="#section3">セクション3</a></li>
  </ul>
</nav>
```

### navの使用指針
- **すべてのリンクのまとまりに使うわけではない**
- ページ内の主要なナビゲーションブロックに限定して使う
- フッター内のリンク集にはnavを使わなくてもよい（使ってもよい）
- 複数の `<nav>` がある場合は `aria-label` で区別する

---

## 6.5 main要素

`<main>` はページの**主要なコンテンツ**を表します。

```html
<body>
  <header>...</header>
  <nav>...</nav>
  <main>
    <h1>記事のタイトル</h1>
    <p>ここがメインコンテンツです。</p>
  </main>
  <footer>...</footer>
</body>
```

### mainの重要なルール
- **1ページに1つだけ**（複数配置しない）
- `<header>`, `<footer>`, `<nav>`, `<aside>` の**中に入れない**
- ページ固有のコンテンツを入れる（サイト共通のヘッダーやナビは入れない）
- スクリーンリーダーの「メインコンテンツへスキップ」機能で使われる

---

## 6.6 section要素

`<section>` はドキュメントのテーマ別セクション（区画）を表します。

```html
<main>
  <section>
    <h2>会社概要</h2>
    <p>当社は2010年に設立されました...</p>
  </section>

  <section>
    <h2>サービス一覧</h2>
    <ul>
      <li>Webサイト制作</li>
      <li>アプリ開発</li>
      <li>コンサルティング</li>
    </ul>
  </section>

  <section>
    <h2>お客様の声</h2>
    <blockquote>
      <p>素晴らしいサービスでした。</p>
    </blockquote>
  </section>
</main>
```

### sectionの使用指針
- **必ず見出し（h1〜h6）を含める**のが原則
- 汎用的なコンテナとして使うなら `<div>` が適切
- 「このまとまりにタイトルを付けられるか？」を判断基準にする

---

## 6.7 article要素

`<article>` は**自己完結型のコンテンツ**を表します。単独で配信しても意味が通じるコンテンツです。

```html
<!-- ブログ記事 -->
<article>
  <header>
    <h2>JavaScriptの非同期処理入門</h2>
    <p>著者：田中太郎 | <time datetime="2024-03-15">2024年3月15日</time></p>
  </header>
  <p>非同期処理とは...</p>
  <footer>
    <p>カテゴリ：プログラミング</p>
  </footer>
</article>

<!-- コメント（記事内にネストされたarticle） -->
<article>
  <h2>記事タイトル</h2>
  <p>記事本文...</p>

  <section>
    <h3>コメント</h3>
    <article>
      <header>
        <p><strong>鈴木花子</strong> - <time datetime="2024-03-16">3月16日</time></p>
      </header>
      <p>とても参考になりました！</p>
    </article>
    <article>
      <header>
        <p><strong>佐藤次郎</strong> - <time datetime="2024-03-17">3月17日</time></p>
      </header>
      <p>わかりやすい解説ですね。</p>
    </article>
  </section>
</article>
```

### articleの使用場面
- ブログの記事
- ニュースの記事
- フォーラムの投稿
- コメント
- 商品カード
- ウィジェット

### article と section の違い
| 要素 | 意味 | 自己完結 | 例 |
|---|---|---|---|
| `<article>` | 独立したコンテンツ | する | ブログ記事、ニュース |
| `<section>` | テーマ別の区画 | しない | 章、タブ、コンテンツの区切り |

> **判断基準**: 「このコンテンツだけを別のページに切り出しても意味が通じるか？」通じるなら `<article>`、通じないなら `<section>` です。

---

## 6.8 aside要素

`<aside>` は本文の補足的な内容を表します。

```html
<!-- サイドバー -->
<aside>
  <h2>関連記事</h2>
  <ul>
    <li><a href="/post/1">CSS入門</a></li>
    <li><a href="/post/2">JavaScript基礎</a></li>
  </ul>
</aside>

<!-- 本文中の補足情報 -->
<article>
  <h2>HTMLの歴史</h2>
  <p>HTMLは1993年に最初の仕様が公開されました...</p>
  <aside>
    <h3>豆知識</h3>
    <p>HTMLを発明したのはティム・バーナーズ＝リーです。</p>
  </aside>
  <p>その後、HTML 2.0、3.2 と進化しました...</p>
</article>
```

### asideの使用場面
- サイドバー
- 関連記事リンク
- 広告
- 用語の補足説明
- プルクォート（記事の一部を強調表示）

---

## 6.9 footer要素

`<footer>` はセクションやページのフッター（末尾の情報）を表します。

```html
<!-- ページ全体のフッター -->
<footer>
  <nav aria-label="フッターナビゲーション">
    <ul>
      <li><a href="/privacy">プライバシーポリシー</a></li>
      <li><a href="/terms">利用規約</a></li>
      <li><a href="/sitemap">サイトマップ</a></li>
    </ul>
  </nav>
  <p><small>&copy; 2024 My Website. All rights reserved.</small></p>
</footer>

<!-- 記事のフッター -->
<article>
  <h2>記事タイトル</h2>
  <p>記事本文...</p>
  <footer>
    <p>投稿日：<time datetime="2024-03-15">2024年3月15日</time></p>
    <p>タグ：HTML, セマンティクス</p>
    <p>著者：<a href="/author/tanaka">田中太郎</a></p>
  </footer>
</article>
```

---

## 6.10 その他のセマンティック要素

### address要素：連絡先情報
```html
<footer>
  <address>
    <p>お問い合わせ先：</p>
    <p>メール：<a href="mailto:info@example.com">info@example.com</a></p>
    <p>電話：<a href="tel:03-1234-5678">03-1234-5678</a></p>
  </address>
</footer>
```

- 最も近い `<article>` または `<body>` の連絡先を表す
- 物理的な住所だけでなく、メール・電話・SNSリンクも含む

### blockquote要素：引用ブロック
```html
<blockquote cite="https://example.com/source">
  <p>良いコードとは、コメントがなくても理解できるコードのことだ。</p>
</blockquote>
<p>— マーティン・ファウラー</p>
```

### time要素：日時
```html
<p>会議は<time datetime="2024-03-15T14:00">3月15日午後2時</time>からです。</p>
<p>締め切り：<time datetime="2024-12-31">2024年末</time></p>
```

### mark要素：ハイライト
```html
<p>検索結果：HTMLの<mark>セマンティック</mark>要素について</p>
```

---

## 6.11 セマンティック要素の選び方フローチャート

コンテンツに合った要素を選ぶための判断基準です。

```
そのコンテンツは...

├── ページの導入部・ロゴ・ナビか？ → <header>
├── 主要なナビゲーションか？ → <nav>
├── ページの主要コンテンツか？ → <main>
├── 独立して意味が通じるか？ → <article>
├── テーマ別の区画か？ → <section>
├── 補足的な内容か？ → <aside>
├── 末尾の情報（著者・日付等）か？ → <footer>
├── 連絡先情報か？ → <address>
├── 他のどれにも当てはまらないか？ → <div>
```

> **ポイント**: `<div>` は「セマンティクスを持たない汎用コンテナ」です。CSSやJavaScriptのための入れ物として使いますが、セマンティックな意味がある場合は他の要素を優先してください。

---

## 6.12 WAI-ARIAの基礎

WAI-ARIA（Web Accessibility Initiative - Accessible Rich Internet Applications）は、HTMLだけでは伝えきれないアクセシビリティ情報を補完する仕様です。

### ARIAの3つの柱

#### 1. ロール（role）
要素の役割を明示します。

```html
<!-- セマンティック要素がない場合の代替 -->
<div role="navigation">
  <a href="/">ホーム</a>
  <a href="/about">概要</a>
</div>

<!-- カスタムUIに役割を付ける -->
<div role="tablist">
  <button role="tab" aria-selected="true">タブ1</button>
  <button role="tab" aria-selected="false">タブ2</button>
</div>
<div role="tabpanel">タブ1の内容</div>
```

> **重要**: セマンティックHTML要素が使える場合は、role属性ではなく**セマンティック要素を使う**のが原則です。`<div role="navigation">` より `<nav>` を使いましょう。

#### 2. プロパティ（aria-*）
要素の追加情報を提供します。

```html
<!-- ラベル付け -->
<button aria-label="メニューを開く">
  ☰
</button>

<nav aria-label="メインナビゲーション">...</nav>
<nav aria-label="フッターナビゲーション">...</nav>

<!-- 説明の参照 -->
<input type="password" aria-describedby="pw-hint">
<p id="pw-hint">8文字以上で、大文字と数字を含めてください。</p>
```

#### 3. ステート（状態）
要素の現在の状態を示します。

```html
<!-- 展開/折りたたみ -->
<button aria-expanded="false" aria-controls="menu">メニュー</button>
<ul id="menu" hidden>
  <li>項目1</li>
  <li>項目2</li>
</ul>

<!-- 選択状態 -->
<li role="option" aria-selected="true">選択済み</li>
<li role="option" aria-selected="false">未選択</li>

<!-- 無効状態 -->
<button aria-disabled="true">送信（無効）</button>
```

### よく使うARIA属性

| 属性 | 説明 | 例 |
|---|---|---|
| `aria-label` | 要素のラベル（テキストがない要素に） | `aria-label="閉じる"` |
| `aria-labelledby` | 別要素のテキストをラベルとして参照 | `aria-labelledby="title-id"` |
| `aria-describedby` | 補足説明を別要素から参照 | `aria-describedby="hint-id"` |
| `aria-hidden` | スクリーンリーダーから隠す | `aria-hidden="true"` |
| `aria-expanded` | 展開/折りたたみの状態 | `aria-expanded="false"` |
| `aria-controls` | 制御する対象の要素を指定 | `aria-controls="panel-id"` |
| `aria-current` | 現在のページや項目を示す | `aria-current="page"` |
| `aria-live` | 動的に変化する領域を通知 | `aria-live="polite"` |
| `aria-required` | 必須入力であることを示す | `aria-required="true"` |

### aria-hidden の使い方

装飾的な要素をスクリーンリーダーから隠すために使います。

```html
<!-- アイコンフォントを隠す -->
<button>
  <span aria-hidden="true">★</span>
  お気に入りに追加
</button>

<!-- 装飾画像を隠す -->
<img src="decoration.png" alt="" aria-hidden="true">
```

> **注意**: `aria-hidden="true"` を付けた要素の中にフォーカス可能な要素（リンク、ボタン等）を入れてはいけません。

### aria-live：動的コンテンツの通知

```html
<!-- 検索結果の件数が変わったら読み上げる -->
<p aria-live="polite">検索結果：<span id="count">0</span>件</p>

<!-- エラーメッセージを即座に読み上げる -->
<div role="alert" aria-live="assertive">
  入力内容にエラーがあります。
</div>
```

| 値 | 動作 |
|---|---|
| `off` | 通知しない（デフォルト） |
| `polite` | ユーザーの操作が終わってから通知 |
| `assertive` | 即座に通知（緊急時のみ使用） |

---

## 6.13 ARIAの「第一ルール」

> **ARIAの第一ルール**: ネイティブHTMLの要素や属性で目的を達成できる場合は、ARIAを使うべきではない。

```html
<!-- 悪い例：ARIAで無理やり役割を付けている -->
<div role="button" tabindex="0" onclick="submit()">送信</div>

<!-- 良い例：ネイティブのbutton要素を使う -->
<button onclick="submit()">送信</button>
```

```html
<!-- 悪い例 -->
<div role="navigation">...</div>

<!-- 良い例 -->
<nav>...</nav>
```

```html
<!-- 悪い例 -->
<span role="checkbox" aria-checked="true" tabindex="0">✓</span>

<!-- 良い例 -->
<input type="checkbox" checked>
```

---

## 6.14 実践：セマンティックなブログページ

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Blog - HTMLの基礎を学ぼう</title>
  <style>
    body { font-family: sans-serif; max-width: 960px; margin: 0 auto; padding: 0 1em; }
    header { border-bottom: 2px solid #333; padding: 1em 0; }
    nav ul { list-style: none; padding: 0; display: flex; gap: 1em; }
    main { display: flex; gap: 2em; margin: 1em 0; }
    article { flex: 3; }
    aside { flex: 1; background: #f5f5f5; padding: 1em; border-radius: 8px; }
    footer { border-top: 1px solid #ccc; padding: 1em 0; text-align: center; }
  </style>
</head>
<body>
  <header>
    <h1>My Blog</h1>
    <nav aria-label="メインナビゲーション">
      <ul>
        <li><a href="/" aria-current="page">ホーム</a></li>
        <li><a href="/archive">アーカイブ</a></li>
        <li><a href="/about">このブログについて</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <article>
      <header>
        <h2>HTMLの基礎を学ぼう</h2>
        <p>
          <time datetime="2024-03-15">2024年3月15日</time> |
          カテゴリ：プログラミング
        </p>
      </header>

      <section>
        <h3>HTMLとは</h3>
        <p>HTMLはWebページの構造を記述する言語です...</p>
      </section>

      <section>
        <h3>セマンティック要素の重要性</h3>
        <p>セマンティック要素を使うと...</p>
        <aside>
          <p><strong>補足：</strong>セマンティクスは「意味論」とも訳されます。</p>
        </aside>
      </section>

      <footer>
        <p>著者：<a href="/author/tanaka">田中太郎</a></p>
        <p>タグ：HTML, セマンティクス, 入門</p>
      </footer>
    </article>

    <aside aria-label="サイドバー">
      <section>
        <h2>プロフィール</h2>
        <p>Web開発者の田中です。</p>
      </section>
      <section>
        <h2>最近の記事</h2>
        <ul>
          <li><a href="/post/1">CSS Gridの使い方</a></li>
          <li><a href="/post/2">JavaScript入門</a></li>
        </ul>
      </section>
    </aside>
  </main>

  <footer>
    <address>
      お問い合わせ：<a href="mailto:info@example.com">info@example.com</a>
    </address>
    <p><small>&copy; 2024 My Blog. All rights reserved.</small></p>
  </footer>
</body>
</html>
```

---

## 6.15 よくある間違い

### 1. divの多用（div地獄）
```html
<!-- 悪い例 -->
<div class="header">
  <div class="nav">...</div>
</div>

<!-- 良い例 -->
<header>
  <nav>...</nav>
</header>
```

### 2. sectionをdivの代わりに使う
```html
<!-- 悪い例：スタイルのためだけにsectionを使う -->
<section class="wrapper">
  <section class="inner">...</section>
</section>

<!-- 良い例：スタイル目的ならdivを使う -->
<div class="wrapper">
  <div class="inner">...</div>
</div>
```

### 3. mainの中にheader/footerを入れない
```html
<!-- 注意：ページ全体のheader/footerはmainの外に置く -->
<!-- mainの中にarticleのheader/footerを入れるのはOK -->
```

### 4. nav の乱用
```html
<!-- 悪い例：すべてのリンクまとまりにnavを使う -->
<nav>
  <a href="/terms">利用規約</a>
  <a href="/privacy">プライバシー</a>
</nav>

<!-- 良い例：主要ナビゲーションにだけ使う -->
<footer>
  <a href="/terms">利用規約</a>
  <a href="/privacy">プライバシー</a>
</footer>
```

### 5. ARIAの過剰使用
```html
<!-- 悪い例：セマンティック要素にroleを二重指定 -->
<nav role="navigation">...</nav>
<main role="main">...</main>

<!-- 良い例：セマンティック要素だけで十分 -->
<nav>...</nav>
<main>...</main>
```

---

## 6.16 アクセシビリティのベストプラクティス

### ランドマークの活用
スクリーンリーダーのユーザーは「ランドマーク」を使ってページ内を移動します。

| セマンティック要素 | 暗黙のランドマーク |
|---|---|
| `<header>`（ページ直下） | banner |
| `<nav>` | navigation |
| `<main>` | main |
| `<aside>` | complementary |
| `<footer>`（ページ直下） | contentinfo |
| `<section>`（見出しあり） | region |
| `<form>`（名前あり） | form |

### スキップリンク
キーボードユーザーのために、メインコンテンツに直接ジャンプできるリンクを設置します。

```html
<body>
  <a href="#main-content" class="skip-link">メインコンテンツへスキップ</a>
  <header>
    <nav>
      <!-- 多数のナビゲーションリンク -->
    </nav>
  </header>
  <main id="main-content">
    <!-- メインコンテンツ -->
  </main>
</body>

<style>
  .skip-link {
    position: absolute;
    left: -9999px;
  }
  .skip-link:focus {
    position: static;
    display: block;
    padding: 0.5em;
    background: #000;
    color: #fff;
    text-align: center;
  }
</style>
```

---

## ポイントまとめ

| 要素 | 用途 | ランドマーク |
|---|---|---|
| `<header>` | 導入コンテンツ、ナビ | banner |
| `<nav>` | 主要ナビゲーション | navigation |
| `<main>` | ページの主要コンテンツ（1つのみ） | main |
| `<section>` | テーマ別のセクション | region |
| `<article>` | 独立した自己完結コンテンツ | article |
| `<aside>` | 補足的な内容 | complementary |
| `<footer>` | フッター情報 | contentinfo |
| `<div>` | 意味を持たない汎用コンテナ | なし |
| `role` | 要素の役割を明示（ARIA） | ― |
| `aria-label` | テキストのないUI要素のラベル | ― |
| `aria-hidden` | スクリーンリーダーから隠す | ― |

---

## 次の章へ
次の章では、`<head>` 要素内のメタ情報（meta tags, OGP, viewport, favicon 等）について詳しく学びます。
