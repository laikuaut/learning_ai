#!/bin/bash
# ============================================================
# Claude Code Git操作自動化デモ
# ============================================================
#
# 学べる内容:
#   - Claude Code を使ったコミットメッセージの自動生成
#   - PR（プルリクエスト）の作成自動化
#   - ブランチ管理の自動化
#   - コードレビューの依頼
#   - Git操作のワンショットモード活用
#
# 実行方法:
#   chmod +x 03_Git操作自動化デモ.sh
#   ./03_Git操作自動化デモ.sh
#
# 注意:
#   このスクリプトはデモ用のGitリポジトリを /tmp に作成します。
#   実際にClaude Codeを呼び出す部分はコメントアウトされています。
#   コメントを外して実行すると実際にClaude Codeが動作します。
# ============================================================

# デモ用ディレクトリ
DEMO_DIR="/tmp/claude-git-demo"

echo "============================================================"
echo " Claude Code Git操作自動化デモ"
echo "============================================================"
echo ""

# ----------------------------------------------------------
# 1. デモ用Gitリポジトリの準備
# ----------------------------------------------------------
echo "【1】デモ用Gitリポジトリを準備します"
echo "------------------------------------------------------------"

# クリーンなデモ環境を作成
rm -rf "$DEMO_DIR"
mkdir -p "$DEMO_DIR"
cd "$DEMO_DIR" || exit 1
git init
git config user.email "demo@example.com"
git config user.name "Demo User"

# 初期ファイルを作成してコミット
cat > "$DEMO_DIR/main.py" << 'PYEOF'
def hello():
    print("Hello, World!")

if __name__ == "__main__":
    hello()
PYEOF

git add main.py
git commit -m "初期コミット: main.py を追加"
echo "デモ用リポジトリを作成しました: $DEMO_DIR"
echo ""

# ----------------------------------------------------------
# 2. コミットメッセージの自動生成
# ----------------------------------------------------------
# Claude Code の /commit コマンドを使うと、
# 変更内容を分析して適切なコミットメッセージを生成してくれる
echo "【2】コミットメッセージの自動生成"
echo "------------------------------------------------------------"

# デモ用に変更を追加
cat > "$DEMO_DIR/utils.py" << 'PYEOF'
def add(a: int, b: int) -> int:
    """2つの整数を足し算する"""
    return a + b

def multiply(a: int, b: int) -> int:
    """2つの整数を掛け算する"""
    return a * b
PYEOF

# main.py を更新
cat > "$DEMO_DIR/main.py" << 'PYEOF'
from utils import add, multiply

def hello():
    print("Hello, World!")
    print(f"1 + 2 = {add(1, 2)}")
    print(f"3 * 4 = {multiply(3, 4)}")

if __name__ == "__main__":
    hello()
PYEOF

git add -A

echo "変更内容:"
git diff --cached --stat
echo ""

# 方法1: 対話モードで /commit コマンドを使う
echo "方法1: 対話モードで /commit を使用"
echo "  $ claude"
echo "  > /commit"
echo "  → 変更内容を分析してコミットメッセージを提案してくれます"
echo ""

# 方法2: ワンショットモードでコミットメッセージを生成
echo "方法2: ワンショットモードでコミット"
echo "  $ claude -p \"現在のステージされた変更をコミットして。コミットメッセージはConventional Commitsに従って\""
echo ""

# 方法3: git diff の出力をパイプで渡す
echo "方法3: git diff をパイプで渡して生成"
echo "  $ git diff --cached | claude -p \"この変更に適切なコミットメッセージを日本語で提案して\""
echo ""

# 実行例（コメントアウト）
# claude -p "ステージされた変更を確認して、Conventional Commits形式でコミットして"

# デモ用に手動コミット
git commit -m "feat: utils.py を追加し、main.py から利用するよう変更"
echo ""

# ----------------------------------------------------------
# 3. ブランチ管理の自動化
# ----------------------------------------------------------
echo "【3】ブランチ管理の自動化"
echo "------------------------------------------------------------"

echo "Claude Code を使ったブランチ操作の例:"
echo ""

# 機能ブランチの作成
echo "● 新機能ブランチの作成と実装:"
echo "  $ claude -p \"'ユーザー認証機能'用の機能ブランチを作成して、基本的な実装をして\""
echo ""

# 実際のブランチ作成（デモ）
git checkout -b feature/add-tests
echo "デモ: feature/add-tests ブランチを作成しました"
echo ""

# テストファイルを追加
cat > "$DEMO_DIR/test_utils.py" << 'PYEOF'
from utils import add, multiply

def test_add():
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 5) == 0
    assert multiply(-2, 3) == -6

if __name__ == "__main__":
    test_add()
    test_multiply()
    print("全テスト合格!")
PYEOF

git add test_utils.py
git commit -m "test: utils.py のユニットテストを追加"
echo ""

# ----------------------------------------------------------
# 4. PR（プルリクエスト）の作成
# ----------------------------------------------------------
echo "【4】PRの作成自動化"
echo "------------------------------------------------------------"
echo ""
echo "Claude Code を使ったPR作成の方法:"
echo ""

# 方法1: 対話モードでPR作成を依頼
echo "方法1: 対話モードでPR作成"
echo "  $ claude"
echo "  > このブランチの変更内容でPRを作成して"
echo "  → gh pr create を使ってPRを自動作成してくれます"
echo ""

# 方法2: ワンショットモードでPR作成
echo "方法2: ワンショットモード"
echo "  $ claude -p \"mainブランチに対するPRを作成して。タイトルと説明は変更内容から自動生成して\""
echo ""

# 方法3: 詳細な指示を与えてPR作成
echo "方法3: 詳細な指示付き"
echo "  $ claude -p \"以下の条件でPRを作成して:"
echo "    - タイトルはConventional Commits形式"
echo "    - 説明に変更内容のサマリーを含める"
echo "    - テスト計画を記載する"
echo "    - レビュアーに @teamlead を指定\""
echo ""

# ブランチ間の差分を確認（PR作成前の確認）
echo "現在のブランチの変更内容（main との差分）:"
git log main..HEAD --oneline
echo ""

# ----------------------------------------------------------
# 5. コードレビューの自動化
# ----------------------------------------------------------
echo "【5】コードレビューの自動化"
echo "------------------------------------------------------------"
echo ""

echo "Claude Code を使ったコードレビュー:"
echo ""
echo "● PRのレビュー依頼:"
echo "  $ claude -p \"PR #123 をレビューして。セキュリティ、パフォーマンス、コード品質の観点で\""
echo ""
echo "● 特定のファイルのレビュー:"
echo "  $ claude -p \"main.py をレビューして。改善点があれば修正して\""
echo ""
echo "● diff を渡してレビュー:"
echo "  $ git diff main..feature/add-tests | claude -p \"この変更をレビューして\""
echo ""

# ----------------------------------------------------------
# 6. Gitワークフロー自動化スクリプト例
# ----------------------------------------------------------
echo "【6】実用的なGitワークフロー自動化スクリプト例"
echo "============================================================"
echo ""
echo "--- 例: 日次レビュースクリプト ---"
echo ""
cat << 'SCRIPT_EXAMPLE'
#!/bin/bash
# 前日のコミットをレビューする自動化スクリプト

# 前日のコミット一覧を取得
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
COMMITS=$(git log --since="$YESTERDAY" --oneline)

if [ -z "$COMMITS" ]; then
    echo "前日のコミットはありません"
    exit 0
fi

# Claude Code にレビューを依頼
echo "$COMMITS" | claude -p \
    "以下のコミット一覧を確認し、問題がありそうなものがあれば指摘してください"
SCRIPT_EXAMPLE
echo ""

echo "--- 例: 自動コミット＆PRスクリプト ---"
echo ""
cat << 'SCRIPT_EXAMPLE2'
#!/bin/bash
# 変更をコミットしてPRを作成する自動化スクリプト

# ステージされた変更がなければ終了
if git diff --cached --quiet; then
    echo "ステージされた変更がありません"
    exit 0
fi

# Claude Code でコミット＆PR作成
claude -p "ステージされた変更をコミットして、mainブランチへのPRを作成して"
SCRIPT_EXAMPLE2
echo ""

# ----------------------------------------------------------
# 7. ブランチ一覧の確認（デモ）
# ----------------------------------------------------------
echo "【7】デモリポジトリの最終状態"
echo "------------------------------------------------------------"
echo ""
echo "ブランチ一覧:"
git branch
echo ""
echo "コミット履歴:"
git log --all --oneline --graph
echo ""

echo "============================================================"
echo " デモ完了 - デモファイルは $DEMO_DIR に作成されました"
echo "============================================================"
