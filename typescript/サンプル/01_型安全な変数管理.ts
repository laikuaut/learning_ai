// ==============================
// 型安全な変数管理プログラム
// 第1章：TypeScriptの基本の総合サンプル
// ==============================
// 学べる内容:
//   - 基本の型注釈（string, number, boolean）
//   - 配列型とタプル型
//   - オブジェクト型とオプショナルプロパティ
//   - 型推論（let vs const の違い）
//   - enum型の使い方
//   - unknown型と型ガード
//   - 型アサーション（as）
//   - null/undefined の安全な扱い方
// 実行方法:
//   npx tsc 01_型安全な変数管理.ts && node 01_型安全な変数管理.js
//   または: npx ts-node 01_型安全な変数管理.ts
// ==============================

// --- 基本の型注釈 ---
const appName: string = "TypeScript学習帳";
const version: number = 1.0;
const isDebug: boolean = true;

console.log("=== 基本の型注釈 ===");
console.log(`アプリ名: ${appName}`);
console.log(`バージョン: ${version}`);
console.log(`デバッグモード: ${isDebug ? "ON" : "OFF"}`);
console.log();

// --- 型推論: let vs const ---
const constantMessage = "固定値";    // 型は "固定値"（リテラル型）
let mutableMessage = "可変値";       // 型は string（変更可能なので広い型）

const constantNumber = 42;           // 型は 42（リテラル型）
let mutableNumber = 42;              // 型は number

console.log("=== 型推論の違い ===");
console.log(`const "固定値" の型 → リテラル型 "固定値"`);
console.log(`let "可変値" の型   → string型`);
console.log();

// --- 配列型 ---
const subjects: string[] = ["国語", "数学", "英語", "理科", "社会"];
const scores: number[] = [85, 92, 78, 95, 88];

console.log("=== 配列型 ===");
console.log(`科目: ${subjects.join(", ")}`);
console.log(`点数: ${scores.join(", ")}`);

const average = scores.reduce((sum, s) => sum + s, 0) / scores.length;
console.log(`平均点: ${average.toFixed(1)}`);
console.log();

// --- タプル型 ---
type StudentRecord = [name: string, age: number, grade: string];

const students: StudentRecord[] = [
  ["太郎", 16, "A"],
  ["花子", 17, "B"],
  ["次郎", 16, "A"],
];

console.log("=== タプル型 ===");
students.forEach(([name, age, grade]) => {
  console.log(`${name}（${age}歳）- 評価: ${grade}`);
});
console.log();

// --- オブジェクト型 ---
const student: {
  readonly id: number;
  name: string;
  age: number;
  club?: string;       // オプショナルプロパティ
} = {
  id: 1,
  name: "田中太郎",
  age: 16,
  club: "プログラミング部",
};

// student.id = 2; // エラー！readonlyプロパティは変更不可

console.log("=== オブジェクト型 ===");
console.log(`ID: ${student.id}`);
console.log(`名前: ${student.name}`);
console.log(`年齢: ${student.age}歳`);
console.log(`部活: ${student.club ?? "未所属"}`);
console.log();

// --- enum型 ---
enum Season {
  Spring = "SPRING",
  Summer = "SUMMER",
  Autumn = "AUTUMN",
  Winter = "WINTER",
}

function getSeasonEmoji(season: Season): string {
  switch (season) {
    case Season.Spring: return "sakura";
    case Season.Summer: return "sun";
    case Season.Autumn: return "leaf";
    case Season.Winter: return "snow";
  }
}

console.log("=== enum型 ===");
const currentSeason = Season.Spring;
console.log(`現在の季節: ${currentSeason} (${getSeasonEmoji(currentSeason)})`);
console.log();

// --- unknown型と型ガード ---
function processInput(input: unknown): string {
  if (typeof input === "string") {
    return `文字列: "${input}"（${input.length}文字）`;
  } else if (typeof input === "number") {
    return `数値: ${input}（${input > 0 ? "正" : input < 0 ? "負" : "ゼロ"}）`;
  } else if (typeof input === "boolean") {
    return `真偽値: ${input ? "真" : "偽"}`;
  } else if (Array.isArray(input)) {
    return `配列: [${input.join(", ")}]（${input.length}要素）`;
  } else if (input === null) {
    return "null値";
  } else if (input === undefined) {
    return "undefined値";
  } else {
    return `その他の型: ${typeof input}`;
  }
}

console.log("=== unknown型と型ガード ===");
const testValues: unknown[] = ["hello", 42, true, [1, 2, 3], null, undefined];
testValues.forEach((val) => {
  console.log(`  ${processInput(val)}`);
});
console.log();

// --- null/undefined の安全な扱い ---
interface UserConfig {
  theme?: string;
  language?: string;
  fontSize?: number;
}

function getConfigValue(config: UserConfig): void {
  // Nullish Coalescing（??）でデフォルト値を設定
  const theme = config.theme ?? "light";
  const language = config.language ?? "ja";
  const fontSize = config.fontSize ?? 14;

  // Optional Chaining（?.）でネストした値に安全にアクセス
  console.log(`テーマ: ${theme}`);
  console.log(`言語: ${language}`);
  console.log(`フォントサイズ: ${fontSize}px`);
}

console.log("=== null/undefined の安全な扱い ===");
const userConfig: UserConfig = { theme: "dark" };
getConfigValue(userConfig);
console.log();

// --- 型アサーション ---
console.log("=== 型アサーション ===");
const rawData: unknown = '{"name": "太郎", "score": 95}';

// unknown → string → パース → 型アサーション
if (typeof rawData === "string") {
  const parsed = JSON.parse(rawData) as { name: string; score: number };
  console.log(`名前: ${parsed.name}, 点数: ${parsed.score}`);
}

// as const で不変の値を定義
const DIRECTIONS = ["north", "south", "east", "west"] as const;
type Direction = (typeof DIRECTIONS)[number]; // "north" | "south" | "east" | "west"

const myDirection: Direction = "north";
console.log(`方角: ${myDirection}`);
console.log();

// --- 総合: 成績管理 ---
console.log("=== 総合: 成績管理 ===");

type Grade = "A" | "B" | "C" | "D" | "F";

function calculateGrade(score: number): Grade {
  if (score >= 90) return "A";
  if (score >= 80) return "B";
  if (score >= 70) return "C";
  if (score >= 60) return "D";
  return "F";
}

function printBar(value: number, maxValue: number = 100, width: number = 20): string {
  const filled = Math.round((value / maxValue) * width);
  return "#".repeat(filled) + "-".repeat(width - filled);
}

console.log(`${"科目"} ${"点数".padStart(4)} ${"グラフ".padStart(4)}        ${"評価"}`);
console.log("-".repeat(50));

subjects.forEach((subject, i) => {
  const score = scores[i];
  const grade = calculateGrade(score);
  const bar = printBar(score);
  console.log(`${subject.padEnd(4)} ${String(score).padStart(4)} [${bar}] ${grade}`);
});

console.log("-".repeat(50));
console.log(`平均: ${average.toFixed(1)} 総合評価: ${calculateGrade(average)}`);
