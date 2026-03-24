// ==============================
// ジェネリック関数サンプル
// 第5章：ジェネリクスの総合サンプル
// ==============================
// 学べる内容:
//   - ジェネリック関数の定義と型推論
//   - 制約（extends）の使い方
//   - keyof を使った型安全なプロパティアクセス
//   - ジェネリックインターフェースとクラス
//   - 実用的なユーティリティ関数の作成
//   - 条件型とマップ型の基礎
// 実行方法:
//   npx tsc 03_ジェネリック関数.ts && node 03_ジェネリック関数.js
//   または: npx ts-node 03_ジェネリック関数.ts
// ==============================

// =====================
// 1. 基本的なジェネリック関数
// =====================

// 配列の最初と最後の要素を取得
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

function last<T>(arr: T[]): T | undefined {
  return arr[arr.length - 1];
}

// タプルの要素を入れ替え
function swap<T, U>(pair: [T, U]): [U, T] {
  return [pair[1], pair[0]];
}

console.log("=== 1. 基本的なジェネリック関数 ===");
console.log(`first([10, 20, 30]) = ${first([10, 20, 30])}`);
console.log(`last(["a", "b", "c"]) = ${last(["a", "b", "c"])}`);
console.log(`swap(["hello", 42]) = ${JSON.stringify(swap(["hello", 42]))}`);
console.log();

// =====================
// 2. 配列操作のユーティリティ
// =====================

// 重複を除去
function unique<T>(arr: T[]): T[] {
  return [...new Set(arr)];
}

// 配列をチャンクに分割
function chunk<T>(arr: T[], size: number): T[][] {
  const result: T[][] = [];
  for (let i = 0; i < arr.length; i += size) {
    result.push(arr.slice(i, i + size));
  }
  return result;
}

// 配列をグループ化
function groupBy<T>(arr: T[], keyFn: (item: T) => string): Record<string, T[]> {
  return arr.reduce((groups, item) => {
    const key = keyFn(item);
    if (!groups[key]) {
      groups[key] = [];
    }
    groups[key].push(item);
    return groups;
  }, {} as Record<string, T[]>);
}

// 配列から条件に合う最初の要素を検索
function findBy<T>(arr: T[], predicate: (item: T) => boolean): T | undefined {
  return arr.find(predicate);
}

console.log("=== 2. 配列操作ユーティリティ ===");
console.log(`unique([1,2,2,3,3,3]) = ${JSON.stringify(unique([1, 2, 2, 3, 3, 3]))}`);
console.log(`chunk([1,2,3,4,5], 2) = ${JSON.stringify(chunk([1, 2, 3, 4, 5], 2))}`);

const people = [
  { name: "太郎", dept: "開発" },
  { name: "花子", dept: "営業" },
  { name: "次郎", dept: "開発" },
  { name: "美咲", dept: "営業" },
  { name: "健太", dept: "企画" },
];

const grouped = groupBy(people, (p) => p.dept);
console.log("グループ化:");
Object.entries(grouped).forEach(([dept, members]) => {
  console.log(`  ${dept}: ${members.map((m) => m.name).join(", ")}`);
});
console.log();

// =====================
// 3. 制約付きジェネリクス
// =====================

// lengthプロパティを持つ型に制約
function getLength<T extends { length: number }>(value: T): number {
  return value.length;
}

// キーに制約をかけた安全なプロパティアクセス
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// 比較可能な値の中から最小値を取得
function minimum<T extends number | string>(values: T[]): T | undefined {
  if (values.length === 0) return undefined;
  return values.reduce((min, val) => (val < min ? val : min));
}

console.log("=== 3. 制約付きジェネリクス ===");
console.log(`getLength("hello") = ${getLength("hello")}`);
console.log(`getLength([1, 2, 3]) = ${getLength([1, 2, 3])}`);

const user = { name: "太郎", age: 25, email: "taro@example.com" };
console.log(`getProperty(user, "name") = ${getProperty(user, "name")}`);
console.log(`getProperty(user, "age") = ${getProperty(user, "age")}`);

console.log(`minimum([5, 3, 8, 1, 9]) = ${minimum([5, 3, 8, 1, 9])}`);
console.log(`minimum(["banana", "apple", "cherry"]) = ${minimum(["banana", "apple", "cherry"])}`);
console.log();

// =====================
// 4. ジェネリック型エイリアスとインターフェース
// =====================

// Result型（成功/失敗を表現）
type Result<T, E = string> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

function err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

// Result型を使う関数
function safeDivide(a: number, b: number): Result<number, string> {
  if (b === 0) return err("ゼロで割ることはできません");
  return ok(a / b);
}

function safeParseInt(input: string): Result<number, string> {
  const num = parseInt(input, 10);
  if (isNaN(num)) return err(`"${input}" は数値に変換できません`);
  return ok(num);
}

// Result型のマップ関数
function mapResult<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => U
): Result<U, E> {
  if (result.ok) return ok(fn(result.value));
  return result;
}

console.log("=== 4. Result型パターン ===");

const div1 = safeDivide(10, 3);
const div2 = safeDivide(10, 0);
console.log(`10 / 3 = ${div1.ok ? div1.value.toFixed(2) : div1.error}`);
console.log(`10 / 0 = ${div2.ok ? div2.value : div2.error}`);

const parse1 = safeParseInt("42");
const parse2 = safeParseInt("abc");
console.log(`parseInt("42") = ${parse1.ok ? parse1.value : parse1.error}`);
console.log(`parseInt("abc") = ${parse2.ok ? parse2.value : parse2.error}`);

// マップで値を変換
const doubled = mapResult(safeDivide(10, 2), (v) => v * 2);
console.log(`(10 / 2) * 2 = ${doubled.ok ? doubled.value : doubled.error}`);
console.log();

// =====================
// 5. ジェネリッククラス: スタック
// =====================

class Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T | undefined {
    return this.items.pop();
  }

  peek(): T | undefined {
    return this.items[this.items.length - 1];
  }

  get size(): number {
    return this.items.length;
  }

  isEmpty(): boolean {
    return this.items.length === 0;
  }

  toArray(): T[] {
    return [...this.items];
  }
}

console.log("=== 5. ジェネリッククラス: スタック ===");
const undoStack = new Stack<string>();
undoStack.push("入力: Hello");
undoStack.push("入力: World");
undoStack.push("削除: World");

console.log(`操作履歴: ${undoStack.toArray().join(" → ")}`);
console.log(`最新の操作: ${undoStack.peek()}`);

const undone = undoStack.pop();
console.log(`取り消し: ${undone}`);
console.log(`残りの操作: ${undoStack.toArray().join(" → ")}`);
console.log();

// =====================
// 6. 実践: 型安全なイベントシステム
// =====================

// イベントの型マップを定義
interface AppEventMap {
  userLogin: { userId: string; timestamp: Date };
  userLogout: { userId: string };
  pageView: { path: string; referrer: string | null };
  purchase: { productId: number; amount: number; currency: string };
}

// 型安全なイベントエミッター
class EventBus<TEvents extends Record<string, any>> {
  private handlers: Partial<{
    [K in keyof TEvents]: Array<(data: TEvents[K]) => void>;
  }> = {};

  on<K extends keyof TEvents>(
    event: K,
    handler: (data: TEvents[K]) => void
  ): void {
    if (!this.handlers[event]) {
      this.handlers[event] = [];
    }
    this.handlers[event]!.push(handler);
  }

  emit<K extends keyof TEvents>(event: K, data: TEvents[K]): void {
    const eventHandlers = this.handlers[event];
    if (eventHandlers) {
      eventHandlers.forEach((handler) => handler(data));
    }
  }
}

console.log("=== 6. 型安全なイベントシステム ===");
const bus = new EventBus<AppEventMap>();

// イベントハンドラの登録（dataの型が自動推論される）
bus.on("userLogin", (data) => {
  console.log(`  ログイン: ${data.userId} at ${data.timestamp.toISOString()}`);
});

bus.on("pageView", (data) => {
  console.log(`  ページ閲覧: ${data.path} (from: ${data.referrer ?? "直接"})`);
});

bus.on("purchase", (data) => {
  console.log(`  購入: 商品#${data.productId} ¥${data.amount.toLocaleString()}`);
});

// イベントの発火（データの型が強制される）
bus.emit("userLogin", { userId: "user-001", timestamp: new Date() });
bus.emit("pageView", { path: "/products", referrer: "/home" });
bus.emit("purchase", { productId: 42, amount: 3200, currency: "JPY" });

// bus.emit("userLogin", { wrong: "data" }); // エラー！型が合わない
console.log();

// =====================
// 7. 実用的なユーティリティ関数集
// =====================

// オブジェクトから指定キーだけ取り出す（型安全なPick）
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>;
  keys.forEach((key) => {
    result[key] = obj[key];
  });
  return result;
}

// オブジェクトから指定キーを除外する（型安全なOmit）
function omit<T extends Record<string, any>, K extends keyof T>(
  obj: T,
  keys: K[]
): Omit<T, K> {
  const result = { ...obj };
  keys.forEach((key) => {
    delete result[key];
  });
  return result as Omit<T, K>;
}

// 2つのオブジェクトをマージ
function merge<T, U>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}

console.log("=== 7. ユーティリティ関数集 ===");

const fullUser = { id: 1, name: "太郎", email: "taro@example.com", age: 25, role: "admin" };

const summary = pick(fullUser, ["id", "name", "role"]);
console.log(`pick(user, ["id", "name", "role"]) = ${JSON.stringify(summary)}`);

const withoutEmail = omit(fullUser, ["email", "age"]);
console.log(`omit(user, ["email", "age"]) = ${JSON.stringify(withoutEmail)}`);

const merged = merge({ name: "太郎" }, { age: 25, role: "admin" });
console.log(`merge({name}, {age, role}) = ${JSON.stringify(merged)}`);
