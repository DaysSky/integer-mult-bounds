import sys, numpy as np
sys.path.insert(0,'.')
from geo import *
K0=list(range(8)); live=[T for T in range(NL) if T not in K0]
def f2rank(M):
    M=[int(''.join(map(str,r)),2) for r in M]; r=0
    rows=list(M)
    for bit in reversed(range(64)):
        piv=[x for x in rows if (x>>bit)&1]
        if not piv: continue
        p=piv[0]; rows=[x^p if (x>>bit)&1 and x!=p else x for x in rows if x!=p]; r+=1
    return r
from collections import Counter
stats=Counter()
for T in live:
    cand=[S for S in live if S!=T and G[T,S]!=0 and any(G[S,f]!=0 and G[T,f]!=0 for f in K0)]
    V=U9[cand]%2
    dim=f2rank(V.tolist())
    Gr=(V@V.T)%2
    rk=f2rank(Gr.tolist())
    stats[(len(cand),dim,rk)]+=1
print(stats)
print('labels self-dot', set(((U9[T]@U9[T])%2) for T in live))
