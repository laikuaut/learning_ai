// ==============================
// 型ガード実践サンプル
// 第7章：型ガードと型の絞り込みの総合サンプル
// ==============================
// 学べる内容:
//   - typeof, instanceof, in による型の絞り込み
//   - 判別共用体（Discriminated Unions）の活用
//   - カスタム型ガード関数（is述語）
//   - アサーション関数（asserts述語）
//   - 配列フィルタリングと型ガードの連携
//   - 実践的なデータバリデーション
//   - 網羅性チェック（Exhaustive Check）
// 実行方法:
//   npx tsc 04_型ガード実践.ts && node 04_型ガード実践.js
//   または: npx ts-node 04_型ガード実践.ts
// ==============================

// =====================
// 1. typeof による絞り込み
// =====================

function formatValue(value: string | number | boolean | null | undefined): string {
  if (value === null) return "(null)";
  if (value === undefined) return "(undefined)";

  switch (typeof value) {
    case "string":
      return `"${value}"（${value.length}文字）`;
    case "number":
      return `${value}（${Number.isInteger(value) ? "整数" : "小数"}）`;
    case "boolean":
      return value ? "真（true）" : "偽（false）";
  }
}

console.log("=== 1. typeof による絞り込み ===");
const testValues: (string | number | boolean | null | undefined)[] = [
  "TypeScript", 42, 3.14, true, false, null, undefined,
];
testValues.forEach((v) => {
  console.log(`  ${String(v).padEnd(12)} → ${formatValue(v)}`);
});
console.log();

// =====================
// 2. 判別共用体パターン
// =====================

// 通知システムの型定義
interface EmailNotification {
  type: "email";
  to: string;
  subject: string;
  body: string;
}

interface SmsNotification {
  type: "sms";
  phoneNumber: string;
  message: string;
}

interface PushNotification {
  type: "push";
  deviceId: string;
  title: string;
  body: string;
  badge?: number;
}

interface SlackNotification {
  type: "slack";
  channel: string;
  message: string;
  mentions?: string[];
}

type Notification = EmailNotification | SmsNotification | PushNotification | SlackNotification;

// 網羅性チェック用ヘルパー
function assertNever(value: never): never {
  throw new Error(`予期しない値: ${JSON.stringify(value)}`);
}

// 判別プロパティ（type）で型を絞り込む
function sendNotification(notification: Notification): string {
  switch (notification.type) {
    case "email":
      return `メール送信: ${notification.to} - "${notification.subject}"`;
    case "sms":
      return `SMS送信: ${notification.phoneNumber} - "${notification.message}"`;
    case "push": {
      const badge = notification.badge ? ` (バッジ: ${notification.badge})` : "";
      return `プッシュ通知: ${notification.deviceId} - "${notification.title}"${badge}`;
    }
    case "slack": {
      const mentions = notification.mentions?.length
        ? ` (メンション: ${notification.mentions.join(", ")})`
        : "";
      return `Slack: #${notification.channel} - "${notification.message}"${mentions}`;
    }
    default:
      // 全ケースを処理していなければコンパイルエラーになる
      return assertNever(notification);
  }
}

console.log("=== 2. 判別共用体パターン ===");
const notifications: Notification[] = [
  { type: "email", to: "user@example.com", subject: "会議のお知らせ", body: "..." },
  { type: "sms", phoneNumber: "090-1234-5678", message: "認証コード: 9876" },
  { type: "push", deviceId: "dev-001", title: "新着メッセージ", body: "...", badge: 3 },
  { type: "slack", channel: "general", message: "デプロイ完了", mentions: ["@team"] },
];

notifications.forEach((n) => {
  console.log(`  ${sendNotification(n)}`);
});
console.log();

// =====================
// 3. カスタム型ガード関数
// =====================

interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "user";
}

interface Product {
  id: number;
  name: string;
  price: number;
  category: string;
}

// is述語によるカスタム型ガード
function isUser(value: unknown): value is User {
  if (typeof value !== "object" || value === null) return false;
  const obj = value as Record<string, unknown>;
  return (
    typeof obj.id === "number" &&
    typeof obj.name === "string" &&
    typeof obj.email === "string" &&
    (obj.role === "admin" || obj.role === "user")
  );
}

function isProduct(value: unknown): value is Product {
  if (typeof value !== "object" || value === null) return false;
  const obj = value as Record<string, unknown>;
  return (
    typeof obj.id === "number" &&
    typeof obj.name === "string" &&
    typeof obj.price === "number" &&
    typeof obj.category === "string"
  );
}

// null/undefinedを除外する汎用型ガード
function isNonNull<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

console.log("=== 3. カスタム型ガード関数 ===");

// unknownデータの分類
const mixedData: unknown[] = [
  { id: 1, name: "太郎", email: "taro@test.com", role: "admin" },
  { id: 2, name: "TypeScript本", price: 3200, category: "書籍" },
  { id: 3, name: "花子", email: "hanako@test.com", role: "user" },
  "無効なデータ",
  null,
  { id: 4, name: "キーボード", price: 12800, category: "周辺機器" },
];

const users = mixedData.filter(isUser);
const products = mixedData.filter(isProduct);

console.log(`ユーザー（${users.length}件）:`);
users.forEach((u) => console.log(`  ${u.name} <${u.email}> [${u.role}]`));

console.log(`商品（${products.length}件）:`);
products.forEach((p) => console.log(`  ${p.name} - ¥${p.price.toLocaleString()}`));

// isNonNullでフィルタリング
const sparseArray: (string | null | undefined)[] = ["a", null, "b", undefined, "c", null];
const cleanArray = sparseArray.filter(isNonNull); // string[]型になる
console.log(`\nNull除去: [${sparseArray.join(", ")}] → [${cleanArray.join(", ")}]`);
console.log();

// =====================
// 4. アサーション関数
// =====================

function assertIsString(value: unknown, name: string = "値"): asserts value is string {
  if (typeof value !== "string") {
    throw new Error(`${name}は文字列でなければなりません（実際: ${typeof value}）`);
  }
}

function assertInRange(
  value: number,
  min: number,
  max: number,
  name: string = "値"
): asserts value is number {
  if (value < min || value > max) {
    throw new Error(`${name}は${min}〜${max}の範囲内でなければなりません（実際: ${value}）`);
  }
}

function assertNonNull<T>(
  value: T | null | undefined,
  message?: string
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message ?? "値がnullまたはundefinedです");
  }
}

// バリデーション関数
interface RegistrationInput {
  name: string;
  age: number;
  email: string;
}

function validateRegistration(data: unknown): RegistrationInput {
  if (typeof data !== "object" || data === null) {
    throw new Error("入力はオブジェクトでなければなりません");
  }

  const obj = data as Record<string, unknown>;

  assertIsString(obj.name, "名前");
  assertIsString(obj.email, "メール");

  if (typeof obj.age !== "number") {
    throw new Error("年齢は数値でなければなりません");
  }
  assertInRange(obj.age, 1, 150, "年齢");

  // ここでobj.name, obj.emailはstring型、obj.ageはnumber型に絞り込まれている
  return { name: obj.name, email: obj.email, age: obj.age };
}

console.log("=== 4. アサーション関数 ===");

const testInputs: unknown[] = [
  { name: "太郎", age: 25, email: "taro@example.com" },
  { name: "花子", age: 200, email: "hanako@example.com" },
  { name: 42, age: 30, email: "test@test.com" },
  null,
];

testInputs.forEach((input, i) => {
  try {
    const validated = validateRegistration(input);
    console.log(`  入力${i + 1}: OK → ${validated.name}（${validated.age}歳）`);
  } catch (e) {
    console.log(`  入力${i + 1}: NG → ${(e as Error).message}`);
  }
});
console.log();

// =====================
// 5. 実践: APIレスポンスの型安全な処理
// =====================

// APIの状態を判別共用体で表現
type ApiState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T; fetchedAt: Date }
  | { status: "error"; error: { code: number; message: string }; retryCount: number };

// 状態に応じた処理
function renderState<T>(state: ApiState<T>, renderData: (data: T) => string): string {
  switch (state.status) {
    case "idle":
      return "待機中...";
    case "loading":
      return "読み込み中...";
    case "success":
      return `${renderData(state.data)}（${state.fetchedAt.toLocaleTimeString()}取得）`;
    case "error":
      return `エラー [${state.error.code}]: ${state.error.message}（リトライ: ${state.retryCount}回）`;
  }
}

console.log("=== 5. APIレスポンスの型安全な処理 ===");

interface UserList {
  users: { name: string; active: boolean }[];
  total: number;
}

const states: ApiState<UserList>[] = [
  { status: "idle" },
  { status: "loading" },
  {
    status: "success",
    data: {
      users: [
        { name: "太郎", active: true },
        { name: "花子", active: false },
        { name: "次郎", active: true },
      ],
      total: 3,
    },
    fetchedAt: new Date(),
  },
  {
    status: "error",
    error: { code: 503, message: "サービス利用不可" },
    retryCount: 2,
  },
];

states.forEach((state) => {
  const rendered = renderState(state, (data) => {
    const activeCount = data.users.filter((u) => u.active).length;
    return `ユーザー${data.total}名（アクティブ: ${activeCount}名）`;
  });
  console.log(`  [${state.status}] ${rendered}`);
});
console.log();

// =====================
// 6. 早期リターンパターン
// =====================

interface OrderItem {
  productName: string;
  quantity: number;
  unitPrice: number;
}

interface Order {
  id: string;
  customer?: {
    name: string;
    email?: string;
    membership?: "gold" | "silver" | "bronze";
  };
  items?: OrderItem[];
  couponCode?: string;
}

// 早期リターンで段階的に型を絞り込む
function processOrder(order: Order | null | undefined): string {
  if (!order) return "注文情報がありません";
  if (!order.customer) return `注文 ${order.id}: 顧客情報が未設定です`;
  if (!order.items || order.items.length === 0) {
    return `注文 ${order.id}: 商品が選択されていません`;
  }

  // ここまで来ると、order.customer と order.items は確実に存在する
  const subtotal = order.items.reduce(
    (sum, item) => sum + item.quantity * item.unitPrice,
    0
  );

  // メンバーシップ割引
  const discountRate =
    order.customer.membership === "gold" ? 0.1
    : order.customer.membership === "silver" ? 0.05
    : 0;

  const discount = Math.floor(subtotal * discountRate);
  const total = subtotal - discount;

  const lines: string[] = [
    `注文 ${order.id}（${order.customer.name}様）`,
    ...order.items.map(
      (item) => `  ${item.productName} x${item.quantity} = ¥${(item.quantity * item.unitPrice).toLocaleString()}`
    ),
    `  小計: ¥${subtotal.toLocaleString()}`,
  ];

  if (discount > 0) {
    lines.push(`  割引（${order.customer.membership}会員）: -¥${discount.toLocaleString()}`);
  }
  lines.push(`  合計: ¥${total.toLocaleString()}`);

  return lines.join("\n");
}

console.log("=== 6. 早期リターンパターン ===");

const orders: (Order | null)[] = [
  null,
  { id: "ORD-001" },
  { id: "ORD-002", customer: { name: "太郎" } },
  {
    id: "ORD-003",
    customer: { name: "花子", email: "hanako@example.com", membership: "gold" },
    items: [
      { productName: "TypeScript入門書", quantity: 1, unitPrice: 3200 },
      { productName: "メカニカルキーボード", quantity: 1, unitPrice: 12800 },
    ],
  },
];

orders.forEach((order) => {
  console.log(processOrder(order));
  console.log("---");
});
