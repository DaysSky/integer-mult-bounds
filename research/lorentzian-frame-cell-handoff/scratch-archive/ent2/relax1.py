import sys
H=int(sys.argv[1])
sys.argv=['multi4.py','/home/user/integer-mult-bounds/research/e8-bit-p111-e1/data/bitE8mut-p111-e1.json.gz','/dev/null','--max','0','--maxS','1000']
src=open('multi4.py').read(); src=src[:src.index('done = []; skipped')]
exec(src)
import collections
h=H
seq0=seq_of(w)
th=[(t,g[0]) for t,g in enumerate(seq0) if g is not None and (g[1]==h or h in g[2])]
t1,F1=th[0]; E=F1; w['start'][h]=E
seq, touch, segs, alpha = analyse(w); T=len(seq); k=alpha[h]
print('h',h,'E',E,'touches',[(t,f,fd[f],seq[t]) for t,f in th][:8])
S={h}; curf=list(w['start']); ptr=collections.defaultdict(int); nextf={}
for r in range(n):
    tl=touch[r]; nextf[r]=tl[0][1] if tl else FULL
epochs={}
for p in range(T+1):
    if p>0 and seq[p-1] is not None:
        f,d,srcs=seq[p-1]
        for r in (d,)+srcs:
            curf[r]=f; ptr[r]+=1; tl=touch[r]; nextf[r]=tl[ptr[r]][1] if ptr[r]<len(tl) else FULL
    lb=0; ub=(1<<128)-1
    for r in S: lb|=fm[curf[r]]; ub&=fm[nextf[r]]
    key=(frozenset(S),lb,ub)
    if not lb&~ub and key not in epochs: epochs[key]=(p,{r:(curf[r],nextf[r]) for r in S})
    if p<T and seq[p] is not None:
        f,d,srcs=seq[p]
        if d in S:
            for s_ in srcs: S^={s_}
cands=[]
for g in range(n):
    if is_y(g): continue
    for (p0,p1,gc,gn,a) in segs[g]:
        if not a: continue
        for (Se,lb,ub),(pe,fr) in epochs.items():
            if g in Se: continue
            lo=lb|fm[gc]; hi=ub&fm[gn]
            if lo&~hi: continue
            Fs=[j for j,m in enumerate(fm) if (m&~hi)==0 and (lo&~m)==0]
            if Fs: cands.append((a,g,p0,p1,gc,gn,pe,sorted(Se),min(Fs,key=lambda j:fd[j]))); break
seen=set(); cu=[]
for c in cands:
    if c[0] in seen: continue
    seen.add(c[0]); cu.append(c)
sol=solve(k,[c[0] for c in cu])
print('cands',len(cu),'solution',sol)
for i in sol or []:
    a,g,p0,p1,gc,gn,pe,Se,F=cu[i]
    print('  g',g,'seg',(p0,p1),'frames',(gc,fd[gc]),(gn,fd[gn]),'epoch at p',pe,'S',Se,'F',F,fd[F],' overlap', not (p1<pe))
