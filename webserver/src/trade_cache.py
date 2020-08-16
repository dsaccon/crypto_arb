import requests
import threading
import time
from cryptostore.aggregator.redis import Redis

from cryptostore.custom_work.stats2 import granularities
from webserver.src.configs import host, db, exchange_names, redis_host, get_currencies_in_pair, get_pair_from_currencies

NOW = 'now'

redis = Redis(
    ip=redis_host,
    port=6379,
    del_after_read=False,
)


def get_last_price_from_redis(exchange: str, ccy1: str, ccy2: str):
    pair = get_pair_from_currencies(exchange, ccy1, ccy2)
    data = redis.read_last(exchange, 'trades', pair)
    if len(data) == 0:
        return None
    return float(data[0][1]['price']), data[0][1]['timestamp']


def get_exchange_currencies(prices_cache):
    exchange_currencies = {}
    for exchange in prices_cache:
        currencies = set()
        for currency1 in prices_cache[exchange]:
            currencies.add(currency1)
            for currency2 in prices_cache[exchange][currency1]:
                currencies.add(currency2)
        exchange_currencies[exchange] = currencies
    return exchange_currencies


def get_all_currencies(prices_cache):
    currencies = set()
    for exchange in prices_cache:
        for currency1 in prices_cache[exchange]:
            currencies.add(currency1)
            for currency2 in prices_cache[exchange][currency1]:
                currencies.add(currency2)
    return currencies


def get_price(prices_cache, exchange_currencies, exchange, currency1, currency2, granularity):
    if exchange in exchange_currencies:
        if granularity == NOW:
            # if the currency pair exists in the cache, then try to get its last value from redis
            pair_data = prices_cache[exchange].get(currency1, {}).get(currency2, {})
            if pair_data:
                if pair_data.get(NOW, {}).get('ts', 0) > time.time() - 1:
                    return pair_data.get(NOW)['price']
                redis_data = get_last_price_from_redis(exchange, currency1, currency2)
                if redis_data:
                    price = redis_data[0]
                    prices_cache[exchange][currency1][currency2][NOW] = {
                        'price': price,
                        'ts': time.time(),
                    }
                    return price
                else:
                    return prices_cache[exchange][currency1][currency2]['1s']

            # try the reversed currency pair
            pair_data = prices_cache[exchange].get(currency2, {}).get(currency1, {})
            if pair_data:
                if pair_data.get(NOW, {}).get('ts', 0) > time.time() - 1:
                    return 1 / pair_data.get(NOW)['price']
                redis_data = get_last_price_from_redis(exchange, currency2, currency1)
                if redis_data:
                    price = redis_data[0]
                    prices_cache[exchange][currency2][currency1][NOW] = {
                        'price': price,
                        'ts': time.time(),
                    }
                    return 1 / price
                else:
                    return 1 / prices_cache[exchange][currency2][currency1]['1s']
        else:
            currencies = exchange_currencies[exchange]
            if currency1 not in currencies or currency2 not in currencies:
                return None
            if currency2 in prices_cache[exchange].get(currency1, {}):
                price = prices_cache[exchange][currency1][currency2].get(granularity)
                if price is not None:
                    return price
            if currency1 in prices_cache[exchange].get(currency2, {}):
                price = prices_cache[exchange][currency2][currency1].get(granularity)
                if price is not None:
                    return 1 / price
            else:
                for ccy in prices_cache[exchange].get(currency1, {}):
                    if ccy in prices_cache[exchange].get(currency2, {}):
                        cross1 = prices_cache[exchange][currency1][ccy].get(granularity)
                        cross2 = prices_cache[exchange][currency2][ccy].get(granularity)
                        if cross1 is not None and cross2 is not None:
                            return cross1 / cross2

    return None


def get_average_price(prices_cache, exchange_currencies, exchanges, currency1, currency2, granularity):
    prices = [
        get_price(prices_cache, exchange_currencies, exchange, currency1, currency2, granularity)
        for exchange in exchanges
    ]
    prices = [price for price in prices if price is not None]
    if len(prices) > 0:
        return sum(prices) / len(prices)
    return None


def get_price_changes(prices_cache, exchanges, price_currency, granularities):
    ret = {}
    all_currencies = get_all_currencies(prices_cache)
    exchange_currencies = get_exchange_currencies(prices_cache)
    for currency in all_currencies:
        if currency != price_currency:
            current_price = get_average_price(
                prices_cache, exchange_currencies, exchanges, currency, price_currency, NOW
            )
            if current_price:
                if not ret.get(currency):
                    ret[currency] = {}
                ret[currency][NOW] = current_price
                for granularity in granularities:
                    previous_price = get_average_price(
                        prices_cache, exchange_currencies, exchanges, currency, price_currency, granularity,
                    )
                    if previous_price:
                        ret[currency][granularity] = (current_price / previous_price) - 1
    return ret


def get_volume_changes(volume_cache, exchanges, price_currency, granularities):
    ret = {}
    for exchange in exchanges:
        for currency2 in volume_cache[exchange].get(price_currency, {}):
            volumes = volume_cache[exchange][price_currency][currency2]
            for granularity in granularities:
                if volumes.get(granularity):
                    last_volume, before_volume = volumes[granularity]
                    if before_volume and last_volume:
                        if ret.get(currency2) is None:
                            ret[currency2] = {}
                        ret[currency2][granularity] = last_volume / before_volume
        for currency1 in volume_cache[exchange]:
            volumes = volume_cache[exchange][currency1].get(price_currency)
            if volumes is not None:
                for granularity in granularities:
                    last_volume, before_volume = volumes[granularity]
                    if before_volume and last_volume:
                        if ret.get(currency1) is None:
                            ret[currency1] = {}
                        ret[currency1][granularity] = last_volume / before_volume
    return ret


def get_volume_change(volumes_cache, exchanges, coin, price_currency, granularity):
    volume_changes = []
    for exchange in exchanges:
        volumes_normal = volumes_cache.get(exchange, {}).get(coin, {}).get(price_currency, {}).get(granularity)
        volumes_reverse = volumes_cache.get(exchange, {}).get(price_currency, {}).get(coin, {}).get(granularity)
        for volumes in [volumes_normal, volumes_reverse]:
            if volumes is not None:
                if len(volumes) < 2:
                    volume_changes.append(1)
                elif volumes[0] == 0:
                    volume_changes.append(0)
                else:
                    volume_changes.append(volumes[1] / volumes[0] - 1)
    return sum(volume_changes) / len(volume_changes) if len(volume_changes) > 0 else 0


global_prices_cache = {}
global_volumes_cache = {}


def get_interval_delta(granularity):
    if granularity == '1s':
        return 1
    if granularity == '5s':
        return 5
    if granularity == '10s':
        return 10
    if granularity == '30s':
        return 30
    if granularity == '1mi':
        return 60
    if granularity == '2mi':
        return 120
    if granularity == '5mi':
        return 300
    if granularity == '10mi':
        return 600
    if granularity == '15mi':
        return 900
    if granularity == '30mi':
        return 1800
    if granularity == '1h':
        return 3600
    if granularity == '2h':
        return 7200
    if granularity == '4h':
        return 14400
    if granularity == '12h':
        return 43200
    if granularity == '1d':
        return 86400
    if granularity == '3d':
        return 259200
    if granularity == '1w':
        return 604800
    if granularity == '2w':
        return 1209600
    if granularity == '1mo':
        return 2592000
    if granularity == '3mo':
        return 7776000
    if granularity == '6mo':
        return 15552000
    if granularity == '1y':
        return 31104000


def fill_trade_cache(prices_cache, timestamp):
    for granularity in granularities:
        for exchange in exchange_names:
            # try:
            r = requests.get(
                f"{host}/query?db={db}",
                params={
                    'q': f'SELECT LAST(price) from "crypto"."autogen"."trades-{exchange}" '
                         f'WHERE time < {int((timestamp - get_interval_delta(granularity)) * 1_000_000_000)} '
                         f'GROUP BY pair '
                }
            )
            r_json = r.json()

            for pair_data in r_json['results'][0].get('series', []):
                pair = pair_data['tags']['pair']
                (currency1, currency2) = get_currencies_in_pair(pair)
                if prices_cache.get(exchange) is None:
                    prices_cache[exchange] = {}
                if prices_cache[exchange].get(currency1) is None:
                    prices_cache[exchange][currency1] = {}
                if prices_cache[exchange][currency1].get(currency2) is None:
                    prices_cache[exchange][currency1][currency2] = {}
                prices_cache[exchange][currency1][currency2][granularity] = pair_data['values'][0][1]

        # except Exception as e:
        #     return None


def fill_volume_cache(cache):
    for exchange in exchange_names:
        if cache.get(exchange) is None:
            cache[exchange] = {}
            # try:
            r = requests.get(
                f"{host}/query?db={db}",
                params={
                    'q': f'SELECT volume from "crypto"."autogen"."stats-{exchange}" '
                         f'GROUP BY pair, granularity '
                         f'ORDER BY time desc '
                         f'limit 2'
                }
            )
            r_json = r.json()
            if 'series' in r_json['results'][0]:
                for volume_data in r_json['results'][0]['series']:
                    pair = volume_data['tags']['pair']
                    (currency1, currency2) = get_currencies_in_pair(pair)
                    granularity = volume_data['tags']['granularity']
                    if cache[exchange].get(currency1) is None:
                        cache[exchange][currency1] = {}
                    if cache[exchange][currency1].get(currency2) is None:
                        cache[exchange][currency1][currency2] = {}
                    if cache[exchange][currency1][currency2].get(granularity) is None:
                        cache[exchange][currency1][currency2][granularity] = []
                    data = cache[exchange][currency1][currency2][granularity] + volume_data['values']
                    data = sorted(data, key=lambda x: x[0])
                    data = [x[1] for x in data]
                    cache[exchange][currency1][currency2][granularity] = data


def fill_trade_cache_starter():
    prices_cache = get_prices_cache()
    volumes_cache = get_volumes_cache()

    while True:
        timestamp = time.time()
        fill_trade_cache(prices_cache, timestamp)
        print('done reloading trade cache')
        fill_volume_cache(volumes_cache)
        print('done reloading volume cache')
        time.sleep(10)


def get_prices_cache():
    return global_prices_cache


def get_volumes_cache():
    return global_volumes_cache


def start_fill_trade_cache_thread():
    x = threading.Thread(target=fill_trade_cache_starter)
    x.start()
