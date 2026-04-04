/*
 * ============================================================
 *  ミニ電卓プログラム
 * ============================================================
 *
 *  【学べる内容】
 *    - enum（列挙型）で演算の種類を表現
 *    - match による網羅的なパターンマッチング
 *    - 関数の定義と戻り値（Result型）
 *    - エラー処理の設計（カスタムエラー型）
 *    - 文字列のパース（トークン分割）
 *    - Option型の活用
 *    - 履歴機能（Vec を使った状態管理）
 *
 *  【実行方法】
 *    rustc 05_ミニ電卓.rs && ./05_ミニ電卓
 *
 * ============================================================
 */

use std::fmt;
use std::io;
use std::io::Write;

// ────────────────────────────────────────
//  演算の種類を表す列挙型
// ────────────────────────────────────────
#[derive(Debug, Clone)]
enum Operator {
    Add,       // 加算 +
    Subtract,  // 減算 -
    Multiply,  // 乗算 *
    Divide,    // 除算 /
    Modulo,    // 剰余 %
    Power,     // 累乗 ^
}

impl Operator {
    /// 文字列から演算子を解析する
    fn from_str(s: &str) -> Option<Operator> {
        // Option型: Some(値) または None を返す
        match s {
            "+" => Some(Operator::Add),
            "-" => Some(Operator::Subtract),
            "*" => Some(Operator::Multiply),
            "/" => Some(Operator::Divide),
            "%" => Some(Operator::Modulo),
            "^" => Some(Operator::Power),
            _ => None,
        }
    }

    /// 演算子の記号を返す
    fn symbol(&self) -> &str {
        match self {
            Operator::Add => "+",
            Operator::Subtract => "-",
            Operator::Multiply => "*",
            Operator::Divide => "/",
            Operator::Modulo => "%",
            Operator::Power => "^",
        }
    }
}

// ────────────────────────────────────────
//  電卓のエラー型
// ────────────────────────────────────────
#[derive(Debug)]
enum CalcError {
    DivisionByZero,            // ゼロ除算
    InvalidNumber(String),     // 数値パースエラー
    InvalidOperator(String),   // 不正な演算子
    InvalidExpression(String), // 式の形式エラー
    Overflow,                  // オーバーフロー
}

impl fmt::Display for CalcError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            CalcError::DivisionByZero => write!(f, "ゼロで割ることはできません"),
            CalcError::InvalidNumber(s) => write!(f, "'{}' は有効な数値ではありません", s),
            CalcError::InvalidOperator(s) => {
                write!(f, "'{}' は有効な演算子ではありません（+, -, *, /, %, ^）", s)
            }
            CalcError::InvalidExpression(s) => {
                write!(f, "式の形式が正しくありません: {}", s)
            }
            CalcError::Overflow => write!(f, "計算結果がオーバーフローしました"),
        }
    }
}

// ────────────────────────────────────────
//  計算式を表す構造体
// ────────────────────────────────────────
#[derive(Debug, Clone)]
struct Expression {
    left: f64,
    operator: Operator,
    right: f64,
}

impl fmt::Display for Expression {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{} {} {}",
            format_number(self.left),
            self.operator.symbol(),
            format_number(self.right)
        )
    }
}

// ────────────────────────────────────────
//  計算履歴を表す構造体
// ────────────────────────────────────────
struct CalculationHistory {
    entries: Vec<(Expression, f64)>, // (式, 結果) のペア
}

impl CalculationHistory {
    fn new() -> Self {
        CalculationHistory {
            entries: Vec::new(),
        }
    }

    fn add(&mut self, expr: Expression, result: f64) {
        self.entries.push((expr, result));
    }

    /// 直前の計算結果を取得する（Option型を返す）
    fn last_result(&self) -> Option<f64> {
        // last() は Option<&(Expression, f64)> を返す
        // map() で中身を変換
        self.entries.last().map(|(_, result)| *result)
    }

    fn display(&self) {
        if self.entries.is_empty() {
            println!("  履歴はまだありません。");
            return;
        }
        println!("┌────────────────────────────────────────┐");
        println!("│           📜 計算履歴                  │");
        println!("├────────────────────────────────────────┤");
        for (i, (expr, result)) in self.entries.iter().enumerate() {
            println!(
                "│  {:>2}. {} = {:<20} │",
                i + 1,
                expr,
                format_number(*result)
            );
        }
        println!("└────────────────────────────────────────┘");
    }
}

// ────────────────────────────────────────
//  数値の表示フォーマット
//  整数なら小数点なし、小数なら小数点あり
// ────────────────────────────────────────
fn format_number(n: f64) -> String {
    if n == n.floor() && n.abs() < 1e15 {
        format!("{}", n as i64)
    } else {
        format!("{:.6}", n)
    }
}

// ────────────────────────────────────────
//  計算実行関数
//  Result<f64, CalcError> を返す
// ────────────────────────────────────────
fn calculate(expr: &Expression) -> Result<f64, CalcError> {
    let result = match &expr.operator {
        Operator::Add => expr.left + expr.right,
        Operator::Subtract => expr.left - expr.right,
        Operator::Multiply => expr.left * expr.right,
        Operator::Divide => {
            // ゼロ除算チェック
            if expr.right == 0.0 {
                return Err(CalcError::DivisionByZero);
            }
            expr.left / expr.right
        }
        Operator::Modulo => {
            if expr.right == 0.0 {
                return Err(CalcError::DivisionByZero);
            }
            expr.left % expr.right
        }
        Operator::Power => expr.left.powf(expr.right),
    };

    // 無限大やNaNのチェック
    if result.is_infinite() || result.is_nan() {
        return Err(CalcError::Overflow);
    }

    Ok(result)
}

// ────────────────────────────────────────
//  式のパース（文字列 → Expression）
//  "ans" キーワードで前回の結果を参照可能
// ────────────────────────────────────────
fn parse_expression(
    input: &str,
    last_result: Option<f64>,
) -> Result<Expression, CalcError> {
    let tokens: Vec<&str> = input.split_whitespace().collect();

    if tokens.len() != 3 {
        return Err(CalcError::InvalidExpression(
            "「数値 演算子 数値」の形式で入力してください（例: 3 + 5）".to_string(),
        ));
    }

    // 左辺の解析（"ans" なら前回の結果を使う）
    let left = parse_number(tokens[0], last_result)?;

    // 演算子の解析
    let operator = Operator::from_str(tokens[1]).ok_or_else(|| {
        // ok_or_else: None を Err に変換
        CalcError::InvalidOperator(tokens[1].to_string())
    })?;

    // 右辺の解析
    let right = parse_number(tokens[2], last_result)?;

    Ok(Expression {
        left,
        operator,
        right,
    })
}

/// 数値文字列をパースする補助関数
fn parse_number(s: &str, last_result: Option<f64>) -> Result<f64, CalcError> {
    if s == "ans" {
        // 前回の結果を使用
        last_result.ok_or_else(|| {
            CalcError::InvalidExpression(
                "まだ計算結果がありません（ans は使えません）".to_string(),
            )
        })
    } else {
        s.parse::<f64>()
            .map_err(|_| CalcError::InvalidNumber(s.to_string()))
    }
}

// ────────────────────────────────────────
//  ヘルプ表示
// ────────────────────────────────────────
fn show_help() {
    println!();
    println!("使い方:");
    println!("  数値 演算子 数値  ... 計算を実行（例: 3 + 5）");
    println!();
    println!("対応する演算子:");
    println!("  +  加算      例: 10 + 3   → 13");
    println!("  -  減算      例: 10 - 3   → 7");
    println!("  *  乗算      例: 10 * 3   → 30");
    println!("  /  除算      例: 10 / 3   → 3.333...");
    println!("  %  剰余      例: 10 % 3   → 1");
    println!("  ^  累乗      例: 2 ^ 10   → 1024");
    println!();
    println!("特殊キーワード:");
    println!("  ans          前回の計算結果を参照（例: ans * 2）");
    println!();
    println!("コマンド:");
    println!("  help         このヘルプを表示");
    println!("  history      計算履歴を表示");
    println!("  quit         終了");
    println!();
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
    println!("║       🔢 ミニ電卓 🔢                ║");
    println!("╚══════════════════════════════════════╝");
    println!();
    println!("数値 演算子 数値 の形式で入力してください。");
    println!("例: 3 + 5 / 10 * 2 / 2 ^ 8");
    println!("help でヘルプ、quit で終了します。");
    println!();

    // デモ計算を実行
    println!("--- デモ計算 ---");
    let demos = vec![
        ("42 + 58", "基本的な加算"),
        ("100 - 37", "減算"),
        ("12 * 8", "乗算"),
        ("100 / 3", "除算（小数が出る例）"),
        ("17 % 5", "剰余"),
        ("2 ^ 10", "累乗"),
    ];

    let mut history = CalculationHistory::new();

    for (expr_str, description) in &demos {
        match parse_expression(expr_str, history.last_result()) {
            Ok(expr) => match calculate(&expr) {
                Ok(result) => {
                    println!(
                        "  {} = {}  ({})",
                        expr,
                        format_number(result),
                        description
                    );
                    history.add(expr, result);
                }
                Err(e) => println!("  エラー: {}", e),
            },
            Err(e) => println!("  パースエラー: {}", e),
        }
    }
    println!();

    // 対話モード
    println!("--- 対話モード ---\n");

    loop {
        let input = read_input("calc > ");

        match input.as_str() {
            "quit" | "q" | "exit" => break,
            "help" | "h" => {
                show_help();
                continue;
            }
            "history" => {
                history.display();
                continue;
            }
            "" => continue,
            _ => {}
        }

        // 式をパースして計算
        match parse_expression(&input, history.last_result()) {
            Ok(expr) => {
                match calculate(&expr) {
                    Ok(result) => {
                        println!("  = {}", format_number(result));
                        println!();
                        history.add(expr, result);
                    }
                    Err(e) => println!("  ⚠️  計算エラー: {}\n", e),
                }
            }
            Err(e) => println!("  ⚠️  入力エラー: {}\n", e),
        }
    }

    // 最終履歴を表示
    println!();
    history.display();
    println!("\nお疲れさまでした！");
}
