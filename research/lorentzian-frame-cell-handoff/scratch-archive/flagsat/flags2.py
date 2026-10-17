import itertools, numpy as np, pickle
n=4
vecs=[v for v in itertools.product((0,1),repeat=n) if any(v)]
def span(basis):
    S=set()
    for coeffs in itertools.product((0,1),repeat=len(basis)):
        v=tuple(sum(c*b[i] for c,b in zip(coeffs,basis))%2 for i in range(n))
        if any(v): S.add(v)
    return frozenset(S)
flags=set()
for a in vecs:
    for b in vecs:
        V2=span([a,b])
        if len(V2)!=3: continue
        for c in vecs:
            V3=span([a,b,c])
            if len(V3)!=7: continue
            flags.add((frozenset([a]),V2,V3))
flags=sorted(flags,key=lambda f:(sorted(f[0]),sorted(f[1]),sorted(f[2])))
idx={f:i for i,f in enumerate(flags)}
print('flags',len(flags))
def act(g,f):
    mv=lambda v: tuple(int(x)%2 for x in (g@np.array(v)))
    return (frozenset(map(mv,f[0])),frozenset(map(mv,f[1])),frozenset(map(mv,f[2])))
def perm(g): return [idx[act(g,f)] for f in flags]
e=[tuple(int(i==j) for j in range(n)) for i in range(n)]
x0=(frozenset([e[3]]),span([e[2],e[3]]),span([e[1],e[2],e[3]]))
i0=idx[x0]
free=[]
for bits in itertools.product((0,1),repeat=6):
    L=np.eye(n,dtype=int); k=0
    for i in range(n):
        for j in range(i):
            L[i,j]=bits[k]; k+=1
    free.append(L)
paid=set()
for v in vecs:
    for w in vecs:
        N=np.outer(v,w)%2
        if np.any(np.tril(N)): continue
        paid.add(tuple((np.eye(n,dtype=int)+N).ravel()%2))
paid=[np.array(p).reshape(n,n) for p in paid]
print('free',len(free),'paid',len(paid))
T=np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]])
cellT=sorted(set(perm(L)[idx[act(T,x0)]] for L in free))
print('target cell size',len(cellT),'x0 fixed by free:',all(perm(L)[i0]==i0 for L in free))
pickle.dump(dict(nf=len(flags),i0=i0,free=[perm(L) for L in free],paid=[perm(u) for u in paid],cellT=cellT),open('f2.pkl','wb'))
