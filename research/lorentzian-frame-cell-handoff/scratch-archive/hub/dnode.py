# Exact checks: (1) s-cell perps = D8 nodes; (2) a legal 3-cover of R(P) built from weightings; (3) G_z frames.
import sys, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
P, T = g.P, g.T
def mask(ls): return sum(1 << u for u in ls)
ok = 0
for h in range(11):
    for j, k in itertools.combinations([x for x in range(11) if x != h], 2):
        cell = mask([P(j, k), T(h, j, k)])
        both = g.HYP[P(j, k)] & g.HYP[T(h, j, k)]
        O = [x for x in range(11) if x not in (h, j, k)]
        D8 = mask([P(a, b) for a, b in itertools.combinations(O, 2)] + [T(h, a, b) for a, b in itertools.combinations(O, 2)])
        ok += (both == D8)
print('s-cells whose common perp lines equal D8(h;O):', ok, 'of 495')
# (2) P target P(x,y) with S9 = A7 + B2
x, y = 0, 1
S9 = [p for p in range(11) if p not in (x, y)]
A, B = S9[:7], S9[7:]
def flat(c, s):
    out = []
    for u in bits(g.HYP[P(x, y)]):
        sp = g.supp[u]
        if g.kind[u] == 'P':
            a, b = sp
            if a in (x, y): continue
            if c[a] == c[b]: out.append(u)
        else:
            if x in sp and y in sp:
                m = [p for p in sp if p not in (x, y)][0]
                if c[m] + s == 0: out.append(u)
            elif c[sp[0]] + c[sp[1]] + c[sp[2]] == 0: out.append(u)
    return mask(out)
c1 = {p: (1 if p in A else -2) for p in S9}; c2 = {p: (0 if p in A else (1 if p == B[0] else -1)) for p in S9}; c3 = {p: 1 for p in S9}
Hs = [flat(c1, 2), flat(c2, 0), flat(c3, -1)]
for Hm in Hs:
    cl = closure(Hm)
    print('flat lines', bin(Hm).count('1'), '| closure lines', bin(cl).count('1'), '| dim', dim(Hm), '| nondegenerate', nondegenerate(cl), '| inside R(t)', cl & ~g.HYP[P(x, y)] == 0)
print('union covers R(P):', (Hs[0] | Hs[1] | Hs[2]) == g.HYP[P(x, y)])
# (3) G_z = F(S9 - z) + T(x y k), k in S9 - z
for z in S9[:1]:
    S8 = [p for p in S9 if p != z]
    Gz = mask([u for u in range(V) if set(g.supp[u]) <= set(S8)] + [T(x, y, k) for k in S8])
    cl = closure(Gz)
    print('G_z lines', bin(Gz).count('1'), 'closure', bin(cl).count('1'), 'dim', dim(Gz), 'nondeg', nondegenerate(cl))
