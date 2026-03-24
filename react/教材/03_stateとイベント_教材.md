# 第3章：stateとイベント

## この章で学ぶこと

- stateとは何か
- useStateフックの使い方
- イベント処理の基本
- フォーム入力の扱い方
- 複数のstateを管理する方法

---

## 1. stateとは？

**state（ステート）** は、コンポーネントが内部に持つ「変化するデータ」です。stateが変わると、Reactは自動的にUIを再描画（再レンダリング）します。

### propsとstateの違い

| | props | state |
|---|-------|-------|
| データの管理場所 | 親コンポーネント | 自分自身 |
| 変更可能か | 変更不可（読み取り専用） | 変更可能 |
| 用途 | 外部から渡されるデータ | 内部で変化するデータ |
| 例 | ユーザー名、商品情報 | 入力値、表示/非表示、カウント |

### なぜ普通の変数ではダメなのか？

```jsx
// NG：普通の変数を変更してもUIは更新されない
function Counter() {
  let count = 0;

  const handleClick = () => {
    count = count + 1;   // 値は変わるが...
    console.log(count);  // コンソールには反映されるが...
    // UIは更新されない！
  };

  return (
    <div>
      <p>カウント: {count}</p>
      <button onClick={handleClick}>+1</button>
    </div>
  );
}
```

Reactは**stateが変更されたとき**にだけ再レンダリングを行います。普通の変数を変更してもReactはそれを検知できません。

---

## 2. useState

`useState`はReactの**フック（Hook）** の1つで、コンポーネントにstateを持たせるための関数です。

### 基本構文

```jsx
import { useState } from 'react';

function Counter() {
  // useState(初期値) → [現在の値, 更新関数] を返す
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>カウント: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
}
```

### useStateの解説

```jsx
const [count, setCount] = useState(0);
//     ↑       ↑                 ↑
//   現在の値  更新関数         初期値
```

| 要素 | 説明 |
|------|------|
| `count` | 現在のstateの値（任意の名前をつけられる） |
| `setCount` | stateを更新する関数（慣例で`set` + 変数名） |
| `0` | stateの初期値 |

### さまざまな型のstate

```jsx
function Examples() {
  // 数値
  const [count, setCount] = useState(0);

  // 文字列
  const [name, setName] = useState("");

  // 真偽値
  const [isVisible, setIsVisible] = useState(false);

  // 配列
  const [items, setItems] = useState([]);

  // オブジェクト
  const [user, setUser] = useState({ name: "", age: 0 });

  // ...
}
```

---

## 3. イベント処理

### 基本的なイベントハンドラ

```jsx
function ClickExample() {
  const handleClick = () => {
    alert("ボタンがクリックされました！");
  };

  return <button onClick={handleClick}>クリック</button>;
}
```

> **注意**：`onClick={handleClick}` であって、`onClick={handleClick()}` ではありません。`()`をつけるとレンダリング時に即実行されてしまいます。

### よく使うイベント

| イベント | 発火タイミング |
|----------|---------------|
| `onClick` | クリック時 |
| `onChange` | 入力値が変わった時 |
| `onSubmit` | フォーム送信時 |
| `onFocus` | フォーカスされた時 |
| `onBlur` | フォーカスが外れた時 |
| `onMouseEnter` | マウスが乗った時 |
| `onMouseLeave` | マウスが離れた時 |
| `onKeyDown` | キーを押した時 |

### イベントオブジェクト

イベントハンドラは自動的にイベントオブジェクト（`e`）を受け取ります。

```jsx
function EventInfo() {
  const handleClick = (e) => {
    console.log("イベントの種類:", e.type);       // "click"
    console.log("ターゲット:", e.target);           // クリックされた要素
    console.log("座標:", e.clientX, e.clientY);    // マウス位置
  };

  return <button onClick={handleClick}>クリックして情報を表示</button>;
}
```

### イベントハンドラに引数を渡す

```jsx
function FruitSelector() {
  const handleSelect = (fruit) => {
    alert(`${fruit}を選びました！`);
  };

  return (
    <div>
      {/* アロー関数で包んで引数を渡す */}
      <button onClick={() => handleSelect("りんご")}>りんご</button>
      <button onClick={() => handleSelect("みかん")}>みかん</button>
      <button onClick={() => handleSelect("バナナ")}>バナナ</button>
    </div>
  );
}
```

---

## 4. stateとイベントの組み合わせ

### カウンター

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  const increment = () => setCount(count + 1);
  const decrement = () => setCount(count - 1);
  const reset = () => setCount(0);

  return (
    <div>
      <h2>カウント: {count}</h2>
      <button onClick={decrement}>-1</button>
      <button onClick={reset}>リセット</button>
      <button onClick={increment}>+1</button>
    </div>
  );
}
```

### 表示/非表示の切り替え（トグル）

```jsx
import { useState } from 'react';

function Toggle() {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div>
      <button onClick={() => setIsVisible(!isVisible)}>
        {isVisible ? "隠す" : "表示する"}
      </button>

      {isVisible && (
        <div style={{ padding: '16px', backgroundColor: '#f0f0f0', marginTop: '8px' }}>
          <p>これは表示/非表示を切り替えられるコンテンツです。</p>
        </div>
      )}
    </div>
  );
}
```

---

## 5. フォーム入力の扱い

### テキスト入力（制御コンポーネント）

Reactでは、フォームの値をstateで管理するのが一般的です。これを**制御コンポーネント（Controlled Component）** と呼びます。

```jsx
import { useState } from 'react';

function NameInput() {
  const [name, setName] = useState("");

  const handleChange = (e) => {
    setName(e.target.value);
  };

  return (
    <div>
      <label>
        名前：
        <input
          type="text"
          value={name}
          onChange={handleChange}
        />
      </label>
      <p>こんにちは、{name || "ゲスト"}さん！</p>
    </div>
  );
}
```

### 複数の入力フィールド

```jsx
import { useState } from 'react';

function SignupForm() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,       // 既存の値をコピー
      [name]: value,     // 変更されたフィールドだけ更新
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();  // ページリロードを防ぐ
    console.log("送信データ:", formData);
    alert(`ようこそ、${formData.username}さん！`);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>ユーザー名：</label>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
        />
      </div>
      <div>
        <label>メール：</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
        />
      </div>
      <div>
        <label>パスワード：</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
        />
      </div>
      <button type="submit">登録</button>
    </form>
  );
}
```

### セレクトボックスとチェックボックス

```jsx
import { useState } from 'react';

function PreferencesForm() {
  const [color, setColor] = useState("blue");
  const [agree, setAgree] = useState(false);

  return (
    <div>
      {/* セレクトボックス */}
      <label>好きな色：</label>
      <select value={color} onChange={(e) => setColor(e.target.value)}>
        <option value="red">赤</option>
        <option value="blue">青</option>
        <option value="green">緑</option>
      </select>
      <p>選択した色：{color}</p>

      {/* チェックボックス */}
      <label>
        <input
          type="checkbox"
          checked={agree}
          onChange={(e) => setAgree(e.target.checked)}
        />
        利用規約に同意する
      </label>
      <p>同意状況：{agree ? "同意済み" : "未同意"}</p>
    </div>
  );
}
```

---

## 6. stateの更新に関する注意点

### 配列のstateを更新する

stateは直接変更（ミューテーション）してはいけません。新しい配列/オブジェクトを作って渡します。

```jsx
import { useState } from 'react';

function TodoSimple() {
  const [todos, setTodos] = useState(["買い物", "洗濯"]);
  const [input, setInput] = useState("");

  // 追加
  const addTodo = () => {
    if (input.trim() === "") return;
    setTodos([...todos, input]);  // スプレッド構文で新しい配列を作る
    setInput("");
  };

  // 削除
  const removeTodo = (index) => {
    setTodos(todos.filter((_, i) => i !== index));
  };

  return (
    <div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="新しいタスク"
      />
      <button onClick={addTodo}>追加</button>

      <ul>
        {todos.map((todo, index) => (
          <li key={index}>
            {todo}
            <button onClick={() => removeTodo(index)}>削除</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### NG：stateを直接変更する

```jsx
// NG：直接変更してもUIは更新されない
const addTodo = () => {
  todos.push(input);     // 配列を直接変更している
  setTodos(todos);        // 同じ参照なのでReactは変化を検知しない
};

// OK：新しい配列を作る
const addTodo = () => {
  setTodos([...todos, input]);  // 新しい配列を作って渡す
};
```

### オブジェクトのstateを更新する

```jsx
const [user, setUser] = useState({ name: "太郎", age: 25 });

// NG
user.name = "花子";
setUser(user);

// OK
setUser({ ...user, name: "花子" });
```

### 更新関数（前の値に基づく更新）

連続して更新する場合、関数形式を使うのが安全です。

```jsx
// 問題あり：バッチ処理で最後の1つしか反映されない場合がある
const handleTripleIncrement = () => {
  setCount(count + 1);
  setCount(count + 1);
  setCount(count + 1);
  // 結果：+1しか増えない！
};

// OK：関数形式なら前の値を確実に参照できる
const handleTripleIncrement = () => {
  setCount(prev => prev + 1);
  setCount(prev => prev + 1);
  setCount(prev => prev + 1);
  // 結果：+3増える
};
```

---

## 7. 実践：シンプルなメモアプリ

```jsx
import { useState } from 'react';

function MemoApp() {
  const [memos, setMemos] = useState([]);
  const [input, setInput] = useState("");

  const addMemo = () => {
    if (input.trim() === "") return;
    const newMemo = {
      id: Date.now(),
      text: input,
      createdAt: new Date().toLocaleString(),
    };
    setMemos([newMemo, ...memos]);
    setInput("");
  };

  const deleteMemo = (id) => {
    setMemos(memos.filter(memo => memo.id !== id));
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      addMemo();
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>メモアプリ</h1>

      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="メモを入力..."
          style={{ flex: 1, padding: '8px' }}
        />
        <button onClick={addMemo} style={{ padding: '8px 16px' }}>
          追加
        </button>
      </div>

      <p>{memos.length}件のメモ</p>

      {memos.map(memo => (
        <div key={memo.id} style={{
          padding: '12px',
          margin: '8px 0',
          backgroundColor: '#fffde7',
          borderRadius: '4px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <div>
            <p style={{ margin: 0 }}>{memo.text}</p>
            <small style={{ color: '#888' }}>{memo.createdAt}</small>
          </div>
          <button onClick={() => deleteMemo(memo.id)}>削除</button>
        </div>
      ))}
    </div>
  );
}

export default MemoApp;
```

---

## まとめ

| 項目 | ポイント |
|------|---------|
| state | コンポーネント内部で変化するデータ |
| useState | `const [値, set関数] = useState(初期値)` |
| 再レンダリング | stateが更新されるとUIが自動で再描画される |
| イベント | `onClick`, `onChange`, `onSubmit` などで処理を実行 |
| 制御コンポーネント | `value` + `onChange` でフォームをstateで管理 |
| 配列の更新 | `[...arr, newItem]`、`arr.filter()`で新しい配列を作る |
| オブジェクトの更新 | `{ ...obj, key: newValue }` で新しいオブジェクトを作る |
| 関数形式の更新 | `setCount(prev => prev + 1)` で前の値に基づいて安全に更新 |

### 次の章では

「**条件分岐**」と「**リストのレンダリング**」を学び、動的なUIをさらに柔軟に構築する方法を理解します。

---

## 動作サンプル

この章の概念を実装した完全なサンプルコードは `サンプル/03_Counter.jsx` にあります。useState、イベントハンドラ、制御コンポーネントを実際に動かして確認できます。
