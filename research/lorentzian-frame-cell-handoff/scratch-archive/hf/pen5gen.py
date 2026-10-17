from e8 import *
import itertools
rng=np.random.default_rng(0)
key=next(iter(PEN)); H=halves_of(key); L=[x for h in H for x in h]; idx={t:i for i,t in enumerate(L)}
hid={t:a for a,h in enumerate(H) for t in h}; cls={a:TET[H[a][0]] for a in range(6)}
T=np.zeros((12,12)); W=np.zeros((12,12))   # target matrix and weights (1 on cross entries)
for t in L:
    for s in L:
        if hid[t]!=hid[s]:
            T[idx[t],idx[s]]=N[t,s]
            W[idx[t],idx[s]]=1.0 if cls[hid[t]]!=cls[hid[s]] else 0.0   # within free
# allowed term shapes at line level: S lines, Q lines with spans<=4, disjoint halves
def span(lines): return len(basis([P[x] for x in lines]))
shapes=[]
opts=[]
for a,(x,y) in enumerate(H):
    opts.append([((),())]+[(s,()) for s in [(x,),(y,),(x,y)]]+[((),q) for q in [(x,),(y,),(x,y)]])
for combo in itertools.product(*opts):
    S=[u for s,q in combo for u in s]; Q=[u for s,q in combo for u in q]
    if S and Q and span(S)<=4 and span(Q)<=4: shapes.append((tuple(idx[u] for u in S),tuple(idx[u] for u in Q)))
# keep maximal shapes
def sub(a,b): return set(a[0])<=set(b[0]) and set(a[1])<=set(b[1])
shapes=sorted(set(shapes),key=lambda s:-(len(s[0])*len(s[1])))
maxs=[]
for s in shapes:
    if not any(sub(s,m) for m in maxs): maxs.append(s)
print('maximal level-5 shapes',len(maxs))
def fit(sh,iters=300):
    k=len(sh); A=[rng.standard_normal(12)*0 for _ in sh]; B=[]
    a=[np.zeros(12) for _ in sh]; b=[np.zeros(12) for _ in sh]
    for e,(S,Q) in enumerate(sh): a[e][list(Q)]=rng.standard_normal(len(Q)); b[e][list(S)]=rng.standard_normal(len(S))
    for it in range(iters):
        for e,(S,Q) in enumerate(sh):
            Rm=T-sum(np.outer(a[f],b[f]) for f in range(k) if f!=e)
            # update a[e] on Q: minimize sum W*(Rm - a b^T)^2
            Ql=list(Q); Sl=list(S)
            bb=b[e][Sl]; Wm=W[np.ix_(Ql,Sl)]; Rs=Rm[np.ix_(Ql,Sl)]
            den=(Wm*bb**2).sum(1)+1e-12; a[e][:]=0; a[e][Ql]=(Wm*Rs*bb).sum(1)/den
            aa=a[e][Ql]; den=(Wm*aa[:,None]**2).sum(0)+1e-12; b[e][:]=0; b[e][Sl]=(Wm*Rs*aa[:,None]).sum(0)/den
    Rm=T-sum(np.outer(a[f],b[f]) for f in range(k))
    return np.sqrt((W*Rm**2).sum())
best=1e9
import random
random.seed(1)
for trial in range(4000):
    sh=random.sample(maxs,4)
    # quick coverage check: every cross entry in some shape
    cov=np.zeros((12,12))
    for S,Q in sh: cov[np.ix_(list(Q),list(S))]=1
    if ((W>0)&(cov==0)).any(): continue
    r=min(fit(sh) for _ in range(3))
    if r<best: best=r; print('trial',trial,'residual',r,flush=True)
    if r<1e-8: print('FOUND 4-term level-5 decomposition', sh); break
print('best',best)
