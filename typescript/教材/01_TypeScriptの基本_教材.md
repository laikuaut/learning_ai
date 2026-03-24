# 第1章: TypeScriptの基本

## 1.1 TypeScriptとは何か

TypeScriptは、Microsoftが開発した**JavaScriptのスーパーセット**（上位互換）言語です。JavaScriptに「型（Type）」の仕組みを追加することで、より安全で保守しやすいコードを書けるようにします。

### TypeScriptの主な特徴

| 特徴 | 説明 |
|------|------|
| 静的型付け | コンパイル時に型エラーを検出できる |
| 型推論 | 明示的に型を書かなくても、自動的に型を推論してくれる |
| JavaScript互換 | 既存のJavaScriptコードはそのままTypeScriptとして動く |
| 最新のJS機能 | ES2015以降の機能を古いブラウザ向けにコンパイルできる |
| エディタ支援 | VSCodeなどで強力な補完・リファクタリングが使える |

### なぜTypeScriptを使うのか

```javascript
// JavaScriptでの問題例
function add(a, b) {
  return a + b;
}

add(1, "2"); // "12" — 意図しない文字列結合が起きる！
```

```typescript
// TypeScriptなら、コンパイル時にエラーを検出
function add(a: number, b: number): number {
  return a + b;
}

add(1, "2"); // エラー: 型 'string' の引数を型 'number' のパラメータに割り当てることはできません
```

---

## 1.2 環境構築

### Node.jsのインストール

TypeScriptを使うには、まずNode.jsが必要です。[公式サイト](https://nodejs.org/)からLTS版をインストールしてください。

```bash
# バージョン確認
node -v
npm -v
```

### TypeScriptのインストール

```bash
# グローバルインストール
npm install -g typescript

# バージョン確認
tsc --version
```

### プロジェクトの初期化

```bash
# プロジェクトディレクトリを作成
mkdir my-ts-project
cd my-ts-project

# package.jsonの初期化
npm init -y

# TypeScriptをローカルにインストール（推奨）
npm install --save-dev typescript

# tsconfig.jsonの生成
npx tsc --init
```

### tsconfig.json の基本設定

`tsconfig.json` はTypeScriptコンパイラの設定ファイルです。以下は基本的な設定例です。

```json
{
  "compilerOptions": {
    // コンパイル先のJavaScriptバージョン
    "target": "ES2020",

    // モジュールシステム
    "module": "commonjs",

    // 出力先ディレクトリ
    "outDir": "./dist",

    // ソースディレクトリ
    "rootDir": "./src",

    // 厳格モード（推奨）
    "strict": true,

    // ESモジュールとの互換性
    "esModuleInterop": true,

    // ソースマップ生成（デバッグ用）
    "sourceMap": true,

    // 未使用変数のチェック
    "noUnusedLocals": true,

    // 未使用パラメータのチェック
    "noUnusedParameters": true,

    // switch文のfall-throughチェック
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### コンパイルと実行

```bash
# TypeScriptファイルをコンパイル
npx tsc

# 特定のファイルだけコンパイル
npx tsc src/index.ts

# ウォッチモード（ファイル変更を監視して自動コンパイル）
npx tsc --watch

# ts-nodeで直接実行（コンパイル不要）
npm install --save-dev ts-node
npx ts-node src/index.ts
```

---

## 1.3 基本の型（プリミティブ型）

### string（文字列）

```typescript
let name: string = "太郎";
let greeting: string = `こんにちは、${name}さん`; // テンプレートリテラルもOK
```

### number（数値）

```typescript
let age: number = 25;
let pi: number = 3.14159;
let hex: number = 0xff;       // 16進数
let binary: number = 0b1010;  // 2進数
let octal: number = 0o744;    // 8進数
let big: bigint = 100n;       // bigint型は別の型
```

### boolean（真偽値）

```typescript
let isDone: boolean = false;
let isActive: boolean = true;
```

---

## 1.4 配列とタプル

### 配列（Array）

```typescript
// 書き方1: 型[]
let numbers: number[] = [1, 2, 3, 4, 5];
let names: string[] = ["太郎", "花子", "次郎"];

// 書き方2: Array<型>（ジェネリック記法）
let scores: Array<number> = [85, 92, 78];

// 読み取り専用配列
let readonlyNumbers: readonly number[] = [1, 2, 3];
// readonlyNumbers.push(4); // エラー！変更不可
```

### タプル（Tuple）

タプルは**要素の数と各位置の型が固定された配列**です。

```typescript
// [名前, 年齢] のタプル
let person: [string, number] = ["太郎", 25];

// 各要素の型が保証される
let name2: string = person[0]; // OK: string
let age2: number = person[1];  // OK: number

// 型が合わないとエラー
// let wrong: [string, number] = [25, "太郎"]; // エラー！

// ラベル付きタプル（読みやすさのため）
type UserInfo = [name: string, age: number, isActive: boolean];
let user: UserInfo = ["花子", 30, true];

// 可変長タプル
type StringNumberBooleans = [string, number, ...boolean[]];
let data: StringNumberBooleans = ["hello", 1, true, false, true];
```

---

## 1.5 特殊な型

### any型

`any` はあらゆる型の値を受け入れます。**型チェックが無効化される**ため、使用は最小限にすべきです。

```typescript
let anything: any = 42;
anything = "hello";    // OK
anything = true;       // OK
anything.foo();        // コンパイルエラーにならない（実行時にエラーの可能性）
anything.bar.baz;      // これもコンパイルエラーにならない

// any は型安全性を破壊するので注意！
let num: number = anything; // エラーにならない！
```

### unknown型

`unknown` は `any` の安全なバージョンです。値を使う前に型チェックが必要です。

```typescript
let value: unknown = 42;

// unknown型はそのままでは操作できない
// let result: number = value + 1; // エラー！

// 型チェック（型ガード）を行えば使える
if (typeof value === "number") {
  let result: number = value + 1; // OK！
  console.log(result); // 43
}

// type assertion（型アサーション）でも使える
let strValue: unknown = "hello";
let strLength: number = (strValue as string).length; // OK
```

**any と unknown の比較:**

| 特徴 | `any` | `unknown` |
|------|-------|-----------|
| 何でも代入できる | はい | はい |
| 他の型に代入できる | はい（危険） | いいえ（型チェック必要） |
| プロパティアクセス | できる（危険） | できない（型チェック必要） |
| 推奨度 | 非推奨 | 推奨 |

### void型

関数が何も返さないことを示します。

```typescript
function logMessage(message: string): void {
  console.log(message);
  // return文がないか、returnだけ
}

// 変数にはほとんど使わない（undefinedのみ代入可能）
let unusable: void = undefined;
```

### never型

**決して値を返さない**型です。到達不可能なコードや、常に例外を投げる関数に使います。

```typescript
// 常に例外を投げる関数
function throwError(message: string): never {
  throw new Error(message);
}

// 無限ループ
function infiniteLoop(): never {
  while (true) {
    // 永遠に終わらない
  }
}

// 網羅性チェック（exhaustive check）に使える
type Shape = "circle" | "square";

function getArea(shape: Shape): number {
  switch (shape) {
    case "circle":
      return Math.PI * 10 * 10;
    case "square":
      return 10 * 10;
    default:
      // shapeがnever型になる（全ケースを処理済みなら到達しない）
      const _exhaustive: never = shape;
      return _exhaustive;
  }
}
```

### null と undefined

```typescript
// strictNullChecks が true の場合（推奨）
let value1: string = "hello";
// value1 = null;      // エラー！
// value1 = undefined; // エラー！

// null を許容する場合
let value2: string | null = "hello";
value2 = null; // OK

// undefined を許容する場合
let value3: string | undefined = "hello";
value3 = undefined; // OK

// null と undefined の両方を許容
let value4: string | null | undefined = "hello";
value4 = null;      // OK
value4 = undefined; // OK
```

---

## 1.6 型注釈（Type Annotations）と型推論（Type Inference）

### 型注釈

変数・引数・戻り値に明示的に型を指定することを**型注釈**と呼びます。

```typescript
// 変数の型注釈
let age: number = 25;
let name: string = "太郎";
let isActive: boolean = true;

// 関数の型注釈
function greet(name: string, age: number): string {
  return `${name}さんは${age}歳です`;
}
```

### 型推論

TypeScriptは多くの場面で型を自動的に推論します。型注釈を省略しても安全なケースが多いです。

```typescript
// 型推論が働く例
let count = 42;          // number と推論される
let message = "hello";   // string と推論される
let items = [1, 2, 3];   // number[] と推論される

// 関数の戻り値も推論される
function add(a: number, b: number) {
  return a + b; // 戻り値は number と推論される
}

// constの場合、リテラル型に推論される
const direction = "north"; // "north" 型（string ではない）
```

### 型注釈を書くべき場面

```typescript
// 1. 関数のパラメータには必ず型注釈を書く
function calculate(x: number, y: number): number {
  return x + y;
}

// 2. 初期値なしで宣言する場合
let result: number;
result = calculate(1, 2);

// 3. 型推論が意図と異なる場合
let ids: number[] = []; // 空配列は any[] と推論されるため明示する

// 4. オブジェクトの型を明示したい場合
let user: { name: string; age: number } = {
  name: "太郎",
  age: 25,
};
```

---

## 1.7 オブジェクト型

```typescript
// インラインでオブジェクト型を定義
let user: { name: string; age: number; email?: string } = {
  name: "太郎",
  age: 25,
  // emailはオプショナルなので省略可能
};

// readonlyプロパティ
let config: { readonly apiUrl: string; timeout: number } = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
};
// config.apiUrl = "..."; // エラー！readonlyプロパティは変更できない
config.timeout = 10000;   // OK
```

---

## 1.8 列挙型（enum）

```typescript
// 数値enum
enum Direction {
  Up = 0,
  Down = 1,
  Left = 2,
  Right = 3,
}

let dir: Direction = Direction.Up;
console.log(dir); // 0

// 文字列enum（推奨：デバッグしやすい）
enum Color {
  Red = "RED",
  Green = "GREEN",
  Blue = "BLUE",
}

let color: Color = Color.Red;
console.log(color); // "RED"

// constEnum（コンパイル時に展開される）
const enum HttpStatus {
  OK = 200,
  NotFound = 404,
  InternalError = 500,
}

let status = HttpStatus.OK; // コンパイル後: let status = 200;
```

> **補足:** モダンなTypeScriptでは、enumの代わりに `as const` を使ったオブジェクトリテラルが推奨されることもあります。これについては第6章で詳しく解説します。

---

## 1.9 型アサーション（Type Assertion）

型アサーションは、TypeScriptのコンパイラに「この値はこの型だ」と伝える方法です。

```typescript
// as 構文（推奨）
let someValue: unknown = "hello world";
let strLength: number = (someValue as string).length;

// アングルブラケット構文（JSXでは使えない）
let strLength2: number = (<string>someValue).length;

// DOM操作での例
const element = document.getElementById("myInput") as HTMLInputElement;
element.value = "TypeScript";

// const assertion
let colors = ["red", "green", "blue"] as const;
// 型は readonly ["red", "green", "blue"] になる
// colors.push("yellow"); // エラー！readonlyなので変更不可
```

**注意:** 型アサーションは型チェックを上書きするため、誤った使い方をするとランタイムエラーの原因になります。可能な限り型ガード（第6章）を使いましょう。

---

## 1.10 まとめ

この章で学んだことをまとめます。

| トピック | 内容 |
|---------|------|
| TypeScriptとは | JavaScriptに型を追加した言語 |
| 環境構築 | tsc, tsconfig.json, ts-node |
| 基本型 | string, number, boolean |
| 配列・タプル | `number[]`, `[string, number]` |
| 特殊な型 | any, unknown, void, never, null, undefined |
| 型注釈と型推論 | 明示的な型指定 vs 自動推論 |
| オブジェクト型 | `{ key: type }` 形式 |
| enum | 列挙型 |
| 型アサーション | `as` を使った型の指定 |

### 次章の予告

次の章では、**インターフェース（interface）と型エイリアス（type）** について詳しく学びます。オブジェクトの形状を定義する方法と、再利用可能な型の作り方を習得しましょう。
