import json
import time
import sortedcontainers
import itertools
from operator import itemgetter

with open('data_arb.json', 'r') as f:
    data = json.loads(f.read())

#print(json.dumps(data, indent=4))

def prep_arb(data):
    t = time.time()
    data_arb = {
        e:{
            p:{
                'b': sorted([t for t in data[e][p] if t['side'] == 'buy'], key=itemgetter('price'), reverse=True),
                'a': sorted([t for t in data[e][p] if t['side'] == 'sell'], key=itemgetter('price'))
            }
        for p in data[e] if data[e][p]
        }
        for e in data
    }

    return data_arb

def calc_arbs(data):
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
    for ((ex_p, p) for ex_p in arb_opps for p in ex_p):
        # Filter any 
        num_uniq_b = len({_p['price'] for _p in data[ex_p.split('/', 0)][p]['b']})
        num_uniq_a = len({_p['price'] for _p in data[ex_p.split('/', 0)][p]['a']})
        if not num_uniq_b == len(data[ex_p.split('/', 0)][p]['b']):
            # Combine vols here
            new_trades = [data[ex_p.split('/', 0)][p]['b'][0]]
            # ...more logic
        if not num_uniq_a == len(data[ex_p.split('/', 0)][p]['a']):
            # Combine vols here
            new_trades = [data[ex_p.split('/', 0)][p]['a'][0]]
            # ...more logic
        #
        num_uniq_b = len({_p['price'] for _p in data[ex_p.split('/', 1)][p]['b']})
        num_uniq_a = len({_p['price'] for _p in data[ex_p.split('/', 1)][p]['a']})
        if not num_uniq_b == len(data[ex_p.split('/', 1)][p]['b']):
            # Combine vols here
            new_trades = [data[ex_p.split('/', 1)][p]['b'][0]]
            # ...more logic
        if not num_uniq_a == len(data[ex_p.split('/', 1)][p]['a']):
            # Combine vols here
            new_trades = [data[ex_p.split('/', 1)][p]['a'][0]]
            # ...more logic
             
    return arb_opps

print(json.dumps(calc_arbs(prep_arb(data)), indent=4))
quit()
print('')
print(list(calc_arbs(prep_arb(data)))[0])
#print(len(list(calc_arbs(prep_arb(data)))))
