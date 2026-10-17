"""Subsets of E8+E8 norm-4 lines with no inner product +-2 (so G mod 2 decides orthogonality: J+Gbar decoder, rank<=17).
Randomized greedy independent sets in the '+-2 graph'.  usage: e8sq.py seconds seed"""
import itertools, sys, time, numpy as np
T=float(sys.argv[1]); rng=np.random.default_rng(int(sys.argv[2]))
# E8 roots in doubled coordinates (D8 + half-spin), norm 8 -> divide later
R=[]
for i,j in itertools.combinations(range(8),2):
    for a,b in itertools.product((2,-2),repeat=2):
        v=[0]*8; v[i]=a; v[j]=b; R.append(v)
for s in itertools.product((1,-1),repeat=8):
    if s.count(-1)%2==0: R.append(list(s))
R=np.array(R)                       # 240 roots, norm 8 (=2*4)
assert len(R)==240
# E8 norm-4 vectors (norm 16 in doubled coords): sums r+s of roots with r.s=0 (doubled: r.s=0)
N4=set()
G=R@R.T
for a in range(240):
    for b in np.nonzero(G[a]==0)[0]:
        N4.add(tuple(R[a]+R[b]))
N4=np.array(sorted(N4)); assert len(N4)==2160, len(N4)
Z=np.zeros_like(R); Z4=np.zeros((2160,8),int)
V=np.vstack([np.hstack([N4,Z4]),np.hstack([Z4,N4]),
             np.array([np.concatenate([r,s]) for r in R for s in R])])
assert len(V)==61920
# lines: canonical sign
def canon(v):
    nz=np.nonzero(v)[0][0]; return v if v[nz]>0 else -v
L=np.unique(np.array([canon(v) for v in V]),axis=0); n=len(L); print('lines',n,flush=True)
# inner products in units: original norm-4 => doubled-coord norm 16; ip_orig = dot/4
best=None; t0=time.time(); it=0
while time.time()-t0<T:
    it+=1; order=rng.permutation(n); alive=np.ones(n,bool); S=[]
    for v in order:
        if not alive[v]: continue
        S.append(v); ip=(L@L[v])//4; alive[np.abs(ip)==2]=False; alive[v]=False
    if best is None or len(S)>len(best):
        best=S; Ls=L[best]; g=(Ls@Ls.T)//4
        vals=sorted(set(np.unique(g).tolist()))
        A=(g%2).astype(np.uint8); rr=0
        for c in range(A.shape[1]):
            p=np.nonzero(A[rr:,c])[0]
            if len(p)==0: continue
            p=p[0]+rr; A[[rr,p]]=A[[p,rr]]; m=A[:,c].copy(); m[rr]=0; A[m==1]^=A[rr]; rr+=1
            if rr==A.shape[0]: break
        rq=np.linalg.matrix_rank(Ls.astype(float)); c_=rr+1
        z=((g==0).sum(1)).mean()
        print('it %d lines %d rankQ %d F2rank %d c<=%d x<=%.3f ip values %s mean orth/line %.0f (%.0fs)'%(it,len(S),rq,rr,c_,c_*rq/len(S),vals,z,time.time()-t0),flush=True)
np.save('e8sq_best_s%s.npy'%sys.argv[2],L[best])
