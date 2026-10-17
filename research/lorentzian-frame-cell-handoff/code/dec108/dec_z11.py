"""Z11-cyclic sub-110 decoder search (C_11-containment form).  Frames F_k = sigma^k F_0 (k = 0..10), F_0 a rank-9
section {p,q}-perp (orbit representatives), plus the invariant frame z3-perp (rank 10, all 55 P lines).
Columns a_k = rot^k(a_0) and a_12 in {all-ones, e-vectors?}.  cost 99 + 10 = 109.  Condition per line u:
label(u) in span{a_k : u in F_k} (+ a_12 if u is a P line).  By Z11 symmetry it suffices to check orbit reps."""
import sys, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
idx = {(g.kind[i], g.supp[i]): i for i in range(V)}
def shift(u, j):
    s = tuple(sorted((x + j) % 11 for x in g.supp[u])); return idx[(g.kind[u], s)]
label = [g.binlabel(u) for u in range(V)]
rot = lambda a, k: ((a << k) | (a >> (11 - k))) & 0x7FF
# check label shifting convention: label(shift(u,1)) == rot(label(u),1)?
conv = all(label[shift(u, 1)] == rot(label[u], 1) for u in range(V))
print('label shift convention ok:', conv, flush=True)
OM = [0] * V
for i in range(V):
    for j in range(V):
        if i != j and G[i, j] == 0: OM[i] |= 1 << j
reps = []; seen = set()
for u in range(V):
    if u in seen: continue
    reps.append(u)
    for j in range(11): seen.add(shift(u, j))
secs = {}
for p in range(V):
    for q in range(p + 1, V):
        if G[p, q] == 0:
            m = OM[p] & OM[q]
            key = min(sum(1 << shift(u, j) for u in range(V) if m >> u & 1) for j in range(11))
            secs.setdefault(key, m)
print('line orbit reps', len(reps), 'section orbits', len(secs), flush=True)
def inspan(x, vecs):
    basis = []
    for v in vecs:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    for b in basis: x = min(x, x ^ b)
    return x == 0
found = 0
for si, (key, m0) in enumerate(secs.items()):
    # memb[u] = list of k with u in sigma^k F0  <=>  shift(u, -k) in F0
    memb = {u: [k for k in range(11) if m0 >> shift(u, (11 - k) % 11) & 1] for u in reps}
    for a12 in (0x7FF, 0):
        for a0 in range(1, 1 << 11):
            ok = True
            for u in reps:
                vs = [rot(a0, k) for k in memb[u]]
                if g.kind[u] == 'P': vs.append(a12)
                if not inspan(label[u], vs): ok = False; break
            if ok:
                found += 1; print('FOUND section orbit', si, 'a0', bin(a0), 'a12', bin(a12), flush=True)
    if si % 100 == 0: print('section orbit', si, 'found so far', found, flush=True)
print('done, found', found)
