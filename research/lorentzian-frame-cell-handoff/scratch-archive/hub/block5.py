"""Z5-symmetric 5-point block: Z = {0..4}, frames F_h = {P(h+1,h+4), P(h+2,h+3), T(h,h+1,h+4), T(h,h+2,h+3)};
express Q = Phi-perp and all E-sets as unions of W-atoms (W = {5..10}) plus Z-lines."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
Z = list(range(5)); W = list(range(5, 11))
orthm = [sum(1 << j for j in range(V) if j != i and G[i, j] == 0) for i in range(V)]
bits = lambda m: [i for i in range(V) if m >> i & 1]
def atom(x):
    k, s = g.kind[x], g.supp[x]
    zs = tuple(sorted(i for i in s if i in Z))
    if len(zs) == len(s): return ('Z', g.kind[x] + ''.join(map(str, s)))
    return (k, zs)            # e.g. ('P', ()) = P(W), ('T', (3,)) = T(3|W), ('T',(1,2)) = T(12|W), ('P',(2,)) = P(2|W)
def name(a):
    if a[0] == 'Z': return a[1]
    return '%s(%s|W)' % (a[0], ''.join(map(str, a[1]))) if a[1] else '%s(W)' % a[0]
def decomp(m):
    cnt = collections.Counter(atom(x) for x in bits(m))
    full = collections.Counter(atom(x) for x in range(V))
    out = []
    for a, c in sorted(cnt.items()):
        if a[0] == 'Z': out.append(name(a))
        elif c == full[a]: out.append(name(a))
        else: out.append('%s[%d/%d]' % (name(a), c, full[a]))
    return out
F = {}
for h in Z:
    a, b, c, d = (h + 1) % 5, (h + 4) % 5, (h + 2) % 5, (h + 3) % 5
    F[h] = [g.P(a, b), g.P(c, d), g.T(h, a, b), g.T(h, c, d)]
nm = lambda x: g.kind[x] + ''.join(map(str, g.supp[x]))
cov = sorted(x for f in F.values() for x in f)
print('covers all 20 Z-lines:', cov == sorted(x for x in range(V) if all(i in Z for i in g.supp[x])))
for h in [0]:
    f = F[h]; print('frame F_%d' % h, [nm(x) for x in f])
    Q = orthm[f[0]] & orthm[f[1]] & orthm[f[2]] & orthm[f[3]]
    print('  Q =', ' + '.join(decomp(Q)))
    for t, e in itertools.combinations(f, 2):
        o = [x for x in f if x not in (t, e)]
        E = orthm[t] & orthm[e] & ~orthm[o[0]] & ~orthm[o[1]]
        print('  E(%s,%s) [%d] =' % (nm(t), nm(e), bin(E).count('1')), ' + '.join(decomp(E)))
