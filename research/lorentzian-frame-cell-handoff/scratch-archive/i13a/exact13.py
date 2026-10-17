"""Exact search: does I_{13,1} admit an aligned good-frame partition (no punctures)?
WLOG it contains f0 = {P(01), P(23), T(014), T(234)}: every partition contains a PPTT frame (P lines lie only in PPTT
frames) and S_13 is transitive on PPTT frames.  DFS: pick the uncovered line with the fewest allowed frames (allowed =
disjoint from chosen lines and compatible with every chosen frame), branch over them.  Exhaustive; logs node counts.
Optional depth/node limit for reporting progress."""
import sys, pickle, numpy as np, time
frames, comp_lists, kinds = pickle.load(open('compat13.pkl', 'rb'))
F = np.array(frames); nf = len(F); V = 364
C = np.zeros((nf, nf), dtype=bool)
for i, js in enumerate(comp_lists): C[i, js] = True
member = np.zeros((V, nf), dtype=bool)
for j in range(nf): member[F[j], j] = True
sys.setrecursionlimit(10000)
f0 = next(i for i in range(nf) if kinds[i] == 'PPTT')
print('f0', f0, F[f0], flush=True)
nodes = [0]; t0 = time.time(); deepest = [0]; maxcov = [0]; sol = [None]
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 10**9
def dfs(allowed, covered, depth, chosen):
    nodes[0] += 1
    if nodes[0] % 20000 == 0:
        print('nodes %d depth %d deepest %d maxcov %d %.0fs' % (nodes[0], depth, deepest[0], maxcov[0], time.time() - t0), flush=True)
    if nodes[0] > LIMIT: raise TimeoutError
    ncov = int(covered.sum()); maxcov[0] = max(maxcov[0], ncov); deepest[0] = max(deepest[0], depth)
    if ncov == V: sol[0] = list(chosen); return True
    unc = np.nonzero(~covered)[0]
    cnt = (member[unc] & allowed).sum(1)
    k = int(np.argmin(cnt))
    if cnt[k] == 0: return False
    u = unc[k]
    for j in np.nonzero(member[u] & allowed)[0]:
        a2 = allowed & C[j]
        a2 &= ~member[F[j]].any(0)
        cov2 = covered.copy(); cov2[F[j]] = True
        chosen.append(j)
        if dfs(a2, cov2, depth + 1, chosen): return True
        chosen.pop()
    return False
allowed = C[f0].copy(); allowed &= ~member[F[f0]].any(0)
covered = np.zeros(V, dtype=bool); covered[F[f0]] = True
try:
    found = dfs(allowed, covered, 1, [f0])
    print('EXHAUSTIVE: aligned partition exists =', found, '; nodes', nodes[0], 'deepest', deepest[0], 'maxcov', maxcov[0], '%.0fs' % (time.time() - t0))
    if found: pickle.dump(sol[0], open('aligned13.pkl', 'wb'))
except TimeoutError:
    print('node limit reached: nodes', nodes[0], 'deepest', deepest[0], 'maxcov', maxcov[0])
