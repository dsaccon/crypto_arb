import json
import time
import sortedcontainers
import itertools
import copy
from operator import itemgetter

def create_arb_dict(data):
    # Construct dictionary to organize data out of raw trades
    # Output to be fed into calc_arbs
    t = time.time()
    data_arb = {
        e:{
            p:{
                'b': sorted(
                    [t for t in data[e][p] if t['side'] == 'buy'],
                    key=itemgetter('price'), reverse=True),
                'a': sorted(
                    [t for t in data[e][p] if t['side'] == 'sell'],
                    key=itemgetter('price'))
            }
        for p in data[e] if data[e][p]
        }
        for e in data
    }

    return data_arb

def combine_vols(data):
    # Utility used by calc_arbs
    # Aggregate like-price trades into one with combined vol
    new_trades = [data[0]]
    if len(data) > 1:
        for tr in data[1:]:
            if new_trades[-1]['price'] == tr['price']:
                new_trades[-1]['amount'] += tr['amount']
            else:
                new_trades.append(tr)
    return new_trades

def filter_arb_opps(data):
    exch_pairs = itertools.combinations(data.keys(), 2)

    # Construct dictionary of arb opportunity candidates
    #
    #     "EXCH_1/EXCH_2": {
    #         "BASE-QUOTE": {
    #            "u": {}
    #         }
    #     },
    #     "EXCH_3/EXCH_4": {
    #         "BASE-QUOTE": {
    #            "d": {}
    #         }
    #     },
    #     ...
    arb_opps = {}
    for ex_p in exch_pairs:
        _ex_p = ex_p[0] + '/' + ex_p[1]
        arb_opps[_ex_p] = {}
        for p in set(data[ex_p[0]].keys()) & set(data[ex_p[1]].keys()):
            # Get common pairs between 2 exchs
            if data[ex_p[0]][p]['b'] and data[ex_p[1]][p]['a']:
                if data[ex_p[0]][p]['b'][0]['price'] < data[ex_p[1]][p]['a'][0]['price']:
                    arb_opps[_ex_p][p] = {'u': {}}
            if data[ex_p[1]][p]['b'] and data[ex_p[0]][p]['a']:
                if data[ex_p[1]][p]['b'][0]['price'] < data[ex_p[0]][p]['a'][0]['price']:
                    arb_opps[_ex_p][p] = {'d': {}}

    # Combine vols of equal price levels in data
    for (ex_p, p) in ((_ex_p, _p) for _ex_p in arb_opps for _p in arb_opps[_ex_p]):
        ex_p_0 = ex_p.split('/')[0]
        ex_p_1 = ex_p.split('/')[1]
        num_uniq_b = len({_p['price'] for _p in data[ex_p_0][p]['b']})
        num_uniq_a = len({_p['price'] for _p in data[ex_p_0][p]['a']})
        if not num_uniq_b == len(data[ex_p_0][p]['b']):
            data[ex_p_0][p]['b'] = combine_vols(data[ex_p_0][p]['b'])
        if not num_uniq_a == len(data[ex_p_0][p]['a']):
            data[ex_p_0][p]['a'] = combine_vols(data[ex_p_0][p]['a'])
        #
        num_uniq_b = len({_p['price'] for _p in data[ex_p_1][p]['b']})
        num_uniq_a = len({_p['price'] for _p in data[ex_p_1][p]['a']})
        if not num_uniq_b == len(data[ex_p_1][p]['b']):
            data[ex_p_1][p]['b'] = combine_vols(data[ex_p_1][p]['b'])
        if not num_uniq_a == len(data[ex_p_1][p]['a']):
            data[ex_p_1][p]['a'] = combine_vols(data[ex_p_1][p]['a'])
    return arb_opps, data

def calc_arbs(arb_opps, data, target, mode='arb_vol'):
    arbs = copy.deepcopy(arb_opps)
    for ex_p in arb_opps:
        ex_p_0 = ex_p.split('/')[0]
        ex_p_1 = ex_p.split('/')[1]
        for p in arb_opps[ex_p]:
            if 'u' in arb_opps[ex_p][p]:
                # Calc arb for ex_p_0 -> ex_p_1 dir
                data_0 = data[ex_p_0][p]['b'][0]
                data_1 = data[ex_p_1][p]['a'][0]
                _arb = 100*(data_1['price']/data_0['price'] - 1)
                if _arb > target:
                    arbs[ex_p][p] = {
                        'arb_yld': _arb,
                        'vol': min(
                            data_0['amount'],
                            data_1['amount']),
                        'dir': 'UP',
                    }
            elif 'd' in arb_opps[ex_p][p]:
                # Calc arb for ex_p_1 -> ex_p_0 dir
                data_0 = data[ex_p_0][p]['a'][0]
                data_1 = data[ex_p_1][p]['b'][0]
                _arb = 100*(data_0['price']/data_1['price'] - 1)
                if _arb > target:
                    arbs[ex_p][p] = {
                        'arb_yld': _arb,
                        'vol': min(
                            data_0['amount'],
                            data_1['amount']),
                        'dir': 'DOWN',
                    }
    return arbs

def get_arbs(data):
    arb_opps, new_data = filter_arb_opps(create_arb_dict(data))
    arbs = calc_arbs(arb_opps, new_data, 0.2, mode='arb_vol')
    arbs = {
        ex_p:{
            _p:arbs[ex_p][_p] for _p,a in p.items()
            if not ('u' in a or 'd' in a)
        }
        for ex_p,p in arbs.items()
    }
    arbs = {ex_p:p for ex_p,p in arbs.items() if p}
    return arbs

if __name__ == '__main__':
    with open('data_arb_test.json', 'r') as f:
        data = json.loads(f.read())
    arbs = get_arbs(data)
    print(json.dumps(arbs, indent=4))
