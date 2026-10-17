"""Pure-window donor test with the pivot's first gate raised: E = F' any listed frame with
  join(current frames of the first gate's operands) <= F' <= meet(next frames of those operands),
F' with a live-root isometry (rank 1, or rank-2 A1xA1).  Donors: z registers g != p with a segment (gc, gn) overlapping
[0, t1] (fixed schedule) and gc <= F' <= gn; alpha_g on that segment.  k_p in span?  (any F', any donor set)"""
import sys
sys.argv=['multi5.py',sys.argv[1] if len(sys.argv)>1 else '/home/user/integer-mult-bounds/research/e8-bit-p111-e1/data/bitE8mut-p111-e1.json.gz','/dev/null','--pivots','0']
src=open('multi5.py').read(); src=src[:src.index('pivots = None')]
exec(src)
import collections
seq, touch, alpha, alpha_at, succ, desc, NA = analyse(w)
POS={r: positions(w, touch, r) for r in range(n) if not is_y(r)}
def rank(vs):
    b={}
    for x in vs:
        while x:
            p=x.bit_length()-1
            if p in b: x^=b[p]
            else: b[p]=x; break
    return len(b)
iso_cache={}
def iso(F):
    if F not in iso_cache:
        lines=sorted(FR[F]); e=fd[F]; ok=False
        def rec(cur,cands):
            if len(cur)==e:
                return ortho_frame(cur) is not None
            for k,c in enumerate(cands):
                if rec(cur+[c],[d_ for d_ in cands[k+1:] if dot(L[c],L[d_])==0]): return True
            return False
        ok = rec([],lines) if e<=6 else False
        iso_cache[F]=ok
    return iso_cache[F]
res=collections.Counter(); hits=[]
for p in range(2*v,n):
    if w['start'][p]!=ZERO or alpha[p]==0: continue
    t1,F1=touch[p][0]
    if t1>=NA: continue
    f,d,srcs=seq[t1]
    ops=(d,)+srcs
    lo=set(); hi=None
    for r in ops:
        cur,nxt=None,None
        for (a,b,c,dd) in POS[r]:
            if b==t1: cur=c   # position ending at t1: cur = frame before t1
            if a==t1: nxt=dd   # position starting after t1: next frame
        if r==p: cur=0 if cur is None else cur
        lo|=FR[cur] if cur is not None else set()
        hi=FR[nxt] if hi is None else hi&FR[nxt]
    Fs=[F for F in range(len(FR)) if lo<=FR[F]<=hi and FR[F1]<=FR[F] and fd[F]>=1 and iso(F)]
    best=None
    for F in Fs:
        vecs=set()
        for g in range(n):
            if is_y(g) or g==p: continue
            for (a,b,gc,gn) in POS[g]:
                if a is not None and a>=t1: break
                if FR[gc]<=FR[F]<=FR[gn]:
                    al=alpha_at(g,(a+1) if a is not None else 0)
                    if al: vecs.add(al)
        vs=list(vecs); ok=rank(vs+[alpha[p]])==rank(vs)
        if ok: best=(F,fd[F],len(vs)); break
    res['convertible' if best else 'no']+=1
    if best: hits.append((p,best))
print(dict(res)); print(hits[:20])
