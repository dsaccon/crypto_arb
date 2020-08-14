export const formatTimestamp = (ts: number) => {
    const dt = new Date(ts * 1000);
    return dt.toLocaleDateString() + ' ' + dt.toLocaleTimeString();
}

export const serverHost = 'http://3.84.167.34:8000/';

export const allExchanges = [
    'Spot AVG', 'Futures AVG',
    // 'BITFINEX',
    'BITMEX', 'BINANCE', 'BINANCE_US', 'BITSTAMP', 'BITTREX', 'BYBIT', 'COINBASE',
    // 'COINBENE',
    'DERIBIT',
    'GEMINI',
    'HITBTC', 'HUOBI',
    // 'KRAKEN',
    'OKCOIN', 'OKEX', 'POLONIEX', 'BITMAX', 'UPBIT',
];
