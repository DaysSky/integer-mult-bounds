"""Rank continuation: random solution at d0, then reduce d one at a time."""
import os, sys, time, argparse
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/vmbundle/tri')
from core import *
p = argparse.ArgumentParser()
p.add_argument('--n', type=int, default=16)
p.add_argument('--p', type=int, default=0)
p.add_argument('--b', type=int, default=1)
p.add_argument('--d0', type=int, default=32)
p.add_argument('--dmin', type=int, default=8)
p.add_argument('--als0', type=int, default=600)
p.add_argument('--ramp', type=int, default=150)
p.add_argument('--polish', type=int, default=300)
p.add_argument('--lm', type=int, default=60)
p.add_argument('--seed', type=int, default=0)
p.add_argument('--mode', default='drop')
p.add_argument('--tag', default='run')
p.add_argument('--init', default=None)
p.add_argument('--thr', type=float, default=1e-4)
p.add_argument('--maxchunks', type=int, default=10)
a = p.parse_args()
import itertools
if a.p:
    T=[tuple(2*i+e for i,e in zip(P,E)) for P in itertools.combinations(range(a.p),3) for E in itertools.product((0,1),repeat=3)]
    X=np.zeros((len(T),2*a.p))
    for i,t in enumerate(T): X[i,list(t)]=1
    A=(np.abs(X@X.T-1)<.5).astype(float); a.n=a.p
else:
    T, X, A = adjacency(a.n)
N = len(T)
if a.init == 'split':
    h=X.shape[1]; Q=np.eye(h)-np.ones((h,h))/9
    Uf=np.zeros((h*a.b,N*a.b)); Vf=np.zeros((h*a.b,N*a.b))
    for t in range(N):
        for j in range(a.b):
            u=np.zeros((h,a.b)); u[list(T[t]),j]=1
            Uf[:,t*a.b+j]=u.ravel(); Vf[:,t*a.b+j]=(Q@u).ravel()/2
    np.savez('_split_tmp_%s.npz'%a.tag,U=Uf,V=Vf); a.init='_split_tmp_%s.npz'%a.tag
M, D = block_mask(A, a.b)

rng = np.random.default_rng(a.seed)
if a.init:
    z = np.load(a.init); Uf, Vf = z['U'], z['V']
else:
    Uf = rng.standard_normal((a.d0, N * a.b)); Vf = rng.standard_normal((a.d0, N * a.b))
    Uf, Vf = als_run(Uf, Vf, A, a.b, a.als0)
Uf, Vf, r, _ = lm_solve(Uf, Vf, M, D, iters=a.lm)
d = Uf.shape[0]
print('start d', d, 'res %.3e max %.3e' % resnorm(Uf, Vf, M, D), flush=True)
np.savez('sol_%s%d_b%d_d%d_%s.npz' % ('p' if a.p else 'n', a.n, a.b, d, a.tag), U=Uf, V=Vf)
while d > a.dmin:
    t0 = time.time()
    if a.mode == 'drop':
        U2, V2, w = balanced_sorted(Uf, Vf)
        print('  weights tail', np.round(w[-4:], 4), flush=True)
        U2, V2 = U2[:-1], V2[:-1]
        prev = np.inf
        for chunk in range(a.maxchunks):
            U2, V2 = als_run(U2, V2, A, a.b, a.polish)
            rr = resnorm(U2, V2, M, D)[0]
            if rr < a.thr or rr > 0.97 * prev:
                break
            prev = rr
    else:
        U2, V2 = reduce_rank(Uf, Vf, A, a.b, M, D, ramp=a.ramp, polish=a.polish)
    U2, V2, r, _ = lm_solve(U2, V2, M, D, iters=a.lm)
    res = resnorm(U2, V2, M, D)
    print('d', d - 1, 'res %.3e max %.3e' % res, '%.1fs' % (time.time() - t0), flush=True)
    if res[0] > a.thr:
        print('stalled at d', d - 1); np.savez('fail_%s%d_b%d_d%d_%s.npz' % ('p' if a.p else 'n', a.n, a.b, d - 1, a.tag), U=U2, V=V2)
        break
    Uf, Vf = U2, V2; d -= 1
    np.savez('sol_%s%d_b%d_d%d_%s.npz' % ('p' if a.p else 'n', a.n, a.b, d, a.tag), U=Uf, V=Vf)
