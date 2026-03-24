# ==============================
# データ変換パイプライン
# 第11章：内包表記とジェネレータの実践
# ==============================
# 学べる内容:
#   - リスト内包表記（基本 / 条件付き / ネスト）
#   - 辞書内包表記・セット内包表記
#   - ジェネレータ式とジェネレータ関数（yield）
#   - map / filter / zip / enumerate の活用
#   - itertools の便利な関数
#   - メモリ効率の良いデータ処理
#   - パイプライン的なデータ変換パターン
# 実行方法:
#   python 11_データ変換パイプライン.py
# ==============================

import itertools
from collections import Counter


# === サンプルデータ ===

# 売上データ（辞書のリスト）
SALES_DATA = [
    {"日付": "2025-04-01", "商品": "りんご", "単価": 150, "数量": 3, "カテゴリ": "果物"},
    {"日付": "2025-04-01", "商品": "牛乳", "単価": 200, "数量": 2, "カテゴリ": "飲料"},
    {"日付": "2025-04-02", "商品": "パン", "単価": 300, "数量": 1, "カテゴリ": "主食"},
    {"日付": "2025-04-02", "商品": "りんご", "単価": 150, "数量": 5, "カテゴリ": "果物"},
    {"日付": "2025-04-02", "商品": "お茶", "単価": 130, "数量": 4, "カテゴリ": "飲料"},
    {"日付": "2025-04-03", "商品": "バナナ", "単価": 100, "数量": 6, "カテゴリ": "果物"},
    {"日付": "2025-04-03", "商品": "牛乳", "単価": 200, "数量": 1, "カテゴリ": "飲料"},
    {"日付": "2025-04-03", "商品": "卵", "単価": 250, "数量": 2, "カテゴリ": "その他"},
    {"日付": "2025-04-04", "商品": "パン", "単価": 300, "数量": 3, "カテゴリ": "主食"},
    {"日付": "2025-04-04", "商品": "みかん", "単価": 80, "数量": 10, "カテゴリ": "果物"},
    {"日付": "2025-04-05", "商品": "りんご", "単価": 150, "数量": 2, "カテゴリ": "果物"},
    {"日付": "2025-04-05", "商品": "お茶", "単価": 130, "数量": 3, "カテゴリ": "飲料"},
    {"日付": "2025-04-05", "商品": "牛乳", "単価": 200, "数量": 2, "カテゴリ": "飲料"},
]

# 学生の成績データ
STUDENT_DATA = [
    {"名前": "田中", "国語": 75, "数学": 88, "英語": 62, "理科": 91, "社会": 70},
    {"名前": "鈴木", "国語": 90, "数学": 72, "英語": 85, "理科": 68, "社会": 88},
    {"名前": "佐藤", "国語": 65, "数学": 95, "英語": 70, "理科": 92, "社会": 60},
    {"名前": "高橋", "国語": 82, "数学": 60, "英語": 90, "理科": 75, "社会": 85},
    {"名前": "伊藤", "国語": 55, "数学": 78, "英語": 68, "理科": 82, "社会": 72},
    {"名前": "渡辺", "国語": 95, "数学": 85, "英語": 92, "理科": 88, "社会": 90},
]


# === デモ1：リスト内包表記の基本 ===

def demo_list_comprehension():
    """リスト内包表記のさまざまなパターン"""
    print("\n" + "=" * 50)
    print("  デモ1：リスト内包表記")
    print("=" * 50)

    # --- 基本 ---
    print("\n--- 基本的なリスト内包表記 ---")

    # 従来の for ループ
    squares_loop = []
    for i in range(1, 11):
        squares_loop.append(i ** 2)

    # リスト内包表記（1行で同じことができる）
    squares = [i ** 2 for i in range(1, 11)]
    print(f"  1〜10の二乗: {squares}")

    # --- 条件付き（if）---
    print("\n--- 条件付きリスト内包表記 ---")

    # 偶数だけ抽出
    evens = [x for x in range(1, 21) if x % 2 == 0]
    print(f"  1〜20の偶数: {evens}")

    # 3の倍数かつ5の倍数
    fizzbuzz = [x for x in range(1, 31) if x % 3 == 0 and x % 5 == 0]
    print(f"  1〜30で3と5の公倍数: {fizzbuzz}")

    # --- 条件式（if-else）---
    print("\n--- 三項演算子付きリスト内包表記 ---")

    # FizzBuzz
    fb = [
        "FizzBuzz" if x % 15 == 0
        else "Fizz" if x % 3 == 0
        else "Buzz" if x % 5 == 0
        else str(x)
        for x in range(1, 21)
    ]
    print(f"  FizzBuzz: {fb}")

    # --- ネストした内包表記 ---
    print("\n--- ネストした内包表記 ---")

    # 九九の表（2重ループ）
    multiplication = [
        f"{i}x{j}={i*j}"
        for i in range(1, 4)
        for j in range(1, 4)
    ]
    print(f"  九九（1〜3）: {multiplication}")

    # 2次元リストの平坦化
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat = [num for row in matrix for num in row]
    print(f"  行列の平坦化: {matrix} → {flat}")

    # --- 文字列操作 ---
    print("\n--- 文字列とリスト内包表記 ---")

    words = ["Python", "JavaScript", "Go", "Rust", "TypeScript"]
    lengths = [(w, len(w)) for w in words]
    print(f"  単語と文字数: {lengths}")

    long_words = [w for w in words if len(w) > 4]
    print(f"  5文字以上の言語: {long_words}")

    upper_words = [w.upper() for w in words]
    print(f"  大文字変換: {upper_words}")


# === デモ2：辞書内包表記・セット内包表記 ===

def demo_dict_set_comprehension():
    """辞書内包表記とセット内包表記"""
    print("\n" + "=" * 50)
    print("  デモ2：辞書・セット内包表記")
    print("=" * 50)

    # --- 辞書内包表記 ---
    print("\n--- 辞書内包表記 ---")

    # 数値を二乗にマッピング
    square_dict = {x: x ** 2 for x in range(1, 6)}
    print(f"  二乗辞書: {square_dict}")

    # 文字列の長さをマッピング
    words = ["Python", "JavaScript", "Go", "Rust"]
    word_lengths = {w: len(w) for w in words}
    print(f"  文字数辞書: {word_lengths}")

    # 売上データから商品→カテゴリの辞書を作成
    product_category = {
        item["商品"]: item["カテゴリ"]
        for item in SALES_DATA
    }
    print(f"  商品→カテゴリ: {product_category}")

    # 辞書のキーと値を入れ替え
    flipped = {v: k for k, v in word_lengths.items()}
    print(f"  キーと値を入替: {flipped}")

    # 条件付き辞書内包表記
    long_words = {w: l for w, l in word_lengths.items() if l > 3}
    print(f"  4文字以上: {long_words}")

    # --- セット内包表記 ---
    print("\n--- セット内包表記 ---")

    # 売上データからユニークなカテゴリを取得
    categories = {item["カテゴリ"] for item in SALES_DATA}
    print(f"  カテゴリ一覧: {categories}")

    # ユニークな商品一覧
    products = {item["商品"] for item in SALES_DATA}
    print(f"  商品一覧: {products}")

    # 売上日一覧
    dates = {item["日付"] for item in SALES_DATA}
    print(f"  売上日: {sorted(dates)}")


# === デモ3：売上データのパイプライン処理 ===

def demo_sales_pipeline():
    """売上データを内包表記で段階的に変換する"""
    print("\n" + "=" * 50)
    print("  デモ3：売上データパイプライン")
    print("=" * 50)

    print("\n--- Step 1: 各行に売上額を追加 ---")
    # 辞書の展開（**）を使って新しいキーを追加
    enriched = [
        {**item, "売上額": item["単価"] * item["数量"]}
        for item in SALES_DATA
    ]
    for row in enriched[:3]:
        print(f"  {row['日付']} {row['商品']} "
              f"{row['単価']}円 x {row['数量']} = {row['売上額']}円")
    print(f"  ... 他 {len(enriched) - 3}件")

    print("\n--- Step 2: カテゴリ別に集計 ---")
    # カテゴリごとの売上額リスト
    category_sales = {}
    for item in enriched:
        cat = item["カテゴリ"]
        if cat not in category_sales:
            category_sales[cat] = []
        category_sales[cat].append(item["売上額"])

    # 辞書内包表記で集計
    category_totals = {
        cat: sum(amounts) for cat, amounts in category_sales.items()
    }
    total = sum(category_totals.values())

    for cat, amount in sorted(category_totals.items(),
                              key=lambda x: x[1], reverse=True):
        ratio = amount / total * 100
        bar = "#" * int(ratio / 2)
        print(f"  {cat:<6} {amount:>6,}円 ({ratio:>5.1f}%) {bar}")
    print(f"  {'合計':<6} {total:>6,}円")

    print("\n--- Step 3: 商品別の売上ランキング ---")
    product_totals = {}
    for item in enriched:
        name = item["商品"]
        product_totals[name] = product_totals.get(name, 0) + item["売上額"]

    # sorted + 辞書内包表記でランキング
    ranking = sorted(product_totals.items(), key=lambda x: x[1], reverse=True)
    for rank, (product, amount) in enumerate(ranking, 1):
        print(f"  {rank}位 {product:<6} {amount:>6,}円")

    print("\n--- Step 4: 日付別の売上推移 ---")
    date_totals = {}
    for item in enriched:
        d = item["日付"]
        date_totals[d] = date_totals.get(d, 0) + item["売上額"]

    max_amount = max(date_totals.values())
    for d, amount in sorted(date_totals.items()):
        bar_len = int(amount / max_amount * 30)
        bar = "#" * bar_len
        print(f"  {d} {amount:>6,}円 {bar}")


# === デモ4：ジェネレータ ===

def demo_generators():
    """ジェネレータ式とジェネレータ関数"""
    print("\n" + "=" * 50)
    print("  デモ4：ジェネレータ")
    print("=" * 50)

    # --- ジェネレータ式 ---
    print("\n--- ジェネレータ式 vs リスト内包表記 ---")

    # リスト内包表記：メモリにすべて展開
    list_comp = [x ** 2 for x in range(10)]
    print(f"  リスト: {list_comp}")
    print(f"  型: {type(list_comp)}")

    # ジェネレータ式：必要なときに1つずつ生成（省メモリ）
    gen_exp = (x ** 2 for x in range(10))
    print(f"  ジェネレータ: {gen_exp}")
    print(f"  型: {type(gen_exp)}")
    print(f"  リストに変換: {list(gen_exp)}")

    # メモリ効率の比較
    import sys
    list_size = sys.getsizeof([x for x in range(10000)])
    gen_size = sys.getsizeof(x for x in range(10000))
    print(f"\n  10000要素のメモリ使用量:")
    print(f"    リスト:       {list_size:>8,} バイト")
    print(f"    ジェネレータ: {gen_size:>8,} バイト")

    # --- ジェネレータ関数（yield）---
    print("\n--- ジェネレータ関数（yield）---")

    def fibonacci(n):
        """フィボナッチ数列ジェネレータ"""
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b

    fib = list(fibonacci(15))
    print(f"  フィボナッチ数列（15項）: {fib}")

    def chunked(iterable, size):
        """イテラブルを指定サイズに分割するジェネレータ"""
        chunk = []
        for item in iterable:
            chunk.append(item)
            if len(chunk) == size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    data = list(range(1, 12))
    chunks = list(chunked(data, 3))
    print(f"  {data} を3つずつ分割: {chunks}")

    def running_average():
        """移動平均ジェネレータ（sendを使わないシンプル版）"""
        values = []
        for val in [10, 20, 30, 25, 35, 40, 30]:
            values.append(val)
            avg = sum(values) / len(values)
            yield val, round(avg, 1)

    print("\n  移動平均:")
    for val, avg in running_average():
        print(f"    値: {val:>3} → 平均: {avg}")

    # --- ジェネレータの連鎖（パイプライン）---
    print("\n--- ジェネレータの連鎖 ---")

    def read_data(data):
        """データを1件ずつ読み出す"""
        for item in data:
            yield item

    def add_total(items):
        """売上額フィールドを追加する"""
        for item in items:
            yield {**item, "売上額": item["単価"] * item["数量"]}

    def filter_by_category(items, category):
        """カテゴリでフィルタリングする"""
        for item in items:
            if item["カテゴリ"] == category:
                yield item

    def format_output(items):
        """出力用にフォーマットする"""
        for item in items:
            yield f"{item['日付']} {item['商品']} {item['売上額']:,}円"

    # パイプラインの組み立て
    pipeline = format_output(
        filter_by_category(
            add_total(
                read_data(SALES_DATA)
            ),
            "果物"
        )
    )

    print("  果物カテゴリの売上（ジェネレータパイプライン）:")
    for line in pipeline:
        print(f"    {line}")


# === デモ5：map / filter / zip / enumerate ===

def demo_functional():
    """関数型プログラミングスタイルのデータ処理"""
    print("\n" + "=" * 50)
    print("  デモ5：map / filter / zip / enumerate")
    print("=" * 50)

    # --- map ---
    print("\n--- map: すべての要素に関数を適用 ---")

    prices = [100, 250, 300, 150, 500]
    # 税込み価格に変換
    with_tax = list(map(lambda p: int(p * 1.1), prices))
    print(f"  税抜: {prices}")
    print(f"  税込: {with_tax}")

    # 内包表記でも同じことができる（こちらが推奨）
    with_tax_comp = [int(p * 1.1) for p in prices]
    print(f"  内包表記版: {with_tax_comp}")

    # --- filter ---
    print("\n--- filter: 条件に合う要素を抽出 ---")

    numbers = [12, 7, 25, 3, 18, 42, 9, 31, 6]
    big_nums = list(filter(lambda x: x >= 20, numbers))
    print(f"  元データ: {numbers}")
    print(f"  20以上: {big_nums}")

    # 内包表記版
    big_nums_comp = [x for x in numbers if x >= 20]
    print(f"  内包表記版: {big_nums_comp}")

    # --- zip ---
    print("\n--- zip: 複数のイテラブルを同時にループ ---")

    names = ["田中", "鈴木", "佐藤", "高橋"]
    scores = [85, 92, 78, 88]
    grades = ["B", "A", "C", "B"]

    print("  名前・点数・成績を対応付け:")
    for name, score, grade in zip(names, scores, grades):
        print(f"    {name}: {score}点 ({grade})")

    # zip で辞書を作成
    score_dict = dict(zip(names, scores))
    print(f"  辞書化: {score_dict}")

    # --- enumerate ---
    print("\n--- enumerate: インデックス付きループ ---")

    fruits = ["りんご", "バナナ", "みかん", "ぶどう"]
    print("  番号付きリスト:")
    for i, fruit in enumerate(fruits, start=1):
        print(f"    {i}. {fruit}")

    # enumerate + 内包表記
    indexed = {i: fruit for i, fruit in enumerate(fruits)}
    print(f"  インデックス辞書: {indexed}")


# === デモ6：成績分析パイプライン ===

def demo_grade_pipeline():
    """成績データの実践的な分析"""
    print("\n" + "=" * 50)
    print("  デモ6：成績分析パイプライン（実践）")
    print("=" * 50)

    subjects = ["国語", "数学", "英語", "理科", "社会"]

    # Step 1: 各生徒の合計・平均を計算
    print("\n--- 個人別成績 ---")
    enriched_students = [
        {
            **student,
            "合計": sum(student[s] for s in subjects),
            "平均": round(sum(student[s] for s in subjects) / len(subjects), 1),
            "最高科目": max(subjects, key=lambda s: student[s]),
            "最低科目": min(subjects, key=lambda s: student[s]),
        }
        for student in STUDENT_DATA
    ]

    # 平均点の降順でソート
    ranked = sorted(enriched_students, key=lambda s: s["平均"], reverse=True)
    print(f"  {'順位':<4} {'名前':<6} {'合計':>4} {'平均':>5}"
          f"  {'得意科目':<6} {'苦手科目':<6}")
    print("  " + "-" * 48)
    for rank, student in enumerate(ranked, 1):
        print(f"  {rank:<4} {student['名前']:<6} {student['合計']:>4}"
              f" {student['平均']:>5.1f}"
              f"  {student['最高科目']:<6} {student['最低科目']:<6}")

    # Step 2: 科目別の統計
    print("\n--- 科目別統計 ---")
    subject_stats = {
        subject: {
            "平均": round(
                sum(s[subject] for s in STUDENT_DATA) / len(STUDENT_DATA), 1
            ),
            "最高点": max(s[subject] for s in STUDENT_DATA),
            "最低点": min(s[subject] for s in STUDENT_DATA),
            "最高者": max(STUDENT_DATA, key=lambda s: s[subject])["名前"],
        }
        for subject in subjects
    }

    print(f"  {'科目':<6} {'平均':>5} {'最高点':>5} {'最低点':>5}  {'トップ':<6}")
    print("  " + "-" * 38)
    for subject, stats in subject_stats.items():
        print(f"  {subject:<6} {stats['平均']:>5.1f}"
              f" {stats['最高点']:>5} {stats['最低点']:>5}"
              f"  {stats['最高者']:<6}")

    # Step 3: 成績の分布
    print("\n--- 得点分布 ---")
    all_scores = [
        student[subject]
        for student in STUDENT_DATA
        for subject in subjects
    ]

    # 得点帯ごとにカウント
    ranges = [
        ("90〜100", lambda x: 90 <= x <= 100),
        ("80〜89 ", lambda x: 80 <= x <= 89),
        ("70〜79 ", lambda x: 70 <= x <= 79),
        ("60〜69 ", lambda x: 60 <= x <= 69),
        ("50〜59 ", lambda x: 50 <= x <= 59),
    ]

    total = len(all_scores)
    for label, condition in ranges:
        count = len([s for s in all_scores if condition(s)])
        ratio = count / total * 100
        bar = "#" * int(ratio)
        print(f"  {label}: {count:>2}人 ({ratio:>5.1f}%) {bar}")

    # Step 4: itertools を使ったペア比較
    print("\n--- 生徒ペアの相関（itertools.combinations）---")
    for s1, s2 in itertools.combinations(STUDENT_DATA, 2):
        # 各科目の差の絶対値の平均
        avg_diff = round(
            sum(abs(s1[sub] - s2[sub]) for sub in subjects) / len(subjects), 1
        )
        similarity = "似ている" if avg_diff < 10 else "異なる"
        print(f"  {s1['名前']} vs {s2['名前']}: "
              f"平均差 {avg_diff}点 → {similarity}")


# === 対話式デモ ===

def interactive_demo():
    """ユーザーが自分でデータを入力して内包表記を体験"""
    print("\n" + "=" * 50)
    print("  対話式：内包表記を体験")
    print("=" * 50)

    nums_input = input("\n  数値をカンマ区切りで入力: ").strip()
    try:
        nums = [int(x.strip()) for x in nums_input.split(",")]
    except ValueError:
        print("  数値を正しく入力してください。")
        return

    print(f"\n  入力データ: {nums}")

    # いろいろな内包表記を適用
    print(f"  二乗:         {[x ** 2 for x in nums]}")
    print(f"  偶数のみ:     {[x for x in nums if x % 2 == 0]}")
    print(f"  奇数のみ:     {[x for x in nums if x % 2 != 0]}")
    print(f"  正の数のみ:   {[x for x in nums if x > 0]}")
    print(f"  絶対値:       {[abs(x) for x in nums]}")
    print(f"  文字列化:     {[str(x) for x in nums]}")
    print(f"  偶奇判定:     {['偶' if x % 2 == 0 else '奇' for x in nums]}")
    print(f"  累積和:       {[sum(nums[:i+1]) for i in range(len(nums))]}")

    # 辞書内包表記
    indexed = {i: v for i, v in enumerate(nums, 1)}
    print(f"  番号付き辞書: {indexed}")

    # ジェネレータ式の合計
    total = sum(x for x in nums)
    print(f"  合計:         {total}")


# === メインプログラム ===

print("+" + "-" * 38 + "+")
print("|    データ変換パイプライン          |")
print("+" + "-" * 38 + "+")
print("内包表記とジェネレータを使った")
print("データ処理のパターンを学びます。")

while True:
    print("\n--- メニュー ---")
    print("1. リスト内包表記の基本")
    print("2. 辞書・セット内包表記")
    print("3. 売上データパイプライン")
    print("4. ジェネレータ")
    print("5. map / filter / zip / enumerate")
    print("6. 成績分析パイプライン（実践）")
    print("7. 対話式デモ（自分で入力）")
    print("8. 終了")

    choice = input("選択 (1-8): ").strip()

    if choice == "1":
        demo_list_comprehension()
    elif choice == "2":
        demo_dict_set_comprehension()
    elif choice == "3":
        demo_sales_pipeline()
    elif choice == "4":
        demo_generators()
    elif choice == "5":
        demo_functional()
    elif choice == "6":
        demo_grade_pipeline()
    elif choice == "7":
        interactive_demo()
    elif choice == "8":
        print("お疲れさまでした！")
        break
    else:
        print("1〜8の数字を入力してください。")
