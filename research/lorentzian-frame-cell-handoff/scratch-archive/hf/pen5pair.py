"""Per-pencil level-5 decompositions (general coefficients, half-level shapes) where every S-set of size 3
is shared by >=2 terms (so registers can exchange at their last gathering frame), or S has size<=2.
Search over multisets of shapes; check exact cross coverage via ALS."""
import itertools, random
import numpy as np
rng=np.random.default_rng(0)
halves=list(range(6)); cls={0:0,1:0,2:1,3:1,4:2,5:2}
T=np.zeros((6,6)); W=np.zeros((6,6))
for q in halves:
    for s in halves:
        if q!=s and cls[q]!=cls[s]: T[q,s]=1.0; W[q,s]=1.0
shapes=[]
for S in itertools.chain(itertools.combinations(halves,2),itertools.combinations(halves,3)):
    rest=[h for h in halves if h not in S]
    for k in (2,3):
        for Q in itertools.combinations(rest,k): shapes.append((S,Q))
def fit(sh,iters=600,restarts=4):
    best=1e9
    for _ in range(restarts):
        k=len(sh); a=[np.zeros(6) for _ in sh]; b=[np.zeros(6) for _ in sh]
        for e,(S,Q) in enumerate(sh): a[e][list(Q)]=rng.standard_normal(len(Q)); b[e][list(S)]=rng.standard_normal(len(S))
        for it in range(iters):
            for e,(S,Q) in enumerate(sh):
                Rm=T-sum(np.outer(a[f],b[f]) for f in range(k) if f!=e)
                Ql=list(Q);Sl=list(S);bb=b[e][Sl];Wm=W[np.ix_(Ql,Sl)];Rs=Rm[np.ix_(Ql,Sl)]
                a[e][:]=0;a[e][Ql]=(Wm*Rs*bb).sum(1)/((Wm*bb**2).sum(1)+1e-12)
                aa=a[e][Ql];b[e][:]=0;b[e][Sl]=(Wm*Rs*aa[:,None]).sum(0)/((Wm*aa[:,None]**2).sum(0)+1e-12)
        Rm=T-sum(np.outer(a[f],b[f]) for f in range(k))
        best=min(best,np.sqrt((W*Rm**2).sum()))
    return best
def ok_pairing(sh):
    from collections import Counter
    c=Counter(S for S,Q in sh if len(S)==3)
    return all(v>=2 for v in c.values())
def covers(sh):
    cov=np.zeros((6,6))
    for S,Q in sh: cov[np.ix_(list(Q),list(S))]=1
    return not ((W>0)&(cov==0)).any()
random.seed(2)
found={}
for n in (4,5,6):
    tries=0; hits=0
    for trial in range(60000):
        # build multiset: choose some 3-sets twice
        sh=[]
        while len(sh)<n:
            s=random.choice(shapes)
            if len(s[0])==3 and len(sh)<=n-2:
                s2=random.choice([x for x in shapes if x[0]==s[0]]); sh+= [s,s2]
            elif len(s[0])==2: sh.append(s)
        sh=sh[:n]
        if not ok_pairing(sh) or not covers(sh): continue
        tries+=1
        r=fit(sh)
        if r<1e-7:
            hits+=1; found.setdefault(n,sh)
            print('n',n,'EXACT',sh,flush=True); break
    print('n',n,'covering pair-ok candidates tried',tries,'exact found',hits,flush=True)
