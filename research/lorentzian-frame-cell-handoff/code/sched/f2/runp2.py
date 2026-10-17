import json, time
from feasp2 import feasible_p2
res = json.load(open('seqprice_K4.json'))
n = 0; t = time.time(); feas = []
for pct, sl, seqs in res:
    if pct <= 0: break
    for q in seqs:
        n += 1
        if feasible_p2(q, 2):
            feas.append((pct, q)); print('F2-FEASIBLE %+.3f%%' % pct, sl, q, flush=True)
    print('# multiset', sl, '%+.2f%%' % pct, 'checked', n, '%.0fs' % (time.time() - t), flush=True)
print('DONE positive-price sequences', n, 'F2-feasible', len(feas), flush=True)
