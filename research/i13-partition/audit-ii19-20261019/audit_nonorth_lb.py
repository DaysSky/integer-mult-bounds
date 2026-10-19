"""Valid decoder lower bound: a set S of pairwise non-orthogonal lines forces B|SxS = I, so rank >= |S| and
cst >= |S|.  Randomized greedy + 1-swap local search for a large S (lower bound on the max)."""
import itertools, random
import numpy as np
roots=[]
for i in range(8):
    for j in range(i+1,8):
        for si in (1,-1):
            for sj in (1,-1):
                v=np.zeros(8); v[i]=si; v[j]=sj; roots.append(v)
half=[np.array(s,float)/2 for s in itertools.product([1,-1],repeat=8) if s.count(-1)%2==0]
def canon(v):
    for x in v:
        if x!=0: return tuple(v) if x>0 else tuple(-v)
d8={}
for r in roots+half: d8[canon(r)]=np.array(r)
R8=list(d8.values()); assert len(R8)==120
def system(kind):
    if kind=='361 (E8+U levels 0-1)':
        L=[list(a)+[0,0] for a in R8]+[list(a)+[1,0] for a in R8]+[list(a)+[0,1] for a in R8]+[[0]*8+[1,1]]
        E=np.eye(10); E[8,8]=E[9,9]=0; E[8,9]=E[9,8]=1
    elif kind=='2-class (a,0,0)/(a,1,0) h=10':
        L=[list(a)+[0,0] for a in R8]+[list(a)+[1,0] for a in R8]
        E=np.eye(10); E[8,8]=E[9,9]=0; E[8,9]=E[9,8]=1
    elif kind=='E8 alone (control: minrank 9)':
        L=[list(a) for a in R8]; E=np.eye(8)
    L=np.array(L,float); G=L@E@L.T
    return L, np.abs(G)>1e-9
def big_nonorth(N,iters=4000,seed=0):
    rnd=random.Random(seed); n=len(N); best=[]
    for it in range(iters):
        order=list(range(n)); rnd.shuffle(order); S=[]
        for x in order:
            if all(N[x,y] for y in S): S.append(x)
        # 1-swap improvement
        improved=True
        while improved:
            improved=False
            Sset=set(S)
            for x in range(n):
                if x in Sset: continue
                bad=[y for y in S if not N[x,y]]
                if len(bad)==0: S.append(x); Sset.add(x); improved=True
        if len(S)>len(best): best=S
    return best
for kind in ('E8 alone (control: minrank 9)','2-class (a,0,0)/(a,1,0) h=10','361 (E8+U levels 0-1)'):
    L,N=system(kind); v=len(L)
    S=big_nonorth(N)
    assert all(N[a,b] for a in S for b in S)
    print('%-34s v=%3d  pairwise-non-orthogonal set |S|=%3d  => cst >= %3d (x >= %.3f); h=10 tie needs x <= 0.45 (cst <= %d)'
          %(kind,v,len(S),len(S),len(S)/v,int(0.45*v)))
