# Telescoped 3-level chains: collector reads full sums along G1 < G2 < H, content = N(G1)+N(G2)+N(H).
# G2 ranges over the 2-cover part flats of H (closures of F_a, F_b), G1 over 2-cover part flats of G2 (and empty).
# Search triples of sections with contents (1-, 2-, 3-level) summing exactly to R(t).
import sys, itertools, numpy as np, pickle, collections, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
from cov2 import all_covers, mask
tname = sys.argv[1]; t0 = time.time()
secs, _ = pickle.load(open('ptop2_%s.pkl' % tname, 'rb'))
t = g.T(0, 1, 2) if tname == 'T' else g.P(0, 1)
Rt = g.HYP[t]
cache = {}
def part_flats(Hlines):
    key = tuple(sorted(Hlines))
    if key in cache: return cache[key]
    r, d, cov = all_covers(list(Hlines), 150)
    out = set()
    for Fa, Fb in cov:
        for F in (Fa, Fb):
            m = closure(mask(F))
            if m and nondegenerate(m) and m != mask(Hlines): out.add(m)
    cache[key] = sorted(out); return cache[key]
opts = []
for u, H, cov, users in secs:
    Hm = mask(H); o = {Hm}
    for G2 in part_flats(H):
        o.add(Hm ^ G2)
        for G1 in part_flats(bits(G2)):
            o.add(Hm ^ G2 ^ G1)
    opts.append(sorted(o))
print(tname, 'sections', len(secs), '| contents per section: mean %.1f max %d' % (np.mean([len(o) for o in opts]), max(len(o) for o in opts)),
      '| %.0fs' % (time.time() - t0), flush=True)
# exact triples: c1 ^ c2 ^ c3 == Rt
idx = {}
for k, o in enumerate(opts):
    for c in o: idx.setdefault(c, []).append(k)
sols = 0; ex = []
for i in range(len(opts)):
    for j in range(i + 1, len(opts)):
        for c1 in opts[i]:
            for c2 in opts[j]:
                need = Rt ^ c1 ^ c2
                for k in idx.get(need, []):
                    if k > j:
                        sols += 1
                        if len(ex) < 10: ex.append((i, j, k, len(secs[i][3]), len(secs[j][3]), len(secs[k][3])))
print('exact 3-section telescoped tops:', sols, '| users of sections in examples', [e[3:] for e in ex], '| %.0fs' % (time.time() - t0), flush=True)
