import tornado.ioloop
import tornado.web

from webserver.src import trades, dashboard, arbs
from webserver.src.trade_cache import start_fill_trade_cache_thread

start_fill_trade_cache_thread()


def make_app():
    return tornado.web.Application([
        (r"/trades", trades.TradesHandler),
        (r"/dashboard", dashboard.DashboardHandler),
        (r"/arb", arbs.ArbHandler),
        (r"/arbs", arbs.ArbsHandler),
    ])

if __name__ == "__main__":
    print('started web server')
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
