/**
 * ============================================================
 * 成績管理システム（Grade Management System）
 * ============================================================
 *
 * 【学べる内容】
 *   - 構造体（struct）の定義と使用
 *   - std::vector による動的配列管理
 *   - 関数の分割とプログラム設計
 *   - ソートアルゴリズム（std::sort + ラムダ式）
 *   - 統計計算（平均・最高・最低・標準偏差）
 *   - メニュー駆動型のプログラム構成
 *   - iomanip による表形式の出力
 *
 * 【実行方法】
 *   g++ -std=c++17 03_成績管理システム.cpp -o grades && ./grades
 *
 * 【テーマ】
 *   学生の成績を登録・管理し、統計分析を行うシステムです。
 *   教育現場で使われるような機能を備えています。
 * ============================================================
 */

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <iomanip>
#include <cmath>
#include <limits>

using namespace std;

// === 学生データを保持する構造体 ===
struct Student {
    int id;              // 学籍番号
    string name;         // 氏名
    int math;            // 数学の点数
    int english;         // 英語の点数
    int science;         // 理科の点数

    // 合計点を返すメンバ関数
    int total() const {
        return math + english + science;
    }

    // 平均点を返すメンバ関数
    double average() const {
        return total() / 3.0;
    }

    // 成績評価を返すメンバ関数
    string grade() const {
        double avg = average();
        if (avg >= 90) return "A+";
        if (avg >= 80) return "A";
        if (avg >= 70) return "B";
        if (avg >= 60) return "C";
        if (avg >= 50) return "D";
        return "F";
    }
};

// === 学生一覧をテーブル形式で表示する関数 ===
void printStudentTable(const vector<Student>& students) {
    if (students.empty()) {
        cout << "No students registered." << endl;
        return;
    }

    // ヘッダー行
    cout << string(76, '-') << endl;
    cout << "| " << setw(4)  << "ID"
         << " | " << setw(14) << "Name"
         << " | " << setw(5)  << "Math"
         << " | " << setw(5)  << "Eng"
         << " | " << setw(5)  << "Sci"
         << " | " << setw(5)  << "Total"
         << " | " << setw(6)  << "Avg"
         << " | " << setw(5)  << "Grade"
         << " |" << endl;
    cout << string(76, '-') << endl;

    // 各学生の行
    for (const auto& s : students) {
        cout << "| " << setw(4) << s.id
             << " | " << setw(14) << s.name
             << " | " << setw(5) << s.math
             << " | " << setw(5) << s.english
             << " | " << setw(5) << s.science
             << " | " << setw(5) << s.total()
             << " | " << fixed << setprecision(1) << setw(6) << s.average()
             << " | " << setw(5) << s.grade()
             << " |" << endl;
    }
    cout << string(76, '-') << endl;
    cout << "Total students: " << students.size() << endl;
}

// === 新しい学生を登録する関数 ===
void addStudent(vector<Student>& students, int& nextId) {
    Student s;
    s.id = nextId++;

    cout << endl;
    cout << "--- Register New Student (ID: " << s.id << ") ---" << endl;

    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Name: ";
    getline(cin, s.name);

    // 各科目の点数を入力（0-100の範囲チェック付き）
    auto inputScore = [](const string& subject) -> int {
        int score;
        do {
            cout << subject << " score (0-100): ";
            cin >> score;
            if (score < 0 || score > 100) {
                cout << "  Please enter 0-100." << endl;
            }
        } while (score < 0 || score > 100);
        return score;
    };

    s.math    = inputScore("Math");
    s.english = inputScore("English");
    s.science = inputScore("Science");

    students.push_back(s);

    cout << endl;
    cout << "Registered: " << s.name
         << " (Total: " << s.total()
         << ", Grade: " << s.grade() << ")" << endl;
}

// === 学生を名前で検索する関数 ===
void searchStudent(const vector<Student>& students) {
    if (students.empty()) {
        cout << "No students registered." << endl;
        return;
    }

    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Search name (partial match): ";
    string keyword;
    getline(cin, keyword);

    // 部分一致検索
    vector<Student> results;
    for (const auto& s : students) {
        if (s.name.find(keyword) != string::npos) {
            results.push_back(s);
        }
    }

    if (results.empty()) {
        cout << "No students found matching \"" << keyword << "\"." << endl;
    } else {
        cout << "Found " << results.size() << " student(s):" << endl;
        printStudentTable(results);
    }
}

// === 学生を削除する関数 ===
void deleteStudent(vector<Student>& students) {
    if (students.empty()) {
        cout << "No students registered." << endl;
        return;
    }

    printStudentTable(students);

    cout << "Enter ID to delete: ";
    int targetId;
    cin >> targetId;

    // erase-remove イディオムによる削除
    auto it = remove_if(students.begin(), students.end(),
                        [targetId](const Student& s) { return s.id == targetId; });

    if (it != students.end()) {
        cout << "Deleted student ID " << targetId << "." << endl;
        students.erase(it, students.end());
    } else {
        cout << "Student ID " << targetId << " not found." << endl;
    }
}

// === ソート機能 ===
void sortStudents(vector<Student>& students) {
    if (students.empty()) {
        cout << "No students registered." << endl;
        return;
    }

    cout << endl;
    cout << "--- Sort By ---" << endl;
    cout << "  1. ID (ascending)" << endl;
    cout << "  2. Name (ascending)" << endl;
    cout << "  3. Total score (descending)" << endl;
    cout << "  4. Math score (descending)" << endl;
    cout << "  5. English score (descending)" << endl;
    cout << "  6. Science score (descending)" << endl;
    cout << "Choice: ";

    int choice;
    cin >> choice;

    // ラムダ式を使ったソート
    switch (choice) {
        case 1:
            sort(students.begin(), students.end(),
                 [](const Student& a, const Student& b) { return a.id < b.id; });
            break;
        case 2:
            sort(students.begin(), students.end(),
                 [](const Student& a, const Student& b) { return a.name < b.name; });
            break;
        case 3:
            sort(students.begin(), students.end(),
                 [](const Student& a, const Student& b) { return a.total() > b.total(); });
            break;
        case 4:
            sort(students.begin(), students.end(),
                 [](const Student& a, const Student& b) { return a.math > b.math; });
            break;
        case 5:
            sort(students.begin(), students.end(),
                 [](const Student& a, const Student& b) { return a.english > b.english; });
            break;
        case 6:
            sort(students.begin(), students.end(),
                 [](const Student& a, const Student& b) { return a.science > b.science; });
            break;
        default:
            cout << "Invalid choice." << endl;
            return;
    }

    cout << "Sorted!" << endl;
    printStudentTable(students);
}

// === 統計情報を表示する関数 ===
void showStatistics(const vector<Student>& students) {
    if (students.empty()) {
        cout << "No students registered." << endl;
        return;
    }

    int n = static_cast<int>(students.size());

    // 各科目の統計を計算するラムダ
    auto calcStats = [&](const string& subject, auto getter) {
        vector<int> scores;
        for (const auto& s : students) {
            scores.push_back(getter(s));
        }

        int minScore = *min_element(scores.begin(), scores.end());
        int maxScore = *max_element(scores.begin(), scores.end());
        double sum   = accumulate(scores.begin(), scores.end(), 0.0);
        double avg   = sum / n;

        // 標準偏差の計算
        double variance = 0.0;
        for (int sc : scores) {
            variance += (sc - avg) * (sc - avg);
        }
        double stddev = sqrt(variance / n);

        cout << "  " << setw(10) << subject
             << " | Min: " << setw(3) << minScore
             << " | Max: " << setw(3) << maxScore
             << " | Avg: " << fixed << setprecision(1) << setw(5) << avg
             << " | StdDev: " << setw(5) << stddev
             << endl;
    };

    cout << endl;
    cout << "===== Statistics =====" << endl;
    cout << "  Students: " << n << endl;
    cout << endl;

    calcStats("Math",    [](const Student& s) { return s.math; });
    calcStats("English", [](const Student& s) { return s.english; });
    calcStats("Science", [](const Student& s) { return s.science; });
    calcStats("Total",   [](const Student& s) { return s.total(); });

    cout << endl;

    // 成績分布
    cout << "  --- Grade Distribution ---" << endl;
    vector<string> grades = {"A+", "A", "B", "C", "D", "F"};
    for (const auto& g : grades) {
        int count = 0;
        for (const auto& s : students) {
            if (s.grade() == g) count++;
        }
        // バーグラフの描画
        string bar(count * 3, '#');
        cout << "    " << setw(2) << g << ": " << bar
             << " (" << count << ")" << endl;
    }

    // トップ3の表示
    cout << endl;
    cout << "  --- Top 3 Students ---" << endl;
    vector<Student> sorted = students;
    sort(sorted.begin(), sorted.end(),
         [](const Student& a, const Student& b) { return a.total() > b.total(); });

    int showCount = min(3, n);
    for (int i = 0; i < showCount; i++) {
        string medal;
        if (i == 0) medal = "[1st]";
        else if (i == 1) medal = "[2nd]";
        else medal = "[3rd]";

        cout << "    " << medal << " " << sorted[i].name
             << " - Total: " << sorted[i].total()
             << " (Avg: " << fixed << setprecision(1) << sorted[i].average() << ")"
             << endl;
    }

    cout << "======================" << endl;
}

// === メインメニューの表示 ===
void showMenu() {
    cout << endl;
    cout << "=============================" << endl;
    cout << "   Grade Management System" << endl;
    cout << "=============================" << endl;
    cout << "  1. Add student" << endl;
    cout << "  2. Show all students" << endl;
    cout << "  3. Search student" << endl;
    cout << "  4. Delete student" << endl;
    cout << "  5. Sort students" << endl;
    cout << "  6. Show statistics" << endl;
    cout << "  0. Exit" << endl;
    cout << "-----------------------------" << endl;
    cout << "Choice: ";
}

int main() {
    vector<Student> students;  // 学生データの格納先
    int nextId = 1;            // 次に割り当てるID

    // サンプルデータの投入（デモ用）
    cout << "Load sample data? (1: Yes / 0: No): ";
    int loadSample;
    cin >> loadSample;

    if (loadSample == 1) {
        students = {
            {nextId++, "Tanaka",   85, 72, 91},
            {nextId++, "Suzuki",   60, 88, 75},
            {nextId++, "Sato",     95, 90, 88},
            {nextId++, "Yamada",   45, 55, 62},
            {nextId++, "Watanabe", 78, 82, 70}
        };
        cout << "Loaded 5 sample students." << endl;
    }

    // メインループ
    while (true) {
        showMenu();

        int choice;
        cin >> choice;

        switch (choice) {
            case 1: addStudent(students, nextId);   break;
            case 2: printStudentTable(students);     break;
            case 3: searchStudent(students);         break;
            case 4: deleteStudent(students);         break;
            case 5: sortStudents(students);          break;
            case 6: showStatistics(students);        break;
            case 0:
                cout << "Goodbye!" << endl;
                return 0;
            default:
                cout << "Invalid choice." << endl;
        }
    }

    return 0;
}
