# ==============================
# 簡易ポートスキャナー（教育用）
# ネットワーク基礎：ポートとサービスの仕組みを体験するサンプル
# ==============================
# 学べる内容:
#   - ポート番号の概念とウェルノウンポート
#   - TCP接続の仕組み（3ウェイハンドシェイク）
#   - socket を使ったTCP接続の実装
#   - サービスとポート番号の対応関係
#   - タイムアウトの概念
#
# 実行方法:
#   python 04_ポートスキャナー.py
#
# ╔══════════════════════════════════════════════════╗
# ║  【重要】教育目的限定                            ║
# ║  本プログラムは教育・学習目的でのみ使用して      ║
# ║  ください。自分が管理していないサーバーに対して   ║
# ║  ポートスキャンを行うことは、法律に抵触する      ║
# ║  可能性があります。必ず自分の管理するマシン       ║
# ║  (localhost) でのみ実行してください。             ║
# ╚══════════════════════════════════════════════════╝
# ==============================

import socket
import time


def explain_ports():
    """ポートの概念をアスキーアートで解説します"""
    print("""
  ┌──────────────────────────────────────────────────┐
  │              ポートとは？                         │
  └──────────────────────────────────────────────────┘

  ポートは、コンピュータ上で動作する各サービス（アプリ）を
  識別するための「番号」です。IPアドレスが「住所」なら、
  ポート番号は「部屋番号」のようなものです。

    IPアドレス     ポート番号       サービス
    ┌──────┐      ┌─────┐
    │192.  │      │ :80 │────── Webサーバー (HTTP)
    │168.  │──────│:443 │────── Webサーバー (HTTPS)
    │1.1   │      │ :22 │────── SSH
    │      │      │ :25 │────── メール (SMTP)
    └──────┘      └─────┘

  【ポート番号の範囲】
  ┌──────────────┬─────────────────────────────────┐
  │ 0 〜 1023    │ ウェルノウンポート（予約済み）   │
  │ 1024 〜 49151│ 登録済みポート（アプリ用）       │
  │ 49152〜 65535│ 動的/プライベートポート           │
  └──────────────┴─────────────────────────────────┘

  【TCP 3ウェイハンドシェイク】
  接続確立の手順です:

    クライアント                サーバー
    ┌─────┐                   ┌─────┐
    │     │── SYN ──────────→│     │  (1) 接続要求
    │     │←─ SYN+ACK ───── │     │  (2) 要求承認
    │     │── ACK ──────────→│     │  (3) 確認応答
    │     │                   │     │
    │     │ ←── データ通信 ──→│     │  接続確立！
    └─────┘                   └─────┘
    """)


# ウェルノウンポートの一覧
WELL_KNOWN_PORTS = {
    20: ("FTP-Data", "ファイル転送（データ）"),
    21: ("FTP", "ファイル転送（制御）"),
    22: ("SSH", "セキュアシェル（暗号化リモートアクセス）"),
    23: ("Telnet", "リモートアクセス（非暗号化、非推奨）"),
    25: ("SMTP", "メール送信"),
    53: ("DNS", "名前解決"),
    67: ("DHCP-Server", "IPアドレス自動割当（サーバー側）"),
    68: ("DHCP-Client", "IPアドレス自動割当（クライアント側）"),
    80: ("HTTP", "Webサーバー"),
    110: ("POP3", "メール受信"),
    123: ("NTP", "時刻同期"),
    143: ("IMAP", "メール受信（サーバー管理）"),
    443: ("HTTPS", "Webサーバー（暗号化）"),
    445: ("SMB", "ファイル共有（Windows）"),
    465: ("SMTPS", "メール送信（暗号化）"),
    587: ("SMTP-Submission", "メール送信（サブミッション）"),
    993: ("IMAPS", "メール受信（暗号化）"),
    995: ("POP3S", "メール受信（暗号化）"),
    3306: ("MySQL", "MySQLデータベース"),
    3389: ("RDP", "リモートデスクトップ"),
    5432: ("PostgreSQL", "PostgreSQLデータベース"),
    5900: ("VNC", "仮想ネットワークコンピューティング"),
    6379: ("Redis", "Redisキャッシュサーバー"),
    8080: ("HTTP-Alt", "HTTP代替（開発用など）"),
    8443: ("HTTPS-Alt", "HTTPS代替"),
    27017: ("MongoDB", "MongoDBデータベース"),
}


def get_service_name(port):
    """ポート番号からサービス名を取得します"""
    if port in WELL_KNOWN_PORTS:
        name, desc = WELL_KNOWN_PORTS[port]
        return f"{name} - {desc}"

    # socket モジュールでも調べてみます
    try:
        service = socket.getservbyport(port, "tcp")
        return service
    except OSError:
        return "不明なサービス"


def scan_port(host, port, timeout=1.0):
    """指定ホストの特定ポートが開いているか確認します"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0  # 0 = 接続成功 = ポートが開いている
    except socket.error:
        return False


def scan_ports(host, ports, timeout=0.5):
    """複数のポートをスキャンして結果を表示します"""
    print(f"\n  スキャン対象: {host}")
    print(f"  スキャンポート数: {len(ports)}")
    print(f"  タイムアウト: {timeout}秒")
    print(f"\n  スキャン開始...")

    start_time = time.time()
    open_ports = []
    closed_ports = []

    for i, port in enumerate(ports):
        # 進捗表示
        progress = (i + 1) / len(ports) * 100
        print(f"\r  進捗: [{('█' * int(progress / 5)).ljust(20)}] {progress:.0f}% "
              f"(ポート {port})", end="", flush=True)

        is_open = scan_port(host, port, timeout)

        if is_open:
            open_ports.append(port)
        else:
            closed_ports.append(port)

    elapsed = time.time() - start_time
    print(f"\r  スキャン完了！ (所要時間: {elapsed:.1f}秒)" + " " * 30)

    # 結果表示
    print("\n" + "-" * 55)
    print(f"  スキャン結果: {host}")
    print("-" * 55)

    if open_ports:
        print(f"\n  【開いているポート: {len(open_ports)}個】")
        print(f"  {'ポート':<8} {'状態':<8} {'サービス'}")
        print(f"  {'─' * 8} {'─' * 8} {'─' * 30}")
        for port in open_ports:
            service = get_service_name(port)
            print(f"  {port:<8} {'OPEN':<8} {service}")
    else:
        print("\n  開いているポートはありませんでした。")

    print(f"\n  閉じているポート: {len(closed_ports)}個")
    print(f"  合計スキャン数:   {len(ports)}個")

    return open_ports


def show_well_known_ports():
    """ウェルノウンポートの一覧を表示します"""
    print("\n" + "=" * 65)
    print("  ウェルノウンポート一覧")
    print("=" * 65)
    print(f"\n  {'ポート':<8} {'プロトコル':<15} {'説明'}")
    print(f"  {'─' * 8} {'─' * 15} {'─' * 35}")

    for port in sorted(WELL_KNOWN_PORTS.keys()):
        name, desc = WELL_KNOWN_PORTS[port]
        print(f"  {port:<8} {name:<15} {desc}")


def demo_mode():
    """デモモード: localhostの代表的なポートをスキャンします"""
    print("\n" + "=" * 55)
    print("  【デモモード】localhost のポートスキャン")
    print("=" * 55)
    print("\n  ※ 自分のマシン（localhost）のみスキャンします")

    # ウェルノウンポートの解説
    show_well_known_ports()

    # localhost の代表的なポートをスキャン
    common_ports = [22, 80, 443, 3000, 3306, 5432, 5900, 8080, 8443, 8888]

    print("\n" + "-" * 55)
    print("  localhost の代表的なポートをスキャンします")
    print("-" * 55)

    scan_ports("127.0.0.1", common_ports, timeout=0.3)


def interactive_mode():
    """対話モード: ユーザーが指定したポートをスキャンします"""
    print("\n" + "=" * 55)
    print("  【対話モード】ポートスキャン")
    print("=" * 55)
    print("\n  ╔═══════════════════════════════════════════════╗")
    print("  ║  注意: 自分が管理するマシンのみ対象にして     ║")
    print("  ║  ください。他者のサーバーへのスキャンは        ║")
    print("  ║  法律に抵触する可能性があります。              ║")
    print("  ╚═══════════════════════════════════════════════╝")

    while True:
        print("\n  操作を選んでください:")
        print("  1. localhost をクイックスキャン（主要ポート）")
        print("  2. localhost のポート範囲を指定してスキャン")
        print("  3. 特定ポートの情報を調べる")
        print("  4. ウェルノウンポート一覧を表示")
        print("  5. メニューに戻る")

        choice = input("\n  選択 (1-5): ").strip()

        if choice == "1":
            common = [21, 22, 25, 53, 80, 110, 143, 443, 445, 993,
                      995, 3000, 3306, 5432, 8080, 8443, 8888]
            scan_ports("127.0.0.1", common, timeout=0.3)

        elif choice == "2":
            try:
                start = int(input("  開始ポート番号 (例: 1): ").strip())
                end = int(input("  終了ポート番号 (例: 1024): ").strip())

                if start < 1 or end > 65535 or start > end:
                    print("  ※ 有効なポート範囲（1〜65535）を指定してください。")
                    continue

                port_count = end - start + 1
                if port_count > 1000:
                    print(f"  ※ {port_count}ポートのスキャンには時間がかかります。")
                    confirm = input("  続行しますか？ (y/n): ").strip().lower()
                    if confirm != "y":
                        continue

                ports = list(range(start, end + 1))
                scan_ports("127.0.0.1", ports, timeout=0.2)

            except ValueError:
                print("  ※ 有効な数値を入力してください。")

        elif choice == "3":
            try:
                port = int(input("  ポート番号を入力: ").strip())
                if 1 <= port <= 65535:
                    service = get_service_name(port)
                    is_open = scan_port("127.0.0.1", port, timeout=1.0)
                    print(f"\n  ポート {port}:")
                    print(f"    サービス:  {service}")
                    print(f"    状態:      {'OPEN（開いている）' if is_open else 'CLOSED（閉じている）'}")
                else:
                    print("  ※ 1〜65535 の範囲で入力してください。")
            except ValueError:
                print("  ※ 有効な数値を入力してください。")

        elif choice == "4":
            show_well_known_ports()

        elif choice == "5":
            break
        else:
            print("  ※ 1〜5 の数字を入力してください。")


# --- メインプログラム ---
if __name__ == "__main__":
    print("+" + "=" * 53 + "+")
    print("|        簡易ポートスキャナー（教育用）              |")
    print("|        〜 ポートとサービスの関係を学ぼう 〜        |")
    print("+" + "=" * 53 + "+")
    print()
    print("  ╔═══════════════════════════════════════════════╗")
    print("  ║  【注意】教育目的限定                          ║")
    print("  ║  自分が管理していないサーバーに対する            ║")
    print("  ║  ポートスキャンは法律に抵触する場合が           ║")
    print("  ║  あります。localhost のみで使用してください。   ║")
    print("  ╚═══════════════════════════════════════════════╝")

    # ポートの解説
    explain_ports()

    while True:
        print("\n  モードを選択してください:")
        print("  1. デモモード（localhostの主要ポートをスキャン）")
        print("  2. 対話モード（自分で指定）")
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
