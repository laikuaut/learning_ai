# 実践課題11：ネットワーク設計課題 ─ 社内LAN構築 ★4

> **難易度**: ★★★★☆（上級）
> **前提知識**: 第1章〜第8章（全章）
> **課題の種類**: 設計課題
> **学習目標**: 中規模企業の社内LANを設計し、IPアドレス設計・サブネット分割・ルーティング・セキュリティの考慮を含む総合的なネットワーク設計力を養う

---

## 課題の説明

あなたは従業員100名の中規模企業のネットワーク管理者です。
以下の要件に基づいて社内LANを設計し、設計内容を **Pythonで検証するツール** を作成してください。

### 企業の要件

| 部署 | 人数 | 必要な接続機器 | 特記事項 |
|------|------|---------------|----------|
| 営業部 | 30名 | PC 30台 + プリンタ 2台 | 外部ネットワークへのアクセスが多い |
| 開発部 | 25名 | PC 25台 + 開発サーバ 5台 | 大容量通信、高セキュリティ |
| 総務部 | 20名 | PC 20台 + プリンタ 2台 | 一般的なオフィス利用 |
| 経理部 | 15名 | PC 15台 + プリンタ 1台 | 機密データ取り扱い、アクセス制限 |
| サーバ室 | - | Webサーバ 2台 + DBサーバ 2台 + ファイルサーバ 1台 | DMZ配置、冗長構成 |
| ゲスト用 | - | 最大20台 | 社内ネットワークから分離 |

### 設計要件

1. プライベートIPアドレス `172.16.0.0/16` の範囲を使用する
2. 各部署をサブネットで分離する
3. 将来の拡張性を考慮してアドレス空間に余裕を持たせる
4. サーバ室のWebサーバはDMZ（DeMilitarized Zone）として分離する
5. ゲスト用ネットワークは社内ネットワークから完全に分離する

---

## 完成イメージ

```
===== 社内LAN設計検証ツール =====

【ネットワーク構成図】
  インターネット
       │
    [ルータ/FW]
    ┌──┴──────────────────┐
    │                      │
  [DMZ SW]            [コアSW]
  172.16.0.0/28       ┌──┴──┬──────┬──────┐
  Web/公開サーバ    [分配SW] [分配SW] [分配SW]
                     │       │       │
                   営業部   開発部   総務部
                   /24      /25     /26

【IPアドレス設計表】
  サブネット名    CIDR表記          ホスト範囲                    ホスト数
  ─────────────────────────────────────────────────────────────────────
  DMZ            172.16.0.0/28     172.16.0.1 〜 172.16.0.14        14
  営業部         172.16.1.0/24     172.16.1.1 〜 172.16.1.254      254
  開発部         172.16.2.0/25     172.16.2.1 〜 172.16.2.126      126
  ...

【アドレス重複チェック】
  ✓ 全サブネットのアドレス範囲に重複はありません。
```

---

## 課題の要件

1. 各部署の必要ホスト数を満たすサブネットマスクを計算する
2. IPアドレス設計表を自動生成する
3. サブネット間のアドレス重複をチェックする
4. ネットワーク構成図をアスキーアートで表示する
5. 設計結果をファイルに保存する

---

## ステップガイド

<details>
<summary>ステップ1：必要ホスト数からプレフィックス長を計算する</summary>

必要ホスト数を収容できる最小のサブネットのプレフィックス長を求めます。

```python
import math

def calculate_prefix(required_hosts):
    """必要ホスト数を収容できるプレフィックス長を返す"""
    # ネットワークアドレスとブロードキャストを引く: 2^n - 2 >= required_hosts
    host_bits = math.ceil(math.log2(required_hosts + 2))
    prefix = 32 - host_bits
    return prefix
```

</details>

<details>
<summary>ステップ2：サブネットの自動割り当て</summary>

ベースアドレスから順にサブネットを割り当てます。大きいサブネットから先に割り当てるのがポイントです。

```python
def allocate_subnets(base_ip_int, departments):
    """大きい順にサブネットを割り当てる"""
    # 必要ホスト数の大きい順にソート
    sorted_depts = sorted(departments, key=lambda d: d["hosts"], reverse=True)
    current_address = base_ip_int
    # 各部署にサブネットを割り当て...
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```python
# 社内LAN設計検証ツール
# 学べる内容：サブネット設計、IPアドレス計画、ネットワーク設計
# 実行方法：python lan_designer.py

import math


def ip_to_int(ip_str):
    """IPアドレスを32ビット整数に変換する"""
    result = 0
    for octet in ip_str.split("."):
        result = result * 256 + int(octet)
    return result


def int_to_ip(ip_int):
    """32ビット整数をIPアドレスに変換する"""
    octets = []
    for i in range(3, -1, -1):
        octets.append(str((ip_int >> (8 * i)) & 0xFF))
    return ".".join(octets)


def calculate_prefix(required_hosts):
    """必要ホスト数を収容できるプレフィックス長を返す"""
    host_bits = math.ceil(math.log2(required_hosts + 2))
    prefix = 32 - host_bits
    return prefix


def calculate_subnet_info(network_int, prefix_len):
    """サブネット情報を計算する"""
    mask_int = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)
    host_count = broadcast_int - network_int - 1

    return {
        "network": int_to_ip(network_int),
        "broadcast": int_to_ip(broadcast_int),
        "host_min": int_to_ip(network_int + 1),
        "host_max": int_to_ip(broadcast_int - 1),
        "host_count": host_count,
        "prefix": prefix_len,
        "mask": int_to_ip(mask_int),
        "network_int": network_int,
        "broadcast_int": broadcast_int,
    }


def check_overlap(subnets):
    """サブネット間のアドレス重複をチェックする"""
    overlaps = []
    for i in range(len(subnets)):
        for j in range(i + 1, len(subnets)):
            a = subnets[i]
            b = subnets[j]
            # 範囲が重なるかチェック
            if a["network_int"] <= b["broadcast_int"] and b["network_int"] <= a["broadcast_int"]:
                overlaps.append((a["name"], b["name"]))
    return overlaps


# --- 部署データ ---
departments = [
    {"name": "DMZ（公開サーバ）", "hosts_needed": 10, "description": "Webサーバ・メールサーバ"},
    {"name": "営業部", "hosts_needed": 35, "description": "PC 30台 + プリンタ 2台 + 予備"},
    {"name": "開発部", "hosts_needed": 40, "description": "PC 25台 + 開発サーバ 5台 + 予備"},
    {"name": "総務部", "hosts_needed": 25, "description": "PC 20台 + プリンタ 2台 + 予備"},
    {"name": "経理部", "hosts_needed": 20, "description": "PC 15台 + プリンタ 1台 + 予備"},
    {"name": "サーバ室（内部）", "hosts_needed": 10, "description": "DBサーバ + ファイルサーバ"},
    {"name": "ゲストネットワーク", "hosts_needed": 25, "description": "ゲスト用Wi-Fi"},
    {"name": "管理用ネットワーク", "hosts_needed": 10, "description": "ネットワーク機器管理"},
]

# --- ベースアドレス ---
BASE_IP = "172.16.0.0"
base_ip_int = ip_to_int(BASE_IP)

# --- サブネットの割り当て ---
# 大きいサブネットから順に割り当てる
sorted_depts = sorted(departments, key=lambda d: d["hosts_needed"], reverse=True)

print("===== 社内LAN設計検証ツール =====")
print()

# サブネット計算
subnets = []
current_address = base_ip_int

for dept in sorted_depts:
    prefix = calculate_prefix(dept["hosts_needed"])
    subnet_size = 2 ** (32 - prefix)

    # アドレスをサブネットサイズの境界に揃える
    if current_address % subnet_size != 0:
        current_address = ((current_address // subnet_size) + 1) * subnet_size

    info = calculate_subnet_info(current_address, prefix)
    info["name"] = dept["name"]
    info["description"] = dept["description"]
    info["required"] = dept["hosts_needed"]
    subnets.append(info)

    current_address = info["broadcast_int"] + 1

# --- ネットワーク構成図 ---
print("【ネットワーク構成図】")
print()
print("  インターネット")
print("       │")
print("  [ルータ/ファイアウォール]")
print("    ┌──┴──────────────────────┐")
print("    │                          │")
print("  [DMZ SW]                 [コアSW]")

# DMZの表示
dmz = [s for s in subnets if "DMZ" in s["name"]]
if dmz:
    print(f"  {dmz[0]['network']}/{dmz[0]['prefix']}")

print("                           ┌──┴──┬──────┬──────┐")

# 各部署の表示
internal = [s for s in subnets if "DMZ" not in s["name"]]
names = [s["name"][:6] for s in internal[:4]]
print(f"                         {'  '.join(names)}")
print()

# --- IPアドレス設計表 ---
print("【IPアドレス設計表】")
header = f"  {'サブネット名':<20}{'CIDR表記':<22}{'ホスト範囲':<40}{'ホスト数':>8}{'必要数':>8}"
print(header)
print(f"  {'─' * 96}")

for subnet in subnets:
    cidr = f"{subnet['network']}/{subnet['prefix']}"
    host_range = f"{subnet['host_min']} 〜 {subnet['host_max']}"
    print(f"  {subnet['name']:<20}{cidr:<22}{host_range:<40}{subnet['host_count']:>8}{subnet['required']:>8}")

# 合計
total_hosts = sum(s["host_count"] for s in subnets)
total_required = sum(s["required"] for s in subnets)
print(f"  {'─' * 96}")
print(f"  {'合計':<20}{'':<22}{'':<40}{total_hosts:>8}{total_required:>8}")
print()

# --- アドレス空間の使用状況 ---
total_available = 2 ** 16  # /16 なので 65536
total_used = sum(2 ** (32 - s["prefix"]) for s in subnets)
usage_pct = total_used / total_available * 100

print("【アドレス空間使用状況】")
print(f"  割り当て済み : {total_used:,} / {total_available:,} アドレス ({usage_pct:.1f}%)")
bar_len = int(usage_pct / 2)
bar = "█" * bar_len + "░" * (50 - bar_len)
print(f"  [{bar}]")
print()

# --- アドレス重複チェック ---
print("【アドレス重複チェック】")
overlaps = check_overlap(subnets)
if overlaps:
    print("  ✗ アドレスの重複が検出されました:")
    for a, b in overlaps:
        print(f"    - {a} と {b}")
else:
    print("  ✓ 全サブネットのアドレス範囲に重複はありません。")
print()

# --- セキュリティゾーン ---
print("【セキュリティゾーン設計】")
zones = {
    "外部ゾーン（Internet）": "インターネット接続",
    "DMZゾーン": "公開サーバ（Webサーバ等）",
    "内部ゾーン（Trust）": "営業部、開発部、総務部、経理部",
    "サーバゾーン": "内部サーバ（DB、ファイルサーバ）",
    "ゲストゾーン": "ゲスト用（社内アクセス不可）",
    "管理ゾーン": "ネットワーク機器管理",
}
for zone, description in zones.items():
    print(f"  {zone:<25} : {description}")
print()

# --- ファイアウォールルール ---
print("【ファイアウォールルール（基本方針）】")
rules = [
    ("外部 → DMZ", "HTTP(80), HTTPS(443)のみ許可", "許可"),
    ("外部 → 内部", "すべて拒否", "拒否"),
    ("DMZ → 内部", "DBポート(3306,5432)のみ許可", "限定許可"),
    ("内部 → 外部", "HTTP, HTTPS, DNS許可", "許可"),
    ("内部 → DMZ", "管理ポートのみ許可", "限定許可"),
    ("ゲスト → 外部", "HTTP, HTTPSのみ許可", "許可"),
    ("ゲスト → 内部", "すべて拒否", "拒否"),
]
print(f"  {'通信方向':<18}{'ルール':<35}{'判定'}")
print(f"  {'─' * 60}")
for direction, rule, action in rules:
    print(f"  {direction:<18}{rule:<35}{action}")

# --- 結果をファイルに保存 ---
filename = "lan_design.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write("社内LAN設計書\n")
    f.write("=" * 60 + "\n\n")
    f.write("【IPアドレス設計表】\n")
    for subnet in subnets:
        cidr = f"{subnet['network']}/{subnet['prefix']}"
        f.write(f"  {subnet['name']:<20} {cidr:<22} ホスト数: {subnet['host_count']}\n")
    f.write(f"\n全サブネット重複なし: {'はい' if not overlaps else 'いいえ'}\n")

print(f"\n設計書を保存しました: {filename}")
```

</details>

<details>
<summary>解答例（改良版 ─ 対話式で部署を追加可能）</summary>

ユーザーが対話的に部署を追加・変更でき、設計を試行錯誤できるバージョンです。

```python
# 社内LAN設計検証ツール（改良版）
# 学べる内容：ネットワーク設計、サブネット最適化、対話型ツール
# 実行方法：python lan_designer_v2.py

import math


def ip_to_int(ip_str):
    result = 0
    for o in ip_str.split("."):
        result = result * 256 + int(o)
    return result


def int_to_ip(n):
    return ".".join(str((n >> (8 * i)) & 0xFF) for i in range(3, -1, -1))


def prefix_for_hosts(needed):
    """必要ホスト数からプレフィックス長を計算する"""
    bits = math.ceil(math.log2(needed + 2))
    return 32 - bits


def subnet_info(network_int, prefix):
    """サブネット情報を辞書で返す"""
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    bcast = network_int | (~mask & 0xFFFFFFFF)
    return {
        "network_int": network_int,
        "broadcast_int": bcast,
        "network": int_to_ip(network_int),
        "broadcast": int_to_ip(bcast),
        "first_host": int_to_ip(network_int + 1),
        "last_host": int_to_ip(bcast - 1),
        "hosts": bcast - network_int - 1,
        "prefix": prefix,
        "size": 2 ** (32 - prefix),
    }


def allocate(base_int, departments):
    """部署リストにサブネットを割り当てる"""
    sorted_depts = sorted(departments, key=lambda d: d["needed"], reverse=True)
    current = base_int
    results = []

    for dept in sorted_depts:
        prefix = prefix_for_hosts(dept["needed"])
        block_size = 2 ** (32 - prefix)

        # 境界に揃える
        if current % block_size != 0:
            current = ((current // block_size) + 1) * block_size

        info = subnet_info(current, prefix)
        info["name"] = dept["name"]
        info["needed"] = dept["needed"]
        results.append(info)
        current = info["broadcast_int"] + 1

    return results


def display_design(subnets, base_prefix=16):
    """設計結果を表示する"""
    print(f"\n{'=' * 80}")
    print(f"  {'サブネット名':<20}{'CIDR':<22}{'範囲':<36}{'ホスト':>6}{'必要':>6}")
    print(f"{'─' * 80}")
    for s in subnets:
        cidr = f"{s['network']}/{s['prefix']}"
        rng = f"{s['first_host']} 〜 {s['last_host']}"
        print(f"  {s['name']:<20}{cidr:<22}{rng:<36}{s['hosts']:>6}{s['needed']:>6}")

    total_space = 2 ** (32 - base_prefix)
    used = sum(s["size"] for s in subnets)
    pct = used / total_space * 100
    print(f"{'─' * 80}")
    print(f"  使用率: {used:,} / {total_space:,} ({pct:.1f}%)")
    print(f"{'=' * 80}")


def main():
    print("===== 社内LAN設計検証ツール（改良版） =====\n")

    departments = [
        {"name": "DMZ", "needed": 10},
        {"name": "営業部", "needed": 35},
        {"name": "開発部", "needed": 40},
        {"name": "総務部", "needed": 25},
        {"name": "経理部", "needed": 20},
        {"name": "サーバ室", "needed": 10},
        {"name": "ゲスト", "needed": 25},
        {"name": "管理用", "needed": 10},
    ]

    base_ip = "172.16.0.0"
    base_prefix = 16

    while True:
        print(f"\nベース: {base_ip}/{base_prefix}")
        print("1.設計表示  2.部署追加  3.部署削除  4.部署一覧  5.重複チェック  6.保存  7.終了")
        choice = input("操作: ").strip()

        if choice == "1":
            subnets = allocate(ip_to_int(base_ip), departments)
            display_design(subnets, base_prefix)

        elif choice == "2":
            name = input("部署名: ").strip()
            needed = int(input("必要ホスト数: ").strip())
            departments.append({"name": name, "needed": needed})
            print(f"'{name}'（{needed}ホスト）を追加しました。")

        elif choice == "3":
            for i, d in enumerate(departments):
                print(f"  {i + 1}. {d['name']} ({d['needed']}ホスト)")
            idx = int(input("削除番号: ").strip()) - 1
            if 0 <= idx < len(departments):
                removed = departments.pop(idx)
                print(f"'{removed['name']}' を削除しました。")

        elif choice == "4":
            print("\n【部署一覧】")
            for d in departments:
                prefix = prefix_for_hosts(d["needed"])
                print(f"  {d['name']:<20} 必要: {d['needed']:>4}  → /{prefix} ({2**(32-prefix)-2}ホスト)")

        elif choice == "5":
            subnets = allocate(ip_to_int(base_ip), departments)
            for i in range(len(subnets)):
                for j in range(i + 1, len(subnets)):
                    a, b = subnets[i], subnets[j]
                    if a["network_int"] <= b["broadcast_int"] and b["network_int"] <= a["broadcast_int"]:
                        print(f"  ✗ 重複: {a['name']} と {b['name']}")
                        break
                else:
                    continue
                break
            else:
                print("  ✓ 重複なし")

        elif choice == "6":
            subnets = allocate(ip_to_int(base_ip), departments)
            with open("lan_design.txt", "w", encoding="utf-8") as f:
                f.write("社内LAN設計書\n\n")
                for s in subnets:
                    f.write(f"{s['name']}: {s['network']}/{s['prefix']} (ホスト: {s['hosts']})\n")
            print("lan_design.txt に保存しました。")

        elif choice == "7":
            print("終了します。")
            break


if __name__ == "__main__":
    main()
```

**初心者向けとの違い:**
- 対話的に部署の追加・削除が可能で、設計を試行錯誤できる
- サブネットの割り当てロジックを `allocate()` 関数に集約
- メニュー方式でさまざまな操作に対応
- 部署一覧で推奨プレフィックス長を自動提案

</details>
