# 第4章：MCPサーバー開発（TypeScript）

## 学習目標

- TypeScript で MCP サーバーを構築できるようになる
- `McpServer` クラスと Zod によるスキーマ定義を理解する
- stdio と Streamable HTTP の 2 つのトランスポートを使い分けられるようになる
- ビルドからデプロイまでの一連の流れを習得する

---

## 4.1 開発環境のセットアップ

| 項目 | 要件 |
|------|------|
| Node.js | 18 以上 |
| MCP SDK | `@modelcontextprotocol/sdk` |
| スキーマ定義 | `zod` |
| 言語 | TypeScript 5.0+ |

### プロジェクトの初期化

```bash
mkdir my-mcp-server-ts && cd my-mcp-server-ts
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
npx tsc --init
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"]
}
```

### package.json（重要な設定）

```json
{
  "name": "my-mcp-server-ts",
  "version": "1.0.0",
  "type": "module",
  "bin": { "my-mcp-server": "./dist/index.js" },
  "scripts": { "build": "tsc", "start": "node dist/index.js" }
}
```

> **ポイントまとめ**
> - `"type": "module"` は必須です（SDK が ESM で提供されているため）
> - `"module": "Node16"` と `"moduleResolution": "Node16"` をセットで指定します

---

## 4.2 McpServer による最小サーバー

`McpServer` は SDK が提供するサーバークラスです。ツール・リソース・プロンプトの登録とトランスポートへの接続を管理します。

```typescript
// src/index.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "my-first-server", version: "1.0.0" });

server.tool(
  "greet",
  "指定された名前で挨拶を返します。",
  { name: z.string().describe("挨拶する相手の名前") },
  async ({ name }) => ({
    content: [{ type: "text", text: `こんにちは、${name}さん！` }],
  })
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP サーバーが起動しました");
}
main().catch(console.error);
```

```bash
npm run build && npm start
```

### Python 版（FastMCP）との比較

| 項目 | Python (FastMCP) | TypeScript (McpServer) |
|------|-------------------|------------------------|
| ツール定義 | `@mcp.tool()` デコレータ | `server.tool()` メソッド |
| スキーマ | 型ヒントから自動生成 | Zod で明示的に定義 |
| 起動 | `mcp.run()` | `server.connect(transport)` |

### よくある間違い

| 間違い | 正しい書き方 |
|--------|-------------|
| `import` パスに `.js` を付けない | `.js` 拡張子を必ず付ける（ESM の仕様） |
| `"type": "module"` を忘れる | `package.json` に必ず追加する |
| `console.log()` でデバッグ | `console.error()` を使う（stdout は通信用） |

> **ポイントまとめ**
> - 戻り値は `{ content: [{ type: "text", text: "..." }] }` の形式です
> - `import` パスには `.js` 拡張子が必要です（TypeScript の ESM 制約）

---

## 4.3 ツール（Tool）の実装

`server.tool(名前, 説明, Zodスキーマ, ハンドラー)` の形式で定義します。

### Zod によるスキーマ定義

| Zod | JSON Schema | 説明 |
|-----|-------------|------|
| `z.string()` | `string` | 文字列 |
| `z.number()` | `number` | 数値 |
| `z.boolean()` | `boolean` | 真偽値 |
| `z.enum(["a","b"])` | `string` (enum) | 列挙型 |
| `z.string().optional()` | `string` (nullable) | 省略可能 |
| `z.array(z.string())` | `array` | 配列 |

`.describe()` でパラメータの説明を付加します。AI がパラメータの意味を理解するために重要です。

### 実践的なツール実装例

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "practical-tools", version: "1.0.0" });

server.tool("calculate", "四則演算を行います。", {
    a: z.number().describe("1つ目の数値"),
    b: z.number().describe("2つ目の数値"),
    operator: z.enum(["+", "-", "*", "/"]).describe("演算子"),
  },
  async ({ a, b, operator }) => {
    if (operator === "/" && b === 0) {
      return { content: [{ type: "text", text: "エラー: 0で割れません。" }], isError: true };
    }
    const ops = { "+": a + b, "-": a - b, "*": a * b, "/": a / b };
    return { content: [{ type: "text", text: `${a} ${operator} ${b} = ${ops[operator]}` }] };
  }
);

server.tool("search_items", "アイテムを検索します。", {
    query: z.string().describe("検索キーワード"),
    category: z.enum(["all", "books", "electronics"]).default("all"),
    maxResults: z.number().default(10).describe("最大取得件数"),
  },
  async ({ query, category, maxResults }) => ({
    content: [{ type: "text", text: `「${query}」で${category}を検索（最大${maxResults}件）` }],
  })
);

async function main() { await server.connect(new StdioServerTransport()); }
main().catch(console.error);
```

### エラーハンドリング

エラー時は `isError: true` を含むレスポンスを返します。

```typescript
server.tool(
  "read_file",
  "ファイルの内容を読み取ります。",
  { path: z.string().describe("ファイルパス") },
  async ({ path }) => {
    try {
      const fs = await import("fs/promises");
      const content = await fs.readFile(path, "utf-8");
      return { content: [{ type: "text", text: content }] };
    } catch (error) {
      const msg = error instanceof Error ? error.message : "不明なエラー";
      return { content: [{ type: "text", text: `読み取りエラー: ${msg}` }], isError: true };
    }
  }
);
```

> **ポイントまとめ**
> - `z.enum()` で選択肢を制限すると AI が適切な値を選びやすくなります
> - `.default()` でデフォルト値を設定するとパラメータが省略可能になります
> - エラー時は `isError: true` でクライアントに通知します

---

## 4.4 リソース（Resource）の実装

### 静的リソースと動的リソース

```typescript
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
const server = new McpServer({ name: "resource-demo", version: "1.0.0" });

// 静的リソース: 固定URIでデータを公開
server.resource("app-settings", "config://app/settings",
  async (uri) => ({ contents: [{ uri: uri.href, text: "バージョン: 2.1.0\n環境: production" }] })
);

// 動的リソース: ResourceTemplate でパラメータ付きURIを定義
server.resource("user-profile",
  new ResourceTemplate("users://{userId}/profile", { list: undefined }),
  async (uri, { userId }) => {
    const profiles: Record<string, string> = { "001": "田中太郎, 開発部", "002": "鈴木花子, 企画部" };
    const text = profiles[userId as string] ?? `ユーザー ${userId} は未登録です`;
    return { contents: [{ uri: uri.href, text }] };
  }
);
```

### URI スキーム設計

```
静的:   config://app/settings     docs://api/reference
動的:   users://{userId}/profile  logs://{date}/summary
```

> **ポイントまとめ**
> - 静的リソースは URI 文字列、動的リソースは `ResourceTemplate` で定義します
> - `contents` 配列にテキストデータを含めて返します

---

## 4.5 プロンプト（Prompt）の実装

### 基本のプロンプトと引数付きプロンプト

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
const server = new McpServer({ name: "prompt-demo", version: "1.0.0" });

// 引数なし
server.prompt("code-review", "コードレビュープロンプト",
  async () => ({
    messages: [{ role: "user",
      content: { type: "text", text: "シニアエンジニアとしてコードをレビューしてください。" } }],
  })
);

// 引数付き（Zodスキーマで定義）
server.prompt("explain-code", "コード解説プロンプト",
  { language: z.string(), level: z.enum(["beginner", "intermediate", "advanced"]).default("beginner") },
  async ({ language, level }) => {
    const names: Record<string, string> = { beginner: "初心者", intermediate: "中級者", advanced: "上級者" };
    return { messages: [{ role: "user",
      content: { type: "text", text: `${names[level]}向けに${language}コードを解説してください。` } }] };
  }
);
```

### 複数メッセージのプロンプト

```typescript
server.prompt("debug-help", "デバッグ支援プロンプト",
  { errorMessage: z.string().describe("エラーメッセージ") },
  async ({ errorMessage }) => ({
    messages: [
      { role: "user", content: { type: "text", text: `エラー:\n\`\`\`\n${errorMessage}\n\`\`\`` } },
      { role: "assistant", content: { type: "text", text: "確認しました。質問させてください。" } },
      { role: "user", content: { type: "text", text: "はい、お願いします。" } },
    ],
  })
);
```

> **ポイントまとめ**
> - 引数なしの場合はスキーマを省略できます
> - `messages` 配列で複数ターンの会話テンプレートを定義できます

---

## 4.6 トランスポート設定

| 項目 | StdioServerTransport | StreamableHTTPServerTransport |
|------|---------------------|-------------------------------|
| 通信方式 | 標準入出力 | HTTP + SSE |
| 用途 | ローカルツール | リモートサーバー |
| セッション | 1対1 | 複数クライアント対応 |

### stdio トランスポート（基本）

```typescript
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Streamable HTTP トランスポート

リモートアクセスや複数クライアント対応が必要な場合に使います。`express` の追加インストールが必要です（`npm install express @types/express`）。

```typescript
import express from "express";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const app = express();
app.use(express.json());

const server = new McpServer({ name: "http-server", version: "1.0.0" });

server.tool("hello", "挨拶を返します。", { name: z.string() },
  async ({ name }) => ({ content: [{ type: "text", text: `Hello, ${name}!` }] })
);

app.post("/mcp", async (req, res) => {
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  res.on("close", () => { transport.close(); });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

app.listen(3000, () => console.error("HTTP MCP: http://localhost:3000/mcp"));
```

### よくある間違い

| 間違い | 正しい方法 |
|--------|-----------|
| ローカル用途に HTTP を使う | まず stdio で十分。必要時に HTTP へ移行 |
| `console.log()` を混在させる | 常に `console.error()` を使う習慣にする |

> **ポイントまとめ**
> - ローカル利用（Claude Desktop / Code）には stdio を使います
> - リモートや複数クライアント対応には Streamable HTTP を使います

---

## 4.7 ビルドとデプロイ

### ビルドと実行

```bash
npx tsc                  # dist/ に JS ファイルが生成される
node dist/index.js       # 実行
```

### Claude Desktop の設定

| OS | 設定ファイルのパス |
|----|-------------------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

```json
{
  "mcpServers": {
    "my-ts-server": {
      "command": "node",
      "args": ["/absolute/path/to/dist/index.js"]
    }
  }
}
```

### Claude Code の設定

```bash
claude mcp add my-ts-server -- node /absolute/path/to/dist/index.js
```

### 完全な実装例

```typescript
// src/index.ts - ツール・リソース・プロンプトを含む完全な例
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "my-complete-server", version: "1.0.0" });

server.tool("get_current_time", "現在の日時を返します。", {},
  async () => ({
    content: [{ type: "text", text: `現在: ${new Date().toLocaleString("ja-JP")}` }],
  })
);

server.tool("calculate_bmi", "BMIを計算します。",
  { heightCm: z.number().describe("身長(cm)"), weightKg: z.number().describe("体重(kg)") },
  async ({ heightCm, weightKg }) => {
    if (heightCm <= 0 || weightKg <= 0) {
      return { content: [{ type: "text", text: "正の数を指定してください。" }], isError: true };
    }
    const bmi = weightKg / (heightCm / 100) ** 2;
    return { content: [{ type: "text", text: `BMI: ${bmi.toFixed(1)}` }] };
  }
);

server.resource("server-status", "info://server/status",
  async (uri) => ({ contents: [{ uri: uri.href, text: "ステータス: 正常稼働中" }] })
);

server.prompt("summarize", "要約プロンプト",
  { topic: z.string().describe("要約するトピック") },
  async ({ topic }) => ({
    messages: [{ role: "user", content: { type: "text", text: `「${topic}」を3点に要約してください。` } }],
  })
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP サーバー起動完了");
}
main().catch(console.error);
```

### MCP Inspector でのテスト

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

### よくある間違い

| 間違い | 正しい方法 |
|--------|-----------|
| `.ts` を直接実行する | `tsc` でビルド後に `node dist/index.js` で実行 |
| 設定に相対パスを書く | 絶対パスを使う |
| ビルドし忘れて古いコードが動く | 変更後は必ず `npm run build` |
| `"type": "module"` を忘れる | ESM 必須なので必ず指定する |

> **ポイントまとめ**
> - TypeScript は必ずコンパイルしてから実行します
> - デプロイ前に MCP Inspector で必ずテストしましょう
> - 設定ファイルには絶対パスを使い、Claude Desktop は設定変更後に再起動が必要です
