"""THE R420-EXTENSION BUILD — STAGE 1: THE LOAD + THE SYSTEM + THE RE-BASE (ii19_ext.py).

THE ONE UNTRIED PATH (the commit 61d634e4!!): the R420's published word (the gcheck-PASSING!)
re-based to the h=9 (the +1 final climb per register: the nested chains 0->...->8->9 LEGAL!)
+ the special's extension -> the gcheck -> THE TRUE HIST -> THE TRUE c!! — THE BUILD ANSWERS
THE AUDIT's #8/#14 BOTH (the climb shapes + the true c!!)!

THE HONEST EXPECTATION (the d210c316 scan!!): the dr=9 bands: -34.80% to -50.28% at every
R 380-511 — BELOW at every honest configuration — the build CONFIRMS the definitive true c!
THE MILESTONE EITHER WAY: the FIRST gcheck-PASSING II19-family word (the real, the constructed!)

THE STAGE 1 (this script!):
  (1) THE R420's WORD: the load + the anatomy's re-verification (the frames: the line-index
      lists; the dims: the SPANS!!)
  (2) THE 121-LINE SYSTEM: the R420's own 120 lines (the +0 -> the 9-dim!!) + THE SPECIAL
      (the (0,...,0,1): the norm 2, the ⊥ to all the roots — the diag(1^8, 2) form!!)
  (3) THE RE-BASE: the frames' map: the SAME line-lists; the FULL + the perps: THE +SPECIAL
      (the special ∈ perp(t) for every root t!!) — the 63-line perps -> the 64-line!!
  (4) THE VERIFICATION: the spans' re-computation over the 121-line form — the EXPECTED dims:
      {0: 1, 1: 120, 2: 180, 4: 70, 6: 180, 8: 120, 9: 1} (the perps: the 7 -> 8; the FULL: the 9!)
"""
import gzip, json, sys, time
from fractions import Fraction
from collections import Counter
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (1) THE R420's WORD ============
W = json.load(gzip.open('research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
log('(1) the R420: v=%d h=%d R=%d' % (W['v'], W['h'], W['R']))
log('    the keys: %s' % sorted(W.keys()))
frames = W['frames']
lc = Counter(len(f) for f in frames)
log('    the frames: %d | the line-counts %s' % (len(frames), dict(sorted(lc.items()))))
lines = W['lines']
log('    the lines: %d | the sample [0]: %s' % (len(lines), lines[0]))

# ============ (2) THE 121-LINE SYSTEM (the 9-dim!!) ============
# the R420's own 120 lines (+0 -> the 9-dim) + the special (0,...,0,1)!!
V9 = []
for L in lines:
    v = list(L) + [0]
    V9.append(v)
SPECIAL = [0] * 8 + [1]
V9.append(SPECIAL)
V = 121
log('(2) the 121-line system: V=%d (the 120 roots + the special (0,..,0,1)!!)' % V)

def ipv(u, w):
    s = 0
    for i in range(8):
        s += u[i] * w[i]
    s += 2 * u[8] * w[8]
    return s

norms = Counter(ipv(x, x) for x in V9)
log('    the norms: %s' % dict(sorted(norms.items())))
sp = [s for s in range(V) if V9[s][8] != 0]
log('    the special index: %s' % sp)
# the special ⊥ all the roots!!
bad = [r for r in range(120) if ipv(V9[r], V9[120]) != 0]
log('    the special ⊥-fails vs the roots: %d' % len(bad))

# ============ (3) THE RE-BASE: the frames' map ============
# the frames: the SAME line-lists; the FULL + the perps: the +special!!
SP = 120
rb_frames = []
kinds = []
for f in frames:
    fl = list(f)
    if len(fl) == 120:                 # the FULL: the +special -> the 121!!
        fl = fl + [SP]
        kinds.append('FULL')
    elif len(fl) == 63:                 # the t-perps: the +special (the ⊥ to all roots!!)
        fl = fl + [SP]
        kinds.append('perp')
    else:
        kinds.append('same')
    rb_frames.append(fl)
kc = Counter(kinds)
log('(3) the re-based frames: the kinds %s' % dict(sorted(kc.items())))

# ============ (4) THE VERIFICATION: the spans' re-computation ============
def rref_dim(rows):
    """the span's dim over Q (the EXACT Gaussian elimination with Fractions!!)."""
    M = [[Fraction(x) for x in r] for r in rows]
    dim = 0
    piv = []
    for c in range(9):
        pr = None
        for i in range(dim, len(M)):
            if M[i][c] != 0:
                pr = i
                break
        if pr is None:
            continue
        M[dim], M[pr] = M[pr], M[dim]
        pv = M[dim][c]
        for i in range(dim + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / pv
                for j in range(c, 9):
                    M[i][j] -= f * M[dim][j]
        piv.append(c)
        dim += 1
        if dim == 9:
            break
    return dim, piv

dims = {}
fail = 0
for f in rb_frames:
    if len(f) == 0:
        d = 0
    else:
        d, _ = rref_dim([V9[i] for i in f])
    dims[d] = dims.get(d, 0) + 1
log('(4) the re-based dims (the spans over the 121-line form!!): %s' % dict(sorted(dims.items())))
log('    THE EXPECTED: {0: 1, 1: 120, 2: 180, 4: 70, 6: 180, 8: 120, 9: 1}')
log('    the full-frame dim check: %s' % (rref_dim([V9[i] for i in rb_frames[frames.index([l for l in frames if len(l) == 120][0])]])[0] if any(len(l) == 120 for l in frames) else 'NO FULL FRAME!!'))
# the special-containing frames' dims: the +1 verification!!
perp_dims = Counter()
for f, k in zip(rb_frames, kinds):
    if k == 'perp':
        d, _ = rref_dim([V9[i] for i in f])
        perp_dims[d] += 1
log('    the perps (the 64-line): the dims %s (the expected: the 8!!)' % dict(sorted(perp_dims.items())))
log('DONE — STAGE 1')
