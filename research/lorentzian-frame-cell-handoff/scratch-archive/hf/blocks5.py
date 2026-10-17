from e8 import *
import pickle, itertools
from collections import Counter, defaultdict
PS=pickle.load(open('portspans.pkl','rb'))
pidx={p:i for i,p in enumerate(P)}
Nsgn=np.sign(N).astype(int)
def members(B):
    Sp=span(B); return tuple(sorted(pidx[x] for x in Sp if x in pidx))
blocks=set()
for B in PS[4]:
    m=members(B)
    if len(m)<4: continue
    for k in range(4,len(m)+1):
        for S in itertools.combinations(m,k):
            Sl=list(S)
            Q=[t for t in range(V) if LEG[t,Sl].all()]
            if len(Q)<4: continue
            groups=defaultdict(list)
            for t in Q:
                row=tuple(Nsgn[t,Sl]); 
                if row[0]<0: row=tuple(-x for x in row)
                groups[row].append(t)
            for g in groups.values():
                if len(g)>=4 and len(basis([P[t] for t in g]))<=4 and len(g)*k>=20:
                    blocks.add((S,tuple(g)))
# keep maximal (not contained in another with same or larger both)
bl=sorted(blocks,key=lambda x:-len(x[0])*len(x[1]))
print('raw blocks area>=20 (Q span<=4):',len(bl), Counter((len(s),len(q)) for s,q in bl))
pickle.dump(bl,open('blocks5.pkl','wb'))
