# 第7章：useContextとグローバル状態

## この章で学ぶこと

- props drilling（バケツリレー）の問題
- createContextとuseContextの使い方
- Providerパターン
- 複数のContextの組み合わせ
- Contextを使うべき場面と使うべきでない場面

---

## 1. props drillingの問題

通常、親から子へのデータ受け渡しはpropsで行います。しかし、深くネストしたコンポーネントにデータを渡す場合、中間コンポーネントがデータを使わないのに「バケツリレー」でpropsを渡す必要があります。

```jsx
// 問題：Appのthemeを深い階層のButtonに渡したい
function App() {
  const [theme, setTheme] = useState('light');
  return <Header theme={theme} />;        // Headerはthemeを使わない
}

function Header({ theme }) {
  return <NavBar theme={theme} />;         // NavBarもthemeを使わない
}

function NavBar({ theme }) {
  return <UserMenu theme={theme} />;       // UserMenuもthemeを使わない
}

function UserMenu({ theme }) {
  return <Button theme={theme}>ログアウト</Button>; // Buttonだけがthemeを使う
}
```

この問題を **props drilling** と呼びます。Contextを使えば解決できます。

---

## 2. Contextの基本

### 3ステップで使う

```jsx
import { createContext, useContext, useState } from 'react';

// ステップ1：Contextを作成する
const ThemeContext = createContext('light');

// ステップ2：Providerで値を提供する
function App() {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={theme}>
      <Header />
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        テーマ切替
      </button>
    </ThemeContext.Provider>
  );
}

// ステップ3：useContextで値を取得する
function Header() {
  return <NavBar />;  // propsを渡す必要なし！
}

function NavBar() {
  return <UserMenu />;  // propsを渡す必要なし！
}

function UserMenu() {
  const theme = useContext(ThemeContext);  // 直接取得！
  return (
    <button style={{
      backgroundColor: theme === 'light' ? '#fff' : '#333',
      color: theme === 'light' ? '#333' : '#fff',
    }}>
      ログアウト
    </button>
  );
}
```

### createContextの引数

```jsx
// デフォルト値を設定できる（Providerの外で使われた場合の値）
const ThemeContext = createContext('light');

// オブジェクトも渡せる
const UserContext = createContext({ name: 'ゲスト', isLoggedIn: false });
```

---

## 3. 実践的なContextパターン

### テーマ切り替え

```jsx
import { createContext, useContext, useState } from 'react';

// Context + Provider + フックをセットで作る
const ThemeContext = createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const themeStyles = {
    light: { backgroundColor: '#ffffff', color: '#333333' },
    dark: { backgroundColor: '#1a1a2e', color: '#e0e0e0' },
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, styles: themeStyles[theme] }}>
      {children}
    </ThemeContext.Provider>
  );
}

// カスタムフックでContextを簡単に使えるようにする
function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useThemeはThemeProviderの中で使用してください');
  }
  return context;
}

// 使用するコンポーネント
function Header() {
  const { theme, toggleTheme, styles } = useTheme();

  return (
    <header style={{ ...styles, padding: '16px', display: 'flex', justifyContent: 'space-between' }}>
      <h1>マイアプリ</h1>
      <button onClick={toggleTheme}>
        {theme === 'light' ? 'ダークモード' : 'ライトモード'}
      </button>
    </header>
  );
}

function Content() {
  const { styles } = useTheme();

  return (
    <main style={{ ...styles, padding: '20px', minHeight: '300px' }}>
      <p>テーマが自動的に適用されます。</p>
    </main>
  );
}

// App
function App() {
  return (
    <ThemeProvider>
      <Header />
      <Content />
    </ThemeProvider>
  );
}
```

### 認証状態の管理

```jsx
import { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = (username, password) => {
    // 実際にはAPIを呼ぶ
    if (username && password) {
      setUser({ name: username, role: 'user' });
      return true;
    }
    return false;
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoggedIn: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuthはAuthProviderの中で使用してください');
  }
  return context;
}

// ログインフォーム
function LoginForm() {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    login(username, password);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="ユーザー名" />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="パスワード" />
      <button type="submit">ログイン</button>
    </form>
  );
}

// ユーザー情報表示
function UserInfo() {
  const { user, logout, isLoggedIn } = useAuth();

  if (!isLoggedIn) return <LoginForm />;

  return (
    <div>
      <p>ようこそ、{user.name}さん！</p>
      <button onClick={logout}>ログアウト</button>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <UserInfo />
    </AuthProvider>
  );
}
```

---

## 4. 複数のContextを組み合わせる

```jsx
function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <LanguageProvider>
          <MainContent />
        </LanguageProvider>
      </ThemeProvider>
    </AuthProvider>
  );
}
```

ネストが深くなる場合は、まとめるProviderを作ることもできます。

```jsx
function AppProviders({ children }) {
  return (
    <AuthProvider>
      <ThemeProvider>
        <LanguageProvider>
          {children}
        </LanguageProvider>
      </ThemeProvider>
    </AuthProvider>
  );
}

function App() {
  return (
    <AppProviders>
      <MainContent />
    </AppProviders>
  );
}
```

---

## 5. 言語切り替え（i18n）の実装例

```jsx
import { createContext, useContext, useState } from 'react';

const translations = {
  ja: {
    greeting: 'こんにちは',
    logout: 'ログアウト',
    settings: '設定',
    language: '言語',
  },
  en: {
    greeting: 'Hello',
    logout: 'Logout',
    settings: 'Settings',
    language: 'Language',
  },
};

const LanguageContext = createContext();

function LanguageProvider({ children }) {
  const [lang, setLang] = useState('ja');

  const t = (key) => translations[lang][key] || key;

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

function useLanguage() {
  return useContext(LanguageContext);
}

// 使用例
function Header() {
  const { t, lang, setLang } = useLanguage();

  return (
    <header style={{ padding: '16px', display: 'flex', justifyContent: 'space-between' }}>
      <h1>{t('greeting')}</h1>
      <select value={lang} onChange={(e) => setLang(e.target.value)}>
        <option value="ja">日本語</option>
        <option value="en">English</option>
      </select>
    </header>
  );
}
```

---

## 6. Contextを使うべき場面

| 適している | 適していない |
|-----------|-------------|
| テーマ（ライト/ダーク） | 頻繁に変わるデータ（マウス位置など） |
| ログインユーザー情報 | 一部のコンポーネントだけが使うデータ |
| 言語/ロケール設定 | パフォーマンスが重要な場合 |
| グローバルな設定値 | 複雑な状態管理（→ useReducerと組み合わせ） |

### 注意：Contextの再レンダリング

Providerのvalueが変わると、そのContextを使っている**全ての**子コンポーネントが再レンダリングされます。

```jsx
// 注意：valueにオブジェクトリテラルを直接書くと、
// 毎レンダリングで新しいオブジェクトが作られ、不要な再レンダリングが発生する
function App() {
  const [count, setCount] = useState(0);

  // NG：毎回新しいオブジェクトが作られる
  return (
    <MyContext.Provider value={{ count, setCount }}>
      {children}
    </MyContext.Provider>
  );
}

// OK：useMemoでオブジェクトをメモ化する
function App() {
  const [count, setCount] = useState(0);

  const value = useMemo(() => ({ count, setCount }), [count]);

  return (
    <MyContext.Provider value={value}>
      {children}
    </MyContext.Provider>
  );
}
```

---

## まとめ

| 項目 | ポイント |
|------|---------|
| props drilling | 中間コンポーネントが不要なpropsを中継する問題 |
| createContext | Contextオブジェクトを作成する |
| Provider | `<Context.Provider value={...}>` で値を提供する |
| useContext | Provider配下のコンポーネントで値を取得する |
| カスタムフック | `useTheme()` のようにContextをラップすると使いやすい |
| 複数Context | Providerをネストして組み合わせる |
| 注意点 | valueが変わると全消費コンポーネントが再レンダリングされる |

### 次の章では

より複雑な状態管理を扱う「**useReducer**」を学びます。useContextと組み合わせることで、Reduxに近い状態管理を実現できます。

---

## 動作サンプル

この章の概念を実装した完全なサンプルコードは `サンプル/07_ThemeContext.jsx` にあります。テーマ切り替え、Providerパターン、カスタムフックによるContext活用を実際に動かして確認できます。
