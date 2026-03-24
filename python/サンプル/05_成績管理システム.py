# ==============================
# 成績管理システム
# 第5章：関数の総合サンプル
# ==============================
# 学べる内容:
#   - 関数の定義と呼び出し
#   - 引数と戻り値（return）
#   - デフォルト引数
#   - 複数の戻り値
#   - 関数の組み合わせ（分割設計）
#   - *args, **kwargs
#   - zip(), map(), sorted()
# ==============================


def calculate_average(scores):
    """平均点を計算する（基本的な関数）"""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def get_grade(average):
    """平均点から評価を返す（if-elif-else + return）"""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def get_grade_comment(grade):
    """評価に応じたコメントを返す（辞書 + .get()）"""
    comments = {
        "A": "素晴らしい成績です！",
        "B": "よく頑張りました！",
        "C": "もう少し伸ばせます！",
        "D": "頑張りましょう！",
        "F": "基礎から復習しましょう。",
    }
    return comments.get(grade, "不明な評価です")


def get_statistics(scores):
    """統計情報を返す（複数の戻り値）"""
    avg = calculate_average(scores)
    highest = max(scores)
    lowest = min(scores)
    score_range = highest - lowest
    return avg, highest, lowest, score_range


def print_bar(value, max_value=100, width=30):
    """棒グラフを表示する（デフォルト引数）"""
    filled = int(value / max_value * width)
    bar = "#" * filled + "-" * (width - filled)
    return f"[{bar}] {value}"


def print_report(name, subjects, scores):
    """成績レポートを表示する（関数の組み合わせ + zip）"""
    print()
    print("=" * 50)
    print(f"  成績レポート: {name}")
    print("=" * 50)

    # 科目ごとの成績（zip で2つのリストを同時ループ）
    print(f"\n{'科目':<8} {'点数':>4}  {'グラフ'}")
    print("-" * 50)
    for subject, score in zip(subjects, scores):
        bar = print_bar(score)
        print(f"{subject:<8} {score:>4}  {bar}")

    # 統計情報（複数の戻り値を受け取る）
    avg, highest, lowest, score_range = get_statistics(scores)
    grade = get_grade(avg)
    comment = get_grade_comment(grade)

    print("-" * 50)
    print(f"平均点:   {avg:.1f}")
    print(f"最高点:   {highest}")
    print(f"最低点:   {lowest}")
    print(f"点数幅:   {score_range}")
    print(f"総合評価: {grade}")
    print(f"コメント: {comment}")
    print("=" * 50)


def create_ranking(*students):
    """成績ランキングを作成する（*args で可変長引数）"""
    # students は (名前, 平均点) のタプルのリスト
    sorted_students = sorted(students, key=lambda s: s[1], reverse=True)

    print("\n=== 成績ランキング ===")
    for rank, (name, avg) in enumerate(sorted_students, start=1):
        grade = get_grade(avg)
        medal = {1: "[1st]", 2: "[2nd]", 3: "[3rd]"}.get(rank, f"[{rank}th]")
        print(f"  {medal} {name}: {avg:.1f}点 (評価: {grade})")


def summarize_class(**kwargs):
    """クラス情報を表示する（**kwargs で可変長キーワード引数）"""
    print("\n=== クラス情報 ===")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")


# === メインプログラム ===

# 生徒データ
subjects = ["国語", "数学", "英語", "理科", "社会"]

students_data = [
    {"name": "太郎", "scores": [85, 92, 78, 90, 88]},
    {"name": "花子", "scores": [95, 88, 92, 85, 90]},
    {"name": "次郎", "scores": [70, 65, 72, 68, 75]},
    {"name": "美咲", "scores": [88, 95, 90, 92, 85]},
]

# 各生徒のレポートを表示
for student in students_data:
    print_report(student["name"], subjects, student["scores"])

# ランキング作成（*args に渡すためタプルのリストを展開）
ranking_data = [
    (s["name"], calculate_average(s["scores"]))
    for s in students_data
]
create_ranking(*ranking_data)

# クラス情報（**kwargs）
all_averages = [calculate_average(s["scores"]) for s in students_data]
summarize_class(
    クラス名="3年A組",
    生徒数=len(students_data),
    クラス平均=f"{calculate_average(all_averages):.1f}点",
    最高平均=f"{max(all_averages):.1f}点",
    科目数=len(subjects),
)

# === 対話モード ===
print("\n\n=== あなたの成績を入力 ===")
your_name = input("名前: ")
your_scores = []
for subject in subjects:
    score = int(input(f"  {subject}の点数: "))
    your_scores.append(score)

print_report(your_name, subjects, your_scores)

# あなたも含めたランキング
your_avg = calculate_average(your_scores)
ranking_data.append((your_name, your_avg))
create_ranking(*ranking_data)
