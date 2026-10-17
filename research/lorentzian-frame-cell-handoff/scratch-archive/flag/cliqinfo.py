import sys, numpy as np, networkx as nx
from bld import *
q=int(sys.argv[1]); n=4
C=all_chambers(n,q); I=np.eye(n,dtype=np.int64)
nb=[c for c in C if (lambda w: sum(1 for i in range(n) if w[i]!=i)==2)(weyl(matinv(c,q),q))]
wT=(2,3,0,1)
G=nx.Graph()
for i in range(len(nb)):
    for j in range(i+1,len(nb)):
        if delta(nb[i],nb[j],q)==wT: G.add_edge(i,j)
cl=max(nx.find_cliques(G),key=len)
from collections import Counter
print('q',q,'clique',len(cl))
print('weyl types of clique members:',[weyl(matinv(nb[i],q),q) for i in cl])
print('all nbr types:',Counter(weyl(matinv(c,q),q) for c in nb))
print('number of max cliques:',sum(1 for c in nx.find_cliques(G) if len(c)==len(cl)))
