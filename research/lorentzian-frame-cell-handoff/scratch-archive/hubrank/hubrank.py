# Varying-part hub capacity on partA (E-set top).  Consumers = E-set registers (F,{x,y}) with content
# E_xy = {u : R(u) n F = {x,y}} at pm(x,y).  A hub frame Z serves the consumers whose pair lies in Z-perp
# (Z <= pm(x,y)).  At Z, k parked registers can give each consumer any F2 combination, so the registers needed
# at Z = F2 rank of the matrix M_Z (consumers x lines(Z), entry [u in E_xy]); capacity = ones(M_Z) / rank(M_Z).
# Z ranges over W-perp for W = closure of 1, 2 or 3 consumer pairs (W must be nondegenerate, Z too).
import sys, pickle, itertools, numpy as np, time
from collections import Counter
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
part = pickle.load(open('../blk/partA.pkl', 'rb'))
frames = [tuple(f) for b in part[0] for f in b]; punct = set(part[1])
live = [u for u in range(V) if u not in punct]; LIVE = sum(1 << u for u in live)
RS = {u: g.HYP[u] & LIVE for u in live}
cons = []                     # (frame idx, x, y, E mask)
for fi, f in enumerate(frames):
    for x, y in itertools.combinations(f, 2):
        z, w = [q for q in f if q not in (x, y)]
        E = 0
        for u in live:
            if u in f: continue
            if (RS[u] >> x) & 1 and (RS[u] >> y) & 1 and not (RS[u] >> z) & 1 and not (RS[u] >> w) & 1: E |= 1 << u
        cons.append((fi, x, y, E))
print('consumers', len(cons), 'incidences', sum(bin(c[3]).count('1') for c in cons))
def f2rank(rows):
    piv = {}; r = 0
    for x in rows:
        while x:
            hb = x.bit_length() - 1
            if hb in piv: x ^= piv[hb]
            else: piv[hb] = x; r += 1; break
    return r
def perp(W):
    m = LIVE
    for s in bits(W): m &= g.HYP[s]
    return m
pairs = [(c[1], c[2]) for c in cons]
cand = {}
t0 = time.time()
for k in (1, 2, 3):
    combos = itertools.combinations(range(len(pairs)), k) if k < 3 else None
    if k == 3:
        # 3-pair hubs: extend each good 2-pair W by a third pair
        good2 = sorted(((v[1], W) for W, v in cand.items() if v[0] == 2), reverse=True)[:400]
        combos = ((W, j) for _, W in good2 for j in range(len(pairs)))
    for cb in combos:
        if k < 3:
            m = 0
            for i in cb: m |= (1 << pairs[i][0]) | (1 << pairs[i][1])
            W = closure(m)
        else:
            W0, j = cb; W = closure(W0 | (1 << pairs[j][0]) | (1 << pairs[j][1]))
        if W in cand or dim(W) > 7: continue
        Z = perp(W)
        if not Z: continue
        Zc = closure(Z)
        if not nondegenerate(W) or not nondegenerate(Zc): cand[W] = (k, -1); continue
        users = [c for c in cons if ((W >> c[1]) & 1) and ((W >> c[2]) & 1)]
        rows = [c[3] & Zc for c in users]
        rows = [r for r in rows if r]
        if not rows: cand[W] = (k, 0); continue
        ones = sum(bin(r).count('1') for r in rows); rk = f2rank(rows)
        cand[W] = (k, ones / rk, ones, rk, len(rows), dim(W), dim(Zc))
    print('k', k, 'hubs', len(cand), '%.0fs' % (time.time() - t0), flush=True)
best = sorted((v for v in cand.values() if len(v) > 2), key=lambda v: -v[1])
print('top capacities (k, ones/rank, ones, rank, consumers, rank W, rank Z):')
for v in best[:25]: print('  ', v)
print('capacity histogram (rounded):', sorted(Counter(int(v[1]) for v in best).items()))
pickle.dump(cand, open('hubrank.pkl', 'wb'))
