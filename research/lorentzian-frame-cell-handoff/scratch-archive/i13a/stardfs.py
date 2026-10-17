"""Exact: minimum T punctures for a star-structured aligned partition of I_{13,1} (apex 12, P(12,.) punctured).
Candidates: star frames (apex 12) and TTTT frames on 0..11.  Live lines: 66 P (on 0..11), 66 T through 12, 220 T on
0..11.  WLOG a TTTT frame t0 is in the partition (S_12 transitive; unless all 220 such T lines are punctured).
Iterative deepening on the puncture budget (punctures allowed only on T lines on 0..11; P lines and T(.,.,12) must be
covered since P(12,.) punctures are already spent); force-puncture uncoverable lines; branch on the most constrained."""
import sys, pickle, numpy as np, time
frames, comp_lists, kinds = pickle.load(open('compat13.pkl', 'rb'))
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; Fall = np.array(frames)
supp = lambda l: g.supp[l]
star = [j for j in range(len(frames)) if kinds[j] == 'PPTT' and all(12 in supp(l) for l in Fall[j] if g.kind[l] == 'T')]
tts = [j for j in range(len(frames)) if kinds[j] == 'TTTT' and all(12 not in supp(l) for l in Fall[j])]
cand = star + tts; nc = len(cand); pos = {j: i for i, j in enumerate(cand)}
C = np.zeros((nc, nc), dtype=bool)
for i, j in enumerate(cand):
    arr = comp_lists[j]; sel = arr[np.isin(arr, cand)]
    C[i, [pos[int(k)] for k in sel]] = True
F = Fall[cand]
live = sorted(set(int(l) for q in F for l in q))
lid = {l: i for i, l in enumerate(live)}; NL = len(live)
member = np.zeros((NL, nc), dtype=bool)
for i in range(nc):
    for l in F[i]: member[lid[int(l)], i] = True
punctable = np.array([g.kind[l] == 'T' and 12 not in supp(l) for l in live])
print('candidates', nc, '(star %d, TTTT %d), live lines %d' % (len(star), len(tts), NL), flush=True)
i0 = pos[tts[0]]
nodes = [0]; t0 = time.time()
def dfs(allowed, covered, punct, budget):
    nodes[0] += 1
    if nodes[0] % 20000 == 0: print('   nodes', nodes[0], '%.0fs' % (time.time() - t0), flush=True)
    unc = np.nonzero(~covered)[0]
    if len(unc) == 0: return True
    cnt = (member[unc] & allowed).sum(1)
    zero = unc[cnt == 0]
    if len(zero):
        if not punctable[zero].all() or len(zero) > budget - punct: return False
        cov2 = covered.copy(); cov2[zero] = True
        return dfs(allowed, cov2, punct + len(zero), budget)
    k = int(np.argmin(cnt)); u = unc[k]
    for j in np.nonzero(member[u] & allowed)[0]:
        a2 = allowed & C[j]; a2 &= ~member[[lid[int(l)] for l in F[j]]].any(0)
        cov2 = covered.copy(); cov2[[lid[int(l)] for l in F[j]]] = True
        if dfs(a2, cov2, punct, budget): return True
    if punctable[u] and punct < budget:
        cov2 = covered.copy(); cov2[u] = True
        if dfs(allowed, cov2, punct + 1, budget): return True
    return False
allowed = C[i0].copy(); allowed &= ~member[[lid[int(l)] for l in F[i0]]].any(0)
covered = np.zeros(NL, dtype=bool); covered[[lid[int(l)] for l in F[i0]]] = True
for budget in range(0, int(sys.argv[1]) + 1):
    nodes[0] = 0
    ok = dfs(allowed, covered, 0, budget)
    print('T-puncture budget %d: feasible=%s nodes %d %.0fs' % (budget, ok, nodes[0], time.time() - t0), flush=True)
    if ok: break
