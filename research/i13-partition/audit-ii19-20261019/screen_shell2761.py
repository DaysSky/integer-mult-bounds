"""Per-class reach of the full II_{1,9} norm-2 shell used in screen_reach.py (2761 lines, h=10): where its
mean r2 comes from (best partners), whether it has near-twins, and the relay proxy (partner-subsampled)."""
import numpy as np
from collections import Counter
from screen_reach import lorentz_ii19
Lr, F = lorentz_ii19(True); L = np.array(Lr, dtype=np.int64); v = len(L)
G = L @ F @ L.T; O = (G == 0); np.fill_diagonal(O, False); psz = O.sum(1)
cls = ['(%d,%d)' % (l[8] // 2, l[9] // 2) for l in Lr]
nd = (np.outer(np.diag(G), np.diag(G)) - G * G) != 0; np.fill_diagonal(nd, False)
Of = O.astype(np.float32); M = Of @ Of; M[~nd] = -1
best = M.max(1); arg = M.argmax(1); r2 = best / np.maximum(psz, 1)
print('class   n   perp  r2_mean  best-partner classes')
for c in sorted(set(cls), key=lambda c: -cls.count(c)):
    idx = [i for i in range(v) if cls[i] == c]
    print('%-7s %4d %6.1f %7.3f  %s' % (c, len(idx), psz[idx].mean(), r2[idx].mean(), Counter(cls[arg[i]] for i in idx).most_common(2)))
print('lines with a >=90% partner:', int((r2 > 0.9).sum()))
perp = [int(''.join('1' if O[s, t] else '0' for t in range(v))[::-1], 2) for s in range(v)]
relays = 0
for s in range(v):
    cand = np.nonzero(nd[s])[0]; lost = perp[s] & ~perp[int(arg[s])]
    while lost:
        g, u = max((bin(lost & perp[u]).count('1'), u) for u in cand[::7])
        if g == 0: relays += bin(lost).count('1'); break
        relays += 1; lost &= ~perp[u]
print('relay proxy (partner-subsampled, an upper bound): %.2f per line' % (relays / v))
