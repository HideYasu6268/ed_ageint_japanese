"""Massive の市場データ API から株価を取得する。キーが設定されていない場合はシミュレーターを使う。

MASSIVE_API_KEY を設定するとライブデータを使用する。設定しない場合は market_simulator から
価格を取得するので、トレーディングフロア全体がそのままでも動作する。
"""

import os
from dotenv import load_dotenv
from massive import RESTClient
from .market_simulator import simulated_price

load_dotenv(override=True)

massive_api_key = os.getenv("MASSIVE_API_KEY")


def _last_trade(client: RESTClient, symbol: str) -> float:
    return float(client.get_last_trade(symbol).price)


def _snapshot(client: RESTClient, symbol: str) -> float:
    snapshot = client.get_snapshot_ticker("stocks", symbol)
    return float(snapshot.min.close or snapshot.prev_day.close)


def _previous_close(client: RESTClient, symbol: str) -> float:
    return float(client.get_previous_close_agg(symbol)[0].close)


# 最良の価格を最初に、前日終値を最後に試す。下位プランでは早い段階の呼び出しが拒否されるため、
# 最初に成功したティアを記憶しておき、次回はそこから試す。
price_methods = [_last_trade, _snapshot, _previous_close]
plan_tier = 0


def get_share_price(symbol: str) -> float:
    """Massive またはシミュレーターから、指定した銘柄の現在価格を返す。"""
    if massive_api_key:
        try:
            return get_share_price_massive(symbol)
        except Exception as e:
            print(f"Massive API unavailable ({e}); using a simulated price")
    return simulated_price(symbol)


def get_share_price_massive(symbol: str) -> float:
    """契約プランで許可されている範囲で最良の価格を取得する。成功したティアを記憶し、失敗の繰り返しを避ける。"""
    global plan_tier
    client = RESTClient(massive_api_key)
    for tier in range(plan_tier, len(price_methods)):
        try:
            price = price_methods[tier](client, symbol)
            plan_tier = tier
            return price
        except Exception:
            continue
    raise RuntimeError(f"No Massive price available for {symbol}")


def is_market_open() -> bool:
    """米国市場が開いているかどうか。シミュレーションデータ利用時や Massive に接続できない場合は True。"""
    if not massive_api_key:
        return True
    try:
        client = RESTClient(massive_api_key)
        return client.get_market_status().market == "open"
    except Exception:
        return True
