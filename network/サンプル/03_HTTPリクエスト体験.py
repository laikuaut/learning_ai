# ==============================
# HTTPリクエスト体験ツール
# ネットワーク基礎：HTTPプロトコルの仕組みを体験するサンプル
# ==============================
# 学べる内容:
#   - HTTPリクエスト/レスポンスの基本構造
#   - GET / POST メソッドの違い
#   - HTTPヘッダの確認と意味
#   - ステータスコードの種類と意味
#   - urllib を使ったHTTP通信の実装
#   - JSON レスポンスの解析
#
# 実行方法:
#   python 03_HTTPリクエスト体験.py
#
# ※ 本プログラムは教育目的で作成されています
# ※ インターネット接続が必要です
# ==============================

import urllib.request
import urllib.parse
import urllib.error
import json
import ssl


def explain_http():
    """HTTPプロトコルの基本をアスキーアートで解説します"""
    print("""
  ┌──────────────────────────────────────────────────┐
  │              HTTPプロトコルの基本                 │
  └──────────────────────────────────────────────────┘

  HTTP（HyperText Transfer Protocol）は、
  Webブラウザとサーバー間の通信プロトコルです。

  【リクエスト/レスポンスの流れ】

    クライアント                    サーバー
    ┌─────────┐                   ┌─────────┐
    │ブラウザ  │──(1)リクエスト──→│  Web    │
    │         │  GET /index.html │ サーバー │
    │         │                   │         │
    │         │←(2)レスポンス─── │         │
    │         │  200 OK + HTML   │         │
    └─────────┘                   └─────────┘

  【主なHTTPメソッド】
  ┌────────┬──────────────────────────────────────┐
  │ GET    │ リソースの取得（ページ閲覧など）      │
  │ POST   │ データの送信（フォーム送信など）      │
  │ PUT    │ リソースの更新（全体の置き換え）      │
  │ PATCH  │ リソースの部分更新                    │
  │ DELETE │ リソースの削除                        │
  │ HEAD   │ ヘッダのみ取得（本文なし）            │
  └────────┴──────────────────────────────────────┘

  【主なステータスコード】
  ┌──────┬──────────────────────────────────────────┐
  │ 1xx  │ 情報レスポンス（処理中）                 │
  │ 2xx  │ 成功（200 OK, 201 Created）              │
  │ 3xx  │ リダイレクト（301 永久, 302 一時）       │
  │ 4xx  │ クライアントエラー（404 Not Found）      │
  │ 5xx  │ サーバーエラー（500 Internal Error）     │
  └──────┴──────────────────────────────────────────┘
    """)


# ステータスコードの解説辞書
STATUS_CODES = {
    200: ("OK", "リクエスト成功"),
    201: ("Created", "リソースが正常に作成されました"),
    204: ("No Content", "成功したが返すデータなし"),
    301: ("Moved Permanently", "恒久的なリダイレクト"),
    302: ("Found", "一時的なリダイレクト"),
    304: ("Not Modified", "キャッシュ利用可能"),
    400: ("Bad Request", "リクエストが不正です"),
    401: ("Unauthorized", "認証が必要です"),
    403: ("Forbidden", "アクセス権がありません"),
    404: ("Not Found", "リソースが見つかりません"),
    405: ("Method Not Allowed", "許可されていないメソッドです"),
    429: ("Too Many Requests", "リクエスト回数制限超過"),
    500: ("Internal Server Error", "サーバー内部エラー"),
    502: ("Bad Gateway", "ゲートウェイエラー"),
    503: ("Service Unavailable", "サービス利用不可"),
}


def get_ssl_context():
    """SSL コンテキストを作成します"""
    ctx = ssl.create_default_context()
    return ctx


def send_get_request(url):
    """GETリクエストを送信し、結果を表示します"""
    print(f"\n  ─── GET リクエスト ───")
    print(f"  URL: {url}")
    print(f"  送信中...")

    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", "PythonLearning/1.0 (Educational Purpose)")
        req.add_header("Accept", "application/json, text/html, */*")

        # リクエストヘッダの表示
        print(f"\n  【送信したリクエストヘッダ】")
        print(f"  GET {urllib.parse.urlparse(url).path or '/'} HTTP/1.1")
        print(f"  Host: {urllib.parse.urlparse(url).hostname}")
        for key, value in req.headers.items():
            print(f"  {key}: {value}")

        ctx = get_ssl_context()
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            status = response.status
            headers = response.headers
            body = response.read().decode("utf-8", errors="replace")

            # レスポンスの表示
            print(f"\n  【レスポンス】")

            # ステータスコード
            status_info = STATUS_CODES.get(status, ("Unknown", "不明"))
            print(f"  ステータス: {status} {status_info[0]}")
            print(f"  意味: {status_info[1]}")

            # レスポンスヘッダ
            print(f"\n  【レスポンスヘッダ（主要なもの）】")
            important_headers = [
                "Content-Type", "Content-Length", "Server",
                "Date", "Cache-Control", "X-Request-Id",
            ]
            for h in important_headers:
                value = headers.get(h)
                if value:
                    print(f"  {h}: {value}")

            # ボディ（先頭500文字まで）
            print(f"\n  【レスポンスボディ（先頭500文字）】")
            # JSONの場合は整形して表示
            content_type = headers.get("Content-Type", "")
            if "json" in content_type:
                try:
                    json_data = json.loads(body)
                    formatted = json.dumps(json_data, indent=2, ensure_ascii=False)
                    print(f"  {formatted[:500]}")
                except json.JSONDecodeError:
                    print(f"  {body[:500]}")
            else:
                print(f"  {body[:500]}")

            if len(body) > 500:
                print(f"\n  ... (以下省略、全体: {len(body)} 文字)")

    except urllib.error.HTTPError as e:
        status_info = STATUS_CODES.get(e.code, ("Unknown", "不明"))
        print(f"\n  【HTTPエラー】")
        print(f"  ステータス: {e.code} {status_info[0]}")
        print(f"  意味: {status_info[1]}")
    except urllib.error.URLError as e:
        print(f"\n  ※ 接続エラー: {e.reason}")
    except Exception as e:
        print(f"\n  ※ エラーが発生しました: {e}")


def send_post_request(url, data):
    """POSTリクエストを送信し、結果を表示します"""
    print(f"\n  ─── POST リクエスト ───")
    print(f"  URL: {url}")

    try:
        # データをJSONとしてエンコード
        json_data = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=json_data, method="POST")
        req.add_header("User-Agent", "PythonLearning/1.0 (Educational Purpose)")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")

        # リクエスト内容の表示
        print(f"\n  【送信するデータ】")
        formatted = json.dumps(data, indent=2, ensure_ascii=False)
        print(f"  {formatted}")

        print(f"\n  【送信したリクエストヘッダ】")
        print(f"  POST {urllib.parse.urlparse(url).path or '/'} HTTP/1.1")
        print(f"  Host: {urllib.parse.urlparse(url).hostname}")
        for key, value in req.headers.items():
            print(f"  {key}: {value}")

        print(f"\n  送信中...")
        ctx = get_ssl_context()
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            status = response.status
            body = response.read().decode("utf-8", errors="replace")

            status_info = STATUS_CODES.get(status, ("Unknown", "不明"))
            print(f"\n  【レスポンス】")
            print(f"  ステータス: {status} {status_info[0]}")

            try:
                json_response = json.loads(body)
                formatted = json.dumps(json_response, indent=2, ensure_ascii=False)
                print(f"\n  【レスポンスボディ】")
                print(f"  {formatted[:500]}")
            except json.JSONDecodeError:
                print(f"\n  【レスポンスボディ】")
                print(f"  {body[:500]}")

    except urllib.error.HTTPError as e:
        status_info = STATUS_CODES.get(e.code, ("Unknown", "不明"))
        print(f"\n  【HTTPエラー】")
        print(f"  ステータス: {e.code} {status_info[0]}")
    except urllib.error.URLError as e:
        print(f"\n  ※ 接続エラー: {e.reason}")
    except Exception as e:
        print(f"\n  ※ エラーが発生しました: {e}")


def explain_status_codes():
    """ステータスコードの一覧を表示します"""
    print("\n" + "=" * 60)
    print("  HTTPステータスコード一覧")
    print("=" * 60)

    categories = {
        "1xx 情報レスポンス": [],
        "2xx 成功": [],
        "3xx リダイレクト": [],
        "4xx クライアントエラー": [],
        "5xx サーバーエラー": [],
    }

    for code, (name, desc) in sorted(STATUS_CODES.items()):
        category = f"{code // 100}xx"
        for cat_name in categories:
            if cat_name.startswith(category):
                categories[cat_name].append((code, name, desc))
                break

    for category, codes in categories.items():
        if codes:
            print(f"\n  【{category}】")
            for code, name, desc in codes:
                print(f"    {code} {name:<25} {desc}")


def demo_mode():
    """デモモード: 代表的なHTTPリクエストを実行します"""
    print("\n" + "=" * 55)
    print("  【デモモード】HTTPリクエストの実例")
    print("=" * 55)

    # GETリクエストの例（公開APIを使用）
    print("\n  ◆ GETリクエスト例: JSONPlaceholder（テスト用API）")
    send_get_request("https://jsonplaceholder.typicode.com/posts/1")

    # POSTリクエストの例
    print("\n\n  ◆ POSTリクエスト例: データ送信テスト")
    post_data = {
        "title": "テスト投稿",
        "body": "これはHTTPリクエストの学習用テストです",
        "userId": 1,
    }
    send_post_request("https://jsonplaceholder.typicode.com/posts", post_data)

    # ステータスコード一覧
    explain_status_codes()


def interactive_mode():
    """対話モード: ユーザーがURLを指定してリクエストを送信します"""
    print("\n" + "=" * 55)
    print("  【対話モード】HTTPリクエスト体験")
    print("=" * 55)

    while True:
        print("\n  操作を選んでください:")
        print("  1. GETリクエストを送信")
        print("  2. POSTリクエストを送信（テストAPI宛）")
        print("  3. ステータスコード一覧を表示")
        print("  4. メニューに戻る")

        choice = input("\n  選択 (1-4): ").strip()

        if choice == "1":
            url = input("  URLを入力 (例: https://jsonplaceholder.typicode.com/posts/1): ").strip()
            if url:
                if not url.startswith("http"):
                    url = "https://" + url
                send_get_request(url)
            else:
                print("  ※ URLを入力してください。")

        elif choice == "2":
            print("  テスト用APIにPOSTリクエストを送信します。")
            title = input("  タイトルを入力: ").strip() or "テスト"
            body_text = input("  本文を入力: ").strip() or "テスト投稿です"

            post_data = {
                "title": title,
                "body": body_text,
                "userId": 1,
            }
            send_post_request("https://jsonplaceholder.typicode.com/posts", post_data)

        elif choice == "3":
            explain_status_codes()

        elif choice == "4":
            break
        else:
            print("  ※ 1〜4 の数字を入力してください。")


# --- メインプログラム ---
if __name__ == "__main__":
    print("+" + "=" * 53 + "+")
    print("|        HTTPリクエスト体験ツール                   |")
    print("|        〜 Webの裏側を覗いてみよう 〜              |")
    print("+" + "=" * 53 + "+")

    # HTTPの解説を表示
    explain_http()

    while True:
        print("\n  モードを選択してください:")
        print("  1. デモモード（代表的なリクエストを実行）")
        print("  2. 対話モード（自分で入力）")
        print("  3. 終了")

        mode = input("\n  選択 (1-3): ").strip()

        if mode == "1":
            demo_mode()
        elif mode == "2":
            interactive_mode()
        elif mode == "3":
            print("\n  ご利用ありがとうございました！")
            break
        else:
            print("  ※ 1〜3 の数字を入力してください。")
