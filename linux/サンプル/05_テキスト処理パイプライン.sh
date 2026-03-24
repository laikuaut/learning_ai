#!/bin/bash
# ============================================================================
# 05_テキスト処理パイプライン.sh
# ============================================================================
# 学べる内容:
#   - grep, sed, awk の実践的な組み合わせ方
#   - sort, uniq, cut, tr, wc の活用
#   - パイプラインによるデータ加工の流れ
#   - ヒアドキュメントによるサンプルデータの生成
#   - 実務で使えるテキスト処理パターン
#
# 実行方法:
#   1. chmod +x 05_テキスト処理パイプライン.sh
#   2. ./05_テキスト処理パイプライン.sh
#
# 動作説明:
#   サンプルデータを自動生成し、様々なテキスト処理パイプラインの
#   実行例を対話的にデモンストレーションします。
#   各デモではコマンドとその出力を表示するので、学習に役立ちます。
# ============================================================================

set -euo pipefail

# --- 一時ファイルの管理 ---
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# --- 表示用の関数 ---
print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

print_command() {
    echo ""
    echo "  [コマンド]"
    echo "  $ $1"
    echo ""
    echo "  [出力]"
}

wait_for_enter() {
    echo ""
    echo "  --- Enter キーで次に進みます ---"
    read -r
}

# --- サンプルデータの生成 ---
generate_sample_data() {
    # 社員データ（CSV）
    cat << 'EOF' > "$TMPDIR/employees.csv"
ID,名前,部署,役職,給与
001,田中太郎,営業部,主任,450000
002,鈴木花子,開発部,課長,580000
003,佐藤健一,営業部,部長,620000
004,山田美咲,開発部,一般,420000
005,高橋翔太,総務部,主任,460000
006,伊藤恵美,開発部,主任,510000
007,渡辺洋平,営業部,一般,380000
008,中村千秋,開発部,一般,400000
009,小林正太,総務部,課長,550000
010,加藤由美,営業部,主任,470000
011,吉田剛,開発部,部長,650000
012,松本麻衣,総務部,一般,370000
EOF

    # サーバーログ
    cat << 'EOF' > "$TMPDIR/server.log"
2024-03-20 10:00:01 INFO  [web-01] リクエスト処理開始 /api/users
2024-03-20 10:00:02 INFO  [web-01] リクエスト処理完了 200 45ms
2024-03-20 10:00:15 WARN  [web-02] レスポンスタイム超過 /api/search 2500ms
2024-03-20 10:01:03 ERROR [db-01] 接続タイムアウト host=db-primary port=3306
2024-03-20 10:01:05 INFO  [db-01] 接続リトライ成功 host=db-primary
2024-03-20 10:02:30 INFO  [web-01] リクエスト処理開始 /api/products
2024-03-20 10:02:31 INFO  [web-01] リクエスト処理完了 200 120ms
2024-03-20 10:03:00 ERROR [web-02] メモリ使用量警告 usage=85%
2024-03-20 10:03:45 INFO  [web-02] GC実行 freed=256MB
2024-03-20 10:04:00 WARN  [web-01] SSL証明書期限 残り30日
2024-03-20 10:05:12 ERROR [web-01] NullPointerException at UserService.java:42
2024-03-20 10:05:13 INFO  [web-01] エラーレスポンス送信 500
2024-03-20 10:06:00 INFO  [db-01] スロークエリ検出 query_time=3.5s
2024-03-20 10:07:00 INFO  [web-02] ヘルスチェック OK
2024-03-20 10:08:00 WARN  [db-01] ディスク使用率 usage=78%
EOF

    # 設定ファイル
    cat << 'EOF' > "$TMPDIR/app.conf"
# アプリケーション設定ファイル
# 最終更新: 2024-03-20

# --- サーバー設定 ---
server.host=0.0.0.0
server.port=8080
server.workers=4

# --- データベース設定 ---
db.host=localhost
db.port=3306
db.name=myapp
db.user=appuser
db.password=secret123

# --- キャッシュ設定 ---
cache.enabled=true
cache.ttl=3600
cache.max_size=256MB

# --- ログ設定 ---
log.level=INFO
log.file=/var/log/myapp/app.log
log.max_size=100MB
EOF
}

# --- デモ関数 ---

# デモ1: CSVデータの集計
demo_csv_analysis() {
    print_header "デモ1: CSVデータの分析"

    echo ""
    echo "  [サンプルデータ: employees.csv]"
    cat "$TMPDIR/employees.csv" | sed 's/^/  /'
    echo ""
    wait_for_enter

    # 部署別の人数集計
    print_command "awk -F, 'NR>1 {print \$3}' employees.csv | sort | uniq -c | sort -rn"
    awk -F, 'NR>1 {print $3}' "$TMPDIR/employees.csv" | sort | uniq -c | sort -rn | sed 's/^/  /'
    echo ""
    echo "  -> 部署別の人数を集計しています"
    wait_for_enter

    # 部署別の平均給与
    print_command "awk -F, 'NR>1 {sum[\$3]+=\$5; cnt[\$3]++} END {for(d in sum) printf \"%s: %d円\\n\", d, sum[d]/cnt[d]}' employees.csv"
    awk -F, 'NR>1 {sum[$3]+=$5; cnt[$3]++} END {for(d in sum) printf "%s: %d円\n", d, sum[d]/cnt[d]}' "$TMPDIR/employees.csv" | sort | sed 's/^/  /'
    echo ""
    echo "  -> 部署別の平均給与を計算しています"
    wait_for_enter

    # 給与ランキング
    print_command "awk -F, 'NR>1 {print \$5, \$2, \$3}' employees.csv | sort -rn | head -5"
    awk -F, 'NR>1 {print $5, $2, $3}' "$TMPDIR/employees.csv" | sort -rn | head -5 | sed 's/^/  /'
    echo ""
    echo "  -> 給与の高い順にトップ5を表示しています"
    wait_for_enter

    # 役職別の人数と合計給与
    print_command "awk -F, 'NR>1 {cnt[\$4]++; sum[\$4]+=\$5} END {for(r in cnt) printf \"%-6s: %d人 合計%d円\\n\", r, cnt[r], sum[r]}' employees.csv"
    awk -F, 'NR>1 {cnt[$4]++; sum[$4]+=$5} END {for(r in cnt) printf "%-6s: %d人 合計%d円\n", r, cnt[r], sum[r]}' "$TMPDIR/employees.csv" | sort | sed 's/^/  /'
    echo ""
    echo "  -> 役職別の人数と合計給与を集計しています"
    wait_for_enter
}

# デモ2: ログ解析パイプライン
demo_log_analysis() {
    print_header "デモ2: サーバーログの解析"

    echo ""
    echo "  [サンプルデータ: server.log]"
    cat "$TMPDIR/server.log" | sed 's/^/  /'
    echo ""
    wait_for_enter

    # ログレベル別の件数
    print_command "awk '{print \$3}' server.log | sort | uniq -c | sort -rn"
    awk '{print $3}' "$TMPDIR/server.log" | sort | uniq -c | sort -rn | sed 's/^/  /'
    echo ""
    echo "  -> ログレベル（INFO/WARN/ERROR）別の件数を集計しています"
    wait_for_enter

    # ERROR のみ抽出
    print_command "grep 'ERROR' server.log"
    grep 'ERROR' "$TMPDIR/server.log" | sed 's/^/  /'
    echo ""
    echo "  -> ERROR レベルのログだけを抽出しています"
    wait_for_enter

    # サーバー別のログ件数
    print_command "grep -oP '\\[\\K[^\\]]+' server.log | sort | uniq -c | sort -rn"
    awk '{print $4}' "$TMPDIR/server.log" | tr -d '[]' | sort | uniq -c | sort -rn | sed 's/^/  /'
    echo ""
    echo "  -> サーバー別のログ件数を集計しています"
    wait_for_enter

    # 時刻別のログ件数（分単位）
    print_command "awk '{print substr(\$2,1,5)}' server.log | sort | uniq -c"
    awk '{print substr($2,1,5)}' "$TMPDIR/server.log" | sort | uniq -c | sed 's/^/  /'
    echo ""
    echo "  -> 時間帯（分単位）別のログ件数を集計しています"
    wait_for_enter
}

# デモ3: 設定ファイルの加工
demo_config_processing() {
    print_header "デモ3: 設定ファイルの加工"

    echo ""
    echo "  [サンプルデータ: app.conf]"
    cat "$TMPDIR/app.conf" | sed 's/^/  /'
    echo ""
    wait_for_enter

    # コメント行と空行を除外して有効行のみ表示
    print_command "grep -v '^#' app.conf | grep -v '^$'"
    grep -v '^#' "$TMPDIR/app.conf" | grep -v '^$' | sed 's/^/  /'
    echo ""
    echo "  -> コメント行（#で始まる行）と空行を除外しています"
    wait_for_enter

    # キーと値を整形して表示
    print_command "grep -v '^#' app.conf | grep -v '^\$' | awk -F= '{printf \"%-20s = %s\\n\", \$1, \$2}'"
    grep -v '^#' "$TMPDIR/app.conf" | grep -v '^$' | awk -F= '{printf "%-20s = %s\n", $1, $2}' | sed 's/^/  /'
    echo ""
    echo "  -> 設定値をキーと値に分離して整形表示しています"
    wait_for_enter

    # 特定のセクションだけ抽出（db. で始まる設定）
    print_command "grep '^db\\.' app.conf"
    grep '^db\.' "$TMPDIR/app.conf" | sed 's/^/  /'
    echo ""
    echo "  -> データベース設定（db.で始まる行）だけを抽出しています"
    wait_for_enter

    # sed で値を置換
    print_command "sed 's/db.host=localhost/db.host=192.168.1.100/' app.conf | grep '^db\\.'"
    sed 's/db.host=localhost/db.host=192.168.1.100/' "$TMPDIR/app.conf" | grep '^db\.' | sed 's/^/  /'
    echo ""
    echo "  -> sed で db.host の値を localhost から 192.168.1.100 に置換しています"
    wait_for_enter
}

# デモ4: 定番パイプラインパターン
demo_common_patterns() {
    print_header "デモ4: 実務で使える定番パイプライン"

    # パターン1: 頻度集計パイプライン
    echo ""
    echo "  [パターン1: 頻度集計パイプライン]"
    echo "  ... | sort | uniq -c | sort -rn | head -N"
    echo ""
    print_command "echo -e 'apple\\nbanana\\napple\\ncherry\\napple\\nbanana' | sort | uniq -c | sort -rn"
    echo -e "apple\nbanana\napple\ncherry\napple\nbanana" | sort | uniq -c | sort -rn | sed 's/^/  /'
    wait_for_enter

    # パターン2: 列の抽出と加工
    echo ""
    echo "  [パターン2: 列の抽出と加工]"
    print_command "echo 'John:25:Tokyo' | awk -F: '{print \$1, \"は\", \$3, \"在住の\", \$2, \"歳です\"}'"
    echo "John:25:Tokyo" | awk -F: '{print $1, "は", $3, "在住の", $2, "歳です"}' | sed 's/^/  /'
    wait_for_enter

    # パターン3: 大文字小文字の変換と正規化
    echo ""
    echo "  [パターン3: テキストの正規化]"
    print_command "echo 'Hello, WORLD! 123-456' | tr 'A-Z' 'a-z' | tr -dc 'a-z0-9 \\n'"
    echo "Hello, WORLD! 123-456" | tr 'A-Z' 'a-z' | tr -dc 'a-z0-9 \n' | sed 's/^/  /'
    wait_for_enter

    # パターン4: 複数ファイルの一括処理
    echo ""
    echo "  [パターン4: CSVの特定列の合計計算]"
    print_command "awk -F, 'NR>1 {sum+=\$5} END {printf \"給与合計: %d円\\n平均給与: %d円\\n\", sum, sum/(NR-1)}' employees.csv"
    awk -F, 'NR>1 {sum+=$5} END {printf "給与合計: %d円\n平均給与: %d円\n", sum, sum/(NR-1)}' "$TMPDIR/employees.csv" | sed 's/^/  /'
    wait_for_enter
}

# --- メイン処理 ---
main() {
    echo "╔══════════════════════════════════════════════════╗"
    echo "║     テキスト処理パイプライン デモンストレーション    ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo ""
    echo "  grep, sed, awk を組み合わせたデータ加工のデモを行います。"
    echo "  各デモでは、コマンドとその出力結果を表示します。"
    echo ""

    # サンプルデータの生成
    generate_sample_data
    echo "  サンプルデータを生成しました。"
    wait_for_enter

    # 各デモの実行
    demo_csv_analysis
    demo_log_analysis
    demo_config_processing
    demo_common_patterns

    print_header "デモ完了"
    echo ""
    echo "  すべてのデモが完了しました。"
    echo "  これらのパイプラインパターンは、実務で頻繁に使用します。"
    echo ""
    echo "  定番パターンまとめ:"
    echo "    1. 頻度集計:     ... | sort | uniq -c | sort -rn | head"
    echo "    2. フィールド抽出: awk -F区切り '{print \$N}'"
    echo "    3. パターン検索:  grep -E 'パターン1|パターン2'"
    echo "    4. 文字列置換:    sed 's/検索/置換/g'"
    echo "    5. 有効行抽出:    grep -v '^#' | grep -v '^\$'"
    echo ""
}

main
