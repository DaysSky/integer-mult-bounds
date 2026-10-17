"""EXACT existence/enumeration of 4-section PARITY covers of R(t) in I_{13,1}: F1 over Stab(t)-orbit reps (every
parity cover has a frame in some orbit; move it to the rep), F2 over all frames, then F3 xor F4 = Y := R ^ F1p ^ F2p
exactly: F3 over the frames whose perp contains the line of Y with fewest coverers (WLOG F3 holds it), F4 found by
hashed lookup of Y ^ F3p among all perps.  Reports the number of covers found (with repeats) and their type patterns.
usage: python3 i13_parity4.py KIND"""
import sys, pickle, collections, time
import numpy as np
from lgeo13 import *
kind = sys.argv[1]; t0 = time.time()
t, FL, PL = pickle.load(open('i13_frames_%s.pkl' % kind, 'rb'))
R = HYP[t]; NF = len(FL); NW = (V + 63) // 64
def words(m): return [(m >> (64 * w)) & ((1 << 64) - 1) for w in range(NW)]
PW = np.array([words(P) for P in PL], dtype=np.uint64)
perp_index = {P: i for i, P in enumerate(PL)}
cov = collections.defaultdict(list)
for i, P in enumerate(PL):
    for s in bits(P): cov[s].append(i)
covarr = {s: np.array(v, dtype=np.int64) for s, v in cov.items()}
reps = {}; typ = {}
for i, F in enumerate(FL):
    key = canon((1 << t, F))[0]; typ[i] = key
    if key not in reps: reps[key] = i
typename = {}
for key, i in reps.items(): typename[key] = '%d/%d' % (pc(PL[i]), pc(FL[i]))
print(kind, 'frames', NF, 'reps', len(reps), '%.0fs' % (time.time() - t0), flush=True)
# hash of perps: fold words
mult = np.array([0x9E3779B97F4A7C15 + 2 * w + 1 for w in range(NW)], dtype=np.uint64)
def fold(arr):
    with np.errstate(over='ignore'):
        return np.bitwise_xor.reduce(arr * mult, axis=-1)
H = fold(PW); order = np.argsort(H); Hs = H[order]
found = set(); pat = collections.Counter()
for key, i1 in reps.items():
    for i2 in range(NF):
        if i2 == i1: continue
        Y = R ^ PL[i1] ^ PL[i2]
        if not Y: continue
        u = min(bits(Y), key=lambda s: len(cov[s]))
        c3 = covarr[u]
        Z = PW[c3] ^ np.array(words(Y), dtype=np.uint64)
        hz = fold(Z)
        pos = np.searchsorted(Hs, hz)
        pos[pos >= NF] = NF - 1
        hit = np.nonzero(Hs[pos] == hz)[0]
        for h in hit:
            i3 = int(c3[h]); zint = 0
            zw = Z[h]
            for w in range(NW): zint |= int(zw[w]) << (64 * w)
            i4 = perp_index.get(zint)
            if i4 is None or len({i1, i2, i3, i4}) < 4: continue
            q = tuple(sorted((i1, i2, i3, i4)))
            if q in found: continue
            found.add(q)
            pat[tuple(sorted(typename[typ[j]] for j in q))] += 1
    print('  rep %s done, covers so far %d  %.0fs' % (typename[key], len(found), time.time() - t0), flush=True)
print(kind, 'TOTAL 4-section parity covers found:', len(found), flush=True)
for k, v in pat.most_common(20): print('   %5d x types (|perp|/lines): %s' % (v, k), flush=True)
pickle.dump(found, open('i13_parity4_%s.pkl' % kind, 'wb'))
