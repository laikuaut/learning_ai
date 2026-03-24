# 第9章 演習：React Router

> 対応教材: `教材/09_ReactRouter_教材.md`
>
> この演習では、React Router を使った SPA のルーティング、
> 動的パラメータ、ネストされたルート、ナビゲーションガードを練習します。

---

## 演習1（基本）：基本的なルーティングを設定しよう

以下の3ページを持つSPAを React Router で作成してください。

**要件：**
- `/` → ホームページ（「ようこそ！」と表示）
- `/about` → Aboutページ（自己紹介を表示）
- `/contact` → お問い合わせページ（連絡先を表示）
- ナビゲーションバーに `Link` を使った3つのリンクを配置
- 存在しないURLにアクセスしたら404ページを表示

<details>
<summary>ヒント</summary>

`BrowserRouter` でアプリ全体をラップし、`Routes` の中に `Route` を配置します。
404ページには `path="*"` を使います。

```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

// ========================================
// 各ページコンポーネント
// Reactでは1つのHTMLの中でURLに応じた画面切り替えを行う（SPA）
// ========================================
function Home() {
  return (
    <div>
      <h1>ようこそ！</h1>
      <p>React Router で作ったSPAのホームページです。</p>
    </div>
  );
}

function About() {
  return (
    <div>
      <h1>About</h1>
      <p>このサイトはReact Router の学習用サンプルです。</p>
    </div>
  );
}

function Contact() {
  return (
    <div>
      <h1>お問い合わせ</h1>
      <p>メール: example@example.com</p>
    </div>
  );
}

// ========================================
// 404ページ：path="*" はどのルートにもマッチしなかった場合に表示
// ========================================
function NotFound() {
  return (
    <div style={{ textAlign: 'center', padding: '60px' }}>
      <h1 style={{ fontSize: '72px' }}>404</h1>
      <p>ページが見つかりません。</p>
      <Link to="/">ホームに戻る</Link>
    </div>
  );
}

function App() {
  const navStyle = {
    display: 'flex', gap: '16px', padding: '16px',
    backgroundColor: '#2c3e50', listStyle: 'none',
  };
  const linkStyle = { color: 'white', textDecoration: 'none' };

  return (
    <BrowserRouter>
      {/* ナビゲーション：Link を使うとページリロードなしで遷移 */}
      <nav style={navStyle}>
        <Link to="/" style={linkStyle}>ホーム</Link>
        <Link to="/about" style={linkStyle}>About</Link>
        <Link to="/contact" style={linkStyle}>お問い合わせ</Link>
      </nav>

      {/* ルート定義：URLとコンポーネントの対応 */}
      <div style={{ padding: '20px' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
```

**ポイント：**
- `<Link>` は `<a>` タグの代わりに使います。`<a>` だとページ全体がリロードされてしまいます
- `path="*"` は他のどのルートにもマッチしなかった場合のフォールバックです
- `Routes` は最初にマッチした `Route` だけを表示します

</details>

---

## 演習2（基本）：動的ルートでユーザー詳細ページを作ろう

ユーザー一覧と、ユーザーIDに応じた詳細ページを作成してください。

**要件：**
- `/users` → ユーザー一覧を表示（各ユーザー名がリンク）
- `/users/:userId` → 選択したユーザーの詳細を表示
- `useParams` でURLパラメータを取得する
- 存在しないユーザーIDの場合は「ユーザーが見つかりません」と表示

**データ：**
```javascript
const users = [
  { id: 1, name: '田中太郎', email: 'tanaka@example.com', role: 'エンジニア' },
  { id: 2, name: '鈴木花子', email: 'suzuki@example.com', role: 'デザイナー' },
  { id: 3, name: '佐藤次郎', email: 'sato@example.com', role: 'マネージャー' },
];
```

<details>
<summary>ヒント</summary>

`useParams` の返す値は常に**文字列**です。数値と比較するときは `Number()` で変換してください。

```jsx
const { userId } = useParams();
const user = users.find(u => u.id === Number(userId));
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { BrowserRouter, Routes, Route, Link, useParams } from 'react-router-dom';

const users = [
  { id: 1, name: '田中太郎', email: 'tanaka@example.com', role: 'エンジニア' },
  { id: 2, name: '鈴木花子', email: 'suzuki@example.com', role: 'デザイナー' },
  { id: 3, name: '佐藤次郎', email: 'sato@example.com', role: 'マネージャー' },
];

// ========================================
// ユーザー一覧：Link で詳細ページへ遷移
// to={`/users/${user.id}`} で動的なURLを生成
// ========================================
function UserList() {
  return (
    <div>
      <h2>ユーザー一覧</h2>
      {users.map(user => (
        <div key={user.id} style={{
          padding: '12px', margin: '8px 0',
          border: '1px solid #ddd', borderRadius: '8px',
        }}>
          <Link to={`/users/${user.id}`} style={{ fontSize: '18px' }}>
            {user.name}
          </Link>
          <span style={{ marginLeft: '12px', color: '#666' }}>{user.role}</span>
        </div>
      ))}
    </div>
  );
}

// ========================================
// ユーザー詳細：useParams でURLの :userId を取得
// 注意：useParams の値は必ず文字列なので Number() で変換
// ========================================
function UserDetail() {
  const { userId } = useParams();
  const user = users.find(u => u.id === Number(userId));

  if (!user) {
    return (
      <div>
        <h2>ユーザーが見つかりません</h2>
        <p>ID: {userId} のユーザーは存在しません。</p>
        <Link to="/users">一覧に戻る</Link>
      </div>
    );
  }

  return (
    <div>
      <h2>{user.name}</h2>
      <table style={{ borderCollapse: 'collapse' }}>
        <tbody>
          <tr><td style={{ padding: '8px', fontWeight: 'bold' }}>メール</td><td style={{ padding: '8px' }}>{user.email}</td></tr>
          <tr><td style={{ padding: '8px', fontWeight: 'bold' }}>役割</td><td style={{ padding: '8px' }}>{user.role}</td></tr>
        </tbody>
      </table>
      <Link to="/users" style={{ display: 'inline-block', marginTop: '16px' }}>← 一覧に戻る</Link>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: '16px', backgroundColor: '#2c3e50' }}>
        <Link to="/" style={{ color: 'white', marginRight: '16px' }}>ホーム</Link>
        <Link to="/users" style={{ color: 'white' }}>ユーザー</Link>
      </nav>
      <div style={{ padding: '20px' }}>
        <Routes>
          <Route path="/" element={<h1>ホーム</h1>} />
          <Route path="/users" element={<UserList />} />
          <Route path="/users/:userId" element={<UserDetail />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
```

**ポイント：**
- `:userId` はURLパラメータのプレースホルダーです。`/users/1`、`/users/2` などがマッチします
- `useParams()` は `{ userId: "1" }` のようにオブジェクトを返します（値は文字列）
- 存在しないIDへのアクセスを考慮し、ユーザーが見つからない場合のフォールバック表示を用意しましょう

</details>

---

## 演習3（基本）：useNavigateでプログラム的に遷移しよう

ログインフォームを作成し、ログイン成功時に `useNavigate` でダッシュボードへ遷移してください。

**要件：**
- `/login` → ログインフォーム（ユーザー名とパスワードの入力欄）
- `/dashboard` → ダッシュボードページ（ログイン後に表示）
- ユーザー名が `admin`、パスワードが `password` の場合に遷移
- 不正な場合はエラーメッセージを表示
- ダッシュボードに「ログアウト」ボタンを置き、クリックでログインページに戻る

<details>
<summary>ヒント</summary>

`useNavigate` はフック関数で、返される `navigate` 関数を呼び出すとページ遷移できます。

```jsx
const navigate = useNavigate();
navigate('/dashboard');         // ダッシュボードへ遷移
navigate('/login', { replace: true }); // 履歴を置換（戻るボタンで戻れない）
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState } from 'react';
import { BrowserRouter, Routes, Route, useNavigate, Link } from 'react-router-dom';

// ========================================
// ログインフォーム：useNavigate で遷移
// navigate('/dashboard') はリンクのクリックではなく
// JavaScript コードからの遷移（ログイン成功後など）に使う
// ========================================
function LoginForm() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    // 簡易的な認証チェック
    if (username === 'admin' && password === 'password') {
      // 成功 → ダッシュボードへ遷移
      // replace: true にすると「戻る」ボタンでログインページに戻れない
      navigate('/dashboard', { replace: true });
    } else {
      setError('ユーザー名またはパスワードが間違っています');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '40px auto', padding: '20px' }}>
      <h2>ログイン</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '12px' }}>
          <label style={{ display: 'block', marginBottom: '4px' }}>ユーザー名</label>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="admin"
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        <div style={{ marginBottom: '12px' }}>
          <label style={{ display: 'block', marginBottom: '4px' }}>パスワード</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="password"
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
        {error && <p style={{ color: '#e74c3c' }}>{error}</p>}
        <button type="submit" style={{ width: '100%', padding: '10px' }}>ログイン</button>
      </form>
    </div>
  );
}

// ========================================
// ダッシュボード：ログアウトで navigate(-1) ではなく
// navigate('/login') で明示的にログインページへ遷移
// ========================================
function Dashboard() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: '20px' }}>
      <h2>ダッシュボード</h2>
      <p>ログインに成功しました！</p>
      <button onClick={() => navigate('/login', { replace: true })}>
        ログアウト
      </button>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginForm />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

**ポイント：**
- `navigate('/path')` はボタンクリックやフォーム送信後などのプログラム的な遷移に使います
- `{ replace: true }` オプションを付けると、ブラウザの「戻る」ボタンで前の画面に戻れなくなります（ログアウト後にダッシュボードに戻れてしまうのを防ぐ）
- リンクをクリックして遷移する場合は `<Link>` を使い、コードで遷移する場合は `useNavigate` を使い分けます

</details>

---

## 演習4（応用）：ネストされたルートでレイアウトを共有しよう

共通ヘッダー・フッターを持つレイアウトルートを作成し、ネストされた子ルートで各ページを表示してください。

**要件：**
- `Layout` コンポーネント：ヘッダー（NavLink で3つのリンク）、フッター、`<Outlet />` で子ルートを表示
- `NavLink` でアクティブなリンクにスタイルを適用
- `/` → ホームページ（`index` ルート）
- `/products` → 商品一覧
- `/products/:productId` → 商品詳細
- `*` → 404ページ

<details>
<summary>ヒント</summary>

- レイアウトルートは子 `Route` をネストすることで作ります
- `<Outlet />` は子ルートのコンポーネントが表示される場所です
- `NavLink` は `isActive` プロパティで現在のURLとマッチしているか判定できます
- `index` ルートは親パスと同じURLにマッチします

```jsx
<Route path="/" element={<Layout />}>
  <Route index element={<Home />} />
  <Route path="products" element={<Products />} />
</Route>
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { BrowserRouter, Routes, Route, Link, NavLink, Outlet, useParams } from 'react-router-dom';

const products = [
  { id: 1, name: 'React入門書', price: 2800, description: 'Reactの基礎を丁寧に解説' },
  { id: 2, name: 'TypeScriptガイド', price: 3200, description: 'TSの実践的な使い方を網羅' },
  { id: 3, name: 'Next.js実践', price: 3500, description: 'フルスタック開発をマスター' },
];

// ========================================
// レイアウトコンポーネント：
// ヘッダー + Outlet（子ルートの表示場所）+ フッター
// ========================================
function Layout() {
  // NavLink は isActive で現在アクティブかどうか判定できる
  const navStyle = ({ isActive }) => ({
    color: isActive ? '#3498db' : '#ecf0f1',
    fontWeight: isActive ? 'bold' : 'normal',
    textDecoration: 'none',
    padding: '8px 16px',
    borderBottom: isActive ? '2px solid #3498db' : '2px solid transparent',
  });

  return (
    <div>
      <header style={{
        backgroundColor: '#2c3e50', padding: '16px',
        display: 'flex', alignItems: 'center', gap: '16px',
      }}>
        <h1 style={{ color: 'white', margin: 0, fontSize: '20px' }}>マイショップ</h1>
        <nav style={{ display: 'flex', gap: '4px' }}>
          {/* end をつけると /products でもアクティブにならない */}
          <NavLink to="/" style={navStyle} end>ホーム</NavLink>
          <NavLink to="/products" style={navStyle}>商品</NavLink>
          <NavLink to="/about" style={navStyle}>About</NavLink>
        </nav>
      </header>

      <main style={{ padding: '20px', minHeight: '60vh' }}>
        {/* 子ルートのコンポーネントがここに表示される */}
        <Outlet />
      </main>

      <footer style={{
        backgroundColor: '#ecf0f1', padding: '16px',
        textAlign: 'center', color: '#666',
      }}>
        &copy; 2026 マイショップ
      </footer>
    </div>
  );
}

function Home() {
  return (
    <div>
      <h2>ようこそ！</h2>
      <p>最新の技術書が揃っています。</p>
    </div>
  );
}

function ProductList() {
  return (
    <div>
      <h2>商品一覧</h2>
      {products.map(product => (
        <div key={product.id} style={{
          padding: '16px', margin: '8px 0',
          border: '1px solid #ddd', borderRadius: '8px',
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        }}>
          <div>
            <Link to={`/products/${product.id}`} style={{ fontSize: '18px' }}>
              {product.name}
            </Link>
            <p style={{ color: '#666', margin: '4px 0 0' }}>{product.description}</p>
          </div>
          <span style={{ fontSize: '18px', fontWeight: 'bold' }}>
            ¥{product.price.toLocaleString()}
          </span>
        </div>
      ))}
    </div>
  );
}

function ProductDetail() {
  const { productId } = useParams();
  const product = products.find(p => p.id === Number(productId));

  if (!product) {
    return (
      <div>
        <h2>商品が見つかりません</h2>
        <Link to="/products">商品一覧に戻る</Link>
      </div>
    );
  }

  return (
    <div>
      <h2>{product.name}</h2>
      <p>{product.description}</p>
      <p style={{ fontSize: '24px', fontWeight: 'bold' }}>¥{product.price.toLocaleString()}</p>
      <Link to="/products">← 商品一覧に戻る</Link>
    </div>
  );
}

function About() {
  return <p>技術書専門のオンラインショップです。</p>;
}

function NotFound() {
  return (
    <div style={{ textAlign: 'center' }}>
      <h2>404 - ページが見つかりません</h2>
      <Link to="/">ホームに戻る</Link>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Layout が親ルート。子ルートは <Outlet /> に表示される */}
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="products" element={<ProductList />} />
          <Route path="products/:productId" element={<ProductDetail />} />
          <Route path="about" element={<About />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

**ポイント：**
- ネストされた `Route` は親の `<Outlet />` の場所に表示されます
- `NavLink` の `end` プロパティは「完全一致」の場合のみアクティブにするオプションです（`/` が `/products` でもアクティブにならないようにする）
- `index` ルートは親パスと同じURL（この場合 `/`）にマッチする特別なルートです

</details>

---

## 演習5（応用）：useSearchParamsで検索機能を作ろう

クエリパラメータを使った商品検索ページを作成してください。

**要件：**
- 検索キーワードの入力欄
- カテゴリの選択（全て / フロントエンド / バックエンド / インフラ）
- URLのクエリパラメータ（`?q=React&category=frontend`）と同期
- ブラウザの戻る/進むボタンで検索状態が復元される

<details>
<summary>ヒント</summary>

`useSearchParams` は URL のクエリパラメータ（`?key=value`）を読み書きできるフックです。

```jsx
const [searchParams, setSearchParams] = useSearchParams();
const query = searchParams.get('q') || '';
setSearchParams({ q: 'React', category: 'frontend' });
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { BrowserRouter, Routes, Route, useSearchParams } from 'react-router-dom';

const allProducts = [
  { id: 1, name: 'React入門', category: 'frontend', price: 2800 },
  { id: 2, name: 'Vue.js実践', category: 'frontend', price: 3200 },
  { id: 3, name: 'Node.js入門', category: 'backend', price: 2500 },
  { id: 4, name: 'Python Django', category: 'backend', price: 3000 },
  { id: 5, name: 'Docker入門', category: 'infra', price: 2200 },
  { id: 6, name: 'AWS実践ガイド', category: 'infra', price: 3800 },
  { id: 7, name: 'TypeScript完全ガイド', category: 'frontend', price: 3500 },
];

// ========================================
// useSearchParams でURLのクエリパラメータと同期
// → ブラウザの「戻る」「進む」で検索状態が復元できる
// → URLをブックマーク/共有すれば同じ検索結果を再現できる
// ========================================
function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();

  // URLからクエリパラメータを読み取り
  const query = searchParams.get('q') || '';
  const category = searchParams.get('category') || 'all';

  // フィルタリング
  const filteredProducts = allProducts.filter(product => {
    const matchesQuery = product.name.toLowerCase().includes(query.toLowerCase());
    const matchesCategory = category === 'all' || product.category === category;
    return matchesQuery && matchesCategory;
  });

  // クエリパラメータを更新する関数
  const updateParams = (newParams) => {
    const current = Object.fromEntries(searchParams.entries());
    setSearchParams({ ...current, ...newParams });
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h2>商品検索</h2>

      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
        <input
          value={query}
          onChange={(e) => updateParams({ q: e.target.value })}
          placeholder="キーワードで検索..."
          style={{ flex: 1, padding: '8px' }}
        />
        <select
          value={category}
          onChange={(e) => updateParams({ category: e.target.value })}
          style={{ padding: '8px' }}
        >
          <option value="all">すべて</option>
          <option value="frontend">フロントエンド</option>
          <option value="backend">バックエンド</option>
          <option value="infra">インフラ</option>
        </select>
      </div>

      <p style={{ color: '#666' }}>{filteredProducts.length} 件の商品</p>

      {filteredProducts.map(product => (
        <div key={product.id} style={{
          padding: '12px', margin: '8px 0',
          border: '1px solid #ddd', borderRadius: '8px',
          display: 'flex', justifyContent: 'space-between',
        }}>
          <div>
            <strong>{product.name}</strong>
            <span style={{
              marginLeft: '8px', backgroundColor: '#e3f2fd',
              padding: '2px 8px', borderRadius: '12px', fontSize: '12px',
            }}>
              {product.category}
            </span>
          </div>
          <span>¥{product.price.toLocaleString()}</span>
        </div>
      ))}

      {filteredProducts.length === 0 && (
        <p style={{ textAlign: 'center', color: '#999', padding: '40px' }}>
          該当する商品がありません
        </p>
      )}
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SearchPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

**ポイント：**
- `useSearchParams` は `useState` に似た API ですが、値がURLのクエリパラメータと同期されます
- URLに検索状態が反映されるため、ブックマークやURL共有で検索条件を再現できます
- `searchParams.get('key')` は値がなければ `null` を返すので、デフォルト値を `||` で設定します

</details>

---

## 演習6（チャレンジ）：保護されたルートを実装しよう

ログイン状態に応じてアクセスを制御する「保護されたルート」を実装してください。

**要件：**
- `ProtectedRoute` コンポーネントを作成
- ログインしていない状態で `/dashboard` にアクセスすると `/login` にリダイレクト
- ログイン後は `/dashboard` にアクセスできる
- ログイン状態は `useState` で管理（簡易的な実装でOK）
- Navigate コンポーネントを使ってリダイレクトを実装

<details>
<summary>ヒント</summary>

`ProtectedRoute` は children を受け取り、ログイン状態に応じて `<Navigate>` でリダイレクトするコンポーネントです。

```jsx
import { Navigate } from 'react-router-dom';

function ProtectedRoute({ isLoggedIn, children }) {
  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }
  return children;
}
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState } from 'react';
import { BrowserRouter, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';

// ========================================
// ProtectedRoute：認証ガード
// ログインしていない場合は /login にリダイレクト
// replace を付けることで、戻るボタンで保護されたページに戻らない
// ========================================
function ProtectedRoute({ isLoggedIn, children }) {
  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function LoginPage({ onLogin }) {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username === 'admin' && password === 'password') {
      onLogin(true);
      navigate('/dashboard', { replace: true });
    } else {
      setError('認証に失敗しました（admin / password でログイン）');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '40px auto', padding: '20px' }}>
      <h2>ログイン</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '12px' }}>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="ユーザー名"
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>
        <div style={{ marginBottom: '12px' }}>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="パスワード"
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>
        {error && <p style={{ color: '#e74c3c', fontSize: '14px' }}>{error}</p>}
        <button type="submit" style={{ width: '100%', padding: '10px' }}>ログイン</button>
      </form>
    </div>
  );
}

function Dashboard({ onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/login', { replace: true });
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>ダッシュボード</h2>
      <p>ログイン中のユーザーだけがアクセスできるページです。</p>
      <button onClick={handleLogout}>ログアウト</button>
    </div>
  );
}

function Settings({ onLogout }) {
  return (
    <div style={{ padding: '20px' }}>
      <h2>設定</h2>
      <p>こちらも保護されたページです。</p>
    </div>
  );
}

function Home() {
  return (
    <div style={{ padding: '20px' }}>
      <h2>ホーム</h2>
      <p>誰でもアクセスできるページです。</p>
    </div>
  );
}

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <BrowserRouter>
      <nav style={{
        padding: '16px', backgroundColor: '#2c3e50',
        display: 'flex', gap: '16px', alignItems: 'center',
      }}>
        <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>ホーム</Link>
        <Link to="/dashboard" style={{ color: 'white', textDecoration: 'none' }}>ダッシュボード</Link>
        <Link to="/settings" style={{ color: 'white', textDecoration: 'none' }}>設定</Link>
        <span style={{ marginLeft: 'auto', color: isLoggedIn ? '#2ecc71' : '#e74c3c' }}>
          {isLoggedIn ? 'ログイン中' : '未ログイン'}
        </span>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LoginPage onLogin={setIsLoggedIn} />} />
        {/* 保護されたルート */}
        <Route path="/dashboard" element={
          <ProtectedRoute isLoggedIn={isLoggedIn}>
            <Dashboard onLogout={() => setIsLoggedIn(false)} />
          </ProtectedRoute>
        } />
        <Route path="/settings" element={
          <ProtectedRoute isLoggedIn={isLoggedIn}>
            <Settings />
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

**ポイント：**
- `<Navigate to="/login" replace />` はレンダリング時に即座にリダイレクトするコンポーネントです
- `ProtectedRoute` パターンは実務でよく使われる認証ガードの基本形です
- 実際のアプリでは、認証状態を Context で管理し、トークンの検証なども行います
- `replace` を付けることで、ブラウザの履歴にリダイレクト元のURLが残りません

</details>

---

## まとめ

| 演習 | レベル | 学習ポイント |
|------|--------|-------------|
| 1 | 基本 | BrowserRouter、Routes、Route、Link、404ページ |
| 2 | 基本 | 動的ルート（:param）、useParams |
| 3 | 基本 | useNavigate、プログラム的な遷移 |
| 4 | 応用 | ネストされたルート、Outlet、NavLink |
| 5 | 応用 | useSearchParams、クエリパラメータとの同期 |
| 6 | チャレンジ | ProtectedRoute、Navigate、認証ガード |
