"""Toy I_{11,1} word demonstrating z-group helpers (format check only, no price ambition).
Groups: timelike ambient vectors z_j (every frame containing z_j is nondegenerate).  Each target t is assigned a
group j with t perp z_j.  Design (direct):
  A: frame-0 branch b[u][j] reads source u at span(u); 11 decoder totals at FULL on frame-0 helpers.
  scatter: B0 labels.
  B: group-j targets climb to span(z_j) and read every group helper they will use while it is still pure
     (group-D); then group helper g[t,u] (starts at span(z_j)) reads b[u][j] at span(u, z_j); then target t reads
     its g[t,u] at t-perp.
  D: frame-0 dirt compensation (computed); C: literal reverse of z-gates at FULL.
usage: zdemo.py OUT.json.gz"""
import sys, os, json, gzip, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; H = 11
BASIS = [g.P(i, i + 1) for i in range(10)] + [g.T(0, 1, 2)]
LB = [[int(x) for x in g.L[b]] for b in BASIS]          # 11 basis vectors in R^12
def coords(x):
    """exact coordinates c (len 11) with sum c_i LB_i = x (x in R^12, in the ambient)"""
    # solve LB^T c = x by Gaussian elimination over Fractions (12 equations, 11 unknowns, consistent)
    A = [[Fr(LB[j][i]) for j in range(11)] + [Fr(x[i])] for i in range(12)]
    r = 0; piv = []
    for c in range(11):
        p = next((i for i in range(r, 12) if A[i][c] != 0), None)
        assert p is not None
        A[r], A[p] = A[p], A[r]; iv = 1 / A[r][c]; A[r] = [a * iv for a in A[r]]
        for i in range(12):
            if i != r and A[i][c] != 0:
                f = A[i][c]; A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(c); r += 1
    assert all(A[i][11] == 0 for i in range(11, 12)), 'not in ambient'
    return [A[i][11] for i in range(11)]
COORD = [[int(v) for v in coords(g.L[s])] for s in range(V)]
eta = [1] * 11 + [-1]
GRAM = [[sum(LB[a][i] * LB[b][i] * eta[i] for i in range(12)) for b in range(11)] for a in range(11)]
def ip12(x, y): return sum(x[i] * y[i] * eta[i] for i in range(12))
# timelike group vectors (b; sum(b)/3), scaled by 3 to be integral
Bs = [(-1, -1, -1, -1, -1, -2, -1, -1, -1, -1, -1), (-1, -3, -3, -3, -3, -1, -3, -3, -3, -1, -3),
      (1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1), (-3, -2, -2, -2, -2, -2, -2, -2, -2, 0, -2)]
Z12 = [[3 * x for x in b] + [sum(b)] for b in Bs]
for z in Z12: assert ip12(z, [1] * 11 + [3]) == 0 and ip12(z, z) < 0
ZC = []
for z in Z12:
    c = coords(z); den = 1
    for x in c: den = den * x.denominator // __import__('math').gcd(den, x.denominator)
    ZC.append([int(x * den) for x in c])
grp = {}
for t in range(V):
    for j, z in enumerate(Z12):
        if ip12(g.L[t], z) == 0: grp[t] = j; break
    assert t in grp, 'uncovered target'
R = [[u for u in range(V) if u != t and g.G[t, u] == 0] for t in range(V)]
# ---------------- frames (explicit vectors in basis coordinates) ----------------
def rref(rows):
    m = [[Fr(x) for x in r] for r in rows]; r = 0
    for c in range(H):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return tuple(tuple(x) for x in m[:r])
frames = {}; flist = []
def fid(rows):
    key = rref(rows) if rows else ()
    if key not in frames:
        frames[key] = len(flist)
        # integral basis rows for JSON
        out = []
        for row in key:
            den = 1
            for x in row: den = den * x.denominator // __import__('math').gcd(den, x.denominator)
            out.append([int(x * den) for x in row])
        flist.append(out)
    return frames[key]
F0 = fid([]); FULL = fid([[1 if i == j else 0 for i in range(H)] for j in range(H)])
LINE = [fid([COORD[s]]) for s in range(V)]
def perp_rows(t):
    # basis of t-perp in coordinates: lines of R(t) span it
    return [COORD[u] for u in R[t]]
TPERP = [fid(perp_rows(t)) for t in range(V)]
ZF = [fid([ZC[j]]) for j in range(4)]
UZ = {}
def uz(u, j):
    if (u, j) not in UZ: UZ[(u, j)] = fid([COORD[u], ZC[j]])
    return UZ[(u, j)]
# ---------------- registers and gates ----------------
nreg = 2 * V
start = [LINE[s] for s in range(V)] + [F0] * V
def helper(sf):
    global nreg
    start.append(sf); nreg += 1; return nreg - 1
need = set()
for t in range(V):
    for u in R[t]: need.add((u, grp[t]))
br = {key: helper(F0) for key in sorted(need)}
tot = [helper(F0) for _ in range(11)]
gh = {}
for t in range(V):
    for u in R[t]: gh[(t, u)] = helper(ZF[grp[t]])
A = []; Bp = []
for (u, j), b in br.items(): A.append([LINE[u], b, [u]])
D10 = []
for i in range(11):
    D10.append([s for s in range(V) if g.binlabel(s) >> i & 1])
    A.append([FULL, tot[i], D10[i]])
scatter = [[i for i in range(11) if g.binlabel(t) >> i & 1] for t in range(V)]
for t in range(V):   # group-D reads (pure), one gate per target at span(z)
    Bp.append([ZF[grp[t]], V + t, [gh[(t, u)] for u in R[t]]])
for t in range(V):
    for u in R[t]: Bp.append([uz(u, grp[t]), gh[(t, u)], [br[(u, grp[t])]]])
for t in range(V): Bp.append([TPERP[t], V + t, [gh[(t, u)] for u in R[t]]])
# D: dirt left in targets (symbolic over helpers)
dv = [0] * nreg
for r in range(2 * V, nreg): dv[r] = 1 << (r - 2 * V)
for _, d, srcs in A:
    for s in srcs: dv[d] ^= dv[s]
for t in range(V):
    for k in scatter[t]: dv[V + t] ^= dv[tot[k]]
for _, d, srcs in Bp:
    for s in srcs: dv[d] ^= dv[s]
D = []
gset = set(gh.values())
for t in range(V):
    m = dv[V + t]; srcs = []
    while m:
        bb = m & -m; r = 2 * V + bb.bit_length() - 1; m ^= bb
        assert r not in gset, 'group helper dirt left for D'
        srcs.append(r)
    if srcs: D.append([F0, V + t, srcs])
Cl = [[FULL, d, s] for F, d, s in reversed(A + Bp) if not (V <= d < 2 * V)]
final = [FULL] * V + [TPERP[t] for t in range(V)] + [FULL] * (nreg - 2 * V)
w = dict(format='bitGen/1+mut', family='I_{11,1} z-group demo', h=H, v=V, R=nreg - 2 * V, lines=COORD,
         form={'num': GRAM, 'den': 1}, frames=flist, start=start, final=final, ret=tot, ret_frames=[FULL] * 11,
         scatter=scatter, D=D, A=A, B=Bp, C=Cl)
with gzip.open(sys.argv[1], 'wt') as fh: json.dump(w, fh)
print('R', nreg - 2 * V, 'branches', len(br), 'group helpers', len(gh), 'frames', len(flist),
      'groups', [sum(1 for t in range(V) if grp[t] == j) for j in range(4)])
