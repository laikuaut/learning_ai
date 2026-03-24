# 第7章 演習：メタ情報とhead要素

---

## 基本問題

### 問題1：meta charset と viewport
以下の2つの meta タグの役割をそれぞれ説明してください。また、これらが `<head>` 内のどの位置に書くべきかも答えてください。

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

<details>
<summary>解答</summary>

**`<meta charset="UTF-8">`**
- ページの文字エンコーディングを UTF-8 に指定します
- ブラウザが文字化けせず日本語を表示するために必要です
- **`<head>` の最初**に記述するべきです（ブラウザは最初の1024バイト以内で文字コードを判定するため）

**`<meta name="viewport" content="width=device-width, initial-scale=1.0">`**
- モバイルデバイスでページの表示幅をデバイスの幅に合わせます
- レスポンシブデザインに必須の設定です
- charset の直後に記述するのが一般的です

</details>

---

### 問題2：title要素の改善
以下の `<title>` を SEO とユーザビリティの観点から改善してください。

1. `<title>ページ</title>`
2. `<title>株式会社ABCのWebサイトへようこそ。当社は創業50年の実績を持つ老舗企業であり、お客様に最高のサービスを提供することをモットーに日々邁進しております。</title>`
3. `<title>ABC会社 | ABC会社 | ABC会社について</title>`

<details>
<summary>解答例</summary>

1. **問題**: 内容が不明確で、どのページかわからない
   - 改善: `<title>お問い合わせ | ABC株式会社</title>`

2. **問題**: 長すぎる（検索結果で途中が省略される。30〜60文字が目安）
   - 改善: `<title>ABC株式会社 | 創業50年の信頼と実績</title>`

3. **問題**: 同じキーワードの重複。意味のない繰り返し
   - 改善: `<title>会社概要 | ABC株式会社</title>`

</details>

---

### 問題3：meta description
以下のページに適切な meta description を書いてください（70〜160文字程度）。

- ページ内容：Python入門の学習教材。変数、関数、リストなどの基本構文を初心者向けに解説。実行可能なコード例付き。

<details>
<summary>解答例</summary>

```html
<meta name="description" content="Python入門者向けの学習教材です。変数・関数・リストなど基本構文を、コピペで実行できるコード例とともにわかりやすく解説。プログラミング未経験でも安心して学べます。">
```

<!-- description は検索結果のスニペットに表示される可能性があります。ページの内容を具体的に要約し、ユーザーがクリックしたくなる文言にしましょう。 -->

</details>

---

### 問題4：meta robots
以下の要件に合う meta robots タグを書いてください。

1. 検索結果に表示させたくないページ（社内マニュアルなど）
2. 検索結果に表示するが、ページ内のリンクはたどらせたくない
3. 検索結果に表示し、リンクもたどらせる（デフォルト動作）

<details>
<summary>解答例</summary>

```html
<!-- 1. インデックス禁止 -->
<meta name="robots" content="noindex, nofollow">

<!-- 2. インデックスするが、リンクはたどらない -->
<meta name="robots" content="index, nofollow">

<!-- 3. デフォルト動作（省略しても同じだが、明示する場合） -->
<meta name="robots" content="index, follow">
```

<!--
  noindex: 検索結果に表示しない
  nofollow: ページ内のリンクをクロールしない
  デフォルトは index, follow なので、通常はこのタグを書く必要はありません。
-->

</details>

---

### 問題5：link要素
以下の目的に合う `<link>` 要素を書いてください。

1. 外部CSSファイル `styles/main.css` を読み込む
2. ファビコン `favicon.ico` を設定する
3. Google Fonts から「Noto Sans JP」を読み込むためのプリコネクト

<details>
<summary>解答例</summary>

```html
<!-- 1. 外部CSS -->
<link rel="stylesheet" href="styles/main.css">

<!-- 2. ファビコン -->
<link rel="icon" href="favicon.ico">

<!-- 3. Google Fonts のプリコネクト -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

<!--
  rel="stylesheet" でCSSを読み込みます。
  rel="icon" でブラウザのタブに表示されるアイコンを指定します。
  rel="preconnect" で外部ドメインへの接続を事前に確立し、フォントの読み込みを高速化します。
-->

</details>

---

## 応用問題

### 問題6：OGP（Open Graph Protocol）の設定
以下の条件を満たす OGP メタタグを書いてください。

- ページタイトル：「HTML入門ガイド」
- ページの説明：「初心者向けHTMLの基礎を解説する学習ガイドです」
- ページのURL：`https://example.com/html-guide`
- OGP画像：`https://example.com/images/html-guide-ogp.jpg`
- サイト名：「Web開発入門」
- Twitter カードの形式：summary_large_image

<details>
<summary>ヒント</summary>

OGP タグは `<meta property="og:xxx">` の形式で記述します。Twitter カードは `<meta name="twitter:xxx">` で指定します。

</details>

<details>
<summary>解答例</summary>

```html
<!-- OGP 基本設定 -->
<meta property="og:type" content="article">
<meta property="og:title" content="HTML入門ガイド">
<meta property="og:description" content="初心者向けHTMLの基礎を解説する学習ガイドです">
<meta property="og:url" content="https://example.com/html-guide">
<meta property="og:image" content="https://example.com/images/html-guide-ogp.jpg">
<meta property="og:site_name" content="Web開発入門">

<!-- Twitter カード -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="HTML入門ガイド">
<meta name="twitter:description" content="初心者向けHTMLの基礎を解説する学習ガイドです">
<meta name="twitter:image" content="https://example.com/images/html-guide-ogp.jpg">
```

<!-- OGPを設定すると、SNSでURLをシェアしたときにタイトル・説明文・画像がリッチに表示されます。 -->

</details>

---

### 問題7：head 内の記述順序
以下の要素を `<head>` 内で推奨される順序に並べ替えてください。

A. `<link rel="stylesheet" href="style.css">`
B. `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
C. `<title>ページタイトル</title>`
D. `<meta charset="UTF-8">`
E. `<meta name="description" content="...">`
F. `<script src="app.js" defer></script>`
G. `<link rel="icon" href="favicon.ico">`
H. `<meta property="og:title" content="...">`

<details>
<summary>解答</summary>

推奨される順序：

1. **D** `<meta charset="UTF-8">` — 文字コードは最優先（先頭1024バイト以内）
2. **B** `<meta name="viewport">` — モバイル対応の基本設定
3. **C** `<title>` — ページタイトル
4. **E** `<meta name="description">` — ページの説明文
5. **H** `<meta property="og:title">` — OGP設定
6. **G** `<link rel="icon">` — ファビコン
7. **A** `<link rel="stylesheet">` — CSS読み込み
8. **F** `<script defer>` — JavaScript（defer で読み込みを遅延）

**ポイント**: charset は必ず先頭に。meta → title → link → script の順が一般的です。

</details>

---

## チャレンジ問題

### 問題8：実務レベルの head テンプレート作成
以下の要件を満たす完全な `<head>` セクションを持つHTMLページを作成してください。

- 文字コード UTF-8
- レスポンシブ対応のビューポート設定
- ページタイトル「プログラミング学習ガイド | TechLearn」
- description（100文字前後で具体的に）
- OGP 設定一式（type, title, description, url, image, site_name）
- Twitter カード（summary_large_image）
- ファビコン（PNG形式: `favicon.png`）
- 外部CSS: `css/style.css`
- Google Fonts のプリコネクト設定
- 外部JS: `js/main.js` を defer で読み込み
- robots: index, follow
- body には h1 でページタイトルと簡単な段落を1つ

<details>
<summary>解答例</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <!-- 文字コード（最優先） -->
  <meta charset="UTF-8">
  <!-- レスポンシブ対応 -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- ページタイトル -->
  <title>プログラミング学習ガイド | TechLearn</title>

  <!-- 検索エンジン向け -->
  <meta name="description" content="Python・JavaScript・HTMLなど主要な言語を初心者向けにわかりやすく解説。実行可能なコード例と演習問題で実践的に学べるプログラミング学習サイトです。">
  <meta name="robots" content="index, follow">

  <!-- OGP（SNSシェア用） -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="プログラミング学習ガイド | TechLearn">
  <meta property="og:description" content="初心者向けプログラミング学習サイト。実践的なコード例で効率よく学べます。">
  <meta property="og:url" content="https://techlearn.example.com/">
  <meta property="og:image" content="https://techlearn.example.com/images/ogp.jpg">
  <meta property="og:site_name" content="TechLearn">

  <!-- Twitter カード -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="プログラミング学習ガイド | TechLearn">
  <meta name="twitter:description" content="初心者向けプログラミング学習サイト。実践的なコード例で効率よく学べます。">
  <meta name="twitter:image" content="https://techlearn.example.com/images/ogp.jpg">

  <!-- ファビコン -->
  <link rel="icon" type="image/png" href="favicon.png">

  <!-- Google Fonts プリコネクト -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- CSS -->
  <link rel="stylesheet" href="css/style.css">

  <!-- JavaScript（defer で非同期読み込み） -->
  <script src="js/main.js" defer></script>
</head>
<body>
  <h1>プログラミング学習ガイド</h1>
  <p>このサイトでは、初心者向けにプログラミングの基礎から応用までをわかりやすく解説しています。</p>
</body>
</html>
```

</details>
