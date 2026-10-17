"""Decoder of the E8 bit pattern with small corrector span.
B = U V^T over F2 (U,V: 120 x n), B_TT=1, B_TS=0 for non-orthogonal pairs, and for each target T the correctors
{S != T : B_TS = 1} lie in one subspace W chosen (selector) from menu subs_TYPE.pkl[T].
usage: corrsat.py TYPE n [sym]   -> saves corr_TYPE_n.pkl with U,V,B, chosen W per T."""
import pickle, sys, time, numpy as np
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
d=pickle.load(open('../k2/e8f.pkl','rb')); G=d['GL']; nl=120
typ=sys.argv[1]; n=int(sys.argv[2]); sym=len(sys.argv)>3 and sys.argv[3]=='sym'
menu=pickle.load(open('subs_%s.pkl'%typ,'rb'))
pool=IDPool(); sol=Cadical153(); nc=[0]
def add(cl): sol.add_clause(cl); nc[0]+=1
U=[[pool.id() for _ in range(n)] for _ in range(nl)]
V=U if sym else [[pool.id() for _ in range(n)] for _ in range(nl)]
def AND(a,b):
    z=pool.id(); add([-z,a]); add([-z,b]); add([z,-a,-b]); return z
def XOR(a,b):
    z=pool.id(); add([-z,a,b]); add([-z,-a,-b]); add([z,-a,b]); add([z,a,-b]); return z
def par(l):
    acc=l[0]
    for x in l[1:]: acc=XOR(acc,x)
    return acc
sel={}
for T in range(nl):
    sel[T]=[pool.id() for _ in menu[T]]
    for c in CardEnc.equals(lits=sel[T],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses: add(c)
B={}
for T in range(nl):
    add([par([AND(U[T][j],V[T][j]) for j in range(n)])])
    for S in range(nl):
        if S==T: continue
        b=par([AND(U[T][j],V[S][j]) for j in range(n)])
        if G[T,S]!=0: add([-b])
        else:
            B[(T,S)]=b
            allowed=[sel[T][w] for w,W in enumerate(menu[T]) if S in W]
            add([-b]+allowed)
# gauge on a pairwise non-orthogonal set
K=[]
for T in range(nl):
    if all(G[T,S]!=0 for S in K): K.append(T)
K=K[:n]
for i,T in enumerate(K):
    for j in range(n):
        add([U[T][j]] if j==i else [-U[T][j]])
print(typ,'n',n,'sym',sym,'menu sizes',sorted(set(len(m) for m in menu.values())),'vars',pool.top,'clauses',nc[0],flush=True)
t0=time.time(); r=sol.solve(); print('SAT' if r else 'UNSAT',round(time.time()-t0,1),flush=True)
if r:
    m=set(l for l in sol.get_model() if l>0)
    Um=np.array([[1 if U[T][j] in m else 0 for j in range(n)] for T in range(nl)])
    Vm=np.array([[1 if V[T][j] in m else 0 for j in range(n)] for T in range(nl)])
    Bm=(Um@Vm.T)%2
    ch={T:[w for w in range(len(menu[T])) if sel[T][w] in m] for T in range(nl)}
    print('row weights',sorted(set((Bm.sum(1)-1).tolist())))
    pickle.dump(dict(U=Um,V=Vm,B=Bm,ch=ch,typ=typ),open('corr_%s_%d%s.pkl'%(typ,n,'_sym' if sym else ''),'wb'))
