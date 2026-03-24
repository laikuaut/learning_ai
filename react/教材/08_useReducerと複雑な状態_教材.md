# 第8章：useReducerと複雑な状態

## この章で学ぶこと

- useReducerの基本的な使い方
- action / reducer パターン
- useReducer vs useState の使い分け
- useReducer + useContext の組み合わせ
- 実践的なアプリケーション

---

## 1. useReducerとは？

**useReducer**は、useStateの代替として使えるフックです。状態の更新ロジックが複雑な場合や、複数の状態が密接に関連している場合に適しています。

### useStateでは辛くなるケース

```jsx
// 問題：関連する複数のstateを個別に管理している
function ShoppingCart() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [itemCount, setItemCount] = useState(0);
  const [discount, setDiscount] = useState(0);

  const addItem = (item) => {
    setItems([...items, item]);
    setTotal(total + item.price);
    setItemCount(itemCount + 1);
    if (itemCount + 1 >= 3) setDiscount(10); // 3個以上で10%割引
  };

  // 更新の整合性を保つのが大変...
}
```

useReducerなら、1つのreducer関数で全ての状態更新を一元管理できます。

---

## 2. useReducerの基本

### 基本構文

```jsx
import { useReducer } from 'react';

// reducer関数：現在のstateとactionを受け取り、新しいstateを返す
function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    case 'reset':
      return { count: 0 };
    default:
      return state;
  }
}

function Counter() {
  // useReducer(reducer関数, 初期state)
  const [state, dispatch] = useReducer(reducer, { count: 0 });

  return (
    <div>
      <h2>カウント: {state.count}</h2>
      <button onClick={() => dispatch({ type: 'decrement' })}>-1</button>
      <button onClick={() => dispatch({ type: 'reset' })}>リセット</button>
      <button onClick={() => dispatch({ type: 'increment' })}>+1</button>
    </div>
  );
}
```

### 用語の整理

| 用語 | 説明 |
|------|------|
| **state** | 現在の状態（オブジェクト） |
| **action** | 「何をするか」を表すオブジェクト。`type` プロパティが必須 |
| **dispatch** | actionを送信する関数。`dispatch({ type: '...' })` |
| **reducer** | stateとactionを受け取り、新しいstateを返す純粋関数 |

### actionにデータを持たせる（payload）

```jsx
function reducer(state, action) {
  switch (action.type) {
    case 'set_name':
      return { ...state, name: action.payload };
    case 'set_age':
      return { ...state, age: action.payload };
    case 'reset':
      return { name: '', age: 0 };
    default:
      return state;
  }
}

function UserForm() {
  const [state, dispatch] = useReducer(reducer, { name: '', age: 0 });

  return (
    <div>
      <input
        value={state.name}
        onChange={(e) => dispatch({ type: 'set_name', payload: e.target.value })}
        placeholder="名前"
      />
      <input
        type="number"
        value={state.age}
        onChange={(e) => dispatch({ type: 'set_age', payload: Number(e.target.value) })}
        placeholder="年齢"
      />
      <button onClick={() => dispatch({ type: 'reset' })}>リセット</button>
      <p>名前: {state.name}, 年齢: {state.age}</p>
    </div>
  );
}
```

---

## 3. 実践：Todoアプリ

```jsx
import { useReducer, useState } from 'react';

// 初期state
const initialState = {
  todos: [],
  filter: 'all', // all, active, completed
};

// reducer
function todoReducer(state, action) {
  switch (action.type) {
    case 'add':
      return {
        ...state,
        todos: [
          ...state.todos,
          { id: Date.now(), text: action.payload, completed: false },
        ],
      };

    case 'toggle':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.payload
            ? { ...todo, completed: !todo.completed }
            : todo
        ),
      };

    case 'delete':
      return {
        ...state,
        todos: state.todos.filter(todo => todo.id !== action.payload),
      };

    case 'edit':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.payload.id
            ? { ...todo, text: action.payload.text }
            : todo
        ),
      };

    case 'set_filter':
      return { ...state, filter: action.payload };

    case 'clear_completed':
      return {
        ...state,
        todos: state.todos.filter(todo => !todo.completed),
      };

    default:
      return state;
  }
}

function TodoApp() {
  const [state, dispatch] = useReducer(todoReducer, initialState);
  const [input, setInput] = useState('');

  const handleAdd = () => {
    if (input.trim() === '') return;
    dispatch({ type: 'add', payload: input });
    setInput('');
  };

  // フィルタリング
  const filteredTodos = state.todos.filter(todo => {
    if (state.filter === 'active') return !todo.completed;
    if (state.filter === 'completed') return todo.completed;
    return true;
  });

  const activeCount = state.todos.filter(t => !t.completed).length;

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <h1>Todoアプリ</h1>

      {/* 入力エリア */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleAdd()}
          placeholder="新しいタスク..."
          style={{ flex: 1, padding: '8px' }}
        />
        <button onClick={handleAdd}>追加</button>
      </div>

      {/* フィルタボタン */}
      <div style={{ marginBottom: '16px' }}>
        {['all', 'active', 'completed'].map(filter => (
          <button
            key={filter}
            onClick={() => dispatch({ type: 'set_filter', payload: filter })}
            style={{
              marginRight: '8px',
              fontWeight: state.filter === filter ? 'bold' : 'normal',
              backgroundColor: state.filter === filter ? '#3498db' : '#ecf0f1',
              color: state.filter === filter ? 'white' : '#333',
              border: 'none',
              padding: '4px 12px',
              borderRadius: '4px',
            }}
          >
            {filter === 'all' ? 'すべて' : filter === 'active' ? '未完了' : '完了済み'}
          </button>
        ))}
      </div>

      {/* Todoリスト */}
      {filteredTodos.map(todo => (
        <div key={todo.id} style={{
          display: 'flex', alignItems: 'center', gap: '8px',
          padding: '8px', margin: '4px 0', backgroundColor: '#f9f9f9', borderRadius: '4px',
        }}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => dispatch({ type: 'toggle', payload: todo.id })}
          />
          <span style={{
            flex: 1,
            textDecoration: todo.completed ? 'line-through' : 'none',
            color: todo.completed ? '#999' : '#333',
          }}>
            {todo.text}
          </span>
          <button onClick={() => dispatch({ type: 'delete', payload: todo.id })}>
            削除
          </button>
        </div>
      ))}

      {/* フッター */}
      <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'space-between' }}>
        <span>残り {activeCount} 件</span>
        <button onClick={() => dispatch({ type: 'clear_completed' })}>
          完了済みを削除
        </button>
      </div>
    </div>
  );
}
```

---

## 4. useState vs useReducer

| 比較項目 | useState | useReducer |
|----------|----------|------------|
| 適したケース | シンプルな状態（数値、文字列、真偽値） | 複雑なオブジェクト/配列の状態 |
| 更新ロジック | set関数の中で直接記述 | reducer関数に集約 |
| 関連する状態 | 個別に管理 | 1つのstateオブジェクトで管理 |
| テスト | コンポーネントのテストが必要 | reducerを単体テストしやすい |
| デバッグ | set関数の呼び出し箇所を追う | action.typeでログを取りやすい |
| 学習コスト | 低い | やや高い |

### 判断基準

```jsx
// useStateが適している
const [name, setName] = useState("");           // 単純な値
const [isOpen, setIsOpen] = useState(false);     // 真偽値

// useReducerが適している
// - 状態がオブジェクトで複数のプロパティがある
// - 状態の更新パターンが多い
// - 次の状態が前の状態に依存する
// - 複数の状態が連動して変わる
const [state, dispatch] = useReducer(reducer, {
  items: [],
  filter: 'all',
  sortBy: 'date',
  page: 1,
});
```

---

## 5. useReducer + useContext：ミニRedux

useReducerとuseContextを組み合わせると、グローバルな状態管理ができます。

```jsx
import { createContext, useContext, useReducer } from 'react';

// --- Context定義 ---
const AppContext = createContext();

// --- Reducer ---
const initialState = {
  user: null,
  theme: 'light',
  notifications: [],
};

function appReducer(state, action) {
  switch (action.type) {
    case 'LOGIN':
      return { ...state, user: action.payload };
    case 'LOGOUT':
      return { ...state, user: null };
    case 'TOGGLE_THEME':
      return { ...state, theme: state.theme === 'light' ? 'dark' : 'light' };
    case 'ADD_NOTIFICATION':
      return {
        ...state,
        notifications: [...state.notifications, { id: Date.now(), ...action.payload }],
      };
    case 'REMOVE_NOTIFICATION':
      return {
        ...state,
        notifications: state.notifications.filter(n => n.id !== action.payload),
      };
    default:
      return state;
  }
}

// --- Provider ---
function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

// --- カスタムフック ---
function useAppState() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppStateはAppProviderの中で使用してください');
  }
  return context;
}

// --- コンポーネント ---
function Header() {
  const { state, dispatch } = useAppState();

  return (
    <header style={{
      padding: '16px',
      backgroundColor: state.theme === 'light' ? '#fff' : '#333',
      color: state.theme === 'light' ? '#333' : '#fff',
    }}>
      <h1>マイアプリ</h1>
      <button onClick={() => dispatch({ type: 'TOGGLE_THEME' })}>
        テーマ切替
      </button>
      {state.user ? (
        <span>こんにちは、{state.user.name}さん</span>
      ) : (
        <button onClick={() => dispatch({ type: 'LOGIN', payload: { name: '太郎' } })}>
          ログイン
        </button>
      )}
    </header>
  );
}

function App() {
  return (
    <AppProvider>
      <Header />
    </AppProvider>
  );
}
```

---

## 6. reducerのテスト

reducer関数は純粋関数なので、単体テストが簡単です。

```jsx
// テスト例（Jest）
describe('todoReducer', () => {
  test('タスクを追加できる', () => {
    const state = { todos: [], filter: 'all' };
    const action = { type: 'add', payload: '買い物' };
    const newState = todoReducer(state, action);

    expect(newState.todos).toHaveLength(1);
    expect(newState.todos[0].text).toBe('買い物');
    expect(newState.todos[0].completed).toBe(false);
  });

  test('タスクの完了を切り替えられる', () => {
    const state = {
      todos: [{ id: 1, text: 'テスト', completed: false }],
      filter: 'all',
    };
    const action = { type: 'toggle', payload: 1 };
    const newState = todoReducer(state, action);

    expect(newState.todos[0].completed).toBe(true);
  });
});
```

---

## まとめ

| 項目 | ポイント |
|------|---------|
| useReducer | 複雑な状態管理のためのフック |
| reducer | `(state, action) => newState` の純粋関数 |
| action | `{ type: '...', payload: ... }` で何をするかを指示 |
| dispatch | actionを送信してstateを更新する関数 |
| vs useState | シンプルならuseState、複雑ならuseReducer |
| + useContext | 組み合わせてグローバル状態管理を実現 |
| テスト | reducerは純粋関数なので単体テストしやすい |

### 次の章では

**React Router**を使って、複数ページのSPA（Single Page Application）を構築する方法を学びます。

---

## 動作サンプル

この章の概念を実装した完全なサンプルコードは `サンプル/08_ShoppingCart.jsx` にあります。useReducerによるカート管理、dispatch/actionパターンを実際に動かして確認できます。
