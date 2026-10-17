"""Hub pairs (Y, X = Y-perp) in I_{11,1}: flats Y of rank 3..5 from closures of 3-4 lines (H55 orbit reps), with
#lines of Y, rank, #lines of X, rank, nondegeneracy.  Report the largest |Y|*|X| and the largest |X| per rank of Y."""
import itertools, random
from lcommon import *
random.seed(1)
seen = set(); rows = []
cands = list(range(V))
for trial in range(60000):
    k = random.choice((3, 4))
    S = random.sample(cands, k)
    m = 0
    for s in S: m |= 1 << s
    Y, r = g.closure(m)
    if r < 3 or r > 5: continue
    c = canon_mask(Y)
    if c in seen: continue
    seen.add(c)
    X = perpmask(Y)
    if not X: continue
    rx = g.dim(X)
    rows.append((pc(Y) * pc(X), pc(Y), r, pc(X), rx, Y))
rows.sort(reverse=True)
print('distinct flats', len(seen))
for prod, ny, r, nx, rx, Y in rows[:12]:
    print('Y lines %d rank %d | X lines %d rank %d | nondeg Y %s | example Y kinds %s' % (ny, r, nx, rx, nondeg_span(Y), collections.Counter(g.kind[s] for s in bits(Y))))
best = {}
for prod, ny, r, nx, rx, Y in rows:
    if r not in best or nx > best[r][0]: best[r] = (nx, ny, rx)
print('largest X per rank of Y:', best)
