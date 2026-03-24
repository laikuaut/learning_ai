# 第1章 演習：HTMLの基本構造

---

## 基本問題

### 問題1：最小限のHTMLテンプレート
以下の条件を満たすHTMLファイルを作成してください。
- 文字コードは UTF-8
- 言語は日本語
- タイトルは「はじめてのHTML」
- bodyに「こんにちは、世界！」という段落を1つ

<details>
<summary>ヒント</summary>

`<!DOCTYPE html>` から始めて、`<html lang="ja">` でルート要素を作ります。`<head>` に `<meta charset="UTF-8">` と `<title>` を入れ、`<body>` にコンテンツを書きましょう。

</details>

<details>
<summary>解答例</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>はじめてのHTML</title>
</head>
<body>
  <p>こんにちは、世界！</p>
</body>
</html>
```

</details>

---

### 問題2：DOCTYPE宣言の役割
DOCTYPE宣言がない場合、ブラウザはどのようなモードでページを表示しますか？正しいものを選んでください。

A. 標準モード（Standards Mode）
B. 互換モード（Quirks Mode）
C. 厳格モード（Strict Mode）
D. エラーモード（Error Mode）

<details>
<summary>解答</summary>

**B. 互換モード（Quirks Mode）**

DOCTYPE宣言がないと、ブラウザは古いブラウザの挙動を模倣する「互換モード」でページを表示します。互換モードではCSSの解釈が異なるため、意図しない表示になることがあります。必ずHTMLファイルの1行目に `<!DOCTYPE html>` を記述しましょう。

</details>

---

### 問題3：head要素の中身
次のうち、`<head>` 要素の中に配置**できない**ものはどれですか？

A. `<meta charset="UTF-8">`
B. `<title>ページタイトル</title>`
C. `<p>段落テキスト</p>`
D. `<link rel="stylesheet" href="style.css">`
E. `<script src="app.js"></script>`

<details>
<summary>解答</summary>

**C. `<p>段落テキスト</p>`**

`<p>` はコンテンツを表示する要素で、`<body>` 内に配置します。`<head>` には meta, title, link, style, script, base, noscript のみ配置できます。

</details>

---

### 問題4：lang属性の重要性
`<html lang="ja">` の `lang="ja"` を指定する主な理由を3つ挙げてください。

<details>
<summary>解答例</summary>

1. **スクリーンリーダー**が正しい言語で読み上げるため（日本語の音声合成エンジンが使われる）
2. **検索エンジン**がページの言語を判定するヒントにするため
3. **翻訳ツール**が翻訳の要否を正しく判定するため

その他に、ブラウザのフォント選択やハイフネーション処理の参考にもなります。

</details>

---

### 問題5：エラー修正
以下のHTMLには複数の問題があります。すべて見つけて修正してください。

```html
<html>
<head>
<title>マイページ
</head>
<body>
<h1>ようこそ</h1>
<p>はじめてのページです
</body>
</html>
```

<details>
<summary>ヒント</summary>

DOCTYPE宣言、lang属性、meta charset、閉じタグの忘れを確認してください。

</details>

<details>
<summary>解答例</summary>

問題点：
1. `<!DOCTYPE html>` がない
2. `<html>` に `lang` 属性がない
3. `<meta charset="UTF-8">` がない
4. `<meta name="viewport">` がない
5. `<title>` の閉じタグがない
6. `<p>` の閉じタグがない

修正後：
```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>マイページ</title>
</head>
<body>
  <h1>ようこそ</h1>
  <p>はじめてのページです</p>
</body>
</html>
```

</details>

---

## 応用問題

### 問題6：空要素の識別
次のHTML要素のうち、空要素（終了タグが不要な要素）をすべて選んでください。

A. `<br>`
B. `<p>`
C. `<img>`
D. `<div>`
E. `<hr>`
F. `<input>`
G. `<span>`
H. `<meta>`

<details>
<summary>解答</summary>

**A. `<br>`、C. `<img>`、E. `<hr>`、F. `<input>`、H. `<meta>`**

空要素は内容を持たず、終了タグが不要です。`<p>`, `<div>`, `<span>` は通常の要素で、開始タグと終了タグが必要です。

</details>

---

## チャレンジ問題

### 問題7：自己紹介ページの作成
以下の要件を満たすHTMLファイル `index.html` を作成してください。

- 正しいHTMLテンプレート構造
- タイトルは「自己紹介 | ○○のホームページ」（○○はあなたの名前）
- body内に見出し（h1）で名前
- 段落（p）で自己紹介文を2〜3段落
- コメントで「ここに画像を追加予定」と記述

<details>
<summary>解答例</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>自己紹介 | 田中のホームページ</title>
</head>
<body>
  <h1>田中太郎</h1>
  <!-- ここに画像を追加予定 -->
  <p>はじめまして、田中太郎です。Web開発を学んでいます。</p>
  <p>趣味はプログラミングと読書です。最近はHTMLとCSSを勉強中です。</p>
  <p>このページでは、学習の記録を公開していく予定です。</p>
</body>
</html>
```

</details>
