import pickle, sys, numpy as np, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V
punct = pickle.load(open(sys.argv[1],'rb'))[1] if len(sys.argv)>1 and sys.argv[1]!='full' else []
live=sorted(set(range(V))-set(punct))
def vec(u):
    x=np.zeros(12)
    if g.kind[u]=='P':
        a,b=sorted(g.supp[u]); x[a]=1; x[b]=-1
    else:
        for i in g.supp[u]: x[i]=1
        x[11]=1
    return x
VV=np.array([vec(u) for u in range(V)])
D10=[]
for h in range(11):
    D10.append(frozenset(u for u in live if (g.kind[u]=='P' and h not in g.supp[u]) or (g.kind[u]=='T' and h in g.supp[u])))
res=[]
for mask in range(1,2048):
    s=set()
    for h in range(11):
        if mask>>h&1: s^=D10[h]
    rk=np.linalg.matrix_rank(VV[sorted(s)]) if s else 0
    res.append((rk,len(s),mask))
cnt=collections.Counter(r for r,_,_ in res)
print('live',len(live),'rank distribution of the 2047 combos:',sorted(cnt.items()))
# min-weight basis (greedy over F2 independence of masks)
res.sort()
basis=[]; piv={}
def indep(m):
    x=m
    for b in sorted(piv,reverse=True):
        if x>>b&1: x^=piv[b]
    return x
tot=0
for rk,sz,m in res:
    x=indep(m)
    if x:
        piv[x.bit_length()-1]=x; basis.append((rk,sz,m)); tot+=rk
    if len(basis)==11: break
print('min-rank basis: total rank (cst) =',tot,[(r,s) for r,s,_ in basis])
