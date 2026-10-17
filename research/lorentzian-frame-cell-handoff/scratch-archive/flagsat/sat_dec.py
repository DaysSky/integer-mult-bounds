"""Mixed-characteristic flag relaxation: frames over F_q (radix q odd, data file gq.pkl), payload F_2.
usage: sat_mix.py gq.pkl W S L   (L elementary layers per free block). Clauses streamed into CaDiCaL."""
import pickle, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
D=pickle.load(open(sys.argv[1],'rb')); NF=D['nf']; i0=D['i0']; GENS=D['gens']; PAID=D['paid']; CELL=set(D['cellT'])
W=int(sys.argv[2]); S=int(sys.argv[3]); L=int(sys.argv[4])
pool=IDPool(); sol=Cadical153(); nc=[0]; LOG=[]
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
def newrow(): return [[pool.id() for f in range(NF)] for c in range(W)]
def layer(X):
    opts=[('id',)]+[('row',i,j) for i in range(W) for j in range(W) if i!=j]+[('swap',i,j) for i in range(W) for j in range(i+1,W)]+[('gen',r,g) for r in range(W) for g in range(len(GENSi))]
    sel=onehot(len(opts)); LOG.append(('layer',opts,sel)); Y=[newrow() for r in range(W)]
    for r in range(W):
        touch=[k for k,o in enumerate(opts) if o[0]!='id' and (o[1]==r or (o[0]=='swap' and o[2]==r))]
        # if no option touching row r is selected, row copies
        for c in range(W):
            for f in range(NF):
                a,b=Y[r][c][f],X[r][c][f]
                add([-a,b]+[sel[k] for k in touch]); add([a,-b]+[sel[k] for k in touch])
        for k in touch:
            o=opts[k]; s=sel[k]
            for c in range(W):
                for f in range(NF):
                    y=Y[r][c][f]; x=X[r][c][f]
                    if o[0]=='swap':
                        x2=X[o[2] if o[1]==r else o[1]][c][f]; add([-s,-y,x2]); add([-s,y,-x2])
                    elif o[0]=='row':
                        z=X[o[2]][c][f]
                        add([-s,-y,x,z]); add([-s,-y,-x,-z]); add([-s,y,-x,z]); add([-s,y,x,-z])
                    else:
                        x2=X[r][c][GENSi[o[2]][f]]; add([-s,-y,x2]); add([-s,y,-x2])
    return Y
def paid_layer(X):
    sel=onehot(W*len(PAIDi)); LOG.append(('paid',W,sel)); Y=[newrow() for r in range(W)]
    for r in range(W):
        mine=sel[r*len(PAIDi):(r+1)*len(PAIDi)]
        for c in range(W):
            for f in range(NF):
                a,b=Y[r][c][f],X[r][c][f]; add([-a,b]+mine); add([a,-b]+mine)
        for k,pi in enumerate(PAIDi):
            s=mine[k]
            for c in range(W):
                for f in range(NF):
                    y=Y[r][c][f]; x=X[r][c][pi[f]]; add([-s,-y,x]); add([-s,y,-x])
    return Y
t0=time.time()
X=[newrow() for r in range(W)]
for r in range(W):
    for c in range(W):
        for f in range(NF): add([X[r][c][f]] if (r==c and f==i0) else [-X[r][c][f]])
def block(X):
    for _ in range(L): X=layer(X)
    return X
X=block(X)
for s in range(S): X=paid_layer(X); X=block(X)
z=[[pool.id() for c in range(W)] for r in range(W)]
for r in range(W):
    for c in range(W):
        bits=X[r][c]; add([-z[r][c]]+bits)
        for f in range(NF):
            add([z[r][c],-bits[f]])
            if f not in CELL: add([-bits[f]])
        for cc in CardEnc.atmost(lits=[bits[f] for f in CELL],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses: add(cc)
    for cc in CardEnc.equals(lits=z[r],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses: add(cc)
for c in range(W):
    for cc in CardEnc.equals(lits=[z[r][c] for r in range(W)],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses: add(cc)
print(sys.argv[1:],'vars',pool.top,'clauses',nc[0],round(time.time()-t0,1),flush=True)
res=sol.solve()
print('SAT' if res else 'UNSAT',round(time.time()-t0,1),flush=True)
if res:
    mdl=set(l for l in sol.get_model() if l>0)
    out=[]
    for kind,o,sel in LOG:
        k=[i for i,s in enumerate(sel) if s in mdl][0]
        out.append((kind, o[k] if kind=='layer' else (k//len(PAIDi), k%len(PAIDi))))
    pickle.dump(out,open('word_%s_%s_%s_%s.pkl'%(sys.argv[1],W,S,L),'wb'))
    for x in out: print(x)
