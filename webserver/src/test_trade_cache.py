import time
from unittest import TestCase

from src.trade_cache import get_price_changes, NOW, get_volume_changes, fill_trade_cache
from src.configs import get_currencies_in_pair


class Test(TestCase):
    def test_get_price_changes(self):
        prices_cache = {
            'COINBASE': {
                'BTC': {
                    'USD': {
                        '1y': 6000,
                        NOW: 7000,
                    }
                }
            },
            'KRAKEN': {
                'BTC': {
                    'USD': {
                        '1y': 6500,
                        NOW: 7500,
                    }
                }
            }
        }
        self.assertEqual(
            get_price_changes(prices_cache, ['COINBASE'], 'USD', ['1y']),
            {'BTC': {'1y': 0.16666666666666674}}
        )
        self.assertEqual(
            get_price_changes(prices_cache, ['COINBASE', 'KRAKEN'], 'USD', ['1y']),
            {'BTC': {'1y': 0.15999999999999992}}
        )
        self.assertEqual(
            get_price_changes(prices_cache, ['KRAKEN'], 'BTC', ['1y']),
            {'USD': {'1y': -0.1333333333333333}}
        )

    def test_get_volume_changes(self):
        volume_cache = {
            'COINBASE': {
                'BTC': {
                    'USD': {
                        '1h': (5, 10)
                    }
                }
            }
        }
        self.assertEqual(get_volume_changes(volume_cache, ['COINBASE'], 'BTC', ['1h']), {'USD': {'1h': 0.5}})
        self.assertEqual(get_volume_changes(volume_cache, ['COINBASE'], 'USD', ['1h']), {'BTC': {'1h': 0.5}})
        self.assertEqual(get_volume_changes(volume_cache, ['COINBASE'], 'BTC', ['1mi']), {})

    def test_fill_trade_cache(self):
        cache = {}
        x = time.time()
        fill_trade_cache(cache, 1587075761)
        print('took')
        print(time.time() - x)
        self.assertFalse(cache is None)

    def test_get_currencies_in_pair(self):
        self.assertEqual(get_currencies_in_pair('BTC-USD'), ('BTC', 'USD'))
        self.assertEqual(get_currencies_in_pair('BTC-PERPETUAL'), ('BTC', 'USD'))
        self.assertEqual(get_currencies_in_pair('XBTUSD'), ('BTC', 'USD'))
