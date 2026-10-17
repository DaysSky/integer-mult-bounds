# All maximum (6-block) edge-disjoint K4 packings of K11, up to isomorphism (exhaustive; first block fixed by symmetry).
import itertools, networkx as nx
P = list(range(11))
K4 = [frozenset(c) for c in itertools.combinations(P, 4)]
E = lambda b: [frozenset(e) for e in itertools.combinations(sorted(b), 2)]
sols = []
def rec(chosen, used, start):
    if len(chosen) == 6: sols.append(list(chosen)); return
    for i in range(start, len(K4)):
        b = K4[i]; es = E(b)
        if any(e in used for e in es): continue
        rec(chosen + [b], used | set(es), i + 1)
rec([K4[0]], set(E(K4[0])), 1)
print('6-packings containing {0,1,2,3}:', len(sols))
def graph(bl):
    G = nx.Graph()
    for p in P: G.add_node(('p', p), t=0)
    for j, b in enumerate(bl):
        G.add_node(('b', j), t=1)
        for p in b: G.add_edge(('p', p), ('b', j))
    return G
reps = []
for s in sols:
    G = graph(s)
    if not any(nx.is_isomorphic(G, H, node_match=lambda a, b: a['t'] == b['t']) for H, _ in reps): reps.append((G, s))
print('non-isomorphic maximum packings:', len(reps))
for _, s in reps:
    deg = sorted((sum(1 for b in s if p in b) for p in P), reverse=True)
    print([sorted(b) for b in s], 'point degrees', deg)
