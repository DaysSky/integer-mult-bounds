"""THE R420 WORD ANATOMY v3 — THE CONTENTS + THE SEMANTICS (the correction design's ground truth!!).

THE SS1450 DISCOVERIES: the R420's helpers = THE RUNNING SUMS climbing the D4 flag
(the singleton -> the cell -> the 12-frame -> the 30-frame -> FULL, 1 src per A-gate!!);
THE TARGETS read ~4 helpers (1 at a cell + 3 at the perp!!); THE 9 BIG GATES AT FULL
(23-46 srcs!!) = the gathers (built hierarchically!!); the KeyError: 'ret_frames' does
not exist in the R420's format (the key differs from the identity template!!).

THIS v3 measures THE DECISIVE REMAINING DATA:
1. THE WORD'S KEYS (the format!!) + the retained's structure;
2. THE FULL REPLAY WITH THE CONTENT-TRACKING (the val-mask per register!!): the helpers'
   FINAL CONTENTS (the sizes + the line-sets!!) + the A-gate anatomy per helper (the src
   counts at each frame!!);
3. THE TARGETS' SEMANTICS VERIFICATION: the scatter's XOR + the 4 B-reads' contents:
   THE XOR == perp(t)?? THE CORRECTION DESIGN'S GROUND TRUTH!!!;
4. THE HELPER-SHARING: the read-sets per target (the reuse!!!).
"""
import gzip, json
from collections import Counter, defaultdict
import numpy as np

path = '/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz'
w = json.loads(gzip.open(path, 'rt').read())
h, v, R = w['h'], w['v'], w['R']
print('THE R420 WORD: h=%d v=%d R=%d (rho %.2f)' % (h, v, R, R / v))
print('\n(0) THE WORD KEYS: %s' % sorted(w.keys()))
L = np.array(w['lines'], dtype=float)
fr = w['frames']
def span_rank(idxs):
    if not idxs:
        return 0
    return int(np.linalg.matrix_rank(L[list(idxs)]))
dims = [span_rank(F) for F in fr]
nreg = 2 * v + R
print('    the scatter: %s' % type(w['scatter']).__name__)
# the retained: the word's structure!!
if 'ret' in w:
    ret = w['ret']
    print('    the ret: %d entries; the sample: %s' % (len(ret), ret[:12]))
    rf = w.get('retf') or w.get('ret_frames') or w.get('retframe')
    for key in ('retf', 'ret_frames', 'retframe', 'ret_fr'):
        if key in w:
            print('    the retained-frames key: %r: %d entries; the dims: %s' % (key, len(w[key]), [dims[f] for f in w[key]]))
            rf = w[key]
            break
    print('    the scatter sample: %s' % (w['scatter'][:3] if isinstance(w['scatter'], list) else list(w['scatter'].items())[:3]))

# ============ (2) THE FULL REPLAY WITH THE CONTENT-TRACKING ============
print('\n(2) THE REPLAY (the contents!!)')
start = w['start']
cur = list(start)
val = [1 << i for i in range(nreg)]   # the initial: the dirt!!
def replay(gates, phase):
    for F, d, srcs in gates:
        for r in [d] + list(srcs):
            cur[r] = F
        for s in srcs:
            val[d] ^= val[s]
replay(w['D'], 'D')
replay(w['A'], 'A')
# the scatter!!
if isinstance(w['scatter'], list) and ret:
    for t in range(v):
        for k in w['scatter'][t]:
            val[v + t] ^= val[ret[k]]
replay(w['B'], 'B')
replay(w['C'], 'C')

def bits(x):
    out = []
    while x:
        b = x & -x
        out.append(b.bit_length() - 1)
        x ^= b
    return out

# the helpers' final contents!!
hsizes = Counter()
hlines = {}
for q in range(2 * v, nreg):
    c = val[q] & ((1 << v) - 1)
    hsizes[len(bits(c))] += 1
    hlines[q] = set(bits(c))
print('    the helpers\' final content sizes: %s (the mean %.1f)' %
      (dict(sorted(hsizes.items())), sum(k * n for k, n in hsizes.items()) / R))
# the A-gate anatomy per helper: the src counts!!
agates = defaultdict(list)
for F, d, srcs in w['A']:
    if d >= 2 * v:
        agates[d].append((F, len(srcs)))
gs = Counter()
for q, lst in agates.items():
    gs[tuple(n for _, n in lst)] += 1
print('    the helpers\' A-gate src-count patterns: %s' % dict(sorted(gs.items())[:14]))
print('    the distinct patterns: %d; the A-gated helpers: %d' % (len(gs), len(agates)))
# the big gates' dests (the gathers!!)
big = [(d, len(srcs)) for F, d, srcs in w['A'] if len(srcs) > 2]
print('    the big A-gates (the dests, srcs): %s' % big[:12])
if ret:
    print('    the ret indices: %s' % ret)
    rq = [d for d, _ in big]
    print('    the big-gate dests == the ret?? %s' % set(rq) == set(ret))
    for q in ret:
        print('      the gather %d: the content %d lines; the gates %s' % (q, len(hlines[q]), agates.get(q)))

# ============ (3) THE TARGETS' SEMANTICS ============
print('\n(3) THE TARGETS\' SEMANTICS VERIFICATION')
# the perp(t)!!
G = L @ L.T
ok_cnt, bad_cnt = 0, 0
tread = defaultdict(list)
for F, d, srcs in w['B']:
    if v <= d < 2 * v:
        tread[d - v].extend(srcs)
for t in range(v):
    perp = set(s for s in range(v) if s != t and abs(G[s][t]) < 1e-9)
    # the B-reads' contents XOR!!
    acc = set()
    for q in tread[t]:
        acc ^= hlines[q]
    # the scatter's contribution: the gathers' contents XOR!!
    if isinstance(w['scatter'], list) and ret:
        sc = set()
        for k in w['scatter'][t]:
            sc ^= hlines[ret[k]]
    else:
        sc = set()
    # the semantics: scatter ⊕ B-reads ⊕ {t} == perp?!? the delivered x: the bit t!!
    tot = sc ^ acc
    if tot == ({t} | perp):
        ok_cnt += 1
    else:
        bad_cnt += 1
        if bad_cnt <= 3:
            print('      the target %d: scatter^reads (%d lines) vs B[t] (%d): the diff %s' %
                  (t, len(tot), len(perp) + 1, len(tot ^ ({t} | perp))))
print('    the targets where scatter^reads == B[t]: %d ok, %d bad' % (ok_cnt, bad_cnt))
# the read-set sizes!!
rs = Counter(len(qs) for qs in tread.values())
print('    the targets\' B-read counts: %s' % dict(sorted(rs.items())))
# the helpers read by the targets: the reuse!!
huse = Counter()
for t, qs in tread.items():
    for q in qs:
        huse[q] += 1
print('    the helpers\' user counts: %s' % dict(sorted(Counter(huse.values()).items())))
print('DONE')
