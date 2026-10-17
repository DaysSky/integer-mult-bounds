"""Sparse low-rank decoders for the E8 bit unit (120 root lines, E8 form).
Find U,V in F_2^{120 x c}: <u_T,v_T>=1, <u_S,v_T>=0 for non-orthogonal pairs (both orders), and at most k
off-diagonal ones per row of B (B_TS=<v_T,u_S>, only orthogonal pairs can be 1).  usage: sparsedec.py c k [sym]"""
import pickle, sys, time, numpy as np
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
d=pickle.load(open('e8f.pkl','rb')); GL=d['GL']; n=GL.shape[0]
c=int(sys.argv[1]); k=int(sys.argv[2]); sym=len(sys.argv)>3 and sys.argv[3]=='sym'
pool=IDPool(); sol=Cadical153(); nc=[0]
def add(cl): sol.add_clause(cl); nc[0]+=1
U=[[pool.id() for _ in range(c)] for _ in range(n)]
V=U if sym else [[pool.id() for _ in range(c)] for _ in range(n)]
def AND(a,b):
    z=pool.id(); add([-z,a]); add([-z,b]); add([z,-a,-b]); return z
def XOR(a,b):
    z=pool.id(); add([-z,a,b]); add([-z,-a,-b]); add([z,-a,b]); add([z,a,-b]); return z
def par(lits):
    acc=lits[0]
    for l in lits[1:]: acc=XOR(acc,l)
    return acc
B={}
for T in range(n):
    add([par([AND(V[T][j],U[T][j]) for j in range(c)])])
for T in range(n):
    for S in range(n):
        if S==T: continue
        b=par([AND(V[T][j],U[S][j]) for j in range(c)])
        if GL[T,S]!=0: add([-b])
        else: B[(T,S)]=b
for T in range(n):
    lits=[B[(T,S)] for S in range(n) if (T,S) in B]
    for cl in CardEnc.atmost(lits=lits,bound=k,vpool=pool,encoding=EncType.seqcounter).clauses: add(cl)
# gauge: an orthogonal 8-clique? use a pairwise NON-orthogonal set K (B[K,K]=I) of size min(c, |K|)
# greedy pairwise non-orthogonal set
K=[]
for T in range(n):
    if all(GL[T,S]!=0 for S in K): K.append(T)
K=K[:c]
for i,T in enumerate(K):
    for j in range(c):
        add([U[T][j]] if j==i else [-U[T][j]])
        if not sym and len(K)==c: add([V[T][j]] if j==i else [-V[T][j]])
t0=time.time()
print('c',c,'k',k,'sym',sym,'|K|',len(K),'vars',pool.top,'clauses',nc[0],flush=True)
res=sol.solve()
print('SAT' if res else 'UNSAT',round(time.time()-t0,1),flush=True)
if res:
    m=set(l for l in sol.get_model() if l>0)
    Bm=np.zeros((n,n),dtype=int)
    for T in range(n):
        Bm[T,T]=1
    for (T,S),b in B.items(): Bm[T,S]=1 if b in m else 0
    print('row nonzeros (offdiag):',sorted(set((Bm.sum(1)-1).tolist())))
    pickle.dump(Bm,open('sparsedec_c%d_k%d%s.pkl'%(c,k,'_sym' if sym else ''),'wb'))
