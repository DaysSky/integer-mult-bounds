import sys, pickle, collections, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lbuild')
import lw
from lw import g, V, bits, nondegenerate
from fastcl import fclosure
pc = lambda m: bin(m).count('1')
good = pickle.load(open('../part/good4.pkl', 'rb'))
D4 = set()
for q in good:
    m = sum(1 << x for x in q); c = fclosure(m)
    if pc(c) == 12 and lw.dim(c) == 4: D4.add(c)
print('D4 from good frames', len(D4))
D5 = collections.Counter(); ex = {}
for d in D4:
    for l in range(V):
        if d >> l & 1: continue
        c = fclosure(d | (1 << l))
        if pc(c) == 20 and lw.dim(c) == 5 and c not in ex:
            key = (sum(1 for x in bits(c) if g.kind[x] == 'P'), nondegenerate(c))
            ex[c] = key; D5[key] += 1
print('D5 subsystems found (P-count, nondegenerate) -> count:', dict(D5))
pickle.dump(ex, open('d5.pkl', 'wb'))
for key in D5:
    c = next(m for m, k in ex.items() if k == key)
    print(key, sorted((g.kind[x] + ''.join('%x' % i for i in g.supp[x])) for x in bits(c)))
