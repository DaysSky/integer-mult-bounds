"""Is the frame + support-4 part of O^-(8,2)'s nonsingular configuration (w.r.t. a Lagrangian holding 8 nonsingular
points) isomorphic, as an orthogonality graph, to E8's (O^+ nonsingular)?  Also: for each support-8 point, how many
of the 120 are omega-orthogonal to it."""
import itertools, networkx as nx, numpy as np, collections
n = 4
def omega(a, b): return sum(((a >> (2 * i)) & 1) * ((b >> (2 * i + 1)) & 1) + ((a >> (2 * i + 1)) & 1) * ((b >> (2 * i)) & 1) for i in range(n)) % 2
def Q(a, eps):
    s = 0
    for i in range(n):
        x, y = (a >> (2 * i)) & 1, (a >> (2 * i + 1)) & 1
        s += x * y if (eps == '+' or i < n - 1) else (x + x * y + y)
    return s % 2
def graph(pts):
    G = nx.Graph(); G.add_nodes_from(range(len(pts)))
    G.add_edges_from((i, j) for i in range(len(pts)) for j in range(i + 1, len(pts)) if omega(pts[i], pts[j]) == 0)
    return G
mpts = [a for a in range(1, 256) if Q(a, '-') == 1]
ppts = [a for a in range(1, 256) if Q(a, '+') == 1]
# find a Lagrangian (4-dim omega-isotropic subspace) with 8 nonsingular points
def span(gens):
    S = {0}
    for g in gens: S |= {s ^ g for s in S}
    return S
found = None
for gens in itertools.combinations(mpts, 4):
    if any(omega(a, b) for a, b in itertools.combinations(gens, 2)): continue
    L = span(gens)
    if len(L) != 16: continue
    ns = [x for x in L if x and Q(x, '-') == 1]
    if len(ns) == 8: found = L; break
L = found
def supp(x): return sum(1 for l in L if l and Q(l, '-') == 1 and omega(x, l) == 1)
frame = [x for x in L if x and Q(x, '-') == 1]
s4 = [x for x in mpts if x not in L and supp(x) == 4]; s8 = [x for x in mpts if x not in L and supp(x) == 8]
print('frame', len(frame), 'support-4', len(s4), 'support-8', len(s8), flush=True)
G120 = graph(frame + s4); GE8 = graph(ppts)
ev = lambda G: np.round(np.linalg.eigvalsh(nx.to_numpy_array(G)), 6)
print('degree seqs', sorted(collections.Counter(d for _, d in G120.degree()).items()), sorted(collections.Counter(d for _, d in GE8.degree()).items()))
print('same spectrum:', np.allclose(ev(G120), ev(GE8)), flush=True)
iso = nx.is_isomorphic(G120, GE8)
print('isomorphic to E8 orthogonality graph:', iso, flush=True)
sub = frame + s4
for w in s8[:3]:
    perp = [x for x in sub if omega(w, x) == 0]
    print('support-8 point: omega-orthogonal to %d of the 120' % len(perp), flush=True)
