# ==============================
# IPアドレス計算ツール
# ネットワーク基礎：IPアドレスとサブネットの総合サンプル
# ==============================
# 学べる内容:
#   - IPアドレスのクラス判定（クラスA〜E）
#   - サブネットマスクとCIDR表記の相互変換
#   - ネットワークアドレス・ブロードキャストアドレスの計算
#   - 利用可能なホスト数の算出
#   - ビット演算（AND, OR, NOT）の実践的な活用
#
# 実行方法:
#   python 01_IPアドレス計算ツール.py
#
# ※ 本プログラムは教育目的で作成されています
# ==============================

import ipaddress


def ip_to_binary(ip_str):
    """IPアドレスを2進数表記に変換します"""
    octets = ip_str.split(".")
    binary_parts = []
    for octet in octets:
        binary_parts.append(format(int(octet), "08b"))
    return ".".join(binary_parts)


def classify_ip(ip_str):
    """IPアドレスのクラスを判定します（クラスフルアドレッシング）"""
    first_octet = int(ip_str.split(".")[0])

    if 1 <= first_octet <= 126:
        return "A", "255.0.0.0", 8
    elif 128 <= first_octet <= 191:
        return "B", "255.255.0.0", 16
    elif 192 <= first_octet <= 223:
        return "C", "255.255.255.0", 24
    elif 224 <= first_octet <= 239:
        return "D（マルチキャスト）", "なし", 0
    elif 240 <= first_octet <= 255:
        return "E（実験用）", "なし", 0
    else:
        return "特殊（ループバック等）", "なし", 0


def check_private_ip(ip_str):
    """プライベートIPアドレスかどうか判定します"""
    # RFC 1918 で定義されたプライベートアドレス範囲
    private_ranges = [
        ("10.0.0.0", "10.255.255.255", "クラスA プライベート"),
        ("172.16.0.0", "172.31.255.255", "クラスB プライベート"),
        ("192.168.0.0", "192.168.255.255", "クラスC プライベート"),
    ]

    ip_int = int(ipaddress.IPv4Address(ip_str))

    for start, end, label in private_ranges:
        start_int = int(ipaddress.IPv4Address(start))
        end_int = int(ipaddress.IPv4Address(end))
        if start_int <= ip_int <= end_int:
            return True, label
    return False, "グローバルIPアドレス"


def calculate_subnet(ip_str, prefix_length):
    """サブネット計算を行います"""
    # ipaddress モジュールで計算
    network = ipaddress.IPv4Network(f"{ip_str}/{prefix_length}", strict=False)

    # 手動でも計算してみましょう（学習用）
    ip_int = int(ipaddress.IPv4Address(ip_str))
    mask_int = (0xFFFFFFFF << (32 - prefix_length)) & 0xFFFFFFFF

    # ネットワークアドレス = IPアドレス AND サブネットマスク
    network_addr_int = ip_int & mask_int
    # ブロードキャストアドレス = ネットワークアドレス OR (NOT サブネットマスク)
    broadcast_int = network_addr_int | (~mask_int & 0xFFFFFFFF)

    network_addr = str(ipaddress.IPv4Address(network_addr_int))
    broadcast_addr = str(ipaddress.IPv4Address(broadcast_int))
    subnet_mask = str(ipaddress.IPv4Address(mask_int))

    # ホスト数の計算
    host_bits = 32 - prefix_length
    total_hosts = 2 ** host_bits
    usable_hosts = total_hosts - 2 if total_hosts > 2 else 0

    return {
        "network_addr": network_addr,
        "broadcast_addr": broadcast_addr,
        "subnet_mask": subnet_mask,
        "prefix_length": prefix_length,
        "total_addresses": total_hosts,
        "usable_hosts": usable_hosts,
        "first_host": str(ipaddress.IPv4Address(network_addr_int + 1)) if usable_hosts > 0 else "なし",
        "last_host": str(ipaddress.IPv4Address(broadcast_int - 1)) if usable_hosts > 0 else "なし",
    }


def display_ip_info(ip_str):
    """IPアドレスの詳細情報を表示します"""
    print("\n" + "=" * 55)
    print(f"  IPアドレス情報: {ip_str}")
    print("=" * 55)

    # 2進数表記
    binary = ip_to_binary(ip_str)
    print(f"\n  2進数表記:   {binary}")

    # クラス判定
    ip_class, default_mask, default_prefix = classify_ip(ip_str)
    print(f"  IPクラス:    クラス{ip_class}")
    if default_mask != "なし":
        print(f"  デフォルトマスク: {default_mask} (/{default_prefix})")

    # プライベートIP判定
    is_private, label = check_private_ip(ip_str)
    print(f"  種別:        {label}")
    if is_private:
        print("               ※ インターネットに直接接続できないアドレスです")

    # 特殊アドレスのチェック
    ip_obj = ipaddress.IPv4Address(ip_str)
    if ip_obj.is_loopback:
        print("  ※ ループバックアドレス（自分自身を指します）")
    if ip_obj.is_link_local:
        print("  ※ リンクローカルアドレス（DHCP取得失敗時など）")


def display_subnet_info(ip_str, prefix):
    """サブネット計算結果を表示します"""
    result = calculate_subnet(ip_str, prefix)

    print("\n" + "-" * 55)
    print(f"  サブネット計算結果 ({ip_str}/{prefix})")
    print("-" * 55)
    print(f"  サブネットマスク:      {result['subnet_mask']} (/{result['prefix_length']})")
    print(f"  ネットワークアドレス:  {result['network_addr']}")
    print(f"  ブロードキャストアドレス: {result['broadcast_addr']}")
    print(f"  利用可能ホスト範囲:    {result['first_host']} 〜 {result['last_host']}")
    print(f"  総アドレス数:          {result['total_addresses']}")
    print(f"  利用可能ホスト数:      {result['usable_hosts']}")

    # ビット演算の過程を視覚化
    print("\n  【ビット演算の過程】")
    print(f"  IPアドレス:      {ip_to_binary(ip_str)}")
    print(f"  サブネットマスク:  {ip_to_binary(result['subnet_mask'])}")
    print(f"  ─────────────── AND ───────────────")
    print(f"  ネットワーク:    {ip_to_binary(result['network_addr'])}")


def demo_mode():
    """デモモード: 代表的なIPアドレスで計算例を表示します"""
    print("\n" + "=" * 55)
    print("  【デモモード】代表的なIPアドレスの計算例")
    print("=" * 55)

    examples = [
        ("192.168.1.100", 24, "一般家庭でよく使われるアドレス"),
        ("10.0.0.50", 8, "大規模ネットワーク（クラスA プライベート）"),
        ("172.16.10.200", 20, "中規模ネットワーク（サブネット分割例）"),
        ("192.168.100.1", 28, "小規模サブネット分割（/28 = 14台）"),
    ]

    for ip, prefix, description in examples:
        print(f"\n  ◆ {description}")
        display_ip_info(ip)
        display_subnet_info(ip, prefix)
        print()


def interactive_mode():
    """対話モード: ユーザーがIPアドレスを入力して計算します"""
    print("\n" + "=" * 55)
    print("  【対話モード】IPアドレスを入力して計算します")
    print("=" * 55)

    while True:
        print("\n  操作を選んでください:")
        print("  1. IPアドレスの情報を表示")
        print("  2. サブネット計算")
        print("  3. CIDR表記からサブネットマスクに変換")
        print("  4. メニューに戻る")

        choice = input("\n  選択 (1-4): ").strip()

        if choice == "1":
            ip_input = input("  IPアドレスを入力 (例: 192.168.1.1): ").strip()
            try:
                ipaddress.IPv4Address(ip_input)
                display_ip_info(ip_input)
            except ipaddress.AddressValueError:
                print("  ※ 無効なIPアドレスです。正しい形式で入力してください。")

        elif choice == "2":
            ip_input = input("  IPアドレスを入力 (例: 192.168.1.100): ").strip()
            prefix_input = input("  プレフィックス長を入力 (例: 24): ").strip()
            try:
                ipaddress.IPv4Address(ip_input)
                prefix = int(prefix_input)
                if not 0 <= prefix <= 32:
                    raise ValueError
                display_ip_info(ip_input)
                display_subnet_info(ip_input, prefix)
            except (ipaddress.AddressValueError, ValueError):
                print("  ※ 入力が正しくありません。IPアドレスとプレフィックス長を確認してください。")

        elif choice == "3":
            prefix_input = input("  CIDR プレフィックス長を入力 (例: 24): ").strip()
            try:
                prefix = int(prefix_input)
                if not 0 <= prefix <= 32:
                    raise ValueError
                mask_int = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
                mask_str = str(ipaddress.IPv4Address(mask_int))
                print(f"\n  /{prefix} → サブネットマスク: {mask_str}")
                print(f"  2進数: {ip_to_binary(mask_str)}")
                host_bits = 32 - prefix
                print(f"  ホストビット数: {host_bits}")
                print(f"  利用可能ホスト数: {2 ** host_bits - 2 if host_bits > 1 else 0}")
            except ValueError:
                print("  ※ 0〜32 の整数を入力してください。")

        elif choice == "4":
            break
        else:
            print("  ※ 1〜4 の数字を入力してください。")


# --- メインプログラム ---
if __name__ == "__main__":
    print("+" + "=" * 53 + "+")
    print("|        IPアドレス計算ツール                       |")
    print("|        〜 ネットワークの基礎を体験しよう 〜       |")
    print("+" + "=" * 53 + "+")

    while True:
        print("\n  モードを選択してください:")
        print("  1. デモモード（計算例を表示）")
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
