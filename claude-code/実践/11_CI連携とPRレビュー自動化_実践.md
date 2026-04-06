# 実践課題11：CI連携とPRレビュー自動化 ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第8章（全章の知識を総合的に活用）
> **課題の種類**: ミニプロジェクト（総合設計）
> **学習目標**: Claude Codeをチーム開発のCI/CDパイプラインに組み込み、PRの自動レビュー、コード品質チェック、変更要約の自動生成を実現する

---

## 完成イメージ

GitHub Actionsと連携し、PRが作成されるとClaude Codeが自動でレビューコメントを投稿するシステムを構築します。

```
PR作成
  ↓
GitHub Actions 起動
  ↓
┌─────────────────────────────────────────┐
│ 1. PRの差分を取得                        │
│ 2. Claude Codeでコードレビュー実行       │
│ 3. レビュー結果をPRコメントに投稿        │
│ 4. 変更サマリーをPRの説明に追記          │
└─────────────────────────────────────────┘
  ↓
開発者がレビュー結果を確認
```

プロジェクト構造:
```
my-team-project/
├── .github/
│   └── workflows/
│       └── claude-review.yml
├── scripts/
│   ├── review-pr.sh
│   ├── summarize-changes.sh
│   └── check-quality.sh
├── .claude/
│   └── settings.json
├── CLAUDE.md
└── src/
    └── ...
```

---

## 課題の要件

1. PRの自動レビュースクリプトを作成する（Claude Codeワンショットモード活用）
2. 変更サマリーの自動生成スクリプトを作成する
3. コード品質チェックスクリプトを作成する
4. GitHub Actionsワークフローファイルを作成する
5. CLAUDE.mdにレビュー基準を記載する
6. エラーハンドリングとコスト制御の仕組みを組み込む

---

## ステップガイド

<details>
<summary>ステップ1：プロジェクトの基本構造を作成</summary>

```bash
mkdir -p ~/claude-code-practice/task11/my-team-project
cd ~/claude-code-practice/task11/my-team-project
git init

# ディレクトリ構造
mkdir -p .github/workflows
mkdir -p scripts
mkdir -p .claude
mkdir -p src

# 基本ファイル
cat > package.json << 'EOF'
{
  "name": "my-team-project",
  "version": "1.0.0",
  "scripts": {
    "test": "jest",
    "lint": "eslint src/",
    "build": "tsc"
  }
}
EOF

cat > README.md << 'EOF'
# My Team Project
Claude Code CI連携のデモプロジェクト
EOF
```

</details>

<details>
<summary>ステップ2：レビュースクリプトの作成</summary>

PRの差分をClaude Codeに渡してレビューを実行するスクリプトです。

```bash
cat > scripts/review-pr.sh << 'SCRIPT'
#!/bin/bash
set -euo pipefail

# === 設定 ===
PR_NUMBER=${1:?'使い方: ./scripts/review-pr.sh <PR番号>'}
REPO=${GITHUB_REPOSITORY:-$(gh repo view --json nameWithOwner -q '.nameWithOwner')}
MAX_DIFF_LINES=500

echo "=== PR #${PR_NUMBER} の自動レビュー ==="

# === 差分取得 ===
DIFF=$(gh pr diff "$PR_NUMBER" --repo "$REPO" 2>/dev/null)
if [ -z "$DIFF" ]; then
    echo "ERROR: PRの差分を取得できませんでした"
    exit 1
fi

# 差分が大きすぎる場合は要約版を使用
DIFF_LINES=$(echo "$DIFF" | wc -l)
if [ "$DIFF_LINES" -gt "$MAX_DIFF_LINES" ]; then
    echo "WARNING: 差分が${DIFF_LINES}行あります。統計情報のみでレビューします。"
    DIFF=$(gh pr diff "$PR_NUMBER" --repo "$REPO" | diffstat 2>/dev/null || gh pr diff "$PR_NUMBER" --repo "$REPO" | head -n "$MAX_DIFF_LINES")
fi

# === PR情報取得 ===
PR_INFO=$(gh pr view "$PR_NUMBER" --repo "$REPO" --json title,body,files 2>/dev/null)
PR_TITLE=$(echo "$PR_INFO" | jq -r '.title')
PR_FILES=$(echo "$PR_INFO" | jq -r '.files[].path' | head -20)

# === Claude Codeでレビュー ===
REVIEW=$(echo "$DIFF" | claude -p "
あなたはシニアエンジニアです。以下のPRをレビューしてください。

## PR情報
- タイトル: ${PR_TITLE}
- 変更ファイル:
${PR_FILES}

## レビュー観点
1. **バグの可能性**: ロジックエラー、エッジケースの未処理
2. **セキュリティ**: SQLインジェクション、XSS、認証の漏れ
3. **パフォーマンス**: N+1クエリ、不要なループ、メモリリーク
4. **可読性**: 命名、コメント、複雑度
5. **テスト**: テストカバレッジ、重要なケースの漏れ

## 出力形式
### 概要
（1-2行でPR全体の評価）

### 指摘事項
（重要度: 高/中/低 を付けて箇条書き）

### 良い点
（1-3つ）

### 総合判定
LGTM / 修正推奨 / 要修正

## 差分
以下のコード差分をレビューしてください：
" --max-turns 3 --output-format text 2>/dev/null)

if [ -z "$REVIEW" ]; then
    echo "ERROR: レビューの生成に失敗しました"
    exit 1
fi

# === PRにコメント投稿 ===
gh pr comment "$PR_NUMBER" --repo "$REPO" --body "## 自動コードレビュー

${REVIEW}

---
*このレビューはClaude Codeによる自動生成です（$(date '+%Y-%m-%d %H:%M')）*
*人間のレビューも必ず受けてください。*"

echo "=== レビュー完了: PR #${PR_NUMBER} ==="
SCRIPT

chmod +x scripts/review-pr.sh
```

</details>

<details>
<summary>ステップ3：変更サマリースクリプトの作成</summary>

```bash
cat > scripts/summarize-changes.sh << 'SCRIPT'
#!/bin/bash
set -euo pipefail

PR_NUMBER=${1:?'使い方: ./scripts/summarize-changes.sh <PR番号>'}
REPO=${GITHUB_REPOSITORY:-$(gh repo view --json nameWithOwner -q '.nameWithOwner')}

echo "=== PR #${PR_NUMBER} の変更サマリー生成 ==="

# 差分取得
DIFF=$(gh pr diff "$PR_NUMBER" --repo "$REPO" | head -n 300)

# Claude Codeでサマリー生成
SUMMARY=$(echo "$DIFF" | claude -p "
以下のコード差分を読んで、変更内容を日本語で簡潔にまとめてください。

## 出力形式
### 変更の概要
（1-2文で要約）

### 主な変更点
- （箇条書きで3-5項目）

### 影響範囲
- （影響を受けるコンポーネントや機能）
" --max-turns 2 --output-format text 2>/dev/null)

echo "$SUMMARY"
SCRIPT

chmod +x scripts/summarize-changes.sh
```

</details>

<details>
<summary>ステップ4：コード品質チェックスクリプトの作成</summary>

```bash
cat > scripts/check-quality.sh << 'SCRIPT'
#!/bin/bash
set -euo pipefail

PR_NUMBER=${1:?'使い方: ./scripts/check-quality.sh <PR番号>'}
REPO=${GITHUB_REPOSITORY:-$(gh repo view --json nameWithOwner -q '.nameWithOwner')}

echo "=== PR #${PR_NUMBER} の品質チェック ==="

# 変更されたファイル一覧を取得
FILES=$(gh pr view "$PR_NUMBER" --repo "$REPO" --json files -q '.files[].path')

ISSUES=""

# チェック1: .envファイルの混入
if echo "$FILES" | grep -qE '\.env'; then
    ISSUES="${ISSUES}\n- :warning: **.envファイルが含まれています**。機密情報がコミットされていないか確認してください。"
fi

# チェック2: 大きすぎるファイルの変更
LARGE_FILES=$(gh pr diff "$PR_NUMBER" --repo "$REPO" | grep '^+++' | while read line; do
    FILE=$(echo "$line" | sed 's/^+++ b\///')
    ADDITIONS=$(gh pr diff "$PR_NUMBER" --repo "$REPO" | grep -c "^+[^+]" || true)
    if [ "$ADDITIONS" -gt 300 ]; then
        echo "$FILE ($ADDITIONS行追加)"
    fi
done)
if [ -n "$LARGE_FILES" ]; then
    ISSUES="${ISSUES}\n- :mag: **大規模な変更が含まれています**: ${LARGE_FILES}。分割を検討してください。"
fi

# チェック3: テストファイルの有無
HAS_SRC_CHANGE=$(echo "$FILES" | grep -c '^src/' || true)
HAS_TEST_CHANGE=$(echo "$FILES" | grep -c '^tests/' || true)
if [ "$HAS_SRC_CHANGE" -gt 0 ] && [ "$HAS_TEST_CHANGE" -eq 0 ]; then
    ISSUES="${ISSUES}\n- :test_tube: **テストファイルの変更がありません**。テストの追加を検討してください。"
fi

# 結果出力
if [ -n "$ISSUES" ]; then
    BODY="## 品質チェック結果\n\n以下の点を確認してください：\n${ISSUES}"
    echo -e "$BODY"
    gh pr comment "$PR_NUMBER" --repo "$REPO" --body "$(echo -e "$BODY")"
else
    echo "品質チェック: 問題なし"
fi
SCRIPT

chmod +x scripts/check-quality.sh
```

</details>

<details>
<summary>ステップ5：GitHub Actionsワークフローの作成</summary>

```bash
cat > .github/workflows/claude-review.yml << 'YAML'
name: Claude Code Auto Review

on:
  pull_request:
    types: [opened, synchronize]

# PRへのコメント投稿に必要な権限
permissions:
  contents: read
  pull-requests: write

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Quality Check
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: ./scripts/check-quality.sh ${{ github.event.pull_request.number }}

  claude-review:
    runs-on: ubuntu-latest
    # 品質チェック後にレビューを実行
    needs: quality-check
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code
      
      - name: Run Claude Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
        run: ./scripts/review-pr.sh ${{ github.event.pull_request.number }}
        timeout-minutes: 5

  summarize:
    runs-on: ubuntu-latest
    needs: quality-check
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Generate Summary
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
        run: |
          SUMMARY=$(./scripts/summarize-changes.sh ${{ github.event.pull_request.number }})
          gh pr comment ${{ github.event.pull_request.number }} --body "## 変更サマリー

          ${SUMMARY}
          "
        timeout-minutes: 3
YAML
```

</details>

<details>
<summary>ステップ6：CLAUDE.mdとsettings.jsonの作成</summary>

```bash
# CLAUDE.md
cat > CLAUDE.md << 'EOF'
# My Team Project

## 概要
チーム開発プロジェクト。Claude Code CIによる自動レビュー機能付き。

## 技術スタック
- TypeScript, Express, Jest, ESLint

## コーディング規約
- 命名: camelCase (変数/関数), PascalCase (クラス/型)
- コミット: Conventional Commits (feat:, fix:, chore:)
- テスト: 新機能には必ずテストを追加

## CIパイプライン
- PR作成時: 品質チェック → Claude Codeレビュー → 変更サマリー生成
- scripts/ 内のスクリプトは手動でも実行可能

## 重要なルール
- ANTHROPIC_API_KEYはGitHub Secretsで管理（コードに埋め込まない）
- CIでのClaude Code実行は--max-turnsで制限する（コスト制御）
- 自動レビューはあくまで補助。人間のレビューを代替するものではない
EOF

# settings.json
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(ts|tsx|js|jsx)$'; then cd \"$CLAUDE_PROJECT_DIR\" && npx eslint --fix \"$CLAUDE_FILE_PATH\" 2>&1 || true; fi"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm\\s+-rf|DROP\\s+TABLE|git\\s+push.*main'; then echo 'BLOCKED' >&2; exit 2; fi"
      }
    ]
  }
}
EOF

# 初回コミット
git add -A
git commit -m "feat: Add Claude Code CI integration with auto-review"
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）── 最小構成のCI連携</summary>

最小構成として、レビュースクリプト1つとGitHub Actionsだけで始められます。

```bash
# 最小構成のレビュースクリプト
mkdir -p scripts
cat > scripts/review-pr.sh << 'EOF'
#!/bin/bash
PR_NUM=${1:?'PR番号を指定してください'}
gh pr diff "$PR_NUM" | claude -p "このPRの差分をレビューしてください。バグ、セキュリティ、可読性の観点で指摘してください。" --max-turns 3
EOF
chmod +x scripts/review-pr.sh

# 最小構成のGitHub Actions
mkdir -p .github/workflows
cat > .github/workflows/claude-review.yml << 'EOF'
name: Claude Review
on:
  pull_request:
    types: [opened]
permissions:
  contents: read
  pull-requests: write
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install -g @anthropic-ai/claude-code
      - run: ./scripts/review-pr.sh ${{ github.event.pull_request.number }}
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        timeout-minutes: 5
EOF
```

</details>

<details>
<summary>解答例（改良版）── プロダクション品質のCI連携</summary>

改良版は、エラーハンドリング、コスト制御、レートリミット対策まで含む完全版です。

各スクリプトの差分ポイント:

**1. エラーハンドリングの強化:**
```bash
# Claude Code実行のラッパー関数
run_claude() {
    local input="$1"
    local prompt="$2"
    local max_turns="${3:-3}"
    local result
    
    result=$(echo "$input" | timeout 120 claude -p "$prompt" \
        --max-turns "$max_turns" \
        --output-format text 2>/dev/null) || {
        echo "WARNING: Claude Codeの実行に失敗しました（タイムアウトまたはAPIエラー）"
        return 1
    }
    
    if [ -z "$result" ]; then
        echo "WARNING: Claude Codeの出力が空でした"
        return 1
    fi
    
    echo "$result"
}
```

**2. コスト制御:**
```yaml
# GitHub Actionsでの月額上限チェック
- name: Check monthly budget
  run: |
    MONTHLY_RUNS=$(gh api repos/${{ github.repository }}/actions/runs \
      --jq '[.workflow_runs[] | select(.name == "Claude Review" and .created_at > "2024-01-01")] | length')
    if [ "$MONTHLY_RUNS" -gt 100 ]; then
      echo "WARNING: 月間実行回数が上限（100回）に達しました"
      exit 0  # エラーにせず、スキップ
    fi
```

**3. レビュー結果のキャッシュ:**
```bash
# 同じコミットに対する重複レビューを防止
LAST_COMMIT=$(gh pr view "$PR_NUMBER" --json headRefOid -q '.headRefOid')
CACHE_FILE="/tmp/claude-review-${PR_NUMBER}-${LAST_COMMIT:0:8}"
if [ -f "$CACHE_FILE" ]; then
    echo "このコミットは既にレビュー済みです。スキップします。"
    exit 0
fi
```

**初心者向けとの違い:**
- 初心者向けは「まず動く」ことを目指した最小構成です
- 改良版はプロダクション環境で安定して運用するための考慮（タイムアウト、エラーハンドリング、コスト制御、キャッシュ）を含んでいます
- チームの規模や予算に応じて、段階的に改良版に近づけていくのが現実的なアプローチです

</details>
