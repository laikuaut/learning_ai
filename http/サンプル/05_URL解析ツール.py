"""
HTTP/HTTPSサンプル05：URL解析ツール
====================================

学べる内容:
  - URLの各要素（スキーム、ホスト、パス、クエリ等）の解析
  - クエリパラメータの解析と構築
  - URLエンコード/デコード
  - 相対URLの解決

実行方法:
  python 05_URL解析ツール.py
"""

from urllib.parse import (
    urlparse, urlunparse, parse_qs, urlencode,
    quote, unquote, urljoin
)


def analyze_url(url):
    """URLを各要素に分解して表示"""
    parsed = urlparse(url)

    print(f"\n{'='*60}")
    print(f"URL解析結果")
    print(f"{'='*60}")
    print(f"入力URL: {url}")
    print(f"{'-'*60}")
    print(f"  スキーム    : {parsed.scheme or '(なし)'}")
    print(f"  ユーザー情報 : {parsed.username or '(なし)'}")
    print(f"  ホスト名    : {parsed.hostname or '(なし)'}")
    print(f"  ポート番号  : {parsed.port or '(デフォルト)'}")
    print(f"  パス        : {parsed.path or '/'}")
    print(f"  クエリ文字列 : {parsed.query or '(なし)'}")
    print(f"  フラグメント : {parsed.fragment or '(なし)'}")

    if parsed.query:
        params = parse_qs(parsed.query)
        print(f"\n  --- クエリパラメータ ---")
        for key, values in params.items():
            for v in values:
                print(f"    {key} = {v}")

    # デフォルトポートの情報
    default_ports = {"http": 80, "https": 443, "ftp": 21}
    if parsed.scheme in default_ports and not parsed.port:
        print(f"\n  ※ {parsed.scheme} のデフォルトポートは {default_ports[parsed.scheme]}")


def build_url():
    """パーツからURLを構築"""
    print(f"\n{'='*60}")
    print("URL構築")
    print(f"{'='*60}")

    scheme = input("  スキーム (https): ").strip() or "https"
    host = input("  ホスト名: ").strip() or "example.com"
    path = input("  パス (/api/users): ").strip() or "/api/users"
    params_str = input("  パラメータ (key=value&key2=value2): ").strip()

    url = urlunparse((scheme, host, path, "", params_str, ""))
    print(f"\n  構築されたURL: {url}")
    return url


def encode_decode():
    """URLエンコード/デコードのデモ"""
    print(f"\n{'='*60}")
    print("URLエンコード/デコード")
    print(f"{'='*60}")

    # エンコード
    examples = [
        "東京都 新宿区",
        "hello world!",
        "key=value&name=田中",
        "file name (1).pdf",
    ]

    print("\n  --- エンコード ---")
    for text in examples:
        encoded = quote(text, safe="")
        print(f"    {text}")
        print(f"    → {encoded}")
        print()

    # デコード
    encoded_examples = [
        "%E6%9D%B1%E4%BA%AC%E9%83%BD",
        "hello%20world%21",
        "%E7%94%B0%E4%B8%AD%E5%A4%AA%E9%83%8E",
    ]

    print("  --- デコード ---")
    for encoded in encoded_examples:
        decoded = unquote(encoded)
        print(f"    {encoded}")
        print(f"    → {decoded}")
        print()


def resolve_relative():
    """相対URLの解決"""
    print(f"\n{'='*60}")
    print("相対URL解決")
    print(f"{'='*60}")

    base = "https://example.com/docs/guide/chapter1.html"
    relatives = [
        "chapter2.html",
        "../reference/api.html",
        "/index.html",
        "//cdn.example.com/style.css",
        "https://other.com/page",
    ]

    print(f"\n  ベースURL: {base}")
    print(f"  {'-'*50}")

    for rel in relatives:
        resolved = urljoin(base, rel)
        print(f"  {rel:.<40} → {resolved}")


def query_builder():
    """クエリパラメータの構築"""
    print(f"\n{'='*60}")
    print("クエリパラメータ構築")
    print(f"{'='*60}")

    params = {}
    print("  パラメータを入力してください（空でEnterで終了）")

    while True:
        key = input("  キー> ").strip()
        if not key:
            break
        value = input("  値> ").strip()
        params[key] = value

    if params:
        query = urlencode(params)
        print(f"\n  クエリ文字列: ?{query}")
        print(f"  完全なURL例: https://api.example.com/search?{query}")
    else:
        # デモ
        demo_params = {"q": "Python 入門", "page": "1", "lang": "ja", "sort": "relevance"}
        query = urlencode(demo_params)
        print(f"\n  デモ: {demo_params}")
        print(f"  クエリ文字列: ?{query}")
        print(f"  完全なURL: https://api.example.com/search?{query}")


def main():
    print("=" * 50)
    print("URL解析ツール")
    print("=" * 50)

    while True:
        print("\nメニュー:")
        print("  1. URLを解析する")
        print("  2. URLを構築する")
        print("  3. エンコード/デコード")
        print("  4. 相対URLの解決")
        print("  5. クエリパラメータ構築")
        print("  6. デモ（サンプルURLで解析）")
        print("  q. 終了")

        choice = input("\n選択> ").strip()

        if choice == "q":
            break
        elif choice == "1":
            url = input("URL> ").strip()
            if url:
                analyze_url(url)
        elif choice == "2":
            build_url()
        elif choice == "3":
            encode_decode()
        elif choice == "4":
            resolve_relative()
        elif choice == "5":
            query_builder()
        elif choice == "6":
            samples = [
                "https://www.example.com:8443/api/v2/users?page=3&sort=name&lang=ja#results",
                "http://user:pass@localhost:3000/dashboard",
                "https://search.example.com/search?q=%E6%9D%B1%E4%BA%AC%E3%82%BF%E3%83%AF%E3%83%BC",
                "ftp://files.example.com/pub/docs/readme.txt",
            ]
            for url in samples:
                analyze_url(url)

    print("\nお疲れさまでした！")


if __name__ == "__main__":
    main()
