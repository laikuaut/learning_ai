# 第6章 演習：セマンティックHTML

---

## 基本問題

### 問題1：セマンティック要素の選択
以下のコンテンツに最も適切なセマンティックHTML要素を答えてください。

1. サイトのロゴとメインナビゲーションを含むエリア
2. ブログの個々の記事
3. サイドバーに配置する関連リンクや広告
4. ページのメインコンテンツ（1ページに1つだけ）
5. コピーライトやサイトマップリンクを含む最下部エリア
6. ページ内のナビゲーションリンク一覧

<details>
<summary>解答</summary>

1. `<header>` — サイト全体の導入部分
2. `<article>` — 独立した自己完結型コンテンツ
3. `<aside>` — メインコンテンツに間接的に関連するコンテンツ
4. `<main>` — ページの主要コンテンツ（1ページに1つのみ使用）
5. `<footer>` — ページやセクションのフッター
6. `<nav>` — ナビゲーションリンクのグループ

</details>

---

### 問題2：div を置き換える
以下の非セマンティックなHTMLを、適切なセマンティック要素に置き換えてください。

```html
<div id="header">
  <div id="logo">My Blog</div>
  <div id="navigation">
    <a href="/">ホーム</a>
    <a href="/about">概要</a>
  </div>
</div>
<div id="content">
  <div class="post">
    <div class="post-title">記事タイトル</div>
    <div class="post-body">記事の本文です。</div>
  </div>
</div>
<div id="sidebar">
  <div class="widget">関連リンク</div>
</div>
<div id="footer">
  <p>Copyright 2025</p>
</div>
```

<details>
<summary>解答例</summary>

```html
<header>
  <h1>My Blog</h1>
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
    <p>記事の本文です。</p>
  </article>
</main>
<aside>
  <p>関連リンク</p>
</aside>
<footer>
  <p><small>Copyright 2025</small></p>
</footer>
```

<!--
  div + id/class の組み合わせを、意味を持つセマンティック要素に置き換えました。
  ナビゲーションはul/liで構造化し、テキストは適切な見出し要素（h1, h2）や段落（p）を使います。
-->

</details>

---

### 問題3：section と article の使い分け
以下のコンテンツには `<section>` と `<article>` のどちらが適切か答えてください。

1. ブログの個々の投稿
2. 製品紹介ページの「特徴」「仕様」「レビュー」の各セクション
3. ニュースサイトの各ニュース記事
4. 会社概要ページの「沿革」「アクセス」の各セクション
5. SNSのタイムラインに表示される個々の投稿

<details>
<summary>解答</summary>

1. `<article>` — 個々のブログ投稿は独立した完結コンテンツ
2. `<section>` — ページ内の論理的なまとまり（単独では成り立たない）
3. `<article>` — 各ニュース記事は独立して意味をなす
4. `<section>` — ページ内のテーマ別セクション
5. `<article>` — 各投稿は独立したコンテンツ

**判断基準**: そのコンテンツだけを切り出して別のページに貼り付けても意味が通るなら `<article>`、ページの一部としてのまとまりなら `<section>` です。

</details>

---

### 問題4：time要素
以下の日時情報を `<time>` 要素でマークアップしてください。datetime 属性に機械可読な形式を指定すること。

1. 2025年4月15日
2. 午後3時30分
3. 2025年4月15日 15時30分

<details>
<summary>解答例</summary>

```html
<!-- 日付 -->
<time datetime="2025-04-15">2025年4月15日</time>

<!-- 時刻 -->
<time datetime="15:30">午後3時30分</time>

<!-- 日時 -->
<time datetime="2025-04-15T15:30">2025年4月15日 15時30分</time>
```

<!-- datetime 属性に ISO 8601 形式で記述することで、検索エンジンやブラウザが日時を正しく認識できます。 -->

</details>

---

### 問題5：address 要素
以下の連絡先情報を `<address>` 要素で適切にマークアップしてください。

- 著者名：山田太郎
- メール：yamada@example.com
- 住所：東京都渋谷区1-2-3

<details>
<summary>解答例</summary>

```html
<address>
  <p>山田太郎</p>
  <p>メール：<a href="mailto:yamada@example.com">yamada@example.com</a></p>
  <p>東京都渋谷区1-2-3</p>
</address>
```

<!-- address 要素は「ページやarticleの著者・管理者への連絡先」を示します。一般的な住所表示には使いません。 -->

</details>

---

## 応用問題

### 問題6：aria-label の適用
以下のHTMLでは、2つの `<nav>` があります。スクリーンリーダーが2つのナビゲーションを区別できるように `aria-label` を適切に設定してください。

```html
<header>
  <nav>
    <ul>
      <li><a href="/">ホーム</a></li>
      <li><a href="/products">製品</a></li>
      <li><a href="/contact">お問い合わせ</a></li>
    </ul>
  </nav>
</header>

<footer>
  <nav>
    <ul>
      <li><a href="/privacy">プライバシーポリシー</a></li>
      <li><a href="/terms">利用規約</a></li>
      <li><a href="/sitemap">サイトマップ</a></li>
    </ul>
  </nav>
</footer>
```

<details>
<summary>解答例</summary>

```html
<header>
  <nav aria-label="メインナビゲーション">
    <ul>
      <li><a href="/">ホーム</a></li>
      <li><a href="/products">製品</a></li>
      <li><a href="/contact">お問い合わせ</a></li>
    </ul>
  </nav>
</header>

<footer>
  <nav aria-label="フッターナビゲーション">
    <ul>
      <li><a href="/privacy">プライバシーポリシー</a></li>
      <li><a href="/terms">利用規約</a></li>
      <li><a href="/sitemap">サイトマップ</a></li>
    </ul>
  </nav>
</footer>
```

<!--
  aria-label を付けることで、スクリーンリーダーは
  「メインナビゲーション」「フッターナビゲーション」と読み上げ、
  ユーザーが2つのnavを区別できるようになります。
-->

</details>

---

### 問題7：正しい見出しレベル
以下のHTMLの見出しレベルには問題があります。正しい階層構造に修正してください。

```html
<body>
  <h1>会社概要</h1>
  <h3>代表挨拶</h3>
  <p>代表の挨拶文...</p>
  <h3>会社情報</h3>
  <h5>所在地</h5>
  <p>東京都...</p>
  <h5>設立</h5>
  <p>2020年...</p>
  <h1>事業内容</h1>
  <p>事業の説明...</p>
</body>
```

<details>
<summary>ヒント</summary>

見出しレベルは h1 → h2 → h3 のように段階的に下げます。レベルを飛ばす（h1 の次に h3）のは不適切です。また、h1 は通常ページに1つだけ使います。

</details>

<details>
<summary>解答例</summary>

```html
<body>
  <h1>会社概要</h1>

  <h2>代表挨拶</h2>
  <p>代表の挨拶文...</p>

  <h2>会社情報</h2>
  <h3>所在地</h3>
  <p>東京都...</p>
  <h3>設立</h3>
  <p>2020年...</p>

  <h2>事業内容</h2>
  <p>事業の説明...</p>
</body>
```

<!--
  修正ポイント：
  1. h3 → h2 に修正（h1の直下はh2であるべき）
  2. h5 → h3 に修正（h2の直下はh3であるべき）
  3. 2つ目の h1 → h2 に修正（h1はページに1つが原則）
-->

</details>

---

## チャレンジ問題

### 問題8：ブログ記事ページの作成
以下の要件を満たすセマンティックHTMLで構成された完全なHTMLページを作成してください。

- ページタイトル「HTMLの基本を学ぼう | 田中のブログ」
- **header**: サイト名（h1）+ メインナビゲーション（ホーム、記事一覧、お問い合わせ）
- **main** 内に：
  - **article**: ブログ記事
    - 記事の **header**: タイトル（h2）、投稿日（time要素）、著者名
    - 2つの **section**: それぞれにh3見出しと段落
    - 記事の **footer**: カテゴリタグ、シェアリンク
  - **aside**: サイドバー（著者プロフィール、人気記事リスト）
- **footer**: コピーライト、フッターナビゲーション（aria-label付き）、address 要素
- 複数の nav がある場合は aria-label で区別すること

<details>
<summary>解答例</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HTMLの基本を学ぼう | 田中のブログ</title>
</head>
<body>
  <!-- サイトヘッダー -->
  <header>
    <h1>田中のブログ</h1>
    <nav aria-label="メインナビゲーション">
      <ul>
        <li><a href="/">ホーム</a></li>
        <li><a href="/articles">記事一覧</a></li>
        <li><a href="/contact">お問い合わせ</a></li>
      </ul>
    </nav>
  </header>

  <!-- メインコンテンツ -->
  <main>
    <!-- ブログ記事 -->
    <article>
      <header>
        <h2>HTMLの基本を学ぼう</h2>
        <p>
          投稿日：<time datetime="2025-04-15">2025年4月15日</time>
          ／ 著者：田中太郎
        </p>
      </header>

      <section>
        <h3>HTMLとは何か</h3>
        <p>HTMLはWebページの構造を定義するマークアップ言語です。タグを使ってテキストに意味を持たせ、ブラウザが正しく表示できるようにします。</p>
      </section>

      <section>
        <h3>セマンティックHTMLの重要性</h3>
        <p>セマンティックHTMLを使うことで、アクセシビリティが向上し、検索エンジンがコンテンツを正しく理解できるようになります。divの代わりに意味のある要素を使いましょう。</p>
      </section>

      <footer>
        <p>カテゴリ：<a href="/category/html">HTML</a>、<a href="/category/web">Web開発</a></p>
        <p>シェア：
          <a href="#">Twitter</a> |
          <a href="#">Facebook</a>
        </p>
      </footer>
    </article>

    <!-- サイドバー -->
    <aside>
      <section>
        <h2>著者プロフィール</h2>
        <p>田中太郎 — Web開発を学ぶエンジニア。HTML/CSSを中心に情報発信中。</p>
      </section>
      <section>
        <h2>人気記事</h2>
        <ol>
          <li><a href="/articles/css-flexbox">CSS Flexbox入門</a></li>
          <li><a href="/articles/js-basic">JavaScript基礎</a></li>
          <li><a href="/articles/responsive">レスポンシブデザイン</a></li>
        </ol>
      </section>
    </aside>
  </main>

  <!-- フッター -->
  <footer>
    <nav aria-label="フッターナビゲーション">
      <ul>
        <li><a href="/privacy">プライバシーポリシー</a></li>
        <li><a href="/terms">利用規約</a></li>
      </ul>
    </nav>
    <address>
      <p>お問い合わせ：<a href="mailto:tanaka@example.com">tanaka@example.com</a></p>
    </address>
    <p><small>Copyright 2025 田中のブログ. All rights reserved.</small></p>
  </footer>
</body>
</html>
```

</details>
