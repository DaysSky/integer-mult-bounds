import numpy as np, itertools, random, sys, time
from scipy.optimize import least_squares
from fastsolve import paths
W=3
pts=list(itertools.product((0,1),repeat=3))
def f(v,sign=1):  # Z4 function [v.x] * sign as tuple over 8 points
    return tuple((sign*(sum(a*b for a,b in zip(v,x))%2))%4 for x in pts)
vs=[v for v in pts if any(v)]
frames=[(v,s) for v in vs for s in (1,-1)]
FR={fr:np.array(f(*fr)) for fr in frames}
T=np.array([sum(x)%4 for x in pts])   # wt(x) mod 4  = [x1]+[x2]+[x3]
def attempt(seq, tries=4, seed=0, nfev=2000):
    s=len(seq); G=[FR[g] for g in seq]
    keys={}; cid=np.zeros(1<<s,dtype=int)
    for S in range(1<<s):
        v=sum((G[a] for a in range(s) if S>>a&1), np.zeros(8,dtype=int))%4
        k=v.tobytes()
        if k not in keys: keys[k]=len(keys)
        cid[S]=keys[k]
    tk=T.tobytes()
    if tk not in keys: return None, len(keys)
    nc=len(keys); TT=np.zeros((nc,W,W),dtype=complex); TT[keys[tk]]=np.eye(W)
    def res(z):
        c=z.reshape(2,s,6); c=c[0]+1j*c[1]; X=c[:,:3]; Y=c[:,3:]
        Ms=paths(X,Y); S_=np.zeros((nc,W,W),dtype=complex); np.add.at(S_,cid,Ms)
        r=np.concatenate([(S_-TT).ravel(), np.einsum('ij,ij->i',X,Y)-1]); return np.concatenate([r.real,r.imag])
    rng=np.random.default_rng(seed); best=1e9
    for t in range(tries):
        r=least_squares(res,rng.normal(size=12*s),method='lm',max_nfev=nfev)
        c=np.linalg.norm(r.fun); best=min(best,c)
        if c<1e-8: return (c,r.x),nc
    return (best,None),nc
if __name__=='__main__':
    # sanity trivial 9: [x1],[x2],[x3] three times
    triv=[((1,0,0),1),((0,1,0),1),((0,0,1),1)]*3
    print('trivial9',attempt(triv,tries=2)[0][0])
    rng=random.Random(int(sys.argv[1])); tl=float(sys.argv[2]); t0=time.time(); n=0; best=1e9
    while time.time()-t0<tl:
        seq=[rng.choice(frames) for _ in range(8)]
        # necessary: sum of frames == 3T mod 4 (determinant) 
        tot=sum(FR[g] for g in seq)%4
        if not np.array_equal(tot,(3*T)%4): continue
        n+=1
        r,nc=attempt(seq,tries=2,seed=n,nfev=1500)
        if r is None: continue
        if r[0]<best:
            best=r[0]; print(n,'classes',nc,'res',r[0],seq,flush=True)
        if r[0]<1e-8: print('SOLUTION',seq); break
    print('tested',n,'best',best)
