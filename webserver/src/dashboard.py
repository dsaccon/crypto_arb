import json

import tornado

from webserver.src.configs import spot_exchange_names, futures_exchange_names
from webserver.src.trade_cache import get_prices_cache, get_price_changes, NOW, \
    get_volumes_cache, get_volume_change


class DashboardHandler(tornado.web.RequestHandler):
    def post(self):
        json_body = tornado.escape.json_decode(self.request.body)
        exchanges = json_body.get('exchanges')
        if 'Spot AVG' in exchanges:
            exchanges.remove('Spot AVG')
            exchanges = exchanges + spot_exchange_names
            list(dict.fromkeys(exchanges)) # remove duplicates
        if 'Futures AVG' in exchanges:
            exchanges.remove('Futures AVG')
            exchanges = exchanges + futures_exchange_names
            list(dict.fromkeys(exchanges)) # remove duplicates
        price_currency = json_body.get('priceCurrency')
        visible_columns = json_body.get('visibleColumns')
        price_garnularities = [column.replace('price_', '') for column in visible_columns if 'price_' in column]
        volume_granularities = [column.replace('volume_', '') for column in visible_columns if 'volume_' in column]
        prices_cache = get_prices_cache()
        volumes_cache = get_volumes_cache()

        ret = []
        if prices_cache:
            price_changes = get_price_changes(prices_cache, exchanges, price_currency, price_garnularities)
            for coin in price_changes:
                price_changes_dict = {
                    'price_' + granularity: price_changes[coin][granularity]
                    for granularity in price_changes[coin] if granularity != NOW
                }
                price_changes_dict['coin'] = coin
                price_changes_dict['price'] = price_changes[coin][NOW]
                for granularity in volume_granularities:
                    price_changes_dict['volume_' + granularity] = \
                        get_volume_change(volumes_cache, exchanges, coin, price_currency, granularity)

                ret.append(price_changes_dict)

        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.write(json.dumps(ret))

    def options(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.write('')

