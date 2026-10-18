"""Trivial per-block lower bound on extras: live B-lines needed by the taus' Np (union) minus the best single-line coverage
(one fk line per non-dual pair, freed lines)."""
import sys,itertools
sys.path.insert(0,'.')
from fastb import *
P=[10,15,51,53,56,66,72,89,111]
for B in range(10):
    bk=Blk(B,P)
    if not bk.taus: continue
    U=0
    for p in bk.taus: U|=bk.Np0[p]
    need=set(bits(U))
    cov=set(bk.freed)
    pairsB=[set(c) for c in bk.cells]
    best=max(len(need & (cov|set(ch))) for ch in itertools.product(*[list(c) for c in bk.cells]))
    print('B',B,'taus',bk.taus,'|Np|',[bin(bk.Np0[p]).count('1') for p in bk.taus],'union',len(need),'freed',bk.freed,'cells',bk.cells,'LB',len(need)-best)
