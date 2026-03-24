# 第1章：Reactの基本

## この章で学ぶこと

- Reactとは何か、なぜ使うのか
- 開発環境のセットアップ（Vite）
- JSXの基本文法
- コンポーネントの考え方
- 最初のReactアプリを作る

---

## 1. Reactとは？

**React**は、Meta（旧Facebook）が開発したUIライブラリです。Webアプリケーションの「見た目（UI）」を効率的に構築するために使われます。

### Reactの3つの特徴

| 特徴 | 説明 |
|------|------|
| **コンポーネントベース** | UIを小さな部品（コンポーネント）に分割して組み立てる |
| **宣言的UI** | 「どう変更するか」ではなく「何を表示するか」を記述する |
| **仮想DOM** | 効率的にDOMを更新し、高速な描画を実現する |

### 従来のJavaScriptとの違い

```javascript
// 従来のDOM操作（命令的）
const button = document.getElementById('counter-btn');
let count = 0;
button.addEventListener('click', () => {
  count++;
  document.getElementById('display').textContent = `カウント: ${count}`;
});
```

```jsx
// React（宣言的）
function Counter() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <p>カウント: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
}
```

Reactでは「今の状態に応じて何を表示するか」を書くだけで、DOMの更新はReactが自動で行います。

---

## 2. 開発環境のセットアップ

### 必要なもの

- **Node.js**（v18以上推奨）：[https://nodejs.org/](https://nodejs.org/)
- **テキストエディタ**：VS Code推奨
- **ターミナル**（コマンドプロンプト / PowerShell / ターミナル）

### Viteでプロジェクトを作成する

現在のReact開発では **Vite（ヴィート）** を使うのが主流です。

```bash
# プロジェクトを作成
npm create vite@latest my-first-react -- --template react

# プロジェクトフォルダに移動
cd my-first-react

# 依存パッケージをインストール
npm install

# 開発サーバーを起動
npm run dev
```

ブラウザで `http://localhost:5173` を開くと、Reactアプリが表示されます。

### プロジェクトの構造

```
my-first-react/
├── node_modules/      # 依存パッケージ（触らない）
├── public/            # 静的ファイル
├── src/               # ソースコード（ここを編集する）
│   ├── App.jsx        # メインのコンポーネント
│   ├── App.css        # スタイル
│   ├── main.jsx       # エントリーポイント
│   └── index.css      # グローバルスタイル
├── index.html         # HTMLテンプレート
├── package.json       # プロジェクトの設定
└── vite.config.js     # Viteの設定
```

### エントリーポイント（main.jsx）

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

- `ReactDOM.createRoot`：ReactアプリをDOMに接続する
- `<React.StrictMode>`：開発中の問題を検出するラッパー（本番には影響なし）
- `<App />`：最初に表示されるコンポーネント

---

## 3. JSXとは

**JSX（JavaScript XML）** は、JavaScript内にHTMLのような構文を書ける拡張文法です。

### 基本的なJSX

```jsx
function App() {
  return (
    <div>
      <h1>こんにちは、React！</h1>
      <p>これがJSXです。</p>
    </div>
  );
}
```

> JSXはHTMLに似ていますが、JavaScriptです。ブラウザが直接理解できるわけではなく、ビルドツール（Vite）が通常のJavaScriptに変換します。

### JSXのルール

#### ルール1：単一のルート要素を返す

```jsx
// NG：複数のルート要素
function App() {
  return (
    <h1>タイトル</h1>
    <p>説明</p>
  );
}

// OK：divで囲む
function App() {
  return (
    <div>
      <h1>タイトル</h1>
      <p>説明</p>
    </div>
  );
}

// OK：フラグメント（<>...</>）を使う（余計なDOMを追加しない）
function App() {
  return (
    <>
      <h1>タイトル</h1>
      <p>説明</p>
    </>
  );
}
```

#### ルール2：タグは必ず閉じる

```jsx
// HTML では OK だが、JSXでは NG
<img src="photo.jpg">
<br>
<input type="text">

// JSXでは自己閉じタグが必要
<img src="photo.jpg" />
<br />
<input type="text" />
```

#### ルール3：`class`ではなく`className`を使う

```jsx
// NG
<div class="container">

// OK
<div className="container">
```

#### ルール4：JavaScriptの式は `{}` で埋め込む

```jsx
function Greeting() {
  const name = "太郎";
  const age = 25;

  return (
    <div>
      <h1>こんにちは、{name}さん！</h1>
      <p>年齢：{age}歳</p>
      <p>来年は{age + 1}歳ですね。</p>
      <p>現在時刻：{new Date().toLocaleTimeString()}</p>
    </div>
  );
}
```

### JSXに埋め込めるもの・埋め込めないもの

| 埋め込めるもの | 例 |
|---------------|-----|
| 文字列 | `{"Hello"}` |
| 数値 | `{42}` |
| 式・計算 | `{1 + 2}` |
| 関数の戻り値 | `{getName()}` |
| 三項演算子 | `{isOk ? "OK" : "NG"}` |

| 埋め込めないもの | 理由 |
|-----------------|------|
| オブジェクト `{{a: 1}}` | そのまま表示できない |
| if文 | 文（statement）は埋め込めない |
| for文 | 文（statement）は埋め込めない |

---

## 4. コンポーネントの基本

**コンポーネント**は、UIの部品を関数として定義したものです。

### コンポーネントを作る

```jsx
// コンポーネント＝大文字で始まる関数
function Welcome() {
  return <h1>ようこそ！</h1>;
}

// 使い方
function App() {
  return (
    <div>
      <Welcome />
      <Welcome />
      <Welcome />
    </div>
  );
}
```

### コンポーネントの命名ルール

| ルール | 例 |
|--------|-----|
| 必ず大文字で始める | `Welcome`, `UserCard`, `App` |
| パスカルケース（PascalCase） | `TodoList`, `HeaderNav` |
| 小文字で始めるとHTML要素と見なされる | `div`, `span`, `p` |

### コンポーネントをファイルに分割する

実際の開発では、コンポーネントを別ファイルに分けます。

```jsx
// src/components/Welcome.jsx
function Welcome() {
  return <h1>ようこそ！</h1>;
}

export default Welcome;
```

```jsx
// src/App.jsx
import Welcome from './components/Welcome';

function App() {
  return (
    <div>
      <Welcome />
    </div>
  );
}

export default App;
```

---

## 5. スタイルの適用

### インラインスタイル

JSXではstyle属性にオブジェクトを渡します。プロパティ名はキャメルケースです。

```jsx
function StyledBox() {
  const boxStyle = {
    backgroundColor: '#3498db',
    color: 'white',
    padding: '20px',
    borderRadius: '8px',
    fontSize: '18px',
  };

  return <div style={boxStyle}>スタイル付きのボックス</div>;
}
```

### CSSファイルを使う

```css
/* src/App.css */
.card {
  background-color: #f0f0f0;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

```jsx
// src/App.jsx
import './App.css';

function App() {
  return <div className="card">カードコンポーネント</div>;
}
```

---

## 6. 実践：自己紹介カードを作る

ここまでの知識を使って、簡単な自己紹介カードを作ってみましょう。

```jsx
// src/App.jsx
import './App.css';

function ProfileCard() {
  const profile = {
    name: "田中太郎",
    age: 28,
    job: "フロントエンドエンジニア",
    hobbies: "読書、プログラミング、映画鑑賞",
  };

  const cardStyle = {
    maxWidth: '400px',
    margin: '40px auto',
    padding: '24px',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
    backgroundColor: '#ffffff',
    fontFamily: 'sans-serif',
  };

  const nameStyle = {
    fontSize: '24px',
    color: '#2c3e50',
    marginBottom: '12px',
  };

  return (
    <div style={cardStyle}>
      <h2 style={nameStyle}>{profile.name}</h2>
      <p>年齢：{profile.age}歳</p>
      <p>職業：{profile.job}</p>
      <p>趣味：{profile.hobbies}</p>
    </div>
  );
}

function App() {
  return (
    <div>
      <h1 style={{ textAlign: 'center' }}>自己紹介</h1>
      <ProfileCard />
    </div>
  );
}

export default App;
```

---

## まとめ

| 項目 | ポイント |
|------|---------|
| Reactとは | UIを効率的に構築するためのライブラリ |
| セットアップ | `npm create vite@latest` でプロジェクト作成 |
| JSX | JavaScript内にHTMLライクな構文を書ける |
| JSXのルール | 単一ルート要素、タグを閉じる、`className`を使う |
| `{}` | JSX内でJavaScriptの式を埋め込む |
| コンポーネント | 大文字で始まる関数。UIの部品を定義する |
| ファイル分割 | `export default` と `import` で分離 |
| スタイル | インラインスタイル（オブジェクト）またはCSSファイル |

### 次の章では

コンポーネントにデータを渡す「**props**」について学びます。これにより、同じコンポーネントを異なるデータで再利用できるようになります。

---

## 動作サンプル

この章の概念を実装した完全なサンプルコードは `サンプル/01_HelloReact.jsx` にあります。JSXの基本、コンポーネントの作成、スタイルの適用を実際に動かして確認できます。
