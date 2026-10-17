import numpy as np, itertools, pickle
# E8 roots in doubled coordinates (integers), true inner product = dot/4
R=[]
for i,j in itertools.combinations(range(8),2):
    for si in (2,-2):
        for sj in (2,-2):
            v=[0]*8; v[i]=si; v[j]=sj; R.append(v)
for signs in itertools.product((1,-1),repeat=8):
    if signs.count(-1)%2==0: R.append(list(signs))
R=np.array(R); assert len(R)==240
G=R@R.T//4
# lines: pick representative with first nonzero positive
lines=[]
seen=set()
for a in range(240):
    if a in seen: continue
    b=[x for x in range(240) if (R[x]==-R[a]).all()][0]
    seen.add(a); seen.add(b); lines.append(a)
L=R[lines]; GL=L@L.T//4  # 120x120, diag 2
n=len(lines)
frames=[(a,b) for a in range(n) for b in range(a+1,n) if GL[a,b]==0]
print('lines',n,'frames',len(frames))
F=np.array(frames)
# cross products
A=F[:,0];B=F[:,1]
def cross(i):
    a,b=frames[i]
    return GL[a][:,None]*0
# vectorized: P[t,s] = sum of 4 products
gA=GL[A][:,A]; gAB=GL[A][:,B]; gBA=GL[B][:,A]; gB=GL[B][:,B]
tot=gA+gAB+gBA+gB
orth=(gA==0)&(gAB==0)&(gBA==0)&(gB==0)
odd=(tot%2!=0)
comp=orth|odd
np.fill_diagonal(comp,False)
deg=comp.sum(1)
print('compat degree min/max',deg.min(),deg.max(),'density',comp.mean())
print('orth deg',orth.sum(1)[0],'odd deg',(odd&~orth).sum(1)[0])
pickle.dump(dict(L=L,GL=GL,frames=frames,comp=comp,orth=orth),open('e8f.pkl','wb'))
