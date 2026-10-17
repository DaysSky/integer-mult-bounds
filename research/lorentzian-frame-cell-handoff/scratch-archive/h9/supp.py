"""Exact support-level bound for lines in R^{8,1} containing an orthogonal 8-frame (see cand.py).
Per class, lines are grouped by support; same-support patterns are bounded by Kleitman (diameter <= 3 in Q_k):
k=4: 8 (all sign classes), k=5: 10, k=6: 12, k=7: 14, k=8: 16.  Support compatibility (parity of products):
 k4-k4: |T n T'| even;  A: k6-k6 |S n S'| even, k4-k6 |T n S| even;  B1: k5-k5 |S n S'| odd, k4-k5 |T n S| even;
 B2: k8 vs k4 fine (parity), k5-k8 impossible;  C: k7-k7 equal supports only, k4-k7 T inside S.
Maximise 8|F4| + c_k |Fk| over compatible families (exhaustive max-weight clique on supports)."""
import itertools, networkx as nx
P = range(8)
def best(k, ck, kk_ok, k4_ok):
    S4 = [frozenset(c) for c in itertools.combinations(P, 4)]
    Sk = [frozenset(c) for c in itertools.combinations(P, k)]
    G = nx.Graph(); nodes = [('4', s) for s in S4] + [('k', s) for s in Sk]
    w = {('4', s): 8 for s in S4}; w.update({('k', s): ck for s in Sk})
    for n in nodes: G.add_node(n, weight=w[n])
    for a, b in itertools.combinations(nodes, 2):
        if a[0] == '4' and b[0] == '4': ok = len(a[1] & b[1]) % 2 == 0
        elif a[0] == 'k' and b[0] == 'k': ok = kk_ok(a[1], b[1])
        else:
            t, s = (a[1], b[1]) if a[0] == '4' else (b[1], a[1]); ok = k4_ok(t, s)
        if ok: G.add_edge(a, b)
    # max weight clique with at least one k-support: fix one k-support (symmetry: all k-sets equivalent under S8)
    s0 = Sk[0]; H = G.subgraph([s0 and ('k', s0)] + list(G.neighbors(('k', s0)))).copy()
    c, wt = nx.max_weight_clique(H, weight='weight')
    n4 = sum(1 for x in c if x[0] == '4'); nk = sum(1 for x in c if x[0] == 'k')
    return wt, n4, nk
res = {}
res['A (k4,k6)'] = best(6, 12, lambda s, t: len(s & t) % 2 == 0, lambda t, s: len(t & s) % 2 == 0)
res['B1 (k4,k5)'] = best(5, 10, lambda s, t: len(s & t) % 2 == 1, lambda t, s: len(t & s) % 2 == 0)
res['C (k4,k7)'] = best(7, 14, lambda s, t: s == t, lambda t, s: t <= s)
for k, (wt, n4, nk) in res.items():
    print('%-11s max 8|F4| + c|Fk| = %d (|F4| %d, |Fk| %d) -> total lines <= %d' % (k, wt, n4, nk, 8 + wt))
