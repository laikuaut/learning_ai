"""
HTTP/HTTPSサンプル01：HTTPリクエスト入門
========================================

学べる内容:
  - urllib を使った GET / POST リクエスト
  - レスポンスヘッダーの読み取り
  - JSON レスポンスの解析
  - エラーハンドリング

実行方法:
  python 01_HTTPリクエスト入門.py
"""

from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import json


def get_request(url):
    """GETリクエストを送信して結果を表示"""
    print(f"\n{'='*50}")
    print(f"GET {url}")
    print(f"{'='*50}")

    try:
        with urlopen(url) as response:
            print(f"ステータス: {response.status} {response.reason}")
            print(f"Content-Type: {response.getheader('Content-Type')}")
            print(f"Content-Length: {response.getheader('Content-Length')}")

            body = response.read().decode("utf-8")
            try:
                data = json.loads(body)
                print(f"レスポンス (JSON):")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
            except json.JSONDecodeError:
                print(f"レスポンス (テキスト):")
                print(body[:300])

    except HTTPError as e:
        print(f"HTTPエラー: {e.code} {e.reason}")
    except URLError as e:
        print(f"接続エラー: {e.reason}")


def post_request(url, data):
    """POSTリクエストを送信して結果を表示"""
    print(f"\n{'='*50}")
    print(f"POST {url}")
    print(f"データ: {data}")
    print(f"{'='*50}")

    json_data = json.dumps(data).encode("utf-8")
    req = Request(url, data=json_data, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urlopen(req) as response:
            print(f"ステータス: {response.status} {response.reason}")
            body = json.loads(response.read())
            print(f"送信されたデータ: {body.get('json', {})}")

    except HTTPError as e:
        print(f"HTTPエラー: {e.code} {e.reason}")


def show_headers(url):
    """レスポンスヘッダーを全件表示"""
    print(f"\n{'='*50}")
    print(f"レスポンスヘッダー一覧: {url}")
    print(f"{'='*50}")

    with urlopen(url) as response:
        for header, value in response.getheaders():
            print(f"  {header}: {value}")


def main():
    print("HTTP/HTTPS リクエスト入門")
    print("=" * 50)

    BASE = "https://httpbin.org"

    while True:
        print("\nメニュー:")
        print("  1. GET リクエスト")
        print("  2. POST リクエスト（JSON）")
        print("  3. レスポンスヘッダー一覧")
        print("  4. エラーレスポンス（404）")
        print("  5. デモ（全機能実行）")
        print("  q. 終了")

        choice = input("\n選択> ").strip()

        if choice == "q":
            break
        elif choice == "1":
            get_request(f"{BASE}/get")
        elif choice == "2":
            post_request(f"{BASE}/post", {"name": "田中太郎", "age": 30})
        elif choice == "3":
            show_headers(f"{BASE}/get")
        elif choice == "4":
            get_request(f"{BASE}/status/404")
        elif choice == "5":
            get_request(f"{BASE}/get")
            post_request(f"{BASE}/post", {"message": "Hello, HTTP!"})
            show_headers(f"{BASE}/response-headers?X-Custom=test")
            get_request(f"{BASE}/status/404")

    print("\nお疲れさまでした！")


if __name__ == "__main__":
    main()
