'''
Copyright (C) 2018-2020  Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
import asyncio
from multiprocessing import Process
import time
import logging
import os
from datetime import timedelta

TRADES = 'trades'
STATS = 'stats'

from cryptostore.custom_work.stats2 import init_cache, update_stats, InfluxConfig, Trade
from cryptostore.custom_work import arb
from cryptostore.util import get_time_interval
from cryptostore.aggregator.redis import Redis
from cryptostore.aggregator.kafka import Kafka
from cryptostore.data.storage import Storage
from cryptostore.config import DynamicConfig
from webserver.src.async_mysql import MySQLClient

LOG = logging.getLogger('cryptostore')


class Aggregator(Process):
    def __init__(self, config_file=None):
        self.config_file = config_file
        super().__init__()
        self.daemon = True
        self.mysql_client = None
        self.last_arb_id = None

    def run(self):
        LOG.info("Aggregator running on PID %d", os.getpid())
        loop = asyncio.get_event_loop()
        self.config = DynamicConfig(file_name=self.config_file)
        self.mysql_client = MySQLClient(loop)
        _last_arb_id = loop.run_until_complete(self.mysql_client.get_last_arb_id())
        if not _last_arb_id == None:
            self.last_arb_id = int(_last_arb_id[0])
        else:
            self.last_arb_id = 0
        loop.create_task(self.loop())
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        except Exception:
            LOG.error("Aggregator running on PID %d died due to exception", os.getpid(), exc_info=True)

    async def write_arbs(self, data):
        arbs, self.last_arb_id = arb.get_arbs(data, self.last_arb_id)
        mysql_task = [self.mysql_client.insert_dicts('Arb', arbs)]
        await asyncio.gather(*mysql_task)

    def collect_stats(self, data, exchange, pair, stats_cache):
        LOG.info('HAVING trades')
        stats_to_write = []
        for trade in data:
            if 'id' not in trade:
                trade['id'] = None
            typed_trade = Trade(**trade)
            update_stats(stats_cache[exchange][pair], typed_trade, stats_to_write)
        LOG.info('DONE computing stats for %s-%s', exchange, pair)
        return stats_to_write
#        self.store.aggregate(stats_to_write)
#        store.write(exchange, STATS, pair, time.time())

    async def loop(self):
        if self.config.cache == 'redis':
            cache = Redis(ip=self.config.redis['ip'],
                          port=self.config.redis['port'],
                          socket=self.config.redis.socket,
                          del_after_read=self.config.redis['del_after_read'],
                          flush=self.config.redis['start_flush'],
                          retention=self.config.redis.retention_time if 'retention_time' in self.config.redis else None)
        elif self.config.cache == 'kafka':
            cache = Kafka(self.config.kafka['ip'],
                          self.config.kafka['port'],
                          flush=self.config.kafka['start_flush'])
        self.store = Storage(self.config) ### tmp

        interval = self.config.storage_interval
        time_partition = False
        multiplier = 1
        if not isinstance(interval, int):
            if len(interval) > 1:
                multiplier = int(interval[:-1])
                interval = interval[-1]
            base_interval = interval
            if interval in {'M', 'H', 'D'}:
                time_partition = True
                if interval == 'M':
                    interval = 60 * multiplier
                elif interval == 'H':
                    interval = 3600 * multiplier
                else:
                    interval = 86400 * multiplier

        stats_cache = {}
        for exchange in self.config.exchanges:
            stats_cache[exchange] = {}
            for pair in self.config.exchanges[exchange][TRADES]:
                stats_cache[exchange][pair] = init_cache(InfluxConfig(
                    db='crypto',
                    host='http://localhost:8086',
                    exchange=exchange,
                    pair=pair,
                ))

        while True:
            start, end = None, None
            try:
                aggregation_start = time.time()
                if time_partition:
                    interval_start = aggregation_start
                    if end:
                        interval_start = end + timedelta(seconds=interval + 1)
                    start, end = get_time_interval(interval_start, base_interval, multiplier=multiplier)
                if 'exchanges' in self.config and self.config.exchanges:
                    data_arb = {}
                    for exchange in self.config.exchanges:
                        stats_all = [] ### Stats from each loop iter stored here
                        data_all = [] ### Data... ""
                        data_arb[exchange] = {}
                        for dtype in self.config.exchanges[exchange]:
                            # Skip over the retries arg in the config if present.
                            if dtype in {'retries', 'channel_timeouts'}:
                                continue
#                            for pair in self.config.exchanges[exchange][dtype] if 'symbols' not in \
#                                                                                  self.config.exchanges[exchange][
#                                                                                      dtype] else \
#                                    self.config.exchanges[exchange][dtype]['symbols']:
                            for pair in self.config.exchanges[exchange][dtype]: ### tmp
#                                store = Storage(self.config)
                                LOG.info('Reading %s-%s-%s', exchange, dtype, pair)
                                data = cache.read(exchange, dtype, pair, start=start, end=end)
                                data_all.append(data)
                                data_arb[exchange][pair] = data
                                if len(data) == 0:
                                    LOG.info('No data for %s-%s-%s', exchange, dtype, pair)
                                    continue
                                #
                                if dtype == TRADES:
                                    stats_all.append(self.collect_stats(data, exchange, pair, stats_cache))
#                                    LOG.info('HAVING trades')
#                                    stats_to_write = []
#                                    for trade in data:
#                                        if 'id' not in trade:
#                                            trade['id'] = None
#                                        typed_trade = Trade(**trade)
#                                        update_stats(stats_cache[exchange][pair], typed_trade, stats_to_write)
#                                    LOG.info('DONE computing stats for %s-%s', exchange, pair)
#                                    store.aggregate(stats_to_write)
#                                    store.write(exchange, STATS, pair, time.time())
                                #
#                                self.store.aggregate(data)
#                                self.store.write(exchange, dtype, pair, time.time())

                                cache.delete(exchange, dtype, pair)
#                                LOG.info('Write Complete %s-%s-%s', exchange, dtype, pair)
                    #
                    self.store.aggregate(stats_all)
                    self.store.write(exchange, STATS, pair, time.time())
                    if any(data_all):
                        self.store.aggregate(data_all)
                        self.store.write(exchange, dtype, pair, time.time())
                    if data_arb:
                        await self.write_arbs(data_arb)
                    #
                    total = time.time() - aggregation_start
                    wait = interval - total
                    if wait <= 0:
                        LOG.warning("Storage operations currently take %.1f seconds, longer than the interval of %d",
                                    total, interval)
                        wait = 0.5
                    else:
                        LOG.warning(f"Storage operations took {total}s, interval {interval}s")
                    await asyncio.sleep(wait)
                else:
                    await asyncio.sleep(30)
            except Exception:
                LOG.error("Aggregator running on PID %d died due to exception", os.getpid(), exc_info=True)
                raise
