from datetime import datetime
import json

import requests
import tornado.web
import pymysql

from webserver.src.configs import host, db, exchanges, get_currencies_in_pair


def get_arbs(
        allowed_exchanges, currencies1, currencies2, from_ts=None, to_ts=None, limit=10, min_price=None,
        max_price=None, min_amount=None, max_amount=None, side=None,
):
    trades_ret = []
    for exchange_name in allowed_exchanges:
        pairs = []
        exchange_pairs = [exchange_data[0] for exchange_data in exchanges if exchange_name == exchange_data[1]][0]
        for pair in exchange_pairs:
            ccy1, ccy2 = get_currencies_in_pair(pair)
            if (len(currencies1) == 0 or ccy1 in currencies1) and (len(currencies2) == 0 or ccy2 in currencies2):
                pairs.append(pair)
        if len(pairs) == 0:
            continue

        pair_filters = " or ".join([f"pair='{pair}'" for pair in pairs])

        filters = [
            [from_ts, from_ts and f'time >= {int(from_ts * 1_000_000_000)}'],
            [to_ts, to_ts and f'time < {int(to_ts * 1_000_000_000)}'],
            [pair_filters, pair_filters],
            [min_price, min_price and f'price >= {min_price}'],
            [max_price, max_price and f'price <= {max_price}'],
            [min_amount, min_amount and f'amount >= {min_amount}'],
            [max_amount, max_amount and f'amount <= {max_amount}'],
            [side == 'buy' or side == 'sell', f'side =  \'{side}\''],
        ]
        filter_str = ' and '.join([f[1] for f in filters if f[0]])

        r = requests.get(
            f"{host}/query?db={db}",
            params={
                'q': f'SELECT * from "crypto"."autogen"."trades-{exchange_name}" '
                     f'WHERE {filter_str} '
                     f'ORDER BY time DESC '
                     f'LIMIT {limit} '
            }
        )
        r_json = r.json()
        if 'series' not in r_json['results'][0]:
            continue
        trades = r_json['results'][0]['series'][0]['values']
        columns = r_json['results'][0]['series'][0]['columns']
        # COLUMNS ['time', 'amount', 'exchange', 'id', 'pair', 'price', 'receipt_timestamp', 'side', 'timestamp']
        columns_dict = {columns[i]: i for i in range(len(columns))}
        trades_ret = trades_ret + [{
            "timestamp": trade[columns_dict['timestamp']],
            "exchange": trade[columns_dict['exchange']],
            "pair": trade[columns_dict['pair']],
            "amount": trade[columns_dict['amount']],
            "price": trade[columns_dict['price']],
            "side": trade[columns_dict['side']],
        } for trade in trades]
    return sorted(trades_ret, key=lambda x: -x['timestamp'])

def get_latest_arbs(period=10):
    mysql_client = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='crypto',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    query = f'SELECT * FROM Arb WHERE FROM_UNIXTIME( timestamp ) > date_sub(now(), interval {period} second)'
    try:
        with mysql_client.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    finally:
        mysql_client.close()
    return result

class ArbHandler(tornado.web.RequestHandler):
    def post(self):
        json_body = tornado.escape.json_decode(self.request.body)
        arbs = get_latest_arbs()
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.write(json.dumps(arbs))

    def options(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.write('')

class ArbsHandler(tornado.web.RequestHandler):
    def get(self):
        arbs = get_latest_arbs()
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.write(json.dumps(arbs, indent=4))

    def options(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.write('')
