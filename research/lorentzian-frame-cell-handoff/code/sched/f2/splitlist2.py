"""K = 4 options with two splits at the SAME boundary (not covered by the <= 1-per-time search): total stretches <= 9,
positive price, touch-time bounds satisfied."""
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
        c, d = price(tuned, 111, 8, 439, s, K, list(sl)); cache[sl] = float((c / ref - 1) * 100) if c else -999
    return cache[sl]
def touch_ok(sq, sp):
    tau = {r: 99 for r in range(K)}; lam = {r: -1 for r in range(K)}
    for j, p in enumerate(sq): tau[p] = min(tau[p], j); lam[p] = max(lam[p], j + 1)
    for b in range(1, s):
        if sq[b - 1] != sq[b]:
            for r in (sq[b - 1], sq[b]): tau[r] = min(tau[r], b); lam[r] = max(lam[r], b)
    for (r, b) in sp: tau[r] = min(tau[r], b); lam[r] = max(lam[r], b)
    ts = sorted(tau.values()); ls = sorted(lam.values(), reverse=True)
    return all(ts[k] <= 2 * k for k in range(K)) and all(s - ls[k] <= 2 * k for k in range(K))
out = []
for sq in itertools.product(range(K), repeat=s):
    firsts = []
    for x in sq:
        if x not in firsts: firsts.append(x)
    if firsts != list(range(K)): continue
    act = {r: [j for j in range(s) if sq[j] == r] for r in range(K)}
    if any(act[r] == [0] or act[r] == [s - 1] for r in range(K)): continue
    def interior(r, b):
        last = max([j for j in act[r] if j < b], default=-1); nxt = min([j for j in act[r] if j >= b], default=s)
        return (last + 1) < b < nxt
    opts = [(r, b) for b in range(1, s) for r in range(K) if r not in (sq[b - 1], sq[b]) and interior(r, b)]
    base = len(slots(list(sq), ()))
    for k in (2, 3):
        if base + k > 9: break
        for sp in itertools.combinations(opts, k):
            times = [b for (_, b) in sp]
            if len(set(times)) == len(times): continue          # need a double split at some time
            sl = slots(list(sq), sp)
            if pr(sl) > 0 and touch_ok(sq, sp): out.append((pr(sl), list(sq), sp, sl))
out.sort(reverse=True)
print(len(out), 'options with a double split at one boundary, positive, touch-OK')
for r in out[:20]: print('%+.3f%%' % r[0], r[1], r[2], r[3])
json.dump([(a, b, [list(x) for x in c], list(d)) for a, b, c, d in out], open('splitlist_double.json', 'w'))
