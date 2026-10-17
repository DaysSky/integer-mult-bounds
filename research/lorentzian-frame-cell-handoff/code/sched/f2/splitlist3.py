"""K = 4 candidates including PASSIVE pairs (never active; touched only by splits).  Sequences use pairs 0..a-1
(a = 2, 3; canonical first-occurrence order); pairs a..3 are passive.  Split options: (pair, boundary) with the pair
idle across the boundary (passive pairs: every boundary).  Keep options with <= 9 stretches, positive price and the
touch-time bounds; every passive pair needs >= 1 touch."""
import itertools, json, sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/sched')
from genprice import price
import mpmath as mp
ref = mp.mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
K = 4; s = 9; a7 = 7
cache = {}
def pr(sl):
    if sl not in cache:
        c, d = price(tuned, 111, 8, 439, s, K, list(sl)); cache[sl] = float((c / ref - 1) * 100) if c else -999
    return cache[sl]
def slots(sq, sp):
    out = []
    for r in range(K):
        actv = [j for j in range(s) if sq[j] == r]; lv = 0
        cuts = sorted(b for (q, b) in sp if q == r)
        for j in actv + [s]:
            if j > lv:
                pts = [lv] + [x for x in cuts if lv < x < j] + [j]
                out += [(pts[i + 1] - pts[i]) * a7 for i in range(len(pts) - 1)]
            lv = j + 1
    return tuple(sorted(out, reverse=True))
def touch_ok(sq, sp):
    tau = {r: 99 for r in range(K)}; lam = {r: -1 for r in range(K)}
    for j, p in enumerate(sq): tau[p] = min(tau[p], j); lam[p] = max(lam[p], j + 1)
    for b in range(1, s):
        if sq[b - 1] != sq[b]:
            for r in (sq[b - 1], sq[b]): tau[r] = min(tau[r], b); lam[r] = max(lam[r], b)
    for (r, b) in sp: tau[r] = min(tau[r], b); lam[r] = max(lam[r], b)
    if any(tau[r] == 99 for r in range(K)): return False
    ts = sorted(tau.values()); ls = sorted(lam.values(), reverse=True)
    return all(ts[k] <= 2 * k for k in range(K)) and all(s - ls[k] <= 2 * k for k in range(K))
out = []
for A in (2, 3):
    for sq in itertools.product(range(A), repeat=s):
        firsts = []
        for x in sq:
            if x not in firsts: firsts.append(x)
        if firsts != list(range(A)): continue
        act = {r: [j for j in range(s) if sq[j] == r] for r in range(K)}
        if any(act[r] == [0] or act[r] == [s - 1] for r in range(A)): continue
        def interior(r, b):
            last = max([j for j in act[r] if j < b], default=-1); nxt = min([j for j in act[r] if j >= b], default=s)
            return (last + 1) < b < nxt
        opts = [(r, b) for b in range(1, s) for r in range(K) if r not in (sq[b - 1], sq[b]) and interior(r, b)]
        base = len(slots(sq, ()))          # passive pairs contribute one 63-stretch each before splits
        for k in range(K - A, 4):
            if base + k > 9: break
            for sp in itertools.combinations(opts, k):
                if any(not any(q == r for q, _ in sp) for r in range(A, K)): continue
                times = [b for _, b in sp]
                if any(times.count(t) > 2 for t in times): continue
                sl = slots(sq, sp)
                if len(sl) > 9: continue
                v = pr(sl)
                if v > 0 and touch_ok(sq, sp): out.append((v, list(sq), sp, sl))
out.sort(reverse=True)
print(len(out), 'options with passive pairs')
byseq = {}
for v, sq, sp, sl in out: byseq.setdefault(tuple(sq), []).append((v, sp))
print(len(byseq), 'sequences')
for r in out[:20]: print('%+.3f%%' % r[0], r[1], r[2], r[3])
json.dump([(a, b, [list(x) for x in c], list(d)) for a, b, c, d in out], open('splitlist_passive.json', 'w'))
