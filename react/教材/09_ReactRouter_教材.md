# 第9章：React Router

## この章で学ぶこと

- SPAとルーティングの概念
- React Routerのセットアップ
- BrowserRouter、Route、Linkの基本
- useNavigate、useParamsの使い方
- ネストされたルートとレイアウトルート
- 404ページとリダイレクト

---

## 1. SPAとルーティング

### SPA（Single Page Application）とは

従来のWebサイトはページ遷移のたびにサーバーからHTMLを取得していました。SPAでは、最初に1つのHTMLを読み込み、その後はJavaScriptがページの内容を動的に切り替えます。

| 項目 | 従来のWebサイト | SPA |
|------|---------------|-----|
| ページ遷移 | サーバーに毎回リクエスト | JavaScriptが画面を切り替え |
| 速度 | 遷移のたびにリロード | 高速（必要な部分だけ更新） |
| ユーザー体験 | ちらつきが発生 | スムーズな遷移 |

### React Routerとは

**React Router**は、ReactでSPAのルーティング（URLに応じた画面切り替え）を実現するライブラリです。

---

## 2. セットアップ

```bash
# React Routerをインストール
npm install react-router-dom
```

### 基本構造

```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      {/* ナビゲーション */}
      <nav>
        <Link to="/">ホーム</Link>
        <Link to="/about">About</Link>
        <Link to="/contact">お問い合わせ</Link>
      </nav>

      {/* ルート定義 */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </BrowserRouter>
  );
}

function Home() {
  return <h1>ホームページ</h1>;
}

function About() {
  return <h1>Aboutページ</h1>;
}

function Contact() {
  return <h1>お問い合わせページ</h1>;
}
```

### 主要コンポーネント

| コンポーネント | 役割 |
|-------------|------|
| `BrowserRouter` | ルーティング機能を有効にするラッパー |
| `Routes` | Routeのグループ（最初にマッチしたRouteを表示） |
| `Route` | URLパスとコンポーネントの対応を定義 |
| `Link` | ページ遷移用のリンク（`<a>`タグの代わり） |

### Link vs aタグ

```jsx
// NG：aタグだとページ全体がリロードされてしまう
<a href="/about">About</a>

// OK：Linkを使うとSPAの遷移（リロードなし）
<Link to="/about">About</Link>
```

---

## 3. useNavigate：プログラム的なページ遷移

```jsx
import { useNavigate } from 'react-router-dom';

function LoginForm() {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // ログイン処理...

    // 成功したらホームへ遷移
    navigate('/');

    // 前のページに戻る
    // navigate(-1);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="ユーザー名" />
      <input type="password" placeholder="パスワード" />
      <button type="submit">ログイン</button>
    </form>
  );
}
```

### navigateの使い方

| 呼び出し方 | 動作 |
|-----------|------|
| `navigate('/path')` | 指定パスに遷移 |
| `navigate(-1)` | 前のページに戻る |
| `navigate(-2)` | 2ページ前に戻る |
| `navigate(1)` | 次のページに進む |
| `navigate('/path', { replace: true })` | 現在の履歴を置換（戻るボタンで戻れない） |

---

## 4. 動的ルート（useParams）

URLにパラメータを含めることで、動的なページを作れます。

```jsx
import { BrowserRouter, Routes, Route, Link, useParams } from 'react-router-dom';

function App() {
  const users = [
    { id: 1, name: '田中太郎' },
    { id: 2, name: '鈴木花子' },
    { id: 3, name: '佐藤次郎' },
  ];

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<UserList users={users} />} />
        <Route path="/users/:userId" element={<UserDetail users={users} />} />
      </Routes>
    </BrowserRouter>
  );
}

function UserList({ users }) {
  return (
    <div>
      <h1>ユーザー一覧</h1>
      {users.map(user => (
        <div key={user.id}>
          <Link to={`/users/${user.id}`}>{user.name}</Link>
        </div>
      ))}
    </div>
  );
}

function UserDetail({ users }) {
  // URLのパラメータを取得
  const { userId } = useParams();
  const user = users.find(u => u.id === Number(userId));

  if (!user) return <p>ユーザーが見つかりません。</p>;

  return (
    <div>
      <h1>{user.name}</h1>
      <Link to="/">一覧に戻る</Link>
    </div>
  );
}
```

### URLパラメータの書き方

```jsx
// :パラメータ名 でURLの一部を変数として受け取れる
<Route path="/users/:userId" element={<UserDetail />} />
// → /users/1, /users/2, /users/abc ... がマッチ

<Route path="/posts/:category/:postId" element={<PostDetail />} />
// → /posts/tech/123 がマッチ

// useParamsで取得
const { userId } = useParams();       // "1", "2", "abc" など（文字列）
const { category, postId } = useParams(); // "tech", "123"
```

> **注意**：useParamsの値は常に**文字列**です。数値として使うなら `Number(userId)` で変換してください。

---

## 5. ネストされたルートとレイアウトルート

### レイアウトルート

共通のレイアウト（ヘッダー、サイドバーなど）を持つページ群をまとめられます。

```jsx
import { BrowserRouter, Routes, Route, Link, Outlet } from 'react-router-dom';

// 共通レイアウト
function Layout() {
  return (
    <div>
      <header style={{
        backgroundColor: '#2c3e50', color: 'white', padding: '16px',
        display: 'flex', gap: '16px',
      }}>
        <Link to="/" style={{ color: 'white' }}>ホーム</Link>
        <Link to="/products" style={{ color: 'white' }}>商品</Link>
        <Link to="/about" style={{ color: 'white' }}>About</Link>
      </header>

      <main style={{ padding: '20px' }}>
        {/* 子ルートの内容がここに表示される */}
        <Outlet />
      </main>

      <footer style={{ backgroundColor: '#ecf0f1', padding: '16px', textAlign: 'center' }}>
        &copy; 2026 マイショップ
      </footer>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Layoutが親ルート */}
        <Route path="/" element={<Layout />}>
          {/* index：親パスと同じURL */}
          <Route index element={<Home />} />
          <Route path="products" element={<Products />} />
          <Route path="products/:id" element={<ProductDetail />} />
          <Route path="about" element={<About />} />
          {/* 404ページ */}
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

### Outlet

`<Outlet />` は、ネストされた子ルートのコンポーネントが表示される場所です。レイアウトコンポーネント内に配置します。

---

## 6. NavLink：アクティブなリンクのスタイル

```jsx
import { NavLink } from 'react-router-dom';

function Navigation() {
  const linkStyle = ({ isActive }) => ({
    color: isActive ? '#3498db' : '#333',
    fontWeight: isActive ? 'bold' : 'normal',
    textDecoration: 'none',
    padding: '8px 16px',
    borderBottom: isActive ? '2px solid #3498db' : 'none',
  });

  return (
    <nav style={{ display: 'flex', gap: '8px', borderBottom: '1px solid #ddd' }}>
      <NavLink to="/" style={linkStyle} end>ホーム</NavLink>
      <NavLink to="/products" style={linkStyle}>商品</NavLink>
      <NavLink to="/about" style={linkStyle}>About</NavLink>
    </nav>
  );
}
```

> **`end`プロパティ**：`<NavLink to="/" end>` とすると、`/products` などの子パスでもアクティブになるのを防ぎます。

---

## 7. 404ページとリダイレクト

### 404（Not Found）ページ

```jsx
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/about" element={<About />} />
  {/* どのルートにもマッチしない場合 */}
  <Route path="*" element={<NotFound />} />
</Routes>

function NotFound() {
  return (
    <div style={{ textAlign: 'center', padding: '60px' }}>
      <h1 style={{ fontSize: '72px' }}>404</h1>
      <p>ページが見つかりません。</p>
      <Link to="/">ホームに戻る</Link>
    </div>
  );
}
```

### リダイレクト（Navigate）

```jsx
import { Navigate } from 'react-router-dom';

// 古いURLから新しいURLへリダイレクト
<Route path="/old-page" element={<Navigate to="/new-page" replace />} />

// ログインしていない場合にリダイレクト
function ProtectedRoute({ children }) {
  const { isLoggedIn } = useAuth();

  if (!isLoggedIn) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

// 使い方
<Route path="/dashboard" element={
  <ProtectedRoute>
    <Dashboard />
  </ProtectedRoute>
} />
```

---

## 8. useSearchParams：クエリパラメータ

```jsx
import { useSearchParams } from 'react-router-dom';

function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();

  const query = searchParams.get('q') || '';
  const category = searchParams.get('category') || 'all';

  return (
    <div>
      <h1>検索</h1>

      <input
        value={query}
        onChange={(e) => {
          setSearchParams({ q: e.target.value, category });
        }}
        placeholder="検索キーワード..."
      />

      <select
        value={category}
        onChange={(e) => {
          setSearchParams({ q: query, category: e.target.value });
        }}
      >
        <option value="all">すべて</option>
        <option value="books">書籍</option>
        <option value="electronics">電子機器</option>
      </select>

      <p>検索中: {query} (カテゴリ: {category})</p>
      {/* URL: /search?q=React&category=books */}
    </div>
  );
}
```

---

## 9. 実践：ブログサイトのルーティング

```jsx
import { BrowserRouter, Routes, Route, Link, Outlet, useParams, NavLink } from 'react-router-dom';

// データ
const posts = [
  { id: 1, title: 'React入門', category: 'frontend', content: 'Reactの基本を学びましょう...' },
  { id: 2, title: 'Node.js入門', category: 'backend', content: 'Node.jsでサーバーを作りましょう...' },
  { id: 3, title: 'CSS Tips', category: 'frontend', content: 'CSSの便利なテクニック集...' },
];

// レイアウト
function BlogLayout() {
  const navStyle = ({ isActive }) => ({
    padding: '8px 16px',
    backgroundColor: isActive ? '#3498db' : 'transparent',
    color: isActive ? 'white' : '#333',
    textDecoration: 'none',
    borderRadius: '4px',
  });

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <header style={{ padding: '16px', borderBottom: '2px solid #3498db' }}>
        <h1>マイブログ</h1>
        <nav style={{ display: 'flex', gap: '8px' }}>
          <NavLink to="/" style={navStyle} end>ホーム</NavLink>
          <NavLink to="/posts" style={navStyle}>記事一覧</NavLink>
          <NavLink to="/about" style={navStyle}>About</NavLink>
        </nav>
      </header>
      <main style={{ padding: '20px' }}>
        <Outlet />
      </main>
    </div>
  );
}

function Home() {
  return (
    <div>
      <h2>最新の記事</h2>
      {posts.slice(0, 2).map(post => (
        <div key={post.id} style={{ margin: '8px 0' }}>
          <Link to={`/posts/${post.id}`}>{post.title}</Link>
        </div>
      ))}
    </div>
  );
}

function PostList() {
  return (
    <div>
      <h2>記事一覧</h2>
      {posts.map(post => (
        <div key={post.id} style={{
          padding: '12px', margin: '8px 0',
          border: '1px solid #ddd', borderRadius: '8px',
        }}>
          <Link to={`/posts/${post.id}`} style={{ fontSize: '18px' }}>
            {post.title}
          </Link>
          <span style={{
            marginLeft: '8px', backgroundColor: '#e3f2fd',
            padding: '2px 8px', borderRadius: '12px', fontSize: '12px',
          }}>
            {post.category}
          </span>
        </div>
      ))}
    </div>
  );
}

function PostDetail() {
  const { postId } = useParams();
  const post = posts.find(p => p.id === Number(postId));

  if (!post) return <p>記事が見つかりません。</p>;

  return (
    <article>
      <h2>{post.title}</h2>
      <span style={{ color: '#666' }}>カテゴリ: {post.category}</span>
      <p style={{ marginTop: '16px', lineHeight: '1.8' }}>{post.content}</p>
      <Link to="/posts">一覧に戻る</Link>
    </article>
  );
}

function About() {
  return <p>このブログはReact学習用のサンプルです。</p>;
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
        <Route path="/" element={<BlogLayout />}>
          <Route index element={<Home />} />
          <Route path="posts" element={<PostList />} />
          <Route path="posts/:postId" element={<PostDetail />} />
          <Route path="about" element={<About />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

---

## まとめ

| 項目 | ポイント |
|------|---------|
| React Router | SPAのURLルーティングを管理するライブラリ |
| BrowserRouter | アプリ全体をラップしてルーティングを有効にする |
| Route | `path` と `element` でURLとコンポーネントを対応付け |
| Link / NavLink | SPAのページ遷移リンク。NavLinkはアクティブ状態を検出できる |
| useNavigate | プログラム的にページ遷移する |
| useParams | URLパラメータ（`:id`）を取得する |
| Outlet | ネストされた子ルートの表示場所 |
| `path="*"` | 404ページに使う |
| Navigate | リダイレクトに使う |

### 次の章では

**パフォーマンス最適化**のテクニック（React.memo、useMemo、useCallback、lazy/Suspense）を学びます。

---

## 動作サンプル

この章の概念を実装した完全なサンプルコードは `サンプル/09_MultiPageApp.jsx` にあります。ルーティング、ネストされたルート、動的パラメータ、レイアウトルートを実際に動かして確認できます。
