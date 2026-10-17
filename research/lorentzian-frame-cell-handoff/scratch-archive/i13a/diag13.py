"""Diagnostic for the PG(2,3) Z13 partition of I_{13,1} vs E8: for each line u, the demands containing u (frame
Q-parts and E-sets of other frames), the fraction containing a frame-mate of u, and a greedy cover size."""
import sys, pickle, itertools, collections, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; G = g.G
part = pickle.load(open('pg23_partition.pkl', 'rb'))
orth = (G == 0); np.fill_diagonal(orth, False)
OM = [sum(1 << j for j in range(V) if orth[i, j]) for i in range(V)]
frame_of = {u: f for f in part for u in f}
dem = []
for f in part:
    dem.append(('Q', f, OM[f[0]] & OM[f[1]] & OM[f[2]] & OM[f[3]]))
    for a, b in itertools.combinations(range(4), 2):
        o = [z for z in range(4) if z not in (a, b)]
        dem.append(('E', f, OM[f[a]] & OM[f[b]] & ~OM[f[o[0]]] & ~OM[f[o[1]]]))
stats = collections.Counter(); fr = []; greedy = []
for u in range(V):
    mates = [x for x in frame_of[u] if x != u]
    Du = [d for d in dem if d[2] >> u & 1]
    hit = sum(1 for d in Du if any(d[2] >> m & 1 for m in mates))
    fr.append(hit / len(Du))
    # greedy set cover with partners
    unc = set(range(len(Du))); cnt = 0
    while unc:
        best = max(range(V), key=lambda v: sum(1 for i in unc if Du[i][2] >> v & 1) if v != u else -1)
        cov = {i for i in unc if Du[i][2] >> best & 1}
        if not cov: cnt += len(unc); break
        unc -= cov; cnt += 1
    greedy.append(cnt)
    stats[(g.kind[u], len(Du))] += 1
print('demands per line (kind, count):', dict(stats))
print('fraction of a line\'s demands containing a frame-mate: mean %.3f min %.3f max %.3f' % (np.mean(fr), min(fr), max(fr)))
print('greedy cover size per line: mean %.2f min %d max %d' % (np.mean(greedy), min(greedy), max(greedy)), sorted(collections.Counter(greedy).items()))
