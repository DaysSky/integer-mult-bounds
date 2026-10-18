"""I10 3-section design: per-target min-weight representations with 1-line corrections.
R(t) = XOR of <= 3 sections + one free in-chain line.  Pair-hash search; reuse-coordinated.
I10: v = 165, |R(t)| = 87-92, sections 42-47 -> c_t = 2-3, break-even ~600-660 = 3.6-4v."""
import sys, time, collections, pickle
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(10); V = g.V; HYP = g.HYP; G = g.G
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def sections_of(t):
    mates = [e for e in range(V) if e != t and G[t, e] == 0]
    secs = []
    for i in range(len(mates)):
        for j in range(i + 1, len(mates)):
            if G[mates[i], mates[j]] == 0:
                secs.append(HYP[mates[i]] & HYP[mates[j]])
    return secs
solutions = {}
sec_use = collections.Counter()
c_hist = collections.Counter()
corrections = {}
for t in range(V):
    R_t = HYP[t] & ~(1 << t)
    secs = sections_of(t)
    n = len(secs)
    pd = {}
    for i in range(n):
        si = secs[i]
        for j in range(i + 1, n):
            x = si ^ secs[j]
            if x not in pd: pd[x] = (i, j)
    best = None
    R_lines = [x for x in range(V) if R_t >> x & 1] + [-1]
    for l in R_lines:
        key = R_t if l == -1 else R_t ^ (1 << l)
        if key in pd:
            i, j = pd[key]
            sc = sec_use[secs[i]] + sec_use[secs[j]]
            if best is None or (2, -sc) < (best[0], -best[1]):
                best = (2, sc, (secs[i], secs[j]), l)
    if best is None:
        for l in R_lines:
            base = R_t if l == -1 else R_t ^ (1 << l)
            for k, s in enumerate(secs):
                key = base ^ s
                if key in pd:
                    i, j = pd[key]
                    if k in (i, j): continue
                    sc = sec_use[s] + sec_use[secs[i]] + sec_use[secs[j]]
                    if best is None or (3, -sc) < (best[0], -best[1]):
                        best = (3, sc, (s, secs[i], secs[j]), l)
    if best is None:
        c_hist['none'] += 1
        continue
    w, sc, used, corr = best
    c_hist[w] += 1
    for s in used: sec_use[s] += 1
    corrections[t] = corr
    solutions[t] = used
    if len(solutions) % 55 == 0:
        log('solved %d targets, distinct sections %d' % (len(solutions), len(sec_use)))
log('DONE: %d / %d solved' % (len(solutions), V))
log('weight histogram:', dict(c_hist))
log('distinct sections:', len(sec_use))
log('use histogram:', dict(sorted(collections.Counter(sec_use.values()).items())))
content = sum(bin(s).count('1') for s in sec_use)
log('TOTAL DISTINCT CONTENT: %d (E8 ref 3,000)' % content)
ct = sum(len(v) for v in solutions.values()) + sum(1 for c in corrections.values() if c != -1)
log('sum c_t = %d -> R_identity = %d + dead' % (ct, ct - V))
pickle.dump({'sec_use': dict(sec_use), 'solutions': {t: list(v) for t, v in solutions.items()},
             'corrections': corrections}, open('i10_3sec_design.pkl', 'wb'))
log('saved i10_3sec_design.pkl')