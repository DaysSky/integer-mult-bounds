"""Grassmannian relaxation data for general m over F_q (radix q): points = m-dim subspaces of F_q^{2m}.
Free = generators of P = Stab(D-space) (relaxation), paid = H += M D with rank(M)=1.
Target = subspaces transversal to the D-space.  usage: mkgrm.py m q"""
import itertools, numpy as np, pickle, sys
m=int(sys.argv[1]); q=int(sys.argv[2]); n=2*m
def rref(M):
    M=M.copy()%q; r=0
    for c in range(M.shape[1]):
        p=next((i for i in range(r,M.shape[0]) if M[i,c]),None)
        if p is None: continue
        M[[r,p]]=M[[p,r]]; M[r]=(M[r]*pow(int(M[r,c]),q-2,q))%q
        for i in range(M.shape[0]):
            if i!=r and M[i,c]: M[i]=(M[i]-M[i,c]*M[r])%q
        r+=1
    return M[:r]
def key(B): return rref(B.T.copy()).tobytes()
e=np.eye(n,dtype=np.int64)
D0=e[:,m:]
# enumerate points by BFS from D0 under elementary matrices
gensall=[]
for i in range(n):
    for j in range(n):
        if i!=j:
            X=np.eye(n,dtype=np.int64); X[i,j]=1; gensall.append(X)
from collections import deque
seen={key(D0):D0}; dq=deque([D0])
while dq:
    B=dq.popleft()
    for g in gensall:
        C=(g@B)%q; k=key(C)
        if k not in seen: seen[k]=C; dq.append(C)
keys=list(seen); idx={k:i for i,k in enumerate(keys)}; bases=[seen[k] for k in keys]
print('m',m,'q',q,'points',len(keys),flush=True)
def perm(g): return [idx[key((g@B)%q)] for B in bases]
gens=[]
for i in range(n):
    for j in range(n):
        if i==j: continue
        if (i<m and j>=m): continue   # upper block (H += D) is paid
        for c in range(1,q):
            X=np.eye(n,dtype=np.int64); X[i,j]=c; gens.append(X)
for i in range(n):
    for c in range(2,q):
        X=np.eye(n,dtype=np.int64); X[i,i]=c; gens.append(X)
gp=[perm(g) for g in gens]; i0=idx[key(D0)]; assert all(p[i0]==i0 for p in gp)
paid=set(); vh=[v for v in itertools.product(range(q),repeat=m) if any(v)]
for a in vh:
    for b in vh:
        g=np.eye(n,dtype=np.int64); g[:m,m:]=np.outer(a,b)%q; paid.add(tuple(perm(g)))
paid=[list(p) for p in paid]
cell=[i for i,B in enumerate(bases) if rref(np.hstack([B,D0]).T.copy()).shape[0]==n]
print('free gens',len(gp),'paid',len(paid),'target',len(cell),flush=True)
pickle.dump(dict(nf=len(keys),i0=i0,gens=gp,paid=paid,cellT=cell),open('grm%d_q%d.pkl'%(m,q),'wb'))
