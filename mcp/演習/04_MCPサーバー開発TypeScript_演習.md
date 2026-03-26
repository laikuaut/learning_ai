# 第4章 演習：TypeScript SDKによるサーバー開発

---

## 基本問題

---

### 問題1：最小構成のMCPサーバー（基本）

TypeScript MCP SDKを使って、最小構成のMCPサーバーを作成してください。
サーバーに `greet` ツールを登録し、名前を受け取って挨拶を返すようにします。

**期待される出力（ツール呼び出し結果）：**
```
こんにちは、太郎さん！MCPの世界へようこそ。
```

<details>
<summary>ヒント</summary>

- `@modelcontextprotocol/sdk` パッケージの `McpServer` と `StdioServerTransport` を使います
- `server.tool()` メソッドでツールを登録します
- Zodスキーマでパラメータを定義します
- `StdioServerTransport` で標準入出力トランスポートを生成し、`server.connect()` で接続します

</details>

<details>
<summary>解答例</summary>

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// サーバーインスタンスを生成
const server = new McpServer({
  name: "greeting-server",
  version: "1.0.0",
});

// ツールを登録
server.tool(
  "greet",                          // ツール名
  "名前を受け取って挨拶を返します。",    // 説明
  { name: z.string() },             // パラメータスキーマ（Zod）
  async ({ name }) => ({            // ハンドラ関数
    content: [
      {
        type: "text" as const,
        text: `こんにちは、${name}さん！MCPの世界へようこそ。`,
      },
    ],
  })
);

// 標準入出力トランスポートで起動
const transport = new StdioServerTransport();
await server.connect(transport);
```

**ポイント：**
- `McpServer` の引数には `name` と `version` を指定します
- `server.tool()` はPythonの `@mcp.tool()` に相当します
- Zodスキーマがパラメータの型定義と検証の両方を担います
- レスポンスは `{ content: [{ type: "text", text: "..." }] }` の形式で返します

</details>

---

### 問題2：Zodスキーマの基本（基本）

以下のツール仕様に合うZodスキーマを書いてください。ツール登録のコード全体を記述してください。

**ツール仕様：**
- ツール名：`create_user`
- パラメータ：
  - `name`（文字列、必須）：ユーザー名
  - `age`（数値、必須、1以上150以下）：年齢
  - `email`（文字列、必須、メール形式）：メールアドレス
  - `role`（文字列、任意、デフォルト "member"）：役割（"admin" / "member" / "guest" のいずれか）

**期待される出力例：**
```
ユーザーを作成しました:
  名前: 田中太郎
  年齢: 30
  メール: tanaka@example.com
  役割: admin
```

<details>
<summary>ヒント</summary>

- `z.string()` で文字列、`z.number()` で数値を定義します
- `.min()` / `.max()` で範囲制限を設定できます
- `.email()` でメール形式のバリデーションを追加できます
- `.enum()` で選択肢を制限できます
- `.optional().default()` で任意パラメータにデフォルト値を設定できます
- `.describe()` で各パラメータの説明を追加できます

</details>

<details>
<summary>解答例</summary>

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "user-server",
  version: "1.0.0",
});

server.tool(
  "create_user",
  "新しいユーザーを作成します。",
  {
    // 文字列・必須
    name: z.string().describe("ユーザー名"),
    // 数値・必須・範囲制限
    age: z.number().min(1).max(150).describe("年齢（1〜150）"),
    // 文字列・必須・メール形式
    email: z.string().email().describe("メールアドレス"),
    // 列挙型・任意・デフォルト値あり
    role: z
      .enum(["admin", "member", "guest"])
      .optional()
      .default("member")
      .describe("役割（admin / member / guest）"),
  },
  async ({ name, age, email, role }) => ({
    content: [
      {
        type: "text" as const,
        text: [
          "ユーザーを作成しました:",
          `  名前: ${name}`,
          `  年齢: ${age}`,
          `  メール: ${email}`,
          `  役割: ${role}`,
        ].join("\n"),
      },
    ],
  })
);
```

**ポイント：**
- Zodは型の定義とランタイムバリデーションを同時に行えるライブラリです
- `.describe()` の内容はMCPスキーマの `description` に反映されます
- `.optional().default()` で省略時のデフォルト値を設定できます
- `.enum()` で選択肢を限定すると、LLMが不正な値を送る可能性を減らせます

</details>

---

### 問題3：StdioServerTransportの設定（基本）

以下の質問に答え、それぞれコードで示してください。

1. `StdioServerTransport` はどのような場面で使いますか？
2. サーバーの起動コードを、エラーハンドリング付きで記述してください。
3. `package.json` にはどのような設定が必要ですか？

**期待される出力（起動時のログイメージ）：**
```
MCPサーバー "my-server" を起動しています...
サーバーが正常に起動しました。
```

<details>
<summary>ヒント</summary>

- `StdioServerTransport` はローカルプロセスとして実行するMCPサーバーで使います
- `process.stderr.write()` でログ出力できます（stdoutはMCP通信に使われるため）
- `try/catch` でエラーをキャッチし、プロセスを安全に終了させましょう

</details>

<details>
<summary>解答例</summary>

```typescript
// 1. StdioServerTransport は、MCPクライアント（Claude Desktop等）が
//    ローカルプロセスとしてサーバーを起動する場面で使います。
//    標準入力（stdin）で要求を受け取り、標準出力（stdout）で応答します。

// 2. エラーハンドリング付き起動コード
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0",
});

// ツール登録などはここで行う

async function main() {
  try {
    // ログはstderrに出力する（stdoutはMCP通信用）
    process.stderr.write('MCPサーバー "my-server" を起動しています...\n');

    const transport = new StdioServerTransport();
    await server.connect(transport);

    process.stderr.write("サーバーが正常に起動しました。\n");
  } catch (error) {
    process.stderr.write(`起動エラー: ${error}\n`);
    process.exit(1);
  }
}

main();

// 3. package.json の設定例
// {
//   "name": "my-mcp-server",
//   "version": "1.0.0",
//   "type": "module",
//   "bin": {
//     "my-mcp-server": "./dist/index.js"
//   },
//   "scripts": {
//     "build": "tsc",
//     "start": "node dist/index.js"
//   },
//   "dependencies": {
//     "@modelcontextprotocol/sdk": "^1.11.0",
//     "zod": "^3.24.0"
//   },
//   "devDependencies": {
//     "typescript": "^5.8.0",
//     "@types/node": "^22.0.0"
//   }
// }
```

**ポイント：**
- `StdioServerTransport` はstdin/stdoutベースなので、ログは必ず `stderr` に出力します
- `stdout` に任意の文字列を書き込むとMCPプロトコルが壊れるので注意してください
- `package.json` の `"type": "module"` は ES Modules を使うために必要です
- `"bin"` フィールドを設定すると `npx` で実行可能になります

</details>

---

### 問題4：Resourceの登録（基本）

TypeScript SDKでリソースを登録する方法を学びます。以下のリソースを登録してください。

1. `config://app/settings`：アプリケーション設定を返す静的リソース
2. `docs://guide/{topic}`：トピックに応じたガイド文書を返すリソーステンプレート

**期待される出力例（config://app/settings）：**
```json
{
  "theme": "dark",
  "language": "ja",
  "notifications": true
}
```

**期待される出力例（docs://guide/setup）：**
```
# セットアップガイド

1. リポジトリをクローンしてください
2. npm install を実行してください
3. npm run build でビルドしてください
```

<details>
<summary>ヒント</summary>

- `server.resource()` でリソースを登録します
- 第1引数がリソース名、第2引数がURIまたはURIテンプレートです
- テンプレートの場合は `ResourceTemplate` を使います
- レスポンスは `{ contents: [{ uri, text }] }` の形式です

</details>

<details>
<summary>解答例</summary>

```typescript
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({
  name: "docs-server",
  version: "1.0.0",
});

// 1. 静的リソース
server.resource(
  "app-settings",               // リソース名
  "config://app/settings",      // URI
  async (uri) => ({
    contents: [
      {
        uri: uri.href,
        text: JSON.stringify(
          {
            theme: "dark",
            language: "ja",
            notifications: true,
          },
          null,
          2
        ),
      },
    ],
  })
);

// 2. リソーステンプレート（動的URI）
const guides: Record<string, string> = {
  setup: `# セットアップガイド

1. リポジトリをクローンしてください
2. npm install を実行してください
3. npm run build でビルドしてください`,
  usage: `# 使い方ガイド

1. サーバーを起動してください
2. クライアントから接続してください
3. ツール一覧を確認してください`,
};

server.resource(
  "guide",                                      // リソース名
  new ResourceTemplate("docs://guide/{topic}"), // URIテンプレート
  async (uri, { topic }) => {
    const content = guides[topic as string] ?? `トピック "${topic}" のガイドは見つかりません。`;
    return {
      contents: [
        {
          uri: uri.href,
          text: content,
        },
      ],
    };
  }
);
```

**ポイント：**
- 静的リソースはURIを直接文字列で渡し、テンプレートは `ResourceTemplate` を使います
- テンプレートの `{topic}` 部分がハンドラの第2引数に渡されます
- レスポンスの `contents` は配列で、複数のコンテンツを返すこともできます

</details>

---

### 問題5：Promptの登録（基本）

TypeScript SDKでプロンプトテンプレートを登録してください。
コードのバグ修正を依頼するプロンプト `debug_help` を作成します。

**引数：**
- `code`（文字列）：バグのあるコード
- `error_message`（文字列）：エラーメッセージ
- `language`（文字列、任意、デフォルト "TypeScript"）：プログラミング言語

**期待される出力（プロンプト展開結果）：**
```
以下のTypeScriptコードでエラーが発生しています。原因を特定して修正方法を教えてください。

エラーメッセージ:
TypeError: Cannot read property 'name' of undefined

コード:
const user = getUser(id);
console.log(user.name);
```

<details>
<summary>ヒント</summary>

- `server.prompt()` でプロンプトを登録します
- 第3引数でZodスキーマによりパラメータを定義します
- レスポンスは `{ messages: [{ role, content: { type, text } }] }` の形式です
- プロンプトのパラメータは全て文字列型（`z.string()`）で定義します

</details>

<details>
<summary>解答例</summary>

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "debug-server",
  version: "1.0.0",
});

server.prompt(
  "debug_help",                            // プロンプト名
  "コードのバグ修正を依頼するプロンプトです。",  // 説明
  {
    code: z.string().describe("バグのあるコード"),
    error_message: z.string().describe("エラーメッセージ"),
    language: z.string().optional().default("TypeScript").describe("プログラミング言語"),
  },
  async ({ code, error_message, language }) => ({
    messages: [
      {
        role: "user" as const,
        content: {
          type: "text" as const,
          text: `以下の${language}コードでエラーが発生しています。原因を特定して修正方法を教えてください。

エラーメッセージ:
${error_message}

コード:
${code}`,
        },
      },
    ],
  })
);
```

**ポイント：**
- `server.prompt()` の構造は `server.tool()` と似ていますが、返すデータ形式が異なります
- プロンプトの返り値は `messages` 配列で、`role`（"user" / "assistant"）と `content` を持ちます
- プロンプトのパラメータはMCP仕様上すべて文字列型です
- `.optional().default()` で省略可能なパラメータを定義できます

</details>

---

## 応用問題

---

### 問題6：ブックマーク管理MCPサーバー（応用）

ブックマーク（お気に入りURL）を管理するMCPサーバーを実装してください。

**ツール：**
1. `add_bookmark(url, title, tags)` - ブックマークを追加
2. `search_bookmarks(query)` - タイトルまたはタグで検索
3. `delete_bookmark(url)` - ブックマークを削除
4. `list_bookmarks()` - 全ブックマーク一覧

**期待される動作例：**
```
add_bookmark("https://example.com", "Example Site", ["reference", "web"])
→ "ブックマークを追加しました: Example Site (https://example.com)"

search_bookmarks("reference")
→ "検索結果（1件）:
   - Example Site (https://example.com) [reference, web]"

list_bookmarks()
→ "ブックマーク一覧（1件）:
   1. Example Site
      URL: https://example.com
      タグ: reference, web"
```

<details>
<summary>ヒント</summary>

- ブックマークはサーバー内の `Map` で管理します（URLをキーにすると重複防止になります）
- タグは `z.array(z.string())` で配列として定義します
- 検索はタイトルとタグの両方を対象にし、部分一致で検索します
- `.optional().default([])` でタグを任意にできます

</details>

<details>
<summary>解答例</summary>

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "bookmark-manager",
  version: "1.0.0",
});

// ブックマークデータの型定義
interface Bookmark {
  url: string;
  title: string;
  tags: string[];
  addedAt: string;
}

// インメモリでブックマークを管理
const bookmarks = new Map<string, Bookmark>();

// ブックマークを追加
server.tool(
  "add_bookmark",
  "ブックマークを追加します。",
  {
    url: z.string().url().describe("ブックマークするURL"),
    title: z.string().describe("ブックマークのタイトル"),
    tags: z
      .array(z.string())
      .optional()
      .default([])
      .describe("タグの配列"),
  },
  async ({ url, title, tags }) => {
    if (bookmarks.has(url)) {
      return {
        content: [
          {
            type: "text" as const,
            text: `エラー: ${url} は既にブックマークされています。`,
          },
        ],
      };
    }

    bookmarks.set(url, {
      url,
      title,
      tags,
      addedAt: new Date().toISOString(),
    });

    return {
      content: [
        {
          type: "text" as const,
          text: `ブックマークを追加しました: ${title} (${url})`,
        },
      ],
    };
  }
);

// ブックマークを検索
server.tool(
  "search_bookmarks",
  "タイトルまたはタグでブックマークを検索します。",
  {
    query: z.string().describe("検索キーワード"),
  },
  async ({ query }) => {
    const lowerQuery = query.toLowerCase();
    const results: Bookmark[] = [];

    for (const bookmark of bookmarks.values()) {
      const titleMatch = bookmark.title.toLowerCase().includes(lowerQuery);
      const tagMatch = bookmark.tags.some((tag) =>
        tag.toLowerCase().includes(lowerQuery)
      );
      if (titleMatch || tagMatch) {
        results.push(bookmark);
      }
    }

    if (results.length === 0) {
      return {
        content: [
          {
            type: "text" as const,
            text: `"${query}" に一致するブックマークは見つかりませんでした。`,
          },
        ],
      };
    }

    const lines = results.map(
      (b) => `  - ${b.title} (${b.url}) [${b.tags.join(", ")}]`
    );

    return {
      content: [
        {
          type: "text" as const,
          text: `検索結果（${results.length}件）:\n${lines.join("\n")}`,
        },
      ],
    };
  }
);

// ブックマークを削除
server.tool(
  "delete_bookmark",
  "指定されたURLのブックマークを削除します。",
  {
    url: z.string().url().describe("削除するブックマークのURL"),
  },
  async ({ url }) => {
    const bookmark = bookmarks.get(url);
    if (!bookmark) {
      return {
        content: [
          {
            type: "text" as const,
            text: `エラー: ${url} はブックマークされていません。`,
          },
        ],
      };
    }

    bookmarks.delete(url);
    return {
      content: [
        {
          type: "text" as const,
          text: `ブックマークを削除しました: ${bookmark.title} (${url})`,
        },
      ],
    };
  }
);

// 全ブックマーク一覧
server.tool(
  "list_bookmarks",
  "全てのブックマークを一覧表示します。",
  {},
  async () => {
    if (bookmarks.size === 0) {
      return {
        content: [
          {
            type: "text" as const,
            text: "ブックマークはまだ登録されていません。",
          },
        ],
      };
    }

    const lines: string[] = [];
    let i = 1;
    for (const b of bookmarks.values()) {
      lines.push(`  ${i}. ${b.title}`);
      lines.push(`     URL: ${b.url}`);
      lines.push(`     タグ: ${b.tags.join(", ") || "なし"}`);
      i++;
    }

    return {
      content: [
        {
          type: "text" as const,
          text: `ブックマーク一覧（${bookmarks.size}件）:\n${lines.join("\n")}`,
        },
      ],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

**ポイント：**
- `z.string().url()` でURL形式のバリデーションが自動的に行われます
- `z.array(z.string())` で文字列配列を定義できます
- `Map` を使うとキー（URL）の重複チェックが自然に行えます
- TypeScriptの型定義（`interface`）を使うことで、コードの可読性が向上します

</details>

---

### 問題7：メモ管理MCPサーバー（応用）

メモの作成・更新・検索ができるMCPサーバーを実装してください。
Tools と Resources の両方を活用します。

**Tools：**
1. `create_memo(title, content, category)` - メモを作成
2. `update_memo(memo_id, content)` - メモの内容を更新
3. `search_memos(keyword)` - キーワードでメモを検索

**Resources：**
1. `memos://list` - メモ一覧（タイトルとIDのリスト）
2. `memos://{memo_id}` - 個別メモの全文

**期待される動作例：**
```
create_memo("買い物リスト", "牛乳、卵、パン", "生活")
→ "メモを作成しました: [M001] 買い物リスト"

memos://list
→ "M001: 買い物リスト (生活) - 2026-03-26"

memos://M001
→ "タイトル: 買い物リスト
   カテゴリ: 生活
   作成日: 2026-03-26
   ---
   牛乳、卵、パン"
```

<details>
<summary>ヒント</summary>

- メモIDは `M001`, `M002` のように自動採番します
- `ResourceTemplate` を使ってメモIDに応じたリソースを返します
- 更新時は内容の差し替えと更新日時の記録を行います

</details>

<details>
<summary>解答例</summary>

```typescript
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "memo-manager",
  version: "1.0.0",
});

// メモデータの型定義
interface Memo {
  id: string;
  title: string;
  content: string;
  category: string;
  createdAt: string;
  updatedAt: string;
}

const memos = new Map<string, Memo>();
let memoCounter = 0;

function generateMemoId(): string {
  memoCounter++;
  return `M${String(memoCounter).padStart(3, "0")}`;
}

function formatDate(iso: string): string {
  return iso.split("T")[0];
}

// ==================== Tools ====================

server.tool(
  "create_memo",
  "新しいメモを作成します。",
  {
    title: z.string().describe("メモのタイトル"),
    content: z.string().describe("メモの本文"),
    category: z.string().optional().default("未分類").describe("カテゴリ"),
  },
  async ({ title, content, category }) => {
    const id = generateMemoId();
    const now = new Date().toISOString();

    memos.set(id, {
      id,
      title,
      content,
      category,
      createdAt: now,
      updatedAt: now,
    });

    return {
      content: [
        {
          type: "text" as const,
          text: `メモを作成しました: [${id}] ${title}`,
        },
      ],
    };
  }
);

server.tool(
  "update_memo",
  "既存メモの内容を更新します。",
  {
    memo_id: z.string().describe("更新するメモのID（例: M001）"),
    content: z.string().describe("新しい本文"),
  },
  async ({ memo_id, content }) => {
    const memo = memos.get(memo_id);
    if (!memo) {
      return {
        content: [
          {
            type: "text" as const,
            text: `エラー: メモ ${memo_id} は存在しません。`,
          },
        ],
      };
    }

    memo.content = content;
    memo.updatedAt = new Date().toISOString();

    return {
      content: [
        {
          type: "text" as const,
          text: `メモ [${memo_id}] ${memo.title} を更新しました。`,
        },
      ],
    };
  }
);

server.tool(
  "search_memos",
  "キーワードでメモを検索します。",
  {
    keyword: z.string().describe("検索キーワード"),
  },
  async ({ keyword }) => {
    const lowerKeyword = keyword.toLowerCase();
    const results: Memo[] = [];

    for (const memo of memos.values()) {
      if (
        memo.title.toLowerCase().includes(lowerKeyword) ||
        memo.content.toLowerCase().includes(lowerKeyword) ||
        memo.category.toLowerCase().includes(lowerKeyword)
      ) {
        results.push(memo);
      }
    }

    if (results.length === 0) {
      return {
        content: [
          {
            type: "text" as const,
            text: `"${keyword}" に一致するメモは見つかりませんでした。`,
          },
        ],
      };
    }

    const lines = results.map(
      (m) => `  - [${m.id}] ${m.title} (${m.category})`
    );

    return {
      content: [
        {
          type: "text" as const,
          text: `検索結果（${results.length}件）:\n${lines.join("\n")}`,
        },
      ],
    };
  }
);

// ==================== Resources ====================

// メモ一覧リソース
server.resource(
  "memo-list",
  "memos://list",
  async (uri) => {
    if (memos.size === 0) {
      return {
        contents: [{ uri: uri.href, text: "メモはまだありません。" }],
      };
    }

    const lines: string[] = [];
    for (const memo of memos.values()) {
      lines.push(
        `${memo.id}: ${memo.title} (${memo.category}) - ${formatDate(memo.createdAt)}`
      );
    }

    return {
      contents: [{ uri: uri.href, text: lines.join("\n") }],
    };
  }
);

// 個別メモリソース（テンプレート）
server.resource(
  "memo-detail",
  new ResourceTemplate("memos://{memo_id}"),
  async (uri, { memo_id }) => {
    const memo = memos.get(memo_id as string);
    if (!memo) {
      return {
        contents: [
          {
            uri: uri.href,
            text: `エラー: メモ ${memo_id} は存在しません。`,
          },
        ],
      };
    }

    const text = [
      `タイトル: ${memo.title}`,
      `カテゴリ: ${memo.category}`,
      `作成日: ${formatDate(memo.createdAt)}`,
      `更新日: ${formatDate(memo.updatedAt)}`,
      "---",
      memo.content,
    ].join("\n");

    return {
      contents: [{ uri: uri.href, text }],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

**ポイント：**
- ToolsとResourcesの使い分けが重要です。操作（CRUD）はToolsで、参照はResourcesで行います
- `ResourceTemplate` のパラメータ（`{memo_id}`）はハンドラの第2引数で受け取ります
- TypeScriptの `interface` でデータ構造を明示することで、型安全な実装ができます

</details>

---

### 問題8：エラーハンドリングとバリデーション（応用）

以下のような堅牢なエラーハンドリングを持つ「計算機MCPサーバー」を実装してください。

**ツール：**
1. `calculate(expression)` - 数式を評価して結果を返す
2. `convert_base(number, from_base, to_base)` - 基数変換

**エラーケースへの対応：**
- 不正な数式の検出と適切なエラーメッセージ
- ゼロ除算の検出
- 不正な基数の検出（2, 8, 10, 16のみ対応）
- `isError: true` フラグでエラーレスポンスを示す

**期待される出力例：**
```
calculate("2 + 3 * 4") → "結果: 14"
calculate("10 / 0") → "[エラー] ゼロで除算することはできません。"
convert_base("ff", 16, 10) → "ff (16進数) = 255 (10進数)"
convert_base("102", 2, 10) → "[エラー] '102' は有効な2進数ではありません。"
```

<details>
<summary>ヒント</summary>

- 数式の評価には安全な独自パーサーを実装するか、許可された文字のみを受け付けるようにします
- `parseInt(number, base)` で基数変換ができます
- `Number.toString(base)` で任意の基数に変換できます
- `isError: true` をレスポンスに含めるとMCPクライアントにエラーとして伝わります

</details>

<details>
<summary>解答例</summary>

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "calculator",
  version: "1.0.0",
});

// 安全な数式評価（基本的な四則演算のみ許可）
function safeEvaluate(expression: string): number {
  // 許可する文字: 数字、演算子、括弧、スペース、小数点
  const sanitized = expression.replace(/\s/g, "");
  if (!/^[0-9+\-*/().]+$/.test(sanitized)) {
    throw new Error("不正な文字が含まれています。数字と演算子（+, -, *, /）のみ使用できます。");
  }

  // ゼロ除算チェック
  if (/\/\s*0(?![0-9.])/.test(sanitized)) {
    throw new Error("ゼロで除算することはできません。");
  }

  // Function コンストラクタで評価（限定された文字のみ許可済み）
  const result = new Function(`return (${sanitized})`)();

  if (typeof result !== "number" || !isFinite(result)) {
    throw new Error("計算結果が無効です。");
  }

  return result;
}

// 数式計算ツール
server.tool(
  "calculate",
  "数式を評価して結果を返します。四則演算と括弧に対応しています。",
  {
    expression: z.string().describe("計算する数式（例: 2 + 3 * 4）"),
  },
  async ({ expression }) => {
    try {
      const result = safeEvaluate(expression);
      return {
        content: [
          {
            type: "text" as const,
            text: `結果: ${result}`,
          },
        ],
      };
    } catch (error) {
      return {
        isError: true,
        content: [
          {
            type: "text" as const,
            text: `[エラー] ${error instanceof Error ? error.message : "不明なエラーが発生しました。"}`,
          },
        ],
      };
    }
  }
);

// 基数変換ツール
const VALID_BASES = [2, 8, 10, 16] as const;

server.tool(
  "convert_base",
  "数値の基数変換を行います（2進数、8進数、10進数、16進数）。",
  {
    number: z.string().describe("変換する数値（文字列）"),
    from_base: z.number().describe("変換元の基数（2, 8, 10, 16）"),
    to_base: z.number().describe("変換先の基数（2, 8, 10, 16）"),
  },
  async ({ number, from_base, to_base }) => {
    // 基数の妥当性チェック
    if (!VALID_BASES.includes(from_base as any)) {
      return {
        isError: true,
        content: [
          {
            type: "text" as const,
            text: `[エラー] 基数 ${from_base} はサポートされていません。対応: ${VALID_BASES.join(", ")}`,
          },
        ],
      };
    }
    if (!VALID_BASES.includes(to_base as any)) {
      return {
        isError: true,
        content: [
          {
            type: "text" as const,
            text: `[エラー] 基数 ${to_base} はサポートされていません。対応: ${VALID_BASES.join(", ")}`,
          },
        ],
      };
    }

    // 数値の妥当性チェック
    const parsed = parseInt(number, from_base);
    if (isNaN(parsed)) {
      return {
        isError: true,
        content: [
          {
            type: "text" as const,
            text: `[エラー] '${number}' は有効な${from_base}進数ではありません。`,
          },
        ],
      };
    }

    // 再エンコードして元の入力と比較（不正な桁の検出）
    if (parsed.toString(from_base) !== number.toLowerCase()) {
      return {
        isError: true,
        content: [
          {
            type: "text" as const,
            text: `[エラー] '${number}' は有効な${from_base}進数ではありません。`,
          },
        ],
      };
    }

    const result = parsed.toString(to_base);
    const baseNames: Record<number, string> = {
      2: "2進数",
      8: "8進数",
      10: "10進数",
      16: "16進数",
    };

    return {
      content: [
        {
          type: "text" as const,
          text: `${number} (${baseNames[from_base]}) = ${result} (${baseNames[to_base]})`,
        },
      ],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

**ポイント：**
- `isError: true` をレスポンスに含めると、MCPクライアントはそれをエラーとして扱います
- エラーメッセージは具体的で、ユーザーが修正できる情報を含めるのがベストプラクティスです
- 数式評価は非常にセキュリティリスクが高いため、入力の厳格なバリデーションが必須です
- `parseInt()` の返り値と再エンコード結果の比較で、不正な桁を検出できます

</details>

---

## チャレンジ問題

---

### 問題9：Streamable HTTPトランスポートによるリモートMCPサーバー（チャレンジ）

Streamable HTTPトランスポートを使って、HTTP経由でアクセスできるリモートMCPサーバーを設計・実装してください。

**要件：**
- ExpressでHTTPサーバーを構築
- `/mcp` エンドポイントでMCPプロトコルを処理
- ステートレスモード（セッション管理なし）で動作
- 以下のツールを提供：
  1. `get_weather(city)` - 天気情報を返す（ダミーデータ）
  2. `get_news(category)` - ニュースを返す（ダミーデータ）
  3. `translate(text, to_lang)` - 翻訳を返す（ダミーデータ）

**期待される動作：**
```
# HTTPサーバーが http://localhost:3000 で起動
# MCPクライアントが http://localhost:3000/mcp に接続

get_weather("東京")
→ "東京の天気: 晴れ / 気温: 22°C / 湿度: 45%"

get_news("technology")
→ "テクノロジーニュース:
   1. AI技術の最新動向 - 新しいモデルが発表されました
   2. 量子コンピュータの進展 - 実用化に向けた新たな一歩"

translate("Hello, World!", "ja")
→ "翻訳結果: こんにちは、世界！"
```

<details>
<summary>ヒント</summary>

- `express` パッケージでHTTPサーバーを構築します
- `StreamableHTTPServerTransport` を使います
- ステートレスモードでは各リクエストが独立して処理されます
- POSTリクエストのbodyをトランスポートに渡し、レスポンスを返します
- GETリクエストはステートレスモードではサポートしないため405を返します
- DELETEリクエストもセッションがないため405を返します

</details>

<details>
<summary>解答例</summary>

```typescript
import express, { Request, Response } from "express";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

// ==================== サーバーとツールの定義 ====================

function createMcpServer(): McpServer {
  const server = new McpServer({
    name: "remote-api-server",
    version: "1.0.0",
  });

  // ダミー天気データ
  const weatherData: Record<string, { weather: string; temp: number; humidity: number }> = {
    "東京": { weather: "晴れ", temp: 22, humidity: 45 },
    "大阪": { weather: "曇り", temp: 20, humidity: 55 },
    "札幌": { weather: "雪", temp: -2, humidity: 70 },
    "那覇": { weather: "晴れ", temp: 28, humidity: 65 },
  };

  server.tool(
    "get_weather",
    "指定された都市の天気情報を取得します。",
    {
      city: z.string().describe("都市名（例: 東京）"),
    },
    async ({ city }) => {
      const data = weatherData[city];
      if (!data) {
        return {
          content: [
            {
              type: "text" as const,
              text: `"${city}" の天気情報は見つかりません。対応都市: ${Object.keys(weatherData).join(", ")}`,
            },
          ],
        };
      }
      return {
        content: [
          {
            type: "text" as const,
            text: `${city}の天気: ${data.weather} / 気温: ${data.temp}°C / 湿度: ${data.humidity}%`,
          },
        ],
      };
    }
  );

  // ダミーニュースデータ
  const newsData: Record<string, string[]> = {
    technology: [
      "AI技術の最新動向 - 新しいモデルが発表されました",
      "量子コンピュータの進展 - 実用化に向けた新たな一歩",
    ],
    business: [
      "株式市場が最高値を更新 - テック企業が牽引",
      "新しいスタートアップが大型資金調達に成功",
    ],
    science: [
      "火星探査の新発見 - 水の痕跡が確認されました",
      "再生医療の画期的な成果が発表されました",
    ],
  };

  server.tool(
    "get_news",
    "指定されたカテゴリのニュースを取得します。",
    {
      category: z
        .enum(["technology", "business", "science"])
        .describe("ニュースカテゴリ"),
    },
    async ({ category }) => {
      const categoryNames: Record<string, string> = {
        technology: "テクノロジー",
        business: "ビジネス",
        science: "サイエンス",
      };
      const articles = newsData[category] ?? [];
      const lines = articles.map((a, i) => `  ${i + 1}. ${a}`);

      return {
        content: [
          {
            type: "text" as const,
            text: `${categoryNames[category]}ニュース:\n${lines.join("\n")}`,
          },
        ],
      };
    }
  );

  // ダミー翻訳データ
  const translations: Record<string, Record<string, string>> = {
    ja: {
      "Hello, World!": "こんにちは、世界！",
      "Good morning": "おはようございます",
      "Thank you": "ありがとうございます",
    },
    en: {
      "こんにちは": "Hello",
      "ありがとう": "Thank you",
    },
  };

  server.tool(
    "translate",
    "テキストを指定された言語に翻訳します（ダミー）。",
    {
      text: z.string().describe("翻訳するテキスト"),
      to_lang: z.enum(["ja", "en"]).describe("翻訳先言語コード（ja / en）"),
    },
    async ({ text, to_lang }) => {
      const dict = translations[to_lang];
      const result = dict?.[text] ?? `[翻訳データなし] ${text} → ${to_lang}`;

      return {
        content: [
          {
            type: "text" as const,
            text: `翻訳結果: ${result}`,
          },
        ],
      };
    }
  );

  return server;
}

// ==================== HTTPサーバーの構築 ====================

const app = express();
app.use(express.json());

// POST /mcp - MCPリクエストを処理
app.post("/mcp", async (req: Request, res: Response) => {
  try {
    // リクエストごとに新しいサーバーとトランスポートを生成（ステートレス）
    const mcpServer = createMcpServer();
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined, // ステートレスモード
    });

    // サーバーとトランスポートを接続
    await mcpServer.connect(transport);

    // リクエストをトランスポートに渡して処理
    await transport.handleRequest(req, res);
  } catch (error) {
    console.error("MCPリクエスト処理エラー:", error);
    if (!res.headersSent) {
      res.status(500).json({ error: "Internal Server Error" });
    }
  }
});

// GET /mcp - ステートレスモードではSSEは不要なので405
app.get("/mcp", (_req: Request, res: Response) => {
  res.status(405).json({
    error: "Method Not Allowed",
    message: "このサーバーはステートレスモードで動作しています。GETリクエストはサポートされていません。",
  });
});

// DELETE /mcp - セッション管理なしのため405
app.delete("/mcp", (_req: Request, res: Response) => {
  res.status(405).json({
    error: "Method Not Allowed",
    message: "このサーバーはステートレスモードで動作しています。DELETEリクエストはサポートされていません。",
  });
});

// サーバー起動
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`リモートMCPサーバーが起動しました: http://localhost:${PORT}/mcp`);
});
```

**ポイント：**
- `StreamableHTTPServerTransport` はHTTP経由でMCPプロトコルを扱うためのトランスポートです
- `sessionIdGenerator: undefined` でステートレスモードになり、各リクエストが独立して処理されます
- ステートレスモードではリクエストごとにサーバーインスタンスを生成します
- GET（SSE接続）とDELETE（セッション終了）はステートレスモードでは不要なため405を返します
- 本番環境では認証ミドルウェアの追加が必須です

</details>

---

### 問題10：認証付きリモートMCPサーバーの設計（チャレンジ）

問題9を拡張して、以下のセキュリティ機能を追加した設計を行ってください。
コード実装に加えて、設計の考え方も記述してください。

**追加要件：**
1. Bearer Token認証ミドルウェア
2. レートリミット（1分あたり60リクエスト）
3. CORS設定
4. リクエストログの記録

**設計書として以下を記述してください：**
- セキュリティアーキテクチャ図（アスキーアート）
- 各ミドルウェアの責務
- エラーレスポンスの設計

**期待される設計出力例：**
```
[クライアント] → [CORS] → [認証] → [レートリミット] → [ログ] → [MCP処理]
```

<details>
<summary>ヒント</summary>

- Expressのミドルウェアチェーンで各機能を順番に処理します
- 認証はリクエストヘッダの `Authorization: Bearer <token>` を検証します
- レートリミットはIPアドレスごとにカウンターを管理します
- CORSは `Access-Control-Allow-Origin` 等のヘッダを設定します

</details>

<details>
<summary>解答例</summary>

```typescript
/*
 * ==================== セキュリティアーキテクチャ ====================
 *
 * リクエスト処理フロー:
 *
 *   [MCPクライアント]
 *         │
 *         ▼
 *   ┌─────────────┐
 *   │   CORS      │  ← オリジン検証・プリフライト応答
 *   └──────┬──────┘
 *          ▼
 *   ┌─────────────┐
 *   │   認証       │  ← Bearer Token 検証
 *   └──────┬──────┘
 *          ▼
 *   ┌─────────────┐
 *   │ レートリミット │  ← IP別リクエスト数制限
 *   └──────┬──────┘
 *          ▼
 *   ┌─────────────┐
 *   │   ログ記録   │  ← リクエスト情報の記録
 *   └──────┬──────┘
 *          ▼
 *   ┌─────────────┐
 *   │  MCP処理     │  ← ツール実行・レスポンス生成
 *   └─────────────┘
 *
 * エラーレスポンス設計:
 *   - 401 Unauthorized: トークン未指定 or 無効
 *   - 403 Forbidden: トークンの権限不足
 *   - 429 Too Many Requests: レートリミット超過
 *   - 500 Internal Server Error: サーバー内部エラー
 */

import express, { Request, Response, NextFunction } from "express";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const app = express();
app.use(express.json());

// ==================== 1. CORS ミドルウェア ====================
// 責務: 許可されたオリジンからのリクエストのみ受け付ける

const ALLOWED_ORIGINS = ["https://your-app.example.com"];

function corsMiddleware(req: Request, res: Response, next: NextFunction): void {
  const origin = req.headers.origin;

  if (origin && ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
  }

  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  res.setHeader("Access-Control-Max-Age", "86400");

  // プリフライトリクエストへの応答
  if (req.method === "OPTIONS") {
    res.status(204).end();
    return;
  }

  next();
}

// ==================== 2. 認証ミドルウェア ====================
// 責務: Bearer Tokenの検証

const VALID_TOKENS = new Set([
  "mcp-token-abc123",
  "mcp-token-def456",
]);

function authMiddleware(req: Request, res: Response, next: NextFunction): void {
  const authHeader = req.headers.authorization;

  if (!authHeader) {
    res.status(401).json({
      error: "Unauthorized",
      message: "Authorization ヘッダが必要です。",
    });
    return;
  }

  if (!authHeader.startsWith("Bearer ")) {
    res.status(401).json({
      error: "Unauthorized",
      message: "Bearer Token 形式で指定してください。",
    });
    return;
  }

  const token = authHeader.slice(7);

  if (!VALID_TOKENS.has(token)) {
    res.status(401).json({
      error: "Unauthorized",
      message: "無効なトークンです。",
    });
    return;
  }

  next();
}

// ==================== 3. レートリミットミドルウェア ====================
// 責務: IPアドレスごとに1分あたりのリクエスト数を制限

interface RateLimitEntry {
  count: number;
  resetAt: number;
}

const rateLimitStore = new Map<string, RateLimitEntry>();
const RATE_LIMIT = 60;            // 1分あたりの最大リクエスト数
const RATE_WINDOW_MS = 60 * 1000; // 1分間のウィンドウ

function rateLimitMiddleware(req: Request, res: Response, next: NextFunction): void {
  const clientIp = req.ip ?? "unknown";
  const now = Date.now();

  let entry = rateLimitStore.get(clientIp);

  // ウィンドウの期限切れ or 初回アクセスならリセット
  if (!entry || now > entry.resetAt) {
    entry = { count: 0, resetAt: now + RATE_WINDOW_MS };
    rateLimitStore.set(clientIp, entry);
  }

  entry.count++;

  // レートリミットヘッダの付与
  res.setHeader("X-RateLimit-Limit", RATE_LIMIT.toString());
  res.setHeader("X-RateLimit-Remaining", Math.max(0, RATE_LIMIT - entry.count).toString());
  res.setHeader("X-RateLimit-Reset", Math.ceil(entry.resetAt / 1000).toString());

  if (entry.count > RATE_LIMIT) {
    const retryAfter = Math.ceil((entry.resetAt - now) / 1000);
    res.setHeader("Retry-After", retryAfter.toString());
    res.status(429).json({
      error: "Too Many Requests",
      message: `レート制限を超えました。${retryAfter}秒後に再試行してください。`,
    });
    return;
  }

  next();
}

// ==================== 4. ログミドルウェア ====================
// 責務: リクエスト情報の記録

function logMiddleware(req: Request, _res: Response, next: NextFunction): void {
  const timestamp = new Date().toISOString();
  const method = req.method;
  const path = req.path;
  const ip = req.ip ?? "unknown";

  console.log(`[${timestamp}] ${method} ${path} - IP: ${ip}`);

  next();
}

// ==================== ミドルウェアの適用 ====================

app.use("/mcp", corsMiddleware);
app.use("/mcp", authMiddleware);
app.use("/mcp", rateLimitMiddleware);
app.use("/mcp", logMiddleware);

// ==================== MCPサーバーの定義 ====================

function createMcpServer(): McpServer {
  const server = new McpServer({
    name: "secure-remote-server",
    version: "1.0.0",
  });

  server.tool(
    "get_weather",
    "天気情報を取得します。",
    { city: z.string().describe("都市名") },
    async ({ city }) => ({
      content: [
        {
          type: "text" as const,
          text: `${city}の天気: 晴れ / 気温: 22°C / 湿度: 45%`,
        },
      ],
    })
  );

  return server;
}

// ==================== エンドポイント ====================

app.post("/mcp", async (req: Request, res: Response) => {
  try {
    const mcpServer = createMcpServer();
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
    });
    await mcpServer.connect(transport);
    await transport.handleRequest(req, res);
  } catch (error) {
    console.error("MCP処理エラー:", error);
    if (!res.headersSent) {
      res.status(500).json({
        error: "Internal Server Error",
        message: "サーバー内部でエラーが発生しました。",
      });
    }
  }
});

// ヘルスチェック（認証不要）
app.get("/health", (_req: Request, res: Response) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`セキュアMCPサーバーが起動しました: http://localhost:${PORT}/mcp`);
});
```

**ポイント：**
- ミドルウェアは「責務の分離」の原則に従い、1つのミドルウェアに1つの機能を持たせます
- 処理順序は CORS → 認証 → レートリミット → ログ → MCP処理 が推奨です
  - CORSを最初に置くことで、プリフライトリクエストを早期に処理します
  - 認証をレートリミットの前に置くことで、未認証リクエストをカウントしません
- レートリミットのストアは本番環境ではRedis等の外部ストアを使用します
- 本番環境ではトークンをハッシュ化して保存し、環境変数から読み込みます
- `/health` エンドポイントはロードバランサーからのヘルスチェック用で、認証をバイパスします

</details>

---

**お疲れさまでした！** この演習を通じて、TypeScript SDKによるMCPサーバー開発の基本から、リモートサーバーの設計・セキュリティまでを実践できました。次の章ではMCPクライアントの実装に進みます。
