from common import *
import pickle
D4 = load_d4()
full = [W for W in D4 if len([P for P in planes if P & ~W == 0]) == 12 and len([Q for Q in planes if Q & ~perpmask(W) == 0]) == 12]
blk = {s: k for k, W in enumerate(full) for s in e8.bits(W)}
comp = {k: full.index(perpmask(W)) for k, W in enumerate(full)}
A2s = [P for P in planes if pc(P) == 3]
# A3s inside blocks containing >= 1 design A2
A3s = set()
for i, P in enumerate(A2s):
    for P2 in A2s[i+1:]:
        F, r = e8.closure(P | P2)
        if r == 3 and pc(F) == 6: A3s.add(F)
A3s = sorted(A3s)
print('A3s spanned by two design A2s:', len(A3s))
st = collections.Counter(); conj = 0; tot = 0
for A in A3s:
    G = perpmask(A)
    B = blk[e8.bits(A)[0]]
    secs = [Q for Q in A2s if Q & ~A == 0]
    other = G & ~full[comp[B]]
    st[(pc(G), len(secs), tuple(sorted(collections.Counter(blk[s] for s in e8.bits(other)).values())))] += 1
print(st)
for Q in A2s:
    B = blk[e8.bits(Q)[0]]
    mine = [A for A in A3s if Q & ~A == 0]
    for k, C in enumerate(full):
        if k in (B, comp[B]): continue
        tot += 1
        u = 0
        for A in mine: u |= perpmask(A) & C
        if u == perpmask(Q) & C: conj += 1
print('A2 sections: #A3s containing each', collections.Counter(len([A for A in A3s if Q & ~A == 0]) for Q in A2s))
print('conjecture Q-perp ∩ C == union over A3∋Q of (A-perp ∩ C):', conj, 'of', tot)
