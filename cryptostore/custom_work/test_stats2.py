from unittest import TestCase

from cryptostore.custom_work.stats2 import ts_floor_ceil, months_floor_ceil, get_interval_heads, i_5mi, i_1h, i_1w, \
    i_2w, i_1mo, i_3mo, i_6mo, i_1y, Stats, compose_stats, i_1s, Trade, update_stats


class Test(TestCase):
    def test_add_months(self):
        self.assertEqual(ts_floor_ceil(1586801721.12, 2), (1586801720., 1586801722.))

    def test_months_floor_ceil(self):
        self.assertEqual(months_floor_ceil(1586801721.12, 2), (1583020800.0, 1588291200.0))

    def test_get_interval_heads(self):
        self.assertEqual(get_interval_heads(i_5mi, 1586801721.12), (1586801700., 1586802000.))
        self.assertEqual(get_interval_heads(i_1h, 1586801721.12), (1586800800., 1586804400.))
        self.assertEqual(get_interval_heads(i_1w, 1586801721.12), (1586736000., 1587340800.))
        self.assertEqual(get_interval_heads(i_2w, 1586801721.12), (1586131200., 1587340800.))
        self.assertEqual(get_interval_heads(i_2w, 1587340800.12), (1587340800., 1588550400.))
        self.assertEqual(get_interval_heads(i_1mo, 1587340800.12), (1585699200., 1588291200.))
        self.assertEqual(get_interval_heads(i_3mo, 1587340800.12), (1585699200., 1593561600.))
        self.assertEqual(get_interval_heads(i_6mo, 1587340800.12), (1577836800., 1593561600.))
        self.assertEqual(get_interval_heads(i_1y, 1587340800.12), (1577836800., 1609459200.))

    def test_compose_stats(self):
        stats1 = Stats(open=10., high=15., low=10., close=10.5, volume=1., ts=1, end_ts=2)
        stats2 = Stats(open=11., high=13., low=9., close=10., volume=1.5, ts=1, end_ts=2)

        self.assertEqual(
            compose_stats([stats1, stats2], 1., 2.),
            Stats(open=10., high=15., low=9., close=10., volume=2.5, ts=1., end_ts=2.)
        )

        self.assertEqual(compose_stats([None, stats1], stats1.ts, stats1.end_ts), stats1)

    def test_update_stats(self):
        ts = 1586722261.612
        trade1 = Trade(
            feed='BITMEX',
            pair='XBTUSD',
            timestamp=ts,
            receipt_timestamp=1586722261.648669,
            side='sell',
            amount=2.0,
            price=7158.0,
            id='72e3cf51-8d47-4f81-8828-8da727eec651',
        )
        stats_to_write, cache = update_stats({}, trade1, [])
        self.assertEqual(stats_to_write[0], [])
        self.assertEqual(
            cache['10mi'],
            Stats(ts=1586722200.0, end_ts=1586722800.0, open=7158.0, high=7158.0, low=7158.0, close=7158.0, volume=2.0),
        )

        # add another trade two seconds later
        trade2 = Trade(
            feed='BITMEX',
            pair='XBTUSD',
            timestamp=ts+2,
            receipt_timestamp=1586722261.648669,
            side='sell',
            amount=1.0,
            price=715.0,
            id='72e3cf51-8d47-4f81-8828-8da727eec651',
        )
        stats_to_write, cache = update_stats(cache, trade2, [])
        self.assertEqual(
            stats_to_write[0],
            [Stats(ts=1586722261.0, end_ts=1586722262.0, open=7158.0, high=7158.0, low=7158.0, close=7158., volume=2.)],
        )
        self.assertEqual(
            cache['10mi'],
            Stats(ts=1586722200.0, end_ts=1586722800.0, open=7158.0, high=7158.0, low=715.0, close=715.0, volume=3.0),
        )
        self.assertEqual(
            cache['1s'],
            Stats(ts=1586722263.0, end_ts=1586722264.0, open=715.0, high=715.0, low=715.0, close=715.0, volume=1.0),
        )

        # add another trade during the same second
        trade3 = Trade(
            feed='BITMEX',
            pair='XBTUSD',
            timestamp=ts + 2.01,
            receipt_timestamp=1586722261.648669,
            side='sell',
            amount=1.0,
            price=715.0,
            id='72e3cf51-8d47-4f81-8828-8da727eec651',
        )
        stats_to_write, cache = update_stats(cache, trade3, [])
        self.assertEqual(
            stats_to_write[0],
            [],
        )
        self.assertEqual(
            cache['1s'],
            Stats(ts=1586722263.0, end_ts=1586722264.0, open=715.0, high=715.0, low=715.0, close=715.0, volume=2.0),
        )
