// ==============================
// ユーティリティ型活用サンプル
// 第8章：ユーティリティ型の総合サンプル
// ==============================
// 学べる内容:
//   - Partial, Required, Readonly の使い方
//   - Pick, Omit による型の選択と除外
//   - Record によるマッピング型の作成
//   - Exclude, Extract によるユニオン型の操作
//   - ReturnType, Parameters の活用
//   - ユーティリティ型の組み合わせ
//   - カスタムユーティリティ型の自作
//   - 実践的なCRUD型設計パターン
// 実行方法:
//   npx tsc 05_ユーティリティ型活用.ts && node 05_ユーティリティ型活用.js
//   または: npx ts-node 05_ユーティリティ型活用.ts
// ==============================

// =====================
// 1. 基本のユーティリティ型
// =====================

interface User {
  id: number;
  name: string;
  email: string;
  age: number;
  role: "admin" | "editor" | "viewer";
  createdAt: Date;
  updatedAt: Date;
}

// --- Partial: 部分更新 ---
function updateUser(current: User, updates: Partial<User>): User {
  return { ...current, ...updates, updatedAt: new Date() };
}

// --- Readonly: 不変データの保護 ---
function freezeUser(user: User): Readonly<User> {
  return Object.freeze({ ...user });
}

const baseUser: User = {
  id: 1,
  name: "太郎",
  email: "taro@example.com",
  age: 25,
  role: "editor",
  createdAt: new Date("2025-01-01"),
  updatedAt: new Date("2025-01-01"),
};

console.log("=== 1. Partial / Readonly ===");
const updated = updateUser(baseUser, { name: "太郎（更新済み）", age: 26 });
console.log(`更新前: ${baseUser.name}（${baseUser.age}歳）`);
console.log(`更新後: ${updated.name}（${updated.age}歳）`);

const frozen = freezeUser(baseUser);
// frozen.name = "変更不可"; // エラー！Readonlyなので変更できない
console.log(`凍結済み: ${frozen.name}（変更不可）`);
console.log();

// =====================
// 2. Pick / Omit で型を派生
// =====================

// Pick: 必要なプロパティだけ抽出
type UserSummary = Pick<User, "id" | "name" | "role">;

// Omit: 不要なプロパティを除外
type CreateUserInput = Omit<User, "id" | "createdAt" | "updatedAt">;
type UpdateUserInput = Partial<CreateUserInput>;

// 新規作成関数
function createUser(input: CreateUserInput): User {
  const now = new Date();
  return {
    id: Math.floor(Math.random() * 10000),
    ...input,
    createdAt: now,
    updatedAt: now,
  };
}

console.log("=== 2. Pick / Omit ===");

const summary: UserSummary = { id: 1, name: "太郎", role: "admin" };
console.log(`概要: #${summary.id} ${summary.name} [${summary.role}]`);

const newUser = createUser({
  name: "花子",
  email: "hanako@example.com",
  age: 28,
  role: "viewer",
});
console.log(`新規作成: #${newUser.id} ${newUser.name} [${newUser.role}]`);
console.log();

// =====================
// 3. Record でマッピング
// =====================

// ロールごとの権限定義
type Permission = "read" | "write" | "delete" | "manage";
type RolePermissions = Record<User["role"], Permission[]>;

const permissions: RolePermissions = {
  admin: ["read", "write", "delete", "manage"],
  editor: ["read", "write"],
  viewer: ["read"],
};

// ステータスコードのメッセージ
type HttpStatus = 200 | 201 | 400 | 401 | 404 | 500;
const statusMessages: Record<HttpStatus, string> = {
  200: "OK",
  201: "Created",
  400: "Bad Request",
  401: "Unauthorized",
  404: "Not Found",
  500: "Internal Server Error",
};

console.log("=== 3. Record ===");
console.log("権限テーブル:");
(Object.entries(permissions) as [User["role"], Permission[]][]).forEach(
  ([role, perms]) => {
    console.log(`  ${role}: ${perms.join(", ")}`);
  }
);

function hasPermission(role: User["role"], action: Permission): boolean {
  return permissions[role].includes(action);
}

console.log(`\neditor は write 可能? ${hasPermission("editor", "write")}`);
console.log(`viewer は delete 可能? ${hasPermission("viewer", "delete")}`);
console.log();

// =====================
// 4. Exclude / Extract / NonNullable
// =====================

type AllEvents = "click" | "hover" | "keydown" | "keyup" | "scroll" | "resize";
type MouseEvents = Extract<AllEvents, "click" | "hover" | "scroll">;
type NonMouseEvents = Exclude<AllEvents, "click" | "hover" | "scroll">;

console.log("=== 4. Exclude / Extract ===");

const mouseEvents: MouseEvents[] = ["click", "hover", "scroll"];
const keyEvents: NonMouseEvents[] = ["keydown", "keyup", "resize"];

console.log(`マウスイベント: ${mouseEvents.join(", ")}`);
console.log(`非マウスイベント: ${keyEvents.join(", ")}`);

// NonNullable
type MaybeValues = string | number | null | undefined;
type DefiniteValues = NonNullable<MaybeValues>; // string | number

const values: MaybeValues[] = ["hello", 42, null, undefined, "world"];
const definite: DefiniteValues[] = values.filter(
  (v): v is DefiniteValues => v !== null && v !== undefined
);
console.log(`\nNonNullable: [${values.join(", ")}] → [${definite.join(", ")}]`);
console.log();

// =====================
// 5. ReturnType / Parameters
// =====================

// 既存の関数
function fetchUserData(userId: number, includeProfile: boolean) {
  return {
    id: userId,
    name: `User-${userId}`,
    profile: includeProfile ? { bio: "..." } : null,
    fetchedAt: new Date(),
  };
}

// 関数の型情報を取得
type UserData = ReturnType<typeof fetchUserData>;
type FetchParams = Parameters<typeof fetchUserData>;

// ログ付きラッパー
function fetchWithLogging(
  ...args: FetchParams
): UserData {
  console.log(`  API呼び出し: userId=${args[0]}, includeProfile=${args[1]}`);
  const result = fetchUserData(...args);
  console.log(`  結果: ${result.name}（プロフィール: ${result.profile ? "あり" : "なし"}）`);
  return result;
}

console.log("=== 5. ReturnType / Parameters ===");
fetchWithLogging(42, true);
fetchWithLogging(99, false);
console.log();

// =====================
// 6. カスタムユーティリティ型
// =====================

// 指定プロパティだけオプショナルにする
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// 指定プロパティだけ必須にする
type RequiredBy<T, K extends keyof T> = T & Required<Pick<T, K>>;

// 安全なOmit（存在しないキーを指定するとエラー）
type StrictOmit<T, K extends keyof T> = Omit<T, K>;

// 全プロパティをNullable（T | null）にする
type NullableAll<T> = {
  [K in keyof T]: T[K] | null;
};

console.log("=== 6. カスタムユーティリティ型 ===");

// PartialBy: emailとageだけオプショナル
type UserWithOptionalContact = PartialBy<User, "email" | "age">;
const partialUser: UserWithOptionalContact = {
  id: 1,
  name: "太郎",
  role: "viewer",
  createdAt: new Date(),
  updatedAt: new Date(),
  // email と age は省略可能
};
console.log(`PartialBy: ${partialUser.name}（email省略OK）`);

// NullableAll: フォーム入力の初期状態
type FormState = NullableAll<Pick<User, "name" | "email" | "age">>;
const initialForm: FormState = { name: null, email: null, age: null };
console.log(`NullableAll: ${JSON.stringify(initialForm)}`);
console.log();

// =====================
// 7. 実践: CRUD型セットの設計
// =====================

// エンティティの基底型
interface Entity {
  id: number;
  createdAt: Date;
  updatedAt: Date;
}

// CRUD操作に必要な型を自動生成
type CRUDTypes<T extends Entity> = {
  Full: T;
  Create: Omit<T, keyof Entity>;
  Update: Partial<Omit<T, keyof Entity>>;
  List: Pick<T, "id"> & Partial<Omit<T, "id">>;
};

// 商品エンティティ
interface Product extends Entity {
  name: string;
  price: number;
  category: string;
  stock: number;
  description: string;
}

// 型を自動導出
type ProductTypes = CRUDTypes<Product>;

// インメモリストア
class CRUDStore<T extends Entity> {
  private items: T[] = [];
  private nextId = 1;

  create(data: Omit<T, keyof Entity>): T {
    const now = new Date();
    const item = {
      ...data,
      id: this.nextId++,
      createdAt: now,
      updatedAt: now,
    } as T;
    this.items.push(item);
    return item;
  }

  findAll(): T[] {
    return [...this.items];
  }

  findById(id: number): T | undefined {
    return this.items.find((item) => item.id === id);
  }

  update(id: number, data: Partial<Omit<T, keyof Entity>>): T | undefined {
    const index = this.items.findIndex((item) => item.id === id);
    if (index === -1) return undefined;

    this.items[index] = {
      ...this.items[index],
      ...data,
      updatedAt: new Date(),
    };
    return this.items[index];
  }

  delete(id: number): boolean {
    const initialLength = this.items.length;
    this.items = this.items.filter((item) => item.id !== id);
    return this.items.length < initialLength;
  }
}

console.log("=== 7. CRUD型セット ===");

const productStore = new CRUDStore<Product>();

// Create
const p1 = productStore.create({
  name: "TypeScript実践ガイド",
  price: 3200,
  category: "書籍",
  stock: 50,
  description: "TypeScriptの実践的な使い方",
});
console.log(`作成: #${p1.id} ${p1.name} ¥${p1.price.toLocaleString()}`);

const p2 = productStore.create({
  name: "メカニカルキーボード",
  price: 12800,
  category: "周辺機器",
  stock: 30,
  description: "Cherry MX軸搭載",
});
console.log(`作成: #${p2.id} ${p2.name} ¥${p2.price.toLocaleString()}`);

const p3 = productStore.create({
  name: "USBハブ",
  price: 2500,
  category: "周辺機器",
  stock: 100,
  description: "USB 3.0対応 4ポート",
});
console.log(`作成: #${p3.id} ${p3.name} ¥${p3.price.toLocaleString()}`);

// Read
console.log(`\n全商品（${productStore.findAll().length}件）:`);
productStore.findAll().forEach((p) => {
  console.log(`  #${p.id} ${p.name} - ¥${p.price.toLocaleString()} (在庫: ${p.stock})`);
});

// Update
const updatedProduct = productStore.update(1, { price: 2800, stock: 45 });
if (updatedProduct) {
  console.log(`\n更新: #${updatedProduct.id} → ¥${updatedProduct.price.toLocaleString()} (在庫: ${updatedProduct.stock})`);
}

// Delete
const deleted = productStore.delete(3);
console.log(`\n削除(#3): ${deleted ? "成功" : "失敗"}`);
console.log(`残り: ${productStore.findAll().length}件`);
console.log();

// =====================
// 8. ユーティリティ型一覧のデモ
// =====================

console.log("=== 8. ユーティリティ型一覧 ===");
console.log("組み込みユーティリティ型:");
console.log("  Partial<T>      - 全プロパティをオプショナルに");
console.log("  Required<T>     - 全プロパティを必須に");
console.log("  Readonly<T>     - 全プロパティを読み取り専用に");
console.log("  Pick<T, K>      - 指定プロパティだけ抽出");
console.log("  Omit<T, K>      - 指定プロパティを除外");
console.log("  Record<K, V>    - キーと値の型を指定");
console.log("  Exclude<T, U>   - ユニオンから型を除外");
console.log("  Extract<T, U>   - ユニオンから型を抽出");
console.log("  NonNullable<T>  - null/undefinedを除外");
console.log("  ReturnType<T>   - 関数の戻り値型を取得");
console.log("  Parameters<T>   - 関数のパラメータ型を取得");
console.log("  Awaited<T>      - Promiseの中身の型を取得");
console.log();
console.log("カスタムユーティリティ型:");
console.log("  PartialBy<T, K>   - 指定プロパティだけオプショナル");
console.log("  RequiredBy<T, K>  - 指定プロパティだけ必須");
console.log("  StrictOmit<T, K>  - 存在しないキーでエラー");
console.log("  NullableAll<T>    - 全プロパティをnull許容に");
console.log("  CRUDTypes<T>      - CRUD操作用の型セット自動生成");
