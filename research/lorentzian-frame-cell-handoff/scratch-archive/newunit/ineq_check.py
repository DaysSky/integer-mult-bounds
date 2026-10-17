# Check (F3) |N[t]|avg >= (v - 2^(w/2))/2 (odd-or-zero, w = F2 rank of Gram mod 2) and the realisability bounds
# (F1) Euclidean: sum d >= 4(v-h)^2/h + 4(v-h);  (F2) Lorentzian: sum d >= 4(v-h+1)^2/(h-1) + 4(v-h+1)
# (d_t = number of non-orthogonal partners, products in {0,+-1}, norms 2).  Also the O^-(8,2) nonsingular graph.
import sys, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
from smallsys import roots, gram
def f2rank(M):
    M = (np.array(M) % 2).astype(np.uint8).copy(); r = 0; rows, cols = M.shape
    for c in range(cols):
        p = [i for i in range(r, rows) if M[i, c]]
        if not p: continue
        M[[r, p[0]]] = M[[p[0], r]]
        for i in range(rows):
            if i != r and M[i, c]: M[i] ^= M[r]
        r += 1
        if r == rows: break
    return r
def report(name, G, h, lorentz):
    v = len(G); w = f2rank(G % 2); N = [(G[t] == 0).sum() + 1 for t in range(v)]   # closed nbhd (diag != 0)
    d = [(G[t] != 0).sum() - 1 for t in range(v)]; D = sum(d)
    f3 = (v - 2 ** (w / 2)) / 2
    f1 = 4 * (v - h) ** 2 / h + 4 * (v - h); f2 = 4 * (v - h + 1) ** 2 / (h - 1) + 4 * (v - h + 1)
    print('%-8s v %3d h %2d w %2d | avg |N[t]| %.1f >= F3 %.1f | D %d  F1 %.0f  F2 %.0f (%s)' % (name, v, h, w, np.mean(N), f3, D, f1, f2, 'Lorentzian' if lorentz else 'Euclidean'))
R, sc = roots('E8'); G, A = gram(R, sc); report('E8', G, 8, False)
report('I11', np.array(g.G).astype(int), 11, True)
# O^-(8,2): quadratic form q on F2^8 of minus type: q = x1x2 + x3x4 + x5x6 + x7^2 + x7x8 + x8^2
def q(x): return (x[0]*x[1] + x[2]*x[3] + x[4]*x[5] + x[6] + x[6]*x[7] + x[7]) % 2
def B(x, y): return (q([(a + b) % 2 for a, b in zip(x, y)]) + q(x) + q(y)) % 2
pts = [x for x in itertools.product((0, 1), repeat=8) if any(x) and q(x) == 1]
n = len(pts); deg = [sum(B(a, b) for b in pts) for a in pts]
print('O^-(8,2) nonsingular points', n, 'B=1 degree', sorted(set(deg)))
D = sum(deg)
for h in (9, 10, 11, 12):
    f2 = 4 * (n - h + 1) ** 2 / (h - 1) + 4 * (n - h + 1)
    print('  h', h, 'D', D, 'F2 bound', round(f2), 'realisable?' , D >= f2)
