"""市場データ API キーが設定されていない場合に使うシミュレートされた株価。

スムーズなバリューノイズを使って、ある時点でのティッカーの信憑性のある価格を生成する。
価格はティッカーとタイムスタンプだけで完全に決まるため、同じ入力からは常に同じ価格が得られ、
かつランダムに飛び跳ねるのではなく、実際の株価のように緩やかに変動する。
"""

import hashlib
import math
from datetime import datetime, timezone

EPOCH = datetime(2025, 1, 1, tzinfo=timezone.utc)
SWING = 0.4  # 価格が基準レベルからどれだけ変動するか(割合)
OCTAVES = 5  # ノイズの層の数。緩やかな日次トレンドから日中の細かな揺れまで


def _seed(ticker: str) -> int:
    """ティッカーから導出される、プロセス間で再現可能な安定した整数値。"""
    digest = hashlib.sha256(ticker.upper().encode()).digest()
    return int.from_bytes(digest[:8], "big")


def _lattice(seed: int, n: int) -> float:
    """整数点 n における、再現可能な [-1, 1] の範囲の疑似ランダム値。"""
    digest = hashlib.sha256(f"{seed}:{n}".encode()).digest()
    return int.from_bytes(digest[:4], "big") / 0xFFFFFFFF * 2 - 1


def _noise(seed: int, x: float) -> float:
    """x の周囲の格子点の間を滑らかに補間したノイズ。"""
    low = math.floor(x)
    t = x - low
    smooth = t * t * (3 - 2 * t)
    return _lattice(seed, low) * (1 - smooth) + _lattice(seed, low + 1) * smooth


def _wander(seed: int, x: float) -> float:
    """複数のオクターブのノイズを合成し、自然なトレンド+揺れの形を作る。"""
    total = 0.0
    normaliser = 0.0
    amplitude = 1.0
    frequency = 1.0
    for _ in range(OCTAVES):
        total += amplitude * _noise(seed, x * frequency)
        normaliser += amplitude
        amplitude /= 2
        frequency *= 2
    return total / normaliser


def simulated_price(ticker: str, when: datetime | None = None) -> float:
    """ティッカーについて、信憑性のある滑らかに変動する株価を返す。"""
    when = when or datetime.now(timezone.utc)
    seed = _seed(ticker)
    base = 20 + seed % 480
    days = (when - EPOCH).total_seconds() / 86400
    return round(base * (1 + SWING * _wander(seed, days)), 2)
