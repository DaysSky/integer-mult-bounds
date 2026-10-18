"""THE R420 WORD ANATOMY v2 — the frames are LINE-INDEX SETS (SS1446's discovery!!).

THE SS1446 DISCOVERY: the R420's frames = the line-index lists: {0: 1, 1: 120, 2: 180
(THE CELLS!!), 12: 70 (the D4 12-line frames!), 30: 180, 63: 120 (the perps!), 120: 1
(THE FULL!!)} — the spans of the line-sets (NO arbitrary fillers!!) — THE FLAG DESIGN.

THIS v2 measures:
1. THE SPAN DIMS (the ranks of the line-sets!!) — the true frame dims;
2. THE FLAGS: the nesting (the line-set inclusions per chain!!);
3. THE HELPERS' ANATOMY: the 420 = the build frames (the A-dests!!) + the reads:
   the cells (the 2-line builds!) vs the tops (the 12/30-line builds!!);
4. THE TARGETS' CHAINS: the read frames + the shared components (the users per frame!!);
5. THE PIECES' SHARING (the user counts!!) + THE D/SCATTER/RETAINED.
"""
import gzip, json
from collections import Counter, defaultdict
import numpy as np

path = '/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz'
w = json.loads(gzip.open(path, 'rt').read())
h, v, R = w['h'], w['v'], w['R']
print('THE R420 WORD: h=%d v=%d R=%d (rho %.2f)' % (h, v, R, R / v))
L = np.array(w['lines'], dtype=float)

# ============ (1) THE FRAMES: the line-index sets + the span dims ============
fr = w['frames']
def span_rank(idxs):
    if not idxs:
        return 0
    return int(np.linalg.matrix_rank(L[list(idxs)]))
sr = [span_rank(F) for F in fr]
print('\n(1) THE FRAMES: %d; the SPAN-DIMS histogram: %s' % (len(fr), dict(sorted(Counter(sr).items()))))
ncount = Counter(len(F) for F in fr)
print('    the line-count histogram: %s' % dict(sorted(ncount.items())))
# the (line-count, span-dim) classes!!
cls = Counter((len(F), span_rank(F)) for F in fr if F)
print('    the (lines, span-dim) classes: %s' % dict(sorted(cls.items())))

# ============ (2) THE GATES' REPLAY (the chains!!) ============
dims = sr
nreg = 2 * v + R
cur = list(w['start'])
chains = defaultdict(list)
def replay(gates, phase):
    for F, d, srcs in gates:
        for r in [d] + list(srcs):
            if cur[r] != F:
                chains[r].append((phase, F, dims[F] - dims[cur[r]]))
                cur[r] = F
replay(w['D'], 'D')
replay(w['A'], 'A')
replay(w['B'], 'B')
replay(w['C'], 'C')

print('\n(2) THE HELPERS\' CHAIN PATTERNS (the climb-delta sequences over the span-dims!!)')
hp = defaultdict(list)
for r in range(2 * v, nreg):
    seq = tuple(d for (_, _, d) in chains[r] if d > 0)
    hp[seq].append(r)
for pat, regs in sorted(hp.items(), key=lambda kv: -len(kv[1]))[:14]:
    print('    the deltas %s: %d helpers' % (list(pat), len(regs)))
print('    the distinct helper patterns: %d' % len(hp))
# the sample chains: one cell + one top!!
for pat, regs in list(hp.items())[:2]:
    r = regs[0]
    print('    the helper %d (R420 q-%d): %s' % (r, r - 2 * v, [(ph, 'fr%d' % f, 'lines%d' % len(fr[f]), 'dim%d' % dims[f]) for (ph, f, d) in chains[r]]))

print('\n(3) THE TARGETS\' CHAIN PATTERNS')
tp = defaultdict(list)
for t in range(v, 2 * v):
    seq = tuple(d for (_, _, d) in chains[t] if d > 0)
    tp[seq].append(t)
for pat, regs in sorted(tp.items(), key=lambda kv: -len(kv[1]))[:10]:
    print('    the deltas %s: %d targets' % (list(pat), len(regs)))
print('    the distinct target patterns: %d' % len(tp))
r0 = list(tp.values())[0][0]
print('    the target %d: %s' % (r0, [(ph, 'fr%d' % f, 'lines%d' % len(fr[f]), 'dim%d' % dims[f]) for (ph, f, d) in chains[r0]]))

# ============ (4) THE B-GATE COMPONENTS (the shared read-frames!!) ============
print('\n(4) THE B-TARGET-GATES: the shared frames')
bf = defaultdict(lambda: dict(targets=0, pieces=0, pl=set()))
for F, d, srcs in w['B']:
    if v <= d < 2 * v:
        bf[F]['targets'] += 1
        bf[F]['pieces'] += len(srcs)
        bf[F]['pl'].update(srcs)
print('    the B-target-gates: %d; the DISTINCT frames: %d' %
      (sum(1 for F, d, s in w['B'] if v <= d < 2 * v), len(bf)))
stat = Counter((len(fr[F]), dims[F], info['targets'], info['pieces']) for F, info in bf.items())
print('    the (frame-lines, dim, target-gates, piece-reads) histogram: %s' % dict(sorted(stat.items())))
preads = defaultdict(set)
pusers = Counter()
for F, d, srcs in w['B']:
    if v <= d < 2 * v:
        for q in srcs:
            preads[q].add(F)
            pusers[q] += 1
nfr = Counter(len(s) for s in preads.values())
print('    the pieces\' read-frame counts: %s (the pieces read: %d)' % (dict(sorted(nfr.items())), len(preads)))
print('    the pieces\' user counts: mean %.1f max %d' % (sum(pusers.values()) / max(1, len(pusers)), max(pusers.values()) if pusers else 0))
uc = Counter(pusers.values())
print('    the user-count histogram: %s' % dict(sorted(uc.items())))

# ============ (5) THE A-GATES (the builds!!) + THE D + THE SCATTER ============
print('\n(5) THE A-GATES (the builds): the helper classes')
ab = Counter()
asrc = Counter()
for F, d, srcs in w['A']:
    ab[(len(fr[F]), dims[F], len(srcs))] += 1
    asrc[len(srcs)] += 1
print('    the A-gates: %d; the (frame-lines, dim, srcs) classes: %s' % (len(w['A']), dict(sorted(ab.items()))))
print('    the A-srcs histogram: %s' % dict(sorted(asrc.items())))
# the helpers' build frames: the FIRST A-gate per helper!!
bfirst = {}
for F, d, srcs in w['A']:
    if d not in bfirst:
        bfirst[d] = F
bc = Counter((len(fr[F]), dims[F]) for F in bfirst.values())
print('    the helpers\' FIRST-build frames: %d; the (lines, dim) classes: %s' % (len(bfirst), dict(sorted(bc.items()))))
print('    the D-gates: %d (the srcs: %s)' % (len(w['D']), dict(sorted(Counter(len(s) for _, _, s in w['D']).items()))))
ret, rf = w['ret'], w['ret_frames']
print('    the retained: %d; the ret_frames: %s (cst = %d)' % (len(ret), [(len(fr[f]), dims[f]) for f in rf], sum(dims[f] for f in rf)))
print('    the scatter: the per-target counts: %s' % dict(sorted(Counter(len(s) for s in w['scatter']).items())))
print('DONE')
