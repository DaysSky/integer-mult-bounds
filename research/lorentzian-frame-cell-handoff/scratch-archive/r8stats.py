import sys, os, json, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
import lw
from lw import V, g, bits, FULL
HYP=g.HYP; pc=lambda m: bin(m).count('1')
DET, POOL = sys.argv[1], sys.argv[2]
D=json.load(open(DET)); sel={int(k):v for k,v in D['sel'].items()}; det=D['det']
cov=pickle.load(open(POOL,'rb')); n=11
def img_line(s, perm): return g.idx[(g.kind[s], tuple(sorted(perm[i] for i in g.supp[s])))]
rot=[img_line(s,[(i+1)%n for i in range(n)]) for s in range(V)]
rotp=[list(range(V))]
for k in range(1,n): rotp.append([rot[x] for x in rotp[-1]])
def rotm(m,k):
    r=0
    for s in bits(m): r|=1<<rotp[k%n][s]
    return r
orb={}; reps=[]
for s in range(V):
    if s in orb: continue
    reps.append(s); x=s
    for k in range(n): orb[x]=(len(reps)-1,k); x=rot[x]
asg=collections.defaultdict(int)
for key,val in det['assign'].items():
    ri,i,u=map(int,key.split(','))
    if val: asg[(ri,i)]|=1<<u
PM={}
def pm(m):
    r=PM.get(m)
    if r is None:
        r=FULL
        for s in bits(m): r&=HYP[s]
        PM[m]=r
    return r
users=collections.defaultdict(list)
for t in range(V):
    o,k=orb[t]
    Fs=[rotm(F,k) for F in cov[reps[o]][sel[reps[o]]]]
    for j in range(4):
        users[pm(Fs[j])].append((t, rotm(asg[(o,j)],k), j==det['cin'][o].index(1), Fs[j]))
print('nodes', len(users), 'users/node', sorted(collections.Counter(len(u) for u in users.values()).items()))
print('node sizes', sorted(collections.Counter(pc(S) for S in users).items()))
print('node ranks', sorted(collections.Counter(lw.dim(S) for S in users).items()))
# distinct parts per node, delivered users, rank of delivered parts
st=collections.Counter(); rk=collections.Counter(); psz=collections.Counter()
import numpy as np
def rank2(vs):
    b=[]; 
    for v in vs:
        for x in b:
            if v ^ x < v: v ^= x
        if v:
            b.append(v); b.sort(reverse=True)
    return len(b)
deliv=0; inch=0; tot_need=0
for S,us in users.items():
    dl=[p for (t,p,ic,F) in us if not ic]; il=[p for (t,p,ic,F) in us if ic]
    deliv+=len(dl); inch+=len(il)
    r=rank2(dl); rall=rank2(dl+il)
    st[(len(dl),len(il),len(set(dl)),r,rall)]+=1
    for p in dl+il: psz[pc(p)]+=1
    tot_need += max(len(dl), rall)
print('delivered', deliv, 'inchain', inch)
for k,v in sorted(st.items()): print(' (deliv, inch, distinct deliv, rank deliv, rank all)', k, v)
print('part sizes', sorted(psz.items())[:40])
print('section-level registers needed (max(deliv, rank all)) summed:', tot_need)
