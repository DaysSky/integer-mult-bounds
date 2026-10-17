"""Relaxation SAT with payload F_3 (coefficients 0,1,2 encoded by two bits a='1', b='2').
usage: sat_p3.py DATA.pkl W S L    (points/gens/paid/cellT from mkgr*/mkgens; paid on any register)"""
import pickle, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
D=pickle.load(open(sys.argv[1],'rb')); NF=D['nf']; i0=D['i0']; GENS=D['gens']; PAID=D['paid']; CELL=set(D['cellT'])
W=int(sys.argv[2]); S=int(sys.argv[3]); L=int(sys.argv[4])
pool=IDPool(); sol=Cadical153(); nc=[0]
def add(c): sol.add_clause(c); nc[0]+=1
def inv(p):
    q=[0]*len(p)
    for i,j in enumerate(p): q[j]=i
    return q
GENSi=[inv(p) for p in GENS]; PAIDi=[inv(p) for p in PAID]
def onehot(n):
    v=[pool.id() for _ in range(n)]
    for c in CardEnc.equals(lits=v,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses: add(c)
    return v
def newvar():
    a,b=pool.id(),pool.id(); add([-a,-b]); return (a,b)
def newrow(): return [[newvar() for f in range(NF)] for c in range(W)]
def isv(x,v):   # list of literals whose conjunction means x==v
    a,b=x
    return [-a,-b] if v==0 else ([a] if v==1 else [b])
def notv(x,v):  # clause-literals meaning x!=v
    a,b=x
    return [a,b] if v==0 else ([-a] if v==1 else [-b])
def force(guard,y,w):  # guard-literals (list, all must hold) -> y==w
    for lit in isv(y,w): add([-g for g in guard]+[lit])
def copy(sel_neg,y,x):  # (OR of sel_neg false) -> y==x ; sel_neg: list of selector lits that, if any true, disable
    for v in range(3):
        for lit in isv(y,v): add(sel_neg+notv(x,v)+[lit])
def layer(X):
    opts=[('id',)]
    for i in range(W):
        for j in range(W):
            if i!=j: opts+= [('row',i,j,1),('row',i,j,2)]
    for i in range(W):
        for j in range(i+1,W): opts.append(('swap',i,j))
    for i in range(W): opts.append(('neg',i))
    for r in range(W):
        for g in range(len(GENSi)): opts.append(('gen',r,g))
    sel=onehot(len(opts)); Y=[newrow() for r in range(W)]
    for r in range(W):
        touch=[k for k,o in enumerate(opts) if o[0]!='id' and (o[1]==r or (o[0]=='swap' and o[2]==r))]
        tl=[sel[k] for k in touch]
        for c in range(W):
            for f in range(NF): copy(tl,Y[r][c][f],X[r][c][f])
        for k in touch:
            o=opts[k]; s=sel[k]
            for c in range(W):
                for f in range(NF):
                    y=Y[r][c][f]; x=X[r][c][f]
                    if o[0]=='swap':
                        copy([-s],y,X[o[2] if o[1]==r else o[1]][c][f])
                    elif o[0]=='neg':
                        for v in range(3):
                            for lit in isv(y,(2*v)%3): add([-s]+notv(x,v)+[lit])
                    elif o[0]=='gen':
                        copy([-s],y,X[r][c][GENSi[o[2]][f]])
                    else:
                        z=X[o[2]][c][f]; lam=o[3]
                        for vx in range(3):
                            for vz in range(3):
                                w=(vx+lam*vz)%3
                                for lit in isv(y,w): add([-s]+notv(x,vx)+notv(z,vz)+[lit])
    return Y
def paid_layer(X):
    sel=onehot(W*len(PAIDi)); Y=[newrow() for r in range(W)]
    for r in range(W):
        mine=sel[r*len(PAIDi):(r+1)*len(PAIDi)]
        for c in range(W):
            for f in range(NF): copy(mine,Y[r][c][f],X[r][c][f])
        for k,pi in enumerate(PAIDi):
            for c in range(W):
                for f in range(NF): copy([-mine[k]],Y[r][c][f],X[r][c][pi[f]])
    return Y
t0=time.time()
X=[newrow() for r in range(W)]
for r in range(W):
    for c in range(W):
        for f in range(NF):
            for lit in isv(X[r][c][f],1 if (r==c and f==i0) else 0): add([lit])
def block(X):
    for _ in range(L): X=layer(X)
    return X
X=block(X)
for s in range(S): X=paid_layer(X); X=block(X)
z=[[pool.id() for c in range(W)] for r in range(W)]
for r in range(W):
    for c in range(W):
        nzs=[]
        for f in range(NF):
            a,b=X[r][c][f]; nz=pool.id(); add([-nz,a,b]); add([nz,-a]); add([nz,-b]); nzs.append(nz)
            add([z[r][c],-nz])
            if f not in CELL: add([-nz])
        add([-z[r][c]]+nzs)
        for cc in CardEnc.atmost(lits=[nzs[f] for f in CELL],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses: add(cc)
    for cc in CardEnc.equals(lits=z[r],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses: add(cc)
for c in range(W):
    for cc in CardEnc.equals(lits=[z[r][c] for r in range(W)],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses: add(cc)
print(sys.argv[1:],'vars',pool.top,'clauses',nc[0],round(time.time()-t0,1),flush=True)
res=sol.solve()
print('SAT' if res else 'UNSAT',round(time.time()-t0,1),flush=True)
if res: pickle.dump(sol.get_model(),open('model_p3_%s_%s_%s.pkl'%(W,S,L),'wb'))
