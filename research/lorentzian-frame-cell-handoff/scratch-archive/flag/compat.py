import sys, numpy as np, itertools, networkx as nx, time
from bld import *
m=int(sys.argv[1]); q=int(sys.argv[2]); n=2*m
t0=time.time()
C=all_chambers(n,q); print('chambers',len(C),round(time.time()-t0,1),flush=True)
I=np.eye(n,dtype=np.int64)
wT=tuple([i+m for i in range(m)]+[i for i in range(m)])
def rl(w): # reflection length = n - cycles
    seen=set(); cyc=0
    for i in range(n):
        if i in seen: continue
        cyc+=1; j=i
        while j not in seen: seen.add(j); j=w[j]
    return n-cyc
print('wT',wT,'rl',rl(wT))
D=[delta(I,c,q) for c in C]
from collections import Counter
print('dist from e by reflection length:',Counter(rl(w) for w in D))
nb=[c for c,w in zip(C,D) if rl(w)==1]
print('cost-1 neighbours',len(nb),flush=True)
G=nx.Graph(); G.add_nodes_from(range(len(nb)))
for i in range(len(nb)):
    for j in range(i+1,len(nb)):
        if delta(nb[i],nb[j],q)==wT: G.add_edge(i,j)
print('compat edges',G.number_of_edges(),round(time.time()-t0,1),flush=True)
cl=max(nx.find_cliques(G),key=len) if G.number_of_edges() else [0]
print('max pairwise session-compatible set',len(cl))
