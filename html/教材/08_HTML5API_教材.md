# 第8章：HTML5の便利な要素とAPI

## この章のゴール
- data-* 属性（カスタムデータ属性）を使ってHTMLにデータを埋め込む方法を習得する
- details / summary 要素でアコーディオンUIを作成できる
- dialog 要素でモーダルダイアログを実装できる
- progress / meter 要素で進捗や測定値を視覚的に表現できる
- その他の HTML5 要素（template, output, wbr 等）を理解し活用できる

---

## 8.1 data-* 属性（カスタムデータ属性）

`data-*` 属性を使うと、HTML要素に**独自のデータ**を埋め込むことができます。JavaScriptやCSSからアクセスでき、見た目には影響しません。

### 基本構文
```html
<div data-user-id="12345" data-role="admin" data-active="true">
  ユーザー情報
</div>
```

### 命名ルール
- `data-` で始まり、その後に任意の名前を付ける
- 名前は**小文字の英字**とハイフンで構成する
- 大文字、コロン、ピリオドは使わない

```html
<!-- 良い例 -->
<div data-product-id="100" data-category="electronics">商品</div>

<!-- 悪い例 -->
<div data-ProductID="100">商品</div>  <!-- 大文字はNG -->
```

### JavaScriptからのアクセス（dataset）

```html
<article id="post" data-author="tanaka" data-post-id="42" data-published="2024-03-15">
  <h2>記事タイトル</h2>
</article>

<script>
  const post = document.getElementById('post');

  // data属性の読み取り（ハイフンがキャメルケースに変換される）
  console.log(post.dataset.author);     // "tanaka"
  console.log(post.dataset.postId);     // "42"（data-post-id → postId）
  console.log(post.dataset.published);  // "2024-03-15"

  // data属性の設定
  post.dataset.views = "100";
  // → <article data-views="100" ...>
</script>
```

> **ポイント**: `data-post-id` のようなハイフン区切りは、JavaScript の `dataset` プロパティでは `postId` のようにキャメルケースに変換されます。

### CSSからのアクセス

```html
<style>
  /* data属性の値を表示 */
  [data-tooltip]:hover::after {
    content: attr(data-tooltip);
    position: absolute;
    background: #333;
    color: #fff;
    padding: 0.3em 0.6em;
    border-radius: 4px;
    font-size: 0.8em;
  }

  /* data属性による条件付きスタイル */
  [data-status="active"] {
    color: green;
  }
  [data-status="inactive"] {
    color: gray;
  }
</style>

<span data-tooltip="これはツールチップです" style="position: relative; cursor: help;">
  ホバーしてね
</span>

<p data-status="active">アクティブなユーザー</p>
<p data-status="inactive">非アクティブなユーザー</p>
```

### data属性の活用例

```html
<!-- 商品カード -->
<div class="product-card"
     data-product-id="SKU-001"
     data-price="2980"
     data-category="books"
     data-in-stock="true">
  <h3>HTML入門書</h3>
  <p>価格：2,980円</p>
  <button onclick="addToCart(this.closest('[data-product-id]').dataset)">
    カートに追加
  </button>
</div>

<!-- タブUI -->
<div data-tab-group="settings">
  <button data-tab-target="general">一般</button>
  <button data-tab-target="display">表示</button>
  <button data-tab-target="privacy">プライバシー</button>
</div>
```

### data属性を使うべき場面と使うべきでない場面
| 場面 | 推奨 |
|---|---|
| JSやCSSで使う補助データ | data属性を使う |
| ツールチップやUI状態 | data属性を使う |
| SEO に関わる情報 | メタタグや構造化データを使う |
| スクリーンリーダーに伝える情報 | ARIA属性を使う |
| 大量のデータの格納 | JavaScript変数やAPIを使う |

---

## 8.2 details / summary 要素：アコーディオン

`<details>` と `<summary>` を使うと、**JavaScriptなし**で開閉可能なアコーディオンUIが作れます。

### 基本構文
```html
<details>
  <summary>クリックして詳細を表示</summary>
  <p>ここに隠されたコンテンツが入ります。summaryをクリックすると表示されます。</p>
</details>
```

### 初期状態を開いた状態にする
```html
<details open>
  <summary>最初から開いている</summary>
  <p>ページ読み込み時から表示されています。</p>
</details>
```

### FAQセクションの例
```html
<h2>よくある質問</h2>

<details>
  <summary>送料はいくらですか？</summary>
  <p>全国一律500円です。5,000円以上のご注文で送料無料になります。</p>
</details>

<details>
  <summary>返品・交換はできますか？</summary>
  <p>商品到着から7日以内であれば、未使用品に限り返品・交換を承ります。
     返品の場合は、カスタマーサポートまでご連絡ください。</p>
</details>

<details>
  <summary>配送にかかる日数はどのくらいですか？</summary>
  <p>ご注文から通常2〜3営業日でお届けいたします。
     北海道・沖縄・離島は追加で1〜2日かかる場合があります。</p>
</details>
```

### スタイルのカスタマイズ
```html
<style>
  details {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 0.5em;
    margin-bottom: 0.5em;
  }
  summary {
    font-weight: bold;
    cursor: pointer;
    padding: 0.5em;
  }
  summary:hover {
    background-color: #f0f0f0;
  }
  /* 開いた時のマーカーを変更 */
  details[open] summary {
    border-bottom: 1px solid #ddd;
    margin-bottom: 0.5em;
  }
  /* デフォルトの三角マーカーを非表示にする */
  summary::marker {
    content: "";
  }
  /* カスタムマーカー */
  summary::before {
    content: "▶ ";
  }
  details[open] summary::before {
    content: "▼ ";
  }
</style>
```

### details のイベント（JavaScript）
```html
<details id="my-details">
  <summary>詳細を表示</summary>
  <p>コンテンツ</p>
</details>

<script>
  const details = document.getElementById('my-details');
  details.addEventListener('toggle', () => {
    if (details.open) {
      console.log('開かれました');
    } else {
      console.log('閉じられました');
    }
  });
</script>
```

---

## 8.3 dialog 要素：ダイアログ（モーダル）

`<dialog>` 要素は、モーダルダイアログやポップアップを作成するためのHTML標準の要素です。

### 基本構文

```html
<dialog id="my-dialog">
  <h2>確認</h2>
  <p>この操作を実行しますか？</p>
  <form method="dialog">
    <button value="cancel">キャンセル</button>
    <button value="confirm">確認</button>
  </form>
</dialog>

<button onclick="document.getElementById('my-dialog').showModal()">
  ダイアログを開く
</button>
```

### dialog の表示方法
| メソッド | 動作 |
|---|---|
| `show()` | 非モーダルで表示（背景を操作できる） |
| `showModal()` | モーダルで表示（背景を操作できない、背景が暗くなる） |
| `close()` | ダイアログを閉じる |

### モーダルダイアログの完全な例

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>dialog要素のデモ</title>
  <style>
    dialog {
      border: none;
      border-radius: 8px;
      padding: 2em;
      max-width: 400px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    dialog::backdrop {
      background: rgba(0, 0, 0, 0.5);
    }
    dialog h2 {
      margin-top: 0;
    }
    .dialog-buttons {
      display: flex;
      justify-content: flex-end;
      gap: 0.5em;
      margin-top: 1.5em;
    }
    .dialog-buttons button {
      padding: 0.5em 1.5em;
      border: 1px solid #ccc;
      border-radius: 4px;
      cursor: pointer;
    }
    .btn-primary {
      background: #4285f4;
      color: white;
      border-color: #4285f4;
    }
  </style>
</head>
<body>
  <h1>dialog要素のデモ</h1>
  <button id="open-btn">削除の確認</button>
  <p id="result"></p>

  <dialog id="confirm-dialog">
    <h2>削除の確認</h2>
    <p>このアイテムを削除してもよろしいですか？この操作は取り消せません。</p>
    <div class="dialog-buttons">
      <form method="dialog">
        <button value="cancel">キャンセル</button>
        <button value="delete" class="btn-primary">削除する</button>
      </form>
    </div>
  </dialog>

  <script>
    const dialog = document.getElementById('confirm-dialog');
    const openBtn = document.getElementById('open-btn');
    const result = document.getElementById('result');

    openBtn.addEventListener('click', () => {
      dialog.showModal();
    });

    dialog.addEventListener('close', () => {
      result.textContent = '選択結果: ' + dialog.returnValue;
    });
  </script>
</body>
</html>
```

### dialog の特徴
- `showModal()` で表示すると、**背景の操作がブロック**される
- `::backdrop` 疑似要素で背景のスタイルを変更できる
- `Escape` キーで閉じることができる（デフォルト動作）
- `<form method="dialog">` 内のボタンで閉じると、`returnValue` にボタンの `value` が設定される
- `autofocus` 属性を付けた要素に自動フォーカスされる

### アクセシビリティの配慮
```html
<dialog id="my-dialog" aria-labelledby="dialog-title" aria-describedby="dialog-desc">
  <h2 id="dialog-title">アカウント削除</h2>
  <p id="dialog-desc">アカウントを削除すると、すべてのデータが失われます。</p>
  <form method="dialog">
    <button value="cancel">キャンセル</button>
    <button value="delete" autofocus>削除する</button>
  </form>
</dialog>
```

---

## 8.4 progress 要素：進捗バー

`<progress>` は処理の**進捗状況**を視覚的に表示します。

### 基本構文
```html
<!-- 確定的な進捗（値がわかっている） -->
<progress value="70" max="100">70%</progress>

<!-- 不確定な進捗（値が不明、ローディング表示） -->
<progress>読み込み中...</progress>
```

### 属性
| 属性 | 説明 |
|---|---|
| `value` | 現在の進捗値 |
| `max` | 最大値（デフォルト: 1.0） |

### 活用例

```html
<h3>ファイルアップロード</h3>
<label for="upload-progress">アップロード進捗：</label>
<progress id="upload-progress" value="0" max="100">0%</progress>
<span id="upload-text">0%</span>

<script>
  // 進捗の更新（実際にはfetchやXMLHttpRequestと組み合わせる）
  function updateProgress(percent) {
    const bar = document.getElementById('upload-progress');
    const text = document.getElementById('upload-text');
    bar.value = percent;
    text.textContent = percent + '%';
  }
</script>
```

```html
<!-- スキルレベルの表示 -->
<h3>スキル</h3>
<p>
  HTML：<progress value="90" max="100">90%</progress> 90%
</p>
<p>
  CSS：<progress value="75" max="100">75%</progress> 75%
</p>
<p>
  JavaScript：<progress value="60" max="100">60%</progress> 60%
</p>
```

---

## 8.5 meter 要素：測定値の表示

`<meter>` はある範囲内の**測定値やスカラー量**を表示します。progress と似ていますが、`<meter>` は「進捗」ではなく「既知の範囲内の値」を表します。

### 基本構文
```html
<meter value="0.7" min="0" max="1">70%</meter>
```

### 属性
| 属性 | 説明 |
|---|---|
| `value` | 現在の値（**必須**） |
| `min` | 最小値（デフォルト: 0） |
| `max` | 最大値（デフォルト: 1） |
| `low` | 「低い」と見なす閾値 |
| `high` | 「高い」と見なす閾値 |
| `optimum` | 「最適」な値の位置 |

### 色が変わる仕組み

`low`, `high`, `optimum` を使うと、値に応じてバーの色が自動で変わります（ブラウザ依存）。

```html
<!-- ディスク使用量（低い方が良い） -->
<p>ディスク使用量：
  <meter value="20" min="0" max="100" low="50" high="80" optimum="30">
    20GB / 100GB
  </meter>
</p>

<!-- 体温（36.5付近が最適） -->
<p>体温：
  <meter value="36.5" min="35" max="42" low="36" high="37.5" optimum="36.5">
    36.5度
  </meter>
</p>

<!-- バッテリー残量 -->
<p>バッテリー：
  <meter value="15" min="0" max="100" low="20" high="80" optimum="90">
    15%
  </meter>
  <!-- low(20)未満なので警告色（赤/黄）で表示される -->
</p>
```

### progress と meter の違い
| 要素 | 用途 | 例 |
|---|---|---|
| `<progress>` | 処理の進捗 | アップロード、ダウンロード |
| `<meter>` | 範囲内の測定値 | ディスク容量、得点、温度 |

---

## 8.6 template 要素

`<template>` 要素は、**ページ上に表示されない**HTMLテンプレートを定義します。JavaScriptからクローンして使います。

```html
<!-- テンプレート定義（非表示） -->
<template id="card-template">
  <div class="card">
    <h3 class="card-title"></h3>
    <p class="card-body"></p>
  </div>
</template>

<!-- テンプレートから要素を生成 -->
<div id="card-container"></div>

<script>
  const template = document.getElementById('card-template');
  const container = document.getElementById('card-container');

  const items = [
    { title: 'HTML入門', body: 'HTMLの基本を学びます' },
    { title: 'CSS入門', body: 'CSSの基本を学びます' },
    { title: 'JS入門', body: 'JavaScriptの基本を学びます' }
  ];

  items.forEach(item => {
    const clone = template.content.cloneNode(true);
    clone.querySelector('.card-title').textContent = item.title;
    clone.querySelector('.card-body').textContent = item.body;
    container.appendChild(clone);
  });
</script>
```

### template の特徴
- `<template>` 内のコンテンツはレンダリングされない
- 画像のダウンロードやスクリプトの実行も行われない
- `content` プロパティで DocumentFragment としてアクセスできる
- `cloneNode(true)` でコピーして使い回す

---

## 8.7 wbr 要素：改行可能位置

`<wbr>`（Word Break Opportunity）は、ブラウザに「ここで改行してもよい」と伝えます。長い文字列が画面幅を超える場合に役立ちます。

```html
<p>このURLは長いです：
  https://www.example.com/<wbr>very/<wbr>long/<wbr>path/<wbr>to/<wbr>page
</p>

<p>ファイルパス：
  C:\Users\<wbr>tanaka\<wbr>Documents\<wbr>projects\<wbr>my-website
</p>
```

- 通常時は改行されない
- 画面幅が足りなくなった時だけ `<wbr>` の位置で改行される
- `<br>` とは違い、強制改行ではない

---

## 8.8 実践：HTML5要素の総合デモ

以下はこの章で学んだ要素を組み合わせた動作するHTMLページです。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HTML5要素のデモ</title>
  <style>
    body {
      font-family: sans-serif;
      max-width: 700px;
      margin: 2em auto;
      padding: 0 1em;
      line-height: 1.6;
    }
    section {
      margin-bottom: 2em;
      padding: 1em;
      border: 1px solid #ddd;
      border-radius: 8px;
    }
    h2 { color: #333; border-bottom: 2px solid #4285f4; padding-bottom: 0.3em; }
    details { margin: 0.5em 0; }
    summary { cursor: pointer; font-weight: bold; }
    .card {
      border: 1px solid #ccc;
      border-radius: 4px;
      padding: 1em;
      margin: 0.5em 0;
      background: #fafafa;
    }
    dialog { border: none; border-radius: 8px; padding: 2em; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
    dialog::backdrop { background: rgba(0,0,0,0.5); }
    meter, progress { width: 200px; }
  </style>
</head>
<body>
  <h1>HTML5要素のデモ</h1>

  <!-- data属性 -->
  <section>
    <h2>data-* 属性</h2>
    <div id="user-info" data-user-id="42" data-role="admin">
      <p>ユーザー情報（data属性に格納）</p>
      <button onclick="showData()">data属性を表示</button>
      <p id="data-output"></p>
    </div>
  </section>

  <!-- details / summary -->
  <section>
    <h2>details / summary（FAQ）</h2>
    <details>
      <summary>HTMLとは何ですか？</summary>
      <p>HTMLはWebページの構造を記述するマークアップ言語です。</p>
    </details>
    <details>
      <summary>CSSとの違いは？</summary>
      <p>HTMLが「構造」を担当し、CSSが「見た目」を担当します。</p>
    </details>
    <details open>
      <summary>この項目は最初から開いています</summary>
      <p>open属性を付けると、初期状態で展開されます。</p>
    </details>
  </section>

  <!-- dialog -->
  <section>
    <h2>dialog（モーダル）</h2>
    <button id="dialog-open">ダイアログを開く</button>
    <p id="dialog-result"></p>

    <dialog id="demo-dialog" aria-labelledby="dlg-title">
      <h3 id="dlg-title">設定の変更</h3>
      <p>設定を保存しますか？</p>
      <form method="dialog">
        <button value="cancel">キャンセル</button>
        <button value="save">保存する</button>
      </form>
    </dialog>
  </section>

  <!-- progress / meter -->
  <section>
    <h2>progress と meter</h2>
    <h3>progress（進捗バー）</h3>
    <p>
      <label>ダウンロード：</label>
      <progress id="demo-progress" value="0" max="100">0%</progress>
      <span id="progress-text">0%</span>
      <button onclick="startProgress()">開始</button>
    </p>

    <h3>meter（測定値）</h3>
    <p>
      ディスク使用量：
      <meter value="65" min="0" max="100" low="50" high="80" optimum="30">65%</meter>
      65GB / 100GB
    </p>
    <p>
      バッテリー残量：
      <meter value="15" min="0" max="100" low="20" high="80" optimum="90">15%</meter>
      15%（低残量）
    </p>
    <p>
      テストの得点：
      <meter value="85" min="0" max="100" low="40" high="70" optimum="100">85点</meter>
      85点（良好）
    </p>
  </section>

  <!-- template -->
  <section>
    <h2>template（テンプレート）</h2>
    <button onclick="addCards()">カードを追加</button>
    <div id="card-container"></div>

    <template id="card-tmpl">
      <div class="card">
        <h4 class="card-title"></h4>
        <p class="card-desc"></p>
      </div>
    </template>
  </section>

  <script>
    // data属性の表示
    function showData() {
      const el = document.getElementById('user-info');
      const output = document.getElementById('data-output');
      output.textContent = 'userId=' + el.dataset.userId + ', role=' + el.dataset.role;
    }

    // dialogの制御
    const dialog = document.getElementById('demo-dialog');
    document.getElementById('dialog-open').addEventListener('click', () => {
      dialog.showModal();
    });
    dialog.addEventListener('close', () => {
      document.getElementById('dialog-result').textContent =
        '選択結果: ' + dialog.returnValue;
    });

    // progressのアニメーション
    function startProgress() {
      const bar = document.getElementById('demo-progress');
      const text = document.getElementById('progress-text');
      let value = 0;
      bar.value = 0;
      const interval = setInterval(() => {
        value += 2;
        bar.value = value;
        text.textContent = value + '%';
        if (value >= 100) {
          clearInterval(interval);
          text.textContent = '完了！';
        }
      }, 50);
    }

    // templateからカード生成
    function addCards() {
      const tmpl = document.getElementById('card-tmpl');
      const container = document.getElementById('card-container');
      container.innerHTML = '';
      const data = [
        { title: 'HTML', desc: 'Webの構造を記述する言語' },
        { title: 'CSS', desc: 'Webの見た目を装飾する言語' },
        { title: 'JavaScript', desc: 'Webに動きを加える言語' }
      ];
      data.forEach(item => {
        const clone = tmpl.content.cloneNode(true);
        clone.querySelector('.card-title').textContent = item.title;
        clone.querySelector('.card-desc').textContent = item.desc;
        container.appendChild(clone);
      });
    }
  </script>
</body>
</html>
```

---

## 8.9 よくある間違い

### 1. data属性の名前に大文字を使う
```html
<!-- 悪い例：大文字を使っている -->
<div data-userName="tanaka">

<!-- 良い例：小文字とハイフンを使う -->
<div data-user-name="tanaka">
```

### 2. details の中に summary がない
```html
<!-- 悪い例：summaryがないとクリックできない -->
<details>
  <p>隠されたコンテンツ</p>
</details>

<!-- 良い例 -->
<details>
  <summary>クリックで表示</summary>
  <p>隠されたコンテンツ</p>
</details>
```

### 3. progress と meter の混同
```html
<!-- 悪い例：ディスク容量にprogressを使う -->
<progress value="65" max="100">65%</progress>

<!-- 良い例：測定値にはmeterを使う -->
<meter value="65" min="0" max="100">65%</meter>
```

### 4. dialog を show() で開いて背景をブロックできない
```html
<!-- show() は非モーダル（背景操作可能） -->
<script>dialog.show();</script>

<!-- showModal() がモーダル（背景操作ブロック） -->
<script>dialog.showModal();</script>
```

### 5. template 内のコンテンツをDOMに追加し忘れる
```html
<!-- template.content を cloneNode して appendChild する必要がある -->
<script>
  // 悪い例：templateの要素を直接使う
  const tmpl = document.getElementById('my-template');
  container.appendChild(tmpl); // templateごと移動してしまう

  // 良い例：cloneNodeで複製してから追加
  const clone = tmpl.content.cloneNode(true);
  container.appendChild(clone);
</script>
```

---

## 8.10 アクセシビリティのベストプラクティス

### details / summary
- `<summary>` のテキストは具体的にする
- アコーディオン内のコンテンツもスクリーンリーダーで読めることを確認する

### dialog
- `aria-labelledby` でダイアログのタイトルを指定する
- `aria-describedby` で説明文を指定する
- モーダルを閉じたとき、フォーカスを元のボタンに戻す
- `Escape` キーで閉じられることを確保する（showModal のデフォルト動作）

### progress / meter
- テキストの代替値（タグ内のテキスト）を必ず記述する
- `<label>` で何の進捗/測定値かを明示する

```html
<!-- アクセシブルなprogress -->
<label for="dl-progress">ダウンロード進捗：</label>
<progress id="dl-progress" value="45" max="100">45%</progress>

<!-- アクセシブルなmeter -->
<label for="disk-usage">ディスク使用量：</label>
<meter id="disk-usage" value="65" min="0" max="100">65GB / 100GB</meter>
```

---

## ポイントまとめ

| 要素・属性 | 説明 |
|---|---|
| `data-*` | カスタムデータ属性。JSの `dataset` でアクセス |
| `<details>` | 開閉可能なコンテンツコンテナ |
| `<summary>` | details の見出し（クリック可能部分） |
| `<dialog>` | ダイアログ / モーダルウィンドウ |
| `showModal()` | モーダルとして表示（背景ブロック） |
| `<progress>` | 処理の進捗を視覚表示 |
| `<meter>` | 範囲内の測定値を視覚表示 |
| `<template>` | 非表示のHTMLテンプレート |
| `<wbr>` | 改行可能な位置を示す |

---

## シリーズのまとめ

ここまでの8章で、HTMLの基礎から実践的なテクニックまでを一通り学びました。

| 章 | テーマ | 主な内容 |
|---|---|---|
| 第1章 | HTMLの基本構造 | DOCTYPE, html, head, body |
| 第2章 | テキストとリンク | h1〜h6, p, a, strong, em |
| 第3章 | 画像とマルチメディア | img, video, audio, picture |
| 第4章 | リストとテーブル | ul, ol, dl, table |
| 第5章 | フォーム | input, form, validation |
| 第6章 | セマンティックHTML | header, nav, main, article, ARIA |
| 第7章 | メタ情報とhead | meta, OGP, favicon, link |
| 第8章 | HTML5の便利な要素 | data属性, details, dialog, progress |

次のステップとして、CSSでHTMLにスタイルを付けることを学んでいきましょう。
