import gzip, json, numpy as np
from geo import *
REPO='/home/user/integer-mult-bounds'
_fw=json.load(gzip.open(REPO+'/research/gauge44-frames-x/evidence/local/FULL-WORD.json.gz'))
P=_fw['ports']; Rr=np.array(_fw['root_lines']); V=len(P)
G=(Rr@Rr.T)//2                      # integer Gram, diag 2
N=np.eye(V)-G/2.0                    # drop-free demand (zero diag, +-1/2 on legal pairs)
LEG=np.array([[dot(P[s],P[t])==0 for s in range(V)] for t in range(V)])  # [t,s] legal
TET=[tuple(np.nonzero(Rr[t])[0]) for t in range(V)]

# ---- pencils / halves / classes -----------------------------------------
def pencils():
    """56 pencils: key (i,j,sigma) -> list of 12 lines; with orientation sign eps[line] s.t. eps*r restricted to (i,j) = (1,sigma)"""
    pen={}
    for t in range(V):
        T=TET[t]
        for i,j in itertools.combinations(T,2):
            sig=int(Rr[t,i]*Rr[t,j])
            pen.setdefault((int(i),int(j),sig),[]).append(t)
    return pen
import itertools
PEN=pencils()
def halves_of(key):
    i,j,sig=key; L=PEN[key]; hs=[]
    used=set()
    for t in L:
        if t in used: continue
        # partner: same tetrad, r differs by flipping the two coords outside {i,j}
        for s in L:
            if s!=t and TET[s]==TET[t] and int(Rr[t]@Rr[s])==0:
                hs.append((t,s)); used|={t,s}; break
    return hs
