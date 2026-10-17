# Partial-section tops: target t takes from each of 3 triangle sections (3 users each) one of {N(H), p, q} where
# (p, q) is a 2-partition of H along its unique 2-hyperplane cover (F_a, F_b): p = (F_a - F_b) u X, q = (F_b - F_a) u (I - X),
# X any subset of I = F_a n F_b.  Find exact solutions c1 + c2 + c3 = N(t-perp) (linear algebra over F2 in the X bits).
import sys, itertools, numpy as np, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
from cov2 import all_covers, sect, mask
tname = sys.argv[1]
t = g.T(0, 1, 2) if tname == 'T' else g.P(0, 1)
A2s = []
for u in range(V):
    if u != t and abs(g.G[t, u]) == 1:
        w = [v for v in range(V) if v not in (t, u) and abs(g.G[t, v]) == 1 and abs(g.G[u, v]) == 1 and
             np.linalg.matrix_rank(g.L[[t, u, v]].astype(float)) == 2]
        for v in w: A2s.append(tuple(sorted((t, u, v))))
A2s = sorted(set(A2s))
print('triangles through t:', len(A2s), flush=True)
secs = []
for Q in A2s:
    H = sect(list(Q)); r, d, cov = all_covers(H, 300)
    secs.append((Q, H, cov))
print('2-cover counts per triangle section:', sorted(set(len(c[2]) for c in secs)), flush=True)
Rt = g.HYP[t]
def bitsof(ls): return mask(ls)
# options per section: list of (fixed_mask, free_list) meaning content = fixed ^ (subset of free chosen by bits)
opts = []
for Q, H, cov in secs:
    o = [('F', bitsof(H), [])]
    for (Fa, Fb) in cov:
        I = sorted(set(Fa) & set(Fb)); a_only = sorted(set(Fa) - set(Fb)); b_only = sorted(set(Fb) - set(Fa))
        o.append(('p', bitsof(a_only), I))                 # p = a_only + X
        # q = b_only + (I - X) = b_only + I + X  -> fixed b_only^I, free I (same X variable)
        o.append(('q', bitsof(b_only) ^ bitsof(I), I))
    opts.append(o)
sols = 0; examples = []
lines_t = bits(Rt)
for (i1, i2, i3) in itertools.combinations(range(len(secs)), 3):
    for o1 in opts[i1]:
        for o2 in opts[i2]:
            for o3 in opts[i3]:
                target = Rt ^ o1[1] ^ o2[1] ^ o3[1]
                frees = [(k, u) for k, o in enumerate((o1, o2, o3)) for u in o[2]]
                if not frees:
                    if target == 0: sols += 1; examples.append(((i1, o1[0]), (i2, o2[0]), (i3, o3[0])))
                    continue
                # solve sum of chosen free columns == target over F2; columns are single lines
                # variables are per (section k, line u); column = e_u.  Each line u: parity of chosen vars at u must equal target bit
                ok = True
                cover_lines = set(u for _, u in frees)
                for u in lines_t:
                    if (target >> u) & 1 and u not in cover_lines: ok = False; break
                if ok:
                    for u in bits(target):
                        if u not in cover_lines: ok = False; break
                if ok:
                    sols += 1
                    if len(examples) < 20: examples.append(((i1, o1[0]), (i2, o2[0]), (i3, o3[0])))
print('target', tname, '| solutions (section triples x part choices with some X assignment):', sols, flush=True)
for e in examples[:10]:
    print('  ', [(secs[i][0], f) for i, f in e])
pickle.dump((secs, examples), open('ptop_%s.pkl' % tname, 'wb'))
