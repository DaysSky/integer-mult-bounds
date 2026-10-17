import sys, pickle, itertools, collections, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V, nondegenerate, closure, dim
HYP = g.HYP
def pm(m):
    r = g.FULL
    for s in bits(m): r &= HYP[s]
    return r
B2 = lambda x, y: (1 << x) | (1 << y)
frames, pun = pickle.load(open('/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/goodframe/goodpart.pkl', 'rb'))
L = g.L.astype(float)
def rk(m):
    b = bits(m)
    return np.linalg.matrix_rank(L[b]) if b else 0
seen = collections.Counter()
for q in frames[:12]:
    t, a, b, c = q
    U = B2(t, a) | B2(b, c); Q = pm(U)
    out = [''.join(g.kind[x] for x in q), 'Q', bin(Q).count('1'), rk(Q), nondegenerate(closure(Q))]
    for x, y in itertools.combinations(q, 2):
        Exy = pm(B2(x, y)) & ~Q & ~U
        cl = closure(Exy)
        out.append('E%s%s:%d r%d cl%d nd%d' % (g.kind[x], g.kind[y], bin(Exy).count('1'), rk(Exy), bin(cl).count('1'), nondegenerate(cl)))
    print(*out)
