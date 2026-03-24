# ==============================
# パケット解析シミュレータ
# ネットワーク基礎：OSI参照モデルとパケット構造を体験するサンプル
# ==============================
# 学べる内容:
#   - OSI参照モデルの7階層の役割
#   - TCP/IPモデルとの対応関係
#   - 各層のヘッダ構造（イーサネット、IP、TCP、HTTP）
#   - カプセル化とデカプセル化の仕組み
#   - パケットの構造を視覚的に理解
#
# 実行方法:
#   python 05_パケット解析シミュレータ.py
#
# ※ 本プログラムは教育目的で作成されています
# ※ 実際のネットワークパケットを傍受するものではありません
# ==============================

import random
import struct
import binascii
import time


def explain_osi_model():
    """OSI参照モデルをアスキーアートで解説します"""
    print("""
  ┌──────────────────────────────────────────────────────────┐
  │              OSI参照モデル（7階層）                       │
  └──────────────────────────────────────────────────────────┘

  OSI参照モデル        TCP/IPモデル     プロトコル例
  ┌──────────────┐    ┌──────────────┐
  │ 第7層        │    │              │
  │ アプリケーション│    │ アプリケーション│   HTTP, SMTP, DNS
  ├──────────────┤    │              │
  │ 第6層        │    │              │   SSL/TLS, JPEG
  │ プレゼンテーション│  │              │
  ├──────────────┤    │              │
  │ 第5層        │    │              │   セッション管理
  │ セッション    │    │              │
  ├──────────────┤    ├──────────────┤
  │ 第4層        │    │ トランスポート │   TCP, UDP
  │ トランスポート │    │              │
  ├──────────────┤    ├──────────────┤
  │ 第3層        │    │ インターネット │   IP, ICMP
  │ ネットワーク  │    │              │
  ├──────────────┤    ├──────────────┤
  │ 第2層        │    │              │
  │ データリンク  │    │ ネットワーク   │   Ethernet, Wi-Fi
  ├──────────────┤    │ インターフェース│
  │ 第1層        │    │              │   電気信号, 光信号
  │ 物理         │    │              │
  └──────────────┘    └──────────────┘

  【カプセル化のイメージ】
  データを送信するとき、各層がヘッダを追加していきます:

  アプリケーション層:              [  HTTP データ  ]
  トランスポート層:        [TCP][  HTTP データ  ]
  ネットワーク層:      [IP][TCP][  HTTP データ  ]
  データリンク層:  [Eth][IP][TCP][  HTTP データ  ][FCS]

  受信側では逆順にヘッダを除去していきます（デカプセル化）。
    """)


def generate_mac_address():
    """ランダムなMACアドレスを生成します"""
    octets = [random.randint(0x00, 0xFF) for _ in range(6)]
    # ユニキャストアドレスにする（最下位ビットを0に）
    octets[0] = octets[0] & 0xFE
    return ":".join(f"{b:02X}" for b in octets)


def generate_ip_address(private=True):
    """ランダムなIPアドレスを生成します"""
    if private:
        return f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
    return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def create_ethernet_header(src_mac, dst_mac, ether_type=0x0800):
    """イーサネットヘッダを作成・表示します"""
    header = {
        "dst_mac": dst_mac,
        "src_mac": src_mac,
        "ether_type": ether_type,
    }

    ether_types = {
        0x0800: "IPv4",
        0x0806: "ARP",
        0x86DD: "IPv6",
        0x8100: "802.1Q VLAN",
    }

    print("  ┌─────────────────────────────────────────────────┐")
    print("  │  【第2層】イーサネットヘッダ (14バイト)          │")
    print("  ├─────────────────────────────────────────────────┤")
    print(f"  │  宛先MACアドレス:   {dst_mac:<20}  (6バイト)│")
    print(f"  │  送信元MACアドレス: {src_mac:<20}  (6バイト)│")
    print(f"  │  タイプ:           0x{ether_type:04X} "
          f"({ether_types.get(ether_type, '不明'):<14})  (2バイト)│")
    print("  └─────────────────────────────────────────────────┘")

    # バイナリ表現
    dst_bytes = dst_mac.replace(":", "")
    src_bytes = src_mac.replace(":", "")
    hex_repr = f"{dst_bytes} {src_bytes} {ether_type:04X}"
    print(f"  HEX: {hex_repr}")

    return header


def create_ip_header(src_ip, dst_ip, protocol=6, total_length=60):
    """IPヘッダを作成・表示します"""
    header = {
        "version": 4,
        "ihl": 5,  # ヘッダ長（32ビット単位）= 20バイト
        "tos": 0,
        "total_length": total_length,
        "identification": random.randint(0, 65535),
        "flags": 0x4000,  # Don't Fragment
        "ttl": 64,
        "protocol": protocol,
        "src_ip": src_ip,
        "dst_ip": dst_ip,
    }

    protocols = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
    }

    print("\n  ┌─────────────────────────────────────────────────┐")
    print("  │  【第3層】IPヘッダ (20バイト)                    │")
    print("  ├─────────────────────────────────────────────────┤")
    print(f"  │  バージョン:       IPv{header['version']}"
          f"                          │")
    print(f"  │  ヘッダ長:         {header['ihl'] * 4}バイト"
          f"                       │")
    print(f"  │  全長:             {total_length}バイト"
          f"                       │")
    print(f"  │  識別子:           0x{header['identification']:04X}"
          f"                       │")
    print(f"  │  TTL:              {header['ttl']}"
          f"                            │")
    print(f"  │  プロトコル:       {protocol} "
          f"({protocols.get(protocol, '不明'):<5})"
          f"                   │")
    print(f"  │  送信元IP:         {src_ip:<18}"
          f"              │")
    print(f"  │  宛先IP:           {dst_ip:<18}"
          f"              │")
    print("  └─────────────────────────────────────────────────┘")

    # TTLの説明
    print(f"  ※ TTL={header['ttl']}: ルーターを{header['ttl']}回通過するとパケットが破棄されます")

    return header


def create_tcp_header(src_port, dst_port, flags="SYN"):
    """TCPヘッダを作成・表示します"""
    seq_num = random.randint(0, 4294967295)
    ack_num = 0

    flag_bits = {
        "SYN": 0x02,
        "SYN-ACK": 0x12,
        "ACK": 0x10,
        "FIN": 0x01,
        "FIN-ACK": 0x11,
        "PSH-ACK": 0x18,
        "RST": 0x04,
    }

    flag_value = flag_bits.get(flags, 0)

    header = {
        "src_port": src_port,
        "dst_port": dst_port,
        "seq_num": seq_num,
        "ack_num": ack_num,
        "data_offset": 5,
        "flags": flags,
        "flag_value": flag_value,
        "window_size": 65535,
    }

    print("\n  ┌─────────────────────────────────────────────────┐")
    print("  │  【第4層】TCPヘッダ (20バイト)                   │")
    print("  ├─────────────────────────────────────────────────┤")
    print(f"  │  送信元ポート:     {src_port:<6}"
          f"                         │")
    print(f"  │  宛先ポート:       {dst_port:<6}"
          f"                         │")
    print(f"  │  シーケンス番号:   {seq_num:<12}"
          f"                   │")
    print(f"  │  確認応答番号:     {ack_num:<12}"
          f"                   │")
    print(f"  │  データオフセット: {header['data_offset'] * 4}バイト"
          f"                       │")
    print(f"  │  フラグ:           {flags} (0x{flag_value:02X})"
          f"                       │")
    print(f"  │  ウィンドウサイズ: {header['window_size']}"
          f"                        │")
    print("  └─────────────────────────────────────────────────┘")

    # フラグビットの視覚化
    print(f"  フラグビット: ", end="")
    flag_names = ["FIN", "SYN", "RST", "PSH", "ACK", "URG"]
    for i, name in enumerate(flag_names):
        bit = (flag_value >> i) & 1
        if bit:
            print(f"[{name}]", end=" ")
        else:
            print(f" {name} ", end=" ")
    print()

    return header


def create_http_data(method="GET", path="/index.html", host="www.example.com"):
    """HTTPリクエストデータを作成・表示します"""
    http_lines = [
        f"{method} {path} HTTP/1.1",
        f"Host: {host}",
        "User-Agent: Mozilla/5.0",
        "Accept: text/html",
        "Connection: keep-alive",
        "",
        "",
    ]
    http_data = "\r\n".join(http_lines)

    print("\n  ┌─────────────────────────────────────────────────┐")
    print("  │  【第7層】HTTPリクエスト（アプリケーションデータ）│")
    print("  ├─────────────────────────────────────────────────┤")
    for line in http_lines[:-2]:  # 空行を除く
        print(f"  │  {line:<47} │")
    print("  └─────────────────────────────────────────────────┘")
    print(f"  データサイズ: {len(http_data)}バイト")

    return http_data


def simulate_full_packet(src_ip=None, dst_ip=None, dst_port=80):
    """完全なパケットのカプセル化をシミュレーションします"""
    if src_ip is None:
        src_ip = generate_ip_address()
    if dst_ip is None:
        dst_ip = generate_ip_address(private=False)

    src_mac = generate_mac_address()
    dst_mac = generate_mac_address()
    src_port = random.randint(49152, 65535)

    print("\n" + "=" * 55)
    print("  パケット構造シミュレーション")
    print("  ─ HTTP GETリクエストのパケット ─")
    print("=" * 55)

    print(f"\n  送信元: {src_ip}:{src_port} ({src_mac})")
    print(f"  宛先:   {dst_ip}:{dst_port} ({dst_mac})")

    # 各層のヘッダを生成
    print("\n" + "─" * 55)
    print("  【カプセル化の過程】上位層 → 下位層")
    print("─" * 55)

    # 第7層: HTTPデータ
    http_data = create_http_data(host=dst_ip)

    # 第4層: TCPヘッダ
    tcp_header = create_tcp_header(src_port, dst_port, flags="PSH-ACK")

    # 第3層: IPヘッダ
    data_size = len(http_data.encode()) + 20 + 20
    ip_header = create_ip_header(src_ip, dst_ip, protocol=6, total_length=data_size)

    # 第2層: イーサネットヘッダ
    print()
    eth_header = create_ethernet_header(src_mac, dst_mac)

    # パケット全体のサイズ
    total_size = 14 + data_size  # イーサネット14 + IP全長
    print(f"\n  【パケット全体のサイズ】")
    print(f"  イーサネットヘッダ: 14バイト")
    print(f"  IPヘッダ:           20バイト")
    print(f"  TCPヘッダ:          20バイト")
    print(f"  HTTPデータ:         {len(http_data.encode())}バイト")
    print(f"  ─────────────────────────")
    print(f"  合計:               {total_size}バイト")

    # カプセル化の視覚化
    print(f"\n  【カプセル化の全体像】")
    print(f"  ┌─────────────────────────────────────────────────┐")
    print(f"  │ Ethernet │  IP  │  TCP  │     HTTP データ      │")
    print(f"  │  14bytes │ 20B  │  20B  │    {len(http_data.encode())}bytes"
          f"{'':>{18 - len(str(len(http_data.encode())))}}│")
    print(f"  └─────────────────────────────────────────────────┘")
    print(f"  ←───────── パケット全体: {total_size}バイト ─────────→")


def simulate_three_way_handshake():
    """TCP 3ウェイハンドシェイクをシミュレーションします"""
    src_ip = generate_ip_address()
    dst_ip = generate_ip_address(private=False)
    src_port = random.randint(49152, 65535)
    dst_port = 443

    print("\n" + "=" * 55)
    print("  TCP 3ウェイハンドシェイク シミュレーション")
    print("=" * 55)
    print(f"\n  クライアント: {src_ip}:{src_port}")
    print(f"  サーバー:     {dst_ip}:{dst_port}")

    # ステップ1: SYN
    print(f"\n  {'─' * 55}")
    print(f"  ステップ1: SYN（接続要求）")
    print(f"  {src_ip} ──── SYN ────→ {dst_ip}")
    print(f"  {'─' * 55}")
    seq1 = random.randint(0, 4294967295)
    print(f"  シーケンス番号: {seq1}")
    print(f"  フラグ: [SYN]")
    print(f"  「接続してもよいですか？」")
    time.sleep(0.5)

    # ステップ2: SYN-ACK
    print(f"\n  {'─' * 55}")
    print(f"  ステップ2: SYN+ACK（要求承認）")
    print(f"  {src_ip} ←── SYN+ACK ── {dst_ip}")
    print(f"  {'─' * 55}")
    seq2 = random.randint(0, 4294967295)
    print(f"  シーケンス番号: {seq2}")
    print(f"  確認応答番号:   {seq1 + 1}")
    print(f"  フラグ: [SYN] [ACK]")
    print(f"  「OKです。こちらからも接続要求します」")
    time.sleep(0.5)

    # ステップ3: ACK
    print(f"\n  {'─' * 55}")
    print(f"  ステップ3: ACK（確認応答）")
    print(f"  {src_ip} ──── ACK ────→ {dst_ip}")
    print(f"  {'─' * 55}")
    print(f"  シーケンス番号: {seq1 + 1}")
    print(f"  確認応答番号:   {seq2 + 1}")
    print(f"  フラグ: [ACK]")
    print(f"  「了解です。接続確立！」")
    time.sleep(0.3)

    print(f"\n  ✓ TCP接続が確立されました！")
    print(f"    以降、データの送受信が可能になります。")


def simulate_encapsulation_animation():
    """カプセル化のアニメーション表示をします"""
    print("\n" + "=" * 55)
    print("  カプセル化プロセスのアニメーション")
    print("=" * 55)

    steps = [
        ("第7層 アプリケーション", "[      HTTP データ      ]"),
        ("第4層 トランスポート",   "[TCP][      HTTP データ      ]"),
        ("第3層 ネットワーク",     "[ IP ][TCP][      HTTP データ      ]"),
        ("第2層 データリンク",     "[Eth][ IP ][TCP][      HTTP データ      ][FCS]"),
    ]

    print("\n  データが各層を通過してカプセル化されていきます:\n")

    for layer_name, packet_view in steps:
        print(f"  {layer_name}")
        print(f"  → {packet_view}")
        print()
        time.sleep(0.8)

    print("  " + "─" * 50)
    print("  受信側ではこの逆順でヘッダを除去します（デカプセル化）")

    print("\n  デカプセル化:\n")
    for layer_name, packet_view in reversed(steps):
        print(f"  {layer_name}")
        print(f"  ← {packet_view}")
        print()
        time.sleep(0.8)

    print("  元のHTTPデータが取り出されました！")


def demo_mode():
    """デモモード: パケット構造の解説と実例を表示します"""
    print("\n  ◆ 完全なパケット構造のシミュレーション")
    simulate_full_packet()

    print("\n\n  ◆ TCP 3ウェイハンドシェイク")
    simulate_three_way_handshake()

    print("\n\n  ◆ カプセル化プロセス")
    simulate_encapsulation_animation()


def interactive_mode():
    """対話モード: ユーザーがパラメータを指定してシミュレーションします"""
    print("\n" + "=" * 55)
    print("  【対話モード】パケット解析シミュレータ")
    print("=" * 55)

    while True:
        print("\n  操作を選んでください:")
        print("  1. パケット構造をシミュレーション")
        print("  2. TCP 3ウェイハンドシェイクを体験")
        print("  3. カプセル化プロセスをアニメーション表示")
        print("  4. 各層のヘッダを個別に確認")
        print("  5. メニューに戻る")

        choice = input("\n  選択 (1-5): ").strip()

        if choice == "1":
            print("\n  パケットのパラメータを設定します。")
            src = input("  送信元IP (空欄でランダム): ").strip()
            dst = input("  宛先IP (空欄でランダム): ").strip()
            port_str = input("  宛先ポート (空欄で80): ").strip()

            src_ip = src if src else None
            dst_ip = dst if dst else None
            dst_port = int(port_str) if port_str.isdigit() else 80

            simulate_full_packet(src_ip, dst_ip, dst_port)

        elif choice == "2":
            simulate_three_way_handshake()

        elif choice == "3":
            simulate_encapsulation_animation()

        elif choice == "4":
            print("\n  確認するヘッダを選んでください:")
            print("  a. イーサネットヘッダ（第2層）")
            print("  b. IPヘッダ（第3層）")
            print("  c. TCPヘッダ（第4層）")
            print("  d. HTTPデータ（第7層）")

            sub = input("\n  選択 (a-d): ").strip().lower()
            if sub == "a":
                create_ethernet_header(generate_mac_address(), generate_mac_address())
            elif sub == "b":
                create_ip_header(generate_ip_address(), generate_ip_address(False))
            elif sub == "c":
                flags_input = input("  TCPフラグ (SYN/SYN-ACK/ACK/FIN/PSH-ACK): ").strip()
                if flags_input not in ("SYN", "SYN-ACK", "ACK", "FIN", "PSH-ACK"):
                    flags_input = "SYN"
                create_tcp_header(
                    random.randint(49152, 65535), 80, flags=flags_input
                )
            elif sub == "d":
                create_http_data()
            else:
                print("  ※ a〜d のいずれかを入力してください。")

        elif choice == "5":
            break
        else:
            print("  ※ 1〜5 の数字を入力してください。")


# --- メインプログラム ---
if __name__ == "__main__":
    print("+" + "=" * 53 + "+")
    print("|        パケット解析シミュレータ                    |")
    print("|        〜 OSI参照モデルを体感しよう 〜             |")
    print("+" + "=" * 53 + "+")

    # OSI参照モデルの解説
    explain_osi_model()

    while True:
        print("\n  モードを選択してください:")
        print("  1. デモモード（全シミュレーションを実行）")
        print("  2. 対話モード（自分で選択）")
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
