# 実践課題02：稼働率とMTBF/MTTR計算 ★1

> **難易度**: ★☆☆☆☆（入門）
> **前提知識**: 第1章（応用数学と離散数学）、第2章（システムアーキテクチャ）
> **課題の種類**: 計算演習 / Pythonコーディング
> **学習目標**: 稼働率・MTBF・MTTRの計算と、直列・並列システムの信頼性計算を正確に行えるようになる

---

## 完成イメージ

```
===== システム稼働率計算ツール =====

--- 単体機器の稼働率 ---
MTBF（平均故障間隔）を入力（時間）: 950
MTTR（平均修理時間）を入力（時間）: 50

稼働率 A = 950 / (950 + 50) = 0.9500 (95.00%)

--- システム構成の稼働率 ---
構成を選択してください:
  1. 直列（すべて稼働で動作）
  2. 並列（1つでも稼働で動作）
  3. 直列＋並列の組み合わせ

選択 (1-3): 2
並列に接続する機器の台数: 2
各機器の稼働率（同一と仮定）: 0.95

並列システムの稼働率 = 1 - (1 - 0.95)^2 = 0.9975 (99.75%)
```

---

## 課題の要件

1. MTBF と MTTR から単体機器の稼働率を計算する
2. 直列システムの稼働率を計算する（各機器の稼働率の積）
3. 並列システムの稼働率を計算する（1 - 非稼働率の積）
4. 直列＋並列の組み合わせ構成に対応する

---

## 背景知識の確認

```
稼働率:          A = MTBF / (MTBF + MTTR)
直列n台:         A_system = A1 × A2 × ... × An
並列n台:         A_system = 1 - (1-A1)(1-A2)...(1-An)
同一機器並列n台:  A_system = 1 - (1-A)^n

┌──────────────────────────────┐
│ 直列接続（両方動いて初めて動作） │
│                              │
│  ─→[機器A]──→[機器B]──→      │
│                              │
│  稼働率 = A_a × A_b          │
└──────────────────────────────┘

┌──────────────────────────────┐
│ 並列接続（どちらか動けば動作）   │
│        ┌→[機器A]─┐            │
│  ─→────┤         ├──→        │
│        └→[機器B]─┘            │
│                              │
│  稼働率 = 1 - (1-A_a)(1-A_b) │
└──────────────────────────────┘
```

---

## ステップガイド

<details>
<summary>ステップ1：単体機器の稼働率を計算する</summary>

```python
mtbf = float(input("MTBF（平均故障間隔）を入力（時間）: "))
mttr = float(input("MTTR（平均修理時間）を入力（時間）: "))

availability = mtbf / (mtbf + mttr)
print(f"稼働率 A = {mtbf} / ({mtbf} + {mttr}) = {availability:.4f} ({availability*100:.2f}%)")
```

</details>

<details>
<summary>ステップ2：直列・並列の計算を関数化する</summary>

```python
def serial_availability(a_list):
    """直列システムの稼働率を計算"""
    result = 1.0
    for a in a_list:
        result *= a
    return result

def parallel_availability(a_list):
    """並列システムの稼働率を計算"""
    result = 1.0
    for a in a_list:
        result *= (1 - a)
    return 1 - result
```

</details>

<details>
<summary>ステップ3：組み合わせ構成に対応する</summary>

直列＋並列の組み合わせは、まず並列部分の稼働率を計算してから、それを直列に組み込む考え方です。

```
例：[機器A] ── [機器B並列2台] ── [機器C]

1. 機器Bの並列稼働率を計算: A_b_parallel = 1 - (1 - A_b)^2
2. 全体を直列計算: A_system = A_a × A_b_parallel × A_c
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```python
# システム稼働率計算ツール
# 学べる内容：稼働率計算、MTBF/MTTR、直列・並列システム
# 実行方法：python availability_calc.py

print("===== システム稼働率計算ツール =====\n")

# --- 単体機器の稼働率 ---
print("--- 単体機器の稼働率 ---")
mtbf = float(input("MTBF（平均故障間隔）を入力（時間）: "))
mttr = float(input("MTTR（平均修理時間）を入力（時間）: "))

a_single = mtbf / (mtbf + mttr)
print(f"稼働率 A = {mtbf} / ({mtbf} + {mttr}) = {a_single:.4f} ({a_single*100:.2f}%)\n")

# --- システム構成の選択 ---
print("--- システム構成の稼働率 ---")
print("構成を選択してください:")
print("  1. 直列（すべて稼働で動作）")
print("  2. 並列（1つでも稼働で動作）")
print("  3. 直列＋並列の組み合わせ")
choice = int(input("\n選択 (1-3): "))

if choice == 1:
    n = int(input("直列に接続する機器の台数: "))
    a = float(input("各機器の稼働率（同一と仮定）: "))
    result = a ** n
    print(f"\n直列システムの稼働率 = {a}^{n} = {result:.4f} ({result*100:.2f}%)")

elif choice == 2:
    n = int(input("並列に接続する機器の台数: "))
    a = float(input("各機器の稼働率（同一と仮定）: "))
    result = 1 - (1 - a) ** n
    print(f"\n並列システムの稼働率 = 1 - (1 - {a})^{n} = {result:.4f} ({result*100:.2f}%)")

elif choice == 3:
    print("\n[直列＋並列] 直列部分の機器数と並列冗長部分を設定します")
    a = float(input("各機器の稼働率（全機器同一と仮定）: "))
    serial_count = int(input("直列部分の機器数（並列化しない）: "))
    parallel_count = int(input("並列冗長する機器の台数: "))

    # 並列部分の稼働率
    a_parallel = 1 - (1 - a) ** parallel_count
    # 全体（直列部分 × 並列部分）
    result = (a ** serial_count) * a_parallel
    print(f"\n並列部分の稼働率 = 1 - (1 - {a})^{parallel_count} = {a_parallel:.4f}")
    print(f"全体の稼働率 = {a}^{serial_count} × {a_parallel:.4f} = {result:.4f} ({result*100:.2f}%)")

else:
    print("無効な選択です。")
```

</details>

<details>
<summary>解答例（改良版 ─ 任意構成対応＆コスト対効果分析付き）</summary>

```python
# システム稼働率計算ツール（改良版）
# 学べる内容：稼働率計算、冗長化のコスト対効果分析
# 実行方法：python availability_advanced.py

def calc_availability(mtbf, mttr):
    """MTBF/MTTRから稼働率を計算"""
    return mtbf / (mtbf + mttr)

def serial(a_list):
    """直列システムの稼働率"""
    result = 1.0
    for a in a_list:
        result *= a
    return result

def parallel(a_list):
    """並列システムの稼働率"""
    result = 1.0
    for a in a_list:
        result *= (1 - a)
    return 1 - result

def downtime_per_year(availability):
    """年間ダウンタイムを計算（時間）"""
    return (1 - availability) * 365.25 * 24

# --- メイン ---
print("===== システム稼働率計算ツール（改良版） =====\n")

mtbf = float(input("MTBF（時間）: "))
mttr = float(input("MTTR（時間）: "))
a = calc_availability(mtbf, mttr)

print(f"\n単体稼働率: {a:.4f} ({a*100:.2f}%)")
print(f"年間ダウンタイム: {downtime_per_year(a):.1f} 時間\n")

# 並列台数を増やしたときの効果を比較
print("--- 冗長化の効果比較 ---")
print(f"{'構成':<16} | {'稼働率':>10} | {'年間DT(時間)':>12} | {'9の数':>6}")
print("-" * 55)

# 直列（冗長なし）
for n in range(1, 5):
    if n == 1:
        label = "単体（冗長なし）"
        a_sys = a
    else:
        label = f"並列{n}台"
        a_sys = 1 - (1 - a) ** n
    dt = downtime_per_year(a_sys)
    # 9の数（ナイン）を計算
    import math
    if a_sys >= 1.0:
        nines = "∞"
    else:
        nines = f"{-math.log10(1 - a_sys):.1f}"
    print(f"{label:<16} | {a_sys:10.6f} | {dt:12.2f} | {nines:>6}")

print("\n※ 9の数: 稼働率99.9%なら「スリーナイン」（3つ）")
print("  ファイブナイン（99.999%）が高可用性の目安")
```

**初心者向けとの違い:**
- 年間ダウンタイムを具体的な時間で表示し、ビジネスインパクトを可視化
- 「ナイン（9の数）」という可用性の業界指標を導入
- 並列台数を増やしたときの効果を一覧比較できる

</details>

---

## 確認問題

手計算してからプログラムで検算しましょう。

**問1:** MTBF = 900時間、MTTR = 100時間の機器の稼働率は？
→ 0.90（90%）

**問2:** 稼働率0.90の機器を2台並列にしたときの稼働率は？
→ 1 - (1-0.9)^2 = 1 - 0.01 = 0.99（99%）

**問3:** 稼働率0.95の機器A（1台）と稼働率0.90の機器B（2台並列）を直列接続したときの全体の稼働率は？
→ 0.95 × (1 - (1-0.9)^2) = 0.95 × 0.99 = 0.9405（94.05%）
