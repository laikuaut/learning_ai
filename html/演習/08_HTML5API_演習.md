# 第8章 演習：HTML5の便利な要素とAPI

---

## 基本問題

### 問題1：data-* 属性の基本
以下の要件を満たす商品カードのHTMLを書いてください。

- div 要素に以下の data 属性を設定：
  - 商品ID: `SKU-1234`
  - カテゴリ: `electronics`
  - 価格: `4980`
  - 在庫: `true`
- 表示内容：商品名「ワイヤレスイヤホン」と価格「4,980円」

<details>
<summary>解答例</summary>

```html
<div class="product-card"
     data-product-id="SKU-1234"
     data-category="electronics"
     data-price="4980"
     data-in-stock="true">
  <h3>ワイヤレスイヤホン</h3>
  <p>4,980円</p>
</div>
```

<!--
  data-* 属性の命名ルール：
  - data- で始まる
  - 小文字の英字とハイフンで構成する
  - 大文字やコロンは使わない
  JavaScriptからは dataset プロパティでアクセスできます（例: element.dataset.productId）。
-->

</details>

---

### 問題2：data属性の JavaScript アクセス
問題1の商品カードに対して、JavaScript で以下を行うコードを書いてください。

1. 商品IDを取得して console.log に出力
2. 価格を取得して数値に変換
3. 新しく `data-views="500"` を設定

<details>
<summary>解答例</summary>

```html
<script>
  const card = document.querySelector('.product-card');

  // 1. 商品IDの取得（data-product-id → dataset.productId）
  console.log(card.dataset.productId);  // "SKU-1234"

  // 2. 価格を数値に変換
  const price = Number(card.dataset.price);
  console.log(price);  // 4980

  // 3. 新しいdata属性を設定
  card.dataset.views = "500";
  // HTMLに data-views="500" が追加される
</script>
```

<!-- ハイフン区切り（data-product-id）はJavaScriptではキャメルケース（productId）に変換されます。 -->

</details>

---

### 問題3：details / summary でFAQ
以下の3つのQ&Aを `<details>` / `<summary>` でアコーディオン形式にしてください。

- Q1: 送料はいくらですか？ → A: 全国一律500円です。5,000円以上で送料無料。
- Q2: 返品はできますか？ → A: 商品到着から7日以内、未使用品のみ返品可能です。
- Q3: 支払い方法は？ → A: クレジットカード、銀行振込、コンビニ払いに対応しています。

<details>
<summary>解答例</summary>

```html
<h2>よくある質問</h2>

<details>
  <summary>送料はいくらですか？</summary>
  <p>全国一律500円です。5,000円以上のご注文で送料無料になります。</p>
</details>

<details>
  <summary>返品はできますか？</summary>
  <p>商品到着から7日以内であれば、未使用品に限り返品を承ります。</p>
</details>

<details>
  <summary>支払い方法は？</summary>
  <p>クレジットカード、銀行振込、コンビニ払いに対応しています。</p>
</details>
```

<!-- details/summary を使うと、JavaScriptなしでクリックによる開閉が実現できます。open 属性を付けると初期状態で開きます。 -->

</details>

---

### 問題4：dialog 要素
以下の条件を満たすモーダルダイアログを作成してください。

- 「設定を削除」ボタンをクリックすると確認ダイアログが開く
- ダイアログ内に「本当に削除しますか？」のメッセージ
- 「キャンセル」ボタンと「削除する」ボタン
- キャンセルでダイアログを閉じる

<details>
<summary>ヒント</summary>

`<dialog>` 要素の `showModal()` メソッドでモーダルとして表示し、`close()` で閉じます。`<form method="dialog">` を使うとボタンクリックで自動的にダイアログが閉じます。

</details>

<details>
<summary>解答例</summary>

```html
<!-- ダイアログを開くボタン -->
<button onclick="document.getElementById('confirmDialog').showModal()">
  設定を削除
</button>

<!-- dialog 要素 -->
<dialog id="confirmDialog">
  <h2>確認</h2>
  <p>本当に削除しますか？この操作は取り消せません。</p>
  <!-- form method="dialog" でボタンクリック時にダイアログが自動で閉じる -->
  <form method="dialog">
    <button value="cancel">キャンセル</button>
    <button value="delete">削除する</button>
  </form>
</dialog>
```

<!--
  showModal() はモーダルとして表示（背景が暗くなり、ダイアログ外の操作をブロック）。
  show() は非モーダルとして表示（背景操作も可能）。
  form method="dialog" を使うと、ボタンの value が dialog の returnValue に設定されます。
-->

</details>

---

### 問題5：progress と meter
以下の要件に合う要素を作成してください。

1. ファイルアップロードの進捗が70%であることを示す `<progress>` 要素
2. ディスク使用率が 80GB / 100GB（警戒レベル）であることを示す `<meter>` 要素

<details>
<summary>解答例</summary>

```html
<!-- 1. progress: タスクの進捗 -->
<label for="upload">アップロード進捗：</label>
<progress id="upload" value="70" max="100">70%</progress>

<!-- 2. meter: 既知の範囲内の測定値 -->
<label for="disk">ディスク使用率：</label>
<meter id="disk" value="80" min="0" max="100"
       low="30" high="70" optimum="20">80GB / 100GB</meter>
```

<!--
  progress: 進行中のタスクの完了度合いを示す（0〜max）。value を省略すると不確定状態（アニメーション）になります。
  meter: 既知の範囲内の数値を示す。low/high/optimum でブラウザが色分けの判断をします。
  high を超える値は「警戒レベル」として赤系の色で表示されることが多いです。
-->

</details>

---

## 応用問題

### 問題6：data属性を使ったフィルタリング
以下のような商品リストを作成し、カテゴリのボタンをクリックすると該当する商品だけが表示されるようにしてください（JavaScript を使います）。

- 商品: りんご（果物）、牛乳（飲料）、パン（主食）、バナナ（果物）、お茶（飲料）
- フィルタボタン: 全て、果物、飲料、主食

<details>
<summary>ヒント</summary>

各商品の div に `data-category` 属性を設定し、ボタンクリック時に `querySelectorAll` と `display` スタイルの切り替えで表示/非表示を制御します。

</details>

<details>
<summary>解答例</summary>

```html
<!-- フィルタボタン -->
<div>
  <button onclick="filterProducts('all')">全て</button>
  <button onclick="filterProducts('fruit')">果物</button>
  <button onclick="filterProducts('drink')">飲料</button>
  <button onclick="filterProducts('staple')">主食</button>
</div>

<!-- 商品リスト（data-category でカテゴリを設定） -->
<div id="products">
  <div class="product" data-category="fruit">りんご</div>
  <div class="product" data-category="drink">牛乳</div>
  <div class="product" data-category="staple">パン</div>
  <div class="product" data-category="fruit">バナナ</div>
  <div class="product" data-category="drink">お茶</div>
</div>

<script>
  function filterProducts(category) {
    // すべての商品を取得
    const products = document.querySelectorAll('.product');

    products.forEach(product => {
      if (category === 'all' || product.dataset.category === category) {
        // 条件に合う商品を表示
        product.style.display = '';
      } else {
        // 条件に合わない商品を非表示
        product.style.display = 'none';
      }
    });
  }
</script>
```

<!--
  data-category 属性でHTMLにカテゴリ情報を埋め込み、
  JavaScriptから dataset.category でアクセスしてフィルタリングしています。
  これがdata属性の典型的な活用パターンです。
-->

</details>

---

### 問題7：details のネストとスタイリング
以下の要件を満たすナレッジベースのUIを作成してください。

- 大カテゴリ：「アカウント」「支払い」の2つ（details で開閉）
- 各大カテゴリ内に小カテゴリの details を2つずつ配置
- CSS でスタイルを整える（ボーダー、パディング、カーソル変更）

<details>
<summary>解答例</summary>

```html
<style>
  details {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 0.5em;
    margin-bottom: 0.5em;
  }
  details details {
    /* ネストした details のスタイル */
    border-color: #eee;
    margin-left: 1em;
  }
  summary {
    font-weight: bold;
    cursor: pointer;
    padding: 0.3em;
  }
  summary:hover {
    background-color: #f0f0f0;
    border-radius: 4px;
  }
</style>

<h2>ヘルプセンター</h2>

<details>
  <summary>アカウント</summary>

  <details>
    <summary>パスワードを忘れた場合</summary>
    <p>ログイン画面の「パスワードを忘れた方」リンクから再設定できます。登録メールアドレスに再設定用のリンクが送信されます。</p>
  </details>

  <details>
    <summary>メールアドレスを変更したい</summary>
    <p>マイページの「アカウント設定」から変更可能です。変更後、確認メールが新しいアドレスに送信されます。</p>
  </details>
</details>

<details>
  <summary>支払い</summary>

  <details>
    <summary>対応している支払い方法</summary>
    <p>クレジットカード（Visa, Mastercard, JCB）、銀行振込、コンビニ払いに対応しています。</p>
  </details>

  <details>
    <summary>請求書の発行について</summary>
    <p>マイページの「注文履歴」から各注文の請求書をPDFで発行できます。</p>
  </details>
</details>
```

</details>

---

## チャレンジ問題

### 問題8：インタラクティブな商品ページの作成
以下の要件を満たす完全なHTMLページを作成してください。

- ページタイトル「商品詳細」
- 商品情報を data 属性で管理（商品ID、カテゴリ、価格、在庫状態）
- 商品画像のプレースホルダー（alt属性を適切に設定）
- 商品説明を details/summary で折りたたみ表示
- 「カートに入れる」ボタンクリックで dialog による確認ダイアログを表示
- 在庫状況を meter 要素で表示（例：残り12個 / 最大50個）
- ユーザーレビューの星評価を meter で表現
- data属性を使ったタグフィルタリング機能（最低2カテゴリ分のタグ）

<details>
<summary>解答例</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>商品詳細</title>
  <style>
    body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
    details { border: 1px solid #ddd; border-radius: 4px; padding: 0.8em; margin: 0.5em 0; }
    summary { font-weight: bold; cursor: pointer; }
    .tag { display: inline-block; padding: 4px 12px; margin: 4px;
           border: 1px solid #007bff; border-radius: 16px; cursor: pointer;
           background: #fff; color: #007bff; }
    .tag.active { background: #007bff; color: #fff; }
    .review { padding: 8px; border-bottom: 1px solid #eee; }
    .review[data-category] { display: block; }
    dialog { border-radius: 8px; border: 1px solid #ccc; padding: 1.5em; }
    dialog::backdrop { background: rgba(0, 0, 0, 0.5); }
  </style>
</head>
<body>
  <!-- 商品情報（data属性で管理） -->
  <div id="product"
       data-product-id="ITEM-5678"
       data-category="electronics"
       data-price="12800"
       data-in-stock="true">

    <h1>ワイヤレスBluetoothスピーカー</h1>
    <img src="speaker.jpg" alt="黒いワイヤレスBluetoothスピーカーの外観写真"
         width="400" height="300">
    <p>価格：<strong>12,800円</strong>（税込）</p>

    <!-- 在庫状況（meter） -->
    <p>在庫状況：
      <meter value="12" min="0" max="50" low="10" high="40" optimum="50">
        残り12個
      </meter>
      残り12個
    </p>

    <!-- 商品説明（details/summary） -->
    <details open>
      <summary>商品説明</summary>
      <p>高音質Bluetoothスピーカー。IPX7防水対応で、アウトドアでも安心して使えます。バッテリー持続時間は最大12時間です。</p>
    </details>

    <details>
      <summary>仕様</summary>
      <ul>
        <li>Bluetooth 5.3 対応</li>
        <li>防水規格: IPX7</li>
        <li>バッテリー: 最大12時間</li>
        <li>重量: 350g</li>
      </ul>
    </details>

    <!-- カートに入れるボタン -->
    <button onclick="document.getElementById('cartDialog').showModal()">
      カートに入れる
    </button>

    <!-- 確認ダイアログ -->
    <dialog id="cartDialog">
      <h2>カートに追加</h2>
      <p>「ワイヤレスBluetoothスピーカー」をカートに追加しますか？</p>
      <form method="dialog">
        <button value="cancel">キャンセル</button>
        <button value="add">追加する</button>
      </form>
    </dialog>
  </div>

  <!-- レビューセクション -->
  <h2>ユーザーレビュー</h2>
  <p>総合評価：
    <meter value="4.2" min="0" max="5" optimum="5">4.2 / 5</meter>
    4.2 / 5（15件）
  </p>

  <!-- タグフィルタ -->
  <div>
    <span class="tag active" onclick="filterReviews('all')">全て</span>
    <span class="tag" onclick="filterReviews('positive')">高評価</span>
    <span class="tag" onclick="filterReviews('negative')">低評価</span>
  </div>

  <div id="reviews">
    <div class="review" data-category="positive">
      <strong>満足です！</strong>
      <meter value="5" min="0" max="5">5/5</meter>
      <p>音質がとても良く、防水機能も安心です。</p>
    </div>
    <div class="review" data-category="positive">
      <strong>コスパ最高</strong>
      <meter value="4" min="0" max="5">4/5</meter>
      <p>この価格帯では十分な性能です。</p>
    </div>
    <div class="review" data-category="negative">
      <strong>少し重い</strong>
      <meter value="3" min="0" max="5">3/5</meter>
      <p>音質は良いですが、持ち運びには少し重いです。</p>
    </div>
  </div>

  <script>
    function filterReviews(category) {
      const reviews = document.querySelectorAll('.review');
      const tags = document.querySelectorAll('.tag');

      // タグのアクティブ状態を切り替え
      tags.forEach(tag => tag.classList.remove('active'));
      event.target.classList.add('active');

      // レビューのフィルタリング
      reviews.forEach(review => {
        if (category === 'all' || review.dataset.category === category) {
          review.style.display = '';
        } else {
          review.style.display = 'none';
        }
      });
    }
  </script>
</body>
</html>
```

</details>
