import numpy as np, itertools, random, pickle, sys
vecs=[v for v in itertools.product((-1,0,1),repeat=3) if any(v)]
# rank-1 matrices up to overall sign: u v^T, canonical sign
pool={}
for u in vecs:
    for v in vecs:
        A=np.outer(u,v)
        f=A.ravel(); nz=f[np.nonzero(f)[0][0]]
        if nz<0: A=-A
        pool[A.tobytes()]=A
pool=list(pool.values()); P=np.array([A.ravel() for A in pool]).astype(float)
print('pool',len(pool))
I=np.eye(3).ravel()
rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 0)
found=[]
for trial in range(20000):
    k=rng.choice([4,5])   # V = span(I, k-1 random pool) -> dim k
    idx=rng.sample(range(len(pool)),k-1)
    Bm=np.vstack([I]+[P[i] for i in idx])
    if np.linalg.matrix_rank(Bm)<k: continue
    # members of pool in V
    Q,_=np.linalg.qr(Bm.T)
    resid=np.linalg.norm(P-(P@Q)@Q.T,axis=1)
    mem=np.nonzero(resid<1e-9)[0]
    if len(mem)>=8:
        found.append((k,tuple(sorted(mem))))
found=sorted(set(found),key=lambda x:-len(x[1]))
print('subspaces with >=8 pool members:',len(found))
for k,m in found[:15]: print(k,len(m))
pickle.dump((pool,found),open('cfg.pkl','wb'))
