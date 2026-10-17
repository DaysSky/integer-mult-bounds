"""Rigorous checks for the I_{13,1} alignment computation.
(1) Independent compatibility implementation (Python bitmask ints, direct definition) vs the numpy matrix on random pairs.
(2) Goodness of every frame (all 70,785) under the definition.
(3) For one PPTT and one TTTT representative f0: lines that no frame compatible with f0 (and disjoint) can cover."""
import sys, itertools, random, pickle, numpy as np, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
n = 13; g = Geom(n); V = g.V; G = g.G
frames, comp_lists, kinds = pickle.load(open('compat13.pkl', 'rb'))
nf = len(frames)
OM = [sum(1 << j for j in range(V) if j != i and G[i, j] == 0) for i in range(V)]
def good_for(t, es):
    R = OM[t] & ~sum(1 << e for e in es)
    a, b, c = (OM[e] for e in es)
    return (R & ~(a ^ b ^ c)) == 0
bad = [q for q in frames if not all(good_for(t, [e for e in q if e != t]) for t in q)]
print('(2) frames failing goodness:', len(bad))
mut = [q for q in frames if not all(G[a, b] == 0 for a, b in itertools.combinations(q, 2))]
print('    frames not mutually orthogonal:', len(mut))
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
def esets(q):
    out = []
    for a, b in pairs:
        o = [c for c in range(4) if c not in (a, b)]
        out.append(OM[q[a]] & OM[q[b]] & ~OM[q[o[0]]] & ~OM[q[o[1]]])
    return out
def compat(i, j):
    q1, q2 = frames[i], frames[j]
    if set(q1) & set(q2): return False
    m1 = sum(1 << x for x in q1); m2 = sum(1 << x for x in q2)
    return all(bin(E & m2).count('1') % 2 == 0 for E in esets(q1)) and all(bin(E & m1).count('1') % 2 == 0 for E in esets(q2))
import bisect
def incomp(i, j):
    a = comp_lists[i]; k = np.searchsorted(a, j)
    return k < len(a) and a[k] == j
random.seed(1); mism = 0; tested = 0; npos = 0
for _ in range(20000):
    i, j = random.randrange(nf), random.randrange(nf)
    if i == j: continue
    a = compat(i, j); b = incomp(i, j)
    tested += 1; npos += a
    if a != b: mism += 1
# also test positives specifically
for i in random.sample(range(nf), 200):
    for j in random.sample(comp_lists[i].tolist(), min(20, len(comp_lists[i]))):
        tested += 1
        if not compat(i, j): mism += 1
print('(1) compat cross-check: tested', tested, 'mismatches', mism, '(random positives %d)' % npos)
print('    symmetry of matrix: asymmetric pairs', sum(1 for i in random.sample(range(nf), 300) for j in comp_lists[i].tolist() if not incomp(j, i)))
member = collections.defaultdict(list)
for j, q in enumerate(frames):
    for u in q: member[u].append(j)
for typ in ('PPTT', 'TTTT'):
    i0 = next(i for i in range(nf) if kinds[i] == typ)
    allowed = set(comp_lists[i0].tolist())
    dead = [u for u in range(V) if u not in frames[i0] and not any(j in allowed for j in member[u])]
    cnts = sorted(sum(1 for j in member[u] if j in allowed) for u in range(V) if u not in frames[i0])
    print('(3) %s f0=%s: uncoverable lines %d %s; min/median allowed per line %d/%d' % (
        typ, [g.supp[x] for x in frames[i0]], len(dead), [(g.kind[u], g.supp[u]) for u in dead[:12]], cnts[0], cnts[len(cnts)//2]))
