/*
 * ============================================================
 *  自己紹介カード生成プログラム
 * ============================================================
 *
 *  【学べる内容】
 *    - 変数の宣言（let, let mut）と型推論
 *    - 基本データ型（i32, f64, bool, String, &str）
 *    - 標準入力からの読み取り（std::io::stdin）
 *    - 文字列のフォーマット（format!, println!）
 *    - 所有権の基本（String と &str の違い）
 *    - 関数の定義と戻り値
 *
 *  【実行方法】
 *    rustc 01_自己紹介カード.rs && ./01_自己紹介カード
 *
 * ============================================================
 */

use std::io;

// ────────────────────────────────────────
//  入力補助関数
//  標準入力から1行読み取って返す
// ────────────────────────────────────────
fn read_line(prompt: &str) -> String {
    println!("{}", prompt);
    print!("> ");
    // print! はバッファリングされるので flush が必要
    use std::io::Write;
    io::stdout().flush().unwrap();

    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("入力の読み取りに失敗しました");
    // 末尾の改行を除去して返す
    input.trim().to_string()
}

// ────────────────────────────────────────
//  自己紹介カードを表す構造体
// ────────────────────────────────────────
struct ProfileCard {
    name: String,       // 名前（String型 = ヒープに確保される可変長文字列）
    age: u32,           // 年齢（符号なし32ビット整数）
    hobby: String,      // 趣味
    language: String,   // 好きなプログラミング言語
    is_student: bool,   // 学生かどうか（真偽値）
}

impl ProfileCard {
    // 自己紹介カードを装飾付きで表示するメソッド
    fn display(&self) {
        let border = "╔══════════════════════════════════════╗";
        let bottom = "╚══════════════════════════════════════╝";
        let sep    = "╟──────────────────────────────────────╢";

        // 身分の表示を三項演算子風に決定
        let status = if self.is_student {
            "学生"
        } else {
            "社会人"
        };

        println!();
        println!("{}", border);
        println!("║        ★ 自己紹介カード ★           ║");
        println!("{}", sep);
        println!("║  名前     : {:<24} ║", self.name);
        println!("║  年齢     : {:<24} ║", format!("{}歳", self.age));
        println!("║  身分     : {:<24} ║", status);
        println!("║  趣味     : {:<24} ║", self.hobby);
        println!("║  推し言語 : {:<24} ║", self.language);
        println!("{}", bottom);
        println!();
    }

    // カードの情報を1行サマリーで返す関数（戻り値の例）
    fn summary(&self) -> String {
        format!(
            "{}さん（{}歳）- 趣味: {}, 推し言語: {}",
            self.name, self.age, self.hobby, self.language
        )
    }
}

// ────────────────────────────────────────
//  年齢の文字列を数値に変換する関数
//  パースに失敗したらデフォルト値を返す
// ────────────────────────────────────────
fn parse_age(input: &str, default: u32) -> u32 {
    // parse() は Result型を返す
    // unwrap_or() でエラー時のデフォルト値を指定
    input.parse::<u32>().unwrap_or(default)
}

// ────────────────────────────────────────
//  基本型のデモ表示
// ────────────────────────────────────────
fn show_type_demo() {
    println!("=== Rust の基本データ型デモ ===\n");

    // 整数型
    let integer: i32 = 42;          // 符号あり32ビット整数
    let unsigned: u64 = 100;        // 符号なし64ビット整数

    // 浮動小数点型
    let pi: f64 = 3.14159;          // 64ビット浮動小数点

    // 真偽値型
    let is_rust_fun: bool = true;   // true または false

    // 文字型（Unicode 1文字）
    let emoji: char = '🦀';         // Rustのマスコット「カニ」

    // 文字列型
    let greeting: &str = "こんにちは";          // 文字列スライス（不変）
    let mut message = String::from("Rust");     // String型（可変）
    message.push_str("は楽しい！");             // 文字列の追加

    println!("  整数 (i32)     : {}", integer);
    println!("  整数 (u64)     : {}", unsigned);
    println!("  小数 (f64)     : {}", pi);
    println!("  真偽値 (bool)  : {}", is_rust_fun);
    println!("  文字 (char)    : {}", emoji);
    println!("  &str           : {}", greeting);
    println!("  String         : {}", message);
    println!();
}

// ────────────────────────────────────────
//  メイン関数
// ────────────────────────────────────────
fn main() {
    println!("╔══════════════════════════════════════╗");
    println!("║    自己紹介カード作成プログラム      ║");
    println!("╚══════════════════════════════════════╝");
    println!();

    // まず基本型のデモを表示
    show_type_demo();

    println!("--- あなたの自己紹介カードを作りましょう！ ---\n");

    // 標準入力から情報を取得
    let name = read_line("お名前を入力してください：");
    let age_str = read_line("年齢を入力してください（数字）：");
    let hobby = read_line("趣味を入力してください：");
    let language = read_line("好きなプログラミング言語を入力してください：");
    let student_input = read_line("学生ですか？（y/n）：");

    // 年齢を数値に変換（パース失敗時は20をデフォルトに）
    let age = parse_age(&age_str, 20);

    // 学生かどうかを判定
    // starts_with で先頭文字をチェック
    let is_student = student_input.starts_with('y')
        || student_input.starts_with('Y')
        || student_input == "はい";

    // 構造体のインスタンスを生成
    let card = ProfileCard {
        name,        // フィールド名と変数名が同じなら省略記法が使える
        age,
        hobby,
        language,
        is_student,
    };

    // カードを表示
    card.display();

    // サマリーも表示
    println!("【サマリー】{}", card.summary());
    println!();
    println!("カードの作成が完了しました！お疲れさまでした。");
}
