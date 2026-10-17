"""Rescheduled injections, regime S = {p} u Src (A section; X placed in A).  Exact conditions for a single X:
frames nested for g, p and every source at its chosen chain position; X's predecessors P (g_k, p_j, x_i) and
successors Q (g_{k+1}, p_{j+1}, x_{i+1}; touches in A only) admit no path Q -> P in the touch DAG of A.
Each candidate is individually realisable by a topological re-sort.  Reports convertible pivots (span test)."""
import sys
sys.argv=['multi4.py',sys.argv[1] if len(sys.argv)>1 else '/home/user/integer-mult-bounds/research/e8-bit-p111-e1/data/bitE8mut-p111-e1.json.gz','/dev/null','--max','0','--maxS','1000']
src=open('multi4.py').read(); src=src[:src.index('done = []; skipped')]
exec(src)
import collections, json
def rank(vs):
    b={}
    for x in vs:
        while x:
            p=x.bit_length()-1
            if p in b: x^=b[p]
            else: b[p]=x; break
    return len(b)
seq, touch, segs, alpha = analyse(w); T=len(seq); NA=len(w['A'])
succ=[set() for _ in range(NA)]
for r,tl in touch.items():
    ta=[t for t,_ in tl if t<NA]
    for a_,b_ in zip(ta,ta[1:]): succ[a_].add(b_)
desc=[0]*NA
for t in range(NA-1,-1,-1):
    d=1<<t
    for s_ in succ[t]: d|=desc[s_]
    desc[t]=d
def reach(a,b):   # path a -> b (a,b times in A or None)
    return a is not None and b is not None and a<NA and b<NA and (desc[a]>>b)&1
# chain positions per register: list of (prev_touch_time or None, next_touch_time or None, cur, nxt)
def positions(r):
    tl=touch[r]; out=[]; prev=None; cur=w['start'][r]
    for t,f in tl+[(None,FULL)]:
        out.append((prev,t,cur,f))
        if t is None: break
        prev=t; cur=f
    return out
POS={r:positions(r) for r in range(n) if not is_y(r)}
gsegs=[]
for g in range(n):
    if is_y(g): continue
    for (pv,nx,gc,gn) in POS[g]:
        if pv is not None and pv>=NA: continue
        tq = pv+1 if pv is not None else 0
        a=None
        for tt,aa in hist_[g] if False else []: pass
        gsegs.append((g,pv,nx,gc,gn))
# alpha after a time: recompute from segs
def alpha_seg(g,pv):
    p0=pv+1 if pv is not None else 0
    for (a0,a1,gc,gn,a) in segs[g]:
        if a0<=p0<=a1: return a
    return None
gsegs=[(g,pv,nx,gc,gn,alpha_seg(g,pv)) for (g,pv,nx,gc,gn) in gsegs]
gsegs=[x for x in gsegs if x[5]]
res=collections.Counter(); report={}
for p in range(2*v,n):
    if w['start'][p]!=ZERO: continue
    th=touch[p]; E=th[0][1]; k=alpha[p]
    vecs={}; Src=set()
    for j in range(-1,len(th)):
        if j>=0:
            t,f=th[j]
            if t>=NA: break
            g_=seq[t]
            if g_[1]==p:
                if any(s>=v for s in g_[2]): break
                for s in g_[2]: Src^={s}
            pc=f; pj=t
        else: pc=E; pj=None
        if j+1>=len(th) or th[j+1][0]>=NA: break
        pn=th[j+1][1]; pq=th[j+1][0]
        S={p}|Src
        Fs=[F for F in range(len(FR)) if FR[pc]<=FR[F]<=FR[pn]]
        for F in Fs:
            # source positions fitting F, and not ordered against p's segment wrongly
            spos={}
            okF=True
            for x in Src:
                ps=[(a,b) for (a,b,c,d) in POS[x] if (a is None or a<NA) and FR[c]<=FR[F]<=FR[d] and not reach(pq,a) and not reach(b,pj)]
                if not ps: okF=False; break
                spos[x]=ps
            if not okF: continue
            for (g,gk,gn_t,gc,gn,a) in gsegs:
                if g in S or a in vecs: continue
                if not (FR[gc]<=FR[F]<=FR[gn]): continue
                if reach(pq,gk) or reach(gn_t,pj): continue
                # choose source positions compatible with g as well
                good=True
                for x,ps in spos.items():
                    if not any(not reach(gn_t,a_) and not reach(b_,gk) for a_,b_ in ps): good=False; break
                if good: vecs[a]=(g,gk,j,F)
    vs=list(vecs); r=rank(vs); ok=rank(vs+[k])==r
    res['in span' if ok else 'no']+=1; report[p]=(len(vs),r,ok)
    if ok: print('pivot',p,'E dim',fd[E],'vecs',len(vs),'rank',r,flush=True)
print(dict(res)); print('rank distribution', collections.Counter(min(x[1]//10*10,110) for x in report.values()))
json.dump({str(k_):v_ for k_,v_ in report.items()},open('relax3.json','w'))
