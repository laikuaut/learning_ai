// ==============================
// インターフェース設計サンプル
// 第2章：インターフェースと型エイリアスの総合サンプル
// ==============================
// 学べる内容:
//   - interfaceの定義と使い方
//   - オプショナルプロパティとreadonlyプロパティ
//   - インターフェースの拡張（extends）
//   - 型エイリアス（type）との使い分け
//   - インデックスシグネチャ
//   - 交差型（&）による合成
//   - 実践的なAPIレスポンス型の設計
// 実行方法:
//   npx tsc 02_インターフェース設計.ts && node 02_インターフェース設計.js
//   または: npx ts-node 02_インターフェース設計.ts
// ==============================

// =====================
// 1. 基本のインターフェース定義
// =====================

// 商品の型定義（interface: オブジェクトの形状を定義）
interface Product {
  readonly id: number;       // 変更不可
  name: string;
  price: number;
  category: string;
  description?: string;      // オプショナル（省略可能）
  tags?: string[];           // オプショナル
}

// 商品データ
const products: Product[] = [
  {
    id: 1,
    name: "TypeScript実践ガイド",
    price: 3200,
    category: "書籍",
    description: "TypeScriptの実践的な使い方を解説",
    tags: ["プログラミング", "TypeScript"],
  },
  {
    id: 2,
    name: "メカニカルキーボード",
    price: 12800,
    category: "周辺機器",
  },
  {
    id: 3,
    name: "ワイヤレスマウス",
    price: 4500,
    category: "周辺機器",
    tags: ["ワイヤレス", "エルゴノミクス"],
  },
];

console.log("=== 1. 商品一覧 ===");
products.forEach((p) => {
  const tags = p.tags ? ` [${p.tags.join(", ")}]` : "";
  console.log(`  #${p.id} ${p.name} - ¥${p.price.toLocaleString()}${tags}`);
});
console.log();

// =====================
// 2. インターフェースの拡張
// =====================

// 基底インターフェース
interface Entity {
  readonly id: number;
  createdAt: Date;
  updatedAt: Date;
}

// Entityを拡張したユーザー
interface User extends Entity {
  name: string;
  email: string;
  role: "admin" | "editor" | "viewer";
}

// Entityを拡張した記事
interface Article extends Entity {
  title: string;
  body: string;
  author: User;
  published: boolean;
}

// ダミーデータの作成
const now = new Date();

const admin: User = {
  id: 1,
  name: "管理者太郎",
  email: "admin@example.com",
  role: "admin",
  createdAt: now,
  updatedAt: now,
};

const article: Article = {
  id: 101,
  title: "TypeScriptの型システム入門",
  body: "TypeScriptの型システムについて解説します...",
  author: admin,
  published: true,
  createdAt: now,
  updatedAt: now,
};

console.log("=== 2. インターフェースの拡張 ===");
console.log(`記事: ${article.title}`);
console.log(`著者: ${article.author.name} (${article.author.role})`);
console.log(`公開: ${article.published ? "はい" : "いいえ"}`);
console.log();

// =====================
// 3. 型エイリアスとの使い分け
// =====================

// ★ ユニオン型は type で定義
type Status = "draft" | "review" | "published" | "archived";
type ID = string | number;

// ★ 関数型は type で定義
type Formatter<T> = (item: T) => string;
type Predicate<T> = (item: T) => boolean;

// ★ タプル型は type で定義
type Coordinate = [latitude: number, longitude: number];

// 関数型の利用例
const formatProduct: Formatter<Product> = (p) =>
  `${p.name}（¥${p.price.toLocaleString()}）`;

const isExpensive: Predicate<Product> = (p) => p.price >= 5000;

console.log("=== 3. 型エイリアスの活用 ===");
console.log("高額商品:");
products.filter(isExpensive).forEach((p) => {
  console.log(`  ${formatProduct(p)}`);
});
console.log();

// =====================
// 4. インデックスシグネチャ（辞書型）
// =====================

interface TranslationDictionary {
  [key: string]: string;
}

const jaToEn: TranslationDictionary = {
  "こんにちは": "Hello",
  "ありがとう": "Thank you",
  "さようなら": "Goodbye",
  "おはよう": "Good morning",
};

function translate(dict: TranslationDictionary, word: string): string {
  return dict[word] ?? `(翻訳なし: ${word})`;
}

console.log("=== 4. 辞書型（インデックスシグネチャ） ===");
const words = ["こんにちは", "ありがとう", "すみません"];
words.forEach((w) => {
  console.log(`  ${w} → ${translate(jaToEn, w)}`);
});
console.log();

// =====================
// 5. 交差型による合成
// =====================

// 共通のメタデータ型
type Timestamped = {
  createdAt: Date;
  updatedAt: Date;
};

type SoftDeletable = {
  deletedAt: Date | null;
  isDeleted: boolean;
};

type Auditable = {
  createdBy: string;
  updatedBy: string;
};

// 交差型で全てを合成
type FullEntity = { id: number } & Timestamped & SoftDeletable & Auditable;

const entity: FullEntity = {
  id: 1,
  createdAt: now,
  updatedAt: now,
  deletedAt: null,
  isDeleted: false,
  createdBy: "admin",
  updatedBy: "admin",
};

console.log("=== 5. 交差型による合成 ===");
console.log(`エンティティ #${entity.id}`);
console.log(`  作成者: ${entity.createdBy}`);
console.log(`  削除済み: ${entity.isDeleted ? "はい" : "いいえ"}`);
console.log();

// =====================
// 6. 実践的なAPIレスポンス型
// =====================

// ジェネリックなレスポンス型
interface ApiResponse<T> {
  status: number;
  message: string;
  data: T;
  timestamp: string;
}

interface PaginationInfo {
  currentPage: number;
  totalPages: number;
  totalItems: number;
  itemsPerPage: number;
  hasNext: boolean;
  hasPrev: boolean;
}

interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: PaginationInfo;
}

// 商品一覧レスポンスのダミーデータ
const productListResponse: PaginatedResponse<Product> = {
  status: 200,
  message: "OK",
  data: products,
  timestamp: new Date().toISOString(),
  pagination: {
    currentPage: 1,
    totalPages: 5,
    totalItems: 47,
    itemsPerPage: 10,
    hasNext: true,
    hasPrev: false,
  },
};

// レスポンスの表示関数
function displayResponse<T>(
  response: PaginatedResponse<T>,
  formatItem: Formatter<T>
): void {
  console.log(`ステータス: ${response.status} ${response.message}`);
  console.log(`データ件数: ${response.data.length}件`);
  response.data.forEach((item, i) => {
    console.log(`  ${i + 1}. ${formatItem(item)}`);
  });
  const { currentPage, totalPages, totalItems } = response.pagination;
  console.log(`ページ: ${currentPage}/${totalPages}（全${totalItems}件）`);
  console.log(`次ページ: ${response.pagination.hasNext ? "あり" : "なし"}`);
}

console.log("=== 6. APIレスポンス型 ===");
displayResponse(productListResponse, formatProduct);
console.log();

// =====================
// 7. メソッドを持つインターフェース
// =====================

interface Calculator {
  add(a: number, b: number): number;
  subtract(a: number, b: number): number;
  multiply(a: number, b: number): number;
  divide(a: number, b: number): number | null;
  history: string[];
}

function createCalculator(): Calculator {
  const calc: Calculator = {
    history: [],
    add(a, b) {
      const result = a + b;
      calc.history.push(`${a} + ${b} = ${result}`);
      return result;
    },
    subtract(a, b) {
      const result = a - b;
      calc.history.push(`${a} - ${b} = ${result}`);
      return result;
    },
    multiply(a, b) {
      const result = a * b;
      calc.history.push(`${a} * ${b} = ${result}`);
      return result;
    },
    divide(a, b) {
      if (b === 0) {
        calc.history.push(`${a} / ${b} = エラー（0除算）`);
        return null;
      }
      const result = a / b;
      calc.history.push(`${a} / ${b} = ${result}`);
      return result;
    },
  };
  return calc;
}

console.log("=== 7. メソッドを持つインターフェース ===");
const calc = createCalculator();

console.log(`10 + 3 = ${calc.add(10, 3)}`);
console.log(`10 - 3 = ${calc.subtract(10, 3)}`);
console.log(`10 * 3 = ${calc.multiply(10, 3)}`);
console.log(`10 / 3 = ${calc.divide(10, 3)?.toFixed(2) ?? "エラー"}`);
console.log(`10 / 0 = ${calc.divide(10, 0) ?? "エラー（0除算）"}`);
console.log();
console.log("計算履歴:");
calc.history.forEach((h) => console.log(`  ${h}`));
