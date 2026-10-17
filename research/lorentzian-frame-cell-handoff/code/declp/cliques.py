"""All maximum pairwise non-orthogonal cliques (size 10) of I_{11,1}; orbit split by line-type pattern."""
import sys, collections, pickle, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
import networkx as nx
G = g.G
H = nx.Graph(); H.add_nodes_from(range(V))
H.add_edges_from((i, j) for i in range(V) for j in range(i + 1, V) if G[i, j] != 0)
t = time.time(); sizes = collections.Counter(); C10 = []
for c in nx.find_cliques(H):
    sizes[len(c)] += 1
    if len(c) == 10: C10.append(tuple(sorted(c)))
print('maximal clique sizes', sorted(sizes.items()), 'time %.0fs' % (time.time() - t), flush=True)
typ = collections.Counter(tuple(sorted(collections.Counter(g.kind[x] for x in c).items())) for c in C10)
print('10-cliques', len(C10), 'by type', typ, flush=True)
pickle.dump(C10, open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/C10.pkl', 'wb'))
