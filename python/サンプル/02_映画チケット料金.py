# ==============================
# 映画チケット料金計算プログラム
# 第2章：条件分岐の総合サンプル
# ==============================
# 学べる内容:
#   - if / elif / else
#   - 比較演算子（<, <=, >=, ==）
#   - 論理演算子（and, or, not）
#   - in 演算子
#   - 三項演算子
#   - ネストした条件分岐
# ==============================

# --- 入力データ ---
age = 15
is_member = True
day = "水"
show_time = 18  # 18時の上映

# --- 基本料金の決定（if-elif-else）---
if age < 4:
    base_price = 0
    category = "幼児（無料）"
elif age <= 12:
    base_price = 800
    category = "子ども"
elif age <= 18:
    base_price = 1200
    category = "中高生"
elif age >= 65:
    base_price = 1100
    category = "シニア"
else:
    base_price = 1800
    category = "一般"

# --- 割引の適用（論理演算子）---
discount = 0
discount_reasons = []

# 会員割引（and）
if is_member and base_price > 0:
    discount += 200
    discount_reasons.append("会員割引 -200円")

# 水曜サービスデー（比較演算子）
if day == "水":
    discount += 200
    discount_reasons.append("水曜サービスデー -200円")

# レイトショー割引（and）
if show_time >= 20 and base_price > 0:
    discount += 300
    discount_reasons.append("レイトショー -300円")

# --- 最終金額の計算 ---
final_price = max(base_price - discount, 0)

# --- 結果表示 ---
print("映画チケット料金計算")
print("=" * 35)
print(f"年齢:     {age}歳（{category}）")
print(f"会員:     {'はい' if is_member else 'いいえ'}")
print(f"曜日:     {day}曜日")
print(f"上映時間: {show_time}:00")
print("-" * 35)
print(f"基本料金: {base_price}円")

if discount_reasons:
    print("適用割引:")
    for reason in discount_reasons:
        print(f"  ・{reason}")
else:
    print("適用割引: なし")

print("-" * 35)
print(f"お支払い: {final_price}円")

# --- 一言メッセージ（in演算子・三項演算子）---
if day in ["土", "日"]:
    print("\n※ 週末は混雑が予想されます。お早めにどうぞ！")
else:
    msg = "お得にご覧いただけます！" if discount > 0 else "映画をお楽しみください！"
    print(f"\n{msg}")

# --- 対話版 ---
print()
print("=== あなたの料金を計算します ===")
your_age = int(input("年齢: "))
your_member = input("会員ですか？(y/n): ").lower() == "y"
your_day = input("曜日（月/火/水/木/金/土/日）: ")

if your_age < 4:
    price = 0
elif your_age <= 12:
    price = 800
elif your_age <= 18:
    price = 1200
elif your_age >= 65:
    price = 1100
else:
    price = 1800

if your_member and price > 0:
    price -= 200
if your_day == "水":
    price -= 200

price = max(price, 0)
print(f"\nあなたの料金: {price}円")
