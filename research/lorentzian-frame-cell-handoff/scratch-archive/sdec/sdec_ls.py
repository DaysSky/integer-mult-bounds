# Local search for a rank-c decoder B = U W^T over F2 for I_{11,1} with B_tt = 1, B_ts = 0 on non-orthogonal pairs,
# minimising total row weight (sum |c_t|).  Objective = BIG * violations + weight.  Moves: flip one bit of U or W.
# A found decoder is checked exactly at the end.  Heuristic search (no optimality claim).
import sys, numpy as np, time, random
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
c = int(sys.argv[1]); T = float(sys.argv[2]); seed = int(sys.argv[3]); mode = sys.argv[4] if len(sys.argv) > 4 else 'b0'
rng = np.random.default_rng(seed); R = random.Random(seed)
NON = (g.G != 0); np.fill_diagonal(NON, False)       # non-orthogonal pairs: B must be 0
ORTH = (g.G == 0); np.fill_diagonal(ORTH, False)
lab = np.array([[(g.binlabel(t) >> i) & 1 for i in range(11)] for t in range(V)], dtype=np.uint8)
if mode == 'b0':
    U = np.zeros((V, c), np.uint8); W = np.zeros((V, c), np.uint8); U[:, :11] = lab; W[:, :11] = lab
else:
    U = rng.integers(0, 2, (V, c), dtype=np.uint8); W = rng.integers(0, 2, (V, c), dtype=np.uint8)
BIG = 50
def score(B):
    viol = int((B & NON).sum()) + int((B.diagonal() == 0).sum())
    wt = int((B & ORTH).sum())
    return viol, wt
B = (U.astype(np.int32) @ W.T.astype(np.int32)) % 2; B = B.astype(np.uint8)
viol, wt = score(B); cur = BIG * viol + wt; best = (viol, wt, U.copy(), W.copy()); t0 = time.time(); it = 0
temp = 2.0
while time.time() - t0 < T:
    it += 1
    if R.random() < 0.5:
        t = R.randrange(V); j = R.randrange(c)
        U[t, j] ^= 1
        newrow = (W.astype(np.int32) @ U[t].astype(np.int32)) % 2      # B[t, :] = U[t] . W[s]
        oldrow = B[t].copy(); B[t] = newrow
        v2, w2 = score(B); new = BIG * v2 + w2
        if new <= cur or R.random() < np.exp((cur - new) / temp): cur, viol, wt = new, v2, w2
        else: U[t, j] ^= 1; B[t] = oldrow
    else:
        s = R.randrange(V); j = R.randrange(c)
        W[s, j] ^= 1
        newcol = (U.astype(np.int32) @ W[s].astype(np.int32)) % 2
        oldcol = B[:, s].copy(); B[:, s] = newcol
        v2, w2 = score(B); new = BIG * v2 + w2
        if new <= cur or R.random() < np.exp((cur - new) / temp): cur, viol, wt = new, v2, w2
        else: W[s, j] ^= 1; B[:, s] = oldcol
    if viol == 0 and (best[0] > 0 or wt < best[1]): best = (viol, wt, U.copy(), W.copy())
    if it % 20000 == 0:
        temp = max(0.2, temp * 0.97)
        print('it', it, 'viol', viol, 'weight', wt, 'best valid weight', best[1] if best[0] == 0 else None, '%.0fs' % (time.time() - t0), flush=True)
v0, w0, U0, W0 = best
B = (U0.astype(np.int32) @ W0.T.astype(np.int32)) % 2
ok = all(B[t, t] == 1 for t in range(V)) and not (B.astype(bool) & NON).any()
print('FINAL best valid' if ok else 'FINAL no valid', 'weight', int((B.astype(bool) & ORTH).sum()), '(B0 26070)')
np.save('sdec_c%d_s%d.npy' % (c, seed), np.hstack([U0, W0]))
