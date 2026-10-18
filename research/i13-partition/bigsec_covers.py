"""Exact-cover search: I12 and I13 rank-9 3-sections (the big-section favorable regime).
Pair-hash weight-2/3 + 1-line corrections, reuse coordination.  These are the two highest-
ceiling systems (I13: v/(h+4)^2 = 1.26, I12: 1.12 vs E8 0.83) and the census gaps closed
today show span-miss ~1 with pair-XOR max (148-200) at or above demand (147-183)."""
import sys, time, collections, pickle
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom

def run(n, tag, tmax=None):
    g = Geom(n); V = g.V; HYP = g.HYP; G = g.G
    t0 = time.time()
    def log(*a): print('[%s %5.0fs]' % (tag, time.time() - t0), *a, flush=True)
    def sections_of(t):
        mates = [e for e in range(V) if e != t and G[t, e] == 0]
        secs = []
        for i in range(len(mates)):
            for j in range(i + 1, len(mates)):
                if G[mates[i], mates[j]] == 0:
                    secs.append(HYP[mates[i]] & HYP[mates[j]])
        return secs
    targets = range(V) if tmax is None else range(tmax)
    solutions = {}
    sec_use = collections.Counter()
    c_hist = collections.Counter()
    corrections = {}
    for t in targets:
        R_t = HYP[t] & ~(1 << t)
        secs = sections_of(t)
        n_ = len(secs)
        pd = {}
        for i in range(n_):
            si = secs[i]
            for j in range(i + 1, n_):
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
        if len(solutions) % 40 == 0:
            log('solved %d/%d targets, distinct sections %d' % (len(solutions), len(list(targets)), len(sec_use)))
    log('DONE %s: %d solved, weights %s' % (tag, len(solutions), dict(c_hist)))
    if solutions:
        content = sum(bin(s).count('1') for s in sec_use)
        ct = sum(len(v) for v in solutions.values()) + sum(1 for c in corrections.values() if c != -1)
        log('   distinct sections %d content %d use-hist %s' % (len(sec_use), content, dict(sorted(collections.Counter(sec_use.values()).items()))))
        log('   sum c_t = %d -> R_identity = %d + dead' % (ct, ct - V))
    pickle.dump({'sec_use': dict(sec_use), 'solutions': {t: list(v) for t, v in solutions.items()},
                 'corrections': corrections, 'c_hist': dict(c_hist)},
                open('%s_3sec_design.pkl' % tag, 'wb'))
    log('   saved')

run(12, 'i12', tmax=40)      # probe first 40 targets
run(13, 'i13r9', tmax=40)    # probe first 40 targets (rank-9 family)