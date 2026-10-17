"""Many random restarts directly at n=9, b=2, d=15 (ALS then LM).  usage: restarts.py seed0 seconds"""
import os, sys, time
os.environ["OMP_NUM_THREADS"]="1"; os.environ["OPENBLAS_NUM_THREADS"]="1"
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/vmbundle/tri')
import numpy as np
from core import adjacency, block_mask, resnorm, als_run, lm_solve
n,b,d=9,2,15; T,X,A=adjacency(n); N=len(T); M,D=block_mask(A,b)
s0=int(sys.argv[1]); tmax=float(sys.argv[2]); t0=time.time(); best=np.inf; k=0
while time.time()-t0<tmax:
    rng=np.random.default_rng(s0*100000+k); k+=1
    U=rng.standard_normal((d,N*b)); V=rng.standard_normal((d,N*b))
    U,V=als_run(U,V,A,b,400)
    U,V,r,_=lm_solve(U,V,M,D,iters=80)
    res=resnorm(U,V,M,D)[0]
    if res<best:
        best=res; print('restart',k,'res %.3e'%res,'%.0fs'%(time.time()-t0),flush=True)
    if res<1e-9:
        np.savez('hit_s%d_k%d.npz'%(s0,k),U=U,V=V); print('HIT'); break
print('done restarts',k,'best %.3e'%best)
