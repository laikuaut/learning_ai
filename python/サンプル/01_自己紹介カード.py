# ==============================
# 自己紹介カード生成プログラム
# 第1章：変数とデータ型の総合サンプル
# ==============================
# 学べる内容:
#   - 変数の作成と代入
#   - データ型（int, float, str, bool）
#   - 算術演算子（+, -, *, /, **）
#   - 型変換（int(), str(), float()）
#   - f文字列による出力
#   - type() で型の確認
# ==============================

# --- 変数とデータ型 ---
name = "Python太郎"          # str（文字列）
age = 20                      # int（整数）
height = 170.5                # float（浮動小数点数）
is_student = True             # bool（真偽値）

# --- 型の確認 ---
print("=== データ型の確認 ===")
print(f"name       → {type(name)}")
print(f"age        → {type(age)}")
print(f"height     → {type(height)}")
print(f"is_student → {type(is_student)}")
print()

# --- 演算 ---
birth_year = 2026 - age            # 引き算
bmi = 65 / (height / 100) ** 2     # 割り算・べき乗
months_lived = age * 12             # 掛け算

# --- 型変換 ---
age_str = str(age)                  # int → str
height_int = int(height)            # float → int（小数切り捨て）

# --- f文字列で出力 ---
print("+" + "-" * 30 + "+")
print("|     自己紹介カード          |")
print("+" + "-" * 30 + "+")
print(f"| 名前:   {name}")
print(f"| 年齢:   {age}歳（{birth_year}年生まれ）")
print(f"| 身長:   {height}cm（約{height_int}cm）")
print(f"| 学生:   {'はい' if is_student else 'いいえ'}")
print(f"| BMI:    {bmi:.1f}")
print(f"| 生きた月数: 約{months_lived}ヶ月")
print("+" + "-" * 30 + "+")

# --- 文字列の連結 ---
print()
message = name + "さんは" + age_str + "歳です"
print("文字列連結:", message)
print(f"f文字列:   {name}さんは{age}歳です")  # こちらの方が便利！

# --- input() を使った対話版 ---
print()
print("=== あなたのカードも作りましょう！ ===")
your_name = input("名前を入力してください: ")
your_age = int(input("年齢を入力してください: "))
your_height = float(input("身長(cm)を入力してください: "))

your_birth = 2026 - your_age
your_bmi = 65 / (your_height / 100) ** 2

print()
print(f"名前: {your_name}")
print(f"年齢: {your_age}歳（{your_birth}年生まれ）")
print(f"BMI:  {your_bmi:.1f}")
