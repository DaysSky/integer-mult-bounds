"""Memory-light version of frcover.py for I_{11,1}: enumerate frames (4 mutually orthogonal lines) as int16, compute
the full-perp odd-incidence weight in chunks (uint8), report the distribution, then solve the min-weight exact cover
by CP-SAT over the frames with weight <= WMAX (exactness of the restriction is reported, not assumed).
usage: frcover2.py WMAX TIME"""
import sys, collections, time, pickle
import numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
from ortools.sat.python import cp_model
G = g.G
WMAX, TL = int(sys.argv[1]), float(sys.argv[2])
P = np.array([[1 if (a != b and G[a, b] == 0) else 0 for b in range(V)] for a in range(V)], dtype=np.uint8)
nbr = [np.nonzero(P[i])[0] for i in range(V)]
nset = [set(x.tolist()) for x in nbr]
fr = []
t0 = time.time()
for a in range(V):
    for b in nbr[a]:
        if b <= a: continue
        ab = nset[a] & nset[b]
        for c in ab:
            if c <= b: continue
            for d in ab & nset[c]:
                if d <= c: continue
                fr.append((a, b, c, d))
F = np.array(fr, dtype=np.int16)
print('frames', len(F), '%.0fs' % (time.time() - t0), flush=True)
w = np.zeros(len(F), dtype=np.int32)
for i0 in range(0, len(F), 50000):
    blk = F[i0:i0 + 50000].astype(np.int64)
    cnt = P[:, blk].sum(axis=2)                       # (V, chunk)
    inF = np.zeros(cnt.shape, dtype=bool)
    for k in range(4): inF[blk[:, k], np.arange(len(blk))] = True
    w[i0:i0 + len(blk)] = ((cnt % 2 == 1) & ~inF).sum(axis=0)
hist = collections.Counter(w.tolist())
print('weight distribution (lowest 12):', sorted(hist.items())[:12], '| min %d mean %.1f max %d' % (w.min(), w.mean(), w.max()), flush=True)
np.savez('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/i11frames.npz', F=F, w=w)
sel = np.nonzero(w <= WMAX)[0]
cover = collections.Counter(int(x) for x in F[sel].ravel())
print('frames with weight <= %d: %d; lines covered by them: %d of %d' % (WMAX, len(sel), len(cover), V), flush=True)
if len(cover) < V: sys.exit(0)
m = cp_model.CpModel(); x = [m.NewBoolVar('') for _ in sel]
byline = collections.defaultdict(list)
for j, f in enumerate(sel):
    for a in F[f]: byline[int(a)].append(x[j])
for a in range(V): m.AddExactlyOne(byline[a])
m.Minimize(sum(int(w[f]) * x[j] for j, f in enumerate(sel)))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(m)
print('I11 exact cover within weight <= %d: %s, total odd incidences %s, bound %s, per target %.2f (+1 own)' % (
    WMAX, sv.StatusName(st), sv.ObjectiveValue(), sv.BestObjectiveBound(), sv.ObjectiveValue() / V if st in (2, 4) else -1), flush=True)
