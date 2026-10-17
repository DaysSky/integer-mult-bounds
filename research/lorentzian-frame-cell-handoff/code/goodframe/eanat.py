import sys, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
pc = lambda m: bin(m).count('1')
orthm = [sum(1 << j for j in range(V) if j != i and G[i, j] == 0) for i in range(V)]
nm = lambda x: g.kind[x] + ''.join('%x' % i for i in g.supp[x])
for q in [(g.P(0,1), g.P(2,3), g.T(0,1,4), g.T(2,3,4)), (g.T(0,1,2), g.T(0,3,4), g.T(1,3,5), g.T(2,4,5))]:
    print('frame', [nm(x) for x in q])
    P = orthm[q[0]] & orthm[q[1]] & orthm[q[2]] & orthm[q[3]]
    print('  perp', pc(P), sorted(nm(x) for x in g.bits(P))[:40])
    for t in q[:1]:
        for e in q:
            if e == t: continue
            o = [x for x in q if x not in (t, e)]
            E = orthm[t] & orthm[e] & ~orthm[o[0]] & ~orthm[o[1]]
            print('  E(%s,%s)' % (nm(t), nm(e)), pc(E), sorted(nm(x) for x in g.bits(E)))
