"""Structure of the 576 distinct sign halves of the 17-Pasch-pair (maxpairs) partition of I_{13,1}: closure ranks,
reader targets, and how far a one-frame-per-dimension register can share them.  Format fact used (gcheck climb rule:
nested climbs with strictly increasing dimension): every register visits at most one frame of each dimension."""
import os, pickle, itertools, collections, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; HYP = g.HYP; G = g.G; bits = g.bits
pc = lambda m: bin(m).count('1')
def cl(m): return g.closure(m)
part = pickle.load(open('/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7/i13n/maxpairs_partition.pkl', 'rb'))
part = [tuple(f) for f in part]
assert sorted(l for f in part for l in f) == list(range(V))
ref = set(sum(1 << u for u in h) for h in pickle.load(open(os.path.join(HERE, 'halves_maxpairs.pkl'), 'rb')))
readers = collections.defaultdict(set); slots = collections.Counter(); owner = collections.defaultdict(set)
Qs = []
for fi, f in enumerate(part):
    Qs.append(HYP[f[0]] & HYP[f[1]] & HYP[f[2]] & HYP[f[3]])
    for a, b in itertools.combinations(range(4), 2):
        c, d = [f[z] for z in range(4) if z not in (a, b)]
        E = HYP[f[a]] & HYP[f[b]] & ~HYP[c] & ~HYP[d]
        Ep = sum(1 << u for u in bits(E) if G[u, c] == G[u, d]); Em = E & ~Ep
        for H in (Ep, Em):
            readers[H] |= {f[a], f[b]}; slots[H] += 1; owner[H].add(fi)
H = sorted(readers)
print('distinct halves', len(H), 'slots', sum(slots.values()), 'match saved file:', set(H) == ref)
print('half sizes', dict(sorted(collections.Counter(pc(h) for h in H).items())))
rk = {h: cl(h)[1] for h in H}; CL = {h: cl(h)[0] for h in H}
print('(size, closure rank, |closure lines|):', dict(sorted(collections.Counter((pc(h), rk[h], pc(CL[h])) for h in H).items())))
print('readers per half:', dict(sorted(collections.Counter(len(readers[h]) for h in H).items())))
print('distinct closures', len(set(CL.values())), '; halves per closure', dict(collections.Counter(collections.Counter(CL.values()).values())))
# common reader perp: dim of intersection of reader perps (as a subspace), lines in it
def perp_lines(ts):
    m = (1 << V) - 1
    for t in ts: m &= HYP[t]
    return m
cr = collections.Counter()
for h in H:
    P = perp_lines(readers[h]); cP, dP = cl(P)
    cr[(rk[h], dP, CL[h] == cP)] += 1
print('(closure rank, rank of reader-common-perp flat, closure == common perp):', dict(sorted(cr.items())))
# per-target view: the halves a target reads, their closure ranks, and how many distinct closures per rank
tv = collections.Counter(); spread = collections.Counter()
by_t = collections.defaultdict(list)
for h in H:
    for t in readers[h]: by_t[t].append(h)
for t, hs in by_t.items():
    tv[len(hs)] += 1
    spread[tuple(sorted(collections.Counter(rk[h] for h in hs).items()))] += 1
print('halves read per target:', dict(sorted(tv.items())))
print('per-target closure-rank profile (rank: #halves) -> #targets:', dict(spread.most_common(6)))
# one-frame-per-dimension: a target's chain has <= 1 frame per dim, so halves with distinct rank-r closures read at
# rank r need distinct dims; the minimum number of chain frames ⊆ t-perp that hold all of t's halves (+ Q) is the
# length of a shortest nested chain covering every closure: computed greedily by joins (exact for <= 7 sets: try all
# orders of first-reading).
def min_private(t):
    hs = by_t[t]
    fi = [i for i, f in enumerate(part) if t in f][0]
    items = [CL[h] for h in hs] + [cl(Qs[fi])[0]]
    best = None
    # a reading chain is F_1 < F_2 < ... ; items read at F_k need closure <= F_k.  Greedy over orderings of items:
    # F_k = closure of the union of the first k items' closures; count distinct frames.
    for order in itertools.permutations(range(len(items))):
        fr = []; acc = 0
        for i in order:
            acc |= items[i]; c, d = cl(acc)
            if not fr or fr[-1][0] != c: fr.append((c, d))
        top = fr[-1][1]
        key = (len(fr), max(d for c, d in fr))
        if best is None or key < best[0]: best = (key, [d for c, d in fr])
    return best
import random; random.seed(1)
sample = random.sample(sorted(by_t), 24)
res = collections.Counter()
for t in sample:
    (n, top), dims = min_private(t)
    res[tuple(dims)] += 1
print('best reading-chain dims over orderings (sample of 24 targets):', dict(res.most_common()))
pickle.dump({'H': H, 'readers': {h: sorted(readers[h]) for h in H}, 'rk': rk}, open(os.path.join(HERE, 'halves_struct.pkl'), 'wb'))
