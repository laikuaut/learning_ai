# 第2章 演習：コンポーネントとprops

---

## 演習1（基本）：propsで名前を渡そう

`Greeting` コンポーネントを作成し、`name` propsを受け取って「こんにちは、〇〇さん！」と表示してください。3つの異なる名前で呼び出しましょう。

<details>
<summary>ヒント</summary>

コンポーネントの引数を `{ name }` と分割代入で受け取ります。呼び出し側では `<Greeting name="太郎" />` のように渡します。

</details>

<details>
<summary>解答例</summary>

```jsx
function Greeting({ name }) {
  return <p>こんにちは、{name}さん！</p>;
}

function App() {
  return (
    <div>
      <Greeting name="太郎" />
      <Greeting name="花子" />
      <Greeting name="次郎" />
    </div>
  );
}

export default App;
```

</details>

---

## 演習2（基本）：複数のpropsを渡そう

`UserCard` コンポーネントを作成し、`name`、`age`、`email` の3つのpropsを受け取って表示してください。

<details>
<summary>ヒント</summary>

複数のpropsは `{ name, age, email }` のようにまとめて分割代入できます。

</details>

<details>
<summary>解答例</summary>

```jsx
function UserCard({ name, age, email }) {
  return (
    <div style={{
      border: '1px solid #ddd',
      borderRadius: '8px',
      padding: '16px',
      margin: '8px',
    }}>
      <h3>{name}</h3>
      <p>年齢：{age}歳</p>
      <p>メール：{email}</p>
    </div>
  );
}

function App() {
  return (
    <div>
      <UserCard name="田中太郎" age={28} email="tanaka@example.com" />
      <UserCard name="鈴木花子" age={32} email="suzuki@example.com" />
    </div>
  );
}

export default App;
```

</details>

---

## 演習3（基本）：デフォルト値を設定しよう

`Button` コンポーネントを作成し、`text`（デフォルト：「クリック」）と `color`（デフォルト：「#3498db」）のpropsを受け取るようにしてください。propsを渡した場合と渡さない場合の両方で動作確認しましょう。

<details>
<summary>ヒント</summary>

分割代入のデフォルト値は `{ text = "クリック", color = "#3498db" }` のように書きます。

</details>

<details>
<summary>解答例</summary>

```jsx
function Button({ text = "クリック", color = "#3498db" }) {
  return (
    <button style={{
      backgroundColor: color,
      color: 'white',
      padding: '8px 24px',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
      margin: '4px',
      fontSize: '16px',
    }}>
      {text}
    </button>
  );
}

function App() {
  return (
    <div style={{ padding: '20px' }}>
      <Button />
      <Button text="送信" />
      <Button text="削除" color="#e74c3c" />
      <Button text="成功" color="#27ae60" />
    </div>
  );
}

export default App;
```

</details>

---

## 演習4（基本）：childrenを使おう

`Card` コンポーネントを作成し、`children` を使って任意のコンテンツを表示できるようにしてください。枠線と角丸のあるカードスタイルを適用しましょう。

<details>
<summary>ヒント</summary>

`children` はタグの中に書いた内容を受け取る特別なpropsです。`<Card><p>内容</p></Card>` のように使います。

</details>

<details>
<summary>解答例</summary>

```jsx
function Card({ children }) {
  return (
    <div style={{
      border: '1px solid #e0e0e0',
      borderRadius: '12px',
      padding: '20px',
      margin: '12px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    }}>
      {children}
    </div>
  );
}

function App() {
  return (
    <div>
      <Card>
        <h2>お知らせ</h2>
        <p>新機能がリリースされました。</p>
      </Card>
      <Card>
        <h2>プロフィール</h2>
        <p>名前：田中太郎</p>
        <p>職業：エンジニア</p>
      </Card>
    </div>
  );
}

export default App;
```

</details>

---

## 演習5（基本）：数値や真偽値をpropsで渡そう

`PriceTag` コンポーネントを作成し、`name`（文字列）、`price`（数値）、`onSale`（真偽値）を受け取って表示してください。セール中なら「SALE!」と表示してください。

<details>
<summary>ヒント</summary>

数値は `price={1000}`、真偽値は `onSale={true}` のように `{}` で渡します。条件付き表示は `{onSale && <span>SALE!</span>}` です。

</details>

<details>
<summary>解答例</summary>

```jsx
function PriceTag({ name, price, onSale }) {
  return (
    <div style={{
      display: 'inline-block',
      border: '1px solid #ddd',
      padding: '12px',
      margin: '8px',
      borderRadius: '8px',
      position: 'relative',
    }}>
      {onSale && (
        <span style={{
          backgroundColor: '#e74c3c',
          color: 'white',
          padding: '2px 8px',
          borderRadius: '4px',
          fontSize: '12px',
          position: 'absolute',
          top: '-8px',
          right: '-8px',
        }}>
          SALE!
        </span>
      )}
      <p style={{ fontWeight: 'bold' }}>{name}</p>
      <p style={{ color: onSale ? '#e74c3c' : '#333', fontSize: '20px' }}>
        ¥{price.toLocaleString()}
      </p>
    </div>
  );
}

function App() {
  return (
    <div style={{ padding: '20px' }}>
      <PriceTag name="Tシャツ" price={2980} onSale={true} />
      <PriceTag name="ジーンズ" price={5980} onSale={false} />
      <PriceTag name="スニーカー" price={8900} onSale={true} />
    </div>
  );
}

export default App;
```

</details>

---

## 演習6（応用）：propsとchildrenを組み合わせたAlertコンポーネント

`Alert` コンポーネントを作成してください。

**要件：**
- `type` props（`"info"`, `"success"`, `"warning"`, `"error"`）で色を切り替える
- `title` propsでタイトルを表示する
- `children` で詳細メッセージを表示する
- typeに応じて背景色を変える

<details>
<summary>ヒント</summary>

typeごとの色をオブジェクトで定義しておくと管理しやすいです。

```javascript
const styles = {
  info: { bg: '#d1ecf1', text: '#0c5460' },
  success: { bg: '#d4edda', text: '#155724' },
  // ...
};
```

</details>

<details>
<summary>解答例</summary>

```jsx
function Alert({ type = "info", title, children }) {
  const colorMap = {
    info:    { bg: '#d1ecf1', border: '#bee5eb', text: '#0c5460' },
    success: { bg: '#d4edda', border: '#c3e6cb', text: '#155724' },
    warning: { bg: '#fff3cd', border: '#ffeeba', text: '#856404' },
    error:   { bg: '#f8d7da', border: '#f5c6cb', text: '#721c24' },
  };

  const colors = colorMap[type];

  return (
    <div style={{
      backgroundColor: colors.bg,
      border: `1px solid ${colors.border}`,
      color: colors.text,
      padding: '16px',
      borderRadius: '4px',
      margin: '8px 0',
    }}>
      {title && <strong style={{ display: 'block', marginBottom: '4px' }}>{title}</strong>}
      {children}
    </div>
  );
}

function App() {
  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <Alert type="success" title="保存完了">
        データが正常に保存されました。
      </Alert>
      <Alert type="error" title="エラー">
        接続に失敗しました。再度お試しください。
      </Alert>
      <Alert type="warning">
        この操作は取り消せません。
      </Alert>
      <Alert type="info" title="お知らせ">
        明日メンテナンスを実施します。
      </Alert>
    </div>
  );
}

export default App;
```

</details>

---

## 演習7（応用）：スプレッド構文でpropsを渡そう

ユーザーデータのオブジェクトを作成し、スプレッド構文（`{...obj}`）を使ってpropsとして渡してください。

**データ例：**
```javascript
const user = {
  name: "山田花子",
  age: 30,
  location: "大阪",
  bio: "デザイナーです。UIデザインが得意です。",
};
```

<details>
<summary>ヒント</summary>

`<UserProfile {...user} />` は `<UserProfile name={user.name} age={user.age} ... />` と同じ意味になります。

</details>

<details>
<summary>解答例</summary>

```jsx
function UserProfile({ name, age, location, bio }) {
  return (
    <div style={{
      maxWidth: '400px',
      margin: '20px auto',
      padding: '20px',
      border: '1px solid #e0e0e0',
      borderRadius: '8px',
    }}>
      <h2>{name}（{age}歳）</h2>
      <p>居住地：{location}</p>
      <p>{bio}</p>
    </div>
  );
}

function App() {
  const user1 = {
    name: "山田花子",
    age: 30,
    location: "大阪",
    bio: "デザイナーです。UIデザインが得意です。",
  };

  const user2 = {
    name: "田中太郎",
    age: 28,
    location: "東京",
    bio: "フロントエンドエンジニアです。",
  };

  return (
    <div>
      <UserProfile {...user1} />
      <UserProfile {...user2} />
    </div>
  );
}

export default App;
```

</details>

---

## 演習8（応用）：関数をpropsとして渡そう

`ActionButton` コンポーネントを作成し、`onAction` propsとしてクリック時の処理を親から渡してください。

**要件：**
- `ActionButton` は `label` と `onAction` を受け取る
- 3つのボタンを作り、それぞれ異なるalertメッセージを表示する

<details>
<summary>ヒント</summary>

関数もpropsとして渡せます。`<ActionButton onAction={() => alert("Hello")} />` のように渡し、子では `onClick={onAction}` で使います。

</details>

<details>
<summary>解答例</summary>

```jsx
function ActionButton({ label, onAction, color = "#3498db" }) {
  return (
    <button
      onClick={onAction}
      style={{
        backgroundColor: color,
        color: 'white',
        padding: '10px 20px',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        margin: '4px',
        fontSize: '14px',
      }}
    >
      {label}
    </button>
  );
}

function App() {
  const handleSave = () => alert("保存しました！");
  const handleDelete = () => alert("削除しました！");
  const handleShare = () => alert("共有リンクをコピーしました！");

  return (
    <div style={{ padding: '20px' }}>
      <h2>アクションボタン</h2>
      <ActionButton label="保存" onAction={handleSave} color="#27ae60" />
      <ActionButton label="削除" onAction={handleDelete} color="#e74c3c" />
      <ActionButton label="共有" onAction={handleShare} color="#8e44ad" />
    </div>
  );
}

export default App;
```

</details>

---

## 演習9（チャレンジ）：レイアウトコンポーネントを設計しよう

以下の3つのレイアウトコンポーネントを作成し、組み合わせてWebページの骨組みを作ってください。

- `PageWrapper` - ページ全体のコンテナ（最大幅960px、中央寄せ）
- `Section` - セクション（`title` propsとchildren）
- `TwoColumn` - 2カラムレイアウト（`left` と `right` をpropsで受け取る）

<details>
<summary>ヒント</summary>

`TwoColumn` は `left` と `right` にJSXを渡します。

```jsx
<TwoColumn
  left={<p>左側の内容</p>}
  right={<p>右側の内容</p>}
/>
```

2カラムのレイアウトは `display: 'flex'` で実現できます。

</details>

<details>
<summary>解答例</summary>

```jsx
function PageWrapper({ children }) {
  return (
    <div style={{
      maxWidth: '960px',
      margin: '0 auto',
      padding: '20px',
      fontFamily: 'sans-serif',
    }}>
      {children}
    </div>
  );
}

function Section({ title, children }) {
  return (
    <section style={{ marginBottom: '32px' }}>
      <h2 style={{
        borderBottom: '2px solid #3498db',
        paddingBottom: '8px',
        marginBottom: '16px',
      }}>
        {title}
      </h2>
      {children}
    </section>
  );
}

function TwoColumn({ left, right }) {
  return (
    <div style={{ display: 'flex', gap: '24px' }}>
      <div style={{ flex: 1 }}>{left}</div>
      <div style={{ flex: 1 }}>{right}</div>
    </div>
  );
}

function App() {
  return (
    <PageWrapper>
      <h1>マイポートフォリオ</h1>

      <Section title="自己紹介">
        <p>Webエンジニアの田中太郎です。React開発が得意です。</p>
      </Section>

      <Section title="スキルと経歴">
        <TwoColumn
          left={
            <div>
              <h3>スキル</h3>
              <ul>
                <li>React / Next.js</li>
                <li>TypeScript</li>
                <li>Node.js</li>
              </ul>
            </div>
          }
          right={
            <div>
              <h3>経歴</h3>
              <ul>
                <li>2020年 Web制作会社入社</li>
                <li>2022年 フリーランスとして独立</li>
                <li>2024年 スタートアップにジョイン</li>
              </ul>
            </div>
          }
        />
      </Section>

      <Section title="お問い合わせ">
        <p>お気軽にご連絡ください。</p>
      </Section>
    </PageWrapper>
  );
}

export default App;
```

</details>

---

## 演習10（チャレンジ）：商品カタログページを作ろう

以下のコンポーネントを組み合わせて、商品カタログページを作成してください。

**作成するコンポーネント：**
1. `PageHeader` - ページタイトルと説明文を表示
2. `ProductCard` - 商品画像、名前、価格、説明を表示
3. `Badge` - カテゴリバッジ（色付きラベル）
4. `ProductGrid` - 商品カードをグリッド表示するレイアウト

**商品データ（3件以上）** を配列で用意し、`map` で表示してください。

<details>
<summary>ヒント</summary>

- `ProductGrid` は `children` を使って、flexまたはgridでレイアウトします
- `Badge` は `label` と `color` を受け取ります
- `ProductCard` の中で `Badge` を使います

</details>

<details>
<summary>解答例</summary>

```jsx
function PageHeader({ title, description }) {
  return (
    <div style={{ textAlign: 'center', marginBottom: '32px' }}>
      <h1 style={{ fontSize: '32px', margin: '0 0 8px 0' }}>{title}</h1>
      <p style={{ color: '#666', fontSize: '16px' }}>{description}</p>
    </div>
  );
}

function Badge({ label, color = "#3498db" }) {
  return (
    <span style={{
      display: 'inline-block',
      backgroundColor: color,
      color: 'white',
      padding: '2px 10px',
      borderRadius: '12px',
      fontSize: '12px',
      marginRight: '4px',
    }}>
      {label}
    </span>
  );
}

function ProductCard({ name, price, description, category, categoryColor, image }) {
  return (
    <div style={{
      border: '1px solid #e0e0e0',
      borderRadius: '12px',
      overflow: 'hidden',
      backgroundColor: '#fff',
    }}>
      <div style={{
        height: '160px',
        backgroundColor: '#f5f5f5',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '48px',
      }}>
        {image}
      </div>
      <div style={{ padding: '16px' }}>
        <Badge label={category} color={categoryColor} />
        <h3 style={{ margin: '8px 0 4px 0' }}>{name}</h3>
        <p style={{ color: '#666', fontSize: '14px' }}>{description}</p>
        <p style={{ fontSize: '20px', fontWeight: 'bold', color: '#e74c3c' }}>
          ¥{price.toLocaleString()}
        </p>
      </div>
    </div>
  );
}

function ProductGrid({ children }) {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
      gap: '20px',
    }}>
      {children}
    </div>
  );
}

function App() {
  const products = [
    { id: 1, name: "ワイヤレスイヤホン", price: 12800, description: "高音質のBluetooth対応", category: "電子機器", categoryColor: "#3498db", image: "🎧" },
    { id: 2, name: "レザーバッグ", price: 29800, description: "上質な本革を使用", category: "ファッション", categoryColor: "#e67e22", image: "👜" },
    { id: 3, name: "観葉植物セット", price: 4980, description: "初心者向け3点セット", category: "インテリア", categoryColor: "#27ae60", image: "🌿" },
    { id: 4, name: "コーヒーメーカー", price: 8980, description: "全自動ドリップ式", category: "キッチン", categoryColor: "#8e44ad", image: "☕" },
  ];

  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '20px' }}>
      <PageHeader
        title="商品カタログ"
        description="厳選されたアイテムをお届けします"
      />
      <ProductGrid>
        {products.map(product => (
          <ProductCard key={product.id} {...product} />
        ))}
      </ProductGrid>
    </div>
  );
}

export default App;
```

</details>
