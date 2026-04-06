# 実践課題05：MCPサーバーの設定と活用 ★2

> **難易度**: ★★☆☆☆（基礎）
> **前提知識**: 第1章〜第3章（環境構築、基本操作、ファイル操作）、第5章（MCPサーバーとツール連携）
> **課題の種類**: ミニプロジェクト
> **学習目標**: MCPサーバーの設定ファイルの書き方を理解し、プロジェクトスコープとユーザースコープの使い分けを習得する

---

## 完成イメージ

プロジェクトにMCPサーバーの設定を追加し、Claude Codeから外部ツールを利用できる状態を作ります。

```
task05-mcp/
├── .claude/
│   └── settings.json        ← プロジェクトスコープの設定
├── README.md
└── src/
    └── app.js

~/.claude/settings.json      ← ユーザースコープの設定（既存）
```

設定後のClaude Codeセッション:
```
> /mcp
MCP Servers:
  ✓ filesystem (connected)
  ✓ github (connected)

> プロジェクト内の全ファイルサイズを一覧表示してください
（MCPツールを使って実行）
```

---

## 課題の要件

1. プロジェクトスコープの設定ファイル（`.claude/settings.json`）を作成する
2. ユーザースコープの設定ファイル（`~/.claude/settings.json`）の構造を確認する
3. MCPサーバーの設定項目（`mcpServers`）の書き方を理解する
4. `claude mcp add` コマンドでMCPサーバーを追加する
5. `/mcp` コマンドでMCPサーバーの接続状態を確認する
6. プロジェクトスコープとユーザースコープの違いを理解する

---

## ステップガイド

<details>
<summary>ステップ1：プロジェクトの準備</summary>

```bash
# プロジェクトディレクトリを作成
mkdir -p ~/claude-code-practice/task05
cd ~/claude-code-practice/task05

# Gitリポジトリとして初期化（MCPの設定にはGitリポジトリが推奨）
git init

# 基本ファイルを作成
echo '# MCP Practice Project' > README.md
mkdir -p src
echo 'console.log("MCP test");' > src/app.js

git add -A
git commit -m "Initial commit"
```

</details>

<details>
<summary>ステップ2：CLIでMCPサーバーを追加する</summary>

`claude mcp add` コマンドを使って、MCPサーバーを追加できます。

```bash
# filesystemサーバーを追加（プロジェクトスコープ）
claude mcp add filesystem -s project -- \
  npx -y @modelcontextprotocol/server-filesystem \
  ~/claude-code-practice/task05

# 設定を確認
claude mcp list
```

上記コマンドにより、`.claude/settings.json` にMCPサーバーの設定が追加されます。

</details>

<details>
<summary>ステップ3：設定ファイルを直接確認・編集する</summary>

CLIで追加された設定を確認し、手動での編集方法も学びましょう。

```bash
# プロジェクトスコープの設定を確認
cat .claude/settings.json
```

設定ファイルの構造:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user/claude-code-practice/task05"
      ]
    }
  }
}
```

各項目の意味:

| 項目 | 説明 |
|---|---|
| `mcpServers` | MCPサーバー設定のルートキー |
| `"filesystem"` | サーバーの識別名（任意の名前） |
| `command` | サーバーを起動するコマンド |
| `args` | コマンドの引数 |

</details>

<details>
<summary>ステップ4：ユーザースコープとの違いを確認する</summary>

```bash
# ユーザースコープの設定を確認
cat ~/.claude/settings.json

# ユーザースコープにMCPサーバーを追加する場合
claude mcp add github -s user -- \
  npx -y @modelcontextprotocol/server-github
```

スコープの使い分け:

```
ユーザースコープ（~/.claude/settings.json）
  → すべてのプロジェクトで使いたいサーバー
  → 例：GitHub MCPサーバー、個人用ツール
  → Gitにコミットされない

プロジェクトスコープ（.claude/settings.json）
  → 特定のプロジェクトでのみ使うサーバー
  → 例：プロジェクト専用のDB接続、ファイルシステム
  → Gitにコミットしてチームで共有可能

ローカルスコープ（.claude/settings.local.json）
  → プロジェクト固有だがGitにコミットしない設定
  → 例：個人のAPIキーを含む設定
  → .gitignoreに追加する
```

</details>

<details>
<summary>ステップ5：Claude Codeで接続確認</summary>

```bash
cd ~/claude-code-practice/task05
claude
```

対話モードで:
```
# MCP接続状態を確認
> /mcp

# MCPツールの一覧を確認
> 使えるMCPツールの一覧を表示してください
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）── CLIコマンドで設定</summary>

```bash
# 1. プロジェクト準備
mkdir -p ~/claude-code-practice/task05
cd ~/claude-code-practice/task05
git init
echo '# MCP Practice' > README.md
git add -A && git commit -m "Initial commit"

# 2. MCPサーバーを追加
claude mcp add filesystem -s project -- \
  npx -y @modelcontextprotocol/server-filesystem \
  ~/claude-code-practice/task05

# 3. 設定確認
claude mcp list

# 4. Claude Codeで確認
claude
# → /mcp を実行してサーバーの接続を確認
```

</details>

<details>
<summary>解答例（改良版）── 手動で設定ファイルを作成</summary>

CLIコマンドに頼らず、設定ファイルを直接作成する方法も覚えておくと応用が効きます。

```bash
# プロジェクトスコープの設定を手動作成
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "."
      ]
    }
  }
}
EOF

# ローカルスコープの設定（Gitにコミットしない）
cat > .claude/settings.local.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
}
EOF

# .gitignoreにローカル設定を追加
echo '.claude/settings.local.json' >> .gitignore
```

**初心者向けとの違い:**
- CLIコマンド（`claude mcp add`）は簡単ですが、設定内容がブラックボックスになりがちです
- 手動で設定ファイルを書くことで、`env`（環境変数）の設定やカスタムオプションなど、より細かい制御が可能です
- `settings.local.json` を使えば、APIキーなどの秘密情報をGitにコミットせずに管理できます
- チーム開発では、共通設定を `.claude/settings.json` に、個人設定を `.claude/settings.local.json` に分けるのがベストプラクティスです

</details>
