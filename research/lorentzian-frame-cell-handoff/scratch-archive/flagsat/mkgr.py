"""Grassmannian relaxation of the full bit flag model, m=2, frames over F_q, for sat_mix/sat_mix2.
Points = 2-dim subspaces of F_q^4 (column vectors); base d0 = <e3,e4> (D-space).
Free = generators of the parabolic P = Stab(d0) (relaxation: P contains B^-).
Paid = H += M D with rank(M)=1.  Target set = all planes transversal to d0 (P-orbit of T d0).
usage: mkgr.py q"""
import itertools, numpy as np, pickle, sys
q=int(sys.argv[1]); n=4
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
def pt(B):  # B: 4x2 column basis -> canonical key
    return rref(B.T.copy()).tobytes()
pts={}
for v in itertools.product(range(q),repeat=8):
    B=np.array(v).reshape(4,2)
    R=rref(B.T.copy())
    if R.shape[0]==2: pts.setdefault(R.tobytes(),R.T.copy())
keys=list(pts); idx={k:i for i,k in enumerate(keys)}; bases=[pts[k] for k in keys]
print('points',len(keys))
def perm(g): return [idx[pt((g@B)%q)] for B in bases]
e=np.eye(n,dtype=np.int64)
d0=idx[pt(e[:,2:4])]
gens=[]
def E(i,j,c):
    X=np.eye(n,dtype=np.int64); X[i,j]=c; return X
for (i,j) in [(1,0),(0,1),(3,2),(2,3),(2,0),(2,1),(3,0),(3,1)]:
    for c in range(1,q): gens.append(E(i,j,c))
for i in range(n):
    for c in range(2,q):
        X=np.eye(n,dtype=np.int64); X[i,i]=c; gens.append(X)
gp=[perm(g) for g in gens]; assert all(p[d0]==d0 for p in gp)
paid=set()
vh=[v for v in itertools.product(range(q),repeat=2) if any(v)]
for a in vh:
    for b in vh:
        M=np.outer(a,b)%q; g=np.eye(n,dtype=np.int64); g[0:2,2:4]=M
        paid.add(tuple(perm(g)))
paid=[list(p) for p in paid]
T=np.eye(n,dtype=np.int64); T[0,2]=1; T[1,3]=1
cell=[i for i,B in enumerate(bases) if np.linalg.matrix_rank(np.hstack([B,e[:,2:4]]).astype(float))==4 and
      __import__('numpy').round(np.linalg.det(np.hstack([B,e[:,2:4]]).astype(float)))%q!=0]
# exact transversality mod q via rank
def rank_q(A):
    return rref(A.T.copy()).shape[0] if False else rref(A.copy()).shape[0]
cell=[i for i,B in enumerate(bases) if rank_q(np.hstack([B,e[:,2:4]]))==4]
print('free gens',len(gp),'paid',len(paid),'target cell',len(cell),'T.d0 in cell', idx[pt((T@e[:,2:4])%q)] in cell)
pickle.dump(dict(nf=len(keys),i0=d0,gens=gp,paid=paid,cellT=cell),open('gr%d.pkl'%q,'wb'))
