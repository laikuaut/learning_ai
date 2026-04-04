/*
 * ============================================================
 *  成績管理システム
 * ============================================================
 *
 *  【学べる内容】
 *    - 構造体（struct）の定義とメソッド実装（impl）
 *    - ベクタ（Vec<T>）の操作（push, iter, len）
 *    - イテレータとクロージャ（map, filter, fold, for_each）
 *    - 列挙型（enum）の活用
 *    - 参照と借用（&, &mut）
 *    - パターンマッチング（match）
 *
 *  【実行方法】
 *    rustc 03_成績管理システム.rs && ./03_成績管理システム
 *
 * ============================================================
 */

use std::io;
use std::io::Write;

// ────────────────────────────────────────
//  成績の評価ランク（列挙型）
// ────────────────────────────────────────
#[derive(Debug, Clone)]   // Debug: {:?}で表示可能, Clone: 複製可能
enum Grade {
    S,  // 90点以上
    A,  // 80点以上
    B,  // 70点以上
    C,  // 60点以上
    F,  // 60点未満（不合格）
}

impl Grade {
    /// 点数から評価ランクを判定する関連関数
    fn from_score(score: u32) -> Grade {
        match score {
            90..=100 => Grade::S,
            80..=89  => Grade::A,
            70..=79  => Grade::B,
            60..=69  => Grade::C,
            _        => Grade::F,
        }
    }

    /// ランクの表示名を返す
    fn label(&self) -> &str {
        match self {
            Grade::S => "S（秀）",
            Grade::A => "A（優）",
            Grade::B => "B（良）",
            Grade::C => "C（可）",
            Grade::F => "F（不可）",
        }
    }
}

// ────────────────────────────────────────
//  学生を表す構造体
// ────────────────────────────────────────
#[derive(Debug, Clone)]
struct Student {
    name: String,
    scores: Vec<u32>,  // 科目ごとの点数を格納するベクタ
}

impl Student {
    /// 新しい学生を作成するコンストラクタ
    fn new(name: &str) -> Student {
        Student {
            name: name.to_string(),
            scores: Vec::new(),  // 空のベクタで初期化
        }
    }

    /// 成績を追加する（可変参照 &mut self が必要）
    fn add_score(&mut self, score: u32) {
        self.scores.push(score);
    }

    /// 平均点を計算する（イテレータの fold を活用）
    fn average(&self) -> f64 {
        if self.scores.is_empty() {
            return 0.0;
        }
        // fold: 初期値 0 から累積的に合計を計算
        let total: u32 = self.scores.iter().fold(0, |acc, &score| acc + score);
        total as f64 / self.scores.len() as f64
    }

    /// 最高点を取得（イテレータの max を使用）
    fn max_score(&self) -> u32 {
        // copied() で &u32 を u32 に変換
        self.scores.iter().copied().max().unwrap_or(0)
    }

    /// 最低点を取得
    fn min_score(&self) -> u32 {
        self.scores.iter().copied().min().unwrap_or(0)
    }

    /// 総合評価を取得
    fn overall_grade(&self) -> Grade {
        Grade::from_score(self.average().round() as u32)
    }

    /// 成績表を表示
    fn display_report(&self) {
        let subjects = ["国語", "数学", "英語", "理科", "社会"];

        println!("┌────────────────────────────────────┐");
        println!("│  📋 成績表: {:<22} │", self.name);
        println!("├────────────────────────────────────┤");

        // iter().enumerate() でインデックスと値を同時に取得
        for (i, &score) in self.scores.iter().enumerate() {
            let subject = if i < subjects.len() {
                subjects[i]
            } else {
                "その他"
            };
            let grade = Grade::from_score(score);
            println!(
                "│  {} : {:>3}点  [{}] {:>12} │",
                subject,
                score,
                grade.label(),
                ""  // スペース調整用
            );
        }

        println!("├────────────────────────────────────┤");
        println!("│  平均点 : {:>6.1}点                 │", self.average());
        println!("│  最高点 : {:>3}点                    │", self.max_score());
        println!("│  最低点 : {:>3}点                    │", self.min_score());
        println!(
            "│  総合評価 : {:<24} │",
            self.overall_grade().label()
        );
        println!("└────────────────────────────────────┘");
    }
}

// ────────────────────────────────────────
//  クラス全体を管理する構造体
// ────────────────────────────────────────
struct Classroom {
    students: Vec<Student>,
}

impl Classroom {
    fn new() -> Classroom {
        Classroom {
            students: Vec::new(),
        }
    }

    /// 学生を追加
    fn add_student(&mut self, student: Student) {
        self.students.push(student);
    }

    /// クラス全体の平均点
    fn class_average(&self) -> f64 {
        if self.students.is_empty() {
            return 0.0;
        }
        let total: f64 = self.students.iter().map(|s| s.average()).sum();
        total / self.students.len() as f64
    }

    /// 成績上位の学生を取得（イテレータの filter + collect）
    fn top_students(&self, min_avg: f64) -> Vec<&Student> {
        self.students
            .iter()
            .filter(|s| s.average() >= min_avg)
            .collect()
    }

    /// 全学生の一覧表示
    fn display_summary(&self) {
        println!("\n╔══════════════════════════════════════╗");
        println!("║       📊 クラス成績サマリー         ║");
        println!("╚══════════════════════════════════════╝\n");

        // for_each を使ったイテレータ処理
        self.students.iter().for_each(|s| {
            println!(
                "  {} : 平均 {:.1}点 [{}]",
                s.name,
                s.average(),
                s.overall_grade().label()
            );
        });

        println!("\n  --- クラス平均: {:.1}点 ---", self.class_average());

        // 成績優秀者（平均80点以上）
        let honor_students = self.top_students(80.0);
        if !honor_students.is_empty() {
            println!("\n  🏆 成績優秀者（平均80点以上）:");
            for s in &honor_students {
                println!("    ・{} ({:.1}点)", s.name, s.average());
            }
        }
    }
}

// ────────────────────────────────────────
//  入力補助
// ────────────────────────────────────────
fn read_input(prompt: &str) -> String {
    print!("{}", prompt);
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    input.trim().to_string()
}

// ────────────────────────────────────────
//  メイン関数
// ────────────────────────────────────────
fn main() {
    println!("╔══════════════════════════════════════╗");
    println!("║      📚 成績管理システム 📚          ║");
    println!("╚══════════════════════════════════════╝");
    println!();

    // まずサンプルデータで動作を確認
    println!("--- サンプルデータでデモを実行します ---\n");

    let mut classroom = Classroom::new();

    // サンプル学生データを作成
    let sample_data = vec![
        ("田中太郎", vec![85, 92, 78, 88, 95]),
        ("鈴木花子", vec![92, 88, 95, 90, 87]),
        ("佐藤次郎", vec![65, 58, 72, 60, 55]),
        ("山田美咲", vec![78, 82, 76, 85, 80]),
    ];

    for (name, scores) in &sample_data {
        let mut student = Student::new(name);
        for &score in scores {
            student.add_score(score);
        }
        student.display_report();
        println!();
        classroom.add_student(student);
    }

    classroom.display_summary();

    // ユーザーによる学生追加
    println!("\n--- 新しい学生を追加できます ---\n");

    loop {
        let name = read_input("学生の名前を入力（終了は q）> ");
        if name == "q" || name == "Q" {
            break;
        }

        let mut student = Student::new(&name);
        let subjects = ["国語", "数学", "英語", "理科", "社会"];

        for subject in &subjects {
            let score_str = read_input(&format!("  {}の点数 (0-100) > ", subject));
            let score: u32 = score_str.parse().unwrap_or(0).min(100);
            student.add_score(score);
        }

        student.display_report();
        classroom.add_student(student);
        println!();
    }

    // 最終サマリー
    classroom.display_summary();
    println!("\nプログラムを終了します。お疲れさまでした！");
}
