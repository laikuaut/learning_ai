# 第7章 演習：実践的なMCPサーバーの構築

---

## 基本問題

---

### 問題1：MCPサーバー設計の要件整理（基本）

あなたは「社内の会議室予約システム」をMCPサーバーとして構築する依頼を受けました。以下の要件を整理してください。

1. このシステムに必要なツール（Tools）を3つ以上挙げてください
2. このシステムに必要なリソース（Resources）を2つ以上挙げてください
3. 各ツールの入力パラメータと戻り値の型を定義してください

**期待される出力例：**
```
=== 会議室予約MCPサーバー 要件定義 ===

【ツール一覧】
1. book_room
   - 説明: 会議室を予約する
   - 入力: room_id (string), date (string), start_time (string), end_time (string), title (string)
   - 戻り値: { booking_id: string, status: "confirmed" | "conflict" }

2. cancel_booking
   - 説明: 予約をキャンセルする
   - 入力: booking_id (string)
   - 戻り値: { status: "cancelled" | "not_found" }

3. list_available_rooms
   - 説明: 指定日時で空いている会議室を一覧する
   - 入力: date (string), start_time (string), end_time (string)
   - 戻り値: { rooms: Array<{ room_id: string, name: string, capacity: number }> }

【リソース一覧】
1. rooms://list
   - 説明: 全会議室の一覧（静的データ）
   - MIMEタイプ: application/json

2. bookings://today
   - 説明: 本日の予約一覧
   - MIMEタイプ: application/json
```

<details>
<summary>ヒント</summary>

MCPのツールは「副作用を伴う操作」、リソースは「データの読み取り」に適しています。会議室予約で必要な操作を「作成・読み取り・更新・削除」の観点で洗い出しましょう。

</details>

<details>
<summary>解答例</summary>

```
=== 会議室予約MCPサーバー 要件定義 ===

【ツール一覧】
1. book_room
   - 説明: 会議室を予約する
   - 入力: room_id (string), date (string), start_time (string),
           end_time (string), title (string), organizer (string)
   - 戻り値: { booking_id: string, status: "confirmed" | "conflict" }

2. cancel_booking
   - 説明: 予約をキャンセルする
   - 入力: booking_id (string), reason? (string)
   - 戻り値: { status: "cancelled" | "not_found" }

3. update_booking
   - 説明: 予約内容を更新する
   - 入力: booking_id (string), updates: { start_time?, end_time?, title? }
   - 戻り値: { status: "updated" | "conflict" | "not_found" }

4. list_available_rooms
   - 説明: 指定日時で空いている会議室を一覧する
   - 入力: date (string), start_time (string), end_time (string),
           min_capacity? (number)
   - 戻り値: { rooms: Array<{ room_id, name, capacity, equipment }> }

【リソース一覧】
1. rooms://list
   - 説明: 全会議室の基本情報一覧（名前、場所、収容人数、設備）
   - MIMEタイプ: application/json

2. bookings://today
   - 説明: 本日の予約一覧
   - MIMEタイプ: application/json

3. bookings://{room_id}/{date}
   - 説明: 特定会議室の特定日の予約スケジュール
   - MIMEタイプ: application/json
   - ※ URIテンプレートでリソースを動的に提供

# ポイント：
# - ツールは状態を変更する操作（予約・キャンセル・更新）に使います
# - リソースは情報の読み取り（一覧取得・スケジュール参照）に使います
# - URIテンプレートを使うと、パラメータ付きのリソースを柔軟に提供できます
# - オプショナルパラメータ（?付き）で使いやすさを向上させます
```

</details>

---

### 問題2：ツールとリソースの粒度判断（基本）

以下のMCPサーバー設計案について、ツールとリソースの粒度（granularity）が適切かどうかを判断し、問題点と改善案を述べてください。

```typescript
// 設計案A：粒度が粗すぎる例
server.tool("manage_database", {
  action: z.enum(["create", "read", "update", "delete", "search", "export", "import"]),
  table: z.string(),
  data: z.any()
}, async ({ action, table, data }) => {
  // 全操作を1つのツールで処理
});

// 設計案B：粒度が細かすぎる例
server.tool("set_user_name", { id: z.string(), name: z.string() }, ...);
server.tool("set_user_email", { id: z.string(), email: z.string() }, ...);
server.tool("set_user_age", { id: z.string(), age: z.number() }, ...);
server.tool("set_user_role", { id: z.string(), role: z.string() }, ...);
// ... フィールドごとに1つのツール
```

**期待される出力例：**
```
=== 設計案A の分析 ===
問題点:
- 1つのツールに責務が集中しすぎている
- LLMがパラメータの使い分けを正しく判断しにくい
- data が any型のため、バリデーションが困難

改善案:
- CRUD操作ごとに個別のツールに分割する
  例: create_record, get_record, update_record, delete_record, search_records

=== 設計案B の分析 ===
問題点:
- ツール数が多すぎてLLMの選択負荷が高い
- 複数フィールドの同時更新に複数回の呼び出しが必要

改善案:
- update_user として1つにまとめ、更新対象をオプショナルパラメータにする
```

<details>
<summary>ヒント</summary>

MCPツールの適切な粒度を判断するポイントは以下の通りです。
- LLMが「いつこのツールを使うべきか」を容易に判断できるか
- 1つのツールが「1つの明確な責務」を持っているか
- パラメータの型が明確に定義されているか（anyは避ける）
- ツール数が多すぎてLLMが混乱しないか（目安：15〜20個以内）

</details>

<details>
<summary>解答例</summary>

```
=== 設計案A の分析 ===

問題点:
1. 単一責任の原則に違反しています
   - 7つの異なる操作を1つのツールに詰め込んでおり、
     LLMがパラメータの正しい組み合わせを推論しにくくなります

2. パラメータの型安全性が低いです
   - data が z.any() のため、操作ごとに異なるデータ構造を
     バリデーションできません
   - LLMへのスキーマ情報が不十分になります

3. エラーハンドリングが複雑化します
   - 操作ごとに異なるエラーパターンを1つの関数で処理する必要があります

4. ツールの説明文（description）が曖昧になります
   - 「データベースを管理する」では、LLMが具体的な使い所を判断できません

改善案:
  server.tool("create_record",
    { table: z.string(), data: z.record(z.unknown()) },
    async (params) => { /* 作成処理 */ }
  );
  server.tool("get_record",
    { table: z.string(), id: z.string() },
    async (params) => { /* 取得処理 */ }
  );
  server.tool("update_record",
    { table: z.string(), id: z.string(), data: z.record(z.unknown()) },
    async (params) => { /* 更新処理 */ }
  );
  server.tool("delete_record",
    { table: z.string(), id: z.string() },
    async (params) => { /* 削除処理 */ }
  );
  server.tool("search_records",
    { table: z.string(), query: z.string(), limit: z.number().optional() },
    async (params) => { /* 検索処理 */ }
  );

=== 設計案B の分析 ===

問題点:
1. ツール数の爆発
   - ユーザーモデルのフィールドが10個あれば10個のツールが必要になります
   - LLMが適切なツールを選択するコストが増大します

2. 複合操作の非効率性
   - 名前とメールを同時に変更するだけで2回のツール呼び出しが必要です
   - 各呼び出し間でデータの不整合が発生するリスクがあります

3. トランザクションの問題
   - 途中で1つの更新が失敗した場合、部分的な更新状態になります

改善案:
  server.tool("update_user", {
    id: z.string(),
    updates: z.object({
      name: z.string().optional(),
      email: z.string().email().optional(),
      age: z.number().min(0).optional(),
      role: z.enum(["admin", "user", "viewer"]).optional()
    })
  }, async ({ id, updates }) => {
    // オプショナルパラメータで柔軟に対応
    // 渡されたフィールドのみ更新する
  });

# まとめ：適切な粒度の目安
# - 1ツール = 1つの明確なアクション（動詞1つで表せること）
# - パラメータは具体的な型で定義する（anyは避ける）
# - 関連する操作はオプショナルパラメータで柔軟に対応
# - ツール総数は15〜20個程度を上限の目安にする
```

</details>

---

### 問題3：MCPサーバーのテスト手法（基本）

以下のMCPサーバーのツール実装に対して、適切なテストケースを設計してください。正常系・異常系・境界値の観点から最低5つのテストケースを挙げてください。

```typescript
server.tool(
  "search_products",
  {
    query: z.string().min(1).max(100),
    category: z.enum(["electronics", "books", "clothing"]).optional(),
    min_price: z.number().min(0).optional(),
    max_price: z.number().min(0).optional(),
    limit: z.number().min(1).max(50).default(10)
  },
  async ({ query, category, min_price, max_price, limit }) => {
    // 商品検索処理
  }
);
```

**期待される出力例：**
```
=== テストケース一覧 ===

【正常系】
1. 基本検索: query="laptop" のみ指定 → 結果が返ること
2. フィルタ付き検索: query="phone", category="electronics", max_price=50000
   → electronics カテゴリかつ50000円以下の結果のみ

【異常系】
3. 空文字クエリ: query="" → バリデーションエラー
...
```

<details>
<summary>ヒント</summary>

テストケース設計では以下の観点を考慮しましょう。
- 正常系：最小パラメータ、全パラメータ指定、各カテゴリでの検索
- 異常系：バリデーション違反、存在しないカテゴリ
- 境界値：文字列長の上限/下限、価格の0、limitの上限/下限
- 組み合わせ：min_price > max_price のような矛盾するパラメータ

</details>

<details>
<summary>解答例</summary>

```
=== テストケース一覧 ===

【正常系】
1. 基本検索（最小パラメータ）
   入力: { query: "laptop" }
   期待: 検索結果の配列が返る、デフォルトlimit=10件以下
   確認: レスポンスのisError が false であること

2. 全パラメータ指定
   入力: { query: "smartphone", category: "electronics",
           min_price: 10000, max_price: 50000, limit: 5 }
   期待: electronicsカテゴリ、10000〜50000円、最大5件の結果
   確認: 全フィルタ条件が反映されていること

3. カテゴリフィルタのみ
   入力: { query: "gift", category: "books" }
   期待: booksカテゴリの商品のみが返ること
   確認: 結果のcategoryが全て"books"であること

4. 検索結果が0件の場合
   入力: { query: "xyznonexistent12345" }
   期待: 空の配列が返る（エラーではない）
   確認: isError が false、結果が空配列

【異常系】
5. 空文字クエリ（バリデーション違反）
   入力: { query: "" }
   期待: バリデーションエラー
   確認: z.string().min(1) による拒否

6. クエリ文字数超過
   入力: { query: "a".repeat(101) }
   期待: バリデーションエラー
   確認: z.string().max(100) による拒否

7. 不正なカテゴリ
   入力: { query: "item", category: "food" }
   期待: バリデーションエラー
   確認: z.enum() による拒否

8. 負の価格
   入力: { query: "item", min_price: -100 }
   期待: バリデーションエラー
   確認: z.number().min(0) による拒否

【境界値】
9. limit の上限
   入力: { query: "item", limit: 50 }
   期待: 最大50件まで正常に返ること

10. limit の上限超過
    入力: { query: "item", limit: 51 }
    期待: バリデーションエラー

11. 価格範囲の矛盾
    入力: { query: "item", min_price: 50000, max_price: 10000 }
    期待: 空の結果 or ビジネスロジックエラー
    確認: min > max の場合の挙動を明確に定義すべき

【統合テスト】
12. MCP Inspector を使った手動テスト
    手順: npx @modelcontextprotocol/inspector でサーバーに接続し、
          各ツールをGUIから呼び出してレスポンスを確認する

# テスト実装のポイント:
# - MCPサーバーのテストはMCP SDKの Client を使って行えます
# - server.tool のハンドラ関数を単体テストすることも有効です
# - MCP Inspector はデバッグ・手動テストに非常に便利です
# - 境界値テストはバリデーションの品質を担保する上で重要です
```

</details>

---

## 応用問題

---

### 問題4：タスク管理MCPサーバーの設計と実装（応用）

以下の要件を満たすタスク管理MCPサーバーを設計・実装してください。

**要件：**
- タスクのCRUD操作（作成・取得・更新・削除）
- ステータス別の検索（todo / in_progress / done）
- 優先度（high / medium / low）によるフィルタリング
- タスクデータはインメモリで管理（Map使用）

**期待される出力例：**
```typescript
// サーバー起動後、以下のようなやりとりが可能：

// タスク作成
> create_task({ title: "MCPの学習", priority: "high" })
{ task_id: "task_1", status: "created" }

// タスク一覧（フィルタ付き）
> list_tasks({ status: "todo", priority: "high" })
{ tasks: [{ id: "task_1", title: "MCPの学習", priority: "high", status: "todo" }] }

// タスク更新
> update_task({ task_id: "task_1", status: "in_progress" })
{ status: "updated" }

// タスク削除
> delete_task({ task_id: "task_1" })
{ status: "deleted" }
```

<details>
<summary>ヒント</summary>

1. まずタスクのデータモデル（型定義）を設計しましょう
2. `Map<string, Task>` でインメモリストレージを実装します
3. 各CRUD操作を個別のツールとして登録します
4. 検索用のリソースも定義すると便利です
5. IDの自動採番にはカウンターやUUIDを使います

</details>

<details>
<summary>解答例</summary>

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// --- データモデル定義 ---
interface Task {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in_progress" | "done";
  priority: "high" | "medium" | "low";
  createdAt: string;
  updatedAt: string;
}

// --- インメモリストレージ ---
const tasks = new Map<string, Task>();
let taskCounter = 0;

// ヘルパー: 一意なIDを生成する
function generateId(): string {
  taskCounter++;
  return `task_${taskCounter}`;
}

// --- MCPサーバーの初期化 ---
const server = new McpServer({
  name: "task-manager",
  version: "1.0.0",
});

// --- ツール1: タスク作成 ---
server.tool(
  "create_task",
  "新しいタスクを作成します",
  {
    title: z.string().min(1).max(200).describe("タスクのタイトル"),
    description: z.string().max(1000).default("").describe("タスクの詳細説明"),
    priority: z.enum(["high", "medium", "low"]).default("medium")
      .describe("優先度"),
  },
  async ({ title, description, priority }) => {
    const id = generateId();
    const now = new Date().toISOString();

    const task: Task = {
      id,
      title,
      description,
      status: "todo",      // 新規作成時は必ず todo
      priority,
      createdAt: now,
      updatedAt: now,
    };

    tasks.set(id, task);

    return {
      content: [{
        type: "text" as const,
        text: JSON.stringify({ task_id: id, status: "created", task }, null, 2),
      }],
    };
  }
);

// --- ツール2: タスク取得 ---
server.tool(
  "get_task",
  "指定したIDのタスクを取得します",
  {
    task_id: z.string().describe("タスクID"),
  },
  async ({ task_id }) => {
    const task = tasks.get(task_id);

    if (!task) {
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({ error: "タスクが見つかりません", task_id }),
        }],
        isError: true,  // エラー時はisErrorをtrueにする
      };
    }

    return {
      content: [{
        type: "text" as const,
        text: JSON.stringify(task, null, 2),
      }],
    };
  }
);

// --- ツール3: タスク更新 ---
server.tool(
  "update_task",
  "既存タスクのステータスや内容を更新します",
  {
    task_id: z.string().describe("タスクID"),
    title: z.string().min(1).max(200).optional().describe("新しいタイトル"),
    description: z.string().max(1000).optional().describe("新しい説明"),
    status: z.enum(["todo", "in_progress", "done"]).optional()
      .describe("新しいステータス"),
    priority: z.enum(["high", "medium", "low"]).optional()
      .describe("新しい優先度"),
  },
  async ({ task_id, title, description, status, priority }) => {
    const task = tasks.get(task_id);

    if (!task) {
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({ error: "タスクが見つかりません", task_id }),
        }],
        isError: true,
      };
    }

    // 渡されたフィールドのみ更新する
    if (title !== undefined) task.title = title;
    if (description !== undefined) task.description = description;
    if (status !== undefined) task.status = status;
    if (priority !== undefined) task.priority = priority;
    task.updatedAt = new Date().toISOString();

    return {
      content: [{
        type: "text" as const,
        text: JSON.stringify({ status: "updated", task }, null, 2),
      }],
    };
  }
);

// --- ツール4: タスク削除 ---
server.tool(
  "delete_task",
  "指定したIDのタスクを削除します",
  {
    task_id: z.string().describe("タスクID"),
  },
  async ({ task_id }) => {
    if (!tasks.has(task_id)) {
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({ error: "タスクが見つかりません", task_id }),
        }],
        isError: true,
      };
    }

    tasks.delete(task_id);

    return {
      content: [{
        type: "text" as const,
        text: JSON.stringify({ status: "deleted", task_id }),
      }],
    };
  }
);

// --- ツール5: タスク検索（フィルタ付き一覧） ---
server.tool(
  "list_tasks",
  "条件に合うタスクを一覧します。フィルタなしで全件取得も可能です",
  {
    status: z.enum(["todo", "in_progress", "done"]).optional()
      .describe("ステータスでフィルタ"),
    priority: z.enum(["high", "medium", "low"]).optional()
      .describe("優先度でフィルタ"),
    limit: z.number().min(1).max(100).default(20)
      .describe("取得件数の上限"),
  },
  async ({ status, priority, limit }) => {
    let results = Array.from(tasks.values());

    // フィルタリング
    if (status) {
      results = results.filter((t) => t.status === status);
    }
    if (priority) {
      results = results.filter((t) => t.priority === priority);
    }

    // 件数制限
    results = results.slice(0, limit);

    return {
      content: [{
        type: "text" as const,
        text: JSON.stringify({
          total: results.length,
          tasks: results,
        }, null, 2),
      }],
    };
  }
);

// --- リソース: タスクサマリ ---
server.resource(
  "tasks-summary",
  "tasks://summary",
  async (uri) => {
    const all = Array.from(tasks.values());
    const summary = {
      total: all.length,
      by_status: {
        todo: all.filter((t) => t.status === "todo").length,
        in_progress: all.filter((t) => t.status === "in_progress").length,
        done: all.filter((t) => t.status === "done").length,
      },
      by_priority: {
        high: all.filter((t) => t.priority === "high").length,
        medium: all.filter((t) => t.priority === "medium").length,
        low: all.filter((t) => t.priority === "low").length,
      },
    };
    return {
      contents: [{
        uri: uri.href,
        mimeType: "application/json",
        text: JSON.stringify(summary, null, 2),
      }],
    };
  }
);

// --- サーバー起動 ---
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Task Manager MCP Server is running");
}

main().catch(console.error);

// 設計のポイント:
// 1. 各ツールは1つの明確な操作に対応しています（単一責任）
// 2. zodスキーマで入力を厳密にバリデーションしています
// 3. エラー時は isError: true を返してLLMに失敗を伝えます
// 4. リソースでタスクのサマリ情報を提供しています
// 5. describe() でLLMにパラメータの意味を伝えています
```

</details>

---

### 問題5：外部API連携MCPサーバーの設計（応用）

天気情報APIと連携するMCPサーバーを設計・実装してください。以下の要件を満たすこと。

**要件：**
- 都市名から現在の天気情報を取得するツール
- APIキーの安全な管理（環境変数から読み取り）
- レート制限の実装（1分間に最大10リクエスト）
- APIエラー時の適切なエラーハンドリング
- リトライ機構（最大3回、指数バックオフ）

**期待される出力例：**
```typescript
// 正常時
> get_weather({ city: "Tokyo" })
{ city: "Tokyo", temp: 18.5, description: "晴れ", humidity: 45 }

// レート制限超過時
> get_weather({ city: "Osaka" })
{ error: "レート制限に達しました。56秒後に再試行してください" }

// APIエラー時（リトライ後も失敗）
> get_weather({ city: "InvalidCity" })
{ error: "天気情報の取得に失敗しました", details: "都市が見つかりません" }
```

<details>
<summary>ヒント</summary>

1. レート制限にはスライディングウィンドウ方式が実用的です
   - リクエストのタイムスタンプを配列で記録し、1分以上前のものを除去します
2. 指数バックオフは `delay = baseDelay * 2^(attempt-1)` で計算します
3. APIキーは `process.env.WEATHER_API_KEY` から取得します
4. fetch でのタイムアウトには `AbortController` を使います

</details>

<details>
<summary>解答例</summary>

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// --- 設定 ---
const API_KEY = process.env.WEATHER_API_KEY;
const RATE_LIMIT = 10;          // 1分間の最大リクエスト数
const RATE_WINDOW_MS = 60_000;  // レート制限のウィンドウ（ミリ秒）
const MAX_RETRIES = 3;          // 最大リトライ回数
const BASE_DELAY_MS = 1000;     // リトライの基本遅延（ミリ秒）
const REQUEST_TIMEOUT_MS = 5000; // リクエストタイムアウト（ミリ秒）

// --- レート制限の実装（スライディングウィンドウ方式） ---
class RateLimiter {
  private timestamps: number[] = [];

  canProceed(): boolean {
    this.cleanup();
    return this.timestamps.length < RATE_LIMIT;
  }

  record(): void {
    this.timestamps.push(Date.now());
  }

  getWaitTime(): number {
    this.cleanup();
    if (this.timestamps.length < RATE_LIMIT) return 0;
    // 最も古いリクエストがウィンドウから外れるまでの時間
    const oldest = this.timestamps[0];
    return Math.ceil((oldest + RATE_WINDOW_MS - Date.now()) / 1000);
  }

  private cleanup(): void {
    const cutoff = Date.now() - RATE_WINDOW_MS;
    this.timestamps = this.timestamps.filter((t) => t > cutoff);
  }
}

// --- リトライ機構（指数バックオフ） ---
async function fetchWithRetry(
  url: string,
  options: RequestInit,
  retries: number = MAX_RETRIES
): Promise<Response> {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      // タイムアウト付きfetch
      const controller = new AbortController();
      const timeoutId = setTimeout(
        () => controller.abort(),
        REQUEST_TIMEOUT_MS
      );

      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });
      clearTimeout(timeoutId);

      // サーバーエラー（5xx）の場合のみリトライ
      if (response.status >= 500 && attempt < retries) {
        const delay = BASE_DELAY_MS * Math.pow(2, attempt - 1);
        console.error(
          `API error ${response.status}, retrying in ${delay}ms ` +
          `(attempt ${attempt}/${retries})`
        );
        await new Promise((resolve) => setTimeout(resolve, delay));
        continue;
      }

      return response;
    } catch (error) {
      if (attempt === retries) throw error;

      const delay = BASE_DELAY_MS * Math.pow(2, attempt - 1);
      console.error(
        `Request failed, retrying in ${delay}ms ` +
        `(attempt ${attempt}/${retries}): ${error}`
      );
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw new Error("リトライ回数の上限に達しました");
}

// --- MCPサーバー初期化 ---
const server = new McpServer({
  name: "weather-server",
  version: "1.0.0",
});

const rateLimiter = new RateLimiter();

// --- ツール: 天気情報取得 ---
server.tool(
  "get_weather",
  "指定した都市の現在の天気情報を取得します",
  {
    city: z.string().min(1).max(100).describe("都市名（英語）"),
    units: z.enum(["metric", "imperial"]).default("metric")
      .describe("温度の単位（metric=摂氏, imperial=華氏）"),
  },
  async ({ city, units }) => {
    // APIキーの確認
    if (!API_KEY) {
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({
            error: "APIキーが設定されていません",
            hint: "環境変数 WEATHER_API_KEY を設定してください",
          }),
        }],
        isError: true,
      };
    }

    // レート制限チェック
    if (!rateLimiter.canProceed()) {
      const waitTime = rateLimiter.getWaitTime();
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({
            error: `レート制限に達しました。${waitTime}秒後に再試行してください`,
          }),
        }],
        isError: true,
      };
    }

    try {
      // APIリクエスト（リトライ付き）
      const url =
        `https://api.openweathermap.org/data/2.5/weather` +
        `?q=${encodeURIComponent(city)}&units=${units}` +
        `&appid=${API_KEY}&lang=ja`;

      rateLimiter.record();
      const response = await fetchWithRetry(url, { method: "GET" });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return {
          content: [{
            type: "text" as const,
            text: JSON.stringify({
              error: "天気情報の取得に失敗しました",
              details: errorData.message || `HTTP ${response.status}`,
            }),
          }],
          isError: true,
        };
      }

      const data = await response.json();

      // 必要な情報のみ抽出して返す
      const result = {
        city: data.name,
        country: data.sys.country,
        temp: data.main.temp,
        feels_like: data.main.feels_like,
        description: data.weather[0].description,
        humidity: data.main.humidity,
        wind_speed: data.wind.speed,
        units: units === "metric" ? "℃" : "℉",
      };

      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify(result, null, 2),
        }],
      };
    } catch (error) {
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({
            error: "天気情報の取得に失敗しました",
            details: error instanceof Error ? error.message : String(error),
          }),
        }],
        isError: true,
      };
    }
  }
);

// --- サーバー起動 ---
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Weather MCP Server is running");
}

main().catch(console.error);

// 設計のポイント:
// 1. APIキーは環境変数で管理し、コードにハードコードしません
// 2. レート制限でAPI利用量を制御し、コスト超過を防ぎます
// 3. 指数バックオフにより、一時的な障害から自動回復します
// 4. 5xxエラーのみリトライし、4xxエラー（ユーザーミス）はリトライしません
// 5. AbortControllerでタイムアウトを設定し、無限待ちを防ぎます
// 6. APIレスポンスから必要な情報のみ抽出して返します
```

</details>

---

## チャレンジ問題

---

### 問題6：社内ナレッジベースMCPサーバーの全体設計（チャレンジ）

あなたは社内のナレッジベース（技術文書・FAQ・手順書などを管理するシステム）をMCPサーバーとして構築するプロジェクトのリードエンジニアです。以下の全フェーズについて設計書を作成してください。

**システム要件：**
- 社内の技術文書（Markdown形式）を管理・検索できる
- カテゴリ・タグによる分類と検索
- 全文検索（キーワードによる本文検索）
- 文書のバージョン管理（更新履歴の保持）
- アクセス制御（部署別の閲覧権限）
- 文書の作成・更新・アーカイブ（物理削除はしない）

**各フェーズで記述する内容：**

1. **要件定義**: ツール・リソース・プロンプトの一覧と各仕様
2. **アーキテクチャ設計**: システム構成図（テキストベース）、技術選定の理由
3. **実装**: 主要コンポーネントのコード（サーバー初期化、認証ミドルウェア、検索ロジック）
4. **テスト計画**: テスト種類ごとのテストケース（単体・統合・E2E）
5. **デプロイ計画**: 環境構成、CI/CD、監視・アラート

**期待される出力例：**
```
========================================
社内ナレッジベースMCPサーバー 設計書
========================================

【1. 要件定義】

■ ツール一覧
  1. create_document - 新規文書を作成
  2. update_document - 文書を更新（バージョン管理付き）
  3. search_documents - 全文検索 + フィルタ
  4. archive_document - 文書をアーカイブ
  ...

■ リソース一覧
  1. kb://categories - カテゴリ一覧
  2. kb://documents/{id} - 文書の取得
  3. kb://documents/{id}/history - 更新履歴
  ...

■ プロンプト一覧
  1. summarize_document - 文書の要約を生成
  2. draft_document - テンプレートから文書を下書き
  ...

【2. アーキテクチャ設計】
  +------------------+     +------------------+
  | LLMクライアント  | <-> | MCPサーバー      |
  +------------------+     +------------------+
                                   |
                           +-------+-------+
                           |               |
                    +------+----+  +-------+------+
                    | PostgreSQL |  | Elasticsearch|
                    | (文書保存) |  | (全文検索)   |
                    +------------+  +--------------+
  ...

（以下、各フェーズの詳細が続く）
```

<details>
<summary>ヒント</summary>

各フェーズを進める際のポイントです。

**要件定義:**
- ツールは「状態を変更する操作」に使います（作成・更新・アーカイブ）
- リソースは「データの読み取り」に使います（文書取得・一覧・履歴）
- プロンプトはLLMに「定型的な作業」をさせるテンプレートです
- アクセス制御はMCPの認証機構（OAuth 2.1）を活用します

**アーキテクチャ:**
- 全文検索にはElasticsearchやSQLiteのFTS5が選択肢です
- バージョン管理は文書テーブルとは別に履歴テーブルを持つのが定石です
- アクセス制御のデータモデル（ユーザー・部署・権限の関係）を明確にしましょう

**テスト:**
- 単体テスト: 各ツールのハンドラ関数、バリデーション、検索ロジック
- 統合テスト: MCP Client経由での一連の操作フロー
- E2Eテスト: 実際のLLMクライアントからの利用シナリオ

**デプロイ:**
- MCPサーバーのホスティング方式（stdio/SSE/Streamable HTTP）を選択します
- 環境変数で設定を外部化します
- ヘルスチェックと監視の仕組みを入れます

</details>

<details>
<summary>解答例</summary>

```
========================================
社内ナレッジベースMCPサーバー 設計書
========================================

【1. 要件定義】

■ ツール一覧（状態変更を伴う操作）

1. create_document
   説明: 新規文書を作成する
   パラメータ:
     - title: string (必須) - 文書タイトル
     - content: string (必須) - Markdown本文
     - category: string (必須) - カテゴリ
     - tags: string[] (任意) - タグの配列
   戻り値: { document_id, version: 1, status: "created" }
   権限: 作成者の部署に紐づく

2. update_document
   説明: 既存文書を更新する（自動でバージョンを採番）
   パラメータ:
     - document_id: string (必須)
     - content: string (任意) - 新しい本文
     - tags: string[] (任意) - 新しいタグ
     - change_summary: string (必須) - 変更概要
   戻り値: { document_id, version: N, status: "updated" }
   権限: 文書の所属部署のメンバーのみ

3. search_documents
   説明: キーワード・フィルタで文書を検索する
   パラメータ:
     - query: string (任意) - 全文検索キーワード
     - category: string (任意) - カテゴリフィルタ
     - tags: string[] (任意) - タグフィルタ（AND条件）
     - limit: number (任意, default: 20)
   戻り値: { total, documents: [{ id, title, snippet, score }] }
   権限: ユーザーが閲覧可能な部署の文書のみ返す

4. archive_document
   説明: 文書をアーカイブする（物理削除しない）
   パラメータ:
     - document_id: string (必須)
     - reason: string (必須) - アーカイブ理由
   戻り値: { document_id, status: "archived" }
   権限: 文書の作成者または管理者のみ

■ リソース一覧（読み取り専用データ）

1. kb://categories
   説明: 全カテゴリの一覧
   MIMEタイプ: application/json

2. kb://documents/{id}
   説明: 特定文書の最新版を取得
   MIMEタイプ: text/markdown
   URIテンプレート: document_id をパラメータに取る

3. kb://documents/{id}/history
   説明: 文書の更新履歴一覧
   MIMEタイプ: application/json

4. kb://stats
   説明: ナレッジベースの統計情報
   MIMEタイプ: application/json

■ プロンプト一覧（LLMへの定型指示テンプレート）

1. summarize_document
   説明: 指定した文書の要約を生成する
   引数: document_id
   テンプレート: 「以下の技術文書を3-5行で要約してください: {content}」

2. draft_document
   説明: テーマに基づいて文書の下書きを生成する
   引数: topic, category
   テンプレート: 「{category}カテゴリの技術文書を作成してください。
                  テーマ: {topic}。社内標準フォーマットに従うこと。」

--------------------------------------------------
【2. アーキテクチャ設計】

■ システム構成図

  +-------------------+       +------------------------+
  | Claude Desktop /  | <---> | MCP Server             |
  | その他LLM Client  | stdio | (Node.js / TypeScript) |
  +-------------------+  or   +------------------------+
                        SSE           |
                                +-----+-----+
                                |           |
                         +------+---+ +-----+--------+
                         |PostgreSQL| |SQLite FTS5   |
                         |          | |(全文検索)     |
                         |・documents| |・検索インデックス|
                         |・versions | +---------------+
                         |・users    |
                         |・permissions|
                         +----------+

■ 技術選定

  - ランタイム: Node.js + TypeScript
    理由: MCP SDK公式のTypeScript実装が最も充実しているため
  - DB: PostgreSQL
    理由: JSONBカラムでメタデータを柔軟に格納できる。
          バージョン管理のトランザクション整合性が必要
  - 全文検索: SQLite FTS5（小規模）/ Elasticsearch（大規模）
    理由: 初期はFTS5で十分。規模拡大時にESに移行可能な設計にする
  - 認証: MCPのOAuth 2.1認証フロー
    理由: MCP仕様で標準化されている認証方式

■ データモデル

  documents テーブル:
    id (UUID, PK)
    title (VARCHAR)
    content (TEXT) - Markdown本文
    category (VARCHAR)
    tags (JSONB) - ["tag1", "tag2"]
    author_id (UUID, FK -> users)
    department_id (UUID, FK -> departments)
    status (ENUM: active, archived)
    current_version (INT)
    created_at (TIMESTAMP)
    updated_at (TIMESTAMP)

  document_versions テーブル:
    id (UUID, PK)
    document_id (UUID, FK -> documents)
    version (INT)
    content (TEXT)
    change_summary (VARCHAR)
    changed_by (UUID, FK -> users)
    created_at (TIMESTAMP)

  users テーブル:
    id (UUID, PK)
    name (VARCHAR)
    department_id (UUID, FK -> departments)
    role (ENUM: admin, member, viewer)

  departments テーブル:
    id (UUID, PK)
    name (VARCHAR)
    parent_id (UUID, nullable) - 部署の階層構造

  permissions テーブル:
    department_id (UUID, FK)
    target_department_id (UUID, FK)
    permission (ENUM: read, write, admin)
    - 「どの部署が、どの部署の文書に、どの権限を持つか」を定義

--------------------------------------------------
【3. 実装（主要コンポーネント）】

■ サーバー初期化とアクセス制御ミドルウェア

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "knowledge-base",
  version: "1.0.0",
});

// アクセス制御: ツール実行前にユーザーの権限を検証する
// MCPの認証情報からユーザーIDを取得し、DBで権限を確認
async function checkPermission(
  userId: string,
  documentId: string,
  requiredPermission: "read" | "write" | "admin"
): Promise<boolean> {
  const user = await db.getUser(userId);
  const document = await db.getDocument(documentId);
  if (!user || !document) return false;

  // 管理者は全権限を持つ
  if (user.role === "admin") return true;

  // 部署間の権限テーブルを確認
  const permission = await db.getPermission(
    user.department_id,
    document.department_id
  );

  const permissionLevel = { read: 1, write: 2, admin: 3 };
  return (
    permission !== null &&
    permissionLevel[permission] >= permissionLevel[requiredPermission]
  );
}

■ 全文検索ロジック

// SQLite FTS5 を使った全文検索
class SearchEngine {
  async indexDocument(id: string, title: string, content: string,
                      tags: string[]): Promise<void> {
    await this.db.run(
      `INSERT OR REPLACE INTO documents_fts (id, title, content, tags)
       VALUES (?, ?, ?, ?)`,
      [id, title, content, tags.join(" ")]
    );
  }

  async search(query: string, limit: number): Promise<SearchResult[]> {
    // FTS5のMATCH構文で全文検索
    const results = await this.db.all(
      `SELECT id, title, snippet(documents_fts, 2, '<b>', '</b>', '...', 32)
         AS snippet, rank
       FROM documents_fts
       WHERE documents_fts MATCH ?
       ORDER BY rank
       LIMIT ?`,
      [query, limit]
    );
    return results;
  }
}

--------------------------------------------------
【4. テスト計画】

■ 単体テスト

1. create_document
   - 正常: 全パラメータ指定で文書が作成されること
   - 正常: tags省略時にデフォルト空配列で作成されること
   - 異常: title空文字でバリデーションエラー
   - 異常: 存在しないcategoryでエラー

2. search_documents
   - 正常: キーワード検索で関連文書がヒットすること
   - 正常: カテゴリ+タグの複合フィルタが正しく機能すること
   - 正常: 検索結果が0件の場合に空配列が返ること
   - 境界値: limit=1 で1件のみ返ること

3. アクセス制御
   - 正常: 同一部署の文書にアクセスできること
   - 正常: 権限のある他部署の文書にアクセスできること
   - 異常: 権限のない他部署の文書にアクセスが拒否されること
   - 正常: admin権限で全文書にアクセスできること

4. バージョン管理
   - 正常: update後にversionが1増加すること
   - 正常: 旧バージョンの内容がhistoryに保存されていること
   - 正常: historyが時系列順に返されること

■ 統合テスト（MCP Client経由）

1. 文書ライフサイクル
   create_document → update_document → search → archive の一連フロー

2. 権限フロー
   ユーザーA（営業部）が作成した文書を、
   ユーザーB（技術部、読み取り権限あり）が検索・閲覧できること

3. バージョン管理フロー
   3回更新後、historyリソースで全3バージョンが確認できること

■ E2Eテスト

1. LLMクライアントから「Reactのベストプラクティスを検索して」と
   自然言語で指示し、search_documentsが呼ばれて結果が返ること

2. 「新しいガイドラインを作成して」という指示から、
   draft_documentプロンプト → create_document の流れが動作すること

--------------------------------------------------
【5. デプロイ計画】

■ 環境構成

  開発環境:  stdio接続、SQLiteローカルDB
  ステージ:  SSE接続、PostgreSQL（共有DB）
  本番環境:  Streamable HTTP接続、PostgreSQL（専用DB）+ ES

■ CI/CDパイプライン

  1. Push → GitHub Actions起動
  2. lint (ESLint) + type check (tsc --noEmit)
  3. 単体テスト (vitest)
  4. 統合テスト (MCP Client使用)
  5. Dockerイメージビルド
  6. ステージング環境へデプロイ
  7. E2Eテスト実行
  8. 承認後、本番デプロイ

■ 環境変数

  DATABASE_URL      - PostgreSQL接続文字列
  SEARCH_ENGINE_URL - Elasticsearch接続先（本番のみ）
  LOG_LEVEL         - ログレベル (debug/info/warn/error)
  MCP_TRANSPORT     - トランスポート方式 (stdio/sse/http)

■ 監視・アラート

  - ヘルスチェック: /health エンドポイント（HTTP接続時）
  - メトリクス: ツール呼び出し回数、レスポンス時間、エラー率
  - アラート条件:
    - エラー率 > 5% が5分間継続
    - レスポンス時間 p95 > 3秒
    - ディスク使用率 > 80%
  - ログ: 構造化ログ（JSON形式）をCloudWatch/Datadogに送信

# 設計のポイント:
# 1. アクセス制御は認証（誰か）と認可（何ができるか）を分離して設計
# 2. 全文検索エンジンは差し替え可能な抽象層を設ける
# 3. バージョン管理で物理削除を避け、監査証跡を残す
# 4. トランスポート方式を環境変数で切り替え可能にする
# 5. 段階的にスケールアップできるアーキテクチャにする
```

</details>

---

## まとめ

この章の演習では、実践的なMCPサーバーの構築に必要な以下のスキルを確認しました。

- **基本問題**: 要件整理、ツール/リソースの適切な粒度設計、テスト手法の理解
- **応用問題**: CRUD操作を持つサーバーの設計・実装、外部API連携時のレート制限やリトライ
- **チャレンジ問題**: エンタープライズ規模のMCPサーバーの全体設計（要件定義からデプロイまで）

実践的なMCPサーバーを構築する際は、ツールの粒度設計、エラーハンドリング、セキュリティ、運用面まで考慮することが重要です。
