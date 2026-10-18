"""THE R420-EXTENSION BUILD — STAGE 2b-i: THE REPLAY + THE CONTROL + THE EXTRACTION (ii19_ext3.py).

THE STAGE 2a (SS1926/SS1932/SS1937!!): the format-dump + the W-machinery + the gcheck's full
spec COMPLETE (the commits e924c05a, b894e703!!).

THE STAGE 2b-i (this script!): THE INSTRUMENTED REPLAY of the R420's arithmetic:
  (1) THE FULL VAL-SIMULATION (the D/A/scatter/B/C phases — the gcheck's own semantics!)
  (2) THE CONTROL: the finals = the expected (the sources {s}, the targets y+x, the helpers
      the own dirt!) + the hist's control (the R420's own {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}!)
  (3) THE PER-TARGET EXTRACTION: the (D-dirt, scatter, B-reads) patterns per target -> the
      [dirt ^ scatter ^ reads] = the x_t verification + the rets' frames at the scatter!
  (4) THE DESIGN DATA: the extension's ground (the special's machinery's arithmetic!)
"""
import gzip, json, time
from collections import Counter
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

W = json.load(gzip.open('research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
v, h, R = W['v'], W['h'], W['R']
nreg = 2 * v + R
frames = W['frames']
start, final = W['start'], W['final']

# ============ (0) THE DIMS' MAP (the R420's spans!!) ============
# the line-count -> the dim (the SS1736: {0:1, 1:120, 2:180, 4:70, 6:180, 7:120, 8:1}!!)
LCDIM = {0: 0, 1: 1, 2: 2, 12: 4, 30: 6, 63: 7, 120: 8}
dims = [LCDIM[len(f)] for f in frames]
log('(0) the frames: %d | the dims histogram %s' % (
    len(frames), dict(sorted(Counter(dims).items()))))

# ============ (1) THE INSTRUMENTED REPLAY ============
val = [1 << i for i in range(nreg)]
cur = list(start)
hist = Counter()
moves = [0]

def climb(r, F):
    if cur[r] == F:
        return
    hist[dims[F] - dims[cur[r]]] += 1
    moves[0] += 1
    cur[r] = F

def run(gates):
    for F, d, srcs in gates:
        for r in [d] + srcs:
            climb(r, F)
        for s in srcs:
            val[d] ^= val[s]

tgt_dirt = [0] * v
tgt_scatter = [0] * v
tgt_reads = [0] * v

# THE D-PHASE (the frame-0 gates: one per target!)
for F, d, srcs in W['D']:
    acc = 0
    for s in srcs:
        acc ^= val[s]
    tgt_dirt[d - v] = acc
    for r in [d] + srcs:
        climb(r, F)
    for s in srcs:
        val[d] ^= val[s]
log('(1a) the D-phase: %d gates | the dirt sizes %s | the srcs per gate %s' % (
    len(W['D']), dict(sorted(Counter(bin(x).count('1') for x in tgt_dirt).items())),
    dict(sorted(Counter(len(s) for _, _, s in W['D']).items()))))

# THE A-PHASE!
run(W['A'])
log('(1b) the A-phase: %d gates' % len(W['A']))

# THE SCATTER (+ the rets' frames snapshot!)
ret = W['ret']
ret_frames_at_scatter = [cur[q] for q in ret]
for t in range(v):
    acc = 0
    for k in W['scatter'][t]:
        acc ^= val[ret[k]]
    tgt_scatter[t] = acc
    val[v + t] ^= acc
log('(1c) the scatter: the rets %d | the rets frames at the scatter: the dims %s' % (
    len(ret), dict(sorted(Counter(dims[f] for f in ret_frames_at_scatter).items()))))
log('    the scatter sizes %s | the scatter-row lens %s' % (
    dict(sorted(Counter(bin(x).count('1') for x in tgt_scatter).items())),
    dict(sorted(Counter(len(r) for r in W['scatter']).items()))))

# THE B-PHASE (the instrumented: the target-dests' reads!)
for F, d, srcs in W['B']:
    for r in [d] + srcs:
        climb(r, F)
    if v <= d < 2 * v:
        acc = 0
        for s in srcs:
            acc ^= val[s]
        tgt_reads[d - v] ^= acc
    for s in srcs:
        val[d] ^= val[s]
log('(1d) the B-phase: %d gates | the reads sizes %s' % (
    len(W['B']), dict(sorted(Counter(bin(x).count('1') for x in tgt_reads).items()))))

# THE C-PHASE!
run(W['C'])
log('(1e) the C-phase: %d gates' % len(W['C']))

# THE FINAL CLIMBS!
for r in range(nreg):
    climb(r, final[r])

# ============ (2) THE CONTROL (the finals!!) ============
bad = 0
for r in range(nreg):
    want = (1 << r) ^ ((1 << (r - v)) if v <= r < 2 * v else 0)
    if val[r] != want:
        bad += 1
log('(2) THE CONTROL: the final-value fails %d (the expected 0!!)' % bad)

# ============ (3) THE PER-TARGET ARITHMETIC ============
ok = 0
for t in range(v):
    if (tgt_dirt[t] ^ tgt_scatter[t] ^ tgt_reads[t]) == (1 << t):
        ok += 1
log('(3) THE ARITHMETIC: the [dirt ^ scatter ^ reads] = x_t for %d/%d targets' % (ok, v))
sc_minus = [tgt_scatter[t] ^ (1 << t) for t in range(v)]
log('    the scatter-minus-x_t (the junk delivered!): the sizes %s' %
    dict(sorted(Counter(bin(x).count('1') for x in sc_minus).items())))
# the per-target x-content of the reads (the ~the junk-cancel!): the reads ^ dirt = the cancel!
cancel = [tgt_reads[t] ^ tgt_dirt[t] for t in range(v)]
log('    the [reads ^ dirt] (the cancel!): the sizes %s' %
    dict(sorted(Counter(bin(x).count('1') for x in cancel).items())))

# ============ (4) THE HIST CONTROL (the R420's own!!) ============
copy_ranks = [dims[f] for f in ret_frames_at_scatter]
for c in copy_ranks:
    hist[c] += 1
mass = sum(k * n for k, n in hist.items())
cst = sum(copy_ranks)
ident = h * R + cst + 2 * v * (h - 1)
log('(4) THE HIST: %s | THE CST %d | the mass %d vs the identity %d: %s' % (
    dict(sorted(hist.items())), cst, mass, ident, 'MATCH!!' if mass == ident else 'MISMATCH!!'))
log("    the R420's own hist control: {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9} | the mass 5112")
log('DONE — STAGE 2b-i')
