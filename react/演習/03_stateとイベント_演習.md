# 第3章 演習：stateとイベント

---

## 演習1（基本）：カウンターを作ろう

`useState` を使って、ボタンをクリックすると数値が1ずつ増えるカウンターを作成してください。

**要件：**
- 現在のカウントを表示する
- 「+1」ボタンで1増える

<details>
<summary>ヒント</summary>

```jsx
const [count, setCount] = useState(0);
```

ボタンの `onClick` に `() => setCount(count + 1)` を渡します。

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h2>カウント: {count}</h2>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
}

export default Counter;
```

</details>

---

## 演習2（基本）：表示/非表示を切り替えよう

ボタンをクリックするたびに、メッセージの表示/非表示が切り替わるコンポーネントを作成してください。

**要件：**
- `isVisible` というstateを使う
- ボタンのテキストも「表示する」「隠す」で切り替わる

<details>
<summary>ヒント</summary>

`const [isVisible, setIsVisible] = useState(false)` を使い、`setIsVisible(!isVisible)` でトグルします。

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState } from 'react';

function ToggleMessage() {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div style={{ padding: '20px' }}>
      <button onClick={() => setIsVisible(!isVisible)}>
        {isVisible ? "隠す" : "表示する"}
      </button>
      {isVisible && (
        <p style={{ marginTop: '12px', padding: '12px', backgroundColor: '#e3f2fd' }}>
          こんにちは！これは表示/非表示を切り替えられるメッセージです。
        </p>
      )}
    </div>
  );
}

export default ToggleMessage;
```

</details>

---

## 演習3（基本）：テキスト入力をリアルタイム表示しよう

入力フィールドに文字を入力すると、その内容がリアルタイムで下に表示されるコンポーネントを作成してください。

**要件：**
- `input` タグの `value` と `onChange` を使う（制御コンポーネント）
- 入力した文字数も表示する

<details>
<summary>ヒント</summary>

`onChange={(e) => setText(e.target.value)}` で入力値をstateに保存します。文字数は `{text.length}` で取得できます。

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState } from 'react';

function LiveInput() {
  const [text, setText] = useState("");

  return (
    <div style={{ padding: '20px' }}>
      <label>テキストを入力：</label>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{ padding: '8px', width: '300px', marginLeft: '8px' }}
      />
      <p>入力内容：{text || "（未入力）"}</p>
      <p>文字数：{text.length}文字</p>
    </div>
  );
}

export default LiveInput;
```

</details>

---

## 演習4（基本）：+1、-1、リセットボタンのあるカウンター

演習1を拡張して、「+1」「-1」「リセット」の3つのボタンがあるカウンターを作成してください。

<details>
<summary>ヒント</summary>

それぞれのボタンに異なる `onClick` ハンドラを設定します。リセットは `setCount(0)` です。

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState } from 'react';

function AdvancedCounter() {
  const [count, setCount] = useState(0);

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h2>カウント: {count}</h2>
      <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
        <button onClick={() => setCount(count - 1)}>-1</button>
        <button onClick={() => setCount(0)}>リセット</button>
        <button onClick={() => setCount(count + 1)}>+1</button>
      </div>
    </div>
  );
}

export default AdvancedCounter;
```

</details>

---

## 演習5（基本）：背景色を切り替えよう

3つのボタン（赤、青、緑）を作り、クリックしたボタンに応じてボックスの背景色が変わるコンポーネントを作成してください。

<details>
<summary>ヒント</summary>

`const [color, setColor] = useState("white")` を使い、各ボタンの `onClick` で `setColor("red")` のように色を設定します。

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState } from 'react';

function ColorChanger() {
  const [color, setColor] = useState("#ffffff");

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
        <button onClick={() => setColor("#e74c3c")}>赤</button>
        <button onClick={() => setColor("#3498db")}>青</button>
        <button onClick={() => setColor("#2ecc71")}>緑</button>
        <button onClick={() => setColor("#ffffff")}>リセット</button>
      </div>
      <div style={{
        width: '200px',
        height: '200px',
        backgroundColor: color,
        border: '2px solid #ddd',
        borderRadius: '8px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        transition: 'background-color 0.3s',
      }}>
        {color}
      </div>
    </div>
  );
}

export default ColorChanger;
```

</details>

---

## 演習6（応用）：セレクトボックスとチェックボックスのフォーム

以下のフォームを作成してください。

**要件：**
- 名前（テキスト入力）
- 好きな言語（セレクトボックス：JavaScript / Python / Rust / Go）
- ニュースレター購読（チェックボックス）
- 入力内容をリアルタイムでプレビュー表示する

<details>
<summary>ヒント</summary>

セレクトボックスは `<select value={lang} onChange={...}>` で制御します。チェックボックスは `checked` と `e.target.checked` を使います。

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState } from 'react';

function SettingsForm() {
  const [name, setName] = useState("");
  const [language, setLanguage] = useState("JavaScript");
  const [subscribe, setSubscribe] = useState(false);

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <h2>設定フォーム</h2>

      <div style={{ marginBottom: '12px' }}>
        <label>名前：</label><br />
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ padding: '8px', width: '100%' }}
        />
      </div>

      <div style={{ marginBottom: '12px' }}>
        <label>好きな言語：</label><br />
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          style={{ padding: '8px', width: '100%' }}
        >
          <option value="JavaScript">JavaScript</option>
          <option value="Python">Python</option>
          <option value="Rust">Rust</option>
          <option value="Go">Go</option>
        </select>
      </div>

      <div style={{ marginBottom: '12px' }}>
        <label>
          <input
            type="checkbox"
            checked={subscribe}
            onChange={(e) => setSubscribe(e.target.checked)}
          />
          ニュースレターを購読する
        </label>
      </div>

      <div style={{
        padding: '16px',
        backgroundColor: '#f0f0f0',
        borderRadius: '8px',
        marginTop: '20px',
      }}>
        <h3>プレビュー</h3>
        <p>名前：{name || "（未入力）"}</p>
        <p>好きな言語：{language}</p>
        <p>ニュースレター：{subscribe ? "購読する" : "購読しない"}</p>
      </div>
    </div>
  );
}

export default SettingsForm;
```

</details>

---

## 演習7（応用）：オブジェクトのstateで複数フィールドを管理しよう

1つの `formData` オブジェクトで、ユーザー名・メール・自己紹介の3つのフィールドを管理するフォームを作成してください。

**要件：**
- stateは `{ username: "", email: "", bio: "" }` の1つのオブジェクト
- `handleChange` 関数を共通化して、`name` 属性で更新するフィールドを判別する

<details>
<summary>ヒント</summary>

`handleChange` では `e.target.name` で入力フィールドの名前を取得し、スプレッド構文で更新します。

```jsx
setFormData({ ...formData, [e.target.name]: e.target.value });
```

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState } from 'react';

function ProfileForm() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    bio: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(JSON.stringify(formData, null, 2));
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <h2>プロフィール編集</h2>

      <div style={{ marginBottom: '12px' }}>
        <label>ユーザー名：</label>
        <input type="text" name="username" value={formData.username} onChange={handleChange} style={{ width: '100%', padding: '8px' }} />
      </div>

      <div style={{ marginBottom: '12px' }}>
        <label>メール：</label>
        <input type="email" name="email" value={formData.email} onChange={handleChange} style={{ width: '100%', padding: '8px' }} />
      </div>

      <div style={{ marginBottom: '12px' }}>
        <label>自己紹介：</label>
        <textarea name="bio" value={formData.bio} onChange={handleChange} rows={4} style={{ width: '100%', padding: '8px' }} />
      </div>

      <button type="submit" style={{ padding: '8px 24px' }}>送信</button>
    </form>
  );
}

export default ProfileForm;
```

</details>

---

## 演習8（応用）：配列stateでタグ入力機能を作ろう

テキスト入力でタグを追加し、各タグの横の「x」ボタンで削除できるタグ入力コンポーネントを作成してください。

**要件：**
- Enterキーまたは「追加」ボタンでタグを追加
- 空文字や重複は追加しない
- 各タグに「x」ボタンで削除できるようにする

<details>
<summary>ヒント</summary>

- 追加：`setTags([...tags, newTag])`
- 削除：`setTags(tags.filter(t => t !== tagToRemove))`
- 重複チェック：`tags.includes(input)`
- Enterキー検出：`onKeyDown` で `e.key === "Enter"` をチェック

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState } from 'react';

function TagInput() {
  const [tags, setTags] = useState(["React", "JavaScript"]);
  const [input, setInput] = useState("");

  const addTag = () => {
    const trimmed = input.trim();
    if (trimmed === "" || tags.includes(trimmed)) return;
    setTags([...tags, trimmed]);
    setInput("");
  };

  const removeTag = (tagToRemove) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addTag();
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <h2>タグ入力</h2>

      <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="タグを入力..."
          style={{ flex: 1, padding: '8px' }}
        />
        <button onClick={addTag}>追加</button>
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
        {tags.map(tag => (
          <span key={tag} style={{
            backgroundColor: '#3498db',
            color: 'white',
            padding: '4px 12px',
            borderRadius: '16px',
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
          }}>
            {tag}
            <button
              onClick={() => removeTag(tag)}
              style={{
                background: 'none',
                border: 'none',
                color: 'white',
                cursor: 'pointer',
                fontSize: '14px',
                padding: '0 2px',
              }}
            >
              x
            </button>
          </span>
        ))}
      </div>

      {tags.length === 0 && <p style={{ color: '#999' }}>タグがありません</p>}
    </div>
  );
}

export default TagInput;
```

</details>

---

## 演習9（チャレンジ）：ストップウォッチを作ろう

「開始」「停止」「リセット」ボタンのあるストップウォッチを作成してください。

**要件：**
- 0.1秒（100ミリ秒）刻みで表示が更新される
- 「開始」で計測開始、「停止」で一時停止、「リセット」で0に戻る
- 表示形式：`00:00.0`（分:秒.10分の1秒）

<details>
<summary>ヒント</summary>

- `setInterval` で100msごとにカウントを更新
- stateは経過ミリ秒を保持する
- `useRef` を使ってintervalIdを保持するのが理想だが、stateだけでも実現可能
- 分・秒・10分の1秒の計算：`Math.floor(ms / 60000)`, `Math.floor((ms % 60000) / 1000)`, `Math.floor((ms % 1000) / 100)`

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState, useEffect } from 'react';

function Stopwatch() {
  const [time, setTime] = useState(0); // ミリ秒
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    if (!isRunning) return;

    const intervalId = setInterval(() => {
      setTime(prev => prev + 100);
    }, 100);

    return () => clearInterval(intervalId);
  }, [isRunning]);

  const minutes = Math.floor(time / 60000);
  const seconds = Math.floor((time % 60000) / 1000);
  const tenths = Math.floor((time % 1000) / 100);

  const display = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${tenths}`;

  const reset = () => {
    setIsRunning(false);
    setTime(0);
  };

  return (
    <div style={{ textAlign: 'center', padding: '40px' }}>
      <h2 style={{ fontSize: '64px', fontFamily: 'monospace', margin: '20px 0' }}>
        {display}
      </h2>
      <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
        <button
          onClick={() => setIsRunning(!isRunning)}
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            backgroundColor: isRunning ? '#e74c3c' : '#27ae60',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          {isRunning ? "停止" : "開始"}
        </button>
        <button
          onClick={reset}
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            backgroundColor: '#95a5a6',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          リセット
        </button>
      </div>
    </div>
  );
}

export default Stopwatch;
```

</details>

---

## 演習10（チャレンジ）：簡易電卓を作ろう

四則演算ができる簡易電卓を作成してください。

**要件：**
- 2つの数値入力フィールド
- 演算子選択（+、-、×、÷）
- 「計算」ボタンで結果を表示
- 0で割った場合はエラーメッセージを表示

<details>
<summary>ヒント</summary>

- 2つの入力値と演算子をstateで管理
- `parseFloat()` で文字列を数値に変換
- switch文で演算子ごとの計算を実行
- 計算結果もstateで保持する

</details>

<details>
<summary>解答例</summary>

```jsx
import { useState } from 'react';

function Calculator() {
  const [num1, setNum1] = useState("");
  const [num2, setNum2] = useState("");
  const [operator, setOperator] = useState("+");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const calculate = () => {
    const a = parseFloat(num1);
    const b = parseFloat(num2);

    if (isNaN(a) || isNaN(b)) {
      setError("有効な数値を入力してください。");
      setResult(null);
      return;
    }

    setError("");
    let res;
    switch (operator) {
      case "+": res = a + b; break;
      case "-": res = a - b; break;
      case "*": res = a * b; break;
      case "/":
        if (b === 0) {
          setError("0で割ることはできません。");
          setResult(null);
          return;
        }
        res = a / b;
        break;
      default: return;
    }

    setResult(Math.round(res * 10000) / 10000);
  };

  const clear = () => {
    setNum1("");
    setNum2("");
    setOperator("+");
    setResult(null);
    setError("");
  };

  const operatorLabel = { "+": "+", "-": "-", "*": "×", "/": "÷" };

  return (
    <div style={{
      maxWidth: '350px',
      margin: '0 auto',
      padding: '24px',
      border: '1px solid #ddd',
      borderRadius: '12px',
    }}>
      <h2 style={{ textAlign: 'center' }}>電卓</h2>

      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
        <input
          type="number"
          value={num1}
          onChange={(e) => setNum1(e.target.value)}
          style={{ flex: 1, padding: '8px', textAlign: 'right' }}
          placeholder="0"
        />
        <select
          value={operator}
          onChange={(e) => setOperator(e.target.value)}
          style={{ padding: '8px', fontSize: '18px' }}
        >
          <option value="+">+</option>
          <option value="-">-</option>
          <option value="*">×</option>
          <option value="/">÷</option>
        </select>
        <input
          type="number"
          value={num2}
          onChange={(e) => setNum2(e.target.value)}
          style={{ flex: 1, padding: '8px', textAlign: 'right' }}
          placeholder="0"
        />
      </div>

      <div style={{ display: 'flex', gap: '8px' }}>
        <button onClick={calculate} style={{
          flex: 1, padding: '10px', backgroundColor: '#3498db',
          color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer',
        }}>
          計算
        </button>
        <button onClick={clear} style={{
          padding: '10px 16px', backgroundColor: '#95a5a6',
          color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer',
        }}>
          C
        </button>
      </div>

      {error && <p style={{ color: 'red', marginTop: '12px' }}>{error}</p>}

      {result !== null && (
        <div style={{
          marginTop: '16px',
          padding: '16px',
          backgroundColor: '#ecf0f1',
          borderRadius: '8px',
          textAlign: 'center',
        }}>
          <p style={{ margin: 0, fontSize: '14px', color: '#666' }}>
            {num1} {operatorLabel[operator]} {num2} =
          </p>
          <p style={{ margin: '4px 0 0', fontSize: '28px', fontWeight: 'bold' }}>
            {result}
          </p>
        </div>
      )}
    </div>
  );
}

export default Calculator;
```

</details>
