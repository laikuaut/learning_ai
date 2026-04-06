# 実践課題05：TCPチャットアプリ ★2

> **難易度**: ★★☆☆☆（基礎）
> **前提知識**: 第2章（OSI参照モデルとTCP/IP）、第4章（TCP/UDP）
> **課題の種類**: ミニプロジェクト
> **学習目標**: TCPソケット通信の基本（サーバ・クライアント構成、コネクション確立・切断）を理解し、実際に動くチャットアプリを作る

---

## 完成イメージ

**サーバ側:**
```
===== TCPチャットサーバ =====
サーバ起動: 0.0.0.0:50000
クライアントの接続を待っています...

[接続] クライアント 127.0.0.1:52341 が接続しました。

[受信] クライアント: こんにちは！
[送信] サーバ: こんにちは！チャットサーバへようこそ。
[受信] クライアント: 今日の天気は？
[送信] サーバ: いい天気ですよ！

[切断] クライアント 127.0.0.1:52341 が切断しました。
```

**クライアント側:**
```
===== TCPチャットクライアント =====
サーバに接続しています... 127.0.0.1:50000
接続成功！（'quit'で終了）

あなた> こんにちは！
サーバ> こんにちは！チャットサーバへようこそ。
あなた> 今日の天気は？
サーバ> いい天気ですよ！
あなた> quit

切断しました。
```

---

## 課題の要件

1. サーバプログラムとクライアントプログラムを別々に作成する
2. サーバはクライアントからの接続を `accept()` で待ち受ける
3. クライアントとサーバで交互にメッセージを送受信する
4. クライアントが `quit` を送ると切断する
5. UTF-8エンコーディングで日本語に対応する

---

## ステップガイド

<details>
<summary>ステップ1：サーバのソケット作成とバインド</summary>

サーバはソケットを作成し、IPアドレスとポート番号にバインド（bind）して待ち受けます。

```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", 50000))
server_socket.listen(1)
print("クライアントの接続を待っています...")
```

- `AF_INET`: IPv4を使用
- `SOCK_STREAM`: TCP（ストリーム型）を使用
- `SO_REUSEADDR`: アドレスの再利用を許可（サーバ再起動時に便利）
- `listen(1)`: 最大1クライアントの待ちキュー

</details>

<details>
<summary>ステップ2：クライアントの接続</summary>

クライアントは `connect()` でサーバに接続します。

```python
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 50000))
```

</details>

<details>
<summary>ステップ3：データの送受信</summary>

`send()` と `recv()` でデータを送受信します。文字列はバイト列に変換する必要があります。

```python
# 送信
message = "こんにちは"
client_socket.send(message.encode("utf-8"))

# 受信
data = client_socket.recv(4096)
received_message = data.decode("utf-8")
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）── サーバ</summary>

```python
# TCPチャットサーバ
# 学べる内容：TCPソケット通信、サーバプログラミング
# 実行方法：python chat_server.py
# ※ 先にサーバを起動してからクライアントを起動してください

import socket

# --- サーバ設定 ---
HOST = "0.0.0.0"  # すべてのインターフェースで待ち受け
PORT = 50000

# --- ソケット作成 ---
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("===== TCPチャットサーバ =====")
print(f"サーバ起動: {HOST}:{PORT}")
print("クライアントの接続を待っています...")
print()

# --- クライアント接続の受け入れ ---
client_socket, client_address = server_socket.accept()
print(f"[接続] クライアント {client_address[0]}:{client_address[1]} が接続しました。")
print()

# --- チャットループ ---
try:
    while True:
        # クライアントからのメッセージ受信
        data = client_socket.recv(4096)
        if not data:
            break

        message = data.decode("utf-8")
        if message.lower() == "quit":
            break

        print(f"[受信] クライアント: {message}")

        # サーバからの返信
        reply = input("[送信] サーバ: ")
        client_socket.send(reply.encode("utf-8"))

except ConnectionResetError:
    print("[エラー] クライアントとの接続が切断されました。")

finally:
    print(f"\n[切断] クライアント {client_address[0]}:{client_address[1]} が切断しました。")
    client_socket.close()
    server_socket.close()
    print("サーバを終了しました。")
```

</details>

<details>
<summary>解答例（初心者向け）── クライアント</summary>

```python
# TCPチャットクライアント
# 学べる内容：TCPソケット通信、クライアントプログラミング
# 実行方法：python chat_client.py
# ※ 先にサーバを起動してからクライアントを起動してください

import socket

# --- 接続先設定 ---
HOST = "127.0.0.1"  # ローカルホスト
PORT = 50000

# --- ソケット作成と接続 ---
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("===== TCPチャットクライアント =====")
print(f"サーバに接続しています... {HOST}:{PORT}")

try:
    client_socket.connect((HOST, PORT))
except ConnectionRefusedError:
    print("エラー: サーバに接続できません。サーバが起動しているか確認してください。")
    exit()

print("接続成功！（'quit'で終了）")
print()

# --- チャットループ ---
try:
    while True:
        # メッセージ入力と送信
        message = input("あなた> ")
        client_socket.send(message.encode("utf-8"))

        if message.lower() == "quit":
            break

        # サーバからの返信受信
        data = client_socket.recv(4096)
        if not data:
            print("サーバとの接続が切断されました。")
            break

        reply = data.decode("utf-8")
        print(f"サーバ> {reply}")

except ConnectionResetError:
    print("サーバとの接続が切断されました。")

finally:
    client_socket.close()
    print("\n切断しました。")
```

</details>

<details>
<summary>解答例（改良版 ─ タイムスタンプとログ記録）</summary>

タイムスタンプの表示とチャットログのファイル保存に対応したサーバです。

```python
# TCPチャットサーバ（改良版）
# 学べる内容：TCPソケット、タイムスタンプ、ファイルログ
# 実行方法：python chat_server_v2.py

import socket
from datetime import datetime


def get_timestamp():
    """現在時刻のタイムスタンプを返す"""
    return datetime.now().strftime("%H:%M:%S")


def log_message(log_file, sender, message):
    """メッセージをログファイルに記録する"""
    timestamp = get_timestamp()
    entry = f"[{timestamp}] {sender}: {message}\n"
    log_file.write(entry)
    log_file.flush()


def run_server(host="0.0.0.0", port=50000):
    """チャットサーバを起動する"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("===== TCPチャットサーバ（改良版） =====")
    print(f"サーバ起動: {host}:{port}")
    print("クライアントの接続を待っています...")

    client_socket, client_address = server_socket.accept()
    client_info = f"{client_address[0]}:{client_address[1]}"
    print(f"\n[{get_timestamp()}] [接続] {client_info}")

    # ログファイルを開く
    log_filename = f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    try:
        with open(log_filename, "w", encoding="utf-8") as log_file:
            log_file.write(f"チャットログ - 開始: {datetime.now()}\n")
            log_file.write(f"クライアント: {client_info}\n")
            log_file.write("-" * 40 + "\n")

            # ウェルカムメッセージを送信
            welcome = "チャットサーバへようこそ！"
            client_socket.send(welcome.encode("utf-8"))
            log_message(log_file, "サーバ（自動）", welcome)

            while True:
                data = client_socket.recv(4096)
                if not data:
                    break

                message = data.decode("utf-8")
                if message.lower() == "quit":
                    break

                print(f"[{get_timestamp()}] [受信] クライアント: {message}")
                log_message(log_file, "クライアント", message)

                reply = input(f"[{get_timestamp()}] [送信] サーバ: ")
                client_socket.send(reply.encode("utf-8"))
                log_message(log_file, "サーバ", reply)

            log_file.write("-" * 40 + "\n")
            log_file.write(f"チャットログ - 終了: {datetime.now()}\n")

        print(f"\nチャットログを保存しました: {log_filename}")

    except ConnectionResetError:
        print(f"\n[{get_timestamp()}] クライアントとの接続が切断されました。")

    finally:
        print(f"[{get_timestamp()}] [切断] {client_info}")
        client_socket.close()
        server_socket.close()


if __name__ == "__main__":
    run_server()
```

対応するクライアント（改良版）:

```python
# TCPチャットクライアント（改良版）
# 実行方法：python chat_client_v2.py

import socket
from datetime import datetime


def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")


def run_client(host="127.0.0.1", port=50000):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("===== TCPチャットクライアント（改良版） =====")
    print(f"接続先: {host}:{port}")

    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print("エラー: サーバに接続できません。")
        return

    print(f"[{get_timestamp()}] 接続成功！（'quit'で終了）\n")

    try:
        # ウェルカムメッセージの受信
        welcome = client_socket.recv(4096).decode("utf-8")
        print(f"[{get_timestamp()}] サーバ> {welcome}\n")

        while True:
            message = input(f"[{get_timestamp()}] あなた> ")
            client_socket.send(message.encode("utf-8"))

            if message.lower() == "quit":
                break

            data = client_socket.recv(4096)
            if not data:
                print("サーバとの接続が切断されました。")
                break

            print(f"[{get_timestamp()}] サーバ> {data.decode('utf-8')}\n")

    except ConnectionResetError:
        print("サーバとの接続が切断されました。")
    finally:
        client_socket.close()
        print(f"\n[{get_timestamp()}] 切断しました。")


if __name__ == "__main__":
    run_client()
```

**初心者向けとの違い:**
- タイムスタンプの表示で時系列が明確
- チャットログをファイルに自動保存
- ウェルカムメッセージの自動送信
- 関数に分割してメインロジックを `run_server()` / `run_client()` に集約

</details>
