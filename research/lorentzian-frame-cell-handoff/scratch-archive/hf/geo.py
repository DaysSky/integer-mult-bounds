import gzip, json, itertools
from collections import Counter
REPO='/home/user/integer-mult-bounds'
CW=REPO+'/research/gauge44-frames-x/evidence/local/CANONICAL-WORD.json.gz'
def load(path=CW):
    return json.load(gzip.open(path))
def dot(a,b): return bin(a&b).count('1')&1
def basis(vs):
    piv={}
    for a in vs:
        while a:
            bit=a.bit_length()-1
            if bit in piv: a^=piv[bit]
            else: piv[bit]=a; break
    for k in sorted(piv):
        for j in piv:
            if j>k and piv[j]>>k&1: piv[j]^=piv[k]
    return tuple(piv[k] for k in sorted(piv,reverse=True))
def span(vs):
    b=basis(vs); S={0}
    for x in b: S|={s^x for s in S}
    return S
def contained(a,b): return basis(list(a)+list(b))==basis(b)
def perp(vs,h=9): return basis([x for x in range(1,1<<h) if all(dot(x,v)==0 for v in vs)])

# ---- E8 / port geometry -------------------------------------------------
import numpy as np
def ports(c=None):
    c=c or load(); return c['ports']
def readers(P):
    v=len(P); return [[t for t in range(v) if dot(P[s],P[t])==0] for s in range(v)]
def rank2(vs): return len(basis(vs))
def S_of(F,P):
    Fs=span(F); return [i for i,p in enumerate(P) if p in Fs]
def all_subspaces(h=9, dim=None):
    """enumerate subspaces of F2^h of given dim as reduced bases (via RREF enumeration)"""
    import itertools
    out=set()
    # brute force via random? use recursive: subspaces of dim k from adding vectors to dim k-1
    cur={()}
    for k in range(dim):
        nxt=set()
        for B in cur:
            Sp=span(B)
            for x in range(1,1<<h):
                if x not in Sp: nxt.add(basis(list(B)+[x]))
        cur=nxt
    return cur
