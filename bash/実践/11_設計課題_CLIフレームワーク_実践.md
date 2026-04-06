# 実践課題11：設計課題 ─ CLIフレームワーク ★5

> **難易度**: ★★★★★（総合）
> **前提知識**: 第1章〜第8章（全章）
> **課題の種類**: 設計課題
> **学習目標**: Bashスクリプトの設計力を養い、再利用可能なCLIフレームワークを設計・実装する

---

## 課題の説明

Gitに似た「サブコマンド方式」のCLIツールフレームワークを設計・実装してください。
このフレームワークを使えば、新しいサブコマンドをファイルを追加するだけで拡張できるようにします。

### 達成目標

```
$ ./mytool.sh help
mytool - カスタムCLIツール (v1.0.0)

使い方: mytool <コマンド> [オプション] [引数]

利用可能なコマンド:
  hello     挨拶を表示する
  greet     名前付きで挨拶する
  sysinfo   システム情報を表示する
  backup    ディレクトリをバックアップする
  help      このヘルプを表示する

詳細: mytool help <コマンド>

$ ./mytool.sh greet --name "太郎" --lang ja
こんにちは、太郎さん！

$ ./mytool.sh greet --name "Taro" --lang en
Hello, Taro!

$ ./mytool.sh sysinfo --section cpu,mem
■ CPU情報
  ...
■ メモリ情報
  ...
```

---

## 設計要件

### 必須要件

1. **サブコマンド方式**: `./mytool.sh <command> [args...]` で実行
2. **プラグイン構造**: コマンドは `commands/` ディレクトリの個別ファイルとして配置
3. **自動検出**: `commands/` 内のファイルを自動的にコマンドとして認識
4. **ヘルプ生成**: 各コマンドファイルから説明を読み取り、ヘルプを自動生成
5. **共通オプション**: `--verbose`, `--dry-run`, `--help` をすべてのコマンドで使用可能
6. **エラーハンドリング**: 不明なコマンドやオプションでわかりやすいエラー表示
7. **最低4つのサブコマンド**を実装する

### 推奨ファイル構成

```
mytool/
├── mytool.sh           ← メインエントリポイント
├── lib/
│   ├── common.sh       ← 共通関数（ログ、色、ユーティリティ）
│   └── options.sh      ← オプション解析ユーティリティ
└── commands/
    ├── hello.sh        ← hello コマンド
    ├── greet.sh        ← greet コマンド
    ├── sysinfo.sh      ← sysinfo コマンド
    └── backup.sh       ← backup コマンド
```

---

## ステップガイド

<details>
<summary>ステップ1：共通ライブラリ（lib/common.sh）を作る</summary>

ログ関数、カラー出力、ユーティリティをまとめた共通ライブラリを作ります。

```bash
# lib/common.sh
# 他のスクリプトから source して使う共通関数

# --- カラー定義 ---
if [ -t 1 ]; then
    readonly CLR_RED='\033[31m'
    readonly CLR_GREEN='\033[32m'
    readonly CLR_YELLOW='\033[33m'
    readonly CLR_CYAN='\033[36m'
    readonly CLR_BOLD='\033[1m'
    readonly CLR_RESET='\033[0m'
else
    readonly CLR_RED="" CLR_GREEN="" CLR_YELLOW="" CLR_CYAN="" CLR_BOLD="" CLR_RESET=""
fi

# --- ログ関数 ---
log_info()  { echo -e "${CLR_GREEN}[INFO]${CLR_RESET} $*" >&2; }
log_warn()  { echo -e "${CLR_YELLOW}[WARN]${CLR_RESET} $*" >&2; }
log_error() { echo -e "${CLR_RED}[ERROR]${CLR_RESET} $*" >&2; }
log_debug() { ${VERBOSE:-false} && echo -e "${CLR_CYAN}[DEBUG]${CLR_RESET} $*" >&2 || true; }
```

</details>

<details>
<summary>ステップ2：メインスクリプト（mytool.sh）の骨格を作る</summary>

サブコマンドの自動検出とディスパッチを行うメインスクリプトです。

```bash
#!/usr/bin/env bash
set -euo pipefail

readonly TOOL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly TOOL_NAME="mytool"
readonly TOOL_VERSION="1.0.0"
readonly COMMANDS_DIR="${TOOL_DIR}/commands"
readonly LIB_DIR="${TOOL_DIR}/lib"

# 共通ライブラリ読み込み
source "${LIB_DIR}/common.sh"

# コマンドの一覧を取得
list_commands() {
    for cmd_file in "$COMMANDS_DIR"/*.sh; do
        [ -f "$cmd_file" ] || continue
        local cmd_name
        cmd_name=$(basename "$cmd_file" .sh)
        # ファイルの先頭コメントから説明を取得
        local description
        description=$(grep '^# description:' "$cmd_file" | head -1 | sed 's/^# description: *//')
        printf "  %-12s %s\n" "$cmd_name" "$description"
    done
}

# メインの処理
# ...
```

</details>

<details>
<summary>ステップ3：コマンドファイルの規約を決める</summary>

各コマンドファイルは以下の規約に従います。

```bash
#!/usr/bin/env bash
# description: このコマンドの1行説明
# usage: greet [--name NAME] [--lang LANG]

# コマンドのメイン関数（必須）
cmd_main() {
    # オプション解析
    # 処理
}

# ヘルプ表示関数（必須）
cmd_help() {
    cat <<EOF
greet - 名前付きで挨拶する

使い方: mytool greet [--name NAME] [--lang LANG]

オプション:
  --name NAME   名前（デフォルト: World）
  --lang LANG   言語（ja/en、デフォルト: ja）
EOF
}
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け ─ シンプル版）</summary>

以下の4ファイルを作成してください。

**mytool.sh（メインスクリプト）:**

```bash
#!/usr/bin/env bash
# mytool - カスタムCLIツール
# 実行方法：chmod +x mytool.sh && ./mytool.sh <コマンド> [引数]

set -euo pipefail

readonly TOOL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly TOOL_NAME="mytool"
readonly TOOL_VERSION="1.0.0"
readonly COMMANDS_DIR="${TOOL_DIR}/commands"
readonly LIB_DIR="${TOOL_DIR}/lib"

# 共通ライブラリ読み込み
source "${LIB_DIR}/common.sh"

# --- コマンド一覧を取得 ---
list_commands() {
    for cmd_file in "$COMMANDS_DIR"/*.sh; do
        [ -f "$cmd_file" ] || continue
        local cmd_name
        cmd_name=$(basename "$cmd_file" .sh)
        local description
        description=$(grep '^# description:' "$cmd_file" | head -1 | sed 's/^# description: *//')
        printf "  %-12s %s\n" "$cmd_name" "${description:-（説明なし）}"
    done
}

# --- ヘルプ表示 ---
show_help() {
    echo "${TOOL_NAME} - カスタムCLIツール (v${TOOL_VERSION})"
    echo ""
    echo "使い方: ${TOOL_NAME} <コマンド> [オプション] [引数]"
    echo ""
    echo "利用可能なコマンド:"
    list_commands
    echo "  help        このヘルプを表示する"
    echo ""
    echo "詳細: ${TOOL_NAME} help <コマンド>"
}

# --- コマンドのヘルプ表示 ---
show_command_help() {
    local cmd_name="$1"
    local cmd_file="${COMMANDS_DIR}/${cmd_name}.sh"

    if [ ! -f "$cmd_file" ]; then
        log_error "不明なコマンド: $cmd_name"
        return 1
    fi

    source "$cmd_file"
    if declare -f cmd_help > /dev/null; then
        cmd_help
    else
        echo "コマンド '$cmd_name' にヘルプはありません。"
    fi
}

# --- メイン処理 ---
main() {
    # 引数なしの場合
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi

    # グローバルオプション（コマンドの前）
    export VERBOSE=false
    export DRY_RUN=false

    local command=""
    local -a cmd_args=()

    for arg in "$@"; do
        case "$arg" in
            --verbose) VERBOSE=true ;;
            --dry-run) DRY_RUN=true ;;
            *)
                if [ -z "$command" ]; then
                    command="$arg"
                else
                    cmd_args+=("$arg")
                fi
                ;;
        esac
    done

    # ヘルプコマンド
    if [ "$command" = "help" ]; then
        if [ ${#cmd_args[@]} -gt 0 ]; then
            show_command_help "${cmd_args[0]}"
        else
            show_help
        fi
        exit 0
    fi

    # コマンドファイルの存在確認
    local cmd_file="${COMMANDS_DIR}/${command}.sh"
    if [ ! -f "$cmd_file" ]; then
        log_error "不明なコマンド: $command"
        echo ""
        echo "利用可能なコマンド:"
        list_commands
        exit 1
    fi

    # コマンドの実行
    log_debug "コマンド実行: $command ${cmd_args[*]:-}"
    source "$cmd_file"
    cmd_main "${cmd_args[@]:-}"
}

main "$@"
```

**lib/common.sh（共通ライブラリ）:**

```bash
# lib/common.sh - 共通関数

# --- カラー定義 ---
if [ -t 1 ]; then
    readonly CLR_RED='\033[31m'
    readonly CLR_GREEN='\033[32m'
    readonly CLR_YELLOW='\033[33m'
    readonly CLR_CYAN='\033[36m'
    readonly CLR_BOLD='\033[1m'
    readonly CLR_RESET='\033[0m'
else
    readonly CLR_RED="" CLR_GREEN="" CLR_YELLOW="" CLR_CYAN="" CLR_BOLD="" CLR_RESET=""
fi

# --- ログ関数 ---
log_info()  { echo -e "${CLR_GREEN}[INFO]${CLR_RESET} $*" >&2; }
log_warn()  { echo -e "${CLR_YELLOW}[WARN]${CLR_RESET} $*" >&2; }
log_error() { echo -e "${CLR_RED}[ERROR]${CLR_RESET} $*" >&2; }
log_debug() { ${VERBOSE:-false} && echo -e "${CLR_CYAN}[DEBUG]${CLR_RESET} $*" >&2 || true; }

# --- ユーティリティ ---
run() {
    if ${DRY_RUN:-false}; then
        log_info "[DRY] $*"
        return 0
    fi
    log_debug "実行: $*"
    "$@"
}

confirm() {
    local message="${1:-続行しますか？}"
    read -rp "$message (y/N): " answer
    [[ "${answer,,}" == "y" ]]
}
```

**commands/hello.sh（helloコマンド）:**

```bash
#!/usr/bin/env bash
# description: 挨拶を表示する
# usage: hello [--count N]

cmd_help() {
    cat <<EOF
hello - 挨拶を表示する

使い方: mytool hello [--count N]

オプション:
  --count N   挨拶の回数（デフォルト: 1）
  --help      このヘルプを表示する
EOF
}

cmd_main() {
    local count=1

    while [ $# -gt 0 ]; do
        case "$1" in
            --count) count="$2"; shift 2 ;;
            --help)  cmd_help; return 0 ;;
            *)       log_error "不明なオプション: $1"; return 1 ;;
        esac
    done

    for ((i = 1; i <= count; i++)); do
        echo "Hello, World! ($i)"
    done
}
```

**commands/greet.sh（greetコマンド）:**

```bash
#!/usr/bin/env bash
# description: 名前付きで挨拶する
# usage: greet [--name NAME] [--lang LANG]

cmd_help() {
    cat <<EOF
greet - 名前付きで挨拶する

使い方: mytool greet [--name NAME] [--lang LANG]

オプション:
  --name NAME   名前（デフォルト: World）
  --lang LANG   言語（ja/en、デフォルト: ja）
  --help        このヘルプを表示する
EOF
}

cmd_main() {
    local name="World"
    local lang="ja"

    while [ $# -gt 0 ]; do
        case "$1" in
            --name) name="$2"; shift 2 ;;
            --lang) lang="$2"; shift 2 ;;
            --help) cmd_help; return 0 ;;
            *)      log_error "不明なオプション: $1"; return 1 ;;
        esac
    done

    case "$lang" in
        ja)
            local hour
            hour=$(date "+%H")
            if (( 10#$hour < 12 )); then
                echo "おはようございます、${name}さん！"
            elif (( 10#$hour < 18 )); then
                echo "こんにちは、${name}さん！"
            else
                echo "こんばんは、${name}さん！"
            fi
            ;;
        en)
            echo "Hello, ${name}!"
            ;;
        *)
            log_error "未対応の言語: $lang (ja/en)"
            return 1
            ;;
    esac
}
```

**commands/sysinfo.sh（sysinfoコマンド）:**

```bash
#!/usr/bin/env bash
# description: システム情報を表示する
# usage: sysinfo [--section SECTIONS]

cmd_help() {
    cat <<EOF
sysinfo - システム情報を表示する

使い方: mytool sysinfo [--section SECTIONS]

オプション:
  --section SECTIONS  表示セクション（カンマ区切り: os,cpu,mem,disk）
                      デフォルト: すべて
  --help              このヘルプを表示する
EOF
}

cmd_main() {
    local sections="os,cpu,mem,disk"

    while [ $# -gt 0 ]; do
        case "$1" in
            --section) sections="$2"; shift 2 ;;
            --help)    cmd_help; return 0 ;;
            *)         log_error "不明なオプション: $1"; return 1 ;;
        esac
    done

    if [[ ",$sections," == *",os,"* ]]; then
        echo "■ OS情報"
        printf "  %-14s %s\n" "ホスト名:" "$(hostname)"
        printf "  %-14s %s\n" "OS:" "$(uname -s)"
        printf "  %-14s %s\n" "カーネル:" "$(uname -r)"
        printf "  %-14s %s\n" "アーキテクチャ:" "$(uname -m)"
        echo ""
    fi

    if [[ ",$sections," == *",cpu,"* ]]; then
        echo "■ CPU情報"
        if [ -f /proc/cpuinfo ]; then
            printf "  %-14s %s\n" "モデル:" "$(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | sed 's/^ //')"
            printf "  %-14s %s\n" "コア数:" "$(grep -c 'processor' /proc/cpuinfo)"
        elif command -v sysctl > /dev/null 2>&1; then
            printf "  %-14s %s\n" "モデル:" "$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo '不明')"
        fi
        echo ""
    fi

    if [[ ",$sections," == *",mem,"* ]]; then
        echo "■ メモリ情報"
        if command -v free > /dev/null 2>&1; then
            free -h | awk '/^Mem:/ {printf "  %-14s %s / %s\n", "使用量:", $3, $2}'
        fi
        echo ""
    fi

    if [[ ",$sections," == *",disk,"* ]]; then
        echo "■ ディスク情報"
        df -h 2>/dev/null | awk 'NR>1 && /^\// {printf "  %-14s %s / %s (%s)\n", $6, $3, $2, $5}'
        echo ""
    fi
}
```

**commands/backup.sh（backupコマンド）:**

```bash
#!/usr/bin/env bash
# description: ディレクトリをバックアップする
# usage: backup <ソース> [--dest DIR] [--keep N]

cmd_help() {
    cat <<EOF
backup - ディレクトリをバックアップする

使い方: mytool backup <ソースディレクトリ> [オプション]

オプション:
  --dest DIR    バックアップ先（デフォルト: ./backups/）
  --keep N      保持する世代数（デフォルト: 5）
  --help        このヘルプを表示する
EOF
}

cmd_main() {
    local source_dir=""
    local dest_dir="./backups"
    local keep=5

    while [ $# -gt 0 ]; do
        case "$1" in
            --dest) dest_dir="$2"; shift 2 ;;
            --keep) keep="$2"; shift 2 ;;
            --help) cmd_help; return 0 ;;
            -*)     log_error "不明なオプション: $1"; return 1 ;;
            *)      source_dir="$1"; shift ;;
        esac
    done

    if [ -z "$source_dir" ]; then
        log_error "ソースディレクトリを指定してください"
        cmd_help
        return 1
    fi

    if [ ! -d "$source_dir" ]; then
        log_error "ディレクトリが見つかりません: $source_dir"
        return 1
    fi

    local timestamp
    timestamp=$(date "+%Y%m%d_%H%M%S")
    local backup_path="${dest_dir}/backup_${timestamp}"

    log_info "バックアップ: $source_dir → $backup_path"

    run mkdir -p "$backup_path"

    if command -v rsync > /dev/null 2>&1; then
        run rsync -a "$source_dir/" "$backup_path/"
    else
        run cp -r "$source_dir"/. "$backup_path/"
    fi

    local file_count
    file_count=$(find "$backup_path" -type f 2>/dev/null | wc -l | tr -d '[:space:]')
    log_info "バックアップ完了: ${file_count} ファイル"

    # 古いバックアップの削除
    local -a old_backups=()
    mapfile -t old_backups < <(ls -dt "${dest_dir}"/backup_* 2>/dev/null)
    local total=${#old_backups[@]}
    if [ "$total" -gt "$keep" ]; then
        log_info "古いバックアップを削除: $((total - keep))件"
        for ((i = keep; i < total; i++)); do
            run rm -rf "${old_backups[$i]}"
        done
    fi
}
```

</details>

<details>
<summary>解答例（改良版 ─ 自動補完とプラグインバリデーション付き）</summary>

改良版では以下を追加します。

**mytool.sh に追加する改良点:**

```bash
#!/usr/bin/env bash
set -euo pipefail

readonly TOOL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly TOOL_NAME="mytool"
readonly TOOL_VERSION="1.0.0"
readonly COMMANDS_DIR="${TOOL_DIR}/commands"
readonly LIB_DIR="${TOOL_DIR}/lib"

source "${LIB_DIR}/common.sh"

# --- コマンドファイルのバリデーション ---
validate_command_file() {
    local cmd_file="$1"
    local cmd_name
    cmd_name=$(basename "$cmd_file" .sh)
    local errors=0

    # 必須関数のチェック
    if ! grep -q '^cmd_main()' "$cmd_file"; then
        log_warn "コマンド '$cmd_name': cmd_main() が定義されていません"
        errors=$((errors + 1))
    fi

    if ! grep -q '^cmd_help()' "$cmd_file"; then
        log_warn "コマンド '$cmd_name': cmd_help() が定義されていません"
        errors=$((errors + 1))
    fi

    if ! grep -q '^# description:' "$cmd_file"; then
        log_warn "コマンド '$cmd_name': # description: が記述されていません"
        errors=$((errors + 1))
    fi

    return $errors
}

# --- 類似コマンド候補の表示 ---
suggest_command() {
    local input="$1"
    local -a suggestions=()

    for cmd_file in "$COMMANDS_DIR"/*.sh; do
        [ -f "$cmd_file" ] || continue
        local cmd_name
        cmd_name=$(basename "$cmd_file" .sh)

        # 前方一致
        if [[ "$cmd_name" == "$input"* ]]; then
            suggestions+=("$cmd_name")
        fi
    done

    if [ ${#suggestions[@]} -gt 0 ]; then
        echo ""
        echo "もしかして:"
        for s in "${suggestions[@]}"; do
            echo "  ${TOOL_NAME} ${s}"
        done
    fi
}

# --- Bash補完スクリプト生成 ---
generate_completion() {
    cat <<'COMPLETION_EOF'
_mytool_completion() {
    local cur prev commands
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    if [ "$COMP_CWORD" -eq 1 ]; then
        commands=$(ls "${COMMANDS_DIR}"/*.sh 2>/dev/null | xargs -I{} basename {} .sh)
        COMPREPLY=($(compgen -W "$commands help" -- "$cur"))
    fi
}
complete -F _mytool_completion mytool
COMPLETION_EOF
}

# --- コマンド一覧 ---
list_commands() {
    for cmd_file in "$COMMANDS_DIR"/*.sh; do
        [ -f "$cmd_file" ] || continue
        local cmd_name
        cmd_name=$(basename "$cmd_file" .sh)
        local description
        description=$(grep '^# description:' "$cmd_file" | head -1 | sed 's/^# description: *//')
        printf "  %-12s %s\n" "$cmd_name" "${description:-（説明なし）}"
    done
}

# --- ヘルプ ---
show_help() {
    echo -e "${CLR_BOLD}${TOOL_NAME}${CLR_RESET} - カスタムCLIツール (v${TOOL_VERSION})"
    echo ""
    echo "使い方: ${TOOL_NAME} <コマンド> [オプション] [引数]"
    echo ""
    echo "利用可能なコマンド:"
    list_commands
    echo "  help        このヘルプを表示する"
    echo ""
    echo "グローバルオプション:"
    echo "  --verbose   詳細出力"
    echo "  --dry-run   ドライラン"
    echo ""
    echo "詳細: ${TOOL_NAME} help <コマンド>"
    echo "補完: eval \"\$(${TOOL_NAME} --completion)\""
}

# --- メイン処理 ---
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi

    export VERBOSE=false
    export DRY_RUN=false

    local command=""
    local -a cmd_args=()

    for arg in "$@"; do
        case "$arg" in
            --verbose)    VERBOSE=true ;;
            --dry-run)    DRY_RUN=true ;;
            --completion) generate_completion; exit 0 ;;
            --version)    echo "${TOOL_NAME} v${TOOL_VERSION}"; exit 0 ;;
            *)
                if [ -z "$command" ]; then
                    command="$arg"
                else
                    cmd_args+=("$arg")
                fi
                ;;
        esac
    done

    case "$command" in
        help)
            if [ ${#cmd_args[@]} -gt 0 ]; then
                local help_cmd="${cmd_args[0]}"
                local help_file="${COMMANDS_DIR}/${help_cmd}.sh"
                [ -f "$help_file" ] || { log_error "不明なコマンド: $help_cmd"; exit 1; }
                source "$help_file"
                cmd_help
            else
                show_help
            fi
            ;;
        *)
            local cmd_file="${COMMANDS_DIR}/${command}.sh"
            if [ ! -f "$cmd_file" ]; then
                log_error "不明なコマンド: $command"
                suggest_command "$command"
                exit 1
            fi
            source "$cmd_file"
            cmd_main "${cmd_args[@]:-}"
            ;;
    esac
}

main "$@"
```

**初心者向けとの違い:**
- コマンドファイルのバリデーション → プラグイン作成時のミスを早期発見
- 類似コマンドのサジェスト → タイプミス時に候補を表示
- Bash補完スクリプト生成 → `eval "$(./mytool.sh --completion)"` でTab補完が有効に
- `--version` オプション → バージョン表示
- カラー付きヘルプ → 見やすい
- グローバルオプションの明示 → ヘルプに共通オプションを記載

</details>
