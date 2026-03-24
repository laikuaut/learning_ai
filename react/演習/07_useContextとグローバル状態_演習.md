# 第7章 演習：useContextとグローバル状態

---

## 演習1（基本）：テーマContextを作成しよう

`ThemeContext` を作成し、アプリ全体のテーマ（ライト/ダーク）を切り替えられるようにしてください。

**要件：**
- `createContext` で `ThemeContext` を作成
- `ThemeProvider` コンポーネントで `theme` stateと `toggleTheme` 関数を提供
- 子コンポーネントから `useContext` でテーマを取得
- ヘッダーとコンテンツ領域がテーマに応じてスタイルを変える

<details>
<summary>ヒント</summary>

Contextの3ステップを思い出してください。
1. `createContext()` でContextを作成
2. `Provider` で値を提供
3. `useContext()` で値を取得

```jsx
const ThemeContext = createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  const toggleTheme = () => setTheme(prev => prev === 'light' ? 'dark' : 'light');
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { createContext, useContext, useState } from 'react';

// ========================================
// ステップ1：Contextを作成する
// createContextの引数はデフォルト値（Providerの外で使ったときの値）
// ========================================
const ThemeContext = createContext(null);

// ========================================
// ThemeProvider：テーマの状態と切り替え関数を子孫に提供する
// Providerパターンでは、stateとその操作関数をまとめて
// 1つのオブジェクトとしてvalueに渡すのが一般的
// ========================================
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  // テーマに応じたスタイルオブジェクトも提供する
  const themeStyles = {
    light: { bg: '#ffffff', text: '#333333', accent: '#3498db', cardBg: '#f8f9fa' },
    dark:  { bg: '#1a1a2e', text: '#e0e0e0', accent: '#e94560', cardBg: '#16213e' },
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, styles: themeStyles[theme] }}>
      {children}
    </ThemeContext.Provider>
  );
}

// ========================================
// カスタムフック：useTheme
// useContextを直接使う代わりに、専用のフックを提供する
// こうするとProviderの外で使ったときに分かりやすいエラーを出せる
// ========================================
function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme は ThemeProvider の中で使ってください');
  }
  return context;
}

// ========================================
// ステップ3：子コンポーネントでuseContextを使って値を取得
// props drillingなしでどの階層からでもテーマにアクセスできる
// ========================================
function Header() {
  const { theme, toggleTheme, styles } = useTheme();

  return (
    <header style={{
      backgroundColor: styles.accent,
      color: '#fff',
      padding: '16px 24px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    }}>
      <h1 style={{ margin: 0, fontSize: '20px' }}>My App</h1>
      <button
        onClick={toggleTheme}
        style={{
          padding: '8px 16px',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        {theme === 'light' ? 'ダークモード' : 'ライトモード'}
      </button>
    </header>
  );
}

function ContentArea() {
  const { styles } = useTheme();

  return (
    <main style={{ padding: '24px' }}>
      <div style={{
        backgroundColor: styles.cardBg,
        padding: '20px',
        borderRadius: '8px',
        color: styles.text,
      }}>
        <h2>コンテンツエリア</h2>
        <p>このエリアはテーマに応じてスタイルが変わります。</p>
      </div>
    </main>
  );
}

// ========================================
// Appコンポーネント：ThemeProviderで全体を囲む
// ========================================
function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

function AppContent() {
  const { styles } = useTheme();

  return (
    <div style={{
      backgroundColor: styles.bg,
      minHeight: '100vh',
      transition: 'background-color 0.3s',
    }}>
      <Header />
      <ContentArea />
    </div>
  );
}

export default App;
```

**ポイント：**
- `ThemeProvider` の中にstate管理のロジックを閉じ込めることで、コンポーネントはテーマの「使い方」だけを知ればよい
- `useTheme` カスタムフックを作ると、Providerの外で使ったときにエラーメッセージで問題を特定しやすい
- Context の `value` にはオブジェクトを渡すのが一般的（状態 + 操作関数をまとめて渡す）

</details>

---

## 演習2（基本）：言語切替（i18n）Contextを作ろう

アプリ全体の表示言語を日本語/英語で切り替えられる `LanguageContext` を作成してください。

**要件：**
- 言語データ（翻訳テーブル）を定義
- `LanguageProvider` で現在の言語とテキスト取得関数を提供
- 言語切替ボタンで日本語/英語を切り替え
- 各コンポーネントが翻訳テキストを取得して表示

<details>
<summary>ヒント</summary>

翻訳テーブルはオブジェクトで管理します。

```javascript
const translations = {
  ja: { greeting: "こんにちは", description: "これはサンプルです" },
  en: { greeting: "Hello", description: "This is a sample" },
};
```

`t(key)` のような関数を作って、キーから現在の言語のテキストを返します。

</details>

<details>
<summary>解答例</summary>

```jsx
import { createContext, useContext, useState } from 'react';

// ========================================
// 翻訳テーブル：言語ごとのテキストをオブジェクトで管理
// 実務ではJSONファイルに分離することが多い
// ========================================
const translations = {
  ja: {
    appTitle: "サンプルアプリ",
    greeting: "こんにちは！",
    description: "このアプリは多言語対応のデモです。",
    switchLang: "English",
    profile: "プロフィール",
    name: "名前",
    email: "メールアドレス",
    settings: "設定",
  },
  en: {
    appTitle: "Sample App",
    greeting: "Hello!",
    description: "This app is a multilingual demo.",
    switchLang: "日本語",
    profile: "Profile",
    name: "Name",
    email: "Email",
    settings: "Settings",
  },
};

const LanguageContext = createContext(null);

// ========================================
// LanguageProvider：言語の状態と翻訳関数を提供
// ========================================
function LanguageProvider({ children }) {
  const [lang, setLang] = useState('ja');

  // t関数：キーを渡すと現在の言語のテキストを返す
  const t = (key) => {
    return translations[lang][key] || key;  // 見つからなければキーをそのまま返す
  };

  const toggleLanguage = () => {
    setLang(prev => prev === 'ja' ? 'en' : 'ja');
  };

  return (
    <LanguageContext.Provider value={{ lang, t, toggleLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
}

function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) throw new Error('useLanguage は LanguageProvider の中で使ってください');
  return context;
}

// ========================================
// 子コンポーネント：t関数で翻訳テキストを取得
// ========================================
function Header() {
  const { t, toggleLanguage } = useLanguage();

  return (
    <header style={{
      padding: '16px 24px',
      backgroundColor: '#2c3e50',
      color: '#fff',
      display: 'flex',
      justifyContent: 'space-between',
    }}>
      <h1 style={{ margin: 0 }}>{t('appTitle')}</h1>
      <button onClick={toggleLanguage} style={{ padding: '6px 12px' }}>
        {t('switchLang')}
      </button>
    </header>
  );
}

function ProfileCard() {
  const { t } = useLanguage();

  return (
    <div style={{
      border: '1px solid #ddd',
      borderRadius: '8px',
      padding: '20px',
      margin: '16px 0',
    }}>
      <h3>{t('profile')}</h3>
      <p><strong>{t('name')}:</strong> React 太郎</p>
      <p><strong>{t('email')}:</strong> react@example.com</p>
    </div>
  );
}

function MainContent() {
  const { t } = useLanguage();

  return (
    <main style={{ padding: '24px' }}>
      <h2>{t('greeting')}</h2>
      <p>{t('description')}</p>
      <ProfileCard />
    </main>
  );
}

function App() {
  return (
    <LanguageProvider>
      <Header />
      <MainContent />
    </LanguageProvider>
  );
}

export default App;
```

**ポイント：**
- `t(key)` 関数パターンは実際の国際化（i18n）ライブラリ（`react-i18next` など）と同じ発想です
- 翻訳にないキーが渡されたとき、キーをそのまま返すフォールバックは実務でも一般的です
- Contextで共有するのは「言語」という「グローバルな設定値」であり、Contextに最適なユースケースです

</details>

---

## 演習3（基本）：認証Contextを作ろう

ログイン/ログアウト機能を持つ `AuthContext` を作成し、認証状態に応じてUIを切り替えてください。

**要件：**
- `AuthProvider` でユーザー情報と認証関数を提供
- `login(username, password)` で疑似ログイン
- `logout()` でログアウト
- ログイン状態に応じてヘッダーの表示を切り替え

<details>
<summary>ヒント</summary>

`user` stateが `null` なら未ログイン、オブジェクトならログイン中と判定します。

</details>

<details>
<summary>解答例</summary>

```jsx
import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

// ========================================
// AuthProvider：認証状態とログイン/ログアウト関数を提供
// ========================================
function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");

  // ========================================
  // 疑似ログイン：実際にはAPIへのリクエストになる
  // ここではユーザー名が空でなければログイン成功とする
  // ========================================
  const login = (username, password) => {
    setError("");
    if (!username.trim()) {
      setError("ユーザー名を入力してください");
      return false;
    }
    if (password.length < 4) {
      setError("パスワードは4文字以上です");
      return false;
    }
    // 疑似的にユーザー情報をセット
    setUser({ name: username, email: `${username}@example.com` });
    return true;
  };

  const logout = () => {
    setUser(null);
  };

  // isAuthenticated は user から計算できる派生値
  const isAuthenticated = user !== null;

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, logout, error }}>
      {children}
    </AuthContext.Provider>
  );
}

function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth は AuthProvider の中で使ってください');
  return context;
}

// ========================================
// ログインフォーム
// ========================================
function LoginForm() {
  const { login, error } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const success = login(username, password);
    if (success) {
      setUsername("");
      setPassword("");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{
      maxWidth: '300px',
      margin: '40px auto',
      padding: '24px',
      border: '1px solid #ddd',
      borderRadius: '8px',
    }}>
      <h2>ログイン</h2>
      {error && <p style={{ color: '#e74c3c' }}>{error}</p>}
      <input
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="ユーザー名"
        style={{ width: '100%', padding: '8px', marginBottom: '8px' }}
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="パスワード"
        style={{ width: '100%', padding: '8px', marginBottom: '12px' }}
      />
      <button type="submit" style={{ width: '100%', padding: '10px' }}>ログイン</button>
    </form>
  );
}

// ========================================
// ヘッダー：認証状態に応じて表示を切り替え
// ========================================
function Header() {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <header style={{
      padding: '12px 24px',
      backgroundColor: '#2c3e50',
      color: '#fff',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    }}>
      <h1 style={{ margin: 0, fontSize: '20px' }}>My App</h1>
      {isAuthenticated ? (
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span>ようこそ、{user.name} さん</span>
          <button onClick={logout}>ログアウト</button>
        </div>
      ) : (
        <span>ゲスト</span>
      )}
    </header>
  );
}

// ========================================
// ダッシュボード：ログイン後に表示されるコンテンツ
// ========================================
function Dashboard() {
  const { user } = useAuth();

  return (
    <div style={{ padding: '24px' }}>
      <h2>ダッシュボード</h2>
      <p>{user.name} さんのダッシュボードです。</p>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Header />
      <MainArea />
    </AuthProvider>
  );
}

function MainArea() {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <Dashboard /> : <LoginForm />;
}

export default App;
```

**ポイント：**
- 認証情報は多くのコンポーネントから参照されるため、Contextで共有するのが最適です
- `isAuthenticated` は `user !== null` から計算できる派生値なので、stateにする必要はありません
- 実務では `login` 関数の中でAPI呼び出しを行い、レスポンスのトークンをlocalStorageに保存します

</details>

---

## 演習4（応用）：バグを見つけて修正しよう

以下のコードにはContextに関するバグが2つあります。見つけて修正してください。

```jsx
import { createContext, useContext, useState } from 'react';

const CounterContext = createContext();

function CounterProvider({ children }) {
  const [count, setCount] = useState(0);
  return (
    <CounterContext.Provider value={{ count, setCount }}>
      {children}
    </CounterContext.Provider>
  );
}

function App() {
  return (
    <div>
      <CounterProvider>
        <Display />
      </CounterProvider>
      <Controls />  {/* バグ1 */}
    </div>
  );
}

function Display() {
  const { count } = useContext(CounterContext);
  return <h2>カウント: {count}</h2>;
}

function Controls() {
  const { count, setCount } = useContext(CounterContext);  {/* バグ2 */}
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>+1</button>
      <button onClick={() => setCount(count - 1)}>-1</button>
    </div>
  );
}
```

<details>
<summary>ヒント</summary>

- **バグ1：** `Controls` コンポーネントが `CounterProvider` の外側に配置されている
- **バグ2：** Providerの外で `useContext` を使うと、`undefined` が返る（デフォルト値が `undefined` のため）

</details>

<details>
<summary>解答例</summary>

```jsx
import { createContext, useContext, useState } from 'react';

const CounterContext = createContext();

function CounterProvider({ children }) {
  const [count, setCount] = useState(0);
  return (
    <CounterContext.Provider value={{ count, setCount }}>
      {children}
    </CounterContext.Provider>
  );
}

// ========================================
// 修正1：Controls を CounterProvider の内側に移動
//
// 修正前：Controls が Provider の外側にあったため、
// useContext で値を取得できず undefined エラーが発生していた
//
// Contextの値を使うコンポーネントは、必ず対応する
// Providerの子孫として配置する必要がある
// ========================================
function App() {
  return (
    <div>
      <CounterProvider>
        <Display />
        <Controls />  {/* Providerの中に移動 */}
      </CounterProvider>
    </div>
  );
}

function Display() {
  const { count } = useContext(CounterContext);
  return <h2>カウント: {count}</h2>;
}

// ========================================
// 修正2：関数型更新を使う
//
// 修正前：setCount(count + 1) だと、クロージャの問題で
// 連続クリック時に正しく動かない可能性がある
// 修正後：setCount(prev => prev + 1) で常に最新値を使う
// ========================================
function Controls() {
  const { setCount } = useContext(CounterContext);
  return (
    <div>
      <button onClick={() => setCount(prev => prev + 1)}>+1</button>
      <button onClick={() => setCount(prev => prev - 1)}>-1</button>
    </div>
  );
}

export default App;
```

**バグのまとめ：**
1. **Providerの外でuseContextを使っていた** → Providerの子孫として配置する
2. **関数型更新を使っていなかった** → `setCount(prev => prev + 1)` で最新値を参照する

**追加の改善案：** `useContext` を直接使う代わりにカスタムフックを作り、Providerの外で使ったときに明確なエラーを出すようにすると、バグの発見が早くなります。

</details>

---

## 演習5（応用）：複数のContextを組み合わせよう

テーマ（ライト/ダーク）と認証（ログイン/ログアウト）の2つのContextを組み合わせた小さなアプリを作成してください。

**要件：**
- `ThemeProvider` と `AuthProvider` の2つのProviderを使う
- ログインしていないとテーマ切替ボタンが無効
- ヘッダーにユーザー名とテーマ切替ボタンを表示
- テーマに応じたスタイルでページ全体を描画

<details>
<summary>ヒント</summary>

複数のProviderはネストして使います。順序は機能的な依存関係で決めます。

```jsx
<AuthProvider>
  <ThemeProvider>
    <App />
  </ThemeProvider>
</AuthProvider>
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { createContext, useContext, useState } from 'react';

// ========================================
// Context 1：認証
// ========================================
const AuthContext = createContext(null);

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = (name) => setUser({ name });
  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth は AuthProvider の中で使ってください');
  return ctx;
}

// ========================================
// Context 2：テーマ
// ========================================
const ThemeContext = createContext(null);

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  const toggleTheme = () => setTheme(prev => prev === 'light' ? 'dark' : 'light');

  const colors = {
    light: { bg: '#ffffff', text: '#333', header: '#3498db' },
    dark:  { bg: '#1a1a2e', text: '#eee', header: '#e94560' },
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, colors: colors[theme] }}>
      {children}
    </ThemeContext.Provider>
  );
}

function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme は ThemeProvider の中で使ってください');
  return ctx;
}

// ========================================
// 2つのContextを組み合わせたコンポーネント
// ========================================
function Header() {
  const { user, isAuthenticated, logout } = useAuth();
  const { theme, toggleTheme, colors } = useTheme();

  return (
    <header style={{
      backgroundColor: colors.header,
      color: '#fff',
      padding: '12px 24px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    }}>
      <h1 style={{ margin: 0, fontSize: '20px' }}>My App</h1>
      <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
        {/* ログインしていないとテーマ切替が無効 */}
        <button
          onClick={toggleTheme}
          disabled={!isAuthenticated}
          style={{ opacity: isAuthenticated ? 1 : 0.5, padding: '6px 12px' }}
        >
          {theme === 'light' ? 'ダーク' : 'ライト'}
        </button>
        {isAuthenticated && (
          <>
            <span>{user.name}</span>
            <button onClick={logout} style={{ padding: '6px 12px' }}>ログアウト</button>
          </>
        )}
      </div>
    </header>
  );
}

function LoginArea() {
  const { login } = useAuth();
  const [name, setName] = useState("");

  return (
    <div style={{ padding: '40px', textAlign: 'center' }}>
      <h2>ログイン</h2>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="名前を入力"
        style={{ padding: '8px', marginRight: '8px' }}
      />
      <button onClick={() => name && login(name)} style={{ padding: '8px 16px' }}>
        ログイン
      </button>
    </div>
  );
}

function Dashboard() {
  const { user } = useAuth();
  const { colors } = useTheme();

  return (
    <div style={{ padding: '24px', color: colors.text }}>
      <h2>ダッシュボード</h2>
      <p>{user.name} さん、ようこそ。テーマを切り替えてみてください。</p>
    </div>
  );
}

// ========================================
// App：複数のProviderをネストして組み合わせる
// 外側のProviderの値は内側でも使える
// ========================================
function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <AppContent />
      </ThemeProvider>
    </AuthProvider>
  );
}

function AppContent() {
  const { isAuthenticated } = useAuth();
  const { colors } = useTheme();

  return (
    <div style={{ backgroundColor: colors.bg, minHeight: '100vh' }}>
      <Header />
      {isAuthenticated ? <Dashboard /> : <LoginArea />}
    </div>
  );
}

export default App;
```

**ポイント：**
- 複数のContextを使う場合、Providerはネストして配置します
- Provider の順序に注意：内側の Provider から外側の Context にアクセスできます
- 各Contextは独立した関心事を管理し、必要に応じて組み合わせます
- Providerが多くなりすぎたら「Provider地獄」を避けるために統合を検討します

</details>

---

## 演習6（チャレンジ）：通知システムをContextで作ろう

アプリ全体で使える通知（トースト）システムを `NotificationContext` で作成してください。

**要件：**
- `addNotification(message, type)` で通知を追加（type: "success", "error", "info"）
- 通知は3秒後に自動で消える
- 画面右上に通知を表示
- 複数の通知を同時に表示可能
- 通知を手動で閉じるボタン

<details>
<summary>ヒント</summary>

- 通知は配列で管理します：`[{ id, message, type }]`
- `setTimeout` で3秒後に自動削除します
- 通知の追加には `Date.now()` をIDとして使うと便利です

</details>

<details>
<summary>解答例</summary>

```jsx
import { createContext, useContext, useState, useCallback } from 'react';

const NotificationContext = createContext(null);

// ========================================
// NotificationProvider：通知の状態管理と追加/削除関数を提供
// ========================================
function NotificationProvider({ children }) {
  const [notifications, setNotifications] = useState([]);

  // ========================================
  // 通知を削除する関数
  // ========================================
  const removeNotification = useCallback((id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);

  // ========================================
  // 通知を追加する関数
  // 3秒後に自動で消えるsetTimeoutもセットする
  // ========================================
  const addNotification = useCallback((message, type = 'info') => {
    const id = Date.now();
    const newNotification = { id, message, type };

    setNotifications(prev => [...prev, newNotification]);

    // 3秒後に自動で削除
    setTimeout(() => {
      removeNotification(id);
    }, 3000);
  }, [removeNotification]);

  return (
    <NotificationContext.Provider value={{ addNotification }}>
      {children}
      {/* 通知の表示エリア（右上に固定） */}
      <div style={{
        position: 'fixed',
        top: '16px',
        right: '16px',
        zIndex: 1000,
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
      }}>
        {notifications.map(notification => (
          <NotificationItem
            key={notification.id}
            notification={notification}
            onClose={() => removeNotification(notification.id)}
          />
        ))}
      </div>
    </NotificationContext.Provider>
  );
}

// ========================================
// 通知1件分の表示コンポーネント
// ========================================
function NotificationItem({ notification, onClose }) {
  const typeStyles = {
    success: { bg: '#d4edda', border: '#28a745', text: '#155724' },
    error:   { bg: '#f8d7da', border: '#dc3545', text: '#721c24' },
    info:    { bg: '#d1ecf1', border: '#17a2b8', text: '#0c5460' },
  };

  const style = typeStyles[notification.type] || typeStyles.info;

  return (
    <div style={{
      backgroundColor: style.bg,
      border: `1px solid ${style.border}`,
      color: style.text,
      padding: '12px 16px',
      borderRadius: '6px',
      minWidth: '250px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    }}>
      <span>{notification.message}</span>
      <button
        onClick={onClose}
        style={{
          background: 'none',
          border: 'none',
          color: style.text,
          cursor: 'pointer',
          fontSize: '18px',
          marginLeft: '12px',
        }}
      >
        x
      </button>
    </div>
  );
}

function useNotification() {
  const ctx = useContext(NotificationContext);
  if (!ctx) throw new Error('useNotification は NotificationProvider の中で使ってください');
  return ctx;
}

// ========================================
// 使用例：通知をテストするコンポーネント
// ========================================
function NotificationDemo() {
  const { addNotification } = useNotification();

  return (
    <div style={{ padding: '40px', textAlign: 'center' }}>
      <h2>通知テスト</h2>
      <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
        <button
          onClick={() => addNotification('保存しました！', 'success')}
          style={{ padding: '10px 20px', backgroundColor: '#28a745', color: '#fff', border: 'none', borderRadius: '4px' }}
        >
          成功通知
        </button>
        <button
          onClick={() => addNotification('エラーが発生しました', 'error')}
          style={{ padding: '10px 20px', backgroundColor: '#dc3545', color: '#fff', border: 'none', borderRadius: '4px' }}
        >
          エラー通知
        </button>
        <button
          onClick={() => addNotification('新しいメッセージがあります', 'info')}
          style={{ padding: '10px 20px', backgroundColor: '#17a2b8', color: '#fff', border: 'none', borderRadius: '4px' }}
        >
          情報通知
        </button>
      </div>
    </div>
  );
}

function App() {
  return (
    <NotificationProvider>
      <NotificationDemo />
    </NotificationProvider>
  );
}

export default App;
```

**ポイント：**
- 通知システムはContextの優れたユースケースです。どのコンポーネントからでも `addNotification` を呼べます
- Providerの中にUI（通知表示エリア）を含めることで、コンポーネントは通知の「表示方法」を気にせず「追加」だけすればよくなります
- `useCallback` を使って関数をメモ化しているのは、子コンポーネントへの不要な再レンダリングを防ぐためです（第10章で詳しく学びます）

</details>

---

## 演習7（チャレンジ）：設計を考えよう ― Contextを使うべき？

以下のシナリオについて、Contextを使うべきかどうか判断し、理由を説明してください。

**シナリオA：** フォームの入力値を親と子コンポーネントで共有したい（2階層）

**シナリオB：** ログインユーザーの情報を、ヘッダー、サイドバー、コンテンツ、フッターの4箇所で表示したい

**シナリオC：** リスト内の各アイテムが持つ「展開/折りたたみ」状態を管理したい

**シナリオD：** アプリの「現在のページタイトル」をパンくずリストとブラウザタブの2箇所で使いたい

<details>
<summary>解答例</summary>

### シナリオA：Contextは不要 → propsで十分

```
2階層の場合はpropsで直接渡すのが最もシンプルです。

理由：
- 階層が浅い（2階層）のでprops drillingの問題が発生しない
- フォームの値は局所的な関心事
- Contextを使うとオーバーエンジニアリングになる

推奨：通常のprops渡し、またはstate巻き上げ（lifting state up）
```

### シナリオB：Contextが適切

```
ログインユーザー情報は典型的なContextのユースケースです。

理由：
- 多くのコンポーネント（4箇所以上）で同じデータが必要
- ユーザー情報は「アプリ全体に関わるグローバルな状態」
- propsで渡すと中間コンポーネントが不要なpropsを受け取ることになる

推奨：AuthContextを作成する
```

### シナリオC：Contextは不要 → 各アイテムのローカルstate

```
各アイテムの展開/折りたたみは、それぞれのアイテムの
ローカルな関心事です。

理由：
- 各アイテムの状態は独立している
- 他のコンポーネントがこの状態を知る必要がない
- 各ListItemコンポーネントが自分のstateを持てばよい

推奨：各アイテムコンポーネント内でuseState
```

### シナリオD：場合による → まずpropsを検討、必要ならContext

```
2箇所だけなので、コンポーネントの階層構造によります。

- パンくずリストとブラウザタブが近い階層にある → propsで十分
- 離れた階層にある → Contextが便利

理由：
- 使用箇所が少ない場合、Contextは過剰
- ただしページタイトルは「ルーティング状態」の一部と考えると、
  React Routerと組み合わせて管理するのが自然

推奨：コンポーネント構成を確認し、propsで済むならprops、
済まなければContextを検討する
```

### Contextを使うべきかの判断基準

| 条件 | Context？ |
|------|-----------|
| 2-3階層のprops渡し | 不要（propsで十分） |
| 多くのコンポーネントで同じ値を参照 | 適切 |
| 頻繁に変わる値（入力値など） | 注意（再レンダリング問題） |
| テーマ、認証、言語などの「設定値」 | 最適 |
| リストの各アイテムのローカル状態 | 不要 |

</details>
