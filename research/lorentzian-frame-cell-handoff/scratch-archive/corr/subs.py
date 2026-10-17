"""For each E8 root line T, the line-spanned subspaces W of T^perp of a given type, as line sets lines(W).
usage: subs.py TYPE  with TYPE in D4 (orth 4-frame span, 12 lines), A4 (4-chain, 10 lines), A3 (3-chain, 6 lines),
D5 (span with 20 lines), E6 (36 lines), D6 (30 lines).  Membership via Gram projection (exact rationals not needed:
small integers, tolerance)."""
import pickle, itertools, sys, numpy as np
d=pickle.load(open('../k2/e8f.pkl','rb')); G=d['GL'].astype(float); n=120
def lines_in_span(basis):
    B=list(basis); Gb=G[np.ix_(B,B)]; Gi=np.linalg.inv(Gb)
    P=G[:,B]; q=np.einsum('ij,jk,ik->i',P,Gi,P)
    return frozenset(np.nonzero(np.abs(q-2.0)<1e-6)[0].tolist())
typ=sys.argv[1]
want={'D4':12,'A4':10,'A3':6,'D5':20,'E6':36,'D6':30}[typ]; dim={'D4':4,'A4':4,'A3':3,'D5':5,'E6':6,'D6':6}[typ]
res={}
for T in range(n):
    E=[S for S in range(n) if G[T,S]==0]
    Ws=set(); covered=set()
    # grow independent sets greedily via DFS over increasing indices, pruning by rank
    def rec(basis,start):
        if len(basis)==dim:
            W=lines_in_span(basis)
            if len(W)==want: Ws.add(W)
            return
        for i in range(start,len(E)):
            S=E[i]
            nb=basis+[S]
            if np.linalg.matrix_rank(G[np.ix_(nb,nb)])<len(nb): continue
            if len(nb)>=2:
                W=lines_in_span(nb)
                # canonical: only extend if nb are the lexicographically-first basis? cheap prune: skip if S not min new
            rec(nb,i+1)
    if dim<=4:
        rec([],0)
    else:
        # higher dims: extend each found (dim-1)-subspace candidate is expensive; use complement trick:
        # W of dim d in T^perp  <->  W^perp (in R^8) of dim 8-d containing T.
        cod=8-dim; Ws2=set()
        others=[S for S in range(n) if S!=T]
        for comb in itertools.combinations(others,cod-1):
            B=[T]+list(comb)
            if np.linalg.matrix_rank(G[np.ix_(B,B)])<cod: continue
            perp=frozenset(S for S in range(n) if all(G[S,b]==0 for b in B))
            if len(perp)==want: Ws2.add(perp)
        Ws=Ws2
    res[T]=sorted(Ws,key=sorted)
    if T%10==0: print(T,len(Ws),flush=True)
print('per-line counts',sorted(set(len(v) for v in res.values())))
pickle.dump(res,open('subs_%s.pkl'%typ,'wb'))
