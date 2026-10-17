"""Rank-b labels on the paired cube (transversal triples of p pairs; neighbours |S cap T| = 1) in dimension r.
Random restarts of ALS + LM (core.py from the triple solver).  usage: pc.py p b r seconds seed"""
import os, sys, time, itertools
os.environ["OMP_NUM_THREADS"]="1"; os.environ["OPENBLAS_NUM_THREADS"]="1"
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/vmbundle/tri')
import numpy as np
import core
from core import block_mask, resnorm, als_run, lm_solve
p,b,r,tmax,seed=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5])
T=[tuple(2*i+e for i,e in zip(P,E)) for P in itertools.combinations(range(p),3) for E in itertools.product((0,1),repeat=3)]
N=len(T); X=np.zeros((N,2*p))
for i,t in enumerate(T): X[i,list(t)]=1
I=X@X.T; A=(np.abs(I-1)<.5).astype(float)
M,D=block_mask(A,b)
print('p',p,'ports',N,'h',2*p,'b',b,'r',r,'neighbours/port',int(A.sum(1)[0]),flush=True)
t0=time.time(); best=np.inf; k=0
while time.time()-t0<tmax:
    rng=np.random.default_rng(seed*100000+k); k+=1
    U=rng.standard_normal((r,N*b)); V=rng.standard_normal((r,N*b))
    U,V=als_run(U,V,A,b,500)
    U,V,_,_=lm_solve(U,V,M,D,iters=100)
    res=resnorm(U,V,M,D)[0]
    if res<best: best=res; print('restart',k,'res %.3e'%res,'%.0fs'%(time.time()-t0),flush=True)
    if res<1e-9: np.savez('pc_p%d_b%d_r%d_s%d.npz'%(p,b,r,seed),U=U,V=V); print('HIT'); break
print('done',k,'best %.3e'%best)
