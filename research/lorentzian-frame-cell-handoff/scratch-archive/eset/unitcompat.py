"""Internal alignment of the sharing units: odd (E-set, frame) pairs inside a complete star-D4 block (3 PPTT frames)
and inside a Pasch pair (2 TTTT frames); and cross statistics between disjoint units by support overlap."""
import sys, itertools, collections, random
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
idx = {(g.kind[i], g.supp[i]): i for i in range(V)}
P = lambda a, b: idx[('P', tuple(sorted((a, b))))]; T = lambda a, b, c: idx[('T', tuple(sorted((a, b, c))))]
orth = lambda a, b: a != b and G[a, b] == 0
ES = {}
def esets(f):
    if f not in ES:
        out = []
        for t, e in itertools.combinations(f, 2):
            k, l = [x for x in f if x not in (t, e)]
            out.append(set(u for u in range(V) if orth(u, t) and orth(u, e) and not orth(u, k) and not orth(u, l)))
        ES[f] = out
    return ES[f]
def cost(f1, f2): return sum(len(E & set(f2)) % 2 for E in esets(f1)) + sum(len(E & set(f1)) % 2 for E in esets(f2))
def block(h, S):
    a, b, c, d = S
    return [tuple(sorted((P(p, q), P(r, s), T(p, q, h), T(r, s, h)))) for (p, q), (r, s) in (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))]
def pasch(M):   # M = perfect matching of a 6-set: three pairs
    tr = [tuple(sorted((x, y, z))) for x in M[0] for y in M[1] for z in M[2]]
    cls = collections.defaultdict(list)
    for t in tr: cls[(t.index(M[0][0]) if False else 0, (M[0][0] in t) ^ (M[1][0] in t) ^ (M[2][0] in t))].append(T(*t))
    return [tuple(sorted(v)) for v in cls.values()]
B = block(4, (0, 1, 2, 3)); print('star block internal odd pairs:', sum(cost(a, b) for a, b in itertools.combinations(B, 2)))
Pp = pasch(((0, 1), (2, 3), (4, 5))); print('Pasch pair internal odd pairs:', sum(cost(a, b) for a, b in itertools.combinations(Pp, 2)), [len(x) for x in Pp])
# cross: random disjoint unit pairs by support overlap
random.seed(1); st = collections.defaultdict(list)
units = []
for h in range(11):
    for S in itertools.combinations([i for i in range(11) if i != h], 4): units.append(('B', set(S) | {h}, block(h, S)))
for Y in itertools.combinations(range(11), 6):
    for M in [((Y[0], Y[1]), (Y[2], Y[3]), (Y[4], Y[5])), ((Y[0], Y[2]), (Y[1], Y[3]), (Y[4], Y[5]))]:
        units.append(('P', set(Y), pasch(M)))
for _ in range(4000):
    u1, u2 = random.sample(units, 2)
    if set(x for f in u1[2] for x in f) & set(x for f in u2[2] for x in f): continue
    c = sum(cost(a, b) for a in u1[2] for b in u2[2])
    st[(u1[0] + u2[0], len(u1[1] & u2[1]))].append(c)
for k in sorted(st): print(k, 'n', len(st[k]), 'mean odd pairs %.1f' % (sum(st[k]) / len(st[k])), 'zero-cost frac %.2f' % (sum(1 for c in st[k] if c == 0) / len(st[k])))
