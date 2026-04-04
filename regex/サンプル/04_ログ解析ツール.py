"""
正規表現サンプル04：ログ解析ツール
==================================

学べる内容:
  - 名前付きグループ (?P<name>...) の活用
  - re.compile() + re.VERBOSE による可読性の向上
  - Counter を使った集計処理
  - 正規表現と他のPython機能の組み合わせ

実行方法:
  python 04_ログ解析ツール.py
"""

import re
from collections import Counter
from datetime import datetime


# サンプルログデータ
SAMPLE_LOG = """192.168.1.10 - admin [05/Apr/2026:09:00:00 +0900] "GET /index.html HTTP/1.1" 200 2048
192.168.1.20 - - [05/Apr/2026:09:00:01 +0900] "GET /style.css HTTP/1.1" 200 512
10.0.0.5 - - [05/Apr/2026:09:00:02 +0900] "POST /api/login HTTP/1.1" 401 128
192.168.1.10 - admin [05/Apr/2026:09:00:03 +0900] "GET /dashboard HTTP/1.1" 200 4096
10.0.0.5 - - [05/Apr/2026:09:00:04 +0900] "POST /api/login HTTP/1.1" 200 256
192.168.1.30 - guest [05/Apr/2026:09:00:05 +0900] "GET /admin HTTP/1.1" 403 64
192.168.1.10 - admin [05/Apr/2026:09:00:06 +0900] "GET /api/users HTTP/1.1" 200 1024
10.0.0.5 - user1 [05/Apr/2026:09:00:07 +0900] "GET /dashboard HTTP/1.1" 200 4096
192.168.1.20 - - [05/Apr/2026:09:00:08 +0900] "GET /notfound HTTP/1.1" 404 128
192.168.1.10 - admin [05/Apr/2026:09:00:09 +0900] "DELETE /api/users/1 HTTP/1.1" 500 64
10.0.0.5 - user1 [05/Apr/2026:09:15:00 +0900] "GET /api/products HTTP/1.1" 200 2048
192.168.1.20 - - [05/Apr/2026:09:15:01 +0900] "GET /index.html HTTP/1.1" 200 2048
10.0.0.100 - - [05/Apr/2026:09:15:02 +0900] "POST /api/upload HTTP/1.1" 413 32
192.168.1.10 - admin [05/Apr/2026:09:30:00 +0900] "GET /api/stats HTTP/1.1" 200 512
10.0.0.5 - user1 [05/Apr/2026:09:30:01 +0900] "PUT /api/users/1 HTTP/1.1" 200 128"""

# ログ行の正規表現パターン
LOG_PATTERN = re.compile(r"""
    (?P<ip>\d{1,3}(?:\.\d{1,3}){3})       # IPアドレス
    \s-\s                                   # 区切り
    (?P<user>\S+)                           # ユーザー名（-は未認証）
    \s\[                                    # [
    (?P<datetime>[^\]]+)                    # 日時
    \]\s"                                   # ] "
    (?P<method>[A-Z]+)                      # HTTPメソッド
    \s                                      # スペース
    (?P<path>\S+)                           # リクエストパス
    \s                                      # スペース
    (?P<protocol>HTTP/[\d.]+)               # プロトコル
    "\s                                     # "
    (?P<status>\d{3})                       # ステータスコード
    \s                                      # スペース
    (?P<size>\d+)                           # レスポンスサイズ
""", re.VERBOSE)


def parse_log(log_text):
    """ログテキストを解析してエントリのリストを返す"""
    entries = []
    for line in log_text.strip().split("\n"):
        match = LOG_PATTERN.match(line.strip())
        if match:
            entry = match.groupdict()
            entry["status"] = int(entry["status"])
            entry["size"] = int(entry["size"])
            entries.append(entry)
    return entries


def print_summary(entries):
    """ログのサマリーレポートを出力"""
    print(f"\n{'=' * 60}")
    print(f"  アクセスログ解析レポート")
    print(f"{'=' * 60}")

    # 総リクエスト数
    print(f"\n■ 総リクエスト数: {len(entries)}件")

    # ステータスコード別
    print(f"\n■ ステータスコード別:")
    status_counter = Counter(e["status"] for e in entries)
    for status in sorted(status_counter):
        count = status_counter[status]
        bar = "█" * count
        label = {200: "OK", 401: "Unauthorized", 403: "Forbidden",
                 404: "Not Found", 413: "Payload Too Large", 500: "Server Error"}
        print(f"    {status} {label.get(status, ''): <20} {bar} ({count}件)")

    # HTTPメソッド別
    print(f"\n■ HTTPメソッド別:")
    method_counter = Counter(e["method"] for e in entries)
    for method, count in method_counter.most_common():
        print(f"    {method: <8} {count}件")

    # IPアドレス Top5
    print(f"\n■ アクセス数 Top 5 (IPアドレス):")
    ip_counter = Counter(e["ip"] for e in entries)
    for i, (ip, count) in enumerate(ip_counter.most_common(5), 1):
        print(f"    {i}. {ip: <16} {count}回")

    # 人気パス Top5
    print(f"\n■ アクセス数 Top 5 (パス):")
    path_counter = Counter(e["path"] for e in entries)
    for i, (path, count) in enumerate(path_counter.most_common(5), 1):
        print(f"    {i}. {path: <25} {count}回")

    # エラーリクエスト
    errors = [e for e in entries if e["status"] >= 400]
    if errors:
        print(f"\n■ エラーリクエスト ({len(errors)}件):")
        for e in errors:
            print(f"    [{e['status']}] {e['ip']} {e['method']} {e['path']}")

    # 転送量
    total_size = sum(e["size"] for e in entries)
    print(f"\n■ 総転送量: {total_size:,} bytes ({total_size / 1024:.1f} KB)")

    print(f"\n{'=' * 60}")


def search_logs(entries):
    """対話式のログ検索"""
    print("\n--- ログ検索モード ---")
    print("検索条件を入力してください（例: status=404, ip=192.168, path=/api）")
    print("'back' で戻ります")

    while True:
        query = input("\n検索> ").strip()
        if query.lower() == "back":
            break

        if "=" not in query:
            print("  形式: フィールド名=値 で入力してください")
            continue

        field, value = query.split("=", 1)
        field = field.strip()
        value = value.strip()

        results = []
        for e in entries:
            if field in e:
                entry_value = str(e[field])
                if re.search(value, entry_value):
                    results.append(e)

        print(f"  {len(results)}件見つかりました:")
        for e in results:
            print(f"    {e['ip']} [{e['status']}] {e['method']} {e['path']}")


def main():
    print("=" * 50)
    print("正規表現 ログ解析ツール")
    print("=" * 50)

    entries = parse_log(SAMPLE_LOG)

    while True:
        print("\nメニュー:")
        print("  1. サマリーレポート表示")
        print("  2. ログ検索")
        print("  3. 生データ表示（先頭5件）")
        print("  q. 終了")

        choice = input("\n選択> ").strip()

        if choice == "q":
            break
        elif choice == "1":
            print_summary(entries)
        elif choice == "2":
            search_logs(entries)
        elif choice == "3":
            print("\n--- 解析済みデータ（先頭5件）---")
            for i, e in enumerate(entries[:5], 1):
                print(f"\n  エントリ {i}:")
                for k, v in e.items():
                    print(f"    {k}: {v}")

    print("\nお疲れさまでした！")


if __name__ == "__main__":
    main()
