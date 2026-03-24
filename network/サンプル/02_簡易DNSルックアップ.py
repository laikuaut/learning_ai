# ==============================
# 簡易DNSルックアップツール
# ネットワーク基礎：DNSの仕組みを体験するサンプル
# ==============================
# 学べる内容:
#   - DNS（Domain Name System）の基本的な仕組み
#   - socket.getaddrinfo() を使った名前解決
#   - IPv4 / IPv6 アドレスの違い
#   - 正引き（ドメイン名 → IPアドレス）の実践
#   - 逆引き（IPアドレス → ドメイン名）の試行
#   - DNSレコードタイプ（A, AAAA）の理解
#
# 実行方法:
#   python 02_簡易DNSルックアップ.py
#
# ※ 本プログラムは教育目的で作成されています
# ※ インターネット接続が必要です
# ==============================

import socket
import time


def explain_dns():
    """DNSの仕組みをアスキーアートで解説します"""
    print("""
  ┌──────────────────────────────────────────────────┐
  │              DNSの仕組み                         │
  └──────────────────────────────────────────────────┘

  人間が覚えやすい「ドメイン名」と、
  コンピュータが使う「IPアドレス」を変換する仕組みです。

  【正引き（Forward Lookup）】
  ドメイン名 → IPアドレス

    ユーザー           DNSサーバー          Webサーバー
    ┌─────┐            ┌─────┐            ┌─────┐
    │ PC  │──(1)問い合わせ→│ DNS │            │ Web │
    │     │  example.com│     │            │     │
    │     │←(2)応答──── │     │            │     │
    │     │  93.184.216.34   │            │     │
    │     │──(3)接続──────────────────────→│     │
    └─────┘            └─────┘            └─────┘

  【逆引き（Reverse Lookup）】
  IPアドレス → ドメイン名

  ┌─────────────────────────────────────────────────┐
  │  主なDNSレコードタイプ                           │
  ├──────┬──────────────────────────────────────────┤
  │  A    │ ドメイン名 → IPv4アドレス               │
  │  AAAA │ ドメイン名 → IPv6アドレス               │
  │  MX   │ メールサーバーの指定                     │
  │  CNAME│ ドメインの別名（エイリアス）             │
  │  NS   │ 権威DNSサーバーの指定                    │
  │  TXT  │ テキスト情報（SPF等）                    │
  └──────┴──────────────────────────────────────────┘
    """)


def forward_lookup(domain):
    """正引き: ドメイン名からIPアドレスを取得します"""
    print(f"\n  ─── 正引き: {domain} ───")
    print(f"  問い合わせ中...")

    start_time = time.time()

    results = {"ipv4": [], "ipv6": []}

    try:
        # IPv4 アドレスの取得（Aレコード相当）
        try:
            addr_info_v4 = socket.getaddrinfo(domain, None, socket.AF_INET)
            for info in addr_info_v4:
                ip = info[4][0]
                if ip not in results["ipv4"]:
                    results["ipv4"].append(ip)
        except socket.gaierror:
            pass

        # IPv6 アドレスの取得（AAAAレコード相当）
        try:
            addr_info_v6 = socket.getaddrinfo(domain, None, socket.AF_INET6)
            for info in addr_info_v6:
                ip = info[4][0]
                if ip not in results["ipv6"]:
                    results["ipv6"].append(ip)
        except socket.gaierror:
            pass

        elapsed = (time.time() - start_time) * 1000  # ミリ秒

        if not results["ipv4"] and not results["ipv6"]:
            print(f"  ※ 名前解決できませんでした: {domain}")
            return

        print(f"  応答時間: {elapsed:.1f} ms\n")

        # IPv4 結果
        if results["ipv4"]:
            print(f"  【IPv4 アドレス（Aレコード）】")
            for ip in results["ipv4"]:
                print(f"    {domain} → {ip}")
        else:
            print(f"  【IPv4】レコードが見つかりませんでした")

        # IPv6 結果
        if results["ipv6"]:
            print(f"\n  【IPv6 アドレス（AAAAレコード）】")
            for ip in results["ipv6"]:
                print(f"    {domain} → {ip}")
        else:
            print(f"\n  【IPv6】レコードが見つかりませんでした")

    except socket.gaierror as e:
        print(f"  ※ DNS解決エラー: {e}")
    except Exception as e:
        print(f"  ※ エラーが発生しました: {e}")


def reverse_lookup(ip_str):
    """逆引き: IPアドレスからドメイン名を取得します"""
    print(f"\n  ─── 逆引き: {ip_str} ───")
    print(f"  問い合わせ中...")

    start_time = time.time()

    try:
        hostname, aliases, addresses = socket.gethostbyaddr(ip_str)
        elapsed = (time.time() - start_time) * 1000

        print(f"  応答時間: {elapsed:.1f} ms\n")
        print(f"  【結果】")
        print(f"    IPアドレス: {ip_str}")
        print(f"    ホスト名:   {hostname}")
        if aliases:
            print(f"    別名:")
            for alias in aliases:
                print(f"      - {alias}")

    except socket.herror:
        print(f"  ※ 逆引きレコードが見つかりませんでした")
        print(f"     （すべてのIPアドレスに逆引きが設定されているわけではありません）")
    except socket.gaierror as e:
        print(f"  ※ DNS解決エラー: {e}")
    except Exception as e:
        print(f"  ※ エラーが発生しました: {e}")


def lookup_multiple(domains):
    """複数ドメインをまとめて名前解決します"""
    print("\n" + "=" * 55)
    print("  複数ドメインの一括ルックアップ")
    print("=" * 55)

    results_table = []

    for domain in domains:
        try:
            addr_info = socket.getaddrinfo(domain, None, socket.AF_INET)
            ip = addr_info[0][4][0] if addr_info else "取得失敗"
        except socket.gaierror:
            ip = "解決できず"

        results_table.append((domain, ip))

    # テーブル形式で表示
    print(f"\n  {'ドメイン名':<30} {'IPv4アドレス':<20}")
    print(f"  {'─' * 30} {'─' * 20}")
    for domain, ip in results_table:
        print(f"  {domain:<30} {ip:<20}")


def get_local_info():
    """自分のマシンのネットワーク情報を表示します"""
    print("\n" + "=" * 55)
    print("  ローカルマシンのネットワーク情報")
    print("=" * 55)

    try:
        hostname = socket.gethostname()
        print(f"\n  ホスト名:     {hostname}")

        # ローカルIPアドレスの取得
        try:
            local_ip = socket.gethostbyname(hostname)
            print(f"  ローカルIP:   {local_ip}")
        except socket.gaierror:
            print(f"  ローカルIP:   取得できませんでした")

        # FQDN の取得
        fqdn = socket.getfqdn()
        print(f"  FQDN:         {fqdn}")

    except Exception as e:
        print(f"  ※ 情報取得に失敗しました: {e}")


def demo_mode():
    """デモモード: 代表的なドメインで名前解決を実行します"""
    print("\n" + "=" * 55)
    print("  【デモモード】代表的なドメインのDNSルックアップ")
    print("=" * 55)

    # ローカル情報の表示
    get_local_info()

    # 代表的なドメインの一括ルックアップ
    demo_domains = [
        "www.google.com",
        "www.yahoo.co.jp",
        "github.com",
        "www.python.org",
    ]
    lookup_multiple(demo_domains)

    # 詳細ルックアップの例
    print("\n" + "-" * 55)
    print("  詳細ルックアップの例")
    print("-" * 55)
    forward_lookup("www.google.com")


def interactive_mode():
    """対話モード: ユーザーが入力したドメインで名前解決します"""
    print("\n" + "=" * 55)
    print("  【対話モード】DNSルックアップ")
    print("=" * 55)

    while True:
        print("\n  操作を選んでください:")
        print("  1. 正引き（ドメイン名 → IPアドレス）")
        print("  2. 逆引き（IPアドレス → ドメイン名）")
        print("  3. 自分のマシンのネットワーク情報")
        print("  4. メニューに戻る")

        choice = input("\n  選択 (1-4): ").strip()

        if choice == "1":
            domain = input("  ドメイン名を入力 (例: www.google.com): ").strip()
            if domain:
                forward_lookup(domain)
            else:
                print("  ※ ドメイン名を入力してください。")

        elif choice == "2":
            ip_str = input("  IPアドレスを入力 (例: 8.8.8.8): ").strip()
            if ip_str:
                reverse_lookup(ip_str)
            else:
                print("  ※ IPアドレスを入力してください。")

        elif choice == "3":
            get_local_info()

        elif choice == "4":
            break
        else:
            print("  ※ 1〜4 の数字を入力してください。")


# --- メインプログラム ---
if __name__ == "__main__":
    print("+" + "=" * 53 + "+")
    print("|        簡易DNSルックアップツール                  |")
    print("|        〜 名前解決の仕組みを体験しよう 〜         |")
    print("+" + "=" * 53 + "+")

    # DNSの解説を最初に表示
    explain_dns()

    while True:
        print("\n  モードを選択してください:")
        print("  1. デモモード（代表的なドメインで実行）")
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
