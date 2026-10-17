import sys, itertools, pickle, collections, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
pc = lambda m: bin(m).count('1')
orthm = [sum(1 << j for j in range(V) if j != i and G[i, j] == 0) for i in range(V)]
good = pickle.load(open('good4.pkl', 'rb'))
st = collections.Counter()
ex = {}
for q in good:
    m = sum(1 << x for x in q)
    cl, d = g.closure(m)
    P = orthm[q[0]] & orthm[q[1]] & orthm[q[2]] & orthm[q[3]]
    clP, dP = g.closure(P) if P else (0, 0)
    key = (tuple(sorted(g.kind[x] for x in q)), pc(cl), d, pc(P), dP, pc(clP))
    st[key] += 1
    ex.setdefault(key, q)
for k, v in sorted(st.items()):
    print(k, v, [(g.kind[x], g.supp[x]) for x in ex[k]])
