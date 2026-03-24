# 第2章：コンポーネントとprops

## この章で学ぶこと

- propsの仕組みと使い方
- propsでデータを渡す方法
- デフォルト値の設定
- childrenの活用
- コンポーネント設計の考え方

---

## 1. propsとは？

**props（プロップス）** は、親コンポーネントから子コンポーネントにデータを渡す仕組みです。HTML属性のように書きます。

```jsx
// 親から子へデータを渡す
function App() {
  return <Greeting name="太郎" />;
}

// 子コンポーネントでデータを受け取る
function Greeting(props) {
  return <h1>こんにちは、{props.name}さん！</h1>;
}
```

### propsの特徴

| 特徴 | 説明 |
|------|------|
| **親→子の一方通行** | データは親から子へのみ流れる |
| **読み取り専用** | 子コンポーネント内でpropsを変更してはいけない |
| **何でも渡せる** | 文字列、数値、配列、オブジェクト、関数、JSXも渡せる |

---

## 2. propsの基本的な使い方

### 分割代入で受け取る（推奨）

```jsx
// 分割代入を使うとスッキリ書ける
function Greeting({ name }) {
  return <h1>こんにちは、{name}さん！</h1>;
}

// 複数のpropsを受け取る
function UserCard({ name, age, email }) {
  return (
    <div className="card">
      <h2>{name}</h2>
      <p>年齢：{age}歳</p>
      <p>メール：{email}</p>
    </div>
  );
}

// 使い方
function App() {
  return (
    <UserCard name="田中太郎" age={28} email="taro@example.com" />
  );
}
```

### さまざまな型のデータを渡す

```jsx
function ProductCard({ name, price, inStock, tags, onBuy }) {
  return (
    <div>
      <h3>{name}</h3>
      <p>価格：¥{price.toLocaleString()}</p>
      <p>在庫：{inStock ? "あり" : "なし"}</p>
      <p>タグ：{tags.join(", ")}</p>
      <button onClick={onBuy}>購入する</button>
    </div>
  );
}

function App() {
  const handleBuy = () => {
    alert("購入しました！");
  };

  return (
    <ProductCard
      name="React入門書"          {/* 文字列 */}
      price={2980}                {/* 数値 */}
      inStock={true}              {/* 真偽値 */}
      tags={["React", "初心者"]}  {/* 配列 */}
      onBuy={handleBuy}           {/* 関数 */}
    />
  );
}
```

> **ポイント**：文字列以外の値は `{}` で囲みます。文字列だけは `""` でもOKです。

---

## 3. デフォルト値の設定

propsが渡されなかった場合の初期値を設定できます。

### 方法1：分割代入のデフォルト値（推奨）

```jsx
function Button({ text = "クリック", color = "blue", size = "medium" }) {
  const sizeMap = {
    small: '12px',
    medium: '16px',
    large: '20px',
  };

  return (
    <button style={{ backgroundColor: color, fontSize: sizeMap[size] }}>
      {text}
    </button>
  );
}

// 全てデフォルト値が使われる
<Button />

// textだけ上書き
<Button text="送信" />

// 全て指定
<Button text="削除" color="red" size="large" />
```

### 方法2：defaultPropsプロパティ

```jsx
function Badge({ label, count }) {
  return (
    <span>
      {label}: {count}
    </span>
  );
}

Badge.defaultProps = {
  label: "通知",
  count: 0,
};
```

> **注意**：`defaultProps`は将来的に非推奨になる予定です。分割代入のデフォルト値を使いましょう。

---

## 4. children

`children`は特別なpropsで、コンポーネントの開始タグと終了タグの間に書かれた内容を受け取ります。

### 基本的なchildren

```jsx
function Card({ children }) {
  return (
    <div style={{
      border: '1px solid #ddd',
      borderRadius: '8px',
      padding: '16px',
      margin: '8px',
    }}>
      {children}
    </div>
  );
}

function App() {
  return (
    <div>
      <Card>
        <h2>プロフィール</h2>
        <p>名前：田中太郎</p>
      </Card>

      <Card>
        <h2>お知らせ</h2>
        <p>新機能がリリースされました！</p>
      </Card>
    </div>
  );
}
```

### childrenを使ったレイアウトコンポーネント

```jsx
function PageLayout({ children }) {
  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      {children}
    </div>
  );
}

function Header({ children }) {
  return (
    <header style={{
      backgroundColor: '#2c3e50',
      color: 'white',
      padding: '16px',
    }}>
      {children}
    </header>
  );
}

function Footer({ children }) {
  return (
    <footer style={{
      borderTop: '1px solid #ddd',
      padding: '16px',
      textAlign: 'center',
      color: '#666',
    }}>
      {children}
    </footer>
  );
}

function App() {
  return (
    <PageLayout>
      <Header>
        <h1>マイサイト</h1>
      </Header>
      <main>
        <p>メインコンテンツ</p>
      </main>
      <Footer>
        <p>&copy; 2026 マイサイト</p>
      </Footer>
    </PageLayout>
  );
}
```

### propsとchildrenの組み合わせ

```jsx
function Alert({ type = "info", children }) {
  const colors = {
    info: { bg: '#d1ecf1', border: '#bee5eb', text: '#0c5460' },
    success: { bg: '#d4edda', border: '#c3e6cb', text: '#155724' },
    warning: { bg: '#fff3cd', border: '#ffeeba', text: '#856404' },
    error: { bg: '#f8d7da', border: '#f5c6cb', text: '#721c24' },
  };

  const style = {
    backgroundColor: colors[type].bg,
    border: `1px solid ${colors[type].border}`,
    color: colors[type].text,
    padding: '12px 16px',
    borderRadius: '4px',
    margin: '8px 0',
  };

  return <div style={style}>{children}</div>;
}

function App() {
  return (
    <div>
      <Alert type="success">保存しました！</Alert>
      <Alert type="error">エラーが発生しました。</Alert>
      <Alert type="warning">入力内容を確認してください。</Alert>
      <Alert>お知らせ：メンテナンス予定があります。</Alert>
    </div>
  );
}
```

---

## 5. propsのスプレッド構文

オブジェクトのプロパティをまとめてpropsとして渡せます。

```jsx
function UserProfile({ name, age, location, bio }) {
  return (
    <div>
      <h2>{name}（{age}歳）</h2>
      <p>居住地：{location}</p>
      <p>{bio}</p>
    </div>
  );
}

function App() {
  const userData = {
    name: "鈴木花子",
    age: 32,
    location: "東京",
    bio: "Webエンジニアです。Reactが好きです。",
  };

  // スプレッド構文で一括渡し
  return <UserProfile {...userData} />;

  // 上の書き方は以下と同じ意味
  // return <UserProfile name={userData.name} age={userData.age}
  //   location={userData.location} bio={userData.bio} />;
}
```

---

## 6. コンポーネント設計のコツ

### コンポーネント分割の考え方

```jsx
// 分割前：全部App.jsxに書いてしまった例
function App() {
  return (
    <div>
      <header>
        <h1>ショッピングサイト</h1>
        <nav>
          <a href="/">ホーム</a>
          <a href="/products">商品一覧</a>
          <a href="/cart">カート(3)</a>
        </nav>
      </header>
      <main>
        <div className="product-card">
          <img src="item1.jpg" alt="商品1" />
          <h3>商品名1</h3>
          <p>¥1,000</p>
        </div>
        <div className="product-card">
          <img src="item2.jpg" alt="商品2" />
          <h3>商品名2</h3>
          <p>¥2,000</p>
        </div>
      </main>
    </div>
  );
}
```

```jsx
// 分割後：コンポーネントに分けた例

function NavBar({ cartCount }) {
  return (
    <header>
      <h1>ショッピングサイト</h1>
      <nav>
        <a href="/">ホーム</a>
        <a href="/products">商品一覧</a>
        <a href="/cart">カート({cartCount})</a>
      </nav>
    </header>
  );
}

function ProductCard({ image, name, price }) {
  return (
    <div className="product-card">
      <img src={image} alt={name} />
      <h3>{name}</h3>
      <p>¥{price.toLocaleString()}</p>
    </div>
  );
}

function App() {
  return (
    <div>
      <NavBar cartCount={3} />
      <main>
        <ProductCard image="item1.jpg" name="商品名1" price={1000} />
        <ProductCard image="item2.jpg" name="商品名2" price={2000} />
      </main>
    </div>
  );
}
```

### 分割の判断基準

| 基準 | 説明 |
|------|------|
| **繰り返し** | 同じ構造が複数回出てくる → コンポーネント化 |
| **独立性** | 独立した機能を持つ部分 → コンポーネント化 |
| **再利用性** | 他のページでも使いそう → コンポーネント化 |
| **複雑さ** | 1つのコンポーネントが100行超 → 分割を検討 |

---

## 7. 実践：商品リストページ

```jsx
// src/components/ProductCard.jsx
function ProductCard({ name, price, description, image }) {
  const cardStyle = {
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    overflow: 'hidden',
    maxWidth: '300px',
  };

  const imageStyle = {
    width: '100%',
    height: '200px',
    objectFit: 'cover',
    backgroundColor: '#f0f0f0',
  };

  const contentStyle = {
    padding: '16px',
  };

  const priceStyle = {
    fontSize: '20px',
    fontWeight: 'bold',
    color: '#e74c3c',
  };

  return (
    <div style={cardStyle}>
      <img src={image} alt={name} style={imageStyle} />
      <div style={contentStyle}>
        <h3>{name}</h3>
        <p>{description}</p>
        <p style={priceStyle}>¥{price.toLocaleString()}</p>
      </div>
    </div>
  );
}

export default ProductCard;
```

```jsx
// src/components/Badge.jsx
function Badge({ text, color = "#3498db" }) {
  const style = {
    display: 'inline-block',
    backgroundColor: color,
    color: 'white',
    padding: '2px 8px',
    borderRadius: '12px',
    fontSize: '12px',
    marginRight: '4px',
  };

  return <span style={style}>{text}</span>;
}

export default Badge;
```

```jsx
// src/App.jsx
import ProductCard from './components/ProductCard';

function App() {
  return (
    <div style={{ padding: '20px' }}>
      <h1>商品一覧</h1>
      <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
        <ProductCard
          name="React入門ガイド"
          price={2980}
          description="初心者でもわかりやすいReact学習本"
          image="https://via.placeholder.com/300x200"
        />
        <ProductCard
          name="JavaScript完全ガイド"
          price={3980}
          description="JSの基礎から応用まで網羅"
          image="https://via.placeholder.com/300x200"
        />
        <ProductCard
          name="CSSデザイン集"
          price={1980}
          description="実践的なCSSテクニック100選"
          image="https://via.placeholder.com/300x200"
        />
      </div>
    </div>
  );
}

export default App;
```

---

## まとめ

| 項目 | ポイント |
|------|---------|
| props | 親→子へデータを渡す仕組み。読み取り専用 |
| 分割代入 | `function Comp({ name, age })` で受け取るのが主流 |
| データ型 | 文字列、数値、配列、オブジェクト、関数など何でも渡せる |
| デフォルト値 | `{ name = "ゲスト" }` のように設定できる |
| children | タグの間の内容を受け取る特別なprops |
| スプレッド構文 | `{...obj}` でオブジェクトをまとめて渡せる |
| 設計 | 繰り返し・独立性・再利用性を基準に分割する |

### 次の章では

コンポーネントの内部状態を管理する「**state**」と、ユーザー操作を扱う「**イベント処理**」を学びます。

---

## 動作サンプル

この章の概念を実装した完全なサンプルコードは `サンプル/02_ProfileCard.jsx` にあります。propsの受け渡し、デフォルト値、childrenの活用を実際に動かして確認できます。
