"""Nodes G = P + P' (two orthogonal design A2 cells from complementary blocks): which design sections lie in G-perp."""
from common import *
D4 = load_d4()
full = [W for W in D4 if len([P for P in planes if P & ~W == 0]) == 12 and len([Q for Q in planes if Q & ~perpmask(W) == 0]) == 12]
blk = {s: k for k, W in enumerate(full) for s in e8.bits(W)}
comp = {k: full.index(perpmask(W)) for k, W in enumerate(full)}
A2c = [P for P in planes if pc(P) == 3]
nodes = set()
for i, P in enumerate(A2c):
    for P2 in A2c[i+1:]:
        if blk[e8.bits(P2)[0]] == comp[blk[e8.bits(P)[0]]] and (perpmask(P) & P2) == P2:
            nodes.add(P | P2)
st = collections.Counter(); ex = None
for G in nodes:
    Gp = perpmask(G)
    secs = [Q for Q in planes if Q & ~Gp == 0]
    cl = e8.closure(G)[0]
    key = (pc(cl), tuple(sorted(collections.Counter(pc(Q) for Q in secs).items())),
           tuple(sorted(collections.Counter(tuple(sorted(set(blk[u] for u in e8.bits(Q)))) for Q in secs).values())))
    st[key] += 1
print('A2+A2 nodes from complementary design cells:', len(nodes))
for k, n in st.most_common(): print('  (closure lines, section sizes, ...)', k, n)
