from geo import *
from framenet import FrameNet
import numpy as np
from fractions import Fraction
c=load(); v=c['v']; F=c['frames']; n=2*v+c['R']
# drop-free map: replay A and B (no cut) on source columns
V=np.zeros((n,v)); 
for s in range(v): V[s,s]=1
for part in ('A','B'):
    for e in c[part]:
        if e[0]=='add': V[e[1]]+= e[3]/e[4]*V[e[2]]
        else: V[e[1]]*= e[2]/e[3]
Mdf=V[v:2*v].copy()
print('drop-free target map nnz', int((np.abs(Mdf)>1e-12).sum()))
# chains from frames visited in A,B (+start)
chains=[[] for _ in range(n)]
def visit(r,f):
    fb=tuple(basis(F[f]))
    if not chains[r] or chains[r][-1][1]!=fb: chains[r].append((len(fb),fb))
for r in range(n): visit(r,c['start'][r])
for part in ('A','B'):
    for e in c[part]:
        for r in ([e[1],e[2]] if e[0]=='add' else [e[1]]): visit(r,e[-1])
regs=[]
for r in range(n):
    t='X' if r<v else ('Y' if r<2*v else 'H')
    ch=[(d,f) for d,f in chains[r] if d>0 or t!='X']
    # drop dim-0 frames duplicates
    regs.append({'type':t,'port':(r if r<v else (r-v if r<2*v else None)),'chain':ch})
# merge duplicate dims (a register can visit only one frame per dim if monotone)
fn=FrameNet(regs,Mdf,v)
print('stages group counts', [len(s) for s in fn.stages], 'max group', max((len(g) for s in fn.stages for f,g in s),default=0))
import sys
r=fn.solve(sweeps=int(sys.argv[1]) if len(sys.argv)>1 else 5, verbose=True)
print('final residual',r,'min sv',fn.min_abs_det())
