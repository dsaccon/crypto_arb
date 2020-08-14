from src.configs import currencies, exchanges


def is_pair_valid(pair):
    if ':' in pair:
        return False
    # if '-' in pair:
    #     for ccy in pair.split('-'):
    #         if ccy not in currencies:
    #             return False
    return True


s = ''
for exchange in exchanges:
    valid_pairs = [pair for pair in exchange[0] if is_pair_valid(pair)]
    trades = f"[{', '.join(valid_pairs)}]\n"
    s = s + f"{exchange[1]}:\n  trades: {trades}\n"

print(s)

"""
BINANCE_JERSEY = 'BINANCE_JERSEY'
BINANCE_FUTURES = 'BINANCE_FUTURES'
EXX = 'EXX'
FTX = 'FTX'
BITCOINCOM = 'BITCOINCOM'
"""