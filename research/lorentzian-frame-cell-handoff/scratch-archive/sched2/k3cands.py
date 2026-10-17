"""K = 3 (7 stages): all candidates (active pairs A = 1..3, any splits) with positive price (banks), touch-time and
interval lemma; group by sequence."""
import itertools, json, sys
sys.path.insert(0, '../k3')
import k3slots as KS
K = 3; s = 7
cache = {}
def pr(sl):
    if sl not in cache:
        c, over = KS.price_slots(KS.tuned, 111, 8, 439, s, K, list(sl)); cache[sl] = float((c / KS.ref - 1) * 100) if c else -999
    return cache[sl]
def stretches(sq, sp):
    out = []
    for r in range(K):
        actv = [j for j in range(s) if sq[j] == r]; lv = 0
        cuts = sorted(b for (q, b) in sp if q == r)
        for j in actv + [s]:
            if j > lv:
                pts = [lv] + [x for x in cuts if lv < x < j] + [j]
                out += [(r, pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
            lv = j + 1
    return out
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
def interval_ok(st):
    for b1 in range(s):
        for b2 in range(b1 + 1, s + 1):
            d = len({r for (r, a, b) in st if a <= b1 and b2 <= b})
            if (b2 - b1) - (1 if b1 == 0 else 0) > 2 * (K - d): return False
    return True
out = []
for A in (1, 2, 3):
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
        base = len(stretches(sq, ()))
        for k in range(0, 6 - base):
            for sp in itertools.combinations(opts, k):
                if any(not any(q == r for q, _ in sp) for r in range(A, K)): continue
                st = stretches(sq, sp)
                if len(st) > 5: continue
                sl = tuple(sorted(((b - a) * 7 for _, a, b in st), reverse=True))
                if not touch_ok(sq, sp) or not interval_ok(st): continue
                v = pr(sl)
                if v > 0: out.append((v, list(sq), sp, sl))
out.sort(reverse=True)
print(len(out), 'options;', len({tuple(o[1]) for o in out}), 'sequences')
for r in out[:10]: print('%+.3f%%' % r[0], r[1], r[2], r[3])
json.dump([(a, b, [list(x) for x in c], list(d)) for a, b, c, d in out], open('k3_cands.json', 'w'))
