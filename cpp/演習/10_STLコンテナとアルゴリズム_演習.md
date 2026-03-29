# 第10章：STLコンテナとアルゴリズム - 演習問題

---

## 問題1：単語出現回数（基本）

文章中の各単語の出現回数を `std::map` を使ってカウントし、出現回数の多い順に表示するプログラムを作成してください。

- 単語は空白で区切られるものとします
- 出現回数が同じ場合はアルファベット順で表示します

```cpp
int main() {
    std::string text = "apple banana apple cherry banana apple date cherry banana";
    // ここに処理を記述
    return 0;
}
```

**期待される出力：**
```
apple: 3回
banana: 3回
cherry: 2回
date: 1回
```

<details>
<summary>ヒント</summary>

- `std::istringstream` を使うと文字列から単語を1つずつ取り出せます
- `std::map<std::string, int>` で単語と出現回数を管理します
- ソートには `std::vector<std::pair<std::string, int>>` に変換してから `std::sort` を使います
- カスタム比較関数で出現回数降順、同数ならアルファベット順にソートします

</details>

<details>
<summary>解答例</summary>

```cpp
#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <sstream>
#include <algorithm>

int main() {
    std::string text = "apple banana apple cherry banana apple date cherry banana";

    // 単語を分割してカウント
    std::map<std::string, int> wordCount;
    std::istringstream iss(text);
    std::string word;
    while (iss >> word) {
        wordCount[word]++;
    }

    // ソート用にvectorに変換
    std::vector<std::pair<std::string, int>> sorted(wordCount.begin(), wordCount.end());

    // 出現回数降順、同数ならアルファベット順でソート
    std::sort(sorted.begin(), sorted.end(),
        [](const auto& a, const auto& b) {
            if (a.second != b.second) return a.second > b.second;
            return a.first < b.first;
        });

    // 結果を表示
    for (const auto& [w, count] : sorted) {
        std::cout << w << ": " << count << "回" << std::endl;
    }

    return 0;
}
```

</details>

---

## 問題2：ソートと検索（基本）

整数の `std::vector` に対して以下の操作を行うプログラムを作成してください。

1. 昇順にソート
2. 重複を除去
3. 二分探索で指定した値が存在するか確認
4. 条件を満たす要素数をカウント

```cpp
int main() {
    std::vector<int> nums = {5, 3, 8, 1, 9, 2, 7, 3, 5, 1, 8, 4, 6};

    // 1. 昇順ソート → 表示
    // 2. 重複除去 → 表示
    // 3. 二分探索で 5 と 10 を検索
    // 4. 5以上の要素数をカウント

    return 0;
}
```

**期待される出力：**
```
ソート後: 1 1 2 3 3 4 5 5 6 7 8 8 9
重複除去後: 1 2 3 4 5 6 7 8 9
5 は見つかりました
10 は見つかりませんでした
5以上の要素数: 5
```

<details>
<summary>ヒント</summary>

- `std::sort` でソートします
- 重複除去は `std::unique` と `erase` の組み合わせで行います（erase-remove イディオム）
- 二分探索は `std::binary_search` を使います
- 条件カウントは `std::count_if` を使います

</details>

<details>
<summary>解答例</summary>

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> nums = {5, 3, 8, 1, 9, 2, 7, 3, 5, 1, 8, 4, 6};

    // 1. 昇順ソート
    std::sort(nums.begin(), nums.end());
    std::cout << "ソート後: ";
    for (int n : nums) std::cout << n << " ";
    std::cout << std::endl;

    // 2. 重複除去（sortされている前提）
    nums.erase(std::unique(nums.begin(), nums.end()), nums.end());
    std::cout << "重複除去後: ";
    for (int n : nums) std::cout << n << " ";
    std::cout << std::endl;

    // 3. 二分探索
    if (std::binary_search(nums.begin(), nums.end(), 5)) {
        std::cout << "5 は見つかりました" << std::endl;
    } else {
        std::cout << "5 は見つかりませんでした" << std::endl;
    }

    if (std::binary_search(nums.begin(), nums.end(), 10)) {
        std::cout << "10 は見つかりました" << std::endl;
    } else {
        std::cout << "10 は見つかりませんでした" << std::endl;
    }

    // 4. 5以上の要素数をカウント
    int count = std::count_if(nums.begin(), nums.end(),
        [](int n) { return n >= 5; });
    std::cout << "5以上の要素数: " << count << std::endl;

    return 0;
}
```

</details>

---

## 問題3：フィルタリング（応用）

構造体 `Student` のベクタに対して、STLアルゴリズムとラムダ式を使って各種フィルタリング・集計を行ってください。

```cpp
struct Student {
    std::string name;
    int age;
    double score;
};

int main() {
    std::vector<Student> students = {
        {"太郎", 20, 85.5},
        {"花子", 19, 92.0},
        {"次郎", 21, 78.3},
        {"美咲", 20, 95.8},
        {"健太", 22, 68.0},
        {"由美", 19, 88.5},
        {"大輔", 21, 72.0},
        {"さくら", 20, 91.2}
    };

    // 1. スコアの降順でソートして全員表示
    // 2. スコアが80以上の学生を表示
    // 3. 平均スコアを計算
    // 4. 最高スコアと最低スコアの学生を表示
    // 5. 20歳の学生数を表示

    return 0;
}
```

**期待される出力：**
```
=== スコア降順 ===
美咲 (20歳) 95.8点
花子 (19歳) 92.0点
さくら (20歳) 91.2点
由美 (19歳) 88.5点
太郎 (20歳) 85.5点
次郎 (21歳) 78.3点
大輔 (21歳) 72.0点
健太 (22歳) 68.0点

=== 80点以上の学生 ===
美咲 花子 さくら 由美 太郎

平均スコア: 83.9点
最高スコア: 美咲 (95.8点)
最低スコア: 健太 (68.0点)
20歳の学生数: 3人
```

<details>
<summary>ヒント</summary>

- `std::sort` にラムダ式を渡してスコア降順にソートします
- `std::copy_if` や範囲forでフィルタリングします
- `std::accumulate` でスコアの合計を求め、人数で割ります
- `std::min_element` / `std::max_element` で最高・最低を求めます
- `std::count_if` で条件に合う人数をカウントします
- 小数点以下1桁で表示するには `std::fixed` と `std::setprecision` を使います

</details>

<details>
<summary>解答例</summary>

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>
#include <iomanip>

struct Student {
    std::string name;
    int age;
    double score;
};

int main() {
    std::vector<Student> students = {
        {"太郎", 20, 85.5},
        {"花子", 19, 92.0},
        {"次郎", 21, 78.3},
        {"美咲", 20, 95.8},
        {"健太", 22, 68.0},
        {"由美", 19, 88.5},
        {"大輔", 21, 72.0},
        {"さくら", 20, 91.2}
    };

    // 1. スコアの降順でソート
    std::sort(students.begin(), students.end(),
        [](const Student& a, const Student& b) {
            return a.score > b.score;
        });

    std::cout << "=== スコア降順 ===" << std::endl;
    std::cout << std::fixed << std::setprecision(1);
    for (const auto& s : students) {
        std::cout << s.name << " (" << s.age << "歳) "
                  << s.score << "点" << std::endl;
    }

    // 2. 80点以上の学生
    std::cout << "\n=== 80点以上の学生 ===" << std::endl;
    for (const auto& s : students) {
        if (s.score >= 80.0) {
            std::cout << s.name << " ";
        }
    }
    std::cout << std::endl;

    // 3. 平均スコア
    double total = std::accumulate(students.begin(), students.end(), 0.0,
        [](double sum, const Student& s) { return sum + s.score; });
    std::cout << "\n平均スコア: " << (total / students.size()) << "点" << std::endl;

    // 4. 最高・最低スコアの学生
    auto maxIt = std::max_element(students.begin(), students.end(),
        [](const Student& a, const Student& b) { return a.score < b.score; });
    auto minIt = std::min_element(students.begin(), students.end(),
        [](const Student& a, const Student& b) { return a.score < b.score; });

    std::cout << "最高スコア: " << maxIt->name << " (" << maxIt->score << "点)" << std::endl;
    std::cout << "最低スコア: " << minIt->name << " (" << minIt->score << "点)" << std::endl;

    // 5. 20歳の学生数
    int count20 = std::count_if(students.begin(), students.end(),
        [](const Student& s) { return s.age == 20; });
    std::cout << "20歳の学生数: " << count20 << "人" << std::endl;

    return 0;
}
```

</details>

---

## 問題4：集合演算（応用）

`std::set` を使って、2つの集合に対する以下の集合演算を実装してください。

1. 和集合（union）
2. 積集合（intersection）
3. 差集合（difference）
4. 対称差（symmetric difference）

```cpp
int main() {
    std::set<int> A = {1, 2, 3, 4, 5, 6};
    std::set<int> B = {4, 5, 6, 7, 8, 9};

    // 各集合演算の結果を表示
    return 0;
}
```

**期待される出力：**
```
集合A: {1, 2, 3, 4, 5, 6}
集合B: {4, 5, 6, 7, 8, 9}
和集合 (A∪B): {1, 2, 3, 4, 5, 6, 7, 8, 9}
積集合 (A∩B): {4, 5, 6}
差集合 (A-B): {1, 2, 3}
差集合 (B-A): {7, 8, 9}
対称差 (A△B): {1, 2, 3, 7, 8, 9}
```

<details>
<summary>ヒント</summary>

- `std::set_union` で和集合を求めます
- `std::set_intersection` で積集合を求めます
- `std::set_difference` で差集合を求めます
- `std::set_symmetric_difference` で対称差を求めます
- 結果を格納するには `std::inserter` を使います
- `std::set` は自動的にソートされているため、これらのアルゴリズムがそのまま使えます

</details>

<details>
<summary>解答例</summary>

```cpp
#include <iostream>
#include <set>
#include <algorithm>
#include <iterator>

// setの内容を表示するヘルパー関数
void printSet(const std::string& label, const std::set<int>& s) {
    std::cout << label << ": {";
    bool first = true;
    for (int v : s) {
        if (!first) std::cout << ", ";
        std::cout << v;
        first = false;
    }
    std::cout << "}" << std::endl;
}

int main() {
    std::set<int> A = {1, 2, 3, 4, 5, 6};
    std::set<int> B = {4, 5, 6, 7, 8, 9};

    printSet("集合A", A);
    printSet("集合B", B);

    // 和集合
    std::set<int> unionSet;
    std::set_union(A.begin(), A.end(), B.begin(), B.end(),
                   std::inserter(unionSet, unionSet.begin()));
    printSet("和集合 (A∪B)", unionSet);

    // 積集合
    std::set<int> intersectionSet;
    std::set_intersection(A.begin(), A.end(), B.begin(), B.end(),
                          std::inserter(intersectionSet, intersectionSet.begin()));
    printSet("積集合 (A∩B)", intersectionSet);

    // 差集合 (A-B)
    std::set<int> diffAB;
    std::set_difference(A.begin(), A.end(), B.begin(), B.end(),
                        std::inserter(diffAB, diffAB.begin()));
    printSet("差集合 (A-B)", diffAB);

    // 差集合 (B-A)
    std::set<int> diffBA;
    std::set_difference(B.begin(), B.end(), A.begin(), A.end(),
                        std::inserter(diffBA, diffBA.begin()));
    printSet("差集合 (B-A)", diffBA);

    // 対称差
    std::set<int> symDiff;
    std::set_symmetric_difference(A.begin(), A.end(), B.begin(), B.end(),
                                  std::inserter(symDiff, symDiff.begin()));
    printSet("対称差 (A△B)", symDiff);

    return 0;
}
```

</details>

---

## 問題5：成績統計（応用）

`std::map` と STLアルゴリズムを組み合わせて、科目ごとの成績統計を計算するプログラムを作成してください。

- 各学生の複数科目の点数を管理
- 科目ごとの平均点を計算
- 学生ごとの総合得点を計算してランキングを作成
- 全科目で80点以上の学生を特定

```cpp
int main() {
    // 学生名 → (科目名 → 点数)
    std::map<std::string, std::map<std::string, int>> grades = {
        {"太郎", {{"数学", 85}, {"英語", 72}, {"国語", 90}}},
        {"花子", {{"数学", 92}, {"英語", 88}, {"国語", 85}}},
        {"次郎", {{"数学", 78}, {"英語", 65}, {"国語", 82}}},
        {"美咲", {{"数学", 95}, {"英語", 91}, {"国語", 88}}}
    };

    // 1. 科目ごとの平均点
    // 2. 総合得点ランキング
    // 3. 全科目80点以上の学生

    return 0;
}
```

**期待される出力：**
```
=== 科目別平均点 ===
英語: 79.0点
国語: 86.2点
数学: 87.5点

=== 総合得点ランキング ===
1位: 美咲 (274点)
2位: 花子 (265点)
3位: 太郎 (247点)
4位: 次郎 (225点)

=== 全科目80点以上の学生 ===
花子
美咲
```

<details>
<summary>ヒント</summary>

- 科目別平均は、全学生を走査して科目ごとに合計と人数を集計します
- ランキングは `std::vector<std::pair<std::string, int>>` に変換してソートします
- 全科目80点以上かの判定は `std::all_of` が使えます

</details>

<details>
<summary>解答例</summary>

```cpp
#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>

int main() {
    // 学生名 → (科目名 → 点数)
    std::map<std::string, std::map<std::string, int>> grades = {
        {"太郎", {{"数学", 85}, {"英語", 72}, {"国語", 90}}},
        {"花子", {{"数学", 92}, {"英語", 88}, {"国語", 85}}},
        {"次郎", {{"数学", 78}, {"英語", 65}, {"国語", 82}}},
        {"美咲", {{"数学", 95}, {"英語", 91}, {"国語", 88}}}
    };

    // 1. 科目ごとの平均点
    std::map<std::string, double> subjectAvg;
    std::map<std::string, int> subjectCount;

    for (const auto& [student, subjects] : grades) {
        for (const auto& [subject, score] : subjects) {
            subjectAvg[subject] += score;
            subjectCount[subject]++;
        }
    }

    std::cout << "=== 科目別平均点 ===" << std::endl;
    std::cout << std::fixed << std::setprecision(1);
    for (auto& [subject, total] : subjectAvg) {
        total /= subjectCount[subject];
        std::cout << subject << ": " << total << "点" << std::endl;
    }

    // 2. 総合得点ランキング
    std::vector<std::pair<std::string, int>> ranking;
    for (const auto& [student, subjects] : grades) {
        int total = 0;
        for (const auto& [subject, score] : subjects) {
            total += score;
        }
        ranking.push_back({student, total});
    }

    std::sort(ranking.begin(), ranking.end(),
        [](const auto& a, const auto& b) { return a.second > b.second; });

    std::cout << "\n=== 総合得点ランキング ===" << std::endl;
    for (size_t i = 0; i < ranking.size(); ++i) {
        std::cout << (i + 1) << "位: " << ranking[i].first
                  << " (" << ranking[i].second << "点)" << std::endl;
    }

    // 3. 全科目80点以上の学生
    std::cout << "\n=== 全科目80点以上の学生 ===" << std::endl;
    for (const auto& [student, subjects] : grades) {
        bool allAbove80 = std::all_of(subjects.begin(), subjects.end(),
            [](const auto& pair) { return pair.second >= 80; });
        if (allAbove80) {
            std::cout << student << std::endl;
        }
    }

    return 0;
}
```

</details>

---

## 問題6：タスク管理システム（チャレンジ）

STLコンテナとアルゴリズムを活用して、簡易タスク管理システムを作成してください。以下の機能を実装します。

- タスクの追加（タイトル、優先度、期限、完了フラグ）
- 優先度順にソート
- 未完了タスクのフィルタリング
- 優先度別のタスク数集計
- タスクの検索（タイトルに指定文字列を含むもの）

```cpp
enum class Priority { LOW, MEDIUM, HIGH, CRITICAL };

struct Task {
    int id;
    std::string title;
    Priority priority;
    std::string deadline;
    bool completed;
};

// 以下の機能を実装してテストしてください
```

**期待される出力：**
```
=== 全タスク（優先度順） ===
[CRITICAL] #5 セキュリティパッチ適用 (期限: 2026-04-01) [未完了]
[HIGH] #1 ログイン機能実装 (期限: 2026-04-05) [未完了]
[HIGH] #4 バグ修正: メモリリーク (期限: 2026-04-03) [完了]
[MEDIUM] #2 ユーザー一覧画面 (期限: 2026-04-10) [未完了]
[MEDIUM] #6 テスト追加 (期限: 2026-04-12) [未完了]
[LOW] #3 READMEの更新 (期限: 2026-04-15) [完了]

=== 未完了タスク ===
[CRITICAL] #5 セキュリティパッチ適用
[HIGH] #1 ログイン機能実装
[MEDIUM] #2 ユーザー一覧画面
[MEDIUM] #6 テスト追加

=== 優先度別タスク数 ===
CRITICAL: 1件
HIGH: 2件
MEDIUM: 2件
LOW: 1件

=== 検索: "バグ" ===
[HIGH] #4 バグ修正: メモリリーク
```

<details>
<summary>ヒント</summary>

- `enum class` の値を文字列に変換する関数を用意すると便利です
- ソートは `std::sort` にカスタム比較関数を渡します
- 未完了タスクの抽出には `std::copy_if` が使えます
- 優先度別集計には `std::map<Priority, int>` を使います
- タイトル検索には `std::string::find` と `std::string::npos` を使います

</details>

<details>
<summary>解答例</summary>

```cpp
#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <algorithm>

enum class Priority { LOW, MEDIUM, HIGH, CRITICAL };

struct Task {
    int id;
    std::string title;
    Priority priority;
    std::string deadline;
    bool completed;
};

// 優先度を文字列に変換
std::string priorityToString(Priority p) {
    switch (p) {
        case Priority::LOW:      return "LOW";
        case Priority::MEDIUM:   return "MEDIUM";
        case Priority::HIGH:     return "HIGH";
        case Priority::CRITICAL: return "CRITICAL";
    }
    return "UNKNOWN";
}

// 優先度を数値に変換（ソート用、大きいほど高優先度）
int priorityToInt(Priority p) {
    switch (p) {
        case Priority::LOW:      return 0;
        case Priority::MEDIUM:   return 1;
        case Priority::HIGH:     return 2;
        case Priority::CRITICAL: return 3;
    }
    return -1;
}

// タスクを1行で表示
void printTask(const Task& t, bool showDeadline = true) {
    std::cout << "[" << priorityToString(t.priority) << "] #" << t.id
              << " " << t.title;
    if (showDeadline) {
        std::cout << " (期限: " << t.deadline << ") "
                  << (t.completed ? "[完了]" : "[未完了]");
    }
    std::cout << std::endl;
}

int main() {
    std::vector<Task> tasks = {
        {1, "ログイン機能実装",       Priority::HIGH,     "2026-04-05", false},
        {2, "ユーザー一覧画面",       Priority::MEDIUM,   "2026-04-10", false},
        {3, "READMEの更新",           Priority::LOW,      "2026-04-15", true},
        {4, "バグ修正: メモリリーク",  Priority::HIGH,     "2026-04-03", true},
        {5, "セキュリティパッチ適用",  Priority::CRITICAL, "2026-04-01", false},
        {6, "テスト追加",             Priority::MEDIUM,   "2026-04-12", false}
    };

    // 1. 優先度順にソート（同じ優先度ならID順）
    std::sort(tasks.begin(), tasks.end(),
        [](const Task& a, const Task& b) {
            if (priorityToInt(a.priority) != priorityToInt(b.priority))
                return priorityToInt(a.priority) > priorityToInt(b.priority);
            return a.id < b.id;
        });

    std::cout << "=== 全タスク（優先度順） ===" << std::endl;
    for (const auto& t : tasks) {
        printTask(t);
    }

    // 2. 未完了タスクのフィルタリング
    std::vector<Task> incomplete;
    std::copy_if(tasks.begin(), tasks.end(), std::back_inserter(incomplete),
        [](const Task& t) { return !t.completed; });

    std::cout << "\n=== 未完了タスク ===" << std::endl;
    for (const auto& t : incomplete) {
        printTask(t, false);
    }

    // 3. 優先度別のタスク数集計
    std::map<Priority, int> countByPriority;
    for (const auto& t : tasks) {
        countByPriority[t.priority]++;
    }

    std::cout << "\n=== 優先度別タスク数 ===" << std::endl;
    // 高い優先度から表示
    for (auto p : {Priority::CRITICAL, Priority::HIGH, Priority::MEDIUM, Priority::LOW}) {
        if (countByPriority.count(p)) {
            std::cout << priorityToString(p) << ": "
                      << countByPriority[p] << "件" << std::endl;
        }
    }

    // 4. タスクの検索
    std::string keyword = "バグ";
    std::cout << "\n=== 検索: \"" << keyword << "\" ===" << std::endl;
    for (const auto& t : tasks) {
        if (t.title.find(keyword) != std::string::npos) {
            printTask(t, false);
        }
    }

    return 0;
}
```

</details>

---
