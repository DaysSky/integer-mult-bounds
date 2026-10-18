"""Combine the per-block census into the minimum total helper count over all puncture sets P (9 eligible lines, one per
4-frame automatically, classes affinely independent, lines 0..7 live)."""
import sys,itertools,pickle,collections
sys.path.insert(0,'/tmp/claude-0/-home-user-integer-mult-bounds/45552e66-7196-5fbb-857a-ded5e6dbacae/scratchpad/p111s')
from loc import *
GI=e8.GI
BROW=[sum((int(GI[t,b])&1)<<b for b in range(V)) for t in range(V)]
def rank(vecs):
    basis=[]
    for v in vecs:
        for b in basis: v=min(v,v^b)
        if v: basis.append(v)
    return len(basis)
out=pickle.load(open(sys.argv[1],'rb'))
EL=[p for p in ELIG if p>=8]
pairs=[(0,1),(2,4),(3,5),(6,9),(7,8)]
pc={}
missing=0
for X,Y in pairs:
    el=[p for p in EL if G.blk[p] in (X,Y)]
    for k in range(len(el)+1):
        for S in itertools.combinations(el,k):
            tot=0
            for B in (X,Y):
                r=out.get((B,S))
                if r is None or r[0] is None: tot=None; break
                tot+=r[0][0]
            if tot is None: missing+=1; continue
            pc[(X,S)]=tot
print('pair subsets evaluated',len(pc),'missing',missing)
res=[]
for P in itertools.combinations(EL,9):
    if rank([(1<<V)|BROW[p] for p in P])!=9: continue
    tot=0
    for X,Y in pairs:
        S=tuple(p for p in P if G.blk[p] in (X,Y))
        if (X,S) not in pc: tot=None; break
        tot+=pc[(X,S)]
    if tot is not None: res.append((tot,P))
res.sort()
print('affine-OK puncture sets fully evaluated',len(res))
print('min extra+junk',res[0][0] if res else None,'-> R',429+res[0][0] if res else None)
print(collections.Counter(t for t,_ in res).most_common()[:8] if res else '')
for t,P in res[:10]: print(t,P,[G.blk[p] for p in P])
