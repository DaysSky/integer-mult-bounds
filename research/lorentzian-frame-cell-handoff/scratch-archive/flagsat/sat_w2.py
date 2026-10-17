"""Flag-space relaxation of the full (non-abelian) bit flag model, m=2, over F_2 frames, payload F_2.
W registers, S paid rank-1 upper transvections (cost 1 each). Is there a word reaching a monomial
state whose nonzero entries are single flags in the target cell C(w_T)?  (necessary condition)"""
import pickle, sys, itertools, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
D=pickle.load(open('f2.pkl','rb')); NF=D['nf']; i0=D['i0']; FREE=D['free']; PAID=D['paid']; CELL=set(D['cellT'])
W=int(sys.argv[1]); S=int(sys.argv[2]); ROUNDS=int(sys.argv[3]) if len(sys.argv)>3 else 2
pool=IDPool(); cl=[]
def newstate():
    return [[[pool.id() for f in range(NF)] for c in range(W)] for r in range(W)]
def inv(p):
    q=[0]*len(p)
    for i,j in enumerate(p): q[j]=i
    return q
FREEi=[inv(p) for p in FREE]; PAIDi=[inv(p) for p in PAID]
def onehot(n):
    v=[pool.id() for _ in range(n)]
    cl.extend(CardEnc.equals(lits=v,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    return v
def perm_layer(X,r,perms_inv,sel=None):
    Y=[row[:] for row in X]; Y=[[col for col in row] for row in Y]
    Y[r]=[[pool.id() for f in range(NF)] for c in range(W)]
    if sel is None: sel=onehot(len(perms_inv))
    for k,pi in enumerate(perms_inv):
        s=sel[k]
        for c in range(W):
            for f in range(NF):
                a=Y[r][c][f]; b=X[r][c][pi[f]]
                cl.append([-s,-a,b]); cl.append([-s,a,-b])
    return Y
# GL_W(F_2) mixing matrices
mats=[]
for bits in itertools.product((0,1),repeat=W*W):
    M=[list(bits[i*W:(i+1)*W]) for i in range(W)]
    # invertible over F2?
    A=[row[:] for row in M]; rk=0; cols=W
    for c in range(cols):
        p=next((i for i in range(rk,W) if A[i][c]),None)
        if p is None: continue
        A[rk],A[p]=A[p],A[rk]
        for i in range(W):
            if i!=rk and A[i][c]: A[i]=[(x+y)%2 for x,y in zip(A[i],A[rk])]
        rk+=1
    if rk==W: mats.append(M)
def xor_eq(out,ins,guard):
    # guard -> out = XOR(ins)
    n=len(ins)
    for bits in itertools.product((0,1),repeat=n):
        par=sum(bits)%2
        # forbid assignment ins=bits, out!=par
        clause=[-guard]+[(-x if b else x) for x,b in zip(ins,bits)]+([-out] if par==0 else [out])
        cl.append(clause)
def mix_layer(X):
    Y=newstate(); sel=onehot(len(mats))
    for k,M in enumerate(mats):
        for r in range(W):
            srcs=[i for i in range(W) if M[r][i]]
            for c in range(W):
                for f in range(NF):
                    xor_eq(Y[r][c][f],[X[i][c][f] for i in srcs],sel[k])
    return Y
def free_block(X):
    X=mix_layer(X)
    for _ in range(ROUNDS):
        for r in range(W): X=perm_layer(X,r,FREEi)
        X=mix_layer(X)
    return X
t0=time.time()
X=newstate()
for r in range(W):
    for c in range(W):
        for f in range(NF): cl.append([X[r][c][f]] if (r==c and f==i0) else [-X[r][c][f]])
X=free_block(X)
for s in range(S):
    X=perm_layer(X,0,PAIDi)        # paid op on register 0 (mixings make this WLOG)
    X=free_block(X)
# final: monomial, single flag in CELL
z=[[pool.id() for c in range(W)] for r in range(W)]
for r in range(W):
    for c in range(W):
        bits=X[r][c]
        cl.append([-z[r][c]]+bits)
        for f in range(NF):
            cl.append([z[r][c],-bits[f]])
            if f not in CELL: cl.append([-bits[f]])
        cl.extend(CardEnc.atmost(lits=[bits[f] for f in CELL],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    cl.extend(CardEnc.equals(lits=z[r],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
for c in range(W):
    cl.extend(CardEnc.equals(lits=[z[r][c] for r in range(W)],bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
print('W',W,'S',S,'rounds',ROUNDS,'vars',pool.top,'clauses',len(cl),round(time.time()-t0,1),flush=True)
sol=Cadical153(bootstrap_with=cl)
res=sol.solve()
print('SAT' if res else 'UNSAT', round(time.time()-t0,1))
if res:
    pickle.dump(sol.get_model(),open('model_w%d_s%d.pkl'%(W,S),'wb'))
