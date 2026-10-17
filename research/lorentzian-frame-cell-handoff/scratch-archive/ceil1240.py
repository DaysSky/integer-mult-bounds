from math import log
m=73; w=896/9; c=64
local={1:2412,2:418,3:432,4:142,5:82,8:8}
def relax(a,R,u=1,cc=c,loc=local):
    mass=sum(r*n for r,n in loc.items())
    idle=(m-u)*w+cc-mass
    s=sum(n*(r/m)**(1-a) for r,n in loc.items())+idle/R*(R/m)**(1-a)
    return s/w
def root(R,**kw):
    lo,hi=0.0,0.5
    for _ in range(100):
        mid=(lo+hi)/2
        if relax(mid,R,**kw)<1: lo=mid
        else: hi=mid
    return lo
for R in (51,60,64,68,72):
    a=root(R); print('R',R,'a*',round(a,6),'kappa',round(a/(1+a),6))
print('local as rank-8, R=72:', root(72,loc={8:5586/8}))
print('centre free, R=72:', root(72,cc=0))
