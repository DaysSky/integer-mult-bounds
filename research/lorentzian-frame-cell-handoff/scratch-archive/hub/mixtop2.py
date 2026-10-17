# Efficient cover search: R(t) <= H u F2 u F3 (H plane section rank 9, F rank-8 closed frames W-perp, W = span(t,u,v)),
# and R(t) <= F1 u F2 u F3 (three rank-8 frames; tests kappa8 >= 4 within closed frames).  Bitset index over frames.
import sys, itertools, numpy as np, collections, pickle, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
tname = sys.argv[1]; t0 = time.time()
t = g.T(0, 1, 2) if tname == 'T' else g.P(0, 1)
Rt = g.HYP[t]; Rl = bits(Rt)
def perpm(ls):
    m = (1 << V) - 1
    for u in ls: m &= g.HYP[u]
    return m
cand = [u for u in range(V) if u != t and abs(g.G[t, u]) <= 1]
F8 = {}
for u, v in itertools.combinations(cand, 2):
    m = perpm([t, u, v]) & Rt
    if m in F8 or m == 0: continue
    if np.linalg.matrix_rank(g.L[[t, u, v]].astype(float)) != 3: continue
    if dim(m) != 8: continue
    F8[m] = sum(1 for w in range(V) if all(abs(g.G[w, h]) < 0.5 for h in bits(m)))
Fl = sorted(F8, key=lambda m: -bin(m).count('1'))
nF = len(Fl)
print(tname, 'rank-8 closed frames', nF, '| max lines', bin(Fl[0]).count('1'), '| %.0fs' % (time.time() - t0), flush=True)
contain = {u: 0 for u in Rl}
for k, m in enumerate(Fl):
    for u in bits(m): contain[u] |= 1 << k
ALL = (1 << nF) - 1
def any_frame_containing(mask):
    s = ALL
    for u in bits(mask):
        s &= contain[u]
        if not s: return 0
    return s
# (F,F,F)
fff = 0
for i, a in enumerate(Fl):
    if bin(a).count('1') * 3 < len(Rl): break
    rest = Rt & ~a
    for b in Fl[i:]:
        r2 = rest & ~b
        if bin(r2).count('1') > bin(Fl[0]).count('1'): continue
        if any_frame_containing(r2): fff += 1; break
print('  (F,F,F) covers found (first-F count):', fff, '| %.0fs' % (time.time() - t0), flush=True)
H9 = {}
for u in cand:
    m = perpm([t, u]) & Rt
    if m and dim(m) == 9: H9.setdefault(m, u)
hff = 0; ex = []; uh = collections.Counter()
for h in H9:
    rest = Rt & ~h
    for a in Fl:
        r2 = rest & ~a
        if bin(r2).count('1') > bin(Fl[0]).count('1'): continue
        s = any_frame_containing(r2)
        if s:
            hff += 1
            k = (s & -s).bit_length() - 1
            uh[(bin(h).count('1'), F8[a], F8[Fl[k]])] += 1
            if len(ex) < 6: ex.append((g.kind[H9[h]], g.supp[H9[h]], bin(a).count('1'), F8[a], bin(Fl[k]).count('1'), F8[Fl[k]]))
print('  (H,F,F) covers (H, F2 pairs extendable):', hff, '| (H lines, users F2, users F3):', uh.most_common(10), flush=True)
print('  examples', ex, '| %.0fs' % (time.time() - t0), flush=True)
pickle.dump((Fl, F8, H9), open('mix_%s.pkl' % tname, 'wb'))
