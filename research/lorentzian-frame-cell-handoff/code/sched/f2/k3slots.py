import sys, itertools, math
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
from mpmath import mpf, mp
ref = mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
def price_slots(local, v, h, R, s, K, idle, T=32):
    a = h - 1; m = 1 + s * a; w = h
    slots = {}
    for c in idle: slots[c] = slots.get(c, 0) + 2 * v
    nres = R * s
    cap = sum(n * (c // w) for c, n in slots.items())
    nh = min(nres, cap); over = nres - nh
    nb = math.ceil(over * w / m); pad = nb * m - over * w
    W = 2 * K * v * T + nb * T
    q = mpf('0.0017')
    for _ in range(60):
        rem = P.host_greedy(slots, nh, w, q, m)
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * s
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        if pad: prof[pad] = prof.get(pad, 0) + T
        q2 = P.root(prof, m, W, env=False)
        if q2 is None: return None, over
        if abs(q2 - q) < mpf(10) ** -25: break
        q = q2
    return q2, over
def slots_of(sq, K, s, a=7):
    out = []
    for p in range(K):
        act = [j for j in range(s) if sq[j] == p]; lv = 0
        for j in act:
            if j > lv: out.append((j - lv) * a)
            lv = j + 1
        if s > lv: out.append((s - lv) * a)
    return tuple(sorted(out, reverse=True))
if __name__ != "__main__": K = 3
else: K = int(sys.argv[1])
s = 2 * K + 1
seen = {}
for sq in itertools.product(range(K), repeat=s):
    firsts = []
    for p in sq:
        if p not in firsts: firsts.append(p)
    if firsts != list(range(K)): continue
    seen.setdefault(slots_of(sq, K, s), sq)
res = []
for sl, sq in seen.items():
    c, over = price_slots(tuned, 111, 8, 439, s, K, list(sl))
    res.append((float((c / ref - 1) * 100) if c else -999, sl, over, sq))
res.sort(reverse=True)
for r in res[:12]: print('%+.2f%%' % r[0], r[1], 'banked', r[2], r[3])
