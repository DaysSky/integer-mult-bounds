"""Write generator data for sat_gen: free generators = elementary lower x_ij(c) (i>j) and torus diag,
paid = rank-1 strictly upper transvections.  Over F_q, n=4.  usage: mkgens.py q"""
import itertools, numpy as np, pickle, sys
q=int(sys.argv[1]); n=4
def canon(g):
    g=g.copy()%q
    # left cosets g B^- : column operations by B^- on the right: col_j += c*col_k for k>j? use flag of column spans
    return g
# represent flags as tuples of RREF subspaces V1<V2<V3 (column vectors), compute by spans of last columns of g
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
def flag_of(g):
    # base flag x0 = <e4> < <e3,e4> < <e2,e3,e4>; g.x0 spanned by last k columns of g
    return tuple(rref(g[:,n-k:].T.copy()).tobytes() for k in (1,2,3))
gens_mats=[]
for i in range(n):
    for j in range(i):
        for c in range(1,q):
            E=np.eye(n,dtype=np.int64); E[i,j]=c; gens_mats.append(E)
for i in range(n):
    for c in range(2,q):
        E=np.eye(n,dtype=np.int64); E[i,i]=c; gens_mats.append(E)
paid_mats=set()
vecs=[v for v in itertools.product(range(q),repeat=n) if any(v)]
for v in vecs:
    for w in vecs:
        N=np.outer(v,w)%q
        if np.any(np.tril(N)): continue
        paid_mats.add(tuple(((np.eye(n,dtype=np.int64)+N)%q).ravel()))
paid_mats=[np.array(p).reshape(n,n) for p in paid_mats]
# enumerate flags via BFS from identity under all elementary matrices
from collections import deque
I=np.eye(n,dtype=np.int64); start=flag_of(I); seen={start:I}; dq=deque([I])
elem=[]
for i in range(n):
    for j in range(n):
        if i!=j:
            E=np.eye(n,dtype=np.int64); E[i,j]=1; elem.append(E)
while dq:
    g=dq.popleft()
    for E in elem:
        h=(E@g)%q; f=flag_of(h)
        if f not in seen: seen[f]=h; dq.append(h)
flags=list(seen); idx={f:k for k,f in enumerate(flags)}; reps=[seen[f] for f in flags]
print('q',q,'flags',len(flags),'free gens',len(gens_mats),'paid',len(paid_mats))
def perm(m): return [idx[flag_of((m@g)%q)] for g in reps]
T=np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]])
i0=idx[start]
gp=[perm(m) for m in gens_mats]
assert all(p[i0]==i0 for p in gp)
# target cell = B^- orbit of T.x0 : closure under free generators
c0=idx[flag_of(T%q)]; cell={c0}; fr=[c0]
while fr:
    nfr=[]
    for x in fr:
        for p in gp:
            y=p[x]
            if y not in cell: cell.add(y); nfr.append(y)
    fr=nfr
print('target cell size',len(cell))
pickle.dump(dict(nf=len(flags),i0=i0,gens=gp,paid=[perm(m) for m in paid_mats],cellT=sorted(cell)),open('g%d.pkl'%q,'wb'))
