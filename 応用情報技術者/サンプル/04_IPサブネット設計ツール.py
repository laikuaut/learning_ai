# ==============================
# IPサブネット設計ツール
# 応用情報技術者：ネットワーク
# ==============================
# 学べる内容:
#   - IPアドレスの構造（ネットワーク部とホスト部）
#   - サブネットマスクとCIDR表記
#   - サブネット分割の計算
#   - アドレスクラス（A/B/C）
#   - ブロードキャストアドレスとネットワークアドレス
#   - 利用可能ホスト数の計算
#   - VLSM（可変長サブネットマスク）による効率的なアドレス割り当て
#   - 応用情報技術者試験のネットワーク問題への対応力
#
# 実行方法:
#   python 04_IPサブネット設計ツール.py
# ==============================


def ip_to_binary(ip_str):
    """IPアドレスを2進数文字列に変換します"""
    octets = ip_str.strip().split(".")
    binary_parts = []
    for octet in octets:
        binary_parts.append(format(int(octet), "08b"))
    return ".".join(binary_parts)


def ip_to_int(ip_str):
    """IPアドレスを32ビット整数に変換します"""
    octets = ip_str.strip().split(".")
    result = 0
    for i, octet in enumerate(octets):
        result += int(octet) << (24 - 8 * i)
    return result


def int_to_ip(num):
    """32ビット整数をIPアドレス文字列に変換します"""
    return f"{(num >> 24) & 0xFF}.{(num >> 16) & 0xFF}.{(num >> 8) & 0xFF}.{num & 0xFF}"


def prefix_to_mask(prefix):
    """プレフィックス長をサブネットマスクに変換します"""
    if prefix == 0:
        return 0
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    return mask


def mask_to_prefix(mask_int):
    """サブネットマスク（整数）をプレフィックス長に変換します"""
    binary = format(mask_int, "032b")
    return binary.count("1")


def get_network_address(ip_int, mask_int):
    """ネットワークアドレスを計算します"""
    return ip_int & mask_int


def get_broadcast_address(ip_int, mask_int):
    """ブロードキャストアドレスを計算します"""
    wildcard = ~mask_int & 0xFFFFFFFF
    return (ip_int & mask_int) | wildcard


def get_host_count(prefix):
    """利用可能なホスト数を計算します"""
    if prefix >= 31:
        return 0 if prefix == 32 else 2
    return (2 ** (32 - prefix)) - 2


def get_address_class(ip_int):
    """IPアドレスのクラスを判定します"""
    first_octet = (ip_int >> 24) & 0xFF
    if first_octet < 128:
        return "A", 8, "0.0.0.0 - 127.255.255.255"
    elif first_octet < 192:
        return "B", 16, "128.0.0.0 - 191.255.255.255"
    elif first_octet < 224:
        return "C", 24, "192.0.0.0 - 223.255.255.255"
    elif first_octet < 240:
        return "D", None, "224.0.0.0 - 239.255.255.255 (マルチキャスト)"
    else:
        return "E", None, "240.0.0.0 - 255.255.255.255 (予約)"


def is_private(ip_int):
    """プライベートIPアドレスかどうか判定します"""
    first = (ip_int >> 24) & 0xFF
    second = (ip_int >> 16) & 0xFF

    # 10.0.0.0/8
    if first == 10:
        return True, "クラスA プライベート (10.0.0.0/8)"
    # 172.16.0.0/12
    if first == 172 and 16 <= second <= 31:
        return True, "クラスB プライベート (172.16.0.0/12)"
    # 192.168.0.0/16
    if first == 192 and second == 168:
        return True, "クラスC プライベート (192.168.0.0/16)"
    return False, "グローバルアドレス"


def analyze_ip(ip_str, prefix):
    """IPアドレスとサブネットを詳細に分析します"""
    ip_int = ip_to_int(ip_str)
    mask_int = prefix_to_mask(prefix)
    network_int = get_network_address(ip_int, mask_int)
    broadcast_int = get_broadcast_address(ip_int, mask_int)
    host_count = get_host_count(prefix)
    addr_class, default_prefix, class_range = get_address_class(ip_int)
    is_priv, priv_desc = is_private(ip_int)

    print(f"\n  {'='*55}")
    print(f"  IPアドレス分析: {ip_str}/{prefix}")
    print(f"  {'='*55}")

    # 基本情報
    print(f"\n  ■ 基本情報")
    print(f"    IPアドレス:           {ip_str}")
    print(f"    サブネットマスク:     {int_to_ip(mask_int)}")
    print(f"    CIDR表記:             {ip_str}/{prefix}")
    print(f"    アドレスクラス:       クラス{addr_class} ({class_range})")
    print(f"    種別:                 {priv_desc}")

    # 2進数表現
    print(f"\n  ■ 2進数表現")
    ip_bin = format(ip_int, "032b")
    mask_bin = format(mask_int, "032b")

    # ネットワーク部とホスト部を分けて表示します
    ip_network = ip_bin[:prefix]
    ip_host = ip_bin[prefix:]
    print(f"    IPアドレス:   {ip_bin[:8]}.{ip_bin[8:16]}.{ip_bin[16:24]}.{ip_bin[24:]}")
    print(f"    サブネット:   {mask_bin[:8]}.{mask_bin[8:16]}.{mask_bin[16:24]}.{mask_bin[24:]}")
    print(f"    ネットワーク部: {ip_network} ({prefix}ビット)")
    print(f"    ホスト部:       {'':>{prefix}}{ip_host} ({32-prefix}ビット)")

    # アドレス範囲
    if host_count > 0:
        first_host = network_int + 1
        last_host = broadcast_int - 1
    else:
        first_host = network_int
        last_host = broadcast_int

    print(f"\n  ■ アドレス範囲")
    print(f"    ネットワークアドレス:   {int_to_ip(network_int)}")
    if host_count > 0:
        print(f"    最初のホスト:           {int_to_ip(first_host)}")
        print(f"    最後のホスト:           {int_to_ip(last_host)}")
    print(f"    ブロードキャスト:       {int_to_ip(broadcast_int)}")
    print(f"    利用可能ホスト数:       {host_count:,}")
    print(f"    総アドレス数:           {2**(32-prefix):,}")

    return {
        "network": network_int,
        "broadcast": broadcast_int,
        "host_count": host_count,
        "mask": mask_int,
    }


def subnet_division(network_str, original_prefix, new_prefix):
    """サブネット分割を行います"""
    if new_prefix <= original_prefix:
        print("  ※ 分割後のプレフィックスは元より大きい必要があります。")
        return

    network_int = ip_to_int(network_str)
    mask_int = prefix_to_mask(original_prefix)
    network_int = get_network_address(network_int, mask_int)

    num_subnets = 2 ** (new_prefix - original_prefix)
    subnet_size = 2 ** (32 - new_prefix)
    hosts_per_subnet = get_host_count(new_prefix)

    print(f"\n  ━━━ サブネット分割 ━━━")
    print(f"  元のネットワーク: {int_to_ip(network_int)}/{original_prefix}")
    print(f"  分割後のプレフィックス: /{new_prefix}")
    print(f"  サブネット数: {num_subnets}")
    print(f"  各サブネットのホスト数: {hosts_per_subnet}")
    print()

    print(f"    {'#':>3} {'ネットワーク':<20} {'範囲':<35} {'ホスト数':>8}")
    print("    " + "-" * 70)

    for i in range(min(num_subnets, 32)):  # 最大32件表示
        sub_network = network_int + i * subnet_size
        sub_broadcast = sub_network + subnet_size - 1

        if hosts_per_subnet > 0:
            first_host = int_to_ip(sub_network + 1)
            last_host = int_to_ip(sub_broadcast - 1)
            range_str = f"{first_host} - {last_host}"
        else:
            range_str = "ポイントツーポイント"

        print(f"    {i+1:>3} {int_to_ip(sub_network) + '/' + str(new_prefix):<20} "
              f"{range_str:<35} {hosts_per_subnet:>8}")

    if num_subnets > 32:
        print(f"    ... 他 {num_subnets - 32} サブネット")


def vlsm_design(network_str, prefix, requirements):
    """VLSM（可変長サブネットマスク）による効率的なアドレス設計を行います

    requirements: [(名前, 必要ホスト数), ...] のリスト
    """
    print(f"\n  ━━━ VLSM設計 ━━━")
    print(f"  ネットワーク: {network_str}/{prefix}")
    print(f"  総アドレス数: {2**(32-prefix):,}")

    # 必要ホスト数が大きい順にソートします
    sorted_reqs = sorted(requirements, key=lambda x: x[1], reverse=True)

    print(f"\n  ■ 要件（必要ホスト数の大きい順に割り当てます）")
    for name, hosts in sorted_reqs:
        # 必要なプレフィックスを計算します
        import math
        host_bits = math.ceil(math.log2(hosts + 2))  # +2: ネットワーク+ブロードキャスト
        needed_prefix = 32 - host_bits
        actual_hosts = 2 ** host_bits - 2
        print(f"    {name}: {hosts}ホスト → /{needed_prefix} ({actual_hosts}ホスト利用可能)")

    # 割り当て実行
    print(f"\n  ■ アドレス割り当て結果")
    print(f"    {'部門/用途':<16} {'必要':>6} {'実際':>6} {'ネットワーク':<20} {'範囲'}")
    print("    " + "-" * 78)

    current_addr = ip_to_int(network_str)
    max_addr = current_addr + 2 ** (32 - prefix)
    total_used = 0

    for name, hosts in sorted_reqs:
        import math
        host_bits = math.ceil(math.log2(hosts + 2))
        needed_prefix = 32 - host_bits
        subnet_size = 2 ** host_bits
        actual_hosts = subnet_size - 2

        # アドレスのアライメント（サブネット境界に合わせます）
        if current_addr % subnet_size != 0:
            current_addr = ((current_addr // subnet_size) + 1) * subnet_size

        if current_addr + subnet_size > max_addr:
            print(f"    {name:<16} ※ アドレス不足！割り当てできません。")
            continue

        network = current_addr
        broadcast = current_addr + subnet_size - 1
        first_host = int_to_ip(network + 1)
        last_host = int_to_ip(broadcast - 1)

        print(f"    {name:<16} {hosts:>6} {actual_hosts:>6} "
              f"{int_to_ip(network) + '/' + str(needed_prefix):<20} "
              f"{first_host} - {last_host}")

        current_addr += subnet_size
        total_used += subnet_size

    total_available = 2 ** (32 - prefix)
    unused = total_available - total_used
    utilization = (total_used / total_available) * 100
    print(f"\n  ■ 利用状況")
    print(f"    総アドレス数: {total_available:,}")
    print(f"    使用アドレス数: {total_used:,}")
    print(f"    未使用アドレス数: {unused:,}")
    print(f"    利用率: {utilization:.1f}%")


def show_subnet_table():
    """よく使うサブネットの一覧表を表示します"""
    print("\n  ■ サブネットマスク一覧（試験で頻出！）")
    print(f"    {'CIDR':>5} {'サブネットマスク':<18} {'ホスト数':>10} {'用途例'}")
    print("    " + "-" * 56)

    entries = [
        (8, "クラスA デフォルト"),
        (16, "クラスB デフォルト"),
        (20, "大規模サブネット"),
        (22, "中規模サブネット"),
        (24, "クラスC デフォルト"),
        (25, "サブネット分割例"),
        (26, "中小規模"),
        (27, "小規模オフィス"),
        (28, "小規模ネットワーク"),
        (29, "ポイントツーポイント+"),
        (30, "ポイントツーポイント"),
        (32, "ホストルート"),
    ]

    for prefix, usage in entries:
        mask = prefix_to_mask(prefix)
        hosts = get_host_count(prefix)
        print(f"    /{prefix:<4} {int_to_ip(mask):<18} {hosts:>10,} {usage}")


# ============================================================
# 対話モード
# ============================================================

def interactive_mode():
    """対話型のIPサブネット設計ツールです"""
    print("\n" + "=" * 55)
    print("  IPサブネット設計ツール - 対話モード")
    print("=" * 55)
    print("  操作を選んでください:")
    print("    1. IPアドレスを分析")
    print("    2. サブネット分割")
    print("    3. VLSM設計")
    print("    4. サブネットマスク一覧")
    print("    5. IP → 2進数変換")
    print("    0. 終了")
    print("-" * 55)

    while True:
        choice = input("\n  選択 (0-5): ").strip()

        if choice == "0":
            print("  IPサブネット設計ツールを終了します。")
            break

        elif choice == "1":
            ip_input = input("  IPアドレス（CIDR表記、例: 192.168.1.100/24）: ").strip()
            try:
                if "/" in ip_input:
                    ip, prefix = ip_input.split("/")
                    prefix = int(prefix)
                else:
                    ip = ip_input
                    prefix = int(input("  プレフィックス長 (例: 24): "))

                if prefix < 0 or prefix > 32:
                    print("  ※ プレフィックスは0-32の範囲で入力してください。")
                    continue

                analyze_ip(ip, prefix)
            except (ValueError, IndexError):
                print("  ※ 正しい形式で入力してください。例: 192.168.1.0/24")

        elif choice == "2":
            try:
                network = input("  ネットワーク（例: 192.168.1.0）: ").strip()
                orig_prefix = int(input("  元のプレフィックス長: "))
                new_prefix = int(input("  分割後のプレフィックス長: "))
                subnet_division(network, orig_prefix, new_prefix)
            except ValueError:
                print("  ※ 正しい値を入力してください。")

        elif choice == "3":
            try:
                network = input("  ネットワーク（例: 192.168.10.0）: ").strip()
                prefix = int(input("  プレフィックス長（例: 24）: "))

                reqs = []
                print("  各部門の必要ホスト数を入力します（空行で終了）:")
                while True:
                    name = input("    部門名: ").strip()
                    if not name:
                        break
                    hosts = int(input(f"    {name} の必要ホスト数: "))
                    reqs.append((name, hosts))

                if reqs:
                    vlsm_design(network, prefix, reqs)
            except ValueError:
                print("  ※ 正しい値を入力してください。")

        elif choice == "4":
            show_subnet_table()

        elif choice == "5":
            ip = input("  IPアドレス（例: 192.168.1.1）: ").strip()
            try:
                binary = ip_to_binary(ip)
                print(f"  {ip} → {binary}")
            except (ValueError, IndexError):
                print("  ※ 正しいIPアドレスを入力してください。")

        else:
            print("  ※ 0-5の番号を入力してください。")


# === デモンストレーション ===
print("=" * 55)
print("  IPサブネット設計ツール")
print("  ～ サブネットの計算を完全マスターしよう ～")
print("=" * 55)

# --- デモ1: IPアドレスの分析 ---
print("\n━━━ デモ1: IPアドレスの分析 ━━━")
demo_ips = [
    ("192.168.1.100", 24),
    ("10.0.0.50", 8),
    ("172.16.10.200", 20),
]
for ip, prefix in demo_ips:
    analyze_ip(ip, prefix)

# --- デモ2: サブネットマスク一覧 ---
show_subnet_table()

# --- デモ3: サブネット分割 ---
print("\n\n━━━ デモ3: サブネット分割 ━━━")
print("  192.168.1.0/24 を /26 に分割します")
print("  → 4つのサブネットに分かれます (2^(26-24) = 4)")
subnet_division("192.168.1.0", 24, 26)

print("\n  10.0.0.0/8 を /16 に分割します")
print("  → 256個のサブネットに分かれます (2^(16-8) = 256)")
subnet_division("10.0.0.0", 8, 16)

# --- デモ4: VLSM設計 ---
print("\n\n━━━ デモ4: VLSM設計 ━━━")
print("  ある会社のネットワーク設計:")
print("  使用可能: 192.168.10.0/24 (254ホスト)")
requirements = [
    ("営業部", 50),
    ("開発部", 100),
    ("人事部", 20),
    ("サーバ室", 10),
    ("管理用", 5),
]
for name, hosts in requirements:
    print(f"    {name}: {hosts}ホスト必要")

vlsm_design("192.168.10.0", 24, requirements)

# --- 試験ポイント ---
print("""

━━━ 試験頻出ポイント ━━━

  ■ IPアドレスの計算手順
    1. IPアドレスとサブネットマスクをANDする → ネットワークアドレス
    2. サブネットマスクを反転する → ワイルドカードマスク
    3. ネットワークアドレス OR ワイルドカードマスク → ブロードキャスト
    4. ホスト数 = 2^(32-プレフィックス) - 2

  ■ よく出る計算
    /24 → 254ホスト (256 - 2)
    /25 → 126ホスト (128 - 2)
    /26 → 62ホスト  (64 - 2)
    /27 → 30ホスト  (32 - 2)
    /28 → 14ホスト  (16 - 2)

  ■ プライベートIPアドレス範囲（暗記必須！）
    クラスA: 10.0.0.0/8        (10.0.0.0 - 10.255.255.255)
    クラスB: 172.16.0.0/12     (172.16.0.0 - 172.31.255.255)
    クラスC: 192.168.0.0/16    (192.168.0.0 - 192.168.255.255)

  ■ -2 の理由
    - ネットワークアドレス（ホスト部が全て0）→ ネットワーク自体を示します
    - ブロードキャストアドレス（ホスト部が全て1）→ 全ホスト宛を示します
""")

# --- 対話モード ---
interactive_mode()
