import math
from scipy.optimize import brentq
from ceil_a import idle_slots
def X(s,h,k,x,a,idle=True,copy=True):
    K=(s-1)//2; m=k+s*a; slots=[(2*s*a,a)]
    if copy: slots.append((s*x,h))
    if idle:
        for r in idle_slots(K,a): slots.append((2*r,max(r,h)))
    D=(s-1)*k-s*x
    if D<=0: return 0
    F=lambda q: sum(ms*((m/c)**q-1) for ms,c in slots if c<m)-D
    if F(0.5)<0: return 0.5
    return brentq(F,1e-12,0.5)
for idle in (True,False):
    best=max((X(s,8,1,63/111,7,idle),s) for s in range(3,201,2))
    print('idle',idle,'best',best)
