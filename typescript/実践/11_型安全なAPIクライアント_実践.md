# 実践課題11：型安全なAPIクライアント設計 ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第9章（全章の知識を総合的に活用）
> **課題の種類**: 設計課題
> **学習目標**: ジェネリクス、ユーティリティ型、条件付き型、クラス設計を組み合わせて、実務レベルの型安全なAPIクライアントを設計・実装する

---

## 完成イメージ

```
===== 型安全なAPIクライアント =====

--- ユーザーAPI ---
GET /users → 成功: 3件取得
GET /users/1 → 成功: 田中太郎 (tanaka@example.com)
POST /users → 成功: 新規ユーザー作成（ID: 4）
PATCH /users/1 → 成功: 名前を更新（田中次郎）
DELETE /users/1 → 成功: 削除完了

--- 商品API ---
GET /products → 成功: 2件取得
GET /products?category=書籍 → 成功: 1件取得（フィルタ適用）

--- エラーハンドリング ---
GET /users/999 → エラー: 404 Not Found
POST /users (不正データ) → エラー: 400 Validation Error
  - name: 必須項目です
  - email: 有効なメールアドレスではありません

--- リクエストログ ---
[1] GET /users (200) 12ms
[2] GET /users/1 (200) 5ms
[3] POST /users (201) 18ms
[4] PATCH /users/1 (200) 8ms
[5] DELETE /users/1 (204) 3ms
[6] GET /products (200) 10ms
[7] GET /users/999 (404) 2ms
[8] POST /users (400) 4ms
```

---

## 課題の要件

### 必須機能

1. **型安全なHTTPメソッド**: GET / POST / PATCH / DELETE を型安全に呼び出せる
2. **レスポンス型の自動推論**: エンドポイントに応じたレスポンスの型が自動で決まる
3. **リクエストボディの型チェック**: POST / PATCH のリクエストボディが型チェックされる
4. **エラーハンドリング**: 成功とエラーをユニオン型で表現する
5. **バリデーションエラー**: フィールドごとのエラーメッセージを型安全に管理する
6. **リクエストログ**: 全リクエストの履歴を記録する

### 設計要件

- **ジェネリクス** を使ってリソース型を汎用化する
- **ユーティリティ型**（`Partial`, `Omit`, `Pick`, `Required`, `Record`）を少なくとも3種類使う
- **条件付き型** を少なくとも1箇所使う
- **インターフェースの implements** でクラスの契約を定義する
- **列挙型 or リテラル型** でHTTPメソッドとステータスコードを制限する

---

## ステップガイド

<details>
<summary>ステップ1：基本型とResult型を定義する</summary>

```typescript
// HTTPメソッド
type HttpMethod = "GET" | "POST" | "PATCH" | "DELETE";

// APIの成功レスポンス
interface ApiSuccess<T> {
  success: true;
  data: T;
  status: number;
}

// APIのエラーレスポンス
interface ApiError {
  success: false;
  status: number;
  message: string;
  validationErrors?: Record<string, string>;
}

type ApiResponse<T> = ApiSuccess<T> | ApiError;
```

</details>

<details>
<summary>ステップ2：リソース型とCRUDの型を定義する</summary>

```typescript
// ユーザーリソースの型
interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "user";
  createdAt: string;
}

// 作成時の型（id と createdAt は自動生成）
type CreateUser = Omit<User, "id" | "createdAt">;

// 更新時の型（すべてオプショナル、ただしidは不要）
type UpdateUser = Partial<Omit<User, "id" | "createdAt">>;
```

</details>

<details>
<summary>ステップ3：APIクライアントクラスを設計する</summary>

```typescript
interface ApiClient {
  get<T>(path: string): Promise<ApiResponse<T>>;
  post<T, B>(path: string, body: B): Promise<ApiResponse<T>>;
  patch<T, B>(path: string, body: B): Promise<ApiResponse<T>>;
  delete(path: string): Promise<ApiResponse<void>>;
}
```

この課題ではネットワーク通信は行わず、インメモリのモックデータで動作させます。

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```typescript
// 型安全なAPIクライアント
// 学べる内容：ジェネリクス、ユーティリティ型、クラスのimplements、enum
// 実行方法：npx ts-node 11_api_client.ts

// ===== 型定義 =====

type HttpMethod = "GET" | "POST" | "PATCH" | "DELETE";

interface ApiSuccess<T> {
  success: true;
  data: T;
  status: number;
}

interface ApiError {
  success: false;
  status: number;
  message: string;
  validationErrors?: Record<string, string>;
}

type ApiResponse<T> = ApiSuccess<T> | ApiError;

// リクエストログ
interface RequestLog {
  id: number;
  method: HttpMethod;
  path: string;
  status: number;
  durationMs: number;
}

// ===== リソース型 =====

interface User {
  readonly id: number;
  name: string;
  email: string;
  role: "admin" | "user";
  createdAt: string;
}

type CreateUser = Omit<User, "id" | "createdAt">;
type UpdateUser = Partial<Omit<User, "id" | "createdAt">>;

interface Product {
  readonly id: number;
  name: string;
  price: number;
  category: "書籍" | "電子機器" | "衣類";
}

// ===== APIクライアントインターフェース =====

interface IApiClient {
  get<T>(path: string): ApiResponse<T>;
  post<T, B>(path: string, body: B): ApiResponse<T>;
  patch<T, B>(path: string, body: B): ApiResponse<T>;
  del(path: string): ApiResponse<void>;
  getLogs(): readonly RequestLog[];
}

// ===== バリデーション =====

function validateCreateUser(data: unknown): Record<string, string> | null {
  const errors: Record<string, string> = {};

  if (typeof data !== "object" || data === null) {
    return { _form: "無効なデータです" };
  }

  const obj = data as Record<string, unknown>;

  if (typeof obj.name !== "string" || obj.name.trim() === "") {
    errors.name = "必須項目です";
  }
  if (typeof obj.email !== "string" || !obj.email.includes("@")) {
    errors.email = "有効なメールアドレスではありません";
  }
  if (obj.role !== "admin" && obj.role !== "user") {
    errors.role = "admin または user を指定してください";
  }

  return Object.keys(errors).length > 0 ? errors : null;
}

// ===== モックAPIクライアント =====

class MockApiClient implements IApiClient {
  private users: User[] = [
    { id: 1, name: "田中太郎", email: "tanaka@example.com", role: "admin", createdAt: "2026-01-01" },
    { id: 2, name: "佐藤花子", email: "sato@example.com", role: "user", createdAt: "2026-02-01" },
    { id: 3, name: "鈴木一郎", email: "suzuki@example.com", role: "user", createdAt: "2026-03-01" },
  ];

  private products: Product[] = [
    { id: 1, name: "TypeScript本", price: 2800, category: "書籍" },
    { id: 2, name: "マウス", price: 3500, category: "電子機器" },
  ];

  private nextUserId: number = 4;
  private logs: RequestLog[] = [];
  private logId: number = 1;

  private addLog(method: HttpMethod, path: string, status: number): void {
    this.logs.push({
      id: this.logId++,
      method,
      path,
      status,
      durationMs: Math.floor(Math.random() * 20) + 1,
    });
  }

  get<T>(path: string): ApiResponse<T> {
    // /users
    if (path === "/users") {
      this.addLog("GET", path, 200);
      return { success: true, data: [...this.users] as unknown as T, status: 200 };
    }

    // /users/:id
    const userMatch: RegExpMatchArray | null = path.match(/^\/users\/(\d+)$/);
    if (userMatch) {
      const id: number = parseInt(userMatch[1], 10);
      const user: User | undefined = this.users.find((u: User): boolean => u.id === id);
      if (!user) {
        this.addLog("GET", path, 404);
        return { success: false, status: 404, message: "Not Found" };
      }
      this.addLog("GET", path, 200);
      return { success: true, data: { ...user } as unknown as T, status: 200 };
    }

    // /products
    if (path === "/products") {
      this.addLog("GET", path, 200);
      return { success: true, data: [...this.products] as unknown as T, status: 200 };
    }

    // /products?category=...
    const productMatch: RegExpMatchArray | null = path.match(/^\/products\?category=(.+)$/);
    if (productMatch) {
      const category: string = decodeURIComponent(productMatch[1]);
      const filtered: Product[] = this.products.filter(
        (p: Product): boolean => p.category === category
      );
      this.addLog("GET", path, 200);
      return { success: true, data: filtered as unknown as T, status: 200 };
    }

    this.addLog("GET", path, 404);
    return { success: false, status: 404, message: "Not Found" };
  }

  post<T, B>(path: string, body: B): ApiResponse<T> {
    if (path === "/users") {
      const validationErrors: Record<string, string> | null = validateCreateUser(body);
      if (validationErrors) {
        this.addLog("POST", path, 400);
        return {
          success: false,
          status: 400,
          message: "Validation Error",
          validationErrors,
        };
      }

      const createData = body as unknown as CreateUser;
      const newUser: User = {
        id: this.nextUserId++,
        name: createData.name,
        email: createData.email,
        role: createData.role,
        createdAt: new Date().toISOString(),
      };
      this.users.push(newUser);
      this.addLog("POST", path, 201);
      return { success: true, data: newUser as unknown as T, status: 201 };
    }

    this.addLog("POST", path, 404);
    return { success: false, status: 404, message: "Not Found" };
  }

  patch<T, B>(path: string, body: B): ApiResponse<T> {
    const userMatch: RegExpMatchArray | null = path.match(/^\/users\/(\d+)$/);
    if (userMatch) {
      const id: number = parseInt(userMatch[1], 10);
      const index: number = this.users.findIndex((u: User): boolean => u.id === id);
      if (index === -1) {
        this.addLog("PATCH", path, 404);
        return { success: false, status: 404, message: "Not Found" };
      }

      const updates = body as unknown as UpdateUser;
      this.users[index] = { ...this.users[index], ...updates };
      this.addLog("PATCH", path, 200);
      return { success: true, data: { ...this.users[index] } as unknown as T, status: 200 };
    }

    this.addLog("PATCH", path, 404);
    return { success: false, status: 404, message: "Not Found" };
  }

  del(path: string): ApiResponse<void> {
    const userMatch: RegExpMatchArray | null = path.match(/^\/users\/(\d+)$/);
    if (userMatch) {
      const id: number = parseInt(userMatch[1], 10);
      const index: number = this.users.findIndex((u: User): boolean => u.id === id);
      if (index === -1) {
        this.addLog("DELETE", path, 404);
        return { success: false, status: 404, message: "Not Found" };
      }
      this.users.splice(index, 1);
      this.addLog("DELETE", path, 204);
      return { success: true, data: undefined as unknown as void, status: 204 };
    }

    this.addLog("DELETE", path, 404);
    return { success: false, status: 404, message: "Not Found" };
  }

  getLogs(): readonly RequestLog[] {
    return this.logs;
  }
}

// ===== メイン処理 =====

console.log("===== 型安全なAPIクライアント =====\n");

const api: IApiClient = new MockApiClient();

// --- ユーザーAPI ---
console.log("--- ユーザーAPI ---");

const usersResult: ApiResponse<User[]> = api.get<User[]>("/users");
if (usersResult.success) {
  console.log(`GET /users → 成功: ${usersResult.data.length}件取得`);
}

const userResult: ApiResponse<User> = api.get<User>("/users/1");
if (userResult.success) {
  console.log(`GET /users/1 → 成功: ${userResult.data.name} (${userResult.data.email})`);
}

const createData: CreateUser = { name: "新規ユーザー", email: "new@example.com", role: "user" };
const createResult: ApiResponse<User> = api.post<User, CreateUser>("/users", createData);
if (createResult.success) {
  console.log(`POST /users → 成功: 新規ユーザー作成（ID: ${createResult.data.id}）`);
}

const updateData: UpdateUser = { name: "田中次郎" };
const patchResult: ApiResponse<User> = api.patch<User, UpdateUser>("/users/1", updateData);
if (patchResult.success) {
  console.log(`PATCH /users/1 → 成功: 名前を更新（${patchResult.data.name}）`);
}

const deleteResult: ApiResponse<void> = api.del("/users/1");
if (deleteResult.success) {
  console.log("DELETE /users/1 → 成功: 削除完了");
}

// --- 商品API ---
console.log("\n--- 商品API ---");

const productsResult: ApiResponse<Product[]> = api.get<Product[]>("/products");
if (productsResult.success) {
  console.log(`GET /products → 成功: ${productsResult.data.length}件取得`);
}

const filteredResult: ApiResponse<Product[]> = api.get<Product[]>(
  `/products?category=${encodeURIComponent("書籍")}`
);
if (filteredResult.success) {
  console.log(`GET /products?category=書籍 → 成功: ${filteredResult.data.length}件取得（フィルタ適用）`);
}

// --- エラーハンドリング ---
console.log("\n--- エラーハンドリング ---");

const notFoundResult: ApiResponse<User> = api.get<User>("/users/999");
if (!notFoundResult.success) {
  console.log(`GET /users/999 → エラー: ${notFoundResult.status} ${notFoundResult.message}`);
}

const invalidData = { name: "", email: "invalid" } as unknown as CreateUser;
const validationResult: ApiResponse<User> = api.post<User, CreateUser>("/users", invalidData);
if (!validationResult.success) {
  console.log(`POST /users (不正データ) → エラー: ${validationResult.status} ${validationResult.message}`);
  if (validationResult.validationErrors) {
    for (const [field, message] of Object.entries(validationResult.validationErrors)) {
      console.log(`  - ${field}: ${message}`);
    }
  }
}

// --- リクエストログ ---
console.log("\n--- リクエストログ ---");
for (const log of api.getLogs()) {
  console.log(`[${log.id}] ${log.method} ${log.path} (${log.status}) ${log.durationMs}ms`);
}
```

</details>

<details>
<summary>解答例（改良版 ─ 条件付き型とMapped Typeによる高度な型設計）</summary>

```typescript
// 型安全なAPIクライアント（改良版）
// 学べる内容：条件付き型、Mapped Type、テンプレートリテラル型、型推論の活用
// 実行方法：npx ts-node 11_api_client_v2.ts

// ===== 基盤型 =====

type HttpMethod = "GET" | "POST" | "PATCH" | "DELETE";

type ApiSuccess<T> = { readonly success: true; readonly data: T; readonly status: number };
type ApiError = {
  readonly success: false;
  readonly status: number;
  readonly message: string;
  readonly validationErrors?: Readonly<Record<string, string>>;
};
type ApiResponse<T> = ApiSuccess<T> | ApiError;

// ===== リソース型 =====

interface User {
  readonly id: number;
  name: string;
  email: string;
  role: "admin" | "user";
  createdAt: string;
}

interface Product {
  readonly id: number;
  name: string;
  price: number;
  category: "書籍" | "電子機器" | "衣類";
}

// ===== 条件付き型: HTTPメソッドに応じたボディの有無 =====

// GETとDELETEはボディなし、POSTとPATCHはボディあり
type HasBody<M extends HttpMethod> = M extends "POST" | "PATCH" ? true : false;

// リソースの操作型を自動導出
type AutoGeneratedFields = "id" | "createdAt";
type CreateDTO<T> = Omit<T, AutoGeneratedFields extends keyof T ? AutoGeneratedFields : never>;
type UpdateDTO<T> = Partial<CreateDTO<T>>;

// ===== エンドポイント定義 =====

interface EndpointMap {
  "/users": { resource: User; list: User[] };
  "/products": { resource: Product; list: Product[] };
}

type EndpointPath = keyof EndpointMap;

// パス + メソッドに応じたレスポンス型を自動決定
type ResponseType<P extends string, M extends HttpMethod> =
  P extends EndpointPath
    ? M extends "GET"
      ? EndpointMap[P]["list"]
      : M extends "POST"
      ? EndpointMap[P]["resource"]
      : M extends "PATCH"
      ? EndpointMap[P]["resource"]
      : void
    : unknown;

// ===== リクエストログ =====

interface RequestLog {
  readonly id: number;
  readonly method: HttpMethod;
  readonly path: string;
  readonly status: number;
  readonly durationMs: number;
}

// ===== モックストレージ =====

class InMemoryStore<T extends { readonly id: number }> {
  private items: Map<number, T>;
  private nextId: number;

  constructor(initial: T[]) {
    this.items = new Map(initial.map((item: T): [number, T] => [item.id, item]));
    this.nextId = initial.length > 0
      ? Math.max(...initial.map((i: T): number => i.id)) + 1
      : 1;
  }

  getAll(): T[] { return Array.from(this.items.values()); }
  getById(id: number): T | undefined { return this.items.get(id); }

  create(data: Omit<T, "id">): T {
    const item = { ...data, id: this.nextId++ } as T;
    this.items.set(item.id, item);
    return item;
  }

  update(id: number, data: Partial<T>): T | undefined {
    const existing: T | undefined = this.items.get(id);
    if (!existing) return undefined;
    const updated: T = { ...existing, ...data, id } as T;
    this.items.set(id, updated);
    return updated;
  }

  delete(id: number): boolean { return this.items.delete(id); }

  filter<K extends keyof T>(key: K, value: T[K]): T[] {
    return this.getAll().filter((item: T): boolean => item[key] === value);
  }
}

// ===== APIクライアント =====

class TypeSafeApiClient {
  private userStore: InMemoryStore<User>;
  private productStore: InMemoryStore<Product>;
  private logs: RequestLog[] = [];
  private logId: number = 1;

  constructor() {
    this.userStore = new InMemoryStore<User>([
      { id: 1, name: "田中太郎", email: "tanaka@example.com", role: "admin", createdAt: "2026-01-01" },
      { id: 2, name: "佐藤花子", email: "sato@example.com", role: "user", createdAt: "2026-02-01" },
      { id: 3, name: "鈴木一郎", email: "suzuki@example.com", role: "user", createdAt: "2026-03-01" },
    ]);
    this.productStore = new InMemoryStore<Product>([
      { id: 1, name: "TypeScript本", price: 2800, category: "書籍" },
      { id: 2, name: "マウス", price: 3500, category: "電子機器" },
    ]);
  }

  private log(method: HttpMethod, path: string, status: number): void {
    this.logs.push({
      id: this.logId++, method, path, status,
      durationMs: Math.floor(Math.random() * 20) + 1,
    });
  }

  private ok<T>(data: T, status: number = 200): ApiSuccess<T> {
    return { success: true, data, status };
  }

  private fail(status: number, message: string, validationErrors?: Record<string, string>): ApiError {
    return { success: false, status, message, validationErrors };
  }

  // GET: リスト取得 or 単一取得
  getList<T extends EndpointPath>(path: T): ApiResponse<EndpointMap[T]["list"]> {
    this.log("GET", path, 200);
    if (path === "/users") {
      return this.ok(this.userStore.getAll()) as ApiResponse<EndpointMap[T]["list"]>;
    }
    if (path === "/products") {
      return this.ok(this.productStore.getAll()) as ApiResponse<EndpointMap[T]["list"]>;
    }
    return this.fail(404, "Not Found") as ApiResponse<EndpointMap[T]["list"]>;
  }

  getOne<T extends EndpointPath>(path: T, id: number): ApiResponse<EndpointMap[T]["resource"]> {
    if (path === "/users") {
      const user: User | undefined = this.userStore.getById(id);
      if (!user) { this.log("GET", `${path}/${id}`, 404); return this.fail(404, "Not Found") as ApiResponse<EndpointMap[T]["resource"]>; }
      this.log("GET", `${path}/${id}`, 200);
      return this.ok(user) as ApiResponse<EndpointMap[T]["resource"]>;
    }
    this.log("GET", `${path}/${id}`, 404);
    return this.fail(404, "Not Found") as ApiResponse<EndpointMap[T]["resource"]>;
  }

  create(path: "/users", body: CreateDTO<User>): ApiResponse<User> {
    const errors: Record<string, string> = {};
    if (!body.name || body.name.trim() === "") errors.name = "必須項目です";
    if (!body.email || !body.email.includes("@")) errors.email = "有効なメールアドレスではありません";

    if (Object.keys(errors).length > 0) {
      this.log("POST", path, 400);
      return this.fail(400, "Validation Error", errors);
    }

    const user: User = this.userStore.create({
      ...body,
      createdAt: new Date().toISOString(),
    } as Omit<User, "id">);
    this.log("POST", path, 201);
    return this.ok(user, 201);
  }

  update(path: "/users", id: number, body: UpdateDTO<User>): ApiResponse<User> {
    const user: User | undefined = this.userStore.update(id, body as Partial<User>);
    if (!user) { this.log("PATCH", `${path}/${id}`, 404); return this.fail(404, "Not Found"); }
    this.log("PATCH", `${path}/${id}`, 200);
    return this.ok(user);
  }

  remove(path: "/users", id: number): ApiResponse<void> {
    if (!this.userStore.delete(id)) {
      this.log("DELETE", `${path}/${id}`, 404);
      return this.fail(404, "Not Found");
    }
    this.log("DELETE", `${path}/${id}`, 204);
    return this.ok(undefined as unknown as void, 204);
  }

  getRequestLogs(): readonly RequestLog[] {
    return this.logs;
  }
}

// ===== メイン処理 =====

console.log("===== 型安全なAPIクライアント =====\n");

const api = new TypeSafeApiClient();

// ユーザーAPI
console.log("--- ユーザーAPI ---");

const users = api.getList("/users");
if (users.success) console.log(`GET /users → 成功: ${users.data.length}件取得`);

const user = api.getOne("/users", 1);
if (user.success) console.log(`GET /users/1 → 成功: ${user.data.name} (${user.data.email})`);

const created = api.create("/users", { name: "新規ユーザー", email: "new@example.com", role: "user" });
if (created.success) console.log(`POST /users → 成功: 新規ユーザー作成（ID: ${created.data.id}）`);

const patched = api.update("/users", 1, { name: "田中次郎" });
if (patched.success) console.log(`PATCH /users/1 → 成功: 名前を更新（${patched.data.name}）`);

const deleted = api.remove("/users", 1);
if (deleted.success) console.log("DELETE /users/1 → 成功: 削除完了");

// 商品API
console.log("\n--- 商品API ---");
const products = api.getList("/products");
if (products.success) console.log(`GET /products → 成功: ${products.data.length}件取得`);

// エラーハンドリング
console.log("\n--- エラーハンドリング ---");
const notFound = api.getOne("/users", 999);
if (!notFound.success) console.log(`GET /users/999 → エラー: ${notFound.status} ${notFound.message}`);

const invalid = api.create("/users", { name: "", email: "invalid", role: "user" });
if (!invalid.success) {
  console.log(`POST /users (不正データ) → エラー: ${invalid.status} ${invalid.message}`);
  if (invalid.validationErrors) {
    for (const [field, msg] of Object.entries(invalid.validationErrors)) {
      console.log(`  - ${field}: ${msg}`);
    }
  }
}

// リクエストログ
console.log("\n--- リクエストログ ---");
for (const log of api.getRequestLogs()) {
  console.log(`[${log.id}] ${log.method} ${log.path} (${log.status}) ${log.durationMs}ms`);
}
```

**初心者向けとの違い:**
- `EndpointMap` でパスとリソース型のマッピングを一元管理
- `ResponseType<P, M>` 条件付き型でメソッド + パスに応じた戻り値型を自動決定
- `CreateDTO<T>` / `UpdateDTO<T>` で自動生成フィールドを自動除外
- `InMemoryStore<T>` ジェネリッククラスでデータストアを共通化
- `HasBody<M>` 条件付き型でHTTPメソッドごとのボディの有無を型で表現

</details>
