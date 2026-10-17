"""Sound-ish relaxation for rescheduled injections, regime S = {p} + sources (A section only).
For pivot p (start E = first-touch frame), for each segment j of p (between its touches j, j+1, both in A) in which
p has read only sources so far (and no register written into... p's value = d + sum of sources Src_j), S = {p} u Src_j.
Each source x in Src_j may sit at any position of its own frame chain (rescheduling): it needs a chain interval
[cur, next] with cur <= F <= next.  g: any z register segment (gc, gn, alpha) with gc <= F <= gn, g not in S.
F listed, F >= frame(p after touch j), F <= frame(p at touch j+1).  Ignores DAG acyclicity -> upper bound for this regime.
Reports per pivot whether k_p is in the span."""
import sys
sys.argv=['multi4.py','/home/user/integer-mult-bounds/research/e8-bit-p111-e1/data/bitE8mut-p111-e1.json.gz','/dev/null','--max','0','--maxS','1000']
src=open('multi4.py').read(); src=src[:src.index('done = []; skipped')]
exec(src)
import collections
def rank(vs):
    b={}
    for x in vs:
        while x:
            p=x.bit_length()-1
            if p in b: x^=b[p]
            else: b[p]=x; break
    return len(b)
seq, touch, segs, alpha = analyse(w); T=len(seq); NA=len(w['A'])
# per register frame chain intervals (cur,next) in A (and beyond)
chain={}
for r in range(n):
    if is_y(r): continue
    ch=[w['start'][r]]+[f for t,f in touch[r]]+[FULL]
    chain[r]=list(zip(ch,ch[1:]))
def src_ok(x,F):
    return any(FR[a]<=FR[F]<=FR[b] for a,b in chain[x])
# g segments list
gsegs=[(g,gc,gn,a) for g in range(n) if not is_y(g) for (p0,p1,gc,gn,a) in segs[g] if a]
res=collections.Counter(); ranks=[]
for p in range(2*v,n):
    if w['start'][p]!=ZERO: continue
    th=touch[p]; E=th[0][1]; k=alpha[p]
    vecs=set(); Src=set(); 
    for j in range(len(th)):
        t,f=th[j]
        if t>=NA: break
        g_=seq[t]
        if g_[1]==p:
            if any(s>=v for s in g_[2]): break     # p reads a non-source: leave regime
            for s in g_[2]: Src^={s}
        # segment after touch j: p at f, next touch frame
        pn=th[j+1][1] if j+1<len(th) else FULL
        S={p}|Src
        Fs=[F for F in range(len(FR)) if FR[f]<=FR[F]<=FR[pn] and all(src_ok(x,F) for x in Src)]
        if not Fs: continue
        for (g,gc,gn,a) in gsegs:
            if g in S or a in vecs: continue
            if any(FR[gc]<=FR[F]<=FR[gn] for F in Fs): vecs.add(a)
    # plus the pure window before first touch: S={p}, F=E
    for (g,gc,gn,a) in gsegs:
        if g!=p and a not in vecs and FR[gc]<=FR[E]<=FR[gn]: vecs.add(a)
    vs=list(vecs); r=rank(vs); ok=rank(vs+[k])==r
    res['in span' if ok else 'no']+=1; ranks.append(r)
print(dict(res)); print('rank distribution', collections.Counter(min(r//10*10,110) for r in ranks))
