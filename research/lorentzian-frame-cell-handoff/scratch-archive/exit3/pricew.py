"""Window-aware hosting MILP with arbitrary residual widths per call (same slot model as price_e1.py)."""
import sys, os
sys.path.insert(0,'/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
from mpmath import mpf
from ortools.linear_solver import pywraplp
a=7; K=4; L=9; v=111; T=32; m=1+L*a; W=2*K*v*T
SLOTS=[('p0post',42,range(3,9)),('p1pre',14,range(0,2)),('p1one',7,[2]),('p1post',28,range(5,9)),('p2pre',28,range(0,4)),('p2one',7,[4]),('p2post',14,range(7,9)),('p3pre',42,range(0,6)),('p3one',7,[6])]
def pats(cap,widths):
    out=[]
    def rec(i,rem,cnt):
        if i==len(widths): out.append(tuple(cnt)); return
        wd=widths[i]
        for k in range(rem//wd+1):
            rec(i+1,rem-k*wd,cnt+[k])
    rec(0,cap,[]); return out
def solve(widthcount,q):
    widths=sorted(widthcount)
    f=lambda r: 0.0 if r==0 else float(mpf(r)*((mpf(m)/r)**q-1))
    sv=pywraplp.Solver.CreateSolver('SCIP'); N=2*v
    x={}; y={}; obj=[]
    for s,(nm,cap,win) in enumerate(SLOTS):
        for pt in pats(cap,widths):
            x[s,pt]=sv.IntVar(0,N,'x'); obj.append(f(cap-sum(k*wd for k,wd in zip(pt,widths)))*x[s,pt])
        sv.Add(sum(x[s,pt] for (ss,pt) in x if ss==s)==N)
        for c in win:
            for wd in widths: y[s,c,wd]=sv.IntVar(0,10**6,'y')
        for i,wd in enumerate(widths):
            sv.Add(sum(y[s,c,wd] for c in win)==sum(pt[i]*x[s,pt] for (ss,pt) in x if ss==s))
    for c in range(L):
        for wd in widths:
            sv.Add(sum(y[s,c,wd] for s,(nm,cap,win) in enumerate(SLOTS) if c in win)==widthcount[wd])
    sv.Minimize(sum(obj)); sv.SetTimeLimit(600000)
    st=sv.Solve()
    if st not in (pywraplp.Solver.OPTIMAL,pywraplp.Solver.FEASIBLE): return None
    rem={}
    for (s,pt),var in x.items():
        k=int(round(var.solution_value())); r=SLOTS[s][1]-sum(kk*wd for kk,wd in zip(pt,widths))
        if k and r: rem[r]=rem.get(r,0)+k
    return rem, st==pywraplp.Solver.OPTIMAL
def price(local,widthcount):
    q=mpf('0.0017334')
    for it in range(12):
        out=solve(widthcount,q)
        if out is None: return None
        rem,opt=out; prof={}
        for r,z in local.items(): prof[r]=prof.get(r,0)+z*T*L
        for r,z in rem.items(): prof[r]=prof.get(r,0)+z*T
        q2=P.root(prof,m,W)
        if abs(q2-q)<mpf(10)**-26: break
        q=q2
    return q2,rem,opt
if __name__=='__main__':
    ref=mpf('0.001733427039589844')
    e1={1:1322,2:1342,3:79,4:44,5:102,6:11,7:19}
    c,rem,o=price(e1,{8:438,7:1}); print('E1 check',float(c),'%+.4f%%'%float((c/ref-1)*100),rem,o)
    e2=dict(e1); e2[1]+=1; e2[7]-=1
    c,rem,o=price(e2,{8:438,1:1}); print('E1 + early cleanup of h470 (width 1, rank-7 C climb -> rank-1)',float(c),'%+.4f%%'%float((c/ref-1)*100),rem,o)

def e1p():
    ref=mpf('0.001733427039589844')
    e1={1:1322,2:1342,3:79,4:44,5:102,6:11,7:19}
    e=dict(e1); e[1]-=1; e[3]-=1; e[2]+=2; e[7]-=1; e[6]+=1
    c,rem,o=price(e,{8:438,6:1}); print("E1' (h470 at frame 186, entrance rank 2, width 6)",float(c),'%+.4f%%'%float((c/ref-1)*100),rem,o)
