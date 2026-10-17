"""Exact minimum number of punctured lines for an aligned good-frame partition of I_{13,1} (frames: full-system good
frames; compatibility is unaffected by punctures since frames contain only live lines).
WLOG f0 = first PPTT frame is in the partition, unless every P line ... (case B: P(01) punctured is handled by
running with the root branch 'puncture P(01)' too).  Iterative deepening on the budget k; at each node every uncovered
line with no allowed frame is force-punctured; branch on the uncovered line with fewest allowed frames: its frames, or
puncture it."""
import sys, pickle, numpy as np, time
frames, comp_lists, kinds = pickle.load(open('compat13.pkl', 'rb'))
F = np.array(frames); nf = len(F); V = 364
C = np.zeros((nf, nf), dtype=bool)
for i, js in enumerate(comp_lists): C[i, js] = True
member = np.zeros((V, nf), dtype=bool)
for j in range(nf): member[F[j], j] = True
f0 = next(i for i in range(nf) if kinds[i] == 'PPTT')
nodes = [0]; t0 = time.time()
def dfs(allowed, covered, punct, budget):
    nodes[0] += 1
    if nodes[0] % 50000 == 0: print('  nodes', nodes[0], '%.0fs' % (time.time() - t0), flush=True)
    unc = np.nonzero(~covered)[0]
    if len(unc) == 0: return True
    cnt = (member[unc] & allowed).sum(1)
    zero = unc[cnt == 0]
    if len(zero) > budget - punct: return False
    if len(zero):
        cov2 = covered.copy(); cov2[zero] = True
        return dfs(allowed, cov2, punct + len(zero), budget)
    k = int(np.argmin(cnt)); u = unc[k]
    for j in np.nonzero(member[u] & allowed)[0]:
        a2 = allowed & C[j]; a2 &= ~member[F[j]].any(0)
        cov2 = covered.copy(); cov2[F[j]] = True
        if dfs(a2, cov2, punct, budget): return True
    if punct < budget:
        cov2 = covered.copy(); cov2[u] = True
        if dfs(allowed, cov2, punct + 1, budget): return True
    return False
root_allowed = C[f0].copy(); root_allowed &= ~member[F[f0]].any(0)
root_cov = np.zeros(V, dtype=bool); root_cov[F[f0]] = True
for budget in range(0, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 40):
    nodes[0] = 0
    ok = dfs(root_allowed, root_cov, 0, budget)
    print('budget %d (frame f0 included): feasible=%s nodes %d %.0fs' % (budget, ok, nodes[0], time.time() - t0), flush=True)
    if ok: break
