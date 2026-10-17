"""D4-block tops for I_{11,1}: all D4 flats (12 lines, rank 4), their users (targets t with the flat inside t-perp),
and whether each target's need t-perp lies in the F2 span of the D4 flats inside it (and of D4 flats + single lines),
with the minimum number of D4 blocks needed (greedy + exact check)."""
import sys, pickle, itertools, collections, numpy as np
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
sys.path.insert(0, D); sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
import flats
G = g.G
reps = pickle.load(open(D + 'flats_reps.pkl', 'rb'))
d4reps = [cl for cl in reps[4].values() if len(cl) == 12]
print('D4 flat orbits (12 lines, rank 4):', len(d4reps), flush=True)
LINES = {tuple(sorted(g.supp[x])): x for x in range(V)}
def image(cl, p): return tuple(sorted(LINES[tuple(sorted(p[i] for i in g.supp[x]))] for x in cl))
allD4 = set()
for rep in d4reps:
    pts = sorted(set(i for x in rep for i in g.supp[x]))
    # orbit: permutations matter only on the support points (images of the support set and its labelling)
    for img in itertools.permutations(range(11), len(pts)):
        p = list(range(11)); mp = dict(zip(pts, img))
        q = [mp.get(i, None) for i in range(11)]
        free = [i for i in range(11) if i not in img]; it = iter(free)
        q = [mp[i] if i in mp else next(it) for i in range(11)]
        allD4.add(image(rep, q))
allD4 = sorted(allD4)
print('D4 flats in total:', len(allD4), flush=True)
users = [[t for t in range(V) if t not in d and all(G[t, x] == 0 for x in d)] for d in allD4]
print('users per D4 flat: distribution', sorted(collections.Counter(len(u) for u in users).items()), flush=True)
def f2_in_span(vecs, target):
    basis = {}
    for v in vecs:
        while v:
            hb = v.bit_length() - 1
            if hb in basis: v ^= basis[hb]
            else: basis[hb] = v; break
    x = target
    while x:
        hb = x.bit_length() - 1
        if hb not in basis: return False, len(basis)
        x ^= basis[hb]
    return True, len(basis)
mask = lambda S: sum(1 << i for i in S)
for t in (55, 0):     # one T line, one P line
    perp = [s for s in range(V) if s != t and G[t, s] == 0]
    inside = [d for d, u in zip(allD4, users) if t in u]
    ok, rk = f2_in_span([mask(d) for d in inside], mask(perp))
    print('target %s %s: |perp| %d, D4 flats inside perp %d (span rank %d), perp in span: %s' % (g.kind[t], tuple(g.supp[t]), len(perp), len(inside), rk, ok), flush=True)
    # with single lines allowed: minimum number of singles needed = distance from perp to the span
    basis = {}
    for v in [mask(d) for d in inside]:
        while v:
            hb = v.bit_length() - 1
            if hb in basis: v ^= basis[hb]
            else: basis[hb] = v; break
    x = mask(perp)
    while x:
        hb = x.bit_length() - 1
        if hb in basis: x ^= basis[hb]
        else: break
    print('   reduced residual weight (upper bound on singles needed): %d' % bin(x).count('1'), flush=True)
pickle.dump(dict(allD4=allD4, users=users), open(D + 'd4flats.pkl', 'wb'))
