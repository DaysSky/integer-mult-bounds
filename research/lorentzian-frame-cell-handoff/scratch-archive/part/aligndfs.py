import sys, pickle, random, time, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V
good = pickle.load(open('good4.pkl', 'rb')); n = len(good)
comp = pickle.load(open('compat.pkl', 'rb'))
C = np.zeros((n, n), dtype=bool)
for i, js in enumerate(comp): C[i, js] = True
F = np.array(good)
inc = [np.zeros(n, dtype=bool) for _ in range(V)]
for i, q in enumerate(good):
    for x in q: inc[x][i] = True
seed = int(sys.argv[1]); rng = random.Random(seed); T = float(sys.argv[2])
best = (0, None); t0 = time.time(); nodes = 0
def dfs(cand, covered, chosen, punct):
    global best, nodes
    nodes += 1
    if time.time() - t0 > T: return True
    ncov = len(covered)
    if ncov - punct > best[0]:
        best = (ncov - punct, list(chosen)); print('covered', ncov - punct, 'frames', len(chosen), 'punct', punct, 'nodes', nodes, round(time.time() - t0, 1), flush=True)
        if ncov - punct >= 216: return True
    free = [x for x in range(V) if x not in covered]
    # line with fewest candidates
    opts = []
    for x in free:
        cx = np.nonzero(cand & inc[x])[0]
        opts.append((len(cx), x, cx))
    opts.sort(key=lambda z: z[0])
    k, x, cx = opts[0]
    if k == 0:
        if punct >= 4: return False
        # puncture x
        covered.add(x)
        r = dfs(cand & ~inc[x], covered, chosen, punct + 1)
        covered.discard(x); return r
    cx = list(cx); rng.shuffle(cx)
    for i in cx[:3]:
        q = good[i]
        newc = cand & C[i]
        for y in q: covered.add(y)
        chosen.append(i)
        if dfs(newc, covered, chosen, punct): return True
        chosen.pop()
        for y in q: covered.discard(y)
    return False
dfs(np.ones(n, dtype=bool), set(), [], 0)
print('best covered', best[0], 'nodes', nodes)
pickle.dump(best, open('align_best_%d.pkl' % seed, 'wb'))
