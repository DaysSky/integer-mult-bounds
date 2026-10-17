import sys, numpy as np, time, networkx as nx
from bld import *
q=int(sys.argv[1]); n=4; m=2
t0=time.time()
C=all_chambers(n,q); print('chambers',len(C),round(time.time()-t0,1),flush=True)
I=np.eye(n,dtype=np.int64)
def rl(w):
    seen=set(); cyc=0
    for i in range(n):
        if i in seen: continue
        cyc+=1; j=i
        while j not in seen: seen.add(j); j=w[j]
    return n-cyc
# chamber matrices c: delta(I,c) = weyl(c^{-1})
nb=[c for c in C if rl(weyl(matinv(c,q),q))==1]
print('cost-1 nbrs',len(nb),round(time.time()-t0,1),flush=True)
A=np.array(nb); Ainv=np.array([matinv(c,q) for c in nb])
N=len(nb)
def det3(M):
    return (M[...,0,0]*(M[...,1,1]*M[...,2,2]-M[...,1,2]*M[...,2,1])
           -M[...,0,1]*(M[...,1,0]*M[...,2,2]-M[...,1,2]*M[...,2,0])
           +M[...,0,2]*(M[...,1,0]*M[...,2,1]-M[...,1,1]*M[...,2,0]))
edges=[]
for i in range(N):
    M=np.einsum('ab,nbc->nac',A[i],Ainv)%q      # y_i y_j^{-1}
    ok=(M[:,0,3]==0)&(M[:,0,2]!=0)&(M[:,1,3]!=0)&(det3(M[:,0:3,1:4])%q==0)
    for j in np.nonzero(ok)[0]:
        if j>i: edges.append((i,int(j)))
print('compat edges',len(edges),round(time.time()-t0,1),flush=True)
G=nx.Graph(); G.add_nodes_from(range(N)); G.add_edges_from(edges)
best=0
for cl in nx.find_cliques(G):
    if len(cl)>best: best=len(cl); print('clique',best,flush=True)
print('max compat set',best)
