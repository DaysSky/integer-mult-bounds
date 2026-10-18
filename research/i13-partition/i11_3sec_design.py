"""I11 3-section design: per-target min-weight representations with 1-line corrections.
R(t) = XOR of <= 3 sections + one line (free in-chain read).  Method: pair-XOR hash:
store XORs of all section pairs; for each correction line l in R(t) and each section s,
check if R(t) ^ l ^ s is in the pair-dict -> weight-3 solution (pair + s).  Also weight-2
directly (R(t) ^ l in pair-dict).  Coordinate: prefer sections reused by other targets.
Output: c_t histogram, distinct sections used, total content, corrections."""
import sys, time, collections
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; HYP = g.HYP; G = g.G
full = (1 << V) - 1
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# sections per target, precomputed lazily
def sections_of(t):
    mates = [e for e in range(V) if e != t and G[t, e] == 0]
    secs = []
    for i in range(len(mates)):
        for j in range(i + 1, len(mates)):
            if G[mates[i], mates[j]] == 0:
                secs.append(HYP[mates[i]] & HYP[mates[j]])
    return secs

targets = list(range(V))
log('targets', len(targets))
solutions = {}
sec_use = collections.Counter()
c_hist = collections.Counter()
corrections = {}
for t in targets:
    R_t = HYP[t] & ~(1 << t)
    secs = sections_of(t)
    # pair-XOR dict (only pairs, not doubles)
    n = len(secs)
    pd = {}
    for i in range(n):
        si = secs[i]
        for j in range(i + 1, n):
            x = si ^ secs[j]
            if x not in pd: pd[x] = (i, j)
    log('%s secs %d pairs %d' % (g.kind[t] + str(g.supp[t]), n, len(pd))) if t % 55 == 0 else None
    best = None  # (weight, reuse_score, used_sections, corr_line)
    R_lines = [x for x in range(V) if R_t >> x & 1]
    # weight-2: R_t ^ l in pd
    for l in R_lines:
        key = R_t ^ (1 << l)
        if key in pd:
            i, j = pd[key]
            sc = sec_use[secs[i]] + sec_use[secs[j]]
            if best is None or (2, -sc) < (best[0], -best[1]):
                best = (2, sc, (secs[i], secs[j]), l)
    # weight-3: R_t ^ l ^ s in pd for some section s
    if best is None or best[0] > 2:
        for l in R_lines:
            base = R_t ^ (1 << l)
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
        log('  solved %d targets, distinct sections so far %d' % (len(solutions), len(sec_use)))
log('DONE: solutions %d / %d' % (len(solutions), len(targets)))
log('weight histogram:', dict(c_hist))
log('distinct sections used:', len(sec_use))
log('use histogram:', dict(sorted(collections.Counter(sec_use.values()).items())))
content = sum(bin(s).count('1') for s in sec_use)
log('TOTAL DISTINCT SECTION CONTENT: %d (E8 R420 reference: 3,000)' % content)
ct = sum(len(v) for v in solutions.values()) + len(solutions)  # sections + 1 corr line each
log('sum c_t = %d -> R_identity = %d + dead' % (ct, ct - V))
pickle_targets = {t: ([bin(s).count('1') for s in v], corrections[t]) for t, v in solutions.items()}
import pickle
pickle.dump({'sec_use': dict(sec_use), 'solutions': {t: list(v) for t, v in solutions.items()},
             'corrections': corrections}, open('i11_3sec_design.pkl', 'wb'))
log('saved i11_3sec_design.pkl')