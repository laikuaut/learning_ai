# 第8章 演習：useReducerと複雑な状態

---

## 演習1（基本）：useReducerでカウンターを作ろう

`useReducer` を使って、以下の機能を持つカウンターを作成してください。

**要件：**
- 「+1」「-1」「+10」「-10」「リセット」の5つのボタン
- カウントが0未満にならないようにする
- reducer関数で全てのアクションを処理

<details>
<summary>ヒント</summary>

`useReducer` は `reducer(state, action)` と初期値を受け取り、`[state, dispatch]` を返します。
`action.type` で処理を分岐させます。

```jsx
const [state, dispatch] = useReducer(reducer, { count: 0 });
dispatch({ type: 'increment' });
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { useReducer } from 'react';

// ========================================
// reducer関数：現在のstateとactionを受け取り、新しいstateを返す
//
// useReducerの核心はこのreducer関数。全ての状態更新ロジックが
// ここに集約されるため、状態の変更を一覧で把握できる
// ========================================
function counterReducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      // 0未満にならないようにガード
      return { count: Math.max(0, state.count - 1) };
    case 'increment_by_10':
      return { count: state.count + 10 };
    case 'decrement_by_10':
      return { count: Math.max(0, state.count - 10) };
    case 'reset':
      return { count: 0 };
    default:
      // 未知のアクションはstateをそのまま返す（安全策）
      return state;
  }
}

function Counter() {
  // ========================================
  // useReducer(reducer関数, 初期state)
  // useStateと違い、状態の「更新ロジック」がコンポーネントの外に出せる
  // ========================================
  const [state, dispatch] = useReducer(counterReducer, { count: 0 });

  const buttonStyle = { padding: '8px 16px', margin: '4px', fontSize: '16px' };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h2>useReducer カウンター</h2>
      <div style={{
        fontSize: '48px',
        fontFamily: 'monospace',
        margin: '20px 0',
        color: state.count === 0 ? '#999' : '#333',
      }}>
        {state.count}
      </div>
      <div>
        <button style={buttonStyle} onClick={() => dispatch({ type: 'decrement_by_10' })}>-10</button>
        <button style={buttonStyle} onClick={() => dispatch({ type: 'decrement' })}>-1</button>
        <button style={buttonStyle} onClick={() => dispatch({ type: 'reset' })}>リセット</button>
        <button style={buttonStyle} onClick={() => dispatch({ type: 'increment' })}>+1</button>
        <button style={buttonStyle} onClick={() => dispatch({ type: 'increment_by_10' })}>+10</button>
      </div>
    </div>
  );
}

export default Counter;
```

**ポイント：**
- `dispatch({ type: 'increment' })` のように「何をしたいか」をオブジェクトで伝えます
- reducer内で `Math.max(0, ...)` を使って不正な値にならないようガードしています
- `default` ケースで未知のアクションに対する安全策を入れておくのがベストプラクティスです

</details>

---

## 演習2（基本）：useReducerでフォーム状態を管理しよう

複数のフィールドを持つフォームの状態を `useReducer` で管理してください。

**要件：**
- 名前、メール、メッセージの3フィールド
- 各フィールドの更新、バリデーション状態の管理
- フォームのリセット
- 送信時のバリデーション

<details>
<summary>ヒント</summary>

stateにフォーム値とエラーをまとめて管理します。`action.payload` で更新するフィールド名と値を渡します。

```javascript
const initialState = {
  values: { name: '', email: '', message: '' },
  errors: {},
  isSubmitting: false,
};
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { useReducer } from 'react';

// ========================================
// 初期state：フォームの値、エラー、送信状態を一つのオブジェクトで管理
// useStateだと3つの別々のstateが必要だが、useReducerなら一元管理できる
// ========================================
const initialState = {
  values: { name: '', email: '', message: '' },
  errors: {},
  isSubmitting: false,
  isSubmitted: false,
};

// ========================================
// reducer：フォームに関する全てのアクションを処理
// ========================================
function formReducer(state, action) {
  switch (action.type) {
    // フィールドの値を更新
    case 'UPDATE_FIELD':
      return {
        ...state,
        values: {
          ...state.values,
          [action.payload.field]: action.payload.value,
        },
        // 入力があったらそのフィールドのエラーをクリア
        errors: {
          ...state.errors,
          [action.payload.field]: undefined,
        },
      };

    // バリデーションエラーをセット
    case 'SET_ERRORS':
      return {
        ...state,
        errors: action.payload,
        isSubmitting: false,
      };

    // 送信開始
    case 'SUBMIT_START':
      return { ...state, isSubmitting: true };

    // 送信成功
    case 'SUBMIT_SUCCESS':
      return { ...initialState, isSubmitted: true };

    // フォームリセット
    case 'RESET':
      return initialState;

    default:
      return state;
  }
}

// バリデーション関数（reducerの外で定義）
function validate(values) {
  const errors = {};
  if (!values.name.trim()) errors.name = '名前は必須です';
  if (!values.email.trim()) {
    errors.email = 'メールは必須です';
  } else if (!/\S+@\S+\.\S+/.test(values.email)) {
    errors.email = 'メールの形式が正しくありません';
  }
  if (!values.message.trim()) errors.message = 'メッセージは必須です';
  if (values.message.length > 200) errors.message = '200文字以内で入力してください';
  return errors;
}

function ContactForm() {
  const [state, dispatch] = useReducer(formReducer, initialState);

  const handleChange = (e) => {
    dispatch({
      type: 'UPDATE_FIELD',
      payload: { field: e.target.name, value: e.target.value },
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errors = validate(state.values);

    if (Object.keys(errors).length > 0) {
      dispatch({ type: 'SET_ERRORS', payload: errors });
      return;
    }

    dispatch({ type: 'SUBMIT_START' });
    // 疑似的なAPI呼び出し
    await new Promise(resolve => setTimeout(resolve, 1000));
    dispatch({ type: 'SUBMIT_SUCCESS' });
  };

  if (state.isSubmitted) {
    return (
      <div style={{ textAlign: 'center', padding: '40px' }}>
        <h2>送信完了！</h2>
        <p>お問い合わせありがとうございます。</p>
        <button onClick={() => dispatch({ type: 'RESET' })}>新しいメッセージ</button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <h2>お問い合わせ</h2>

      {['name', 'email', 'message'].map(field => (
        <div key={field} style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>
            {field === 'name' ? '名前' : field === 'email' ? 'メール' : 'メッセージ'}
          </label>
          {field === 'message' ? (
            <textarea
              name={field}
              value={state.values[field]}
              onChange={handleChange}
              rows={4}
              style={{
                width: '100%', padding: '8px',
                borderColor: state.errors[field] ? '#e74c3c' : '#ddd',
                borderWidth: '1px', borderStyle: 'solid', borderRadius: '4px',
              }}
            />
          ) : (
            <input
              name={field}
              type={field === 'email' ? 'email' : 'text'}
              value={state.values[field]}
              onChange={handleChange}
              style={{
                width: '100%', padding: '8px',
                borderColor: state.errors[field] ? '#e74c3c' : '#ddd',
                borderWidth: '1px', borderStyle: 'solid', borderRadius: '4px',
              }}
            />
          )}
          {state.errors[field] && (
            <p style={{ color: '#e74c3c', fontSize: '14px', margin: '4px 0 0' }}>
              {state.errors[field]}
            </p>
          )}
        </div>
      ))}

      <div style={{ display: 'flex', gap: '8px' }}>
        <button type="submit" disabled={state.isSubmitting} style={{ flex: 1, padding: '10px' }}>
          {state.isSubmitting ? '送信中...' : '送信'}
        </button>
        <button type="button" onClick={() => dispatch({ type: 'RESET' })} style={{ padding: '10px' }}>
          リセット
        </button>
      </div>
    </form>
  );
}

export default ContactForm;
```

**ポイント：**
- フォームの「値」「エラー」「送信状態」を1つのstateオブジェクトにまとめて管理
- `UPDATE_FIELD` アクションでは `action.payload.field` で更新するフィールドを動的に指定
- バリデーション関数はreducerの外に出すことでテストしやすく
- フォームが複雑になるほど、useReducerの一元管理のメリットが大きくなります

</details>

---

## 演習3（基本）：Todoリストをreducerで管理しよう

`useReducer` を使ってTodoリストのCRUD操作を実装してください。

**要件：**
- タスクの追加（ADD_TODO）
- タスクの完了切替（TOGGLE_TODO）
- タスクの削除（DELETE_TODO）
- タスクの編集（EDIT_TODO）
- 全タスクのクリア（CLEAR_ALL）

<details>
<summary>ヒント</summary>

各アクションで `action.payload` にデータを渡します。

```javascript
dispatch({ type: 'ADD_TODO', payload: { text: '新しいタスク' } });
dispatch({ type: 'TOGGLE_TODO', payload: { id: 123 } });
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { useReducer, useState } from 'react';

// ========================================
// reducer：Todoに関する全ての状態更新を一元管理
// 各caseでイミュータブルにstateを更新する（元の配列を変更しない）
// ========================================
function todoReducer(state, action) {
  switch (action.type) {
    case 'ADD_TODO':
      return [
        ...state,
        {
          id: Date.now(),
          text: action.payload.text,
          completed: false,
        },
      ];

    case 'TOGGLE_TODO':
      return state.map(todo =>
        todo.id === action.payload.id
          ? { ...todo, completed: !todo.completed }
          : todo
      );

    case 'DELETE_TODO':
      return state.filter(todo => todo.id !== action.payload.id);

    case 'EDIT_TODO':
      return state.map(todo =>
        todo.id === action.payload.id
          ? { ...todo, text: action.payload.text }
          : todo
      );

    case 'CLEAR_ALL':
      return [];

    default:
      return state;
  }
}

// 初期データ
const initialTodos = [
  { id: 1, text: 'useReducerを学ぶ', completed: true },
  { id: 2, text: 'Todoアプリを作る', completed: false },
  { id: 3, text: 'テストを書く', completed: false },
];

function TodoApp() {
  const [todos, dispatch] = useReducer(todoReducer, initialTodos);
  const [input, setInput] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editText, setEditText] = useState('');

  const handleAdd = () => {
    if (!input.trim()) return;
    dispatch({ type: 'ADD_TODO', payload: { text: input.trim() } });
    setInput('');
  };

  const startEdit = (todo) => {
    setEditingId(todo.id);
    setEditText(todo.text);
  };

  const saveEdit = (id) => {
    if (!editText.trim()) return;
    dispatch({ type: 'EDIT_TODO', payload: { id, text: editText.trim() } });
    setEditingId(null);
  };

  const remaining = todos.filter(t => !t.completed).length;

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <h2>Todo (useReducer版)</h2>

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

      <p style={{ color: '#666' }}>残り {remaining} 件</p>

      {/* タスクリスト */}
      {todos.map(todo => (
        <div key={todo.id} style={{
          display: 'flex', alignItems: 'center', gap: '8px',
          padding: '8px', borderBottom: '1px solid #eee',
        }}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => dispatch({ type: 'TOGGLE_TODO', payload: { id: todo.id } })}
          />

          {editingId === todo.id ? (
            <>
              <input
                value={editText}
                onChange={(e) => setEditText(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && saveEdit(todo.id)}
                style={{ flex: 1, padding: '4px' }}
              />
              <button onClick={() => saveEdit(todo.id)}>保存</button>
              <button onClick={() => setEditingId(null)}>取消</button>
            </>
          ) : (
            <>
              <span style={{
                flex: 1,
                textDecoration: todo.completed ? 'line-through' : 'none',
                color: todo.completed ? '#999' : '#333',
              }}>
                {todo.text}
              </span>
              <button onClick={() => startEdit(todo)}>編集</button>
              <button onClick={() => dispatch({ type: 'DELETE_TODO', payload: { id: todo.id } })}>
                削除
              </button>
            </>
          )}
        </div>
      ))}

      {todos.length > 0 && (
        <button
          onClick={() => dispatch({ type: 'CLEAR_ALL' })}
          style={{ marginTop: '16px', color: '#e74c3c' }}
        >
          全て削除
        </button>
      )}
    </div>
  );
}

export default TodoApp;
```

**ポイント：**
- useReducerを使うことで、Todoの状態更新ロジックが `todoReducer` に集約されます
- reducerは純粋関数なので、テストが容易です（入力と出力が明確）
- `editingId` や `input` のようなUIだけのstateは `useState` のままでOK。全てをreducerに入れる必要はありません

</details>

---

## 演習4（応用）：バグを見つけて修正しよう

以下のreducerにはバグが2つあります。見つけて修正してください。

```jsx
function cartReducer(state, action) {
  switch (action.type) {
    case 'ADD_ITEM':
      const existingItem = state.items.find(item => item.id === action.payload.id);
      if (existingItem) {
        existingItem.quantity += 1;  // バグ1
        return state;
      }
      return {
        ...state,
        items: [...state.items, { ...action.payload, quantity: 1 }],
      };

    case 'REMOVE_ITEM':
      return {
        items: state.items.filter(item => item.id !== action.payload.id),  // バグ2
      };

    default:
      return state;
  }
}

const initialState = { items: [], total: 0, itemCount: 0 };
```

<details>
<summary>ヒント</summary>

- **バグ1：** オブジェクトを直接変更（ミューテーション）している。Reactのstateはイミュータブルに更新する必要がある
- **バグ2：** スプレッド構文 `...state` がないため、`total` と `itemCount` のプロパティが失われる

</details>

<details>
<summary>解答例</summary>

```jsx
import { useReducer } from 'react';

function cartReducer(state, action) {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existingIndex = state.items.findIndex(
        item => item.id === action.payload.id
      );

      let newItems;
      if (existingIndex >= 0) {
        // ========================================
        // 修正1：イミュータブルな更新
        //
        // 修正前：existingItem.quantity += 1 （直接変更＝ミューテーション）
        // → Reactはstateの参照が変わらないと再レンダリングしない
        // → オブジェクトを直接書き換えると参照は変わらないので
        //   画面が更新されないバグが発生する
        //
        // 修正後：map で新しい配列を作り、該当アイテムだけ新しいオブジェクトにする
        // ========================================
        newItems = state.items.map((item, index) =>
          index === existingIndex
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      } else {
        newItems = [...state.items, { ...action.payload, quantity: 1 }];
      }

      // 合計金額とアイテム数を再計算
      const newTotal = newItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
      const newItemCount = newItems.reduce((sum, item) => sum + item.quantity, 0);

      return {
        ...state,
        items: newItems,
        total: newTotal,
        itemCount: newItemCount,
      };
    }

    case 'REMOVE_ITEM': {
      // ========================================
      // 修正2：...state のスプレッドで他のプロパティを保持
      //
      // 修正前：{ items: ... } だけ返していた
      // → total, itemCount などのプロパティが消失する
      //
      // 修正後：...state で全プロパティをコピーし、
      // items だけを上書き、totalとitemCountも再計算
      // ========================================
      const newItems = state.items.filter(
        item => item.id !== action.payload.id
      );
      const newTotal = newItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
      const newItemCount = newItems.reduce((sum, item) => sum + item.quantity, 0);

      return {
        ...state,           // 他のプロパティを保持
        items: newItems,
        total: newTotal,
        itemCount: newItemCount,
      };
    }

    default:
      return state;
  }
}

const initialState = { items: [], total: 0, itemCount: 0 };

function ShoppingCart() {
  const [state, dispatch] = useReducer(cartReducer, initialState);

  const products = [
    { id: 1, name: 'りんご', price: 200 },
    { id: 2, name: 'バナナ', price: 150 },
    { id: 3, name: 'みかん', price: 100 },
  ];

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <h2>商品</h2>
      {products.map(product => (
        <div key={product.id} style={{
          display: 'flex', justifyContent: 'space-between',
          padding: '8px', borderBottom: '1px solid #eee',
        }}>
          <span>{product.name} - ¥{product.price}</span>
          <button onClick={() => dispatch({ type: 'ADD_ITEM', payload: product })}>
            カートに追加
          </button>
        </div>
      ))}

      <h2 style={{ marginTop: '24px' }}>カート ({state.itemCount}点)</h2>
      {state.items.map(item => (
        <div key={item.id} style={{
          display: 'flex', justifyContent: 'space-between',
          padding: '8px', borderBottom: '1px solid #eee',
        }}>
          <span>{item.name} x{item.quantity}</span>
          <div>
            <span>¥{item.price * item.quantity}</span>
            <button
              onClick={() => dispatch({ type: 'REMOVE_ITEM', payload: { id: item.id } })}
              style={{ marginLeft: '8px' }}
            >
              削除
            </button>
          </div>
        </div>
      ))}
      <p style={{ fontWeight: 'bold', marginTop: '12px' }}>
        合計: ¥{state.total.toLocaleString()}
      </p>
    </div>
  );
}

export default ShoppingCart;
```

**2つのバグのまとめ：**
1. **stateの直接変更（ミューテーション）** → `map` で新しい配列・オブジェクトを作ってイミュータブルに更新
2. **スプレッド構文の忘れ** → `...state` で既存のプロパティを保持してからitems等を上書き

</details>

---

## 演習5（応用）：useReducer + useContextを組み合わせよう

ショッピングカートの状態を `useReducer` で管理し、`useContext` でアプリ全体に提供してください。

**要件：**
- `CartProvider` でカートの状態と操作関数を提供
- ヘッダーにカート内のアイテム数を表示
- 商品一覧ページでカートに追加
- カートページでアイテムの数量変更と削除

<details>
<summary>ヒント</summary>

`useReducer` で状態を管理し、`dispatch` 関数をContextで共有します。

```jsx
function CartProvider({ children }) {
  const [state, dispatch] = useReducer(cartReducer, initialState);
  return (
    <CartContext.Provider value={{ state, dispatch }}>
      {children}
    </CartContext.Provider>
  );
}
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { createContext, useContext, useReducer } from 'react';

// ========================================
// reducer：カートの全状態更新を管理
// ========================================
function cartReducer(state, action) {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existingIndex = state.items.findIndex(i => i.id === action.payload.id);
      let newItems;
      if (existingIndex >= 0) {
        newItems = state.items.map((item, idx) =>
          idx === existingIndex ? { ...item, quantity: item.quantity + 1 } : item
        );
      } else {
        newItems = [...state.items, { ...action.payload, quantity: 1 }];
      }
      return { ...state, items: newItems };
    }

    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(i => i.id !== action.payload.id),
      };

    case 'UPDATE_QUANTITY':
      return {
        ...state,
        items: state.items.map(item =>
          item.id === action.payload.id
            ? { ...item, quantity: Math.max(1, action.payload.quantity) }
            : item
        ),
      };

    case 'CLEAR_CART':
      return { ...state, items: [] };

    default:
      return state;
  }
}

// ========================================
// Context + Provider
// useReducer と useContext を組み合わせることで、
// 複雑な状態管理をアプリ全体で共有できる
// ========================================
const CartContext = createContext(null);

function CartProvider({ children }) {
  const [state, dispatch] = useReducer(cartReducer, { items: [] });

  // 派生値の計算（stateから導出できる値）
  const totalItems = state.items.reduce((sum, item) => sum + item.quantity, 0);
  const totalPrice = state.items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <CartContext.Provider value={{ state, dispatch, totalItems, totalPrice }}>
      {children}
    </CartContext.Provider>
  );
}

function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error('useCart は CartProvider の中で使ってください');
  return ctx;
}

// ========================================
// ヘッダー：カート内のアイテム数を表示
// ========================================
function Header() {
  const { totalItems } = useCart();

  return (
    <header style={{
      padding: '12px 24px', backgroundColor: '#2c3e50', color: '#fff',
      display: 'flex', justifyContent: 'space-between',
    }}>
      <h1 style={{ margin: 0, fontSize: '20px' }}>ショップ</h1>
      <span style={{
        backgroundColor: totalItems > 0 ? '#e74c3c' : '#555',
        padding: '4px 12px', borderRadius: '12px',
      }}>
        カート: {totalItems}点
      </span>
    </header>
  );
}

// ========================================
// 商品一覧
// ========================================
function ProductList() {
  const { dispatch } = useCart();

  const products = [
    { id: 1, name: 'React入門書', price: 2800 },
    { id: 2, name: 'TypeScript実践ガイド', price: 3200 },
    { id: 3, name: 'Next.js ハンドブック', price: 3500 },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h2>商品一覧</h2>
      {products.map(product => (
        <div key={product.id} style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          padding: '12px', borderBottom: '1px solid #eee',
        }}>
          <div>
            <strong>{product.name}</strong>
            <span style={{ marginLeft: '12px' }}>¥{product.price.toLocaleString()}</span>
          </div>
          <button onClick={() => dispatch({ type: 'ADD_ITEM', payload: product })}>
            カートに追加
          </button>
        </div>
      ))}
    </div>
  );
}

// ========================================
// カートの中身
// ========================================
function CartView() {
  const { state, dispatch, totalPrice } = useCart();

  if (state.items.length === 0) {
    return <p style={{ padding: '20px', color: '#999' }}>カートは空です</p>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <h2>カートの中身</h2>
      {state.items.map(item => (
        <div key={item.id} style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          padding: '12px', borderBottom: '1px solid #eee',
        }}>
          <span>{item.name}</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <button onClick={() => dispatch({
              type: 'UPDATE_QUANTITY',
              payload: { id: item.id, quantity: item.quantity - 1 },
            })}>-</button>
            <span>{item.quantity}</span>
            <button onClick={() => dispatch({
              type: 'UPDATE_QUANTITY',
              payload: { id: item.id, quantity: item.quantity + 1 },
            })}>+</button>
            <span>¥{(item.price * item.quantity).toLocaleString()}</span>
            <button onClick={() => dispatch({ type: 'REMOVE_ITEM', payload: { id: item.id } })}>
              削除
            </button>
          </div>
        </div>
      ))}
      <p style={{ fontWeight: 'bold', fontSize: '18px', marginTop: '12px' }}>
        合計: ¥{totalPrice.toLocaleString()}
      </p>
      <button onClick={() => dispatch({ type: 'CLEAR_CART' })}>カートを空にする</button>
    </div>
  );
}

function App() {
  return (
    <CartProvider>
      <Header />
      <ProductList />
      <CartView />
    </CartProvider>
  );
}

export default App;
```

**ポイント：**
- `useReducer + useContext` はReduxに似た状態管理パターンです
- 小〜中規模のアプリケーションではこのパターンで十分な場合が多い
- `dispatch` を共有することで、どのコンポーネントからでもアクションを送信できます
- `totalItems` や `totalPrice` は派生値としてProviderで計算し、各コンポーネントでの重複計算を避けています

</details>

---

## 演習6（チャレンジ）：useReducerとuseStateの使い分けを判断しよう

以下のシナリオで、`useState` と `useReducer` のどちらが適切か判断し、理由を説明してください。

**シナリオA：** モーダルの開閉状態（true/false）

**シナリオB：** ECサイトの注文フロー（カート → 配送先入力 → 支払い → 確認 → 完了）

**シナリオC：** テキスト入力フィールドの値管理

**シナリオD：** Undo/Redo機能を持つお絵描きアプリの状態管理

<details>
<summary>解答例</summary>

### シナリオA：モーダルの開閉 → **useState が適切**

```
理由：
- 状態が単純な true/false のみ
- 更新ロジックが単純（反転するだけ）
- useReducerを使うとオーバーエンジニアリング

推奨：const [isOpen, setIsOpen] = useState(false);
```

### シナリオB：注文フロー → **useReducer が適切**

```
理由：
- 複数のステップ（状態遷移）がある
- 各ステップに固有のデータがある（配送先、支払い情報など）
- 「前のステップに戻る」「ステップをスキップ」などの
  複雑な遷移ロジックがある
- 不正な遷移（支払い前に完了へ進む）を防ぐ必要がある

推奨：
const orderReducer = (state, action) => {
  switch (action.type) {
    case 'NEXT_STEP': // 次のステップへ
    case 'PREV_STEP': // 前のステップへ
    case 'SET_SHIPPING': // 配送先設定
    case 'SET_PAYMENT': // 支払い方法設定
    case 'COMPLETE': // 注文完了
  }
};
```

### シナリオC：テキスト入力の値管理 → **useState が適切**

```
理由：
- 単一の値を管理するだけ
- 更新ロジックが単純（入力された値をそのままセット）
- useReducerは過剰

推奨：const [text, setText] = useState('');
```

### シナリオD：Undo/Redo付きお絵描き → **useReducer が適切**

```
理由：
- 過去の状態（履歴）を管理する必要がある
- 複数のアクション（描画、消去、色変更、Undo、Redo）
- 状態の構造が複雑：{ past: [], present: {}, future: [] }
- 各アクションの状態更新ロジックが複雑

推奨：
const drawReducer = (state, action) => {
  switch (action.type) {
    case 'DRAW':  // 描画 → presentをpastに保存、新しい描画をpresentに
    case 'UNDO':  // 元に戻す → presentをfutureに、pastの最後をpresentに
    case 'REDO':  // やり直し → presentをpastに、futureの最初をpresentに
    case 'CLEAR': // クリア
  }
};
```

### 使い分けの判断基準

| 基準 | useState | useReducer |
|------|----------|------------|
| 状態の型 | プリミティブ値（文字列、数値、真偽値） | オブジェクト、配列 |
| 更新パターン | 単純な値の上書き | 複数のアクションパターン |
| 状態の相互依存 | 独立した値 | 密接に関連する複数の値 |
| 更新ロジック | シンプル | 複雑（条件分岐、バリデーション） |
| テスタビリティ | - | reducer関数を単体テスト可能 |

</details>
