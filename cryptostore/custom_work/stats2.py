import time
from typing import NamedTuple, List, Dict, Optional, Tuple
from datetime import datetime, timedelta, timezone

import requests

SECONDS_IN_DAY = 24 * 3600
SECONDS_IN_WEEK = 7 * SECONDS_IN_DAY

Timestamp_float = float
Granularity = str


class Stats(NamedTuple):
    ts: Timestamp_float
    end_ts: Timestamp_float
    open: float = 0
    high: float = 0
    low: float = 0
    close: float = 0
    volume: float = 0


class InfluxConfig(NamedTuple):
    host: str
    db: str
    exchange: str
    pair: str


class Trade(NamedTuple):
    feed: str                           # 'BITMEX'
    pair: str                           # 'XBTUSD'
    timestamp: Timestamp_float          # 1586722261.612
    receipt_timestamp: Timestamp_float  # 1586722261.648669
    side: str                           # 'sell'
    amount: float                       # 2.0
    price: float                        # 7158.0
    id: str                             # '72e3cf51-8d47-4f81-8828-8da727eec651'


i_1s : Granularity = '1s'
i_5s : Granularity = '5s'
i_10s : Granularity = '10s'
i_30s : Granularity = '30s'
i_1mi : Granularity = '1mi'
i_2mi : Granularity = '2mi'
i_5mi : Granularity = '5mi'
i_10mi : Granularity = '10mi'
i_15mi : Granularity = '15mi'
i_30mi : Granularity = '30mi'
i_1h : Granularity = '1h'
i_2h : Granularity = '2h'
i_4h : Granularity = '4h'
i_12h : Granularity = '12h'
i_1d : Granularity = '1d'
i_3d : Granularity = '3d'
i_1w : Granularity = '1w'
i_2w : Granularity = '2w'
i_1mo : Granularity = '1mo'
i_3mo : Granularity = '3mo'
i_6mo : Granularity = '6mo'
i_1y : Granularity = '1y'

granularities = [i_1s, i_5s, i_10s, i_30s, i_1mi, i_2mi, i_5mi, i_10mi, i_15mi, i_30mi, i_1h, i_2h, i_4h, i_12h, i_1d,
    i_3d, i_1w, i_2w, i_1mo, i_3mo, i_6mo, i_1y]


IntervalsCache = Dict[Granularity, Optional[Stats]]


def ts_floor_ceil(timestamp: Timestamp_float, divider: int) -> (Timestamp_float, Timestamp_float):
    start = (timestamp // divider) * divider
    return start, start + divider


def add_months(dt: datetime, months):
    return datetime(dt.year + (dt.month + months - 1) // 12, (dt.month + months - 1) % 12 + 1, 1, tzinfo=timezone.utc)


def months_floor_ceil(timestamp: Timestamp_float, months):
    dt = datetime.fromtimestamp(timestamp)
    start = datetime(dt.year, ((dt.month-1) // months) * months + 1, 1, tzinfo=timezone.utc)
    end = add_months(start, months)
    return datetime.timestamp(start), datetime.timestamp(end)


def get_interval_heads(granularity: Granularity, timestamp: Timestamp_float) -> (Timestamp_float, Timestamp_float):
    if granularity == i_1s:
        return ts_floor_ceil(timestamp, 1)
    if granularity == i_5s:
        return ts_floor_ceil(timestamp, 5)
    if granularity == i_10s:
        return ts_floor_ceil(timestamp, 10)
    if granularity == i_30s:
        return ts_floor_ceil(timestamp, 30)
    if granularity == i_1mi:
        return ts_floor_ceil(timestamp, 60)
    if granularity == i_2mi:
        return ts_floor_ceil(timestamp, 120)
    if granularity == i_5mi:
        return ts_floor_ceil(timestamp, 300)
    if granularity == i_10mi:
        return ts_floor_ceil(timestamp, 600)
    if granularity == i_15mi:
        return ts_floor_ceil(timestamp, 900)
    if granularity == i_30mi:
        return ts_floor_ceil(timestamp, 1800)
    if granularity == i_1h:
        return ts_floor_ceil(timestamp, 3600)
    if granularity == i_2h:
        return  ts_floor_ceil(timestamp, 7200)
    if granularity == i_4h:
        return ts_floor_ceil(timestamp, 14400)
    if granularity == i_12h:
        return ts_floor_ceil(timestamp, 43200)
    if granularity == i_1d:
        return ts_floor_ceil(timestamp, SECONDS_IN_DAY)
    if granularity == i_3d:
        return ts_floor_ceil(timestamp, 3 * SECONDS_IN_DAY)
    if granularity == i_1w:
        dt = datetime.fromtimestamp(ts_floor_ceil(timestamp, SECONDS_IN_DAY)[0])
        start = datetime.timestamp(dt - timedelta(days=dt.weekday()))
        return start, start + SECONDS_IN_WEEK
    if granularity == i_2w:
        dt = datetime.fromtimestamp(ts_floor_ceil(timestamp, SECONDS_IN_DAY)[0])
        start = datetime.timestamp(dt - timedelta(days=dt.weekday()))
        if (start // SECONDS_IN_WEEK) % 2 == 1:
            start = start - SECONDS_IN_WEEK
        return start, start + 2 * SECONDS_IN_WEEK
    if granularity == i_1mo:
        return months_floor_ceil(timestamp, 1)
    if granularity == i_3mo:
        return months_floor_ceil(timestamp, 3)
    if granularity == i_6mo:
        return months_floor_ceil(timestamp, 6)
    if granularity == i_1y:
        return months_floor_ceil(timestamp, 12)


granularity_for_compute = {
    i_1s: None,
    i_5s: i_1s,
    i_10s: i_5s,
    i_30s: i_10s,
    i_1mi: i_30s,
    i_2mi: i_1mi,
    i_5mi: i_1mi,
    i_10mi: i_5mi,
    i_15mi: i_5mi,
    i_30mi: i_15mi,
    i_1h: i_30mi,
    i_2h: i_1h,
    i_4h: i_2h,
    i_12h: i_4h,
    i_1d: i_12h,
    i_3d: i_1d,
    i_1w: i_1d,
    i_2w: i_1w,
    i_1mo: i_1d,
    i_3mo: i_1mo,
    i_6mo: i_3mo,
    i_1y: i_6mo,
}


def compose_stats(stats_list: List[Stats], start: Timestamp_float, end: Timestamp_float) -> Optional[Stats]:
    stats_list = [i for i in stats_list if i is not None]
    if len(stats_list) == 0:
        return None
    first = stats_list[0]
    (open, high, low, close, volume) = (first.open, first.high, first.low, first.close, first.volume)

    for stats in stats_list[1:]:
        high = max(high, stats.high)
        low = min(low, stats.low)
        close = stats.close
        volume = volume + stats.volume
    return Stats(
        ts=start,
        end_ts=end,
        open=open,
        high=high,
        low=low,
        close=close,
        volume=volume,
    )


def query_db(config: InfluxConfig, granularity: Granularity, start: Timestamp_float, end: Timestamp_float) -> List[Stats]:
    return []
    try:
        r = requests.get(
            f"{config.host}/query?db={config.db}",
            params={
                'q': f'SELECT * '
                     f'from "STATS-{config.exchange}" '
                     f'where pair=\'{config.pair}\' and granularity=\'{granularity}\' and time >=\'{start}\' and '
                     f'time < \'{end}\''}
        )
        response = r.json()
        print(response['results'][0])
        return []
    except:
        print("Exception at db query")
        return []


def init_cache(config: InfluxConfig) -> IntervalsCache:
    cache = {}
    now = time.time()
    for granularity in granularities[1:]:
        start, end = get_interval_heads(granularity, now)
        base_granularity = granularity_for_compute[granularity]
        base_stats = query_db(config, base_granularity, start, end)
        composed_stats = compose_stats(base_stats + [cache.get(base_granularity)], start, end)
        cache[granularity] = composed_stats
    return cache


def update_stats(
        cache: IntervalsCache,
        trade: Trade,
        stats_to_write: List[Tuple[Stats, Granularity]]
) -> (List[Tuple[Stats, Granularity]], IntervalsCache):

    for granularity in granularities:
        granularity_cache = cache.get(granularity)
        if granularity_cache is None or trade.timestamp >= granularity_cache.end_ts:
            if granularity_cache is not None:
                stats_to_write.append((granularity_cache, granularity))
            start, end = get_interval_heads(granularity, trade.timestamp)
            cache[granularity] = Stats(
                ts=start,
                end_ts=end,
                open=trade.price,
                high=trade.price,
                low=trade.price,
                close=trade.price,
                volume=trade.amount,
            )
        else:
            # just update the old cache
            cache[granularity] = compose_stats(
                [
                    granularity_cache,
                    Stats(
                        ts=granularity_cache.ts,
                        end_ts=granularity_cache.end_ts,
                        open=trade.price,
                        high=trade.price,
                        low=trade.price,
                        close=trade.price,
                        volume=trade.amount),
                ],
                granularity_cache.ts,
                granularity_cache.end_ts
            )
    return stats_to_write, cache


