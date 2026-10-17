import itertools, sys
sys.path.insert(0, '../k3')
from k3slots import price_slots, slots_of, tuned, ref
from feasp import feasible_p
K = 3; s = 7
rows = []
for sq in itertools.product(range(K), repeat=s):
    firsts = []
    for p in sq:
        if p not in firsts: firsts.append(p)
    if firsts != list(range(K)): continue
    f = feasible_p(list(sq), 2)
    if not f: continue
    sl = slots_of(sq, K, s)
    c, over = price_slots(tuned, 111, 8, 439, s, K, list(sl))
    rows.append((float((c / ref - 1) * 100) if c else -999, sl, sq, f[0][0]))
rows.sort(reverse=True)
for r in rows: print('%+.2f%%' % r[0], r[1], r[2], r[3], flush=True)
