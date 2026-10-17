import numpy as np, itertools, random, pickle, sys, time
from scipy.optimize import least_squares
W=3
def classes_for(frames):
    s=len(frames); keys={}; cid=np.zeros(1<<s,dtype=int)
    for S in range(1<<s):
        M=sum((frames[a] for a in range(s) if S>>a&1), np.zeros((3,3),dtype=int))
        k=M.tobytes()
        if k not in keys: keys[k]=(len(keys),M)
        cid[S]=keys[k][0]
    return cid, keys
def paths(X,Y):
    s=X.shape[0]
    Ms=np.eye(W,dtype=complex)[None]
    for a in range(s):
        N=np.outer(X[a],Y[a]); IN=np.eye(W)-N
        # bit a of S: subsets ordered so that index = sum bit<<a ; build by appending
        Ms=np.concatenate([Ms@IN, Ms@N],axis=0)  # new bit is the highest -> index S with bit a set = old + 2^a
    return Ms
def make_res(frames, targets):
    """targets: dict class-key-bytes -> 3x3 matrix"""
    s=len(frames)
    cid,keys=classes_for(frames)
    # reorder: our paths() puts bit a at position 2^a since concatenation doubles with new block appended
    nc=len(keys)
    T=np.zeros((nc,W,W),dtype=complex)
    for k,M in targets.items():
        if k not in keys: return None,nc
        T[keys[k][0]]+=M
    def res(z):
        c=z[:12*s].reshape(2,s,6); c=c[0]+1j*c[1]
        X=c[:,:3]; Y=c[:,3:]
        Ms=paths(X,Y)
        S=np.zeros((nc,W,W),dtype=complex); np.add.at(S,cid,Ms)
        r=np.concatenate([(S-T).ravel(), np.einsum('ij,ij->i',X,Y)-1])
        return np.concatenate([r.real,r.imag])
    return res,nc
def attempt(frames, targets, tries=6, seed=0, nfev=3000):
    res,nc=make_res(frames,targets)
    if res is None: return None,nc
    rng=np.random.default_rng(seed); best=1e9
    for t in range(tries):
        r=least_squares(res,rng.normal(size=12*len(frames)),method='lm',max_nfev=nfev)
        c=np.linalg.norm(r.fun); best=min(best,c)
        if c<1e-8: return (c,r.x),nc
    return (best,None),nc
if __name__=='__main__':
    # sanity: trivial 9 diag
    E=[np.diag(v).astype(int) for v in ([1,0,0],[0,1,0],[0,0,1])]*3
    tg={}
    for w in range(3):
        T=np.zeros((3,3)); T[w,w]=1; k=np.eye(3,dtype=int).tobytes(); tg[k]=tg.get(k,0)+T
    t=time.time(); print(attempt(E,tg,tries=3)[0][0], time.time()-t)
