# 第7章：メタ情報とhead要素

## この章のゴール
- `<head>` 要素内に記述するメタ情報の全体像を理解する
- 各種 meta タグ（charset, viewport, description, robots 等）の役割と書き方を習得する
- OGP（Open Graph Protocol）を設定し、SNS でシェアされたときの表示を制御できる
- link 要素によるファビコン、スタイルシート、プリロードの指定方法を習得する
- 実務で通用する `<head>` テンプレートを作成できるようになる

---

## 7.1 head要素の役割

`<head>` 要素にはページの**メタ情報**（ページ自体についての情報）を記述します。ブラウザの画面には直接表示されませんが、ブラウザの挙動、検索エンジンの評価、SNSでの表示などに大きく影響します。

```
+---------------------------------------------+
|  <head>                                     |
|                                             |
|  ┌─ meta charset ── 文字コード              |
|  ├─ meta viewport ── モバイル対応            |
|  ├─ title ── ページタイトル                  |
|  ├─ meta description ── ページの説明文       |
|  ├─ meta robots ── クロール制御              |
|  ├─ OGP meta ── SNSシェア時の表示            |
|  ├─ link rel="icon" ── ファビコン            |
|  ├─ link rel="stylesheet" ── CSS読み込み     |
|  ├─ link rel="preconnect" ── 先行接続        |
|  ├─ script ── JavaScript読み込み             |
|  └─ style ── 内部CSS                        |
|                                             |
+---------------------------------------------+
```

### head内に配置できる要素
| 要素 | 用途 |
|---|---|
| `<meta>` | メタ情報（文字コード、説明文、ビューポート等） |
| `<title>` | ページタイトル |
| `<link>` | 外部リソースの参照（CSS、ファビコン、フォント等） |
| `<style>` | 内部CSS |
| `<script>` | JavaScript |
| `<base>` | 相対パスの基準URL |
| `<noscript>` | JavaScript無効時の代替コンテンツ |

---

## 7.2 meta charset：文字エンコーディング

```html
<meta charset="UTF-8">
```

- **必ず `<head>` の最初**に記述する
- ブラウザが最初の1024バイト以内で文字コードを判定するため、先頭に置くことが重要
- UTF-8 は世界中の文字を扱える標準的なエンコーディング
- この指定がないと日本語が文字化けする可能性がある

> **ポイント**: 現代のWebでは UTF-8 が事実上の標準です。特別な理由がない限り UTF-8 を使いましょう。

---

## 7.3 meta viewport：レスポンシブ対応

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### viewport の各設定

| プロパティ | 説明 | 推奨値 |
|---|---|---|
| `width` | ビューポートの幅 | `device-width` |
| `initial-scale` | 初期ズーム倍率 | `1.0` |
| `minimum-scale` | 最小ズーム倍率 | （省略推奨） |
| `maximum-scale` | 最大ズーム倍率 | （省略推奨） |
| `user-scalable` | ユーザーのズーム操作 | （省略推奨） |

### ビューポートの仕組み

```
viewportなし（デフォルト）:
+------------------+
| デスクトップ幅     |  ← スマホでは全体が縮小される
| (通常980px)       |
| で表示            |
+------------------+

viewport指定あり:
+--------+
| デバイス|  ← デバイスの幅に合わせて表示
| 幅で   |
| 表示   |
+--------+
```

> **重要**: `maximum-scale=1.0` や `user-scalable=no` はユーザーのズーム操作を制限するため、**アクセシビリティ上問題**があります。視覚に困難があるユーザーがページを拡大できなくなるため、これらの指定は避けてください。

---

## 7.4 title要素（復習と応用）

```html
<title>HTMLの基礎を学ぼう | Web開発入門ガイド</title>
```

### titleが使われる場所
1. ブラウザのタブ
2. ブックマーク名
3. 検索エンジンの結果ページ
4. SNSシェア時のタイトル（OGPが設定されていない場合）
5. スクリーンリーダーが最初に読み上げるテキスト

### title の書き方テンプレート
| パターン | 例 |
|---|---|
| `ページ名 | サイト名` | `お問い合わせ | ABC株式会社` |
| `ページ名 - サイト名` | `会社概要 - ABC株式会社` |
| `サイト名: ページ名` | `ABC株式会社: 採用情報` |

### SEO に効果的な title
- 30〜60文字程度に収める
- 重要なキーワードを前半に配置する
- 各ページで一意のタイトルを付ける
- サイト名はタイトルの後半に付ける

---

## 7.5 meta description：ページの説明文

```html
<meta name="description" content="HTMLの基礎から応用まで、初心者向けにわかりやすく解説するWebプログラミング学習サイトです。実践的なコード例と演習問題で効率よく学べます。">
```

### description の役割
- **検索結果のスニペット**（概要文）として表示される可能性がある
- Googleは検索クエリに合った部分をページ本文から自動抽出することもある
- 必ずしも description がそのまま使われるとは限らない

### description の書き方
- **70〜160文字**程度が目安
- ページの内容を**具体的に要約**する
- ユーザーが検索結果からクリックしたくなるような文言にする
- 各ページで**固有の説明文**を書く

```html
<!-- 悪い例：汎用的すぎる -->
<meta name="description" content="このページについての説明です。">

<!-- 良い例：具体的で魅力的 -->
<meta name="description" content="HTMLフォームの作り方を15の実践例で解説。input要素の全typeからバリデーションまで、コピペで使えるコード付き。">
```

---

## 7.6 meta robots：クロール制御

```html
<!-- デフォルト（インデックス許可、リンクをたどる） -->
<meta name="robots" content="index, follow">

<!-- インデックス禁止（検索結果に表示しない） -->
<meta name="robots" content="noindex">

<!-- リンクをたどらない -->
<meta name="robots" content="nofollow">

<!-- インデックスもリンク追跡もしない -->
<meta name="robots" content="noindex, nofollow">
```

| 値 | 説明 |
|---|---|
| `index` | 検索エンジンにインデックスさせる（デフォルト） |
| `noindex` | インデックスさせない |
| `follow` | ページ内のリンクをたどる（デフォルト） |
| `nofollow` | リンクをたどらない |
| `noarchive` | キャッシュを保存させない |
| `nosnippet` | スニペット（概要文）を表示させない |

### 使用例
```html
<!-- 開発中のページ（検索結果に出したくない） -->
<meta name="robots" content="noindex, nofollow">

<!-- ログインが必要なページ -->
<meta name="robots" content="noindex">

<!-- 公開ページ（明示的にインデックス許可） -->
<meta name="robots" content="index, follow">
```

---

## 7.7 OGP（Open Graph Protocol）

OGP は、ページが SNS でシェアされたときの**タイトル、説明文、画像**を制御するためのメタ情報です。

### 基本的な OGP タグ

```html
<meta property="og:title" content="HTMLの基礎を学ぼう">
<meta property="og:description" content="初心者向けHTML入門。セマンティクスからフォームまで網羅。">
<meta property="og:image" content="https://example.com/images/ogp.png">
<meta property="og:url" content="https://example.com/html-tutorial">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Web開発入門ガイド">
<meta property="og:locale" content="ja_JP">
```

### OGP タグ一覧
| プロパティ | 必須 | 説明 |
|---|---|---|
| `og:title` | はい | コンテンツのタイトル |
| `og:type` | はい | コンテンツの種類（website, article 等） |
| `og:url` | はい | ページの正規URL |
| `og:image` | はい | シェア時に表示される画像（**絶対URL**） |
| `og:description` | 推奨 | コンテンツの説明文 |
| `og:site_name` | 推奨 | サイト名 |
| `og:locale` | 任意 | ロケール（`ja_JP`, `en_US` 等） |

### og:type の主な値
| 値 | 用途 |
|---|---|
| `website` | Webサイトのトップページ |
| `article` | 記事ページ |
| `profile` | プロフィールページ |
| `product` | 商品ページ |

### OGP 画像の推奨サイズ
- **1200 x 630 px**（横長）が最も広く対応
- 最低でも 600 x 315 px 以上
- ファイルサイズは 1MB 以下が推奨
- JPEG または PNG 形式

### Twitter Card

Twitter（X）では OGP に加えて専用のメタタグがあります。

```html
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@your_account">
<meta name="twitter:title" content="HTMLの基礎を学ぼう">
<meta name="twitter:description" content="初心者向けHTML入門">
<meta name="twitter:image" content="https://example.com/images/twitter-card.png">
```

| カードタイプ | 説明 |
|---|---|
| `summary` | 小さいサムネイル付き |
| `summary_large_image` | 大きな画像付き（推奨） |
| `app` | アプリダウンロード用 |
| `player` | 動画・音声プレーヤー |

---

## 7.8 link要素：外部リソースの参照

### ファビコン（favicon）

ファビコンはブラウザタブやブックマークに表示される小さなアイコンです。

```html
<!-- 基本的なファビコン -->
<link rel="icon" href="/favicon.ico" sizes="32x32">

<!-- SVGファビコン（モダンブラウザ向け） -->
<link rel="icon" href="/favicon.svg" type="image/svg+xml">

<!-- Apple Touch Icon（iOS向け） -->
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">

<!-- 複数サイズの指定 -->
<link rel="icon" href="/favicon-16x16.png" sizes="16x16" type="image/png">
<link rel="icon" href="/favicon-32x32.png" sizes="32x32" type="image/png">
```

### ファビコンの形式と推奨サイズ
| 形式 | サイズ | 用途 |
|---|---|---|
| `.ico` | 32x32 | 従来のブラウザ向け |
| `.svg` | 可変 | モダンブラウザ（ダークモード対応可） |
| `.png` | 16x16, 32x32, 180x180 | 各種デバイス |

### CSSの読み込み

```html
<!-- 外部CSSファイル -->
<link rel="stylesheet" href="css/style.css">

<!-- 印刷用CSS -->
<link rel="stylesheet" href="css/print.css" media="print">

<!-- ダークモード用CSS -->
<link rel="stylesheet" href="css/dark.css" media="(prefers-color-scheme: dark)">
```

### Webフォントの読み込み

```html
<!-- Google Fonts の例 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap">
```

### canonical URL（正規URL）

```html
<link rel="canonical" href="https://example.com/html-tutorial">
```

- 同じコンテンツに複数のURLからアクセスできる場合、正規URLを指定する
- SEO で重複コンテンツのペナルティを防ぐ

### rel 属性の主な値
| 値 | 説明 |
|---|---|
| `stylesheet` | CSSファイルの読み込み |
| `icon` | ファビコン |
| `apple-touch-icon` | iOS用アイコン |
| `canonical` | 正規URL |
| `preconnect` | 外部ドメインへの先行接続 |
| `preload` | リソースの先読み |
| `prefetch` | 次のページのリソース先読み |
| `dns-prefetch` | DNS解決の先行実行 |
| `alternate` | 代替バージョン（言語、フィード等） |
| `manifest` | PWAマニフェスト |

---

## 7.9 パフォーマンス最適化のための link

### preconnect：先行接続

外部ドメインのリソースを使う場合、事前にTCP接続を確立しておくことでロード時間を短縮できます。

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://cdn.example.com" crossorigin>
```

### preload：重要なリソースの先読み

ページで確実に使うリソースを優先的に読み込みます。

```html
<!-- フォントの先読み -->
<link rel="preload" href="/fonts/myfont.woff2" as="font" type="font/woff2" crossorigin>

<!-- 画像の先読み -->
<link rel="preload" href="/images/hero.jpg" as="image">

<!-- CSSの先読み -->
<link rel="preload" href="/css/critical.css" as="style">
```

| as 属性 | リソースの種類 |
|---|---|
| `style` | CSS |
| `script` | JavaScript |
| `font` | フォント |
| `image` | 画像 |
| `fetch` | fetch/XHR リクエスト |

### prefetch：次のページの先読み

ユーザーが次に訪れそうなページのリソースを事前に取得します。

```html
<link rel="prefetch" href="/next-page.html">
<link rel="prefetch" href="/css/next-page.css">
```

### dns-prefetch：DNS の先行解決

```html
<link rel="dns-prefetch" href="https://analytics.example.com">
```

---

## 7.10 script要素とnoscript要素

### script の読み込み方法

```html
<!-- 通常の読み込み（パース中止→読み込み→実行→パース再開） -->
<script src="app.js"></script>

<!-- defer：パースと並行で読み込み、パース完了後に実行 -->
<script src="app.js" defer></script>

<!-- async：パースと並行で読み込み、読み込み完了直後に実行 -->
<script src="analytics.js" async></script>

<!-- module：ES Modules として読み込む（暗黙的にdefer） -->
<script type="module" src="app.mjs"></script>
```

### defer と async の違い

```
通常:
HTML解析: ====|停止|======|停止|======
JSダウンロード:     |====|
JS実行:                  |==|

defer:
HTML解析: ==========================|
JSダウンロード:  |====|              |
JS実行:                             |==|
                          DOMContentLoaded後

async:
HTML解析: ==========|停止|===========
JSダウンロード:  |====|
JS実行:              |==|
                   ダウンロード完了直後
```

| 属性 | ダウンロード | 実行タイミング | 実行順序 | 用途 |
|---|---|---|---|---|
| なし | パース中止 | ダウンロード直後 | 記述順 | 即座に必要なスクリプト |
| `defer` | 並行 | パース完了後 | 記述順を保証 | メインアプリケーション |
| `async` | 並行 | ダウンロード完了直後 | 保証なし | アナリティクス、広告 |

> **推奨**: ほとんどのスクリプトは `defer` を付けて `<head>` に配置するのがベストプラクティスです。

### noscript 要素

JavaScriptが無効な環境でのフォールバックを提供します。

```html
<noscript>
  <p>このサイトの一部機能にはJavaScriptが必要です。
     ブラウザの設定でJavaScriptを有効にしてください。</p>
</noscript>
```

---

## 7.11 その他のメタタグ

### テーマカラー

```html
<!-- ブラウザのアドレスバーの色（モバイル） -->
<meta name="theme-color" content="#4285f4">

<!-- ダークモード時の色 -->
<meta name="theme-color" content="#1a1a2e" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
```

### 作者情報

```html
<meta name="author" content="田中太郎">
```

### 色指定のスキーム

```html
<!-- ダークモード対応を明示 -->
<meta name="color-scheme" content="light dark">
```

### 古い IE 対応（レガシー）

```html
<!-- IE に最新のレンダリングエンジンを使わせる（現在はほぼ不要） -->
<meta http-equiv="X-UA-Compatible" content="IE=edge">
```

### Content Security Policy

```html
<!-- セキュリティポリシーの設定 -->
<meta http-equiv="Content-Security-Policy" content="default-src 'self'">
```

---

## 7.12 実践：本番レベルの head テンプレート

以下は実務で使える完全な `<head>` の例です。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <!-- 文字コード（必ず最初に） -->
  <meta charset="UTF-8">

  <!-- レスポンシブ対応 -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- ページタイトル -->
  <title>HTMLの基礎を学ぼう | Web開発入門ガイド</title>

  <!-- SEO メタタグ -->
  <meta name="description" content="HTMLの基礎から応用まで、初心者向けにわかりやすく解説。実践的なコード例と演習問題で効率よく学べます。">
  <meta name="author" content="田中太郎">

  <!-- OGP -->
  <meta property="og:title" content="HTMLの基礎を学ぼう">
  <meta property="og:description" content="初心者向けHTML入門。セマンティクスからフォームまで網羅。">
  <meta property="og:image" content="https://example.com/images/ogp.png">
  <meta property="og:url" content="https://example.com/html-tutorial">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Web開発入門ガイド">
  <meta property="og:locale" content="ja_JP">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@your_account">

  <!-- テーマカラー -->
  <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#1a1a2e" media="(prefers-color-scheme: dark)">
  <meta name="color-scheme" content="light dark">

  <!-- 正規URL -->
  <link rel="canonical" href="https://example.com/html-tutorial">

  <!-- ファビコン -->
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">

  <!-- 先行接続 -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- Webフォント -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap">

  <!-- CSS -->
  <link rel="stylesheet" href="/css/style.css">

  <!-- JavaScript（defer推奨） -->
  <script src="/js/app.js" defer></script>
</head>
<body>
  <!-- ページの内容 -->
</body>
</html>
```

---

## 7.13 よくある間違い

### 1. meta charset を head の先頭に書かない
```html
<!-- 悪い例：titleの後にcharset -->
<head>
  <title>ページタイトル</title>
  <meta charset="UTF-8">
</head>

<!-- 良い例：charsetを最初に -->
<head>
  <meta charset="UTF-8">
  <title>ページタイトル</title>
</head>
```

### 2. OGP の画像に相対パスを使う
```html
<!-- 悪い例：相対パスでは SNS が取得できない -->
<meta property="og:image" content="images/ogp.png">

<!-- 良い例：絶対URLを使う -->
<meta property="og:image" content="https://example.com/images/ogp.png">
```

### 3. viewport でズームを制限する
```html
<!-- 悪い例：ユーザーのズーム操作を制限 -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

<!-- 良い例：ズーム制限なし -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### 4. description が長すぎる・短すぎる
```html
<!-- 悪い例：短すぎて情報がない -->
<meta name="description" content="HTML入門">

<!-- 悪い例：長すぎて途中で切られる -->
<meta name="description" content="HTMLの基礎から応用まで初心者向けに解説するサイトです。セマンティックHTMLやフォーム、メタ情報、HTML5 APIなどを網羅的にカバーしています。実践的なコード例と演習問題が豊富に用意されており、効率的に学習を進めることができます。プログラミング初心者の方でも安心して取り組めるよう、丁寧な解説を心がけています。">

<!-- 良い例：70〜160文字程度 -->
<meta name="description" content="HTMLの基礎から応用まで、初心者向けにわかりやすく解説。実践的なコード例と演習問題で効率よく学べます。">
```

### 5. title がすべてのページで同じ
```html
<!-- 悪い例：全ページ共通のタイトル -->
<title>My Website</title>

<!-- 良い例：ページ固有のタイトル -->
<title>お問い合わせ | My Website</title>
```

---

## 7.14 アクセシビリティのベストプラクティス

1. **`lang` 属性**を `<html>` に指定する
2. **viewport** でズーム制限をしない
3. **title** をページ固有かつ具体的にする（スクリーンリーダーが最初に読む）
4. **テーマカラー**とダークモードに対応する
5. **`<noscript>`** で JavaScript 無効時のフォールバックを用意する
6. **script に `defer`** を付けて、パースをブロックしない

---

## ポイントまとめ

| 要素・属性 | 説明 |
|---|---|
| `<meta charset="UTF-8">` | 文字コード指定。head の最初に記述 |
| `<meta name="viewport">` | モバイルレスポンシブ対応 |
| `<title>` | ページタイトル。タブ、検索結果、SNSに使われる |
| `<meta name="description">` | ページの説明文。検索結果のスニペット |
| `<meta name="robots">` | 検索エンジンのクロール制御 |
| OGP (`og:*`) | SNSシェア時の表示制御 |
| Twitter Card | Twitter専用のメタ情報 |
| `<link rel="icon">` | ファビコン |
| `<link rel="stylesheet">` | CSS の読み込み |
| `<link rel="canonical">` | 正規URL |
| `<link rel="preconnect">` | 先行接続でパフォーマンス向上 |
| `<script defer>` | JSを非同期でパース完了後に実行 |

---

## 次の章へ
次の章では、HTML5で追加された便利な要素やAPI（data属性、details/summary、dialog、progress/meter等）を学びます。
