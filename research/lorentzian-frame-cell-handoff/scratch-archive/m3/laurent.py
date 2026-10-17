import numpy as np, itertools, sys, random
from scipy.optimize import least_squares
W=3
def expand(alpha, X, Y):
    """alpha: list of int tuples; X,Y: s x W complex. returns dict exp->matrix"""
    D={tuple([0]*len(alpha[0])): np.eye(W,dtype=complex)}
    for a,al in enumerate(alpha):
        N=np.outer(X[a],Y[a]); IN=np.eye(W)-N
        nd={}
        for e,M in D.items():
            for (e2,F) in ((e,IN),(tuple(i+j for i,j in zip(e,al)),N)):
                v=M@F
                if e2 in nd: nd[e2]=nd[e2]+v
                else: nd[e2]=v
        D=nd
    return D
def residual(z, alpha, target):
    s=len(alpha)
    c=z[:12*s].reshape(2,s,6); c=c[0]+1j*c[1]
    X=c[:,:3]; Y=c[:,3:]
    D=expand(alpha,X,Y)
    res=[]
    for e,M in D.items():
        T=target.get(e)
        R=M-T if T is not None else M
        res.append(R.ravel())
    for e,T in target.items():
        if e not in D: res.append(-T.ravel())
    res.append(np.einsum('ij,ij->i',X,Y)-1)
    r=np.concatenate(res)
    return np.concatenate([r.real,r.imag])
def solve(alpha, gamma, perm=(0,1,2), tries=20, seed=0):
    rng=np.random.default_rng(seed)
    target={}
    for w in range(W):
        T=np.zeros((W,W),dtype=complex); T[w,perm[w]]=1
        g=tuple(gamma[w])
        target[g]=target.get(g,0)+T
    best=None
    s=len(alpha)
    for t in range(tries):
        z0=rng.normal(size=12*s)
        r=least_squares(residual,z0,args=(alpha,target),method='lm',max_nfev=4000)
        c=np.linalg.norm(r.fun)
        if best is None or c<best[0]: best=(c,r.x)
        if c<1e-9: break
    return best
if __name__=='__main__':
    # sanity: trivial 9-factor solution
    al=[(1,0,0),(0,1,0),(0,0,1)]*3
    print('trivial 9 coord:', solve([tuple(a) for a in al],[(1,1,1)]*3,tries=5)[0])
