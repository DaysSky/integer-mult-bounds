from e8 import *
import pickle, itertools
from collections import Counter, defaultdict
PS=pickle.load(open('portspans.pkl','rb'))
pidx={p:i for i,p in enumerate(P)}
def members(B):
    Sp=span(B); return tuple(sorted(pidx[x] for x in Sp if x in pidx))
dist=Counter(); big=[]
for B in PS[4]:
    m=members(B); dist[len(m)]+=1
    if len(m)>=5: big.append((B,m))
print('ports per 4-dim port-spanned space:', sorted(dist.items()))
# rank-1 blocks with |S|>=5 : for each big A, subsets S (|S|>=5), targets legal to all S grouped by normalized sign pattern
Nsgn=np.sign(N).astype(int)
best=Counter(); examples={}
for B,m in big:
    for k in range(5,len(m)+1):
        for S in itertools.combinations(m,k):
            Q=[t for t in range(V) if LEG[t,list(S)].all()]
            groups=defaultdict(list)
            for t in Q:
                row=tuple(Nsgn[t,list(S)])
                if row[0]<0: row=tuple(-x for x in row)
                groups[row].append(t)
            for g in groups.values():
                # need Q subset spanning <=4 dims: take the group, check span
                d=len(basis([P[t] for t in g]))
                key=(k,len(g),d)
                best[key]+=1
                if key not in examples: examples[key]=(S,g)
for key in sorted(best, key=lambda x:(-x[0]*x[1],x)):
    if key[2]<=4: print('S',key[0],'Q',key[1],'spanQ',key[2],'count',best[key])
