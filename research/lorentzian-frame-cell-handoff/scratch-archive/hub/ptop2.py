# Partial-section tops over ALL plane sections {t,u}-perp with a 2-hyperplane cover (cells: 2 users, triangles: 3 users).
import sys, itertools, numpy as np, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
from cov2 import all_covers, sect, mask
tname = sys.argv[1]
t = g.T(0, 1, 2) if tname == 'T' else g.P(0, 1)
seen = {}; secs = []
for u in range(V):
    if u == t or abs(g.G[t, u]) > 1: continue
    H = tuple(sect([t, u]))
    if H in seen: continue
    seen[H] = u
    users = [w for w in range(V) if all(abs(g.G[w, h]) < 0.5 for h in H)]
    r, d, cov = all_covers(list(H), 200)
    secs.append((u, list(H), cov, users))
print('distinct plane sections through t:', len(secs), '| with 2-covers:', sum(1 for s in secs if s[2]),
      '| users dist', collections.Counter(len(s[3]) for s in secs if s[2]), flush=True)
Rt = g.HYP[t]
opts = []
for u, H, cov, users in secs:
    o = [('F', mask(H), 0)]
    for (Fa, Fb) in cov:
        I = set(Fa) & set(Fb); a_only = set(Fa) - I; b_only = set(Fb) - I
        o.append(('p', mask(a_only), mask(I)))
        o.append(('q', mask(b_only) ^ mask(I), mask(I)))
    opts.append(o)
idx = [k for k in range(len(secs))]
sols = []; cnt = 0
for (i1, i2, i3) in itertools.combinations(idx, 3):
    for o1 in opts[i1]:
        for o2 in opts[i2]:
            f12 = o1[1] ^ o2[1]; fr12 = o1[2] | o2[2]
            for o3 in opts[i3]:
                target = Rt ^ f12 ^ o3[1]
                if target & ~(fr12 | o3[2]) == 0:
                    cnt += 1
                    if len(sols) < 2000: sols.append(((i1, o1[0]), (i2, o2[0]), (i3, o3[0])))
print('target', tname, '| solutions:', cnt, flush=True)
kinds = collections.Counter(tuple(sorted((len(secs[i][3]), f) for i, f in s)) for s in sols)
print('solution kinds (users, part):', kinds.most_common(12), flush=True)
pickle.dump((secs, sols), open('ptop2_%s.pkl' % tname, 'wb'))
