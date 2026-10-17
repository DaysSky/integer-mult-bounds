import pickle, sys, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V
part=pickle.load(open(sys.argv[1],'rb'))
frames, punct = part
live=sorted(set(range(V))-set(punct))
print('frames',len(frames),'punctured',len(punct),'live',len(live))
# real vectors of lines
def vec(u):
    x=np.zeros(12)
    for i in g.supp[u]: x[i]=1 if g.kind[u]=='T' else 0
    if g.kind[u]=='P':
        a,b=sorted(g.supp[u]); x[a]=1; x[b]=-1
    else: x[11]=1
    return x
VV={u:vec(u) for u in range(V)}
eta=np.diag([1]*11+[-1])
ip=lambda a,b: a@eta@b
# sanity: norms and orthogonality via HYP
u0=live[0]; print('norm',ip(VV[u0],VV[u0]))
perp=lambda t: [u for u in live if u!=t and abs(ip(VV[t],VV[u]))<1e-9]
# F2 matrix A = I + M on live
n=len(live); idx={u:i for i,u in enumerate(live)}
A=np.zeros((n,n),dtype=np.uint8)
for t in live:
    A[idx[t],idx[t]]=1
    for u in perp(t): A[idx[t],idx[u]]^=1
def f2rank(M):
    M=M.copy()%2; r=0; rows,cols=M.shape
    for c in range(cols):
        p=next((i for i in range(r,rows) if M[i,c]),None)
        if p is None: continue
        M[[r,p]]=M[[p,r]]
        for i in range(rows):
            if i!=r and M[i,c]: M[i]^=M[r]
        r+=1
    return r
print('F2 rank of I+M on live lines:', f2rank(A))
# D10 totals restricted to live: real span rank
for h in range(11):
    D=[u for u in live if (g.kind[u]=='P' and h not in g.supp[u]) or (g.kind[u]=='T' and h in g.supp[u])]
    rk=np.linalg.matrix_rank(np.array([VV[u] for u in D])) if D else 0
    print('D10(%d): live lines %d, real rank %d'%(h,len(D),rk))
