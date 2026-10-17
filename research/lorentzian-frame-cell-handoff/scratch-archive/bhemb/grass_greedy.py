"""Constructive Grassmann embedding in the code's causal order (F_2^10, 5-dim subspaces).
Vertex v (in order) picks, among the subspaces at distance <= 1 from one earlier neighbour, one that minimises
(# earlier neighbours at distance > 1) * BIG + (# earlier session partners not complementary) * BIG2 + edge distance sum.
Randomised tie-breaking; many restarts.  usage: grass_greedy.py restarts seed"""
import pickle, json, random, sys, time, itertools
b = pickle.load(open('../bh/bh.pkl', 'rb')); E = b['phys']; S = b['sessions']
order = [int(x) for x in json.load(open('/home/user/ext/multiple-unicast-counterexample/data/182-vertex-code.json'))['order']]
pos = {v: i for i, v in enumerate(order)}; m = 5; n = 10; V = 182
nb = [[] for _ in range(V)]; sv = [[] for _ in range(V)]
for u, v in E: nb[u].append(v); nb[v].append(u)
for s, t in S: sv[s].append(t); sv[t].append(s)
def rank(rows):
    rows = list(rows); r = 0
    for bit in range(n - 1, -1, -1):
        piv = next((i for i in range(r, len(rows)) if rows[i] >> bit & 1), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> bit & 1: rows[i] ^= rows[r]
        r += 1
    return r
def reduce(rows):  # canonical RREF tuple
    rows = list(rows); r = 0; piv_bits = []
    for bit in range(n - 1, -1, -1):
        piv = next((i for i in range(r, len(rows)) if rows[i] >> bit & 1), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> bit & 1: rows[i] ^= rows[r]
        r += 1
    return tuple(sorted(rows[:r]))
def dist(A, B): return rank(list(A) + list(B)) - m
def span(rows):
    out = {0}
    for r in rows: out |= {x ^ r for x in out}
    return out
def neighbours(A):
    """all 5-spaces W with dim(W cap A) >= 4: choose a 4-dim subspace (hyperplane of A) and a new vector outside A."""
    A = list(A); spA = span(A); res = {tuple(sorted(A))}
    hyper = set()
    for f in range(1, 1 << m):     # hyperplanes of A = kernels of nonzero functionals on coordinates of A
        H = [x for x in spA if bin(f & coords(x, A)).count('1') % 2 == 0]
        hyper.add(frozenset(H))
    outside = [x for x in range(1, 1 << n) if x not in spA]
    for H in hyper:
        basisH = basis(list(H))
        for x in outside:
            res.add(reduce(basisH + [x]))
    return res
def basis(vecs):
    B = []
    for v in vecs:
        if v and rank(B + [v]) > len(B): B.append(v)
    return B
CO = {}
def coords(x, A):
    key = (x, tuple(A))
    if key in CO: return CO[key]
    for c in range(1 << m):
        y = 0
        for i in range(m):
            if c >> i & 1: y ^= A[i]
        if y == x: CO[key] = c; return c
R, seed = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed); t0 = time.time(); bestsum = None
for rr in range(R):
    f = {}
    for v in order:
        earlier = [u for u in nb[v] if pos[u] < pos[v]]; ses = [w for w in sv[v] if pos[w] < pos[v]]
        if not earlier:
            while True:
                A = [rng.randrange(1, 1 << n) for _ in range(m)]
                if rank(A) == m: break
            cands = [reduce(A)]
            if ses:   # need complementary to session partners: sample random until ok
                for _ in range(2000):
                    A = [rng.randrange(1, 1 << n) for _ in range(m)]
                    if rank(A) == m and all(dist(A, f[w]) == m for w in ses): cands = [reduce(A)]; break
        else:
            base = f[rng.choice(earlier)]; cands = list(neighbours(base)); rng.shuffle(cands)
        bestc = None
        for C in cands[:4000]:
            far = sum(1 for u in earlier if dist(C, f[u]) > 1); bad = sum(1 for w in ses if dist(C, f[w]) < m)
            sc = (bad, far, sum(dist(C, f[u]) for u in earlier))
            if bestc is None or sc < bestc[0]: bestc = (sc, C)
            if sc[0] == 0 and sc[1] == 0: break
        f[v] = bestc[1]
    esum = sum(dist(f[u], f[v]) for u, v in E); sok = sum(1 for s, t in S if dist(f[s], f[t]) == m)
    far = sum(1 for u, v in E if dist(f[u], f[v]) > 1)
    print('restart %d: edge sum %d (edges >1: %d), sessions complementary %d/157  %.0fs' % (rr, esum, far, sok, time.time() - t0), flush=True)
    if sok == 157 and (bestsum is None or esum < bestsum): bestsum = esum; pickle.dump(f, open('greedy_s%d.pkl' % seed, 'wb'))
print('best edge sum with all sessions complementary:', bestsum, '(routing bill 785)')
