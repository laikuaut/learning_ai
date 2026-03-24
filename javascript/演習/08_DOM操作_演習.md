# 第8章：DOM操作 - 演習問題

---

## 基本問題

### 問題1：要素の取得と内容変更

以下のHTMLを前提として、JavaScriptで指定された操作を行ってください。

```html
<div id="app">
  <h1 class="title">タイトル</h1>
  <p class="description">説明文です</p>
  <ul class="list">
    <li class="item">項目1</li>
    <li class="item">項目2</li>
    <li class="item">項目3</li>
  </ul>
</div>
```

1. `h1` のテキストを `"新しいタイトル"` に変更
2. `.description` のテキストを取得して表示
3. すべての `.item` のテキストを配列に格納して表示

**期待される出力：**
```
説明文です
["項目1", "項目2", "項目3"]
```

<details>
<summary>解答例</summary>

```javascript
// 1. テキストの変更
const title = document.querySelector(".title");
title.textContent = "新しいタイトル";

// 2. テキストの取得
const desc = document.querySelector(".description");
console.log(desc.textContent);

// 3. 全ての.itemのテキストを配列に格納
const items = document.querySelectorAll(".item");
const texts = [...items].map(item => item.textContent);
console.log(JSON.stringify(texts));
```

</details>

---

### 問題2：要素の作成と追加

JavaScriptで以下の操作を行ってください。

1. `<p>` 要素を作成し、テキスト `"動的に追加された段落です"` を設定
2. クラス `"dynamic"` を追加
3. `#app` の末尾に追加
4. `<ul class="list">` の中に `<li>` 要素 `"項目4"` と `"項目5"` を追加

**期待される出力（HTML構造）：**
```html
<p class="dynamic">動的に追加された段落です</p>
<!-- #app の末尾に追加される -->

<li>項目4</li>
<li>項目5</li>
<!-- .list の末尾に追加される -->
```

<details>
<summary>解答例</summary>

```javascript
// 1-3. p要素の作成と追加
const p = document.createElement("p");
p.textContent = "動的に追加された段落です";
p.className = "dynamic";
document.getElementById("app").append(p);

// 4. li要素の追加
const list = document.querySelector(".list");
const items = ["項目4", "項目5"];
items.forEach(text => {
  const li = document.createElement("li");
  li.textContent = text;
  list.append(li);
});
```

</details>

---

### 問題3：クラスの操作

ボタンをクリックしたときに、以下のクラス操作を行うHTMLファイルを作成してください。

1. `"highlight"` クラスの追加
2. `"active"` クラスのトグル（あれば削除、なければ追加）
3. `"old-style"` クラスを `"new-style"` に置き換え

**HTMLテンプレート：**
```html
<div id="box" class="box old-style">対象の要素</div>
<button id="addBtn">highlightを追加</button>
<button id="toggleBtn">activeをトグル</button>
<button id="replaceBtn">スタイルを置換</button>
```

<details>
<summary>解答例</summary>

```javascript
const box = document.getElementById("box");

// highlight クラスの追加
document.getElementById("addBtn").addEventListener("click", () => {
  box.classList.add("highlight");
  console.log("クラス:", [...box.classList].join(", "));
});

// active クラスのトグル
document.getElementById("toggleBtn").addEventListener("click", () => {
  box.classList.toggle("active");
  console.log("activeクラス:", box.classList.contains("active") ? "あり" : "なし");
});

// クラスの置き換え
document.getElementById("replaceBtn").addEventListener("click", () => {
  box.classList.replace("old-style", "new-style");
  console.log("クラス:", [...box.classList].join(", "));
});
```

</details>

---

### 問題4：スタイルの操作

JavaScriptでボックス要素のスタイルを動的に変更してください。

```html
<div id="styledBox">スタイル変更テスト</div>
<button id="styleBtn">スタイルを変更</button>
```

ボタンクリック時に以下のスタイルを設定：
- 背景色: `#3498db`（青）
- 文字色: `white`
- パディング: `20px`
- 角丸: `8px`
- フォントサイズ: `18px`

<details>
<summary>解答例</summary>

```javascript
document.getElementById("styleBtn").addEventListener("click", () => {
  const box = document.getElementById("styledBox");
  // Object.assign で複数のスタイルを一度に設定
  Object.assign(box.style, {
    backgroundColor: "#3498db",
    color: "white",
    padding: "20px",
    borderRadius: "8px",
    fontSize: "18px"
  });
});
```

</details>

---

## 応用問題

### 問題5：リストの動的生成

以下のデータからテーブルをDOMで動的に生成してください。

```javascript
const users = [
  { name: "太郎", age: 25, city: "東京" },
  { name: "花子", age: 22, city: "大阪" },
  { name: "次郎", age: 30, city: "福岡" },
  { name: "美咲", age: 28, city: "札幌" }
];
```

ヘッダー行を含む見やすいテーブルを `#app` に追加してください。

<details>
<summary>解答例</summary>

```javascript
const users = [
  { name: "太郎", age: 25, city: "東京" },
  { name: "花子", age: 22, city: "大阪" },
  { name: "次郎", age: 30, city: "福岡" },
  { name: "美咲", age: 28, city: "札幌" }
];

// テーブルの作成
const table = document.createElement("table");
table.style.borderCollapse = "collapse";
table.style.width = "100%";

// ヘッダー行
const thead = document.createElement("thead");
const headerRow = document.createElement("tr");
["名前", "年齢", "都市"].forEach(text => {
  const th = document.createElement("th");
  th.textContent = text;
  th.style.border = "1px solid #ddd";
  th.style.padding = "10px";
  th.style.backgroundColor = "#3498db";
  th.style.color = "white";
  headerRow.append(th);
});
thead.append(headerRow);
table.append(thead);

// データ行
const tbody = document.createElement("tbody");
users.forEach(user => {
  const tr = document.createElement("tr");
  [user.name, user.age, user.city].forEach(value => {
    const td = document.createElement("td");
    td.textContent = value;
    td.style.border = "1px solid #ddd";
    td.style.padding = "10px";
    tr.append(td);
  });
  tbody.append(tr);
});
table.append(tbody);

document.getElementById("app").append(table);
```

</details>

---

### 問題6：要素の削除と入れ替え

リスト内の要素を操作する機能を作成してください。

1. 指定した番号のリスト項目を削除する関数
2. リストの全項目をクリアする関数
3. 指定した番号のリスト項目を新しいテキストに置換する関数

```html
<ul id="myList">
  <li>項目A</li>
  <li>項目B</li>
  <li>項目C</li>
  <li>項目D</li>
</ul>
```

<details>
<summary>解答例</summary>

```javascript
const list = document.getElementById("myList");

// 1. 指定番号の項目を削除（0始まり）
function removeItem(index) {
  const items = list.querySelectorAll("li");
  if (index >= 0 && index < items.length) {
    items[index].remove();
  }
}

// 2. 全項目をクリア
function clearList() {
  while (list.firstChild) {
    list.removeChild(list.firstChild);
  }
}

// 3. 指定番号の項目を置換
function replaceItem(index, newText) {
  const items = list.querySelectorAll("li");
  if (index >= 0 && index < items.length) {
    const newLi = document.createElement("li");
    newLi.textContent = newText;
    items[index].replaceWith(newLi);
  }
}

// テスト
replaceItem(1, "項目B（更新済み）");
removeItem(2); // 項目Cを削除
```

</details>

---

## チャレンジ問題

### 問題7：簡易TODOリスト（DOM操作のみ）

HTMLファイル1つで完結する簡易TODOリストを作成してください。以下の機能を持つこと：

1. テキスト入力欄とボタンでTODO項目を追加
2. 各項目に「完了」ボタンと「削除」ボタンを追加
3. 完了ボタンを押すと取り消し線を表示
4. 削除ボタンを押すと項目を削除

<details>
<summary>ヒント</summary>

- `createElement` で要素を作成し、イベントリスナーを設定してから `append` します。
- 完了は `style.textDecoration = "line-through"` で取り消し線を設定します。
- 削除は `element.remove()` で要素を削除します。

</details>

<details>
<summary>解答例</summary>

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>簡易TODOリスト</title>
  <style>
    body { font-family: sans-serif; max-width: 400px; margin: 40px auto; }
    input { padding: 8px; width: 200px; }
    button { padding: 8px 12px; cursor: pointer; }
    li { padding: 8px 0; display: flex; align-items: center; gap: 8px; }
    .completed { text-decoration: line-through; color: #999; }
  </style>
</head>
<body>
  <h1>TODOリスト</h1>
  <div>
    <input type="text" id="todoInput" placeholder="やることを入力">
    <button id="addBtn">追加</button>
  </div>
  <ul id="todoList"></ul>

  <script>
    const input = document.getElementById("todoInput");
    const addBtn = document.getElementById("addBtn");
    const todoList = document.getElementById("todoList");

    function addTodo() {
      const text = input.value.trim();
      if (!text) return;

      const li = document.createElement("li");

      const span = document.createElement("span");
      span.textContent = text;

      const completeBtn = document.createElement("button");
      completeBtn.textContent = "完了";
      completeBtn.addEventListener("click", () => {
        span.classList.toggle("completed");
      });

      const deleteBtn = document.createElement("button");
      deleteBtn.textContent = "削除";
      deleteBtn.addEventListener("click", () => {
        li.remove();
      });

      li.append(span, completeBtn, deleteBtn);
      todoList.append(li);
      input.value = "";
      input.focus();
    }

    addBtn.addEventListener("click", addTodo);
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") addTodo();
    });
  </script>
</body>
</html>
```

</details>
