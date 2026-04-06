# 実践課題02：SSH鍵ペアの生成と管理 ★1

> **難易度**: ★☆☆☆☆（入門）
> **前提知識**: 第3章（公開鍵認証の設定）
> **課題の種類**: ミニプロジェクト
> **学習目標**: SSH鍵ペアの生成・確認・管理の基本操作を身につけ、用途ごとに鍵を使い分けられるようになる

---

## 完成イメージ

```
$ ls -la ~/.ssh/
-rw-------  1 user user  464 Apr  6 10:00 id_ed25519_github
-rw-r--r--  1 user user  104 Apr  6 10:00 id_ed25519_github.pub
-rw-------  1 user user  464 Apr  6 10:01 id_ed25519_work
-rw-r--r--  1 user user  104 Apr  6 10:01 id_ed25519_work.pub
-rw-------  1 user user  464 Apr  6 10:02 id_ed25519_personal
-rw-r--r--  1 user user  104 Apr  6 10:02 id_ed25519_personal.pub
-rw-r--r--  1 user user  444 Apr  6 10:00 known_hosts

$ ssh-keygen -l -f ~/.ssh/id_ed25519_github.pub
256 SHA256:xxxxx... user@hostname (ED25519)
```

---

## 課題の要件

1. Ed25519 アルゴリズムで3つの鍵ペアを生成する
   - GitHub用（`id_ed25519_github`）
   - 業務サーバー用（`id_ed25519_work`）
   - 個人サーバー用（`id_ed25519_personal`）
2. 各鍵にわかりやすいコメントを付ける
3. 業務サーバー用にはパスフレーズ（passphrase）を設定する
4. 生成した鍵のフィンガープリント（fingerprint）を確認する
5. `~/.ssh/` ディレクトリのパーミッション（permission）が正しいことを確認する

---

## ステップガイド

<details>
<summary>ステップ1：~/.ssh ディレクトリを準備する</summary>

まず `~/.ssh` ディレクトリが存在し、パーミッションが正しいことを確認します。

```bash
# ディレクトリがなければ作成
$ mkdir -p ~/.ssh

# パーミッションを700に設定（所有者のみアクセス可能）
$ chmod 700 ~/.ssh

# 確認
$ ls -ld ~/.ssh
drwx------  2 user user 4096 Apr  6 10:00 /home/user/.ssh
```

</details>

<details>
<summary>ステップ2：鍵ペアを生成する</summary>

`ssh-keygen` コマンドで Ed25519 鍵を生成します。

```bash
# GitHub用（パスフレーズなし ─ 練習用）
$ ssh-keygen -t ed25519 -C "github-myname@example.com" -f ~/.ssh/id_ed25519_github

# 業務サーバー用（パスフレーズあり ─ セキュリティ強化）
$ ssh-keygen -t ed25519 -C "work-server-2024" -f ~/.ssh/id_ed25519_work
# パスフレーズの入力を求められるので、安全な文字列を入力

# 個人サーバー用
$ ssh-keygen -t ed25519 -C "personal-server" -f ~/.ssh/id_ed25519_personal
```

オプションの意味：
- `-t ed25519` : アルゴリズムの種類（Ed25519が最も推奨）
- `-C "コメント"` : 鍵にコメントを付ける（識別用）
- `-f パス` : 保存先ファイルを指定

</details>

<details>
<summary>ステップ3：鍵を確認する</summary>

生成した鍵のフィンガープリントと内容を確認します。

```bash
# フィンガープリントの確認
$ ssh-keygen -l -f ~/.ssh/id_ed25519_github.pub

# 公開鍵の中身を表示（この内容をサーバーに登録する）
$ cat ~/.ssh/id_ed25519_github.pub
```

</details>

<details>
<summary>ステップ4：パーミッションを確認する</summary>

SSH鍵のパーミッションが正しくないと接続エラーになります。

```bash
# 正しいパーミッション
# 秘密鍵: 600（所有者のみ読み書き）
# 公開鍵: 644（所有者は読み書き、他者は読み取りのみ）
$ chmod 600 ~/.ssh/id_ed25519_*
$ chmod 644 ~/.ssh/id_ed25519_*.pub
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）─ 1つずつ実行</summary>

```bash
#!/bin/bash
# SSH鍵ペアの生成と管理
# 学べる内容：ssh-keygen、パーミッション、フィンガープリント
# 実行方法：bash ssh_key_setup.sh

echo "===== SSH鍵ペア生成ツール ====="

# --- ディレクトリ準備 ---
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# --- GitHub用の鍵を生成（パスフレーズなし） ---
echo ""
echo "--- GitHub用の鍵を生成 ---"
ssh-keygen -t ed25519 -C "github-myname@example.com" -f ~/.ssh/id_ed25519_github -N ""
echo "生成完了"

# --- 業務サーバー用の鍵を生成（パスフレーズあり） ---
echo ""
echo "--- 業務サーバー用の鍵を生成 ---"
echo "パスフレーズの入力を求められます。安全な文字列を入力してください。"
ssh-keygen -t ed25519 -C "work-server-2024" -f ~/.ssh/id_ed25519_work

# --- 個人サーバー用の鍵を生成（パスフレーズなし） ---
echo ""
echo "--- 個人サーバー用の鍵を生成 ---"
ssh-keygen -t ed25519 -C "personal-server" -f ~/.ssh/id_ed25519_personal -N ""
echo "生成完了"

# --- パーミッション設定 ---
echo ""
echo "--- パーミッション設定 ---"
chmod 600 ~/.ssh/id_ed25519_github ~/.ssh/id_ed25519_work ~/.ssh/id_ed25519_personal
chmod 644 ~/.ssh/id_ed25519_github.pub ~/.ssh/id_ed25519_work.pub ~/.ssh/id_ed25519_personal.pub

# --- 確認 ---
echo ""
echo "--- 生成された鍵ファイル ---"
ls -la ~/.ssh/id_ed25519_*

echo ""
echo "--- フィンガープリント一覧 ---"
echo "[GitHub用]"
ssh-keygen -l -f ~/.ssh/id_ed25519_github.pub
echo "[業務サーバー用]"
ssh-keygen -l -f ~/.ssh/id_ed25519_work.pub
echo "[個人サーバー用]"
ssh-keygen -l -f ~/.ssh/id_ed25519_personal.pub

echo ""
echo "===== 完了 ====="
```

</details>

<details>
<summary>解答例（改良版）─ 既存鍵の重複チェック付き</summary>

```bash
#!/bin/bash
# SSH鍵ペア管理ツール（改良版）
# 学べる内容：条件分岐による安全な鍵管理、一括操作
# 実行方法：bash ssh_key_manager.sh

set -euo pipefail

SSH_DIR="$HOME/.ssh"

# === ユーティリティ関数 ===

generate_key() {
    local name="$1"
    local comment="$2"
    local passphrase="${3:-}"  # 省略時は空（パスフレーズなし）
    local key_path="$SSH_DIR/$name"

    if [ -f "$key_path" ]; then
        echo "[スキップ] $name は既に存在します。上書きしません。"
        echo "  フィンガープリント: $(ssh-keygen -l -f "${key_path}.pub")"
        return
    fi

    if [ -n "$passphrase" ]; then
        ssh-keygen -t ed25519 -C "$comment" -f "$key_path" -N "$passphrase"
    else
        ssh-keygen -t ed25519 -C "$comment" -f "$key_path" -N ""
    fi

    chmod 600 "$key_path"
    chmod 644 "${key_path}.pub"
    echo "[成功] $name を生成しました。"
}

show_key_info() {
    local name="$1"
    local key_path="$SSH_DIR/$name"

    if [ ! -f "${key_path}.pub" ]; then
        echo "  $name: 見つかりません"
        return
    fi

    local fingerprint
    fingerprint=$(ssh-keygen -l -f "${key_path}.pub")
    local permissions
    permissions=$(stat -c '%a' "$key_path" 2>/dev/null || stat -f '%Lp' "$key_path" 2>/dev/null)

    echo "  $name"
    echo "    フィンガープリント: $fingerprint"
    echo "    秘密鍵パーミッション: $permissions"
}

# === メイン処理 ===

echo "===== SSH鍵ペア管理ツール ====="

# ディレクトリ準備
mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

echo ""
echo "--- 鍵ペアの生成 ---"

# 鍵の定義：名前、コメント、パスフレーズ（空文字=なし）
generate_key "id_ed25519_github"   "github-myname@example.com" ""
generate_key "id_ed25519_work"     "work-server-$(date +%Y)"   "my-secure-passphrase"
generate_key "id_ed25519_personal" "personal-server"            ""

echo ""
echo "--- 鍵ファイル一覧 ---"
ls -la "$SSH_DIR"/id_ed25519_* 2>/dev/null || echo "  鍵ファイルがありません。"

echo ""
echo "--- 鍵の詳細情報 ---"
show_key_info "id_ed25519_github"
show_key_info "id_ed25519_work"
show_key_info "id_ed25519_personal"

echo ""
echo "--- 公開鍵（GitHub に登録する内容） ---"
if [ -f "$SSH_DIR/id_ed25519_github.pub" ]; then
    cat "$SSH_DIR/id_ed25519_github.pub"
fi

echo ""
echo "===== 完了 ====="
```

**初心者向けとの違い:**
- 既存の鍵を上書きしない安全チェック付き → 誤って鍵を消す事故を防止
- 関数に分離して再利用性を高めている → 鍵の追加が1行で済む
- `set -euo pipefail` でエラー時に即停止 → 途中の問題を見逃さない
- 鍵の詳細情報（フィンガープリント、パーミッション）を見やすく表示

</details>
