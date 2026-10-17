"""S11 orbits of the maximal non-orthogonal cliques of I_{11,1} (sizes 10 and 9), via flats.canon."""
import sys, pickle, collections, time
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp')
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
import networkx as nx
import flats
G = g.G
H = nx.Graph(); H.add_nodes_from(range(V))
H.add_edges_from((i, j) for i in range(V) for j in range(i + 1, V) if G[i, j] != 0)
t = time.time()
cl = [tuple(sorted(c)) for c in nx.find_cliques(H) if len(c) >= 9]
orb = collections.defaultdict(list)
for c in cl: orb[flats.canon(c)].append(c)
print('cliques', len(cl), 'orbits', len(orb), '%.0fs' % (time.time() - t), flush=True)
for k, v in sorted(orb.items(), key=lambda kv: (-len(kv[1][0]), -len(kv[1]))):
    c = v[0]
    print('  size %d orbit %d  types %s' % (len(c), len(v), sorted(collections.Counter(g.kind[x] for x in c).items())), flush=True)
pickle.dump(dict(orb), open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/corbits.pkl', 'wb'))
