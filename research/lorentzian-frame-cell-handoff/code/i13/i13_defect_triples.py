"""I_{13,1} parity-top landscape: all triples of sections of t with XOR = R(t) + (<= 1 line) ('defect <= 1').
Sections: perps of rank-2 frames {t,u} (closure of t and one line u; users = its lines) and of nondegenerate rank-3
frames through t (i13_frames_<kind>.pkl).  Search: S1, S2 over rank-2 sections, S3 by hashed lookup over all sections
(defect line e in {none} u R(t) u lines outside R(t)); then S1 rank-2 x S2,S3 rank-3 via pair-table MITM is too big, so
rank-3 x rank-3 x rank-3 triples are covered by the earlier exhaustive 3-cover enumeration (every parity triple with
defect 0 is a cover; defect-1 triples with all rank-3 sections are checked from the cover list + one line).
Reports counts by (section types, defect).  usage: python3 i13_defect_triples.py KIND"""
import sys, pickle, collections, itertools, time
import numpy as np
from lgeo13 import *
kind = sys.argv[1]; t0 = time.time()
t, FL, PL = pickle.load(open('i13_frames_%s.pkl' % kind, 'rb'))
R = HYP[t]
eta = np.diag([1.0] * n + [-1.0])
def nondeg(m):
    M = np.zeros((0, n + 1))
    for s in bits(m):
        M2 = np.vstack([M, g.LA[s]])
        if np.linalg.matrix_rank(M2) > M.shape[0]: M = M2
    return abs(np.linalg.det(M @ eta @ M.T)) > 1e-6
r2 = {}
for u in range(V):
    if u == t: continue
    F = pp((1 << t) | (1 << u))
    if F not in r2 and nondeg(F): r2[F] = pm(F)
R2F = list(r2); R2P = [r2[F] for F in R2F]
allsec = {}
for F, P in zip(R2F, R2P): allsec.setdefault(P, []).append(('r2', F))
for F, P in zip(FL, PL): allsec.setdefault(P, []).append(('r3', F))
def nm(s): return KIND[s] + ''.join('%x' % i for i in SUPP[s])
print(kind, '| rank-2 sections', len(R2F), '| rank-3 sections', len(FL), '%.0fs' % (time.time() - t0), flush=True)
defects = [0] + [1 << e for e in range(V) if e != t]
found = collections.Counter(); examples = {}
for a in range(len(R2F)):
    for b in range(a, len(R2F)):
        X = R ^ R2P[a] ^ R2P[b]
        for d in defects:
            hits = allsec.get(X ^ d)
            if not hits: continue
            for (tp, F) in hits:
                if tp == 'r2' and F in (R2F[a], R2F[b]): continue
                key = ('r2', 'r2', tp, 'defect' if d else 'exact', pc(R2F[a]), pc(R2F[b]), pc(F))
                found[key] += 1
                if key not in examples:
                    examples[key] = ([nm(s) for s in bits(R2F[a])], [nm(s) for s in bits(R2F[b])], [nm(s) for s in bits(F)], [nm(s) for s in bits(d)])
print('  done r2-r2-* in %.0fs' % (time.time() - t0), flush=True)
for k, c in found.most_common(30):
    print('  %6d  %s  e.g. %s' % (c, k, examples[k]), flush=True)
