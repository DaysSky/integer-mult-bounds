import sys, numpy as np, itertools, collections, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V
mode=sys.argv[1] if len(sys.argv)>1 else 'T'
live=[u for u in range(V) if g.kind[u]=='T'] if mode=='T' else list(range(V))
def vec(u):
    x=np.zeros(12)
    if g.kind[u]=='P':
        a,b=sorted(g.supp[u]); x[a]=1; x[b]=-1
    else:
        for i in g.supp[u]: x[i]=1
        x[11]=1
    return x
VV=np.array([vec(u) for u in range(V)]); eta=np.diag([1]*11+[-1])
G=VV@eta@VV.T
n=len(live); idx={u:i for i,u in enumerate(live)}
A=np.zeros((n,n),dtype=np.uint8)
for t in live:
    A[idx[t],idx[t]]=1
    for u in live:
        if u!=t and abs(G[t,u])<1e-9: A[idx[t],idx[u]]^=1
def rowspace(M):
    M=M.copy()%2; r=0; rows,cols=M.shape; piv=[]
    for c in range(cols):
        p=next((i for i in range(r,rows) if M[i,c]),None)
        if p is None: continue
        M[[r,p]]=M[[p,r]]
        for i in range(rows):
            if i!=r and M[i,c]: M[i]^=M[r]
        piv.append(c); r+=1
    return M[:r]
B=rowspace(A); print('live',n,'F2 rank of I+M:',len(B), 'real rank of live lines', np.linalg.matrix_rank(VV[live]))
# enumerate row space (if small) and real ranks of supports
k=len(B)
if k<=16:
    best=collections.Counter(); combos=[]
    for mask in range(1,2**k):
        v=np.zeros(n,dtype=np.uint8)
        for i in range(k):
            if mask>>i&1: v^=B[i]
        supp=[live[j] for j in np.nonzero(v)[0]]
        rk=np.linalg.matrix_rank(VV[supp])
        combos.append((rk,len(supp),mask)); best[rk]+=1
    print('rank distribution', sorted(best.items()))
    combos.sort(); piv={}; tot=0; chosen=[]
    for rk,sz,m in combos:
        x=m
        for b in sorted(piv,reverse=True):
            if x>>b&1: x^=piv[b]
        if x: piv[x.bit_length()-1]=x; tot+=rk; chosen.append((rk,sz))
        if len(chosen)==k: break
    print('min-rank basis cst',tot,chosen,'x =',tot/n)
