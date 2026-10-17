"""Float version of #595 skel.X with the climb a decoupled from h-k (corrector rank d = a).
X(s,h,k,x,a): slots active 2sa@cap a, copies s*x@cap h, idle B_K slots (mass 2r @ cap max(r,h)); D=(s-1)k-s x; m=k+s a."""
import sys, math
from scipy.optimize import brentq
def idle_slots(K,a):
    sl=[]
    if 2*K-2>0: sl.append(a*(2*K-2))
    for p in range(1,K):
        sl+=[2*p*a,a]
        if 2*K-2*p-2>0: sl.append(a*(2*K-2*p-2))
    return sl
def X(s,h,k,x,a):
    K=(s-1)//2; m=k+s*a; slots=[]
    slots.append((2*s*a,a)); slots.append((s*x,h))
    for r in idle_slots(K,a): slots.append((2*r,max(r,h)))
    D=(s-1)*k-s*x
    if D<=0: return None
    F=lambda q: sum(ms*((m/c)**q-1) for ms,c in slots if c<m)-D
    if F(0.5)<0: return 0.5
    return brentq(F,1e-12,0.5)
def best(h,k,x,a):
    r=[(X(s,h,k,x,a) or 0,s) for s in range(3,61,2)]
    return max(r)
if __name__=='__main__':
    print('E8 check', best(8,1,63/111,7))
    for a in [7,6,5,4,3,2]:
        row=[]
        for x in [0.5676,0.6,0.7,0.8,0.9]:
            v,s=best(8,1,x,a); row.append('%.2e(s%d)'%(v,s))
        print('a',a,' '.join(row))
