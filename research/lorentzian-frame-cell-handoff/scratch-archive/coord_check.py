import sys, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lbuild')
import lw
from lw import g, V, bits, nondegenerate, FULL
from fastcl import fclosure
pc=lambda m: bin(m).count('1')
HYP=g.HYP
def Lset(S):
    m=0
    for a,b in itertools.combinations(sorted(S),2): m|=1<<g.P(a,b)
    for a,b,c in itertools.combinations(sorted(S),3): m|=1<<g.T(a,b,c)
    return m
def Kset(a,S):
    m=0
    for x,y in itertools.combinations(sorted(S),2): m|=(1<<g.P(x,y))|(1<<g.T(a,x,y))
    return m
def St(z,S):
    m=0
    for y in S: m|=1<<g.P(z,y)
    for x,y in itertools.combinations(sorted(S),2): m|=1<<g.T(z,x,y)
    return m
def Tpair(a,b,S):
    m=0
    for x in S: m|=1<<g.T(a,b,x)
    return m
N=11
a,b,c=0,1,2
S8=[i for i in range(N) if i not in (a,b,c)]
Na=Kset(a,S8)|(1<<g.P(b,c))
F=fclosure(Na); print('Na', pc(Na), 'closure', pc(F), lw.dim(F), 'nondeg', nondegenerate(F), 'inside HYP', F & ~HYP[g.T(a,b,c)]==0, 'closure==Na', F==Na)
K=Kset(a,S8); FK=fclosure(K); print('K_a(S8)', pc(K), pc(FK), lw.dim(FK), nondegenerate(FK))
tot=0
for x,(y,z) in ((a,(b,c)),(b,(a,c)),(c,(a,b))): tot^=Kset(x,S8)|(1<<g.P(y,z))
print('T top ok', tot==HYP[g.T(a,b,c)])
for k in range(3,10):
    S=list(range(k)); m=Kset(10,S); Fm=fclosure(m)
    print(' K_10(|S|=%d)'%k, pc(m), pc(Fm), lw.dim(Fm), nondegenerate(Fm), Fm==m)
# P target
a,b=0,1; S9=[i for i in range(N) if i not in (a,b)]
z,w=2,3; S8=[i for i in S9 if i!=z]; S7=[i for i in S8 if i!=w]
L8=Lset(S8); X1=St(z,S7); X2=(1<<g.P(z,w))|Tpair(z,w,S7)|Tpair(a,b,S9)
t=g.P(a,b)
print('P top ok', (L8^X1^X2)==HYP[t], 'disjoint', L8&X1==0 and L8&X2==0 and X1&X2==0)
for nm,m in (('L8',L8),('X1',X1),('X2',X2)):
    Fm=fclosure(m); print(nm, pc(m), 'closure', pc(Fm), lw.dim(Fm), 'nondeg', nondegenerate(Fm), 'in HYP', Fm&~HYP[t]==0)
