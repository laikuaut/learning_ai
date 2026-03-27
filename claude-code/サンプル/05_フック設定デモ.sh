#!/bin/bash
# ============================================================
# Claude Code フック設定デモ
# ============================================================
#
# 学べる内容:
#   - Claude Code フック機能の概要と仕組み
#   - PreToolUse フックの設定方法（ツール実行前の制御）
#   - PostToolUse フックの設定方法（ツール実行後の処理）
#   - Notification フックの設定方法（通知の自動化）
#   - リンター・フォーマッター連携フックの実践例
#   - settings.json でのフック設定の書き方
#
# 実行方法:
#   chmod +x 05_フック設定デモ.sh
#   ./05_フック設定デモ.sh
#
# 注意:
#   このスクリプトはフック設定のサンプルファイルを作成するデモです。
#   実際のフック動作にはClaude Codeの環境が必要です。
# ============================================================

# デモ用ディレクトリ
DEMO_DIR="/tmp/claude-hooks-demo"

echo "============================================================"
echo " Claude Code フック設定デモ"
echo "============================================================"
echo ""

# ----------------------------------------------------------
# 1. フック機能の概要
# ----------------------------------------------------------
echo "【1】Claude Code フック機能とは"
echo "------------------------------------------------------------"
echo ""
echo "  フック（Hooks）は、Claude Codeのアクションの前後に"
echo "  カスタムスクリプトを自動実行する仕組みです。"
echo ""
echo "  利用可能なフックの種類:"
echo ""
echo "    PreToolUse    - ツール実行前に呼ばれる"
echo "                    （実行のブロックや入力の検証に使用）"
echo ""
echo "    PostToolUse   - ツール実行後に呼ばれる"
echo "                    （リンター実行やログ記録に使用）"
echo ""
echo "    Notification  - Claude Codeが通知を送る時に呼ばれる"
echo "                    （外部通知サービスとの連携に使用）"
echo ""
echo "    Stop          - エージェントが応答を終了する前に呼ばれる"
echo "                    （追加タスクの実行に使用）"
echo ""

# ----------------------------------------------------------
# 2. デモ環境の準備
# ----------------------------------------------------------
echo "【2】デモ環境を準備します"
echo "------------------------------------------------------------"

rm -rf "$DEMO_DIR"
mkdir -p "$DEMO_DIR/.claude"
mkdir -p "$DEMO_DIR/scripts"
cd "$DEMO_DIR" || exit 1
git init --quiet
echo "デモディレクトリ: $DEMO_DIR"
echo ""

# ----------------------------------------------------------
# 3. PreToolUse フックの設定例
# ----------------------------------------------------------
echo "【3】PreToolUse フック（ツール実行前のフック）"
echo "------------------------------------------------------------"
echo ""
echo "  PreToolUse フックはツールが実行される前に呼ばれます。"
echo "  フックスクリプトの終了コードで動作を制御できます:"
echo ""
echo "    終了コード 0  → ツール実行を許可（自動承認）"
echo "    終了コード 2  → ツール実行をブロック"
echo "    その他        → 通常の権限チェックにフォールバック"
echo ""

# PreToolUse フック用のスクリプト例を作成
cat > "$DEMO_DIR/scripts/check_write_path.sh" << 'HOOKEOF'
#!/bin/bash
# ============================================================
# PreToolUse フック: 書き込み先パスのチェック
# ============================================================
# Write/Edit ツールが特定のパスに書き込もうとした場合にブロックする
#
# このスクリプトは標準入力からJSON形式でツール情報を受け取る:
# {
#   "tool_name": "Write",
#   "tool_input": {
#     "file_path": "/path/to/file",
#     "content": "..."
#   }
# }

# 標準入力からJSONを読み取る
INPUT=$(cat)

# ツール名を取得
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

# Write または Edit ツールの場合のみチェック
if [ "$TOOL_NAME" = "Write" ] || [ "$TOOL_NAME" = "Edit" ]; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

    # 本番環境の設定ファイルへの書き込みをブロック
    if echo "$FILE_PATH" | grep -qE "(production|prod)\.(env|config|json|yaml)"; then
        echo "エラー: 本番環境の設定ファイルへの書き込みはブロックされています"
        echo "ファイル: $FILE_PATH"
        exit 2  # 終了コード 2 でブロック
    fi

    # .env ファイルへの書き込みを警告
    if echo "$FILE_PATH" | grep -qE "\.env$"; then
        echo "警告: .env ファイルへの書き込みです。機密情報を含めないでください。"
        # 終了コード 0 以外を返して通常の権限チェックに任せる
        exit 1
    fi
fi

# その他の場合は通常の権限チェックにフォールバック
exit 1
HOOKEOF

chmod +x "$DEMO_DIR/scripts/check_write_path.sh"

echo "--- スクリプト: scripts/check_write_path.sh ---"
echo "（本番設定ファイルへの書き込みをブロックするフック）"
echo ""

# ----------------------------------------------------------
# 4. PostToolUse フックの設定例
# ----------------------------------------------------------
echo "【4】PostToolUse フック（ツール実行後のフック）"
echo "------------------------------------------------------------"
echo ""
echo "  PostToolUse フックはツール実行後に呼ばれます。"
echo "  リンターやフォーマッターの自動実行に最適です。"
echo ""

# PostToolUse フック用のリンタースクリプト例を作成
cat > "$DEMO_DIR/scripts/auto_lint.sh" << 'HOOKEOF'
#!/bin/bash
# ============================================================
# PostToolUse フック: ファイル変更後の自動リント
# ============================================================
# Write/Edit ツールでファイルが変更された後にリンターを実行する
#
# 標準入力から受け取るJSON:
# {
#   "tool_name": "Write",
#   "tool_input": { "file_path": "/path/to/file.py", ... },
#   "tool_output": { ... }
# }

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

# Write または Edit ツールの場合のみ実行
if [ "$TOOL_NAME" = "Write" ] || [ "$TOOL_NAME" = "Edit" ]; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')
    EXTENSION="${FILE_PATH##*.}"

    case "$EXTENSION" in
        py)
            # Python ファイルの場合は ruff でリント
            echo "Python ファイルを検出: リンター (ruff) を実行します..."
            if command -v ruff &> /dev/null; then
                ruff check "$FILE_PATH" 2>&1
                ruff format --check "$FILE_PATH" 2>&1
            fi
            ;;
        js|ts|jsx|tsx)
            # JavaScript/TypeScript ファイルの場合は eslint でリント
            echo "JS/TS ファイルを検出: リンター (eslint) を実行します..."
            if command -v npx &> /dev/null; then
                npx eslint "$FILE_PATH" 2>&1
            fi
            ;;
        sh)
            # シェルスクリプトの場合は shellcheck でリント
            echo "シェルスクリプトを検出: shellcheck を実行します..."
            if command -v shellcheck &> /dev/null; then
                shellcheck "$FILE_PATH" 2>&1
            fi
            ;;
    esac
fi
HOOKEOF

chmod +x "$DEMO_DIR/scripts/auto_lint.sh"

echo "--- スクリプト: scripts/auto_lint.sh ---"
echo "（ファイル変更後に自動でリンターを実行するフック）"
echo ""

# ----------------------------------------------------------
# 5. Notification フックの設定例
# ----------------------------------------------------------
echo "【5】Notification フック（通知フック）"
echo "------------------------------------------------------------"
echo ""
echo "  Notification フックは、Claude Codeがユーザーの注意を"
echo "  引きたい場合（長時間タスクの完了時など）に呼ばれます。"
echo ""

# Notification フック用のスクリプト例を作成
cat > "$DEMO_DIR/scripts/notify.sh" << 'HOOKEOF'
#!/bin/bash
# ============================================================
# Notification フック: デスクトップ通知の送信
# ============================================================
# Claude Codeの処理完了時にデスクトップ通知を送る
#
# 標準入力から受け取るJSON:
# {
#   "message": "通知メッセージ"
# }

INPUT=$(cat)
MESSAGE=$(echo "$INPUT" | jq -r '.message // "Claude Codeからの通知"')

# OS に応じた通知方法を選択
if command -v notify-send &> /dev/null; then
    # Linux (libnotify)
    notify-send "Claude Code" "$MESSAGE"
elif command -v osascript &> /dev/null; then
    # macOS
    osascript -e "display notification \"$MESSAGE\" with title \"Claude Code\""
elif command -v powershell.exe &> /dev/null; then
    # WSL (Windows)
    powershell.exe -Command "[System.Windows.Forms.MessageBox]::Show('$MESSAGE', 'Claude Code')" 2>/dev/null
fi

# ターミナルベルも鳴らす（フォールバック）
echo -e "\a"

# ログファイルにも記録
echo "[$(date '+%Y-%m-%d %H:%M:%S')] $MESSAGE" >> /tmp/claude-notifications.log
HOOKEOF

chmod +x "$DEMO_DIR/scripts/notify.sh"

echo "--- スクリプト: scripts/notify.sh ---"
echo "（処理完了時にデスクトップ通知を送るフック）"
echo ""

# ----------------------------------------------------------
# 6. settings.json でのフック設定
# ----------------------------------------------------------
echo "【6】settings.json でのフック設定"
echo "============================================================"
echo ""
echo "  フックは settings.json の \"hooks\" セクションで設定します。"
echo ""

# 完全な settings.json を作成
cat > "$DEMO_DIR/.claude/settings.json" << 'SETTINGS_EOF'
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash(pytest:*)",
      "Bash(ruff:*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/check_write_path.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/auto_lint.sh"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/notify.sh"
          }
        ]
      }
    ]
  }
}
SETTINGS_EOF

echo "--- .claude/settings.json（フック設定付き）---"
cat "$DEMO_DIR/.claude/settings.json"
echo ""
echo ""

# ----------------------------------------------------------
# 7. matcher パターンの解説
# ----------------------------------------------------------
echo "【7】matcher パターンの解説"
echo "------------------------------------------------------------"
echo ""
echo "  matcher はフックを適用するツールを正規表現で指定します:"
echo ""
echo "  \"matcher\": \"Write\"         → Write ツールのみ"
echo "  \"matcher\": \"Write|Edit\"    → Write または Edit ツール"
echo "  \"matcher\": \"Bash\"          → Bash ツールのみ"
echo "  \"matcher\": \"\"              → 全てのツール"
echo ""
echo "  PreToolUse の matcher で指定可能なツール名:"
echo "    - Read        （ファイル読み取り）"
echo "    - Write       （ファイル書き込み）"
echo "    - Edit        （ファイル編集）"
echo "    - Bash        （コマンド実行）"
echo "    - Glob        （ファイル検索）"
echo "    - Grep        （テキスト検索）"
echo "    - WebFetch    （Web取得）"
echo ""

# ----------------------------------------------------------
# 8. 実践的なフック活用パターン
# ----------------------------------------------------------
echo "【8】実践的なフック活用パターン"
echo "============================================================"
echo ""

echo "--- パターン1: テスト自動実行 ---"
echo "Pythonファイル変更後に関連テストを自動実行"
echo ""
cat << 'PATTERN1'
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash -c 'FILE=$(echo $CLAUDE_TOOL_INPUT | jq -r .file_path); if [[ $FILE == *.py ]]; then pytest ${FILE/src/tests} 2>/dev/null; fi'"
        }
      ]
    }
  ]
}
PATTERN1
echo ""

echo "--- パターン2: 危険なコマンドのブロック ---"
echo "rm -rf / や DROP TABLE などの危険なコマンドをブロック"
echo ""
cat << 'PATTERN2'
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "bash -c 'CMD=$(cat | jq -r .tool_input.command); if echo \"$CMD\" | grep -qiE \"rm\\s+-rf\\s+/|DROP\\s+TABLE|DROP\\s+DATABASE|mkfs|dd\\s+if=|:(){ :|:& };:\"; then echo \"危険なコマンドをブロックしました: $CMD\"; exit 2; fi; exit 1'"
        }
      ]
    }
  ]
}
PATTERN2
echo ""

echo "--- パターン3: 変更ログの自動記録 ---"
echo "全てのファイル変更をログファイルに記録"
echo ""
cat << 'PATTERN3'
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash -c 'INPUT=$(cat); FILE=$(echo $INPUT | jq -r .tool_input.file_path); echo \"[$(date +\"%Y-%m-%d %H:%M:%S\")] 変更: $FILE\" >> .claude/changes.log'"
        }
      ]
    }
  ]
}
PATTERN3
echo ""

# ----------------------------------------------------------
# 9. 作成したファイルの確認
# ----------------------------------------------------------
echo "【9】作成したファイル一覧"
echo "------------------------------------------------------------"
echo ""
find "$DEMO_DIR" -name ".git" -prune -o -type f -print | sort | while read -r file; do
    echo "  ${file#$DEMO_DIR/}"
done
echo ""

echo "============================================================"
echo " デモ完了 - デモファイルは $DEMO_DIR に作成されました"
echo "============================================================"
