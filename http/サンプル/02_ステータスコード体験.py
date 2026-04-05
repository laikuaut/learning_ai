"""
HTTP/HTTPSサンプル02：ステータスコード体験ツール
================================================

学べる内容:
  - 主要なHTTPステータスコード（2xx, 3xx, 4xx, 5xx）の動作
  - リダイレクトの追跡
  - エラーレスポンスのハンドリング

実行方法:
  python 02_ステータスコード体験.py
"""

from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json

BASE = "https://httpbin.org"

STATUS_INFO = {
    200: ("OK", "リクエスト成功"),
    201: ("Created", "リソース作成成功"),
    204: ("No Content", "成功（ボディなし）"),
    301: ("Moved Permanently", "恒久的リダイレクト"),
    302: ("Found", "一時的リダイレクト"),
    304: ("Not Modified", "キャッシュ有効（変更なし）"),
    400: ("Bad Request", "リクエスト形式が不正"),
    401: ("Unauthorized", "認証が必要"),
    403: ("Forbidden", "アクセス権限なし"),
    404: ("Not Found", "リソースが存在しない"),
    405: ("Method Not Allowed", "メソッド不許可"),
    409: ("Conflict", "リソースの状態と矛盾"),
    429: ("Too Many Requests", "レートリミット超過"),
    500: ("Internal Server Error", "サーバー内部エラー"),
    502: ("Bad Gateway", "上流サーバーから不正応答"),
    503: ("Service Unavailable", "サービス一時停止"),
}


def try_status(code):
    """指定したステータスコードのレスポンスを体験"""
    url = f"{BASE}/status/{code}"
    info = STATUS_INFO.get(code, ("Unknown", "不明"))

    print(f"\n--- {code} {info[0]} ---")
    print(f"説明: {info[1]}")
    print(f"URL: {url}")

    req = Request(url)
    # リダイレクトを自動追跡しない設定
    if code in (301, 302):
        print("※ リダイレクトレスポンスの確認")

    try:
        with urlopen(req) as response:
            print(f"結果: {response.status} {response.reason}")
            location = response.getheader("Location")
            if location:
                print(f"リダイレクト先: {location}")
    except HTTPError as e:
        print(f"結果: {e.code} {e.reason}")
        if e.code == 401:
            www_auth = e.headers.get("WWW-Authenticate", "なし")
            print(f"WWW-Authenticate: {www_auth}")


def main():
    print("=" * 50)
    print("HTTPステータスコード体験ツール")
    print("=" * 50)

    categories = {
        "1": ("2xx 成功", [200, 201, 204]),
        "2": ("3xx リダイレクト", [301, 302]),
        "3": ("4xx クライアントエラー", [400, 401, 403, 404, 405, 429]),
        "4": ("5xx サーバーエラー", [500, 502, 503]),
    }

    while True:
        print("\nカテゴリを選択:")
        for key, (name, _) in categories.items():
            print(f"  {key}. {name}")
        print(f"  5. ステータスコードを直接入力")
        print(f"  6. 全ステータスコードの一覧表示")
        print(f"  q. 終了")

        choice = input("\n選択> ").strip()

        if choice == "q":
            break
        elif choice == "6":
            print("\n--- ステータスコード一覧 ---")
            for code, (name, desc) in sorted(STATUS_INFO.items()):
                print(f"  {code} {name:.<30} {desc}")
        elif choice == "5":
            code_str = input("ステータスコード（100-599）> ").strip()
            if code_str.isdigit() and 100 <= int(code_str) <= 599:
                try_status(int(code_str))
            else:
                print("無効なコードです。")
        elif choice in categories:
            _, codes = categories[choice]
            for code in codes:
                try_status(code)
        else:
            print("無効な選択です。")

    print("\nお疲れさまでした！")


if __name__ == "__main__":
    main()
