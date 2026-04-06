# 実践課題07：SSHエージェントと鍵管理 ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第3章（公開鍵認証の設定）、第4章（SSH設定ファイル）、第7章（SSHエージェントと多段接続）
> **課題の種類**: ミニプロジェクト
> **学習目標**: ssh-agentの起動・鍵登録・管理の一連の操作をマスターし、パスフレーズ付き鍵を効率的に運用する方法を身につける

---

## 完成イメージ

```
# ssh-agent を起動して鍵を登録
$ eval "$(ssh-agent -s)"
Agent pid 12345

$ ssh-add ~/.ssh/id_ed25519_work
Enter passphrase for /home/user/.ssh/id_ed25519_work: ********
Identity added: /home/user/.ssh/id_ed25519_work (work-server-2024)

# 登録済み鍵の一覧
$ ssh-add -l
256 SHA256:xxxxx... work-server-2024 (ED25519)
256 SHA256:yyyyy... github-myname@example.com (ED25519)

# パスフレーズなしで接続（エージェントが代理応答）
$ ssh dev
deploy@dev-server:~$
```

---

## 課題の要件

1. ssh-agent を起動し、パスフレーズ付きの鍵を登録する
2. 複数の鍵を登録し、一覧を確認する
3. 鍵の有効期限（タイムアウト）を設定する
4. 不要な鍵をエージェントから削除する
5. シェル起動時に自動的にssh-agentが起動する設定を作成する

---

## ステップガイド

<details>
<summary>ステップ1：ssh-agent を起動する</summary>

```bash
# ssh-agent を起動（環境変数を現在のシェルに反映）
$ eval "$(ssh-agent -s)"
Agent pid 12345

# 環境変数が設定されたことを確認
$ echo $SSH_AUTH_SOCK
/tmp/ssh-XXXXXXXXXX/agent.12344

$ echo $SSH_AGENT_PID
12345
```

`eval` を使わないと環境変数が設定されず、ssh-addが動作しません。

</details>

<details>
<summary>ステップ2：鍵を登録する</summary>

```bash
# パスフレーズ付き鍵を登録
$ ssh-add ~/.ssh/id_ed25519_work
Enter passphrase for /home/user/.ssh/id_ed25519_work: ********
Identity added: ...

# 有効期限付きで登録（3600秒 = 1時間）
$ ssh-add -t 3600 ~/.ssh/id_ed25519_github

# 登録済み鍵の一覧
$ ssh-add -l
```

</details>

<details>
<summary>ステップ3：鍵を管理する</summary>

```bash
# 特定の鍵を削除
$ ssh-add -d ~/.ssh/id_ed25519_github

# 全ての鍵を削除
$ ssh-add -D

# 鍵のフィンガープリントをSHA256形式で表示
$ ssh-add -l -E sha256
```

</details>

<details>
<summary>ステップ4：自動起動設定を作成する</summary>

`.bashrc` や `.bash_profile` に以下の設定を追加します。

```bash
# ssh-agent の自動起動設定を .bashrc に追記
cat >> ~/.bashrc << 'EOF'

# --- SSH Agent 自動起動 ---
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)" > /dev/null
    ssh-add ~/.ssh/id_ed25519_work 2>/dev/null
fi
EOF
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）─ 基本操作を順番に実行</summary>

```bash
#!/bin/bash
# SSHエージェント練習スクリプト
# 学べる内容：ssh-agent、ssh-add、鍵の登録と管理
# 実行方法：source ssh_agent_practice.sh（evalのためsourceで実行）

echo "===== SSHエージェント練習 ====="

# --- ステップ1: ssh-agentの起動 ---
echo ""
echo "--- ステップ1: ssh-agent の起動 ---"

# 既に起動しているか確認
if [ -n "$SSH_AGENT_PID" ] && kill -0 "$SSH_AGENT_PID" 2>/dev/null; then
    echo "ssh-agent は既に起動しています (PID: $SSH_AGENT_PID)"
else
    eval "$(ssh-agent -s)"
    echo "ssh-agent を起動しました (PID: $SSH_AGENT_PID)"
fi

# --- ステップ2: 鍵の登録 ---
echo ""
echo "--- ステップ2: 鍵の登録 ---"

# 利用可能な鍵ファイルを表示
echo "利用可能な鍵ファイル:"
ls ~/.ssh/id_* 2>/dev/null | grep -v ".pub$" || echo "  鍵ファイルが見つかりません"

echo ""
echo "鍵を登録します（パスフレーズの入力が必要な場合があります）"

# 業務用の鍵を登録（1時間の有効期限付き）
if [ -f ~/.ssh/id_ed25519_work ]; then
    ssh-add -t 3600 ~/.ssh/id_ed25519_work
    echo "  id_ed25519_work を登録しました（有効期限: 1時間）"
fi

# GitHub用の鍵を登録
if [ -f ~/.ssh/id_ed25519_github ]; then
    ssh-add ~/.ssh/id_ed25519_github
    echo "  id_ed25519_github を登録しました"
fi

# --- ステップ3: 登録状況の確認 ---
echo ""
echo "--- ステップ3: 登録済み鍵の一覧 ---"
ssh-add -l 2>/dev/null || echo "  鍵が登録されていません"

# --- ステップ4: 接続テスト ---
echo ""
echo "--- ステップ4: 接続テスト ---"
echo "GitHubへの接続テスト:"
ssh -T git@github.com 2>&1 || true

echo ""
echo "===== 完了 ====="
echo ""
echo "便利なコマンド:"
echo "  ssh-add -l          登録済み鍵の一覧"
echo "  ssh-add -d 鍵パス   特定の鍵を削除"
echo "  ssh-add -D          全ての鍵を削除"
echo "  ssh-agent -k        エージェントを終了"
```

</details>

<details>
<summary>解答例（改良版）─ エージェント永続化とソケット再利用</summary>

```bash
#!/bin/bash
# SSHエージェント管理ツール（改良版）
# 学べる内容：エージェントの永続化、ソケット再利用、自動登録
# 実行方法：source ssh_agent_manager.sh [start|add|list|remove|stop]

SSH_AGENT_ENV="$HOME/.ssh/agent.env"

# === ユーティリティ関数 ===

agent_is_running() {
    if [ -n "$SSH_AGENT_PID" ] && kill -0 "$SSH_AGENT_PID" 2>/dev/null; then
        return 0
    fi
    return 1
}

start_agent() {
    echo "--- ssh-agent の起動 ---"

    # 既存のエージェント情報を読み込む
    if [ -f "$SSH_AGENT_ENV" ]; then
        source "$SSH_AGENT_ENV" > /dev/null
        if agent_is_running; then
            echo "既存のエージェントを再利用します (PID: $SSH_AGENT_PID)"
            return
        fi
    fi

    # 新規起動
    ssh-agent -s > "$SSH_AGENT_ENV"
    chmod 600 "$SSH_AGENT_ENV"
    source "$SSH_AGENT_ENV" > /dev/null
    echo "新しいエージェントを起動しました (PID: $SSH_AGENT_PID)"
}

add_keys() {
    local timeout="${1:-}"
    echo "--- 鍵の登録 ---"

    if ! agent_is_running; then
        echo "[エラー] ssh-agent が起動していません。先に start を実行してください。"
        return 1
    fi

    # 登録済みのフィンガープリントを取得
    local registered
    registered=$(ssh-add -l 2>/dev/null | awk '{print $2}' || true)

    local count=0
    for key_file in ~/.ssh/id_ed25519_* ~/.ssh/id_rsa_*; do
        # 公開鍵ファイルはスキップ
        [[ "$key_file" == *.pub ]] && continue
        [ ! -f "$key_file" ] && continue

        # フィンガープリントを確認
        local fp
        fp=$(ssh-keygen -l -f "$key_file" 2>/dev/null | awk '{print $2}')

        # 既に登録済みならスキップ
        if echo "$registered" | grep -q "$fp" 2>/dev/null; then
            echo "  [スキップ] $(basename "$key_file") (登録済み)"
            continue
        fi

        # タイムアウト付きで登録
        if [ -n "$timeout" ]; then
            echo "  登録中: $(basename "$key_file") (有効期限: ${timeout}秒)"
            ssh-add -t "$timeout" "$key_file"
        else
            echo "  登録中: $(basename "$key_file")"
            ssh-add "$key_file"
        fi
        count=$((count + 1))
    done

    echo "  ${count}個の鍵を新たに登録しました。"
}

list_keys() {
    echo "--- 登録済み鍵の一覧 ---"

    if ! agent_is_running; then
        echo "[エラー] ssh-agent が起動していません。"
        return 1
    fi

    local keys
    keys=$(ssh-add -l 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "$keys" | while IFS= read -r line; do
            local bits algo comment type
            bits=$(echo "$line" | awk '{print $1}')
            algo=$(echo "$line" | awk '{print $NF}')
            comment=$(echo "$line" | awk '{for(i=3;i<NF;i++) printf $i " "; print ""}')
            echo "  [$algo ${bits}bit] $comment"
        done
    else
        echo "  登録済みの鍵はありません。"
    fi

    echo ""
    echo "エージェント情報:"
    echo "  PID: ${SSH_AGENT_PID:-不明}"
    echo "  ソケット: ${SSH_AUTH_SOCK:-不明}"
}

remove_key() {
    local key_file="${1:-}"

    if [ -z "$key_file" ]; then
        echo "--- 全ての鍵を削除 ---"
        ssh-add -D
        echo "全ての鍵を削除しました。"
    else
        echo "--- 鍵の削除: $key_file ---"
        ssh-add -d "$key_file"
    fi
}

stop_agent() {
    echo "--- ssh-agent の停止 ---"

    if agent_is_running; then
        ssh-agent -k > /dev/null
        echo "エージェントを停止しました (PID: $SSH_AGENT_PID)"
    else
        echo "エージェントは起動していません。"
    fi

    rm -f "$SSH_AGENT_ENV"
    unset SSH_AGENT_PID SSH_AUTH_SOCK
}

setup_auto_start() {
    echo "--- 自動起動設定 ---"

    local rc_file="$HOME/.bashrc"
    local marker="# === SSH Agent Auto Start ==="

    if grep -q "$marker" "$rc_file" 2>/dev/null; then
        echo "自動起動設定は既に存在します。"
        return
    fi

    cat >> "$rc_file" << 'BASHRC'

# === SSH Agent Auto Start ===
_ssh_agent_env="$HOME/.ssh/agent.env"
if [ -f "$_ssh_agent_env" ]; then
    source "$_ssh_agent_env" > /dev/null
    if ! kill -0 "$SSH_AGENT_PID" 2>/dev/null; then
        ssh-agent -s > "$_ssh_agent_env"
        chmod 600 "$_ssh_agent_env"
        source "$_ssh_agent_env" > /dev/null
    fi
else
    ssh-agent -s > "$_ssh_agent_env"
    chmod 600 "$_ssh_agent_env"
    source "$_ssh_agent_env" > /dev/null
fi
unset _ssh_agent_env
# === End SSH Agent Auto Start ===
BASHRC

    echo "自動起動設定を $rc_file に追加しました。"
    echo "次回のシェル起動時から有効になります。"
}

# === メイン処理 ===

ACTION="${1:-help}"

case "$ACTION" in
    start)
        start_agent
        ;;
    add)
        add_keys "${2:-}"
        ;;
    list)
        list_keys
        ;;
    remove)
        remove_key "${2:-}"
        ;;
    stop)
        stop_agent
        ;;
    setup)
        setup_auto_start
        ;;
    help|*)
        echo "===== SSHエージェント管理ツール ====="
        echo ""
        echo "使い方: source $0 [コマンド]"
        echo ""
        echo "コマンド:"
        echo "  start          エージェントを起動（既存があれば再利用）"
        echo "  add [秒数]     鍵を登録（秒数指定で有効期限付き）"
        echo "  list           登録済み鍵の一覧"
        echo "  remove [鍵]    鍵を削除（引数なしで全削除）"
        echo "  stop           エージェントを停止"
        echo "  setup          シェルの自動起動設定を追加"
        echo ""
        echo "例:"
        echo "  source $0 start"
        echo "  source $0 add 3600    # 1時間の有効期限付き"
        echo "  source $0 list"
        ;;
esac
```

**初心者向けとの違い:**
- エージェントのソケット情報をファイルに保存 → 別のターミナルからも再利用可能
- 登録済みの鍵をスキップ → 二重登録を防止
- サブコマンド方式で操作を整理 → 実務で使いやすいツール
- `.bashrc` への自動起動設定の追加機能 → 毎回手動起動する手間を省略
- `source` で実行することで環境変数が現在のシェルに反映される

</details>
