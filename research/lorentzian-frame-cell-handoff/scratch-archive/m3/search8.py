import numpy as np, itertools, random, pickle, sys, time
from fastsolve import attempt
pool,found=pickle.load(open('cfg.pkl','rb'))
rng=random.Random(int(sys.argv[1])); tl=float(sys.argv[2])
I=np.eye(3,dtype=int); Iv=I.ravel().astype(float)
def span_contains(mats, M):
    B=np.array([m.ravel() for m in mats],dtype=float)
    r1=np.linalg.matrix_rank(B); r2=np.linalg.matrix_rank(np.vstack([B,M.ravel()]))
    return r1==r2
def up(A): return np.any(np.triu(A,1)!=0)
tg={}
for w in range(3):
    T=np.zeros((3,3)); T[w,w]=1; tg[I.tobytes()]=tg.get(I.tobytes(),0)+T
t0=time.time(); n=0; best=(1e9,None)
while time.time()-t0<tl:
    k,mem=rng.choice(found[:800])
    if len(mem)<8: continue
    idx=rng.sample(list(mem),8)
    frames=[pool[i]*rng.choice((1,-1)) for i in idx]
    if sum(up(A) for A in frames)<2: continue
    if not np.array_equal(sum(frames),3*I):
        # det condition for common target I requires sum = 3I; adjust signs by search
        ok=False
        for sg in itertools.product((1,-1),repeat=8):
            F=[pool[i]*s for i,s in zip(idx,sg)]
            if np.array_equal(sum(F),3*I): frames=F; ok=True; break
        if not ok: continue
    if not all(span_contains([frames[j] for j in c],I) for c in itertools.combinations(range(8),6)): continue
    n+=1
    r,nc=attempt(frames,tg,tries=3,seed=n,nfev=1500)
    if r is None: continue
    if r[0]<best[0]:
        best=(r[0],frames); print('cfg',n,'classes',nc,'resid',r[0],flush=True)
    if r[0]<1e-8:
        print('SOLUTION', [f.tolist() for f in frames]); pickle.dump((frames,r),open('sol_%s.pkl'%sys.argv[1],'wb')); break
print('tested',n,'best',best[0])
