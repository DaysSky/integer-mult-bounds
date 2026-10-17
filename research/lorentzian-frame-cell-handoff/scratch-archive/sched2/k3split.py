import itertools, sys, time
sys.path.insert(0, '../k3')
import k3slots as KS
from splitp import run, slots
K = 3; s = 7
best = {}
t = time.time(); n = 0
for sq in itertools.product(range(K), repeat=s):
    firsts = []
    for x in sq:
        if x not in firsts: firsts.append(x)
    if firsts != list(range(K)): continue
    n += 1
    res = run(list(sq), 2)
    for sp in res:
        sl = slots(list(sq), sp)
        if sl not in best: best[sl] = (sq, sp)
rows = []
for sl, (sq, sp) in best.items():
    c, over = KS.price_slots(KS.tuned, 111, 8, 439, 7, 3, list(sl))
    rows.append((float((c / KS.ref - 1) * 100) if c else -999, sl, sq, sp))
rows.sort(reverse=True)
print('K=3 sequences', n, 'feasible slot multisets', len(rows), '%.0fs' % (time.time() - t))
for r in rows[:15]: print('%+.2f%%' % r[0], r[1], r[2], r[3])
