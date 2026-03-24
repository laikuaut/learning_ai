# 第1章 演習：Reactの基本

---

## 演習1（基本）：JSXで自己紹介を表示しよう

変数に名前と年齢を格納し、JSXの `{}` を使って画面に表示するコンポーネントを作成してください。

**要件：**
- `name` と `age` を変数に格納する
- `<h1>` で名前、`<p>` で年齢を表示する

<details>
<summary>ヒント</summary>

JSX内でJavaScriptの変数を表示するには `{変数名}` を使います。

</details>

<details>
<summary>解答例</summary>

```jsx
function SelfIntro() {
  const name = "田中太郎";
  const age = 25;

  return (
    <div>
      <h1>名前：{name}</h1>
      <p>年齢：{age}歳</p>
    </div>
  );
}

export default SelfIntro;
```

</details>

---

## 演習2（基本）：フラグメントを使おう

以下のコードはエラーになります。フラグメント（`<>...</>`）を使って修正してください。

```jsx
function TwoHeadings() {
  return (
    <h1>見出し1</h1>
    <h2>見出し2</h2>
  );
}
```

<details>
<summary>ヒント</summary>

JSXは単一のルート要素を返す必要があります。余計なDOMを追加したくない場合は `<>...</>` で囲みます。

</details>

<details>
<summary>解答例</summary>

```jsx
function TwoHeadings() {
  return (
    <>
      <h1>見出し1</h1>
      <h2>見出し2</h2>
    </>
  );
}

export default TwoHeadings;
```

</details>

---

## 演習3（基本）：計算結果を表示しよう

商品の `price`（税抜き価格）を変数に持ち、税込み価格（10%）を計算してJSXに表示するコンポーネントを作ってください。

**要件：**
- 税抜き価格と税込み価格の両方を表示する
- `toLocaleString()` で3桁カンマ区切りにする

<details>
<summary>ヒント</summary>

`{}` の中で計算式を書けます。例：`{price * 1.1}`。`Math.floor()` で小数点を切り捨てるとより正確です。

</details>

<details>
<summary>解答例</summary>

```jsx
function PriceDisplay() {
  const price = 19800;
  const taxIncluded = Math.floor(price * 1.1);

  return (
    <div>
      <p>税抜き価格：¥{price.toLocaleString()}</p>
      <p>税込み価格：¥{taxIncluded.toLocaleString()}</p>
    </div>
  );
}

export default PriceDisplay;
```

</details>

---

## 演習4（基本）：コンポーネントを作って再利用しよう

`Greeting` コンポーネントを作成し、`App` コンポーネント内で3回呼び出してください。

<details>
<summary>ヒント</summary>

コンポーネントは大文字で始まる関数です。`<Greeting />` のように呼び出します。

</details>

<details>
<summary>解答例</summary>

```jsx
function Greeting() {
  return <p>こんにちは、Reactの世界へようこそ！</p>;
}

function App() {
  return (
    <div>
      <Greeting />
      <Greeting />
      <Greeting />
    </div>
  );
}

export default App;
```

</details>

---

## 演習5（基本）：インラインスタイルを適用しよう

以下の条件でスタイル付きのボックスを作成してください。

**スタイル要件：**
- 背景色：`#3498db`
- 文字色：白
- パディング：`20px`
- 角丸：`8px`
- フォントサイズ：`18px`

<details>
<summary>ヒント</summary>

JSXのインラインスタイルはオブジェクトで指定します。CSSのプロパティ名はキャメルケース（`backgroundColor`）に変換します。

</details>

<details>
<summary>解答例</summary>

```jsx
function StyledBox() {
  const style = {
    backgroundColor: '#3498db',
    color: 'white',
    padding: '20px',
    borderRadius: '8px',
    fontSize: '18px',
  };

  return <div style={style}>スタイル付きのボックスです</div>;
}

export default StyledBox;
```

</details>

---

## 演習6（応用）：プロフィールカードコンポーネント

オブジェクトにプロフィール情報を格納し、カード形式で表示するコンポーネントを作成してください。

**要件：**
- オブジェクトに `name`, `job`, `hobby`, `motto` を含める
- 見やすいカードレイアウトにスタイルを適用する
- 各情報にラベルを付けて表示する

<details>
<summary>ヒント</summary>

オブジェクトのプロパティには `{profile.name}` のようにアクセスします。カードは `boxShadow` や `borderRadius` でそれっぽく見せられます。

</details>

<details>
<summary>解答例</summary>

```jsx
function ProfileCard() {
  const profile = {
    name: "田中太郎",
    job: "フロントエンドエンジニア",
    hobby: "カフェ巡り",
    motto: "毎日少しずつ成長する",
  };

  const cardStyle = {
    maxWidth: '350px',
    margin: '20px auto',
    padding: '24px',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#fff',
    fontFamily: 'sans-serif',
  };

  return (
    <div style={cardStyle}>
      <h2 style={{ borderBottom: '2px solid #3498db', paddingBottom: '8px' }}>
        {profile.name}
      </h2>
      <p><strong>職業：</strong>{profile.job}</p>
      <p><strong>趣味：</strong>{profile.hobby}</p>
      <p><strong>座右の銘：</strong>{profile.motto}</p>
    </div>
  );
}

export default ProfileCard;
```

</details>

---

## 演習7（応用）：現在の日時を表示しよう

現在の日付と時刻を日本語フォーマットで表示するコンポーネントを作成してください。

**要件：**
- `Date` オブジェクトを使う
- 「2026年3月24日（火）14:30」のような形式で表示する
- 曜日も含める

<details>
<summary>ヒント</summary>

`toLocaleDateString('ja-JP', options)` や `toLocaleTimeString('ja-JP')` を使うと日本語フォーマットにできます。オプションには `{ year: 'numeric', month: 'long', day: 'numeric', weekday: 'short' }` を指定できます。

</details>

<details>
<summary>解答例</summary>

```jsx
function CurrentDateTime() {
  const now = new Date();

  const dateStr = now.toLocaleDateString('ja-JP', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'short',
  });

  const timeStr = now.toLocaleTimeString('ja-JP', {
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <p style={{ fontSize: '24px' }}>{dateStr}</p>
      <p style={{ fontSize: '48px', fontWeight: 'bold' }}>{timeStr}</p>
    </div>
  );
}

export default CurrentDateTime;
```

</details>

---

## 演習8（応用）：ファイル分割を実践しよう

以下の3つのコンポーネントをそれぞれ別ファイルに分割し、`App.jsx` でインポートして組み合わせてください。

- `Header` - サイトのヘッダー（タイトルを表示）
- `Main` - メインコンテンツ（任意の文章）
- `Footer` - フッター（コピーライトを表示）

<details>
<summary>ヒント</summary>

各ファイルで `export default コンポーネント名` とし、App.jsxで `import コンポーネント名 from './components/ファイル名'` でインポートします。

</details>

<details>
<summary>解答例</summary>

```jsx
// src/components/Header.jsx
function Header() {
  return (
    <header style={{ backgroundColor: '#2c3e50', color: 'white', padding: '16px' }}>
      <h1>マイウェブサイト</h1>
    </header>
  );
}
export default Header;

// src/components/Main.jsx
function Main() {
  return (
    <main style={{ padding: '20px', minHeight: '300px' }}>
      <h2>ようこそ</h2>
      <p>これはReactで作ったウェブサイトです。</p>
    </main>
  );
}
export default Main;

// src/components/Footer.jsx
function Footer() {
  return (
    <footer style={{ backgroundColor: '#ecf0f1', padding: '16px', textAlign: 'center' }}>
      <p>&copy; 2026 マイウェブサイト</p>
    </footer>
  );
}
export default Footer;

// src/App.jsx
import Header from './components/Header';
import Main from './components/Main';
import Footer from './components/Footer';

function App() {
  return (
    <div>
      <Header />
      <Main />
      <Footer />
    </div>
  );
}
export default App;
```

</details>

---

## 演習9（チャレンジ）：配列データからカード一覧を表示しよう

商品データの配列からカード一覧を表示してください。（mapの詳細は第4章で学びますが、先取りして挑戦してみましょう。）

**データ：**
```javascript
const products = [
  { id: 1, name: "ノートPC", price: 89800 },
  { id: 2, name: "マウス", price: 3980 },
  { id: 3, name: "キーボード", price: 12800 },
];
```

<details>
<summary>ヒント</summary>

`配列.map(item => <JSX>)` で配列の各要素をJSXに変換できます。各要素には `key` 属性が必要です。

</details>

<details>
<summary>解答例</summary>

```jsx
function ProductList() {
  const products = [
    { id: 1, name: "ノートPC", price: 89800 },
    { id: 2, name: "マウス", price: 3980 },
    { id: 3, name: "キーボード", price: 12800 },
  ];

  return (
    <div style={{ display: 'flex', gap: '16px', padding: '20px' }}>
      {products.map(product => (
        <div key={product.id} style={{
          border: '1px solid #ddd',
          borderRadius: '8px',
          padding: '16px',
          minWidth: '150px',
        }}>
          <h3>{product.name}</h3>
          <p style={{ color: '#e74c3c', fontWeight: 'bold' }}>
            ¥{product.price.toLocaleString()}
          </p>
        </div>
      ))}
    </div>
  );
}

export default ProductList;
```

</details>

---

## 演習10（チャレンジ）：Viteプロジェクトを作成して動かそう

実際にターミナルを使って新しいReactプロジェクトを作成し、以下を行ってください。

**手順：**
1. `npm create vite@latest my-practice -- --template react` でプロジェクトを作成
2. `App.jsx` の内容を自分のオリジナルの自己紹介ページに書き換える
3. 少なくとも2つのコンポーネントを作成して使う
4. インラインスタイルで見た目を整える
5. 開発サーバーで表示を確認する

<details>
<summary>ヒント</summary>

1. ターミナルでコマンドを実行
2. `cd my-practice && npm install && npm run dev`
3. `src/App.jsx` を編集する
4. 新しいコンポーネントは `src/components/` フォルダを作って保存する

</details>

<details>
<summary>解答例</summary>

```bash
# ターミナルで実行
npm create vite@latest my-practice -- --template react
cd my-practice
npm install
npm run dev
```

```jsx
// src/components/SkillBadge.jsx
function SkillBadge({ skill }) {
  return (
    <span style={{
      display: 'inline-block',
      backgroundColor: '#3498db',
      color: 'white',
      padding: '4px 12px',
      borderRadius: '16px',
      margin: '4px',
      fontSize: '14px',
    }}>
      {skill}
    </span>
  );
}
export default SkillBadge;

// src/components/HobbyCard.jsx
function HobbyCard({ title, description }) {
  return (
    <div style={{
      border: '1px solid #e0e0e0',
      borderRadius: '8px',
      padding: '16px',
      margin: '8px',
      flex: 1,
    }}>
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}
export default HobbyCard;

// src/App.jsx
import SkillBadge from './components/SkillBadge';
import HobbyCard from './components/HobbyCard';

function App() {
  const skills = ["HTML", "CSS", "JavaScript", "React"];

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>自己紹介</h1>
      <p>React学習中のエンジニアです。</p>

      <h2>スキル</h2>
      <div>
        {skills.map((skill, i) => (
          <SkillBadge key={i} skill={skill} />
        ))}
      </div>

      <h2>趣味</h2>
      <div style={{ display: 'flex' }}>
        <HobbyCard title="読書" description="技術書をよく読みます" />
        <HobbyCard title="散歩" description="休日は公園を散歩します" />
      </div>
    </div>
  );
}
export default App;
```

</details>
