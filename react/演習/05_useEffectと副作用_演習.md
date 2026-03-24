# 第5章 演習：useEffectと副作用

---

## 演習1（基本）：ドキュメントタイトルを動的に変更しよう

カウンターコンポーネントを作成し、カウントが変わるたびにブラウザのタブタイトル（`document.title`）を更新してください。

**要件：**
- `count` stateを持つ
- +1 / -1 ボタンでカウントを増減
- `useEffect` でカウントが変わるたびに `document.title` を `カウント: {count}` に更新

<details>
<summary>ヒント</summary>

`useEffect` の依存配列に `count` を指定すると、`count` が変化したときだけ副作用が実行されます。

```jsx
useEffect(() => {
  document.title = `カウント: ${count}`;
}, [count]);
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState, useEffect } from 'react';

function TitleCounter() {
  const [count, setCount] = useState(0);

  // ========================================
  // useEffect：countが変化するたびにタブタイトルを更新する
  // 依存配列に[count]を指定しているので、countの値が変わった
  // ときだけこの副作用が実行される
  // ========================================
  useEffect(() => {
    document.title = `カウント: ${count}`;
  }, [count]);

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h2>カウント: {count}</h2>
      <button onClick={() => setCount(count - 1)}>-1</button>
      <button onClick={() => setCount(count + 1)} style={{ marginLeft: '8px' }}>+1</button>
      <p style={{ color: '#888', marginTop: '12px' }}>
        ブラウザのタブタイトルを確認してみてください
      </p>
    </div>
  );
}

export default TitleCounter;
```

**ポイント：**
- `document.title` の変更はDOMへの直接操作であり、典型的な「副作用」です
- 依存配列 `[count]` により、count以外のstateが変化してもこのeffectは再実行されません

</details>

---

## 演習2（基本）：マウント時にデータを取得しよう

コンポーネントがマウントされたタイミングで、以下の疑似APIからユーザー一覧を取得して表示してください。

**疑似API関数（そのまま使ってください）：**
```javascript
const fetchUsers = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { id: 1, name: "田中太郎", email: "tanaka@example.com" },
        { id: 2, name: "鈴木花子", email: "suzuki@example.com" },
        { id: 3, name: "佐藤次郎", email: "sato@example.com" },
      ]);
    }, 1000);
  });
};
```

**要件：**
- ローディング中は「読み込み中...」と表示
- 取得完了後にユーザー一覧を表示
- useEffectの依存配列は空配列 `[]`

<details>
<summary>ヒント</summary>

マウント時に一度だけ実行するには、依存配列を空 `[]` にします。非同期処理は `useEffect` の中で即時関数を使うと書きやすくなります。

```jsx
useEffect(() => {
  const loadData = async () => {
    const data = await fetchUsers();
    setUsers(data);
  };
  loadData();
}, []);
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState, useEffect } from 'react';

// 疑似API：1秒後にユーザーデータを返す
const fetchUsers = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { id: 1, name: "田中太郎", email: "tanaka@example.com" },
        { id: 2, name: "鈴木花子", email: "suzuki@example.com" },
        { id: 3, name: "佐藤次郎", email: "sato@example.com" },
      ]);
    }, 1000);
  });
};

function UserList() {
  // ========================================
  // state定義：ユーザーデータとローディング状態の2つを管理
  // ========================================
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  // ========================================
  // useEffect（マウント時のみ実行）：空配列[]を指定
  // コンポーネントが画面に表示されたとき、1回だけデータを取得する
  // ========================================
  useEffect(() => {
    const loadUsers = async () => {
      const data = await fetchUsers();
      setUsers(data);       // 取得したデータをstateにセット
      setLoading(false);    // ローディング完了
    };
    loadUsers();
  }, []);  // ← 空配列：マウント時に1回だけ実行

  // ========================================
  // ローディング中の表示
  // ========================================
  if (loading) {
    return <p style={{ textAlign: 'center', padding: '20px' }}>読み込み中...</p>;
  }

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <h2>ユーザー一覧</h2>
      {users.map(user => (
        <div key={user.id} style={{
          padding: '12px',
          borderBottom: '1px solid #eee',
        }}>
          <strong>{user.name}</strong>
          <span style={{ color: '#888', marginLeft: '8px' }}>{user.email}</span>
        </div>
      ))}
    </div>
  );
}

export default UserList;
```

**ポイント：**
- `useEffect` に直接 `async` 関数を渡すことはできません（戻り値がPromiseになるため）
- 代わりに内部で `async` 関数を定義して呼び出します
- 空配列 `[]` を忘れると、毎回のレンダリングでAPIが呼ばれてしまいます

</details>

---

## 演習3（基本）：クリーンアップ関数を理解しよう

1秒ごとにカウントアップするストップウォッチを作成してください。コンポーネントがアンマウントされたときにタイマーを適切にクリーンアップしてください。

**要件：**
- `isRunning` stateで開始/停止を切り替え
- 1秒ごとに `seconds` をカウントアップ
- 停止ボタンとリセットボタン
- `setInterval` のクリーンアップを適切に行う

<details>
<summary>ヒント</summary>

`useEffect` の戻り値として関数を返すと、それが**クリーンアップ関数**になります。依存配列の値が変化したとき、または コンポーネントがアンマウントされたときに呼ばれます。

```jsx
useEffect(() => {
  const id = setInterval(() => { /* 処理 */ }, 1000);
  return () => clearInterval(id);  // クリーンアップ
}, [isRunning]);
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState, useEffect } from 'react';

function Stopwatch() {
  const [seconds, setSeconds] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  // ========================================
  // useEffect：isRunningが変化するたびにタイマーを制御
  // isRunning が true の間だけ setInterval を動かし、
  // false になったら（またはアンマウント時に）clearInterval する
  // ========================================
  useEffect(() => {
    if (!isRunning) return; // 停止中なら何もしない

    const intervalId = setInterval(() => {
      setSeconds(prev => prev + 1);  // 関数型更新で最新値を使う
    }, 1000);

    // ========================================
    // クリーンアップ関数：
    // isRunning が変化したとき、またはコンポーネントが
    // アンマウントされたときに実行される
    // タイマーを解除してメモリリークを防ぐ
    // ========================================
    return () => {
      clearInterval(intervalId);
    };
  }, [isRunning]);

  const handleReset = () => {
    setIsRunning(false);
    setSeconds(0);
  };

  // 秒数を「分:秒」形式にフォーマット
  const formatTime = (totalSeconds) => {
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h2 style={{ fontSize: '48px', fontFamily: 'monospace' }}>
        {formatTime(seconds)}
      </h2>
      <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
        <button onClick={() => setIsRunning(!isRunning)}>
          {isRunning ? '停止' : '開始'}
        </button>
        <button onClick={handleReset}>リセット</button>
      </div>
    </div>
  );
}

export default Stopwatch;
```

**ポイント：**
- クリーンアップ関数がないと、コンポーネントが画面から消えてもタイマーが動き続け、**メモリリーク**が発生します
- `setSeconds(prev => prev + 1)` のように**関数型更新**を使うことで、常に最新のstateを参照できます
- `setSeconds(seconds + 1)` だと、クロージャにより古い値を参照してしまう問題が起きます

</details>

---

## 演習4（応用）：バグを見つけて修正しよう

以下のコードにはuseEffectに関するバグがあります。3つのバグを見つけて修正してください。

```jsx
import { useState, useEffect } from 'react';

function BuggySearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  // バグ1：依存配列の問題
  useEffect(() => {
    if (query === "") {
      setResults([]);
      return;
    }

    setLoading(true);

    // バグ2：非同期処理の問題
    const fetchResults = async () => {
      const response = await fakeFetch(query);
      setResults(response);
      setLoading(false);
    };
    fetchResults();
  });

  // バグ3：クリーンアップの問題
  useEffect(() => {
    const handleResize = () => {
      console.log("ウィンドウサイズ:", window.innerWidth);
    };
    window.addEventListener('resize', handleResize);
  }, []);

  return (
    <div>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      {loading && <p>検索中...</p>}
      <ul>
        {results.map((r, i) => <li key={i}>{r}</li>)}
      </ul>
    </div>
  );
}
```

<details>
<summary>ヒント</summary>

- **バグ1：** useEffectの依存配列が指定されていない → 毎回のレンダリングで実行されてしまう
- **バグ2：** 入力が高速に変わると、古いリクエストの結果が後から到着して上書きする可能性がある（競合状態）
- **バグ3：** `addEventListener` に対応する `removeEventListener` が呼ばれていない

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState, useEffect } from 'react';

function FixedSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  // ========================================
  // 修正1：依存配列に[query]を追加
  // これにより、queryが変わったときだけ検索が実行される
  // （修正前は依存配列がなく、毎回のレンダリングで実行されていた）
  // ========================================
  useEffect(() => {
    if (query === "") {
      setResults([]);
      return;
    }

    // ========================================
    // 修正2：競合状態（race condition）を防ぐフラグ
    // 検索中に新しい入力があった場合、古い結果を無視するために
    // ignore フラグを使う。クリーンアップでフラグを立てることで、
    // 古いリクエストの結果がstateを上書きしないようにする
    // ========================================
    let ignore = false;

    setLoading(true);
    const fetchResults = async () => {
      const response = await fakeFetch(query);
      if (!ignore) {       // ignoreがfalseの場合のみstateを更新
        setResults(response);
        setLoading(false);
      }
    };
    fetchResults();

    return () => {
      ignore = true;       // 新しいeffectが始まったら古い結果を無視
    };
  }, [query]);  // ← queryが変わったときだけ実行

  // ========================================
  // 修正3：イベントリスナーのクリーンアップを追加
  // addEventListenerには必ず対になるremoveEventListenerが必要
  // これがないとリスナーが蓄積し、メモリリークが発生する
  // ========================================
  useEffect(() => {
    const handleResize = () => {
      console.log("ウィンドウサイズ:", window.innerWidth);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <div>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      {loading && <p>検索中...</p>}
      <ul>
        {results.map((r, i) => <li key={i}>{r}</li>)}
      </ul>
    </div>
  );
}

export default FixedSearch;
```

**3つのバグと修正の要約：**
1. **依存配列が未指定** → `[query]` を追加して必要なときだけ実行
2. **競合状態（race condition）** → `ignore` フラグでキャンセル処理を実装
3. **イベントリスナーの片付け忘れ** → クリーンアップ関数で `removeEventListener`

</details>

---

## 演習5（応用）：デバウンス検索を実装しよう

テキスト入力に連動した検索機能を作成してください。ただし、入力のたびにすぐ検索するのではなく、ユーザーが入力を止めて500ミリ秒経ってから検索を実行する「デバウンス」を実装してください。

**要件：**
- テキスト入力フィールド
- 入力停止後500ms でフェイクAPIに検索リクエスト
- ローディング表示
- 検索結果の表示

**疑似API関数：**
```javascript
const fakeSearch = (query) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const allItems = ["React", "Redux", "Router", "Remix", "Relay", "RSC", "Recoil"];
      resolve(allItems.filter(item => item.toLowerCase().includes(query.toLowerCase())));
    }, 500);
  });
};
```

<details>
<summary>ヒント</summary>

デバウンスは `setTimeout` と `clearTimeout` の組み合わせで実現します。useEffectのクリーンアップ関数で前回のタイマーをキャンセルすることがポイントです。

```jsx
useEffect(() => {
  const timerId = setTimeout(() => {
    // ここで検索実行
  }, 500);

  return () => clearTimeout(timerId);  // 入力のたびに前回のタイマーをクリア
}, [query]);
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState, useEffect } from 'react';

// 疑似API：入力にマッチする項目を返す
const fakeSearch = (query) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const allItems = ["React", "Redux", "Router", "Remix", "Relay", "RSC", "Recoil"];
      resolve(allItems.filter(item =>
        item.toLowerCase().includes(query.toLowerCase())
      ));
    }, 500);
  });
};

function DebouncedSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  // ========================================
  // デバウンス検索のuseEffect
  //
  // 仕組み：
  // 1. queryが変わるたびにuseEffectが発火する
  // 2. 500ms後に検索を実行するsetTimeoutをセットする
  // 3. 500ms以内にqueryが再度変わると、クリーンアップ関数が
  //    前回のsetTimeoutをキャンセルする
  // 4. 結果として、ユーザーが入力を止めて500ms経過して
  //    初めて検索が実行される
  // ========================================
  useEffect(() => {
    // 空文字のときは検索しない
    if (query.trim() === "") {
      setResults([]);
      setLoading(false);
      return;
    }

    setLoading(true);

    // 500ms後に検索を実行するタイマーをセット
    const timerId = setTimeout(async () => {
      const data = await fakeSearch(query);
      setResults(data);
      setLoading(false);
    }, 500);

    // ========================================
    // クリーンアップ：前回のタイマーをキャンセル
    // queryが変わるたびにこの関数が呼ばれ、
    // まだ実行されていないsetTimeoutをクリアする
    // ========================================
    return () => {
      clearTimeout(timerId);
    };
  }, [query]);

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <h2>デバウンス検索</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Reactライブラリを検索..."
        style={{ width: '100%', padding: '10px', fontSize: '16px' }}
      />

      {loading && <p style={{ color: '#888' }}>検索中...</p>}

      {!loading && query && results.length === 0 && (
        <p style={{ color: '#999' }}>該当する結果がありません</p>
      )}

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {results.map((item, index) => (
          <li key={index} style={{
            padding: '10px',
            borderBottom: '1px solid #eee',
          }}>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default DebouncedSearch;
```

**ポイント：**
- デバウンスは「不要なAPIリクエストを減らす」ための重要なテクニックです
- 1文字入力するたびにAPIを叩くと、サーバーへの負荷が大きくなります
- useEffectのクリーンアップ関数は、依存配列の値が変化した「次のeffectが実行される前」に呼ばれます
- 実務では `lodash.debounce` や `use-debounce` ライブラリもよく使われます

</details>

---

## 演習6（応用）：ローカルストレージと同期しよう

メモアプリを作成し、入力内容をローカルストレージに保存してください。ページをリロードしてもメモの内容が復元されるようにしましょう。

**要件：**
- `textarea` でメモを入力
- メモが変わるたびに `localStorage` に保存
- コンポーネントのマウント時に `localStorage` から復元
- 「クリア」ボタンでメモとlocalStorageをクリア
- 最終保存日時を表示

<details>
<summary>ヒント</summary>

- `useState` の初期値に関数を渡すと、初回レンダリング時のみ実行されます（遅延初期化）
- `JSON.stringify` / `JSON.parse` で localStorage に保存・読み込みをします

```jsx
const [memo, setMemo] = useState(() => {
  return localStorage.getItem('memo') || "";
});
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState, useEffect } from 'react';

function MemoApp() {
  // ========================================
  // stateの遅延初期化：
  // useState に関数を渡すと、初回レンダリング時にのみ実行される
  // ページリロード時に localStorage から前回のメモを復元する
  // ========================================
  const [memo, setMemo] = useState(() => {
    const saved = localStorage.getItem('memo');
    return saved || "";
  });

  const [lastSaved, setLastSaved] = useState(() => {
    return localStorage.getItem('memo-timestamp') || null;
  });

  // ========================================
  // useEffect：memoが変わるたびにlocalStorageに保存
  // ブラウザのローカルストレージに保存することで、
  // ページをリロードしてもデータが残る
  // ========================================
  useEffect(() => {
    localStorage.setItem('memo', memo);
    const now = new Date().toLocaleString('ja-JP');
    localStorage.setItem('memo-timestamp', now);
    setLastSaved(now);
  }, [memo]);

  const handleClear = () => {
    setMemo("");
    localStorage.removeItem('memo');
    localStorage.removeItem('memo-timestamp');
    setLastSaved(null);
  };

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <h2>メモアプリ</h2>
      <textarea
        value={memo}
        onChange={(e) => setMemo(e.target.value)}
        placeholder="ここにメモを入力..."
        style={{
          width: '100%',
          height: '200px',
          padding: '12px',
          fontSize: '16px',
          resize: 'vertical',
        }}
      />
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginTop: '8px',
      }}>
        <span style={{ color: '#888', fontSize: '14px' }}>
          {lastSaved ? `最終保存: ${lastSaved}` : "未保存"}
        </span>
        <button onClick={handleClear}>クリア</button>
      </div>
      <p style={{ color: '#666', fontSize: '14px', marginTop: '12px' }}>
        文字数: {memo.length}
      </p>
    </div>
  );
}

export default MemoApp;
```

**ポイント：**
- `useState(() => ...)` の遅延初期化は、localStorage の読み込みなど「コストの高い初期値」に最適です
- 通常の `useState(localStorage.getItem('memo'))` でも動きますが、毎回のレンダリングで `localStorage.getItem` が呼ばれます
- 遅延初期化なら初回のみ実行されるため効率的です

</details>

---

## 演習7（チャレンジ）：設計を考えよう ― useEffectが不要なケースを見抜く

以下のコードはuseEffectを使っていますが、実はuseEffectなしで書けます。なぜuseEffectが不要なのか説明し、リファクタリングしてください。

```jsx
function ProductPage({ productId, products }) {
  const [product, setProduct] = useState(null);

  useEffect(() => {
    const found = products.find(p => p.id === productId);
    setProduct(found);
  }, [productId, products]);

  if (!product) return <p>商品が見つかりません</p>;

  return (
    <div>
      <h2>{product.name}</h2>
      <p>価格: ¥{product.price.toLocaleString()}</p>
    </div>
  );
}
```

<details>
<summary>ヒント</summary>

propsやstateから**計算できる値**は、stateにせずレンダリング中に直接計算すべきです。useEffectで「propsをstateに同期する」パターンは、多くの場合アンチパターンです。

</details>

<details>
<summary>解答例</summary>

```jsx
function ProductPage({ productId, products }) {
  // ========================================
  // リファクタリング後：useEffect + state が不要
  //
  // なぜ不要なのか：
  // - product は productId と products から計算できる「派生値」
  // - 派生値はstateに保持する必要がない
  // - レンダリング中に直接計算すればよい
  //
  // useEffectで「propsをstateに同期する」パターンは
  // React公式ドキュメントでもアンチパターンとして紹介されている
  //
  // 問題点：
  // 1. 無駄なレンダリングが1回多くなる
  //    (初回: product=null → effect実行 → setProduct → 再レンダリング)
  // 2. コードが複雑になる
  // 3. stateとpropsの同期が崩れるバグのリスク
  // ========================================
  const product = products.find(p => p.id === productId);

  if (!product) return <p>商品が見つかりません</p>;

  return (
    <div>
      <h2>{product.name}</h2>
      <p>価格: ¥{product.price.toLocaleString()}</p>
    </div>
  );
}

export default ProductPage;
```

**重要な原則：「useEffectが必要ないかもしれない」**

以下のケースではuseEffectは不要です：
1. **propsやstateから計算できる値** → レンダリング中に直接計算する
2. **propsが変わったらstateをリセットしたい** → `key` propを使う
3. **イベントに応じた処理** → イベントハンドラ内で直接処理する

useEffectが本当に必要なのは「外部システムとの同期」（API呼び出し、DOM操作、タイマー、イベントリスナーなど）のみです。

</details>

---

## 演習8（チャレンジ）：ウィンドウサイズ監視コンポーネントを作ろう

ブラウザのウィンドウサイズをリアルタイムに表示するコンポーネントを作成してください。さらに、画面サイズに応じて「モバイル」「タブレット」「デスクトップ」のラベルを表示してください。

**要件：**
- `window.innerWidth` / `window.innerHeight` を取得
- `resize` イベントを監視して更新
- クリーンアップで `removeEventListener` を実行
- 幅768px未満:「モバイル」、768-1024px:「タブレット」、1024px以上:「デスクトップ」
- パフォーマンスのため、resizeイベントをデバウンスする（任意）

<details>
<summary>ヒント</summary>

- `window.addEventListener('resize', handler)` でウィンドウサイズの変更を検知できます
- デバウンスを入れないとresizeのたびに大量のレンダリングが発生します

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState, useEffect } from 'react';

function WindowSizeMonitor() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    // ========================================
    // デバウンス付きresizeハンドラ
    // リサイズイベントは1秒間に数十回発火するため、
    // タイマーを使って最後のリサイズから200ms後に
    // 1回だけstateを更新する
    // ========================================
    let timeoutId;

    const handleResize = () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        setWindowSize({
          width: window.innerWidth,
          height: window.innerHeight,
        });
      }, 200);
    };

    window.addEventListener('resize', handleResize);

    // ========================================
    // クリーンアップ：
    // コンポーネントがアンマウントされたとき、
    // イベントリスナーとタイマーの両方を解除する
    // これを忘れるとメモリリークが発生する
    // ========================================
    return () => {
      window.removeEventListener('resize', handleResize);
      clearTimeout(timeoutId);
    };
  }, []);

  // ========================================
  // 画面サイズからデバイスの種類を判定する（派生値）
  // これはstateではなくレンダリング中に計算すればよい
  // ========================================
  const getDeviceType = (width) => {
    if (width < 768) return { label: "モバイル", color: "#e74c3c" };
    if (width < 1024) return { label: "タブレット", color: "#f39c12" };
    return { label: "デスクトップ", color: "#27ae60" };
  };

  const device = getDeviceType(windowSize.width);

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h2>ウィンドウサイズモニター</h2>
      <div style={{ fontSize: '24px', fontFamily: 'monospace', margin: '16px 0' }}>
        {windowSize.width} x {windowSize.height}
      </div>
      <span style={{
        backgroundColor: device.color,
        color: 'white',
        padding: '6px 16px',
        borderRadius: '20px',
        fontSize: '18px',
      }}>
        {device.label}
      </span>
      <p style={{ color: '#888', marginTop: '16px' }}>
        ウィンドウサイズを変更してみてください
      </p>
    </div>
  );
}

export default WindowSizeMonitor;
```

**ポイント：**
- `resize` イベントは非常に頻繁に発火するため、デバウンスがパフォーマンス上重要です
- `getDeviceType` の結果は `width` から計算可能な派生値なので、stateにする必要はありません
- クリーンアップでは `removeEventListener` と `clearTimeout` の両方を忘れずに行います
- このロジックは第6章で学ぶカスタムフック（`useWindowSize`）に切り出すのが理想的です

</details>
