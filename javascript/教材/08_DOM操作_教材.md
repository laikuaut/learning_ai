# 第8章: DOM操作

## この章のゴール

- DOMの基本概念（ツリー構造）を理解する
- 要素の取得・作成・追加・削除ができるようになる
- 要素の属性・スタイル・クラスを操作できる
- DOM操作の現場パターンを身につける

---

## 8.1 DOMとは

DOM（Document Object Model）は、HTMLをJavaScriptで操作するための仕組みです。ブラウザはHTMLをツリー構造のオブジェクトに変換し、JavaScriptからアクセスできるようにします。

```
HTML:
  <html>
    <head><title>My Page</title></head>
    <body>
      <h1>見出し</h1>
      <p>段落</p>
    </body>
  </html>

DOMツリー:
  document
    └── html
        ├── head
        │   └── title
        │       └── "My Page"
        └── body
            ├── h1
            │   └── "見出し"
            └── p
                └── "段落"
```

---

## 8.2 要素の取得

```html
<!-- この HTML を前提とします -->
<div id="app">
  <h1 class="title">メインタイトル</h1>
  <ul class="list">
    <li class="item">項目1</li>
    <li class="item">項目2</li>
    <li class="item active">項目3</li>
  </ul>
  <input type="text" name="username" />
</div>
```

```javascript
// ★ getElementById — IDで1つの要素を取得
const app = document.getElementById("app");

// ★ querySelector — CSSセレクタで最初の1つを取得（推奨）
const title = document.querySelector(".title");
const firstItem = document.querySelector(".item");
const input = document.querySelector('input[name="username"]');

// ★ querySelectorAll — CSSセレクタで全て取得（NodeList）
const items = document.querySelectorAll(".item");
console.log(items.length); // 3

// NodeListはforEachで反復可能
items.forEach((item, index) => {
  console.log(`${index}: ${item.textContent}`);
});

// 配列に変換（map等を使いたい場合）
const itemArray = [...items];
const texts = itemArray.map(item => item.textContent);
console.log(texts); // ["項目1", "項目2", "項目3"]

// getElementsByClassName（HTMLCollection を返す）
const itemsByClass = document.getElementsByClassName("item");
// ※ HTMLCollection は forEach が使えないので注意

// getElementsByTagName
const listItems = document.getElementsByTagName("li");
```

```
querySelector vs getElementById の使い分け:

  getElementById("myId")       → IDで取得（高速）
  querySelector("#myId")       → IDで取得（同じ結果）
  querySelector(".myClass")    → クラスで取得
  querySelector("div > p")     → 複雑なセレクタ
  querySelectorAll(".item")    → 複数取得

  → 基本は querySelector / querySelectorAll を使えばOK
```

---

## 8.3 要素の内容操作

```javascript
const element = document.querySelector(".title");

// textContent — テキストのみ（HTMLタグは無視）
console.log(element.textContent); // "メインタイトル"
element.textContent = "新しいタイトル";

// innerHTML — HTMLを含む内容（XSS注意！）
element.innerHTML = "<strong>太字</strong>のタイトル";

// innerText — 表示されているテキスト（非表示要素は除外）
console.log(element.innerText);
```

```
textContent vs innerHTML の違い:

  textContent:
    ・テキストのみを扱う
    ・HTMLタグは文字列として表示される
    ・安全（XSSリスクなし）
    ・高速

  innerHTML:
    ・HTMLとして解釈・描画される
    ・XSSリスクあり → ユーザー入力は使わない！
    ・テンプレート的に使える
```

```javascript
// ★ XSSの危険な例（絶対にやってはいけない）
// const userInput = '<img src=x onerror="alert(1)">';
// element.innerHTML = userInput; // 悪意のあるスクリプトが実行される！

// ★ 安全な方法
// element.textContent = userInput; // テキストとして表示される
```

---

## 8.4 要素の作成と追加

```javascript
// 要素の作成
const newDiv = document.createElement("div");
newDiv.textContent = "新しい要素です";
newDiv.className = "message";

// 親要素に追加
const app = document.getElementById("app");

// append — 末尾に追加（推奨）
app.append(newDiv);

// prepend — 先頭に追加
app.prepend(newDiv);

// 特定の要素の前に挿入
const title = document.querySelector(".title");
app.insertBefore(newDiv, title);

// before / after — 要素の前後に挿入（推奨）
title.before(newDiv);  // titleの直前
title.after(newDiv);   // titleの直後
```

### リストの動的生成

```javascript
// 実用例: データからリストを生成
const fruits = ["りんご", "みかん", "バナナ", "ぶどう"];

const ul = document.createElement("ul");
ul.className = "fruit-list";

fruits.forEach(fruit => {
  const li = document.createElement("li");
  li.textContent = fruit;
  ul.append(li);
});

document.getElementById("app").append(ul);
```

### DocumentFragment（大量の要素を効率的に追加）

```javascript
// DocumentFragmentを使うと、DOMへのアクセスが1回で済む
const fragment = document.createDocumentFragment();

for (let i = 0; i < 100; i++) {
  const li = document.createElement("li");
  li.textContent = `項目 ${i + 1}`;
  fragment.append(li);
}

// 1回のDOM操作で全てを追加（パフォーマンスが良い）
document.querySelector(".list").append(fragment);
```

---

## 8.5 要素の削除

```javascript
// remove() — 自分自身を削除（推奨）
const element = document.querySelector(".item");
element.remove();

// removeChild() — 親から子を削除（従来の方法）
const list = document.querySelector(".list");
const firstChild = list.firstElementChild;
list.removeChild(firstChild);

// 全ての子要素を削除
const container = document.getElementById("app");
container.innerHTML = ""; // 簡単だがイベントリスナーの解放に注意

// より安全な方法
while (container.firstChild) {
  container.removeChild(container.firstChild);
}

// replaceWith — 要素の置換
const oldElement = document.querySelector(".title");
const newElement = document.createElement("h2");
newElement.textContent = "新しい見出し";
oldElement.replaceWith(newElement);
```

---

## 8.6 属性の操作

```javascript
const link = document.querySelector("a");

// getAttribute / setAttribute
console.log(link.getAttribute("href")); // URL文字列
link.setAttribute("href", "https://example.com");
link.setAttribute("target", "_blank");

// hasAttribute / removeAttribute
console.log(link.hasAttribute("target")); // true
link.removeAttribute("target");

// 直接プロパティでアクセス（一般的な属性）
link.href = "https://example.com";
link.id = "myLink";

// data属性（カスタムデータ）
// HTML: <div data-user-id="123" data-role="admin">
const div = document.querySelector("[data-user-id]");
console.log(div.dataset.userId); // "123"（キャメルケースに変換される）
console.log(div.dataset.role);   // "admin"
div.dataset.status = "active";   // data-status="active" が追加される
```

---

## 8.7 クラスの操作

```javascript
const element = document.querySelector(".item");

// classList — クラスの操作（推奨）
element.classList.add("highlight");      // クラスを追加
element.classList.remove("active");      // クラスを削除
element.classList.toggle("visible");     // あれば削除、なければ追加
element.classList.contains("highlight"); // 含まれるか確認 → true

// 複数クラスを一度に操作
element.classList.add("bold", "large", "primary");
element.classList.remove("bold", "large");

// replace — クラスの置き換え
element.classList.replace("primary", "secondary");

// className — クラス属性全体を操作（上書き注意）
element.className = "item new-class"; // 全てのクラスが置き換わる
```

---

## 8.8 スタイルの操作

```javascript
const box = document.querySelector(".box");

// style プロパティ（インラインスタイル）
box.style.backgroundColor = "blue";   // background-color
box.style.fontSize = "20px";          // font-size
box.style.border = "2px solid red";
box.style.display = "none";           // 非表示
box.style.display = "";               // スタイルを解除（CSSに戻る）

// 複数スタイルを一度に設定
Object.assign(box.style, {
  width: "200px",
  height: "100px",
  padding: "10px",
  borderRadius: "8px"
});

// getComputedStyle — 計算済みスタイルの取得
const computed = getComputedStyle(box);
console.log(computed.width);           // "200px"
console.log(computed.backgroundColor); // "rgb(0, 0, 255)"
```

```
CSS プロパティ名 → JavaScript プロパティ名:

  background-color  →  backgroundColor
  font-size         →  fontSize
  border-radius     →  borderRadius
  z-index           →  zIndex
  margin-top        →  marginTop

  ハイフン区切り → キャメルケースに変換
```

---

## 8.9 要素の位置とサイズ

```javascript
const element = document.querySelector(".box");

// getBoundingClientRect — ビューポート相対の位置とサイズ
const rect = element.getBoundingClientRect();
console.log(rect.top);     // 上端のY座標
console.log(rect.left);    // 左端のX座標
console.log(rect.width);   // 幅
console.log(rect.height);  // 高さ
console.log(rect.bottom);  // 下端のY座標
console.log(rect.right);   // 右端のX座標

// オフセット（親要素からの相対位置）
console.log(element.offsetTop);    // 親要素からの上位置
console.log(element.offsetLeft);   // 親要素からの左位置
console.log(element.offsetWidth);  // ボーダー含む幅
console.log(element.offsetHeight); // ボーダー含む高さ

// スクロール関連
console.log(element.scrollTop);    // スクロール量
console.log(element.scrollHeight); // スクロール可能な全体の高さ

// スクロール操作
element.scrollTo({ top: 0, behavior: "smooth" }); // 先頭に滑らかスクロール
element.scrollIntoView({ behavior: "smooth" });    // 要素を画面内に表示
```

---

## 8.10 DOMの走査（トラバーサル）

```javascript
const item = document.querySelector(".item");

// 親要素
console.log(item.parentElement);       // 直接の親
console.log(item.closest(".list"));    // 最も近い祖先要素（セレクタで検索）

// 子要素
const list = document.querySelector(".list");
console.log(list.children);           // HTMLCollection（要素のみ）
console.log(list.childNodes);         // NodeList（テキストノードも含む）
console.log(list.firstElementChild);  // 最初の子要素
console.log(list.lastElementChild);   // 最後の子要素
console.log(list.childElementCount);  // 子要素の数

// 兄弟要素
console.log(item.previousElementSibling); // 前の兄弟要素
console.log(item.nextElementSibling);     // 次の兄弟要素
```

---

## 8.11 現場で使われるパターン

### テーブルの動的生成

```javascript
function createTable(headers, rows) {
  const table = document.createElement("table");
  table.style.borderCollapse = "collapse";

  // ヘッダー行
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  headers.forEach(text => {
    const th = document.createElement("th");
    th.textContent = text;
    th.style.border = "1px solid #ccc";
    th.style.padding = "8px";
    th.style.backgroundColor = "#f5f5f5";
    headerRow.append(th);
  });
  thead.append(headerRow);
  table.append(thead);

  // データ行
  const tbody = document.createElement("tbody");
  rows.forEach(rowData => {
    const tr = document.createElement("tr");
    rowData.forEach(cellText => {
      const td = document.createElement("td");
      td.textContent = cellText;
      td.style.border = "1px solid #ccc";
      td.style.padding = "8px";
      tr.append(td);
    });
    tbody.append(tr);
  });
  table.append(tbody);

  return table;
}

// 使用例
const table = createTable(
  ["名前", "年齢", "都市"],
  [
    ["太郎", "25", "東京"],
    ["花子", "22", "大阪"],
    ["次郎", "30", "福岡"]
  ]
);
document.body.append(table);
```

### 表示/非表示の切り替え

```javascript
function toggleVisibility(selector) {
  const el = document.querySelector(selector);
  if (el.style.display === "none") {
    el.style.display = "";
  } else {
    el.style.display = "none";
  }
}

// CSSクラスを使う方法（推奨）
// CSS: .hidden { display: none; }
function toggleHidden(selector) {
  document.querySelector(selector).classList.toggle("hidden");
}
```

---

## よくある間違い

### 1. DOMが読み込まれる前にアクセスする

```html
<!-- NG: bodyの前に配置するとnullになる -->
<head>
  <script>
    const title = document.querySelector("h1"); // null!
  </script>
</head>
<body>
  <h1>見出し</h1>
</body>

<!-- OK: scriptをbodyの末尾に配置 -->
<body>
  <h1>見出し</h1>
  <script>
    const title = document.querySelector("h1"); // OK
  </script>
</body>

<!-- OK: DOMContentLoaded イベントを使う -->
<head>
  <script>
    document.addEventListener("DOMContentLoaded", () => {
      const title = document.querySelector("h1"); // OK
    });
  </script>
</head>
```

### 2. innerHTMLにユーザー入力を入れる

```javascript
// NG（XSSの危険性）
// element.innerHTML = userInput;

// OK
element.textContent = userInput;
```

### 3. querySelectorAll の戻り値は配列ではない

```javascript
const items = document.querySelectorAll(".item");
// items.map(...); // エラー！NodeListにmapはない

// 配列に変換してから使う
[...items].map(item => item.textContent);
```

---

## ポイントまとめ

- DOMはHTMLをツリー構造で表現したもので、JavaScriptから操作できます
- `querySelector` / `querySelectorAll` がCSSセレクタで柔軟に要素を取得できるため推奨です
- `textContent` はテキストのみ、`innerHTML` はHTMLを含みますがXSSに注意が必要です
- 要素の作成は `createElement` → プロパティ設定 → `append` の流れです
- 大量の要素追加には `DocumentFragment` を使うとパフォーマンスが良くなります
- クラスの操作は `classList`（add/remove/toggle）が便利です
- スタイル操作はCSS側のクラス切り替えが推奨、直接操作は `element.style` を使います
- DOMが読み込まれてからスクリプトを実行することが重要です
