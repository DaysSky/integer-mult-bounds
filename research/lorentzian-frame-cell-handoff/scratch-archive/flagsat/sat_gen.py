"""Generic flag-space relaxation SAT (full non-abelian bit flag model, payload F_2).
usage: sat_gen.py DATA.pkl W S LAYERS_PER_BLOCK
DATA.pkl: nf, i0, gens (list of perms for free generators), paid (perms), cellT
Each free block = LAYERS elementary layers; each layer selects one of: identity, row op r_i += r_j,
or a free generator applied to one register.  Paid op = one paid perm applied to register 0."""
import pickle, sys, itertools, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
D=pickle.load(open(sys.argv[1],'rb')); NF=D['nf']; i0=D['i0']; GENS=D['gens']; PAID=D['paid']; CELL=set(D['cellT'])
W=int(sys.argv[2]); S=int(sys.argv[3]); L=int(sys.argv[4])
pool=IDPool(); cl=[]
def inv(p):
    q=[0]*len(p)
    for i,j in enumerate(p): q[j]=i
    return q
GENSi=[inv(p) for p in GENS]; PAIDi=[inv(p) for p in PAID]
def onehot(n):
    v=[pool.id() for _ in range(n)]
    cl.extend(CardEnc.equals(lits=v,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    return v
def eq(s,a,b): cl.append([-s,-a,b]); cl.append([-s,a,-b])
def xor2(s,o,a,b):
    for x in (0,1):
        for y in (0,1):
            cl.append([-s]+[(-a if x else a),(-b if y else b)]+([o] if (x^y) else [-o]))
def layer(X):
    opts=[('id',)]+[('row',i,j) for i in range(W) for j in range(W) if i!=j]+[('gen',r,g) for r in range(W) for g in range(len(GENSi))]
    sel=onehot(len(opts))
    Y=[[[pool.id() for f in range(NF)] for c in range(W)] for r in range(W)]
    for o,s in zip(opts,sel):
        for r in range(W):
            for c in range(W):
                for f in range(NF):
                    if o[0]=='row' and o[1]==r: xor2(s,Y[r][c][f],X[r][c][f],X[o[2]][c][f])
                    elif o[0]=='gen' and o[1]==r: eq(s,Y[r][c][f],X[r][c][GENSi[o[2]][f]])
                    else: eq(s,Y[r][c][f],X[r][c][f])
    return Y
def paid_layer(X):
    sel=onehot(len(PAIDi)); Y=[row[:] for row in X]
    Y[0]=[[pool.id() for f in range(NF)] for c in range(W)]
    for k,pi in enumerate(PAIDi):
        for c in range(W):
            for f in range(NF): eq(sel[k],Y[0][c][f],X[0][c][pi[f]])
    return Y
t0=time.time()
X=[[[pool.id() for f in range(NF)] for c in range(W)] for r in range(W)]
for r in range(W):
    for c in range(W):
        for f in range(NF): cl.append([X[r][c][f]] if (r==c and f==i0) else [-X[r][c][f]])
def block(X):
    for _ in range(L): X=layer(X)
    return X
X=block(X)
for s in range(S):
    X=paid_layer(X); X=block(X)
z=[[pool.id() for c in range(W)] for r in range(W)]
for r in range(W):
    for c in range(W):
        bits=X[r][c]; cl.append([-z[r][c]]+bits)
        for f in range(NF):
            cl.append([z[r][c],-bits[f]])
            if f not in CELL: cl.append([-bits[f]])
        cl.extend(CardEnc.atmost(lits=[bits[f] for f in CELL],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    cl.extend(CardEnc.equals(lits=z[r],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
for c in range(W):
    cl.extend(CardEnc.equals(lits=[z[r][c] for r in range(W)],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
print(sys.argv[1:],'vars',pool.top,'clauses',len(cl),round(time.time()-t0,1),flush=True)
sol=Cadical153(bootstrap_with=cl); res=sol.solve()
print('SAT' if res else 'UNSAT',round(time.time()-t0,1),flush=True)
if res: pickle.dump(sol.get_model(),open('model_gen_%s_%s_%s.pkl'%(W,S,L),'wb'))
