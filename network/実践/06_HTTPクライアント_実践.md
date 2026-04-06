# 実践課題06：HTTPクライアント ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第4章（TCP/UDP）、第6章（HTTP）
> **課題の種類**: ミニプロジェクト
> **学習目標**: HTTPプロトコルのリクエスト/レスポンスの構造を理解し、標準ライブラリだけでHTTPクライアントを実装する

---

## 完成イメージ

```
===== HTTPクライアント =====

1. GETリクエスト
2. HTTPヘッダの解析
3. レスポンスステータス一覧
4. URLの解析
5. 終了

選択: 1
URLを入力してください: http://example.com

【リクエスト】
  GET / HTTP/1.1
  Host: example.com
  Connection: close

【レスポンス】
  ステータス  : 200 OK
  Content-Type: text/html; charset=UTF-8
  Content-Length: 1256
  サーバ      : ECS (dcb/7F3B)

  ボディ（先頭500文字）:
  <!doctype html>
  <html>
  <head>
      <title>Example Domain</title>
  ...

選択: 4
URLを入力してください: http://example.com:8080/path/to/page?key=value&lang=ja

【URL解析結果】
  スキーム   : http
  ホスト     : example.com
  ポート     : 8080
  パス       : /path/to/page
  クエリ     : key=value&lang=ja
  パラメータ :
    key  = value
    lang = ja
```

---

## 課題の要件

1. `urllib.request` を使ってGETリクエストを送信し、レスポンスを取得する
2. HTTPレスポンスのステータスコード、ヘッダ、ボディを表示する
3. `urllib.parse` を使ってURLを構成要素に分解する
4. HTTPステータスコードの意味を表示する機能を実装する
5. メニュー形式で繰り返し操作できるようにする

---

## ステップガイド

<details>
<summary>ステップ1：GETリクエストを送信する</summary>

`urllib.request.urlopen()` でHTTPリクエストを送信できます。

```python
from urllib.request import urlopen, Request

url = "http://example.com"
req = Request(url, headers={"User-Agent": "MyHTTPClient/1.0"})
response = urlopen(req)

print(f"ステータス: {response.status}")
print(f"ヘッダ: {response.getheaders()}")
body = response.read().decode("utf-8")
print(f"ボディ: {body[:500]}")
```

</details>

<details>
<summary>ステップ2：URLを解析する</summary>

`urllib.parse` モジュールでURLを分解できます。

```python
from urllib.parse import urlparse, parse_qs

parsed = urlparse("http://example.com:8080/path?key=value")
print(f"スキーム: {parsed.scheme}")
print(f"ホスト: {parsed.hostname}")
print(f"ポート: {parsed.port}")
print(f"パス: {parsed.path}")
print(f"クエリ: {parsed.query}")
```

</details>

<details>
<summary>ステップ3：ステータスコードの辞書を作る</summary>

主要なHTTPステータスコードの意味を辞書で管理します。

```python
status_codes = {
    200: ("OK", "リクエスト成功"),
    301: ("Moved Permanently", "恒久的リダイレクト"),
    404: ("Not Found", "リソースが見つからない"),
    500: ("Internal Server Error", "サーバ内部エラー"),
}
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```python
# HTTPクライアント
# 学べる内容：HTTPプロトコル、urllib.request、URL解析
# 実行方法：python http_client.py

from urllib.request import urlopen, Request
from urllib.parse import urlparse, parse_qs
from urllib.error import URLError, HTTPError


def send_get_request(url):
    """GETリクエストを送信してレスポンスを表示する"""
    print()
    print("【リクエスト】")
    parsed = urlparse(url)
    print(f"  GET {parsed.path or '/'} HTTP/1.1")
    print(f"  Host: {parsed.hostname}")
    print(f"  Connection: close")

    try:
        req = Request(url, headers={"User-Agent": "MyHTTPClient/1.0"})
        response = urlopen(req, timeout=10)

        print()
        print("【レスポンス】")
        print(f"  ステータス  : {response.status} {response.reason}")

        # ヘッダ表示（主要なもの）
        important_headers = [
            "Content-Type", "Content-Length", "Server",
            "Date", "Last-Modified", "Location",
        ]
        for header_name in important_headers:
            value = response.getheader(header_name)
            if value:
                print(f"  {header_name}: {value}")

        # ボディ表示
        charset = response.headers.get_content_charset() or "utf-8"
        body = response.read().decode(charset, errors="replace")
        print()
        print(f"  ボディ（先頭500文字）:")
        for line in body[:500].split("\n"):
            print(f"  {line}")
        if len(body) > 500:
            print(f"  ... (全{len(body)}文字)")

    except HTTPError as e:
        print(f"\n  HTTPエラー: {e.code} {e.reason}")
    except URLError as e:
        print(f"\n  接続エラー: {e.reason}")
    except Exception as e:
        print(f"\n  エラー: {e}")


def analyze_headers(url):
    """HTTPレスポンスヘッダを詳細に表示する"""
    try:
        req = Request(url, headers={"User-Agent": "MyHTTPClient/1.0"})
        response = urlopen(req, timeout=10)

        print()
        print(f"【レスポンスヘッダ詳細: {url}】")
        print(f"  ステータス: {response.status} {response.reason}")
        print()
        print(f"  {'ヘッダ名':<25}{'値'}")
        print(f"  {'─' * 60}")
        for name, value in response.getheaders():
            print(f"  {name:<25}{value}")
        response.close()

    except HTTPError as e:
        print(f"  HTTPエラー: {e.code} {e.reason}")
    except URLError as e:
        print(f"  接続エラー: {e.reason}")


def show_status_codes():
    """HTTPステータスコード一覧を表示する"""
    status_codes = {
        # 1xx: 情報レスポンス
        100: ("Continue", "継続"),
        101: ("Switching Protocols", "プロトコル切替"),
        # 2xx: 成功
        200: ("OK", "リクエスト成功"),
        201: ("Created", "リソース作成成功"),
        204: ("No Content", "内容なし"),
        # 3xx: リダイレクト
        301: ("Moved Permanently", "恒久的リダイレクト"),
        302: ("Found", "一時的リダイレクト"),
        304: ("Not Modified", "未更新（キャッシュ利用）"),
        # 4xx: クライアントエラー
        400: ("Bad Request", "不正なリクエスト"),
        401: ("Unauthorized", "認証が必要"),
        403: ("Forbidden", "アクセス禁止"),
        404: ("Not Found", "リソースが見つからない"),
        405: ("Method Not Allowed", "メソッド不許可"),
        408: ("Request Timeout", "リクエストタイムアウト"),
        429: ("Too Many Requests", "リクエスト過多"),
        # 5xx: サーバエラー
        500: ("Internal Server Error", "サーバ内部エラー"),
        502: ("Bad Gateway", "不正なゲートウェイ"),
        503: ("Service Unavailable", "サービス利用不可"),
        504: ("Gateway Timeout", "ゲートウェイタイムアウト"),
    }

    print()
    print("【HTTPステータスコード一覧】")
    print(f"  {'コード':<8}{'英名':<28}{'説明'}")
    print(f"  {'─' * 55}")

    current_category = 0
    for code, (name, desc) in sorted(status_codes.items()):
        category = code // 100
        if category != current_category:
            current_category = category
            categories = {1: "情報", 2: "成功", 3: "リダイレクト", 4: "クライアントエラー", 5: "サーバエラー"}
            print(f"\n  --- {category}xx: {categories.get(category, '')} ---")
        print(f"  {code:<8}{name:<28}{desc}")


def parse_url(url):
    """URLを構成要素に分解する"""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    print()
    print("【URL解析結果】")
    print(f"  スキーム   : {parsed.scheme or '(なし)'}")
    print(f"  ホスト     : {parsed.hostname or '(なし)'}")
    print(f"  ポート     : {parsed.port or '(デフォルト)'}")
    print(f"  パス       : {parsed.path or '/'}")
    print(f"  クエリ     : {parsed.query or '(なし)'}")
    print(f"  フラグメント: {parsed.fragment or '(なし)'}")

    if params:
        print(f"  パラメータ :")
        for key, values in params.items():
            for value in values:
                print(f"    {key} = {value}")


# --- メイン処理 ---
print("===== HTTPクライアント =====")

while True:
    print()
    print("1. GETリクエスト")
    print("2. HTTPヘッダの解析")
    print("3. ステータスコード一覧")
    print("4. URLの解析")
    print("5. 終了")
    print()

    choice = input("選択: ").strip()

    if choice == "1":
        url = input("URLを入力してください: ").strip()
        send_get_request(url)

    elif choice == "2":
        url = input("URLを入力してください: ").strip()
        analyze_headers(url)

    elif choice == "3":
        show_status_codes()

    elif choice == "4":
        url = input("URLを入力してください: ").strip()
        parse_url(url)

    elif choice == "5":
        print("終了します。")
        break

    else:
        print("1〜5の番号を入力してください。")
```

</details>

<details>
<summary>解答例（改良版 ─ 応答時間計測とリダイレクト追跡）</summary>

応答時間の計測、リダイレクトの追跡、レスポンスサイズの表示を追加したバージョンです。

```python
# HTTPクライアント（改良版）
# 学べる内容：HTTP詳細、リダイレクト追跡、応答時間計測
# 実行方法：python http_client_v2.py

from urllib.request import urlopen, Request, build_opener, HTTPRedirectHandler
from urllib.parse import urlparse, parse_qs
from urllib.error import URLError, HTTPError
import time


class RedirectTracker(HTTPRedirectHandler):
    """リダイレクトを追跡するハンドラ"""

    def __init__(self):
        super().__init__()
        self.redirects = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.redirects.append({
            "code": code,
            "message": msg,
            "from": req.full_url,
            "to": newurl,
        })
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def send_get_with_timing(url):
    """GETリクエストを送信して詳細なレスポンス情報を表示する"""
    parsed = urlparse(url)

    print(f"\n【リクエスト】")
    print(f"  GET {parsed.path or '/'} HTTP/1.1")
    print(f"  Host: {parsed.hostname}")

    tracker = RedirectTracker()
    opener = build_opener(tracker)

    try:
        req = Request(url, headers={
            "User-Agent": "MyHTTPClient/2.0",
            "Accept": "text/html, application/json, */*",
        })

        start = time.time()
        response = opener.open(req, timeout=10)
        elapsed_ms = (time.time() - start) * 1000

        body_bytes = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        body = body_bytes.decode(charset, errors="replace")

        print(f"\n【レスポンス】")
        print(f"  ステータス    : {response.status} {response.reason}")
        print(f"  応答時間      : {elapsed_ms:.0f}ms")
        print(f"  Content-Type  : {response.getheader('Content-Type', '不明')}")
        print(f"  レスポンスサイズ: {len(body_bytes):,} bytes")

        # リダイレクト追跡結果
        if tracker.redirects:
            print(f"\n【リダイレクト追跡】")
            for i, r in enumerate(tracker.redirects, 1):
                print(f"  {i}. [{r['code']}] {r['from']}")
                print(f"     → {r['to']}")

        # ヘッダ
        print(f"\n【主要ヘッダ】")
        for name, value in response.getheaders():
            print(f"  {name}: {value}")

        # ボディ
        print(f"\n【ボディ（先頭300文字）】")
        for line in body[:300].split("\n"):
            print(f"  {line}")

        response.close()

    except HTTPError as e:
        elapsed_ms = (time.time() - start) * 1000
        print(f"\n  HTTPエラー: {e.code} {e.reason} ({elapsed_ms:.0f}ms)")
    except URLError as e:
        print(f"\n  接続エラー: {e.reason}")


def compare_urls(urls):
    """複数URLの応答時間を比較する"""
    print(f"\n{'─' * 65}")
    print(f"  {'URL':<35}{'ステータス':<12}{'サイズ':>10}{'応答時間':>10}")
    print(f"{'─' * 65}")

    for url in urls:
        url = url.strip()
        if not url:
            continue
        try:
            req = Request(url, headers={"User-Agent": "MyHTTPClient/2.0"})
            start = time.time()
            response = urlopen(req, timeout=10)
            elapsed_ms = (time.time() - start) * 1000
            size = len(response.read())
            print(f"  {url:<35}{response.status:<12}{size:>8,}B{elapsed_ms:>8.0f}ms")
            response.close()
        except Exception as e:
            print(f"  {url:<35}{'エラー':<12}{str(e)[:20]:>18}")

    print(f"{'─' * 65}")


def main():
    print("===== HTTPクライアント（改良版） =====")

    while True:
        print("\n1. GETリクエスト  2. URL比較  3. ステータスコード  4. URL解析  5. 終了")
        choice = input("選択: ").strip()

        if choice == "1":
            url = input("URL: ").strip()
            send_get_with_timing(url)
        elif choice == "2":
            urls_str = input("URLをカンマ区切りで入力:\n").strip()
            compare_urls(urls_str.split(","))
        elif choice == "3":
            codes = {
                200: "OK", 301: "Moved Permanently", 302: "Found",
                304: "Not Modified", 400: "Bad Request", 401: "Unauthorized",
                403: "Forbidden", 404: "Not Found", 500: "Internal Server Error",
                502: "Bad Gateway", 503: "Service Unavailable",
            }
            print("\n【主要ステータスコード】")
            for code, name in sorted(codes.items()):
                print(f"  {code} {name}")
        elif choice == "4":
            url = input("URL: ").strip()
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            print(f"\n  スキーム: {parsed.scheme}  ホスト: {parsed.hostname}")
            print(f"  ポート: {parsed.port or 'デフォルト'}  パス: {parsed.path}")
            if params:
                print(f"  パラメータ:")
                for k, v in params.items():
                    print(f"    {k} = {', '.join(v)}")
        elif choice == "5":
            print("終了します。")
            break


if __name__ == "__main__":
    main()
```

**初心者向けとの違い:**
- `HTTPRedirectHandler` をカスタマイズしてリダイレクトチェーンを追跡
- 複数URLの応答時間を比較する機能
- レスポンスサイズの計測と表示
- クラスの継承を活用した拡張

</details>
