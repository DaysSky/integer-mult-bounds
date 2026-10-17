import json, sys, time
from feasp import feasible_p
p = int(sys.argv[1]); K = int(sys.argv[2])
res = json.load(open('seqprice_K%d.json' % K))
n = 0
for pct, sl, seqs in res:
    if pct <= float(sys.argv[3]): break
    for q in seqs:
        t = time.time()
        f = feasible_p(q, p)
        n += 1
        if f: print('%+.2f%%' % pct, sl, q, 'F%d-FEASIBLE' % p, f[0][0], '%.1fs' % (time.time() - t), flush=True)
    print('# done multiset', sl, '%+.2f%%' % pct, 'checked', n, flush=True)
