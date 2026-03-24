# 第1章：TypeScriptの基本 - 演習問題

---

## 問題1：基本の型注釈（基本）

以下の変数に適切な型注釈を付けてください。

```typescript
let userName = "太郎";
let userAge = 25;
let isStudent = true;
let score = 92.5;
```

**期待されるコード：**
型注釈を付けた変数宣言を完成させ、`console.log` で全て出力してください。

**期待される出力：**
```
名前: 太郎
年齢: 25
学生: true
点数: 92.5
```

<details>
<summary>ヒント</summary>

TypeScriptの基本型は `string`, `number`, `boolean` です。`let 変数名: 型 = 値;` の構文で型注釈を付けます。

</details>

<details>
<summary>解答例</summary>

```typescript
// 基本のプリミティブ型に型注釈を付ける
let userName: string = "太郎";
let userAge: number = 25;
let isStudent: boolean = true;
let score: number = 92.5; // 整数も小数もnumber型

console.log(`名前: ${userName}`);
console.log(`年齢: ${userAge}`);
console.log(`学生: ${isStudent}`);
console.log(`点数: ${score}`);
```

</details>

---

## 問題2：配列とタプル（基本）

以下の要件を満たす変数を宣言してください。

1. 文字列の配列 `fruits` に `["りんご", "みかん", "ぶどう"]` を代入
2. 数値の配列 `prices` に `[150, 80, 300]` を代入
3. `[商品名, 価格]` のタプル `item` に `["バナナ", 120]` を代入

**期待される出力：**
```
果物一覧: りんご, みかん, ぶどう
価格一覧: 150, 80, 300
商品: バナナ（120円）
```

<details>
<summary>ヒント</summary>

- 配列の型は `string[]` または `Array<string>` と書きます。
- タプルは `[string, number]` のように要素ごとの型を指定します。

</details>

<details>
<summary>解答例</summary>

```typescript
// 配列の型注釈
const fruits: string[] = ["りんご", "みかん", "ぶどう"];
const prices: number[] = [150, 80, 300];

// タプルの型注釈（要素の位置ごとに型が決まる）
const item: [string, number] = ["バナナ", 120];

console.log(`果物一覧: ${fruits.join(", ")}`);
console.log(`価格一覧: ${prices.join(", ")}`);
console.log(`商品: ${item[0]}（${item[1]}円）`);
```

</details>

---

## 問題3：オブジェクト型（基本）

以下のオブジェクトに適切なインライン型注釈を付けてください。`email` プロパティはオプショナル（省略可能）にしてください。

```typescript
const user = {
  name: "田中太郎",
  age: 30,
  email: "tanaka@example.com",
};
```

さらに、`email` を持たないオブジェクト `user2` も作成してください。

**期待される出力：**
```
ユーザー1: 田中太郎（30歳）- tanaka@example.com
ユーザー2: 山田花子（25歳）- メールなし
```

<details>
<summary>ヒント</summary>

- オブジェクト型は `{ プロパティ名: 型 }` で定義します。
- オプショナルプロパティは `プロパティ名?: 型` と書きます。
- `??` 演算子（Nullish Coalescing）でデフォルト値を設定できます。

</details>

<details>
<summary>解答例</summary>

```typescript
// インラインでオブジェクト型を定義（emailはオプショナル）
const user: { name: string; age: number; email?: string } = {
  name: "田中太郎",
  age: 30,
  email: "tanaka@example.com",
};

// emailを省略したオブジェクト
const user2: { name: string; age: number; email?: string } = {
  name: "山田花子",
  age: 25,
};

// ?? でオプショナルプロパティの安全な表示
console.log(`ユーザー1: ${user.name}（${user.age}歳）- ${user.email ?? "メールなし"}`);
console.log(`ユーザー2: ${user2.name}（${user2.age}歳）- ${user2.email ?? "メールなし"}`);
```

</details>

---

## 問題4：型推論（基本）

以下のコードで、TypeScriptが各変数にどのような型を推論するかを答えてください。

```typescript
const message = "Hello, TypeScript!";
let count = 42;
const isReady = true;
const items = [1, 2, 3];
const mixed = [1, "two", true];
const direction = "north";
let status = "active";
```

**期待される回答：**
各変数の推論される型をコメントとして書き、`console.log` で `typeof` の結果を出力してください。

<details>
<summary>ヒント</summary>

- `const` で宣言した場合、プリミティブ値はリテラル型に推論されます。
- `let` で宣言した場合、より広い型（`string`, `number` など）に推論されます。
- 配列は要素の型のユニオンになります。

</details>

<details>
<summary>解答例</summary>

```typescript
const message = "Hello, TypeScript!"; // "Hello, TypeScript!" 型（リテラル型）
let count = 42;                       // number 型
const isReady = true;                 // true 型（リテラル型）
const items = [1, 2, 3];             // number[] 型
const mixed = [1, "two", true];      // (number | string | boolean)[] 型
const direction = "north";            // "north" 型（リテラル型）
let status = "active";                // string 型（letなので広い型）

// typeof はランタイムの型を返す（TypeScriptの型とは異なる）
console.log(`message: ${typeof message}`);    // string
console.log(`count: ${typeof count}`);        // number
console.log(`isReady: ${typeof isReady}`);    // boolean
console.log(`items: ${typeof items}`);        // object
console.log(`mixed: ${typeof mixed}`);        // object
console.log(`direction: ${typeof direction}`); // string
console.log(`status: ${typeof status}`);      // string
```

</details>

---

## 問題5：any型とunknown型（応用）

以下の2つの関数を完成させてください。

1. `processAny`: `any` 型の引数を受け取り、文字列として長さを返す（危険な例）
2. `processUnknown`: `unknown` 型の引数を受け取り、型ガードを使って安全に処理する

`processUnknown` は以下のルールで処理してください。
- `string` なら文字列の長さを返す
- `number` なら数値をそのまま返す
- それ以外なら `-1` を返す

**期待される出力：**
```
processUnknown("hello") = 5
processUnknown(42) = 42
processUnknown(true) = -1
```

<details>
<summary>ヒント</summary>

- `unknown` 型はそのままでは操作できません。`typeof` で型を確認してから使います。
- `typeof value === "string"` でstring型に絞り込めます。

</details>

<details>
<summary>解答例</summary>

```typescript
// ❌ any型は型安全性がない（参考として掲載）
function processAny(value: any): number {
  // コンパイルエラーにならないが、実行時にエラーの可能性がある
  return value.length; // valueがnumberだったらundefinedが返る
}

// ✅ unknown型 + 型ガードで安全に処理
function processUnknown(value: unknown): number {
  if (typeof value === "string") {
    // ここではvalueはstring型に絞り込まれる
    return value.length;
  } else if (typeof value === "number") {
    // ここではvalueはnumber型に絞り込まれる
    return value;
  } else {
    // それ以外は-1を返す
    return -1;
  }
}

console.log(`processUnknown("hello") = ${processUnknown("hello")}`);
console.log(`processUnknown(42) = ${processUnknown(42)}`);
console.log(`processUnknown(true) = ${processUnknown(true)}`);
```

</details>

---

## 問題6：enum の活用（応用）

信号機の色を管理する `TrafficLight` 列挙型（文字列enum）を作成し、色に応じたメッセージを返す関数 `getAction` を実装してください。

- `Red` → `"RED"` → `"止まれ"`
- `Yellow` → `"YELLOW"` → `"注意"`
- `Green` → `"GREEN"` → `"進め"`

**期待される出力：**
```
RED: 止まれ
YELLOW: 注意
GREEN: 進め
```

<details>
<summary>ヒント</summary>

- 文字列enumは `enum Name { Member = "VALUE" }` の形式で定義します。
- `switch` 文で各メンバーを処理できます。

</details>

<details>
<summary>解答例</summary>

```typescript
// 文字列enum（デバッグしやすく型安全）
enum TrafficLight {
  Red = "RED",
  Yellow = "YELLOW",
  Green = "GREEN",
}

// switch文でenum値に応じた処理
function getAction(light: TrafficLight): string {
  switch (light) {
    case TrafficLight.Red:
      return "止まれ";
    case TrafficLight.Yellow:
      return "注意";
    case TrafficLight.Green:
      return "進め";
  }
}

// enumメンバーを使って呼び出す
console.log(`${TrafficLight.Red}: ${getAction(TrafficLight.Red)}`);
console.log(`${TrafficLight.Yellow}: ${getAction(TrafficLight.Yellow)}`);
console.log(`${TrafficLight.Green}: ${getAction(TrafficLight.Green)}`);
```

</details>

---

## 問題7：型アサーション（応用）

HTMLのフォーム要素を取得する関数を想定して、型アサーション（`as`）を使った安全なDOM操作を書いてください。

以下の関数 `getInputValue` を完成させてください。
- `document.getElementById` でHTML要素を取得
- 取得した要素を `HTMLInputElement` に型アサーション
- 要素が存在しない場合は空文字を返す

**期待されるコード例：**
```typescript
function getInputValue(id: string): string {
  // ここを実装
}
```

<details>
<summary>ヒント</summary>

- `document.getElementById()` の戻り値は `HTMLElement | null` です。
- `as HTMLInputElement` で型アサーションできます。
- `null` チェックを先に行いましょう。

</details>

<details>
<summary>解答例</summary>

```typescript
function getInputValue(id: string): string {
  const element = document.getElementById(id);

  // null チェック（要素が見つからない場合）
  if (element === null) {
    return "";
  }

  // HTMLInputElement に型アサーション
  const inputElement = element as HTMLInputElement;
  return inputElement.value;
}

// 使用例（ブラウザ環境で実行）
// const username = getInputValue("username-input");
// console.log(`入力値: ${username}`);

// Node.js環境ではDOM APIがないため、以下で動作確認
console.log("getInputValue関数を定義しました");
console.log("ブラウザ環境でHTMLのinput要素に対して使用できます");
```

</details>

---

## 問題8：void型とnever型（チャレンジ）

以下の3つの関数を実装してください。

1. `logWithTimestamp(message: string): void` — タイムスタンプ付きでメッセージを出力する関数
2. `throwError(message: string): never` — 常に例外を投げる関数
3. `assertPositive(value: number): void` — 正の数でなければ `throwError` を呼ぶ関数

**期待される出力：**
```
[2026-03-25T...] テスト開始
[2026-03-25T...] 値のチェック: 42 → OK
エラーが正しくキャッチされました: 負の数は許可されていません: -5
```

<details>
<summary>ヒント</summary>

- `void` は「何も返さない」ことを意味します。
- `never` は「関数が正常に終了しない」ことを意味します（例外を投げる、無限ループなど）。
- `try-catch` でエラーをキャッチできます。

</details>

<details>
<summary>解答例</summary>

```typescript
// void: 値を返さない関数
function logWithTimestamp(message: string): void {
  const now = new Date().toISOString();
  console.log(`[${now}] ${message}`);
}

// never: 常に例外を投げる（正常に返ることがない）
function throwError(message: string): never {
  throw new Error(message);
}

// voidを返す関数（内部でnever関数を呼ぶ可能性がある）
function assertPositive(value: number): void {
  if (value <= 0) {
    throwError(`負の数は許可されていません: ${value}`);
  }
}

// 動作確認
logWithTimestamp("テスト開始");

const testValue = 42;
assertPositive(testValue);
logWithTimestamp(`値のチェック: ${testValue} → OK`);

// エラーのテスト
try {
  assertPositive(-5);
} catch (e) {
  if (e instanceof Error) {
    console.log(`エラーが正しくキャッチされました: ${e.message}`);
  }
}
```

</details>

---

## 問題9：readonly と const assertion（チャレンジ）

以下の要件を満たすコードを書いてください。

1. `readonly` プロパティを持つオブジェクト型 `AppConfig` を定義
   - `readonly apiUrl: string`
   - `readonly maxRetries: number`
   - `debug: boolean`（変更可能）

2. `as const` を使って、HTTPメソッドの定数オブジェクト `HTTP_METHODS` を定義
   - GET, POST, PUT, DELETE を含む

3. `HTTP_METHODS` の値の型をユニオン型として抽出し、`HttpMethod` 型を定義

**期待される出力：**
```
API URL: https://api.example.com
Debug mode: ON
HTTPメソッド一覧: GET, POST, PUT, DELETE
GET はHTTPメソッドです
```

<details>
<summary>ヒント</summary>

- `as const` を使うと、オブジェクトの値がリテラル型になります。
- `typeof オブジェクト` でオブジェクトの型を取得できます。
- `(typeof obj)[keyof typeof obj]` で値の型をユニオンとして抽出できます。

</details>

<details>
<summary>解答例</summary>

```typescript
// 1. readonlyプロパティを持つオブジェクト型
type AppConfig = {
  readonly apiUrl: string;
  readonly maxRetries: number;
  debug: boolean; // debugだけは変更可能
};

const config: AppConfig = {
  apiUrl: "https://api.example.com",
  maxRetries: 3,
  debug: true,
};

// config.apiUrl = "new-url"; // エラー！readonlyプロパティ
config.debug = false; // OK！debugは変更可能

// 2. as const で定数オブジェクトを定義
const HTTP_METHODS = {
  GET: "GET",
  POST: "POST",
  PUT: "PUT",
  DELETE: "DELETE",
} as const;

// 3. 値の型をユニオンとして抽出
type HttpMethod = (typeof HTTP_METHODS)[keyof typeof HTTP_METHODS];
// "GET" | "POST" | "PUT" | "DELETE"

// 動作確認
console.log(`API URL: ${config.apiUrl}`);
console.log(`Debug mode: ${config.debug ? "ON" : "OFF"}`);

const methods: HttpMethod[] = [
  HTTP_METHODS.GET,
  HTTP_METHODS.POST,
  HTTP_METHODS.PUT,
  HTTP_METHODS.DELETE,
];
console.log(`HTTPメソッド一覧: ${methods.join(", ")}`);

// 型安全な関数
function isHttpMethod(value: string): value is HttpMethod {
  return Object.values(HTTP_METHODS).includes(value as HttpMethod);
}

const testMethod = "GET";
if (isHttpMethod(testMethod)) {
  console.log(`${testMethod} はHTTPメソッドです`);
}
```

</details>

---

## 問題10：総合問題 — 商品管理システムの型定義（チャレンジ）

以下の要件を満たす商品管理システムの型定義と関数を作成してください。

1. 商品のオブジェクト型（インライン型注釈）を定義
   - `id: number`, `name: string`, `price: number`, `category: string`, `inStock: boolean`
2. 商品の配列を作成（3つ以上の商品）
3. `getInStockItems` 関数：在庫ありの商品だけを返す
4. `getTotalPrice` 関数：全商品の合計金額を返す
5. `formatProduct` 関数：商品情報を整形した文字列を返す

**期待される出力例：**
```
=== 全商品 ===
[1] TypeScript入門書 - ¥3,000（書籍）在庫あり
[2] プログラミングキーボード - ¥15,000（周辺機器）在庫あり
[3] USBハブ - ¥2,500（周辺機器）在庫なし
[4] モニター - ¥35,000（周辺機器）在庫あり

=== 在庫あり商品 ===
TypeScript入門書, プログラミングキーボード, モニター

合計金額: ¥55,500
在庫あり合計: ¥53,000
```

<details>
<summary>ヒント</summary>

- `filter()` で配列を絞り込めます。
- `reduce()` で合計を計算できます。
- `toLocaleString()` で数値を3桁区切りにフォーマットできます。

</details>

<details>
<summary>解答例</summary>

```typescript
// 商品データの配列（インライン型注釈）
const products: {
  id: number;
  name: string;
  price: number;
  category: string;
  inStock: boolean;
}[] = [
  { id: 1, name: "TypeScript入門書", price: 3000, category: "書籍", inStock: true },
  { id: 2, name: "プログラミングキーボード", price: 15000, category: "周辺機器", inStock: true },
  { id: 3, name: "USBハブ", price: 2500, category: "周辺機器", inStock: false },
  { id: 4, name: "モニター", price: 35000, category: "周辺機器", inStock: true },
];

// 商品の型をtypeofで取得（配列の要素の型）
type Product = (typeof products)[number];

// 在庫ありの商品を返す
function getInStockItems(items: Product[]): Product[] {
  return items.filter((item) => item.inStock);
}

// 合計金額を返す
function getTotalPrice(items: Product[]): number {
  return items.reduce((total, item) => total + item.price, 0);
}

// 商品情報を整形
function formatProduct(product: Product): string {
  const stockStatus = product.inStock ? "在庫あり" : "在庫なし";
  const priceStr = product.price.toLocaleString();
  return `[${product.id}] ${product.name} - ¥${priceStr}（${product.category}）${stockStatus}`;
}

// 出力
console.log("=== 全商品 ===");
products.forEach((p) => console.log(formatProduct(p)));

const inStockItems = getInStockItems(products);
console.log("\n=== 在庫あり商品 ===");
console.log(inStockItems.map((p) => p.name).join(", "));

console.log(`\n合計金額: ¥${getTotalPrice(products).toLocaleString()}`);
console.log(`在庫あり合計: ¥${getTotalPrice(inStockItems).toLocaleString()}`);
```

</details>
