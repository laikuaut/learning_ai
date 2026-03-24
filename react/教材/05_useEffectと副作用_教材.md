# 第5章：useEffectと副作用

## この章で学ぶこと

- 副作用（side effect）とは何か
- useEffectの基本的な使い方
- 依存配列の仕組み
- クリーンアップ関数
- APIからデータを取得する方法
- よくある使用パターン

---

## 1. 副作用（Side Effect）とは？

Reactコンポーネントの主な仕事は「UIを描画すること」です。それ以外の処理を**副作用**と呼びます。

### 副作用の例

| 副作用 | 具体例 |
|--------|--------|
| データの取得 | APIからユーザー情報を取得する |
| DOM操作 | ページタイトルを変更する |
| タイマー | setInterval / setTimeout |
| イベント登録 | window.addEventListener |
| ローカルストレージ | localStorage.setItem |
| ログ出力 | console.log（デバッグ用） |

これらの処理は、レンダリング中に直接実行すると問題が起きます。そこで**useEffect**を使います。

---

## 2. useEffectの基本

### 基本構文

```jsx
import { useEffect } from 'react';

useEffect(() => {
  // ここに副作用の処理を書く
}, [依存配列]);
```

### 3つのパターン

#### パターン1：毎回実行（依存配列なし）

```jsx
useEffect(() => {
  console.log("レンダリングのたびに実行される");
});
```

#### パターン2：マウント時のみ実行（空の依存配列）

```jsx
useEffect(() => {
  console.log("コンポーネントが表示された時に1回だけ実行");
}, []);
```

#### パターン3：特定の値が変わった時に実行

```jsx
useEffect(() => {
  console.log(`countが${count}に変わった`);
}, [count]);
```

### まとめ表

| 依存配列 | 実行タイミング |
|----------|---------------|
| 指定なし | 毎回のレンダリング後 |
| `[]`（空配列） | 初回レンダリング後のみ |
| `[a, b]` | `a`または`b`が変わった時 |

---

## 3. 具体的な使用例

### ページタイトルの変更

```jsx
import { useState, useEffect } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `カウント: ${count}`;
  }, [count]);

  return (
    <div>
      <p>カウント: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
}
```

### ローカルストレージとの連携

```jsx
import { useState, useEffect } from 'react';

function PersistentNote() {
  // ローカルストレージから初期値を読み込む
  const [note, setNote] = useState(() => {
    return localStorage.getItem('my-note') || "";
  });

  // noteが変わるたびにローカルストレージに保存
  useEffect(() => {
    localStorage.setItem('my-note', note);
  }, [note]);

  return (
    <div>
      <h2>メモ帳（自動保存）</h2>
      <textarea
        value={note}
        onChange={(e) => setNote(e.target.value)}
        rows={10}
        cols={50}
        placeholder="ここにメモを書くと自動保存されます..."
      />
      <p>{note.length}文字</p>
    </div>
  );
}
```

> **ポイント**：`useState(() => ...)` のように関数を渡すと、初回レンダリング時にだけその関数が実行されます（遅延初期化）。

---

## 4. クリーンアップ関数

useEffectの中で返す関数は**クリーンアップ関数**と呼ばれ、コンポーネントがアンマウント（画面から消える）時や、次のエフェクト実行前に呼ばれます。

### 基本構文

```jsx
useEffect(() => {
  // セットアップ処理

  return () => {
    // クリーンアップ処理
  };
}, [依存配列]);
```

### タイマーのクリーンアップ

```jsx
import { useState, useEffect } from 'react';

function Timer() {
  const [seconds, setSeconds] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    if (!isRunning) return;

    const intervalId = setInterval(() => {
      setSeconds(prev => prev + 1);
    }, 1000);

    // クリーンアップ：タイマーを停止
    return () => {
      clearInterval(intervalId);
    };
  }, [isRunning]);

  const reset = () => {
    setIsRunning(false);
    setSeconds(0);
  };

  return (
    <div>
      <h2>{seconds}秒</h2>
      <button onClick={() => setIsRunning(!isRunning)}>
        {isRunning ? "停止" : "開始"}
      </button>
      <button onClick={reset}>リセット</button>
    </div>
  );
}
```

### イベントリスナーのクリーンアップ

```jsx
import { useState, useEffect } from 'react';

function WindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);

    // クリーンアップ：イベントリスナーを削除
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // 空配列：マウント時に1回だけ登録

  return (
    <p>
      ウィンドウサイズ：{size.width} x {size.height}
    </p>
  );
}
```

### クリーンアップが必要な場合

| 処理 | クリーンアップ |
|------|---------------|
| `setInterval` | `clearInterval` |
| `setTimeout` | `clearTimeout` |
| `addEventListener` | `removeEventListener` |
| WebSocket接続 | `socket.close()` |
| AbortController（API中断） | `controller.abort()` |

---

## 5. APIからデータを取得する

### 基本的なfetch

```jsx
import { useState, useEffect } from 'react';

function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('https://jsonplaceholder.typicode.com/users')
      .then(response => {
        if (!response.ok) {
          throw new Error('データの取得に失敗しました');
        }
        return response.json();
      })
      .then(data => {
        setUsers(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []); // 空配列：マウント時に1回だけ実行

  if (loading) return <p>読み込み中...</p>;
  if (error) return <p style={{ color: 'red' }}>エラー：{error}</p>;

  return (
    <div>
      <h2>ユーザー一覧（{users.length}人）</h2>
      {users.map(user => (
        <div key={user.id} style={{
          padding: '8px',
          margin: '4px 0',
          borderBottom: '1px solid #eee',
        }}>
          <strong>{user.name}</strong>
          <span style={{ color: '#666', marginLeft: '8px' }}>{user.email}</span>
        </div>
      ))}
    </div>
  );
}
```

### async/awaitを使う方法

useEffectのコールバック関数自体をasyncにすることはできません。内部でasync関数を定義して呼び出します。

```jsx
useEffect(() => {
  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await fetch('https://jsonplaceholder.typicode.com/posts');
      if (!response.ok) throw new Error('取得失敗');
      const data = await response.json();
      setUsers(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  fetchData();
}, []);
```

> **注意**：`useEffect(async () => {...})` とは書けません。useEffectはクリーンアップ関数（またはundefined）を返す必要がありますが、async関数はPromiseを返すためです。

### 検索キーワードに応じてAPIを呼ぶ

```jsx
import { useState, useEffect } from 'react';

function SearchPosts() {
  const [query, setQuery] = useState("");
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (query.trim() === "") {
      setPosts([]);
      return;
    }

    setLoading(true);

    // AbortControllerでリクエストをキャンセル可能にする
    const controller = new AbortController();

    fetch(`https://jsonplaceholder.typicode.com/posts?title_like=${query}`, {
      signal: controller.signal,
    })
      .then(res => res.json())
      .then(data => {
        setPosts(data);
        setLoading(false);
      })
      .catch(err => {
        if (err.name !== 'AbortError') {
          setLoading(false);
        }
      });

    // クリーンアップ：前のリクエストをキャンセル
    return () => {
      controller.abort();
    };
  }, [query]); // queryが変わるたびに実行

  return (
    <div>
      <h2>投稿を検索</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="検索キーワード..."
        style={{ padding: '8px', width: '100%', marginBottom: '16px' }}
      />

      {loading && <p>検索中...</p>}

      {!loading && posts.length === 0 && query && (
        <p>結果が見つかりません。</p>
      )}

      {posts.slice(0, 10).map(post => (
        <div key={post.id} style={{ padding: '8px', borderBottom: '1px solid #eee' }}>
          <h4>{post.title}</h4>
          <p style={{ color: '#666' }}>{post.body.slice(0, 100)}...</p>
        </div>
      ))}
    </div>
  );
}
```

---

## 6. useEffectのよくある間違い

### 間違い1：依存配列の漏れ

```jsx
// NG：countを使っているのに依存配列に入れていない
useEffect(() => {
  document.title = `カウント: ${count}`;
}, []); // countが変わってもタイトルは更新されない

// OK
useEffect(() => {
  document.title = `カウント: ${count}`;
}, [count]);
```

### 間違い2：無限ループ

```jsx
// NG：stateを更新→再レンダリング→useEffect実行→state更新→...（無限ループ）
useEffect(() => {
  setCount(count + 1);
}); // 依存配列がないので毎回実行される

// NG：オブジェクトを依存配列に入れる（毎回新しいオブジェクトが作られる）
const options = { method: 'GET' };
useEffect(() => {
  fetch(url, options);
}, [options]); // optionsは毎回新しい参照→無限ループ
```

### 間違い3：クリーンアップの忘れ

```jsx
// NG：コンポーネントがアンマウントされてもタイマーが動き続ける
useEffect(() => {
  setInterval(() => {
    setCount(prev => prev + 1);
  }, 1000);
}, []);

// OK：クリーンアップでタイマーを停止
useEffect(() => {
  const id = setInterval(() => {
    setCount(prev => prev + 1);
  }, 1000);
  return () => clearInterval(id);
}, []);
```

---

## 7. 実践：天気予報アプリ風コンポーネント

```jsx
import { useState, useEffect } from 'react';

// 擬似的な天気APIのモック関数
function mockFetchWeather(city) {
  const weatherData = {
    "東京": { temp: 22, condition: "晴れ", humidity: 45 },
    "大阪": { temp: 24, condition: "曇り", humidity: 55 },
    "福岡": { temp: 26, condition: "晴れ", humidity: 50 },
    "札幌": { temp: 15, condition: "雨", humidity: 70 },
  };

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const data = weatherData[city];
      if (data) {
        resolve({ city, ...data });
      } else {
        reject(new Error(`${city}のデータが見つかりません`));
      }
    }, 1000); // 1秒の遅延をシミュレート
  });
}

function WeatherApp() {
  const [selectedCity, setSelectedCity] = useState("東京");
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const cities = ["東京", "大阪", "福岡", "札幌"];

  // 選択された都市が変わるたびにデータを取得
  useEffect(() => {
    let isCancelled = false;

    setLoading(true);
    setError(null);

    mockFetchWeather(selectedCity)
      .then(data => {
        if (!isCancelled) {
          setWeather(data);
          setLastUpdated(new Date().toLocaleTimeString());
          setLoading(false);
        }
      })
      .catch(err => {
        if (!isCancelled) {
          setError(err.message);
          setLoading(false);
        }
      });

    return () => {
      isCancelled = true;
    };
  }, [selectedCity]);

  // 30秒ごとに自動更新
  useEffect(() => {
    const intervalId = setInterval(() => {
      mockFetchWeather(selectedCity)
        .then(data => {
          setWeather(data);
          setLastUpdated(new Date().toLocaleTimeString());
        })
        .catch(() => {}); // 自動更新のエラーは無視
    }, 30000);

    return () => clearInterval(intervalId);
  }, [selectedCity]);

  // ページタイトルの更新
  useEffect(() => {
    if (weather) {
      document.title = `${weather.city}: ${weather.temp}°C ${weather.condition}`;
    }
    return () => {
      document.title = 'React App';
    };
  }, [weather]);

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <h1>天気予報</h1>

      {/* 都市選択 */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
        {cities.map(city => (
          <button
            key={city}
            onClick={() => setSelectedCity(city)}
            style={{
              padding: '8px 16px',
              backgroundColor: city === selectedCity ? '#3498db' : '#ecf0f1',
              color: city === selectedCity ? 'white' : '#333',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            {city}
          </button>
        ))}
      </div>

      {/* 表示エリア */}
      {loading && <p>読み込み中...</p>}

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {!loading && !error && weather && (
        <div style={{
          padding: '24px',
          backgroundColor: '#e3f2fd',
          borderRadius: '8px',
          textAlign: 'center',
        }}>
          <h2>{weather.city}</h2>
          <p style={{ fontSize: '48px', margin: '8px 0' }}>{weather.temp}°C</p>
          <p style={{ fontSize: '20px' }}>{weather.condition}</p>
          <p>湿度：{weather.humidity}%</p>
          {lastUpdated && (
            <small style={{ color: '#666' }}>最終更新：{lastUpdated}</small>
          )}
        </div>
      )}
    </div>
  );
}

export default WeatherApp;
```

---

## まとめ

| 項目 | ポイント |
|------|---------|
| 副作用 | UIの描画以外の処理（API通信、タイマー、DOM操作など） |
| useEffect | 副作用を安全に実行するためのフック |
| 依存配列 `[]` | 空配列＝マウント時に1回だけ実行 |
| 依存配列 `[a]` | `a`が変わるたびに実行 |
| 依存配列なし | 毎回のレンダリング後に実行 |
| クリーンアップ | `return () => { ... }` でタイマー停止、イベント解除など |
| API取得パターン | loading / error / data の3つのstateで管理 |
| async/await | useEffect内部で関数を定義して呼び出す |
| AbortController | リクエストのキャンセルに使う |

### ここまでのまとめ

5章を通じて、Reactの基本的な概念を学びました。

| 章 | 学んだこと |
|----|-----------|
| 第1章 | React / JSX / コンポーネントの基本 |
| 第2章 | props / children / コンポーネント設計 |
| 第3章 | state / useState / イベント / フォーム |
| 第4章 | 条件分岐 / リスト / key / フィルタ・ソート |
| 第5章 | useEffect / 副作用 / API通信 / クリーンアップ |

これらの知識を組み合わせることで、実用的なReactアプリケーションを構築できます。演習問題に取り組んで、理解を深めましょう！

### 次の章では

ロジックを再利用可能な形に切り出す「**カスタムフック**」について学びます。

---

## 動作サンプル

この章の概念を実装した完全なサンプルコードは `サンプル/05_DataFetcher.jsx` にあります。useEffect、APIデータ取得、ローディング/エラー管理、クリーンアップを実際に動かして確認できます。
