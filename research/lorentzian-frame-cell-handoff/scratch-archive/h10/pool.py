"""Roots of II_{9,1} in the w-perp model: x in Z^10, y in Z, sum x = 3y, sum x^2 - y^2 = 2, up to sign; y <= YMAX.
Compatibility: |<u,v>| <= 1 (root-like)."""
import itertools, numpy as np, sys
YMAX=int(sys.argv[1]) if len(sys.argv)>1 else 4
n=10
vecs=set()
def gen(y):
    S=3*y; Q=y*y+2
    # entries bounded by sqrt(Q)
    m=int(Q**0.5)
    for x in itertools.product(range(-m,m+1),repeat=n):
        pass
# smarter: enumerate multisets of absolute values with sum of squares Q
def parts(Q, maxv, k):
    # nonincreasing sequences of positive ints with sum squares Q, length<=k
    if Q==0: yield []; return
    if k==0: return
    for a in range(min(maxv,int(Q**0.5)),0,-1):
        for rest in parts(Q-a*a, a, k-1): yield [a]+rest
for y in range(0,YMAX+1):
    S=3*y; Q=y*y+2
    for p in parts(Q, 10, n):
        k=len(p)
        # assign signs and positions
        for pos in itertools.permutations(range(n),k) if False else []: pass
        for comb in itertools.combinations(range(n),k):
            for perm in set(itertools.permutations(p)):
                for signs in itertools.product((1,-1),repeat=k):
                    x=[0]*n
                    for c,a,s in zip(comb,perm,signs): x[c]=a*s
                    if sum(x)==S:
                        v=tuple(x)+(y,)
                        nv=tuple(-t for t in v)
                        vecs.add(max(v,nv))
V=np.array(sorted(vecs),dtype=np.int64)
eta=np.array([1]*n+[-1])
G=(V*eta)@V.T
print('YMAX',YMAX,'lines',len(V),'by y',{int(y):int((np.abs(V[:,-1])==y).sum()) for y in range(YMAX+1)})
A=(np.abs(G)<=1); np.fill_diagonal(A,False)
print('edge density %.3f'%A.mean())
np.save('pool_y%d.npy'%YMAX,V); np.save('adj_y%d.npy'%YMAX,A)
