# ==============================
# ソートアルゴリズム可視化
# 基本情報技術者：整列アルゴリズム
# ==============================
# 学べる内容:
#   - バブルソート（bubble sort）
#   - 選択ソート（selection sort）
#   - 挿入ソート（insertion sort）
#   - クイックソート（quick sort）
#   - マージソート（merge sort）
#   - 各アルゴリズムの計算量と比較
#   - 基本情報技術者試験の整列アルゴリズム問題への対応力
#
# 実行方法:
#   python 04_ソートアルゴリズム可視化.py
# ==============================

import time
import random


def visualize_array(arr, highlight=None, highlight2=None, label=""):
    """配列をバーグラフ風に表示します

    highlight: 比較中の位置（赤）
    highlight2: 交換先の位置（青）
    """
    if label:
        print(f"  {label}")
    max_val = max(arr) if arr else 1
    bar_width = 40

    for i, val in enumerate(arr):
        bar_len = int(val / max_val * bar_width)
        bar = "#" * bar_len

        # ハイライト表示
        if highlight is not None and i == highlight:
            marker = " <<"
        elif highlight2 is not None and i == highlight2:
            marker = " <<"
        else:
            marker = ""

        print(f"    [{i:>2}] {val:>3} |{bar}{marker}")


def print_step(arr, step, swap_info=""):
    """ソートの各ステップを表示します"""
    arr_str = " ".join(f"{x:>3}" for x in arr)
    info = f"  ({swap_info})" if swap_info else ""
    print(f"    ステップ{step:>2}: [{arr_str} ]{info}")


# ============================================================
# 1. バブルソート（Bubble Sort）
# ============================================================

def bubble_sort(arr, verbose=True):
    """バブルソート: 隣接要素を比較・交換して整列します

    計算量: 平均 O(n^2), 最悪 O(n^2), 最良 O(n)
    安定ソート: Yes
    """
    data = arr.copy()
    n = len(data)
    comparisons = 0
    swaps = 0
    step = 0

    if verbose:
        print("\n  ■ バブルソート（Bubble Sort）")
        print("  アルゴリズム: 隣り合う要素を比較し、大きい方を右に移動します")
        print("  イメージ: 泡（bubble）が水面に浮かぶように大きい値が右に移動します")
        print_step(data, 0, "初期状態")

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swaps += 1
                swapped = True
                step += 1
                if verbose:
                    print_step(data, step, f"{data[j+1]}と{data[j]}を交換")

        if not swapped:
            if verbose:
                print(f"    → 交換なし！ソート完了")
            break

    if verbose:
        print(f"    比較回数: {comparisons}, 交換回数: {swaps}")
    return data, comparisons, swaps


# ============================================================
# 2. 選択ソート（Selection Sort）
# ============================================================

def selection_sort(arr, verbose=True):
    """選択ソート: 最小値を選んで先頭から順に確定します

    計算量: 平均 O(n^2), 最悪 O(n^2), 最良 O(n^2)
    安定ソート: No
    """
    data = arr.copy()
    n = len(data)
    comparisons = 0
    swaps = 0

    if verbose:
        print("\n  ■ 選択ソート（Selection Sort）")
        print("  アルゴリズム: 未整列部分から最小値を見つけ、先頭と交換します")
        print_step(data, 0, "初期状態")

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if data[j] < data[min_idx]:
                min_idx = j

        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
            swaps += 1
            if verbose:
                print_step(data, i + 1, f"最小値{data[i]}を位置{i}に配置")
        else:
            if verbose:
                print_step(data, i + 1, f"位置{i}は既に最小値{data[i]}")

    if verbose:
        print(f"    比較回数: {comparisons}, 交換回数: {swaps}")
    return data, comparisons, swaps


# ============================================================
# 3. 挿入ソート（Insertion Sort）
# ============================================================

def insertion_sort(arr, verbose=True):
    """挿入ソート: 未整列の要素を整列済み部分の正しい位置に挿入します

    計算量: 平均 O(n^2), 最悪 O(n^2), 最良 O(n)
    安定ソート: Yes
    """
    data = arr.copy()
    n = len(data)
    comparisons = 0
    shifts = 0

    if verbose:
        print("\n  ■ 挿入ソート（Insertion Sort）")
        print("  アルゴリズム: トランプの手札を並べるように、正しい位置に挿入します")
        print_step(data, 0, "初期状態")

    for i in range(1, n):
        key = data[i]
        j = i - 1
        insert_info = f"{key}を挿入 → "

        while j >= 0 and data[j] > key:
            comparisons += 1
            data[j + 1] = data[j]
            shifts += 1
            j -= 1
        if j >= 0:
            comparisons += 1  # while条件の最後の比較

        data[j + 1] = key
        if verbose:
            insert_info += f"位置{j+1}に配置"
            print_step(data, i, insert_info)

    if verbose:
        print(f"    比較回数: {comparisons}, シフト回数: {shifts}")
    return data, comparisons, shifts


# ============================================================
# 4. クイックソート（Quick Sort）
# ============================================================

def quick_sort(arr, verbose=True):
    """クイックソート: 基準値（pivot）で分割して再帰的に整列します

    計算量: 平均 O(n log n), 最悪 O(n^2), 最良 O(n log n)
    安定ソート: No
    """
    data = arr.copy()
    stats = {"comparisons": 0, "swaps": 0, "step": 0}

    if verbose:
        print("\n  ■ クイックソート（Quick Sort）")
        print("  アルゴリズム: 基準値（pivot）を選び、小さい/大きいグループに分割します")
        print_step(data, 0, "初期状態")

    def _quick_sort(data, low, high, depth=0):
        if low < high:
            pivot_idx = _partition(data, low, high, depth)
            _quick_sort(data, low, pivot_idx - 1, depth + 1)
            _quick_sort(data, pivot_idx + 1, high, depth + 1)

    def _partition(data, low, high, depth):
        pivot = data[high]  # 末尾を基準値にします
        indent = "  " * depth
        if verbose:
            print(f"    {indent}分割 [{low}:{high}], pivot={pivot}")

        i = low - 1
        for j in range(low, high):
            stats["comparisons"] += 1
            if data[j] <= pivot:
                i += 1
                if i != j:
                    data[i], data[j] = data[j], data[i]
                    stats["swaps"] += 1

        data[i + 1], data[high] = data[high], data[i + 1]
        stats["swaps"] += 1
        stats["step"] += 1

        if verbose:
            print_step(data, stats["step"],
                       f"pivot={pivot}, 分割位置={i+1}")
        return i + 1

    _quick_sort(data, 0, len(data) - 1)

    if verbose:
        print(f"    比較回数: {stats['comparisons']}, 交換回数: {stats['swaps']}")
    return data, stats["comparisons"], stats["swaps"]


# ============================================================
# 5. マージソート（Merge Sort）
# ============================================================

def merge_sort(arr, verbose=True):
    """マージソート: 分割してから統合する再帰的アルゴリズムです

    計算量: 平均 O(n log n), 最悪 O(n log n), 最良 O(n log n)
    安定ソート: Yes
    """
    stats = {"comparisons": 0, "step": 0}

    if verbose:
        print("\n  ■ マージソート（Merge Sort）")
        print("  アルゴリズム: 半分に分割 → 再帰的にソート → 統合（merge）")

    def _merge_sort(data, depth=0):
        if len(data) <= 1:
            return data

        indent = "  " * depth
        mid = len(data) // 2
        left = data[:mid]
        right = data[mid:]

        if verbose:
            print(f"    {indent}分割: {data} → {left} | {right}")

        left = _merge_sort(left, depth + 1)
        right = _merge_sort(right, depth + 1)

        return _merge(left, right, depth)

    def _merge(left, right, depth):
        indent = "  " * depth
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            stats["comparisons"] += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        stats["step"] += 1

        if verbose:
            print(f"    {indent}統合: {left} + {right} → {result}")
        return result

    if verbose:
        print(f"    初期状態: {arr}")
        print()

    result = _merge_sort(arr.copy())

    if verbose:
        print(f"\n    比較回数: {stats['comparisons']}")
    return result, stats["comparisons"], 0


# ============================================================
# アルゴリズム比較
# ============================================================

def compare_algorithms(arr):
    """全アルゴリズムの性能を比較します"""
    print("\n━━━ アルゴリズム性能比較 ━━━")
    print(f"  データ: {arr}")
    print(f"  要素数: {len(arr)}")
    print()

    algorithms = [
        ("バブルソート", bubble_sort),
        ("選択ソート", selection_sort),
        ("挿入ソート", insertion_sort),
        ("クイックソート", quick_sort),
        ("マージソート", merge_sort),
    ]

    results = []
    for name, func in algorithms:
        start = time.time()
        sorted_arr, comps, swaps = func(arr, verbose=False)
        elapsed = time.time() - start
        results.append((name, comps, swaps, elapsed))

    # 比較表
    print(f"  {'アルゴリズム':　<16} {'比較回数':>8} {'交換/シフト':>10} {'実行時間':>10}")
    print("  " + "─" * 52)
    for name, comps, swaps, elapsed in results:
        print(f"  {name:<16} {comps:>8} {swaps:>10} {elapsed:>8.6f}秒")

    # 計算量の理論値
    n = len(arr)
    print(f"\n  ■ 計算量の理論比較（n={n}）")
    print(f"    O(n^2)     = {n*n:>10,}")
    print(f"    O(n log n) = {int(n * (n.bit_length())):>10,}")
    print(f"    O(n)       = {n:>10,}")


def show_complexity_chart():
    """各ソートアルゴリズムの計算量を表にまとめます"""
    print("\n  ■ ソートアルゴリズム計算量一覧")
    print(f"    {'アルゴリズム':　<14} {'最良':>10} {'平均':>10} {'最悪':>10} {'安定':>4} {'特徴'}")
    print("    " + "─" * 72)
    data = [
        ("バブルソート", "O(n)", "O(n^2)", "O(n^2)", "Yes", "単純、教育向き"),
        ("選択ソート", "O(n^2)", "O(n^2)", "O(n^2)", "No", "交換回数が少ない"),
        ("挿入ソート", "O(n)", "O(n^2)", "O(n^2)", "Yes", "ほぼ整列済みに強い"),
        ("クイックソート", "O(n log n)", "O(n log n)", "O(n^2)", "No", "実用で最速"),
        ("マージソート", "O(n log n)", "O(n log n)", "O(n log n)", "Yes", "安定かつ高速"),
    ]
    for name, best, avg, worst, stable, note in data:
        print(f"    {name:<14} {best:>10} {avg:>10} {worst:>10} {stable:>4} {note}")


# ============================================================
# 対話モード
# ============================================================

def interactive_mode():
    """対話型のソートアルゴリズム可視化です"""
    print("\n" + "=" * 55)
    print("  ソートアルゴリズム可視化 - 対話モード")
    print("=" * 55)
    print("  操作を選んでください:")
    print("    1. バブルソート")
    print("    2. 選択ソート")
    print("    3. 挿入ソート")
    print("    4. クイックソート")
    print("    5. マージソート")
    print("    6. 全アルゴリズム比較")
    print("    7. ランダムデータで比較")
    print("    0. 終了")
    print("-" * 55)

    while True:
        choice = input("\n  選択 (0-7): ").strip()

        if choice == "0":
            print("  ソートアルゴリズム可視化を終了します。")
            break

        elif choice in ("1", "2", "3", "4", "5"):
            data_input = input("  データを入力（スペース区切り。例: 5 3 8 1 9）: ").strip()
            try:
                data = [int(x) for x in data_input.split()]
                if len(data) < 2:
                    print("  ※ 2つ以上の数を入力してください。")
                    continue

                funcs = {
                    "1": ("バブルソート", bubble_sort),
                    "2": ("選択ソート", selection_sort),
                    "3": ("挿入ソート", insertion_sort),
                    "4": ("クイックソート", quick_sort),
                    "5": ("マージソート", merge_sort),
                }
                name, func = funcs[choice]
                result, comps, swaps = func(data)
                print(f"\n  ソート結果: {result}")
            except ValueError:
                print("  ※ 整数をスペース区切りで入力してください。")

        elif choice == "6":
            data_input = input("  データを入力（スペース区切り）: ").strip()
            try:
                data = [int(x) for x in data_input.split()]
                if len(data) < 2:
                    print("  ※ 2つ以上の数を入力してください。")
                    continue
                compare_algorithms(data)
            except ValueError:
                print("  ※ 整数をスペース区切りで入力してください。")

        elif choice == "7":
            try:
                n = int(input("  要素数を入力 (5-100): "))
                if n < 5 or n > 100:
                    n = 20
                    print("  ※ 20要素で実行します。")
                data = random.sample(range(1, n * 3), n)
                print(f"  ランダムデータ ({n}要素): {data[:10]}{'...' if n > 10 else ''}")
                compare_algorithms(data)
            except ValueError:
                print("  ※ 正しい数値を入力してください。")

        else:
            print("  ※ 0-7の番号を入力してください。")


# === デモンストレーション ===
print("=" * 55)
print("  ソートアルゴリズム可視化")
print("  ～ 整列の仕組みを目で見て理解しよう ～")
print("=" * 55)

# デモ用データ
demo_data = [64, 34, 25, 12, 22, 11, 90]
print(f"\n  デモデータ: {demo_data}")

# 各アルゴリズムのデモ
print("\n" + "=" * 55)
bubble_sort(demo_data)

print("\n" + "=" * 55)
selection_sort(demo_data)

print("\n" + "=" * 55)
insertion_sort(demo_data)

print("\n" + "=" * 55)
quick_sort(demo_data)

print("\n" + "=" * 55)
merge_sort(demo_data)

# バーグラフでの可視化
print("\n\n━━━ バーグラフでの可視化 ━━━")
small_data = [38, 27, 43, 3, 9, 82, 10]
print("  ソート前:")
visualize_array(small_data)
sorted_data, _, _ = bubble_sort(small_data, verbose=False)
print("\n  ソート後:")
visualize_array(sorted_data)

# アルゴリズム比較
compare_algorithms(demo_data)

# 計算量一覧
show_complexity_chart()

# 対話モード
interactive_mode()
