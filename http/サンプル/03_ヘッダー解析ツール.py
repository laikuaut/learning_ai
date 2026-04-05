"""
HTTP/HTTPSサンプル03：ヘッダー解析ツール
========================================

学べる内容:
  - リクエスト/レスポンスヘッダーの確認
  - Content-Type, Cache-Control 等の解析
  - カスタムヘッダーの送信
  - セキュリティヘッダーのチェック

実行方法:
  python 03_ヘッダー解析ツール.py
"""

from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.parse import urlparse


SECURITY_HEADERS = {
    "Strict-Transport-Security": "HSTS（HTTPS強制）",
    "Content-Security-Policy": "CSP（リソース読込元制限）",
    "X-Content-Type-Options": "MIMEスニッフィング防止",
    "X-Frame-Options": "クリックジャッキング防止",
    "X-XSS-Protection": "XSSフィルター",
    "Referrer-Policy": "リファラー制御",
    "Permissions-Policy": "ブラウザ機能制限",
}


def analyze_url(url):
    """URLのレスポンスヘッダーを解析"""
    print(f"\n{'='*60}")
    print(f"ヘッダー解析: {url}")
    print(f"{'='*60}")

    try:
        req = Request(url, method="GET")
        req.add_header("User-Agent", "HTTP-Learning-Tool/1.0")

        with urlopen(req, timeout=10) as response:
            print(f"\nステータス: {response.status} {response.reason}")

            # 全ヘッダー表示
            print(f"\n--- レスポンスヘッダー ---")
            for header, value in response.getheaders():
                print(f"  {header}: {value}")

            # Content-Type 解析
            ct = response.getheader("Content-Type", "")
            print(f"\n--- Content-Type 解析 ---")
            if ";" in ct:
                mime, *params = ct.split(";")
                print(f"  MIMEタイプ: {mime.strip()}")
                for p in params:
                    print(f"  パラメータ: {p.strip()}")
            else:
                print(f"  MIMEタイプ: {ct}")

            # キャッシュ関連
            print(f"\n--- キャッシュ情報 ---")
            cc = response.getheader("Cache-Control", "未設定")
            etag = response.getheader("ETag", "未設定")
            lm = response.getheader("Last-Modified", "未設定")
            print(f"  Cache-Control: {cc}")
            print(f"  ETag: {etag}")
            print(f"  Last-Modified: {lm}")

            # セキュリティヘッダーチェック
            print(f"\n--- セキュリティヘッダーチェック ---")
            score = 0
            total = len(SECURITY_HEADERS)
            for header, desc in SECURITY_HEADERS.items():
                value = response.getheader(header)
                if value:
                    print(f"  ✅ {header}: {value}")
                    score += 1
                else:
                    print(f"  ❌ {header}: 未設定 ({desc})")

            print(f"\n  スコア: {score}/{total}")
            if score == total:
                print("  → 全セキュリティヘッダーが設定されています！")
            elif score >= total * 0.7:
                print("  → 概ね良好ですが、一部改善の余地があります。")
            else:
                print("  → セキュリティヘッダーの設定を強く推奨します。")

            # サーバー情報
            server = response.getheader("Server", "")
            powered = response.getheader("X-Powered-By", "")
            if server or powered:
                print(f"\n--- サーバー情報（露出注意）---")
                if server:
                    print(f"  ⚠ Server: {server}")
                if powered:
                    print(f"  ⚠ X-Powered-By: {powered}")
                print("  → 本番環境ではバージョン情報を隠すべきです")

    except HTTPError as e:
        print(f"HTTPエラー: {e.code} {e.reason}")
    except Exception as e:
        print(f"エラー: {e}")


def main():
    print("=" * 50)
    print("HTTPヘッダー解析ツール")
    print("=" * 50)

    while True:
        print("\nメニュー:")
        print("  1. URLを入力して解析")
        print("  2. サンプルサイトを解析")
        print("  q. 終了")

        choice = input("\n選択> ").strip()

        if choice == "q":
            break
        elif choice == "1":
            url = input("URL（https://...）> ").strip()
            if not url.startswith("http"):
                url = "https://" + url
            analyze_url(url)
        elif choice == "2":
            samples = [
                "https://httpbin.org/get",
                "https://www.google.com",
                "https://github.com",
            ]
            print("\nサンプルサイト:")
            for i, url in enumerate(samples, 1):
                print(f"  {i}. {url}")
            idx = input("番号> ").strip()
            if idx.isdigit() and 1 <= int(idx) <= len(samples):
                analyze_url(samples[int(idx) - 1])

    print("\nお疲れさまでした！")


if __name__ == "__main__":
    main()
