"""For every canonical K=4 sequence, all split sets (<= 3 splits, each split = (idle pair r, level b) interior to r's
idle interval) with total stretches <= 9 and positive price; output sequences sorted by best potential price."""
import itertools, json, sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/sched')
from genprice import price
from splitp import slots
import mpmath as mp
ref = mp.mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
K = 4; s = 9
cache = {}
def pr(sl):
    if sl not in cache:
        c, d = price(tuned, 111, 8, 439, s, K, list(sl))
        cache[sl] = float((c / ref - 1) * 100) if c else -999
    return cache[sl]
out = []
for sq in itertools.product(range(K), repeat=s):
    firsts = []
    for x in sq:
        if x not in firsts: firsts.append(x)
    if firsts != list(range(K)): continue
    act = {r: [j for j in range(s) if sq[j] == r] for r in range(K)}
    def interior(r, b):
        last = max([j for j in act[r] if j < b], default=-1); nxt = min([j for j in act[r] if j >= b], default=s)
        return (last + 1) < b < nxt
    opts = [(r, b) for b in range(1, s) for r in range(K) if r not in (sq[b - 1], sq[b]) and interior(r, b)]
    base = len(slots(list(sq), ()))
    best = None
    for k in range(0, 4):
        if base + k > 9: break
        for sp in itertools.combinations(opts, k):
            sl = slots(list(sq), sp)
            v = pr(sl)
            if v > 0 and (best is None or v > best[0]): best = (v, sp, sl)
    if best: out.append((best[0], list(sq), best[1], best[2]))
out.sort(reverse=True)
json.dump(out, open('splitcands_K4.json', 'w'))
print(len(out), 'sequences with a positive split option')
for r in out[:30]: print('%+.3f%%' % r[0], r[1], r[2], r[3])
