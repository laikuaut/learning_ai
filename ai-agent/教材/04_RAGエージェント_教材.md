# 第4章：RAGエージェント

## 学習目標

- RAG（検索拡張生成）が必要な理由と基本フローを説明できるようになる
- 埋め込み（Embedding）の概念とベクトル類似度検索の仕組みを理解する
- 主要なベクトルデータベースの特徴を比較し、用途に応じて選定できるようになる
- ドキュメント取り込みから回答生成までの RAG パイプラインを実装できるようになる
- HyDE、Re-ranking などの高度な RAG テクニックを理解し適用できるようになる
- RAG システムの品質を評価・改善する方法を習得する

---

## この章のゴール

LLM の知識の限界を補い、最新かつ正確な情報に基づいて回答を生成する **RAGエージェント** を設計・実装・評価できるようになることです。

---

## 4.1 RAG（検索拡張生成）の基本

### なぜ RAG が必要か

LLM には以下の根本的な制約があります。

| 制約 | 説明 | RAG による解決 |
|------|------|---------------|
| **知識のカットオフ** | 学習データの時点までの情報しか持たない | 最新のドキュメントから検索して補完 |
| **ハルシネーション（Hallucination）** | 事実と異なる内容をもっともらしく生成する | 根拠となるソースを明示して回答 |
| **社内情報の欠如** | 公開情報で学習しており、社内データを知らない | 社内ドキュメントを検索対象に追加 |
| **コンテキスト長の制限** | 全ドキュメントを一度に入力できない | 関連部分だけを検索して渡す |

### RAG の基本フロー

```
  ユーザーの質問
      │
      ▼
┌──────────────┐
│  1. 検索      │ ── 質問に関連するドキュメントを検索
│  (Retrieve)  │
└──────┬───────┘
       │  関連ドキュメント（チャンク）
       ▼
┌──────────────┐
│  2. 拡張      │ ── プロンプトに検索結果を付加
│  (Augment)   │
└──────┬───────┘
       │  拡張されたプロンプト
       ▼
┌──────────────┐
│  3. 生成      │ ── LLM が検索結果を参照して回答
│  (Generate)  │
└──────────────┘
       │
       ▼
  根拠に基づいた回答
```

### 最小限の RAG 実装例

```python
# 概念理解のための簡易 RAG（ベクトル検索なし版）
import anthropic

client = anthropic.Anthropic()

# 社内ドキュメント（実際にはDBやファイルから取得）
documents = [
    "当社の有給休暇は入社6ヶ月後に10日付与されます。以降1年ごとに1日ずつ増加し、最大20日です。",
    "リモートワークは週3日まで利用可能です。申請はSlackの#remote-workチャンネルで前日までに行ってください。",
    "経費精算は月末締め、翌月15日払いです。申請は経費精算システムから行い、領収書の添付が必須です。",
]


def simple_keyword_search(query: str, docs: list[str], top_k: int = 2) -> list[str]:
    """キーワードベースの簡易検索（本番ではベクトル検索を使用）"""
    scored = []
    query_words = query.lower().split()
    for doc in docs:
        score = sum(1 for word in query_words if word in doc.lower())
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored[:top_k] if score > 0]


def rag_query(question: str) -> str:
    # 1. 検索（Retrieve）
    relevant_docs = simple_keyword_search(question, documents)

    # 2. 拡張（Augment）
    context = "\n\n".join(f"【参考資料{i+1}】\n{doc}" for i, doc in enumerate(relevant_docs))

    prompt = f"""以下の参考資料に基づいて質問に回答してください。
参考資料に記載がない場合は「資料に記載がありません」と回答してください。

{context}

質問: {question}"""

    # 3. 生成（Generate）
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


# 実行例
answer = rag_query("有給休暇は何日もらえますか")
print(answer)
```

> **ポイントまとめ**
> - RAG は「検索 → 拡張 → 生成」の3ステップで LLM の知識を補完します
> - ハルシネーション対策として、根拠文書を明示させることが重要です
> - 上の例はキーワード検索ですが、本番ではベクトル検索を使うのが一般的です

---

## 4.2 埋め込み（Embedding）と検索

### ベクトル埋め込みとは

埋め込み（Embedding）とは、テキストを **固定長の数値ベクトル** に変換する技術です。意味的に近いテキストは、ベクトル空間上で近い位置にマッピングされます。

```
テキスト                    ベクトル（簡略化）
「犬が公園で遊ぶ」      → [0.82, 0.15, 0.91, ...]
「猫が庭で走る」        → [0.78, 0.12, 0.88, ...]  ← 意味が近いので近い値
「経費精算の方法」      → [0.11, 0.95, 0.03, ...]  ← 意味が遠いので遠い値
```

### 類似度検索の仕組み

2つのベクトル間の「近さ」を測る指標として、主にコサイン類似度（Cosine Similarity）が使われます。

```
コサイン類似度 = (A・B) / (|A| × |B|)

値の範囲: -1 〜 1
  1 に近い → 非常に類似
  0 に近い → 無関係
 -1 に近い → 正反対の意味
```

### Python でのベクトル埋め込み実装

```python
# OpenAI の Embedding API を使用する例
import openai
import numpy as np

openai_client = openai.OpenAI()


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """テキストをベクトルに変換します。"""
    response = openai_client.embeddings.create(input=text, model=model)
    return response.data[0].embedding


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """2つのベクトルのコサイン類似度を計算します。"""
    a = np.array(vec_a)
    b = np.array(vec_b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# 使用例
doc_embedding = get_embedding("有給休暇は入社6ヶ月後に10日付与されます")
query_embedding = get_embedding("有給休暇はいつからもらえますか")
similarity = cosine_similarity(doc_embedding, query_embedding)
print(f"類似度: {similarity:.4f}")  # 例: 0.8932（高い類似度）
```

### チャンク分割（Chunking）戦略

長いドキュメントをそのまま埋め込むと、情報が平均化されて検索精度が下がります。適切なサイズに分割（チャンク分割）する必要があります。

| 戦略 | 説明 | 適するケース |
|------|------|-------------|
| **固定長分割** | 文字数やトークン数で機械的に分割 | 構造がないテキスト |
| **段落・セクション分割** | 見出しや改行で論理的に分割 | 構造化されたドキュメント |
| **オーバーラップ分割** | 前後のチャンクと一部重複させる | 文脈の断絶を防ぎたい場合 |
| **セマンティック分割** | 意味のまとまりで分割 | 高精度が求められる場合 |

```
【オーバーラップ分割の例】（チャンクサイズ200文字、オーバーラップ50文字）

原文: AAAAAABBBBBBCCCCCCDDDDDD...

チャンク1: [AAAAAA BBBBBB]
チャンク2:        [BBBBBB CCCCCC]   ← BBBBBBが重複
チャンク3:               [CCCCCC DDDDDD]  ← CCCCCCが重複
```

```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """テキストをオーバーラップ付きで分割します。"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # オーバーラップ分だけ戻る
    return chunks
```

### よくある間違い

- **チャンクサイズが大きすぎる**: 1チャンクに複数トピックが混在し、検索精度が低下します
- **チャンクサイズが小さすぎる**: 文脈が失われ、LLM が正しく理解できなくなります
- **オーバーラップなし**: 文の途中で分割された情報を検索できなくなります
- **メタデータの欠如**: 出典元（ファイル名、ページ番号）をチャンクに紐づけないと、根拠の提示ができません

> **ポイントまとめ**
> - 埋め込みは「テキストの意味」を数値ベクトルに変換する技術です
> - コサイン類似度で検索クエリと文書の近さを測定します
> - チャンク分割の設計が RAG の検索精度を大きく左右します

---

## 4.3 ベクトルデータベース

### 主要ベクトルデータベースの比較

| 項目 | Chroma | pgvector | Pinecone | Weaviate |
|------|--------|----------|----------|----------|
| **種別** | 組み込み型 | PostgreSQL拡張 | マネージド | セルフホスト/クラウド |
| **セットアップ** | 非常に簡単 | PostgreSQLに追加 | クラウド登録 | Docker等で構築 |
| **スケール** | 小〜中規模 | 中規模 | 大規模 | 大規模 |
| **コスト** | 無料 | 無料（DB費用のみ） | 従量課金 | 無料〜有料 |
| **適するケース** | プロトタイプ、個人開発 | 既存PostgreSQL環境 | 本番環境、大規模 | 柔軟なカスタマイズ |
| **言語対応** | Python | SQL | REST API/SDK | REST API/SDK |

### 選定基準のフローチャート

```
ベクトルDB選定
    │
    ├─ まずは試したい / プロトタイプ → Chroma
    │
    ├─ 既に PostgreSQL を使っている → pgvector
    │
    ├─ 大規模本番 + 運用負荷を減らしたい → Pinecone
    │
    └─ 柔軟なフィルタリング + セルフホスト → Weaviate
```

### Chroma を使った実装例

```python
# pip install chromadb
import chromadb

# クライアント作成（ローカルの永続化ストレージ）
client = chromadb.PersistentClient(path="./chroma_db")

# コレクション（テーブルに相当）を作成
collection = client.get_or_create_collection(
    name="company_docs",
    metadata={"description": "社内ドキュメント"},
)

# ドキュメントを追加（Chromaが自動で埋め込みを生成）
collection.add(
    documents=[
        "当社の有給休暇は入社6ヶ月後に10日付与されます。",
        "リモートワークは週3日まで利用可能です。",
        "経費精算は月末締め、翌月15日払いです。",
    ],
    ids=["doc1", "doc2", "doc3"],
    metadatas=[
        {"source": "就業規則", "chapter": "休暇"},
        {"source": "就業規則", "chapter": "勤務形態"},
        {"source": "経理マニュアル", "chapter": "経費"},
    ],
)

# 検索
results = collection.query(
    query_texts=["休みは何日取れますか"],
    n_results=2,
)

print("検索結果:")
for doc, metadata, distance in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0],
):
    print(f"  [{metadata['source']}] {doc}")
    print(f"  距離: {distance:.4f}")
```

> **ポイントまとめ**
> - 小規模なら Chroma、既存 PostgreSQL 環境なら pgvector が導入しやすいです
> - 本番環境のスケーラビリティが必要なら Pinecone や Weaviate を検討します
> - メタデータによるフィルタリング機能はどのDBでも重要です

---

## 4.4 RAG パイプラインの構築

### パイプライン全体像

```
┌─────────────────────── インデックス構築（事前準備）───────────────────────┐
│                                                                        │
│  ドキュメント → ローダー → チャンク分割 → 埋め込み → ベクトルDB格納     │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

┌─────────────────────── クエリ処理（実行時）─────────────────────────────┐
│                                                                        │
│  質問 → 埋め込み → ベクトルDB検索 → プロンプト構築 → LLM生成 → 回答   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 完全な RAG パイプライン実装

```python
import anthropic
import chromadb
from pathlib import Path

# === 1. 初期設定 ===
anthropic_client = anthropic.Anthropic()
chroma_client = chromadb.PersistentClient(path="./rag_db")
collection = chroma_client.get_or_create_collection(name="knowledge_base")


# === 2. ドキュメントローダー ===
def load_documents(directory: str) -> list[dict]:
    """ディレクトリ内のテキストファイルを読み込みます。"""
    docs = []
    for file_path in Path(directory).glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")
        docs.append({
            "content": content,
            "source": file_path.name,
        })
    return docs


# === 3. チャンク分割 ===
def split_into_chunks(
    text: str,
    source: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[dict]:
    """テキストをチャンクに分割し、メタデータを付与します。"""
    chunks = []
    start = 0
    chunk_index = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append({
            "content": text[start:end],
            "source": source,
            "chunk_index": chunk_index,
        })
        start = end - overlap
        chunk_index += 1
    return chunks


# === 4. インデックス構築 ===
def build_index(directory: str):
    """ドキュメントを読み込み、チャンク分割してベクトルDBに格納します。"""
    docs = load_documents(directory)
    all_chunks = []

    for doc in docs:
        chunks = split_into_chunks(doc["content"], doc["source"])
        all_chunks.extend(chunks)

    # Chroma に追加
    collection.add(
        documents=[c["content"] for c in all_chunks],
        ids=[f"{c['source']}_{c['chunk_index']}" for c in all_chunks],
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]}
                   for c in all_chunks],
    )
    print(f"{len(all_chunks)} チャンクをインデックスに追加しました。")


# === 5. 検索 ===
def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """クエリに関連するチャンクを検索します。"""
    results = collection.query(query_texts=[query], n_results=top_k)
    retrieved = []
    for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
        retrieved.append({"content": doc, "source": metadata["source"]})
    return retrieved


# === 6. プロンプト構築と生成 ===
RAG_SYSTEM_PROMPT = """あなたは社内ドキュメントに基づいて回答するアシスタントです。
以下のルールを守ってください:
1. 提供された参考資料の情報のみに基づいて回答する
2. 参考資料に記載がない場合は「資料に記載がありません」と明示する
3. 回答の根拠となる資料の出典を明記する
4. 推測や一般知識での補完はしない"""


def generate_answer(question: str) -> str:
    """RAG パイプラインで質問に回答します。"""
    # 検索
    contexts = retrieve(question)

    # プロンプト構築
    context_text = "\n\n".join(
        f"【出典: {ctx['source']}】\n{ctx['content']}"
        for ctx in contexts
    )
    user_message = f"""参考資料:
{context_text}

質問: {question}

上記の参考資料に基づいて回答してください。出典も明記してください。"""

    # 生成
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=RAG_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


# === 実行 ===
if __name__ == "__main__":
    # インデックス構築（初回のみ）
    # build_index("./documents")

    # 質問応答
    answer = generate_answer("有給休暇の付与日数を教えてください")
    print(answer)
```

### よくある間違い

- **インデックス構築を毎回実行する**: 大量のドキュメントを毎リクエストで再インデックスするのは非効率です。初回のみ構築し、更新は差分で行いましょう
- **検索結果をそのまま渡す**: 検索結果の品質チェックなしに LLM に渡すと、無関係な情報でノイズが増えます
- **top_k の値が不適切**: 小さすぎると必要な情報を見逃し、大きすぎるとコンテキストがノイズだらけになります。通常 3〜5 が目安です

> **ポイントまとめ**
> - RAG パイプラインは「インデックス構築」と「クエリ処理」の2フェーズで構成されます
> - 各ステップ（ローダー、チャンク分割、埋め込み、検索、生成）を独立したモジュールとして設計すると、改善しやすくなります
> - システムプロンプトで「資料に基づいて回答する」ことを明示するのがハルシネーション対策の基本です

---

## 4.5 高度な RAG テクニック

### テクニック一覧

| テクニック | 概要 | 効果 |
|-----------|------|------|
| **HyDE** | 仮の回答を生成してから検索 | 質問と文書の表現ギャップを埋める |
| **Re-ranking** | 検索結果を再スコアリング | 上位結果の精度向上 |
| **マルチクエリ** | 1つの質問から複数の検索クエリを生成 | 検索の網羅性向上 |
| **Self-RAG** | LLM 自身が検索の必要性を判断 | 不要な検索を減らし精度向上 |
| **Adaptive RAG** | 質問の複雑さに応じて戦略を変更 | リソースの効率的な活用 |

### HyDE（Hypothetical Document Embeddings）

質問文をそのまま埋め込むのではなく、LLM に「仮の回答」を生成させてから、その回答文で検索します。

```
【通常のRAG】
  質問: 「有給の付与日数は？」
    → この質問文を埋め込んで検索

【HyDE】
  質問: 「有給の付与日数は？」
    → LLMが仮の回答を生成: 「有給休暇は入社後6ヶ月で10日付与され...」
    → この仮回答を埋め込んで検索（文書と表現が近くなる）
```

```python
def hyde_retrieve(question: str, top_k: int = 3) -> list[dict]:
    """HyDE を使った検索。仮の回答を生成してから検索します。"""
    # 仮の回答を生成
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": (
                f"以下の質問に対する回答を、実際の社内文書に書かれていそうな文体で"
                f"生成してください。正確でなくても構いません。\n\n質問: {question}"
            ),
        }],
    )
    hypothetical_doc = response.content[0].text

    # 仮の回答で検索
    results = collection.query(query_texts=[hypothetical_doc], n_results=top_k)
    return [
        {"content": doc, "source": meta["source"]}
        for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    ]
```

### Re-ranking（再ランキング）

ベクトル検索で取得した候補を、より精度の高いモデルで再スコアリングします。

```python
def rerank_results(question: str, candidates: list[dict], top_k: int = 3) -> list[dict]:
    """LLM を使って検索結果を再ランキングします。"""
    candidate_text = "\n".join(
        f"候補{i+1}: {c['content'][:200]}"
        for i, c in enumerate(candidates)
    )

    response = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": (
                f"以下の質問に最も関連性の高い候補を、関連度順に{top_k}つ選んで"
                f"番号のみをカンマ区切りで回答してください。\n\n"
                f"質問: {question}\n\n{candidate_text}"
            ),
        }],
    )

    # 番号をパースして並べ替え
    try:
        indices = [int(x.strip()) - 1 for x in response.content[0].text.split(",")]
        return [candidates[i] for i in indices if 0 <= i < len(candidates)]
    except (ValueError, IndexError):
        return candidates[:top_k]
```

### マルチクエリ RAG

```python
def generate_multi_queries(question: str, num_queries: int = 3) -> list[str]:
    """1つの質問から複数の検索クエリを生成します。"""
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": (
                f"以下の質問を別の表現で{num_queries}通りに言い換えてください。"
                f"1行に1つずつ出力してください。\n\n質問: {question}"
            ),
        }],
    )
    queries = response.content[0].text.strip().split("\n")
    return [q.strip().lstrip("0123456789.-) ") for q in queries if q.strip()]
```

### Self-RAG の考え方

```
質問を受け取る
    │
    ▼
「検索が必要か？」を判断
    │
    ├─ 不要（一般知識で回答可能）→ 直接回答
    │
    └─ 必要 → 検索を実行
                │
                ▼
          「検索結果は質問に関連しているか？」を評価
                │
                ├─ 関連あり → 回答を生成
                │              │
                │              ▼
                │        「回答は検索結果に忠実か？」を評価
                │              │
                │              ├─ 忠実 → 回答を返す
                │              └─ 不忠実 → 再生成
                │
                └─ 関連なし → 再検索 or 「わかりません」
```

> **ポイントまとめ**
> - HyDE は質問と文書の表現ギャップを埋め、検索精度を向上させます
> - Re-ranking は計算コストが増えますが、上位結果の精度を大幅に改善します
> - これらのテクニックは組み合わせて使うことで最大の効果を発揮します

---

## 4.6 RAG の評価と改善

### 評価指標

RAG システムの品質は以下の4つの指標で評価します。

| 指標 | 評価対象 | 質問 |
|------|---------|------|
| **Faithfulness（忠実度）** | 生成された回答 | 回答は検索結果に基づいているか？ |
| **Answer Relevancy（回答関連度）** | 生成された回答 | 回答は質問に対して適切か？ |
| **Context Precision（文脈精度）** | 検索結果 | 検索結果の上位に関連文書があるか？ |
| **Context Recall（文脈再現率）** | 検索結果 | 必要な情報が検索結果に含まれているか？ |

```
           検索の品質              生成の品質
         ┌──────────────┐      ┌──────────────┐
質問 ──► │Context       │      │Faithfulness  │ ──► 検索結果に忠実か
         │Precision     │      │              │
         │Context Recall│      │Answer        │ ──► 質問に答えているか
         └──────────────┘      │Relevancy     │
                               └──────────────┘
```

### RAGAS フレームワーク

RAGAS（Retrieval Augmented Generation Assessment）は、RAG システムの自動評価フレームワークです。

```python
# pip install ragas
# RAGAS による評価の概念的な例

evaluation_data = {
    "question": "有給休暇は何日もらえますか？",
    "answer": "入社6ヶ月後に10日付与されます。",
    "contexts": [
        "当社の有給休暇は入社6ヶ月後に10日付与されます。以降1年ごとに1日増加。"
    ],
    "ground_truth": "入社6ヶ月後に10日。以降毎年1日ずつ増加し最大20日。",
}

# 評価の観点
# Faithfulness: 回答「10日付与」は contexts に記載 → 高スコア
# Answer Relevancy: 質問「何日」に「10日」と回答 → 高スコア
# Context Recall: ground_truth の「最大20日」が contexts に含まれる → 高スコア
# Context Precision: 上位に関連文書が来ている → 高スコア
```

### 改善のチェックリスト

検索の品質が低い場合と生成の品質が低い場合で、改善のアプローチが異なります。

```
【検索品質が低い場合の改善策】
  □ チャンクサイズを調整する（大きすぎ／小さすぎ）
  □ オーバーラップを追加する
  □ 埋め込みモデルを変更する
  □ HyDE やマルチクエリを導入する
  □ メタデータフィルタリングを活用する

【生成品質が低い場合の改善策】
  □ システムプロンプトを改善する
  □ 「資料に基づいて回答せよ」を強調する
  □ 検索結果の提示方法を工夫する
  □ Re-ranking を導入する
  □ few-shot 例を追加する
```

### 簡易評価の実装

```python
def evaluate_faithfulness(answer: str, contexts: list[str]) -> str:
    """回答が検索結果に忠実かを LLM で評価します。"""
    context_text = "\n".join(contexts)
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": (
                f"以下の「回答」が「参考資料」の内容に忠実かどうかを評価してください。\n"
                f"「忠実」「部分的に忠実」「忠実でない」のいずれかで回答し、理由を述べてください。\n\n"
                f"参考資料:\n{context_text}\n\n回答:\n{answer}"
            ),
        }],
    )
    return response.content[0].text
```

### よくある間違い

- **評価なしで本番投入**: 主観評価だけでなく、定量的な評価指標を必ず設定しましょう
- **検索と生成を一緒に改善しようとする**: まず検索の品質を確認し、次に生成を改善するというステップで進めましょう
- **ground truth を用意しない**: 正解データがないと Context Recall は測定できません。最低でも50〜100件の評価データセットを作成しましょう

> **ポイントまとめ**
> - RAG の評価は「検索品質」と「生成品質」を分けて測定します
> - Faithfulness（忠実度）は最も重要な指標 -- ハルシネーション防止の要です
> - 改善は「検索 → 生成」の順で段階的に行うのが効率的です
> - RAGAS などのフレームワークを活用すると、自動的かつ定量的に評価できます
