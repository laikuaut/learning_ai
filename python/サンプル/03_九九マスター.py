# ==============================
# 九九マスタープログラム
# 第3章：繰り返しの総合サンプル
# ==============================
# 学べる内容:
#   - for ループ
#   - range() の使い方
#   - enumerate() でインデックス付きループ
#   - while ループ
#   - break / continue
#   - ネストしたループ（二重ループ）
# ==============================

# === 1. 九九の表（二重ループ + range）===
print("=== 九九の表 ===")
print("    ", end="")
for j in range(1, 10):
    print(f"{j:4d}", end="")
print()
print("   " + "-" * 36)

for i in range(1, 10):
    print(f"{i} |", end="")
    for j in range(1, 10):
        print(f"{i * j:4d}", end="")
    print()

print()

# === 2. FizzBuzz（for + if + continue）===
print("=== FizzBuzz (1-30) ===")
for i in range(1, 31):
    if i % 15 == 0:
        print("FizzBuzz", end=" ")
    elif i % 3 == 0:
        print("Fizz", end=" ")
    elif i % 5 == 0:
        print("Buzz", end=" ")
    else:
        print(i, end=" ")
print()
print()

# === 3. 素数を見つける（for-else + break）===
print("=== 1〜50の素数 ===")
primes = []
for num in range(2, 51):
    for i in range(2, num):
        if num % i == 0:
            break
    else:
        primes.append(num)

for i, prime in enumerate(primes, start=1):
    print(f"{prime:3d}", end="  ")
    if i % 10 == 0:
        print()
print(f"\n合計 {len(primes)} 個")
print()

# === 4. ピラミッド描画（for + range + 文字列演算）===
print("=== ピラミッド ===")
height = 7
for i in range(1, height + 1):
    spaces = " " * (height - i)
    stars = "*" * (2 * i - 1)
    print(spaces + stars)

print()

# === 5. 数当てゲーム（while + break）===
import random

print("=== 数当てゲーム ===")
print("1〜50の数を当ててください！")
answer = random.randint(1, 50)
attempts = 0
max_attempts = 7

while attempts < max_attempts:
    remaining = max_attempts - attempts
    guess = int(input(f"[残り{remaining}回] あなたの予想: "))
    attempts += 1

    if guess == answer:
        print(f"正解！ {attempts}回目で当たりました！")
        break
    elif guess > answer:
        print("もっと小さい！")
    else:
        print("もっと大きい！")
else:
    print(f"残念...正解は {answer} でした。")

print()

# === 6. カウントダウンタイマー風表示（while + range逆順）===
print("=== カウントダウン ===")
for i in range(5, 0, -1):
    print(f"  {i}...")
print("  スタート！")
