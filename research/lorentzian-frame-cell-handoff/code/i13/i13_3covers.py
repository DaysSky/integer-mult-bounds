"""EXHAUSTIVE 3-section covers of R(t) in I_{13,1} (nondegenerate rank-3 frames through t, from i13_frames_<kind>.pkl),
first frame up to Stab(t) (orbit reps via lgeo13.canon), F2/F3 all frames.  For every cover: rank of each section's
exclusive part (lines of R(t) in exactly that section) and of the whole section.  An exclusive part of full section
rank forces >= 2 node arrivals for that delivery (I11's lexcl lemma); a proper one does not.
usage: python3 i13_3covers.py KIND   (T or P)"""
import sys, pickle, collections, time
from lgeo13 import *
kind = sys.argv[1]
t, FL, PL = pickle.load(open('i13_frames_%s.pkl' % kind, 'rb'))
R = HYP[t]; NF = len(FL); t0 = time.time()
linefr = {s: 0 for s in bits(R)}
for i, P in enumerate(PL):
    for s in bits(P): linefr[s] |= 1 << i
reps = {}
for i, F in enumerate(FL):
    key = canon((1 << t, F))[0]
    if key not in reps: reps[key] = i
order = sorted(range(NF), key=lambda i: -pc(PL[i]))
covers = set(); RK = {}
def rk(m):
    if m not in RK: RK[m] = rank(m)
    return RK[m]
for key, i1 in reps.items():
    s1 = pc(PL[i1])
    if 3 * s1 < pc(R): continue
    for i2 in order:
        s2 = pc(PL[i2])
        if s2 > s1 or s1 + 2 * s2 < pc(R): continue
        U = R & ~(PL[i1] | PL[i2])
        cand = (1 << NF) - 1
        for s in bits(U):
            cand &= linefr[s]
            if not cand: break
        if not cand: continue
        for i3 in bits(cand):
            if pc(PL[i3]) > s2: continue
            covers.add(tuple(sorted((i1, i2, i3))))
print(kind, '| 3-covers found (first frame up to Stab(t)):', len(covers), '| %.0fs' % (time.time() - t0), flush=True)
hist = collections.Counter()
for c in covers:
    row = []
    for a in c:
        others = 0
        for b in c:
            if b != a: others |= PL[b]
        ex = PL[a] & ~others
        row.append((pc(PL[a]), rk(PL[a]), pc(ex), rk(ex) if ex else 0))
    hist[tuple(sorted(row, reverse=True))] += 1
for k, v in sorted(hist.items(), key=lambda kv: -kv[1]):
    print('  %4d covers | per section (|perp|, rank perp, |excl|, rank excl):' % v, k, flush=True)
