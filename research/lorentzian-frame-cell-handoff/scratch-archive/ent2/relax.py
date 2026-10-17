import sys
sys.argv=['multi4.py','/home/user/integer-mult-bounds/research/e8-bit-p111-e1/data/bitE8mut-p111-e1.json.gz','/dev/null','--max','0','--maxS','1000']
src=open('multi4.py').read(); src=src[:src.index('done = []; skipped')]
exec(src)
def rank(vs):
    b={}
    for x in vs:
        while x:
            p=x.bit_length()-1
            if p in b: x^=b[p]
            else: b[p]=x; break
    return len(b)
import collections
res=collections.Counter(); out=[]
seq0=seq_of(w)
for h in range(2*v,n):
    if w['start'][h]!=ZERO: continue
    th=[(t,g[0]) for t,g in enumerate(seq0) if g is not None and (g[1]==h or h in g[2])]
    t1,F1=th[0]; E=F1
    old=w['start'][h]; w['start'][h]=E
    seq, touch, segs, alpha = analyse(w); T=len(seq); k=alpha[h]
    # S epochs (fixed schedule) with bounds
    S={h}; curf=list(w['start']); ptr=collections.defaultdict(int); nextf={}
    for r in range(n):
        tl=touch[r]; nextf[r]=tl[0][1] if tl else FULL
    epochs=set()
    for p in range(T+1):
        if p>0 and seq[p-1] is not None:
            f,d,srcs=seq[p-1]
            for r in (d,)+srcs:
                curf[r]=f; ptr[r]+=1; tl=touch[r]; nextf[r]=tl[ptr[r]][1] if ptr[r]<len(tl) else FULL
        lb=0; ub=(1<<128)-1
        for r in S: lb|=fm[curf[r]]; ub&=fm[nextf[r]]
        if not lb&~ub: epochs.add((frozenset(S),lb,ub))
        if p<T and seq[p] is not None:
            f,d,srcs=seq[p]
            if d in S:
                for s_ in srcs: S^={s_}
    vecs=set()
    allfm=list(enumerate(fm))
    for g in range(n):
        if is_y(g): continue
        for (p0,p1,gc,gn,a) in segs[g]:
            if not a or a in vecs: continue
            for (Se,lb,ub) in epochs:
                if g in Se: continue
                lo=lb|fm[gc]; hi=ub&fm[gn]
                if lo&~hi: continue
                if any((m&~hi)==0 and (lo&~m)==0 for _,m in allfm):
                    vecs.add(a); break
    vs=list(vecs); r=rank(vs); ok=rank(vs+[k])==r
    res['in span' if ok else 'no']+=1
    out.append((h,len(vs),r,ok)); print(h,len(vs),r,ok,bin(k).count("1"),flush=True) if len(out)<4 else None
    w['start'][h]=old
    if len(out)%50==0: print(len(out),dict(res),flush=True)
print(dict(res)); print('rank distribution',collections.Counter(min(x[2]//10*10,110) for x in out))
