# import queue
# from typing import NamedTuple, List, Dict
# from datetime import datetime, timedelta
#
# SECONDS_IN_DAY = 24 * 3600
# SECONDS_IN_WEEK = 7 * SECONDS_IN_DAY
#
# Timestamp_float = float
# Granularity = str
#
# class Stats(NamedTuple):
#     ts: int
#     open: float = 0
#     high: float = 0
#     low: float = 0
#     close: float = 0
#     volume: float = 0
#
# class GranularityCache(NamedTuple):
#     items: List[Stats]
#     last_item_persisted: bool
#
# i_1s : Granularity = '1s'
# i_5s : Granularity = '5s'
# i_10s : Granularity = '10s'
# i_30s : Granularity = '30s'
# i_1mi : Granularity = '1mi'
# i_2mi : Granularity = '2mi'
# i_5mi : Granularity = '5mi'
# i_10mi : Granularity = '10mi'
# i_15mi : Granularity = '15mi'
# i_30mi : Granularity = '30mi'
# i_1h : Granularity = '1h'
# i_2h : Granularity = '2h'
# i_4h : Granularity = '4h'
# i_12h : Granularity = '12h'
# i_1d : Granularity = '1d'
# i_3d : Granularity = '3d'
# i_1w : Granularity = '1w'
# i_2w : Granularity = '2w'
# i_1mo : Granularity = '1mo'
# i_3mo : Granularity = '3mo'
# i_6mo : Granularity = '6mo'
# i_1y : Granularity = '1y'
#
# IntervalsCache = Dict[Granularity, GranularityCache]
#
# class Trade(NamedTuple):
#     feed: str                           # 'BITMEX'
#     pair: str                           # 'XBTUSD'
#     timestamp: Timestamp_float          # 1586722261.612
#     receipt_timestamp: Timestamp_float  # 1586722261.648669
#     side: str                           # 'sell'
#     amount: float                       # 2.0
#     price: float                        # 7158.0
#     id: str                             # '72e3cf51-8d47-4f81-8828-8da727eec651'
#
# granularities = [i_1s, i_5s, i_10s, i_30s, i_1mi, i_2mi, i_5mi, i_10mi, i_15mi, i_30mi, i_1h, i_2h, i_4h, i_12h, i_1d,
#     i_3d, i_1w, i_2w, i_1mo, i_3mo, i_6mo, i_1y]
#
# """
# Returns the granularity used to compute another granularity. This is not always the previous granularity. For example,
# 5mi is computed from 1mi, not from 2mi. Or 1mo is computed from 1d, not from 2w.
# """
#
# granularity_for_compute = {
#     i_1s: None,
#     i_5s: i_1s,
#     i_10s: i_5s,
#     i_30s: i_10s,
#     i_1mi: i_30s,
#     i_2mi: i_1mi,
#     i_5mi: i_1mi,
#     i_10mi: i_5mi,
#     i_15mi: i_5mi,
#     i_30mi: i_15mi,
#     i_1h: i_30mi,
#     i_2h: i_1h,
#     i_4h: i_2h,
#     i_12h: i_4h,
#     i_1d: i_12h,
#     i_3d: i_1d,
#     i_1w: i_1d,
#     i_2w: i_1w,
#     i_1mo: i_1d,
#     i_3mo: i_1mo,
#     i_6mo: i_3mo,
#     i_1y: i_6mo,
# }
#
# def compute_dependencies():
#     ret = {}
#     for key, val in granularity_for_compute.items():
#         if val is not None:
#             dependencies_for_key = ret.get(val, [])
#             dependencies_for_key.append(key)
#             ret[val] = dependencies_for_key
#     return ret
#
# dependencies = compute_dependencies()
#
# def ts_floor_ceil(timestamp: Timestamp_float, divider: int) -> (Timestamp_float, Timestamp_float):
#     start = (timestamp // divider) * divider
#     return start, start + divider
#
# def get_interval_heads(granularity: Granularity, timestamp: Timestamp_float) -> (Timestamp_float, Timestamp_float):
#     if granularity == i_1s:
#         return ts_floor_ceil(timestamp, 1)
#     if granularity == i_5s:
#         return ts_floor_ceil(timestamp, 5)
#     if granularity == i_10s:
#         return ts_floor_ceil(timestamp, 10)
#     if granularity == i_30s:
#         return ts_floor_ceil(timestamp, 30)
#     if granularity == i_1mi:
#         return ts_floor_ceil(timestamp, 60)
#     if granularity == i_2mi:
#         return ts_floor_ceil(timestamp, 120)
#     if granularity == i_5mi:
#         return ts_floor_ceil(timestamp, 300)
#     if granularity == i_10mi:
#         return ts_floor_ceil(timestamp, 600)
#     if granularity == i_15mi:
#         return ts_floor_ceil(timestamp, 900)
#     if granularity == i_30mi:
#         return ts_floor_ceil(timestamp, 1800)
#     if granularity == i_1h:
#         return ts_floor_ceil(timestamp, 3600)
#     if granularity == i_2h:
#         return  ts_floor_ceil(timestamp, 7200)
#     if granularity == i_4h:
#         return ts_floor_ceil(timestamp, 14400)
#     if granularity == i_12h:
#         return ts_floor_ceil(timestamp, 43200)
#     if granularity == i_1d:
#         return ts_floor_ceil(timestamp, SECONDS_IN_DAY)
#     if granularity == i_3d:
#         return ts_floor_ceil(timestamp, 3 * SECONDS_IN_DAY)
#     if granularity == i_1w:
#         dt = datetime.fromtimestamp(ts_floor_ceil(timestamp, SECONDS_IN_DAY)[0])
#         start = datetime.timestamp(dt - timedelta(days=dt.weekday()))
#         return start, start + SECONDS_IN_WEEK
#     if granularity == i_2w:
#         dt = datetime.fromtimestamp(ts_floor_ceil(timestamp, SECONDS_IN_DAY)[0])
#         start = datetime.timestamp(dt - timedelta(days=dt.weekday()))
#         if (start // SECONDS_IN_WEEK) % 2 == 1:
#             start = start - SECONDS_IN_WEEK
#         return start, start + 2 * SECONDS_IN_WEEK
#     if granularity == i_1mo:
#         dt = datetime.fromtimestamp(ts_floor_ceil(timestamp, 86400))
#         start = datetime.timestamp(dt.replace(day=1))
#         return start
#     if granularity == i_3mo:
#         dt = datetime.fromtimestamp(ts_floor_ceil(timestamp, 86400))
#         month = ((dt.month - 1) // 3) * 3 + 1
#         return datetime.timestamp(dt.replace(day=1, month=month))
#     if granularity == i_6mo:
#         dt = datetime.fromtimestamp(ts_floor_ceil(timestamp, 86400))
#         month = ((dt.month - 1) // 6) * 6 + 1
#         return datetime.timestamp(dt.replace(day=1, month=month))
#     if granularity == i_1y:
#         dt = datetime.fromtimestamp(ts_floor_ceil(timestamp, 86400))
#         return datetime.timestamp(dt.replace(day=1, month=1))
#
# def update_stats(cache: IntervalsCache, trade: Trade, is_first_run):
#     i = 0
#     first_granularity = granularities[i]
#     granularities_to_check = [granularities[i]]
#     granularity_cache = cache[first_granularity]
#     trade_interval_start, trade_interval_end = get_interval_heads(first_granularity, trade.timestamp)
#     if len(granularity_cache.items) > 0 and granularity_cache.items[-1].ts == trade_interval_start:
#         # this item is in the same bucket
#         update(granularity_cache, trade)
#     else:
#         if len(granularity_cache.items) > 0:
#
#         next_start = len(granularity_cache.items) > 0
#         while next_start < trade_interval_end:
#             if not is_first_run:
#                 add_to_updates_for_db(granularity_cache.items[-1])
#             granularity_cache.items.append(Stats(
#                 ts=interval_start,
#                 open=trade.price,
#                 high=trade.price,
#                 low=trade.price,
#                 close=trade.price,
#                 volume=trade.amount
#             ))
#             _, next_start = get_interval_heads(first_granularity, next_start)
#         granularities_to_check = dependencies[first_granularity]
#     i += 1
#
#     while i < len(granularities_to_check):
#         granularity = granularities_to_check[i]
#
#
#
#
#
#
#
#
#     if get_interval_start(trade.timestamp) == cache_first.items
#     while
#     granularity_cache = cache[granularity]
#     if len(granularity_cache.items) == 0:
#         granularity_cache.append(stats)
#
# class StatsUpdater:
#     intervals_cache: IntervalsCache
#
#     def __init__(self, intervals_cache=None):
#         if intervals_cache is None:
#             intervals_cache = {}
#         self.intervals_cache = intervals_cache
#
#     def get_stats_updates(self, trade: Trade):
#         first_stats = self.intervals_cache[granularities[0]]
#         if first_stats.items
#
#         if len(second_stats) == 0:
#             # this means it's the first pass
#             for step in Intervals._fields:
#                 self.past_intervals[step] = get_interval_head()
#
#             second_stats[-1].ts == int(trade.timestamp):
#
#             last_second_stats = second_stats[-1] if len(second_stats) > 0 else Stats(ts=)
#
#         if int(trade.timestamp) > self.past_intervals[Intervals.i_1s][-1].ts
#
#
#
#     """
#     store a dict:
#     {'1s': [{'ts': 1234567, 'open': 15, 'high': 15, 'low': 13, 'close': 13, 'volume': 2}]}]
#     1s, 5s, 30s, 5min
#
#     """
#
#     pass
