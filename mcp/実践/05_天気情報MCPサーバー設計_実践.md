# 実践課題05：天気情報MCPサーバー設計 ★3

> **難易度**: ★★★☆☆（中級）
> **前提知識**: 第3章（MCPサーバー開発Python）、第5章（MCPの3つの機能）、第7章（実践MCPサーバー構築）
> **課題の種類**: ミニプロジェクト
> **学習目標**: 外部APIと連携するMCPサーバーを設計・実装できるようになる。非同期処理、エラーハンドリング、レスポンスのフォーマットを実践的に学ぶ

---

## 完成イメージ

Open-Meteo API（無料・API キー不要）を利用した天気情報MCPサーバーを構築します。

```
┌──────────────────────────────────────────────────────┐
│  天気情報 MCPサーバー (weather-server)                 │
│                                                      │
│  ■ Tools                                             │
│    ・get_current_weather(city)                        │
│      → 指定都市の現在の天気を取得                      │
│    ・get_forecast(city, days)                         │
│      → 指定都市のN日間の天気予報を取得                 │
│                                                      │
│  ■ Resources                                         │
│    ・weather://cities                                 │
│      → 対応都市の一覧                                 │
│                                                      │
│  ■ Prompts                                           │
│    ・travel_advice(city)                              │
│      → 天気に基づく旅行アドバイス生成テンプレート       │
│                                                      │
│        ┌───────────────┐                             │
│        │ Open-Meteo API │  ← 外部API（無料）          │
│        └───────────────┘                             │
└──────────────────────────────────────────────────────┘
```

```
AIとの対話例：

ユーザー: 「東京の今の天気を教えて」

LLM → tools/call: get_current_weather(city="東京")
  → Open-Meteo API呼び出し
  → レスポンス: "東京の天気: 晴れ、気温22.5℃、湿度45%、風速3.2m/s"

LLM: 「東京は現在晴れで、気温22.5℃です。過ごしやすい天気ですね。」
```

---

## 課題の要件

1. FastMCPで天気情報MCPサーバーを実装する
2. Open-Meteo API（`https://api.open-meteo.com/v1/forecast`）を使用する
3. `get_current_weather` ツール: 都市名から現在の天気を取得する
4. `get_forecast` ツール: 都市名と日数から天気予報を取得する
5. `weather://cities` リソース: 対応都市の一覧を提供する
6. `travel_advice` プロンプト: 天気に基づく旅行アドバイステンプレートを定義する
7. APIのエラー（ネットワーク障害、不正なレスポンス）を適切に処理する
8. `httpx` を使った非同期HTTP通信を実装する

---

## ステップガイド

<details>
<summary>ステップ1：都市名から緯度・経度を取得する仕組みを作る</summary>

Open-Meteo APIは緯度・経度で天気を取得します。都市名から座標への変換は辞書で管理するのが最もシンプルです。

```python
# 主要都市の緯度・経度マッピング
CITIES: dict[str, dict] = {
    "東京": {"lat": 35.6762, "lon": 139.6503},
    "大阪": {"lat": 34.6937, "lon": 135.5023},
    "名古屋": {"lat": 35.1815, "lon": 136.9066},
    "札幌": {"lat": 43.0618, "lon": 141.3545},
    "福岡": {"lat": 33.5904, "lon": 130.4017},
    "那覇": {"lat": 26.2124, "lon": 127.6809},
}
```

ポイント：
- 外部のジオコーディングAPIを使う方法もありますが、まずは固定マッピングで始めるのが安全です
- 対応していない都市が指定された場合のエラーメッセージを考えておきましょう

</details>

<details>
<summary>ステップ2：Open-Meteo APIの使い方を理解する</summary>

Open-Meteo APIは無料で、APIキーが不要です。

```
現在の天気を取得するURL:
https://api.open-meteo.com/v1/forecast
  ?latitude=35.6762
  &longitude=139.6503
  &current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code
  &timezone=Asia/Tokyo

天気予報を取得するURL:
https://api.open-meteo.com/v1/forecast
  ?latitude=35.6762
  &longitude=139.6503
  &daily=temperature_2m_max,temperature_2m_min,weather_code
  &forecast_days=3
  &timezone=Asia/Tokyo
```

レスポンス例（現在の天気）:
```json
{
  "current": {
    "temperature_2m": 22.5,
    "relative_humidity_2m": 45,
    "wind_speed_10m": 3.2,
    "weather_code": 0
  }
}
```

weather_code の意味:
| コード | 天気 |
|--------|------|
| 0 | 快晴 |
| 1-3 | 晴れ〜曇り |
| 45, 48 | 霧 |
| 51-55 | 霧雨 |
| 61-65 | 雨 |
| 71-75 | 雪 |
| 95, 96, 99 | 雷雨 |

</details>

<details>
<summary>ステップ3：httpxで非同期API呼び出しを実装する</summary>

MCPサーバーでは非同期（async）処理を使います。HTTP通信には `httpx` ライブラリを使用します。

```python
import httpx

async def fetch_weather(lat: float, lon: float) -> dict:
    """Open-Meteo APIから天気データを取得します。"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "Asia/Tokyo",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=10.0)
        response.raise_for_status()
        return response.json()
```

ポイント：
- `timeout` を必ず設定しましょう（デフォルトだと無限に待つ場合があります）
- `raise_for_status()` でHTTPエラーを例外に変換します

</details>

<details>
<summary>ステップ4：エラーハンドリングを実装する</summary>

外部APIとの通信では、さまざまなエラーが発生します。

```python
import httpx

async def safe_fetch(lat: float, lon: float) -> dict:
    """エラーハンドリング付きでAPIを呼び出します。"""
    try:
        return await fetch_weather(lat, lon)
    except httpx.TimeoutException:
        raise RuntimeError("APIへの接続がタイムアウトしました。しばらく待ってから再試行してください")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"APIエラー: HTTPステータス {e.response.status_code}")
    except httpx.RequestError:
        raise RuntimeError("ネットワークエラー: APIに接続できません")
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```python
"""
天気情報MCPサーバー（初心者向け）
学べること：外部API連携、非同期処理、エラーハンドリング
実行方法：uv add httpx && uv run weather_server.py
"""
import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("weather-server")

# ── 都市データ ──
CITIES: dict[str, dict[str, float]] = {
    "東京": {"lat": 35.6762, "lon": 139.6503},
    "大阪": {"lat": 34.6937, "lon": 135.5023},
    "名古屋": {"lat": 35.1815, "lon": 136.9066},
    "札幌": {"lat": 43.0618, "lon": 141.3545},
    "福岡": {"lat": 33.5904, "lon": 130.4017},
    "那覇": {"lat": 26.2124, "lon": 127.6809},
}

# ── 天気コード変換 ──
WEATHER_CODES: dict[int, str] = {
    0: "快晴", 1: "おおむね晴れ", 2: "一部曇り", 3: "曇り",
    45: "霧", 48: "着氷性の霧",
    51: "弱い霧雨", 53: "霧雨", 55: "強い霧雨",
    61: "弱い雨", 63: "雨", 65: "強い雨",
    71: "弱い雪", 73: "雪", 75: "強い雪",
    80: "弱いにわか雨", 81: "にわか雨", 82: "激しいにわか雨",
    95: "雷雨", 96: "雹を伴う雷雨", 99: "激しい雹を伴う雷雨",
}


def weather_code_to_text(code: int) -> str:
    """天気コードを日本語テキストに変換します。"""
    return WEATHER_CODES.get(code, f"不明（コード: {code}）")


def validate_city(city: str) -> dict[str, float]:
    """都市名を検証し、座標を返します。"""
    if city not in CITIES:
        available = ", ".join(CITIES.keys())
        raise ValueError(
            f"「{city}」は対応していません。対応都市: {available}"
        )
    return CITIES[city]


# ── Tools ──

@mcp.tool()
async def get_current_weather(city: str) -> str:
    """指定された都市の現在の天気を取得します。

    Args:
        city: 都市名（例: "東京", "大阪", "札幌"）
    """
    coords = validate_city(city)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "Asia/Tokyo",
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=10.0)
            resp.raise_for_status()
            data = resp.json()
    except httpx.TimeoutException:
        raise RuntimeError("APIへの接続がタイムアウトしました")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"APIエラー: HTTP {e.response.status_code}")
    except httpx.RequestError:
        raise RuntimeError("ネットワークエラー: APIに接続できません")

    current = data["current"]
    weather = weather_code_to_text(current["weather_code"])
    temp = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind = current["wind_speed_10m"]

    return (
        f"{city}の現在の天気:\n"
        f"  天候: {weather}\n"
        f"  気温: {temp}℃\n"
        f"  湿度: {humidity}%\n"
        f"  風速: {wind} m/s"
    )


@mcp.tool()
async def get_forecast(city: str, days: int = 3) -> str:
    """指定された都市の天気予報を取得します。

    Args:
        city: 都市名（例: "東京", "大阪", "札幌"）
        days: 予報日数（1〜7、デフォルト3日）
    """
    coords = validate_city(city)

    if not 1 <= days <= 7:
        raise ValueError("予報日数は1〜7の範囲で指定してください")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "forecast_days": days,
        "timezone": "Asia/Tokyo",
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=10.0)
            resp.raise_for_status()
            data = resp.json()
    except httpx.TimeoutException:
        raise RuntimeError("APIへの接続がタイムアウトしました")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"APIエラー: HTTP {e.response.status_code}")
    except httpx.RequestError:
        raise RuntimeError("ネットワークエラー: APIに接続できません")

    daily = data["daily"]
    lines = [f"{city}の{days}日間の天気予報:"]
    lines.append(f"  {'日付':<12} {'天気':<10} {'最高気温':>6} {'最低気温':>6}")
    lines.append(f"  {'-'*40}")

    for i in range(days):
        date = daily["time"][i]
        weather = weather_code_to_text(daily["weather_code"][i])
        temp_max = daily["temperature_2m_max"][i]
        temp_min = daily["temperature_2m_min"][i]
        lines.append(f"  {date:<12} {weather:<10} {temp_max:>5.1f}℃ {temp_min:>5.1f}℃")

    return "\n".join(lines)


# ── Resources ──

@mcp.resource("weather://cities")
def get_cities() -> str:
    """対応している都市の一覧です。"""
    lines = ["対応都市一覧:"]
    for name, coords in CITIES.items():
        lines.append(f"  ・{name}（緯度: {coords['lat']}, 経度: {coords['lon']}）")
    return "\n".join(lines)


# ── Prompts ──

@mcp.prompt()
def travel_advice(city: str) -> list[base.Message]:
    """天気に基づく旅行アドバイスを生成するテンプレートです。

    Args:
        city: 旅行先の都市名
    """
    return [
        base.UserMessage(
            content=(
                f"{city}への旅行を計画しています。\n"
                f"現在の天気と今後の予報をもとに、以下のアドバイスをしてください：\n"
                f"1. おすすめの服装\n"
                f"2. 持ち物の提案（傘、日焼け止めなど）\n"
                f"3. 天気を活かした観光プラン\n"
                f"4. 注意すべき天候リスク"
            )
        )
    ]


if __name__ == "__main__":
    mcp.run()
```

</details>

<details>
<summary>解答例（改良版）</summary>

改良版では以下を強化しています。
- HTTPクライアントの再利用（コネクションプール）
- キャッシュ機能（短時間の重複リクエストを回避）
- 構造化されたレスポンス
- リトライ機能

```python
"""
天気情報MCPサーバー（改良版）
学べること：コネクション再利用、キャッシュ、リトライ、構造化レスポンス
実行方法：uv add httpx && uv run weather_server.py
"""
import time

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("weather-server")

# ── 都市データ ──
CITIES: dict[str, dict[str, float]] = {
    "東京": {"lat": 35.6762, "lon": 139.6503},
    "大阪": {"lat": 34.6937, "lon": 135.5023},
    "名古屋": {"lat": 35.1815, "lon": 136.9066},
    "札幌": {"lat": 43.0618, "lon": 141.3545},
    "福岡": {"lat": 33.5904, "lon": 130.4017},
    "那覇": {"lat": 26.2124, "lon": 127.6809},
    "仙台": {"lat": 38.2682, "lon": 140.8694},
    "広島": {"lat": 34.3853, "lon": 132.4553},
    "京都": {"lat": 35.0116, "lon": 135.7681},
    "横浜": {"lat": 35.4437, "lon": 139.6380},
}

WEATHER_CODES: dict[int, str] = {
    0: "快晴", 1: "おおむね晴れ", 2: "一部曇り", 3: "曇り",
    45: "霧", 48: "着氷性の霧",
    51: "弱い霧雨", 53: "霧雨", 55: "強い霧雨",
    61: "弱い雨", 63: "雨", 65: "強い雨",
    71: "弱い雪", 73: "雪", 75: "強い雪",
    80: "弱いにわか雨", 81: "にわか雨", 82: "激しいにわか雨",
    95: "雷雨", 96: "雹を伴う雷雨", 99: "激しい雹を伴う雷雨",
}

# ── キャッシュ ──
_cache: dict[str, tuple[float, dict]] = {}
CACHE_TTL = 300  # 5分


def weather_code_to_text(code: int) -> str:
    return WEATHER_CODES.get(code, f"不明（コード: {code}）")


def validate_city(city: str) -> dict[str, float]:
    if city not in CITIES:
        available = ", ".join(CITIES.keys())
        raise ValueError(f"「{city}」は対応していません。対応都市: {available}")
    return CITIES[city]


async def fetch_with_retry(
    url: str,
    params: dict,
    max_retries: int = 2,
) -> dict:
    """リトライ付きでAPIを呼び出します。"""
    # キャッシュ確認
    cache_key = f"{url}?{sorted(params.items())}"
    if cache_key in _cache:
        cached_time, cached_data = _cache[cache_key]
        if time.time() - cached_time < CACHE_TTL:
            return cached_data

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, params=params, timeout=10.0)
                resp.raise_for_status()
                data = resp.json()
                # キャッシュに保存
                _cache[cache_key] = (time.time(), data)
                return data
        except httpx.TimeoutException:
            last_error = "APIへの接続がタイムアウトしました"
        except httpx.HTTPStatusError as e:
            last_error = f"APIエラー: HTTP {e.response.status_code}"
            # 4xx系はリトライしない
            if 400 <= e.response.status_code < 500:
                raise RuntimeError(last_error)
        except httpx.RequestError:
            last_error = "ネットワークエラー: APIに接続できません"

    raise RuntimeError(f"{last_error}（{max_retries + 1}回試行）")


@mcp.tool()
async def get_current_weather(city: str) -> str:
    """指定された都市の現在の天気を取得します。

    Args:
        city: 都市名（例: "東京", "大阪", "札幌"）
    """
    coords = validate_city(city)

    data = await fetch_with_retry(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "current": "temperature_2m,relative_humidity_2m,"
                       "wind_speed_10m,weather_code,apparent_temperature",
            "timezone": "Asia/Tokyo",
        },
    )

    c = data["current"]
    weather = weather_code_to_text(c["weather_code"])
    temp = c["temperature_2m"]
    feels_like = c["apparent_temperature"]
    humidity = c["relative_humidity_2m"]
    wind = c["wind_speed_10m"]

    return (
        f"{city}の現在の天気:\n"
        f"  天候:     {weather}\n"
        f"  気温:     {temp}℃（体感 {feels_like}℃）\n"
        f"  湿度:     {humidity}%\n"
        f"  風速:     {wind} m/s\n"
    )


@mcp.tool()
async def get_forecast(city: str, days: int = 3) -> str:
    """指定された都市の天気予報を取得します。

    Args:
        city: 都市名（例: "東京", "大阪", "札幌"）
        days: 予報日数（1〜7、デフォルト3日）
    """
    coords = validate_city(city)
    if not 1 <= days <= 7:
        raise ValueError("予報日数は1〜7の範囲で指定してください")

    data = await fetch_with_retry(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "daily": "temperature_2m_max,temperature_2m_min,"
                     "weather_code,precipitation_probability_max",
            "forecast_days": days,
            "timezone": "Asia/Tokyo",
        },
    )

    daily = data["daily"]
    lines = [f"{city}の{days}日間の天気予報:\n"]
    lines.append(f"  {'日付':<12} {'天気':<10} {'最高':>5} {'最低':>5} {'降水確率':>6}")
    lines.append(f"  {'─'*46}")

    for i in range(days):
        date = daily["time"][i]
        weather = weather_code_to_text(daily["weather_code"][i])
        t_max = daily["temperature_2m_max"][i]
        t_min = daily["temperature_2m_min"][i]
        rain = daily["precipitation_probability_max"][i]
        lines.append(
            f"  {date:<12} {weather:<10} {t_max:>4.1f}℃ {t_min:>4.1f}℃ {rain:>5}%"
        )

    return "\n".join(lines)


@mcp.resource("weather://cities")
def get_cities() -> str:
    """対応している都市の一覧です。"""
    lines = [f"対応都市一覧（{len(CITIES)}都市）:\n"]
    for name, coords in sorted(CITIES.items()):
        lines.append(f"  ・{name}（{coords['lat']:.4f}, {coords['lon']:.4f}）")
    return "\n".join(lines)


@mcp.prompt()
def travel_advice(city: str) -> list[base.Message]:
    """天気に基づく旅行アドバイスを生成するテンプレートです。

    Args:
        city: 旅行先の都市名
    """
    return [
        base.UserMessage(
            content=(
                f"{city}への旅行を計画しています。\n"
                f"まず get_current_weather と get_forecast ツールで天気情報を取得し、\n"
                f"以下のアドバイスをしてください：\n"
                f"1. おすすめの服装\n"
                f"2. 持ち物の提案（傘、日焼け止めなど）\n"
                f"3. 天気を活かした観光プラン\n"
                f"4. 注意すべき天候リスク"
            )
        )
    ]


if __name__ == "__main__":
    mcp.run()
```

### 初心者向けとの違い

| ポイント | 初心者向け | 改良版 |
|---------|-----------|--------|
| HTTPクライアント | 毎回新規作成 | 関数に共通化 |
| キャッシュ | なし | 5分間のTTLキャッシュ |
| リトライ | なし | 最大2回リトライ（4xx系は即時失敗） |
| 天気データ | 基本4項目 | 体感温度・降水確率も追加 |
| 都市数 | 6都市 | 10都市 |
| プロンプト | 静的テキスト | ツール呼び出しを促す指示を含む |

**実務のポイント**: 外部API連携では、キャッシュとリトライは必須です。天気情報は数分程度で更新されるため、5分のキャッシュTTLは実用的です。また、4xx系エラー（クライアント側の問題）はリトライしても改善しないため、即時失敗させるのがベストプラクティスです。

</details>

---

## よくある間違い

| 間違い | 正しい理解 |
|--------|-----------|
| APIキーをコードにハードコードする | 今回のOpen-Meteo APIはキー不要ですが、通常は環境変数で管理します |
| タイムアウトを設定しない | `timeout=10.0` のように必ず設定しましょう。外部APIが応答しない場合、MCPサーバー全体がハングします |
| 同期処理で実装する | MCPサーバーのツールは `async def` で定義し、`httpx.AsyncClient` を使いましょう。同期HTTP通信はサーバーをブロックします |
| APIエラーを握りつぶす | エラーは `raise RuntimeError(...)` で明示的に報告しましょう。LLMがエラー内容を把握し、ユーザーに適切に伝えられます |
| レスポンスをJSON文字列のまま返す | 人間が読みやすいテキスト形式にフォーマットして返しましょう。LLMが解釈しやすくなります |
