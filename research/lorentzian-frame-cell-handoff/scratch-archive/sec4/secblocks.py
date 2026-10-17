"""Type of Q-perp ∩ C for each section Q and block C; whether it is a design cell."""
from common import *
D4 = load_d4()
full = [W for W in D4 if len([P for P in planes if P & ~W == 0]) == 12 and len([Q for Q in planes if Q & ~perpmask(W) == 0]) == 12]
blk = {s: k for k, W in enumerate(full) for s in e8.bits(W)}
comp = {k: full.index(perpmask(W)) for k, W in enumerate(full)}
pset = set(planes)
def typ(m):
    n = pc(m); r = e8.dim(m); cl = e8.closure(m)[0]
    return (n, r, 'closed' if cl == m else 'open(%d)' % pc(cl))
st = collections.Counter()
for Q in planes:
    Qp = perpmask(Q); B = blk[e8.bits(Q)[0]]
    for k, C in enumerate(full):
        X = Qp & C
        if not X: continue
        kind = 'own' if k == B or (pc(Q) == 2 and k == blk[e8.bits(Q)[1]]) else ('comp' if k == comp[B] else 'other')
        st[('A2' if pc(Q) == 3 else 'pair', kind, typ(X), X in pset)] += 1
for k, n in sorted(st.items()): print(k, n)
