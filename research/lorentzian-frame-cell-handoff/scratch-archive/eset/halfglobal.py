"""All good 4-frames of I_{11,1} (enumerated here: orthogonal 4-sets where every line perp t, other than the partners,
is perp an odd number of partners).  For every frame and section, its two sign halves (on all 220 lines).  Count how
often each half (as a line set) occurs across all good frames: a half occurring in m frames could be shared by up to
m sections of a partition (E8: every half occurs in 3 sections of the R420 partition)."""
import sys, collections, itertools, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(int(sys.argv[1]) if len(sys.argv) > 1 else 11); V = g.V; G = g.G
OM = [0] * V
for i in range(V):
    for j in range(V):
        if i != j and G[i, j] == 0: OM[i] |= 1 << j
def good(q):
    for t in q:
        es = [e for e in q if e != t]
        R = OM[t] & ~sum(1 << e for e in es); a, b, c = (OM[e] for e in es)
        if R & ~(a ^ b ^ c): return False
    return True
frames = []
for a in range(V):
    for b in range(a + 1, V):
        if not OM[a] >> b & 1: continue
        cab = OM[a] & OM[b] & ~((1 << (b + 1)) - 1)
        while cab:
            x = cab & -cab; c = x.bit_length() - 1; cab ^= x
            cabc = OM[a] & OM[b] & OM[c] & ~((1 << (c + 1)) - 1)
            while cabc:
                y = cabc & -cabc; d = y.bit_length() - 1; cabc ^= y
                if good((a, b, c, d)): frames.append((a, b, c, d))
print('good frames', len(frames), flush=True)
occ = collections.Counter(); where = collections.defaultdict(list)
for fi, f in enumerate(frames):
    for t, e in itertools.combinations(f, 2):
        k, l = [x for x in f if x not in (t, e)]
        E = OM[t] & OM[e] & ~OM[k] & ~OM[l] & ~(1 << k) & ~(1 << l)
        Ep = 0; Em = 0; m = E
        while m:
            x = m & -m; u = x.bit_length() - 1; m ^= x
            if G[u, k] == G[u, l]: Ep |= x
            else: Em |= x
        for H in (Ep, Em):
            occ[H] += 1; where[H].append(fi)
mult = collections.Counter(occ.values())
print('half multiplicity over all good frames (multiplicity: #distinct halves):', sorted(mult.items()), flush=True)
# multiplicity counted in distinct frames
fm = collections.Counter(len(set(v)) for v in where.values())
print('distinct frames per half:', sorted(fm.items()))
pickle.dump(dict(frames=frames, where={H: v for H, v in where.items() if len(set(v)) > 1}), open('halfglobal.pkl', 'wb'))
