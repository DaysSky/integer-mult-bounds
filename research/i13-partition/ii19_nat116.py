"""THE nat116: THE r434-SURGERY AT THE COPY BOUND (R: 434 -> 389!!) — THE +8.06% BUILD!!
THE PLAN: remove the ~45 pure-mass 'ACD' registers (the never-B-read (the padding!!)) + their A-gates +
  their D-srcs + their C-reversals -> the R=389 word -> GCHECK (the exact replay (the judge!!!)) -> THE PRICE!!
THE CAUTION: the padding's self-bits may sit in the build-cascades (the wire-DAGs!!) -> the removal breaks the
  y-balance (the gcheck's exact reject tells (the per-register (the 'final value of register %d'!!!))) ->
  the iteration: the 45-subset choice (the leaf-most padding (the A-src-frequency 0!!!))!!
"""
import json, gzip, os, sys
from collections import Counter

log = print
SRC = 'ii19_pub2_p111-r434.json'
W = json.load(open(SRC, 'rt'))
v, R = W['v'], W['R']
base = 2 * v
nreg = 2 * v + R

# the A-src frequency (the padding-as-the-DAG-src?!?)
asrc = Counter()
for F, d, ss in W['A']:
    for s in ss: asrc[s] += 1
bsrc = set(s for F, d, ss in W['B'] for s in ss)
ret = set(W['ret'])
padding = []
for r in range(base, nreg):
    if r in ret or r in bsrc: continue
    padding.append(r)
log('the padding (never-B-read, non-ret): %d | of which A-srcs-in-DAGs: %d' %
    (len(padding), len([r for r in padding if asrc[r] > 0])))
leaf = [r for r in padding if asrc[r] == 0]
log('the leaf-padding (the zero cascade-impact!!): %d' % len(leaf))

# THE SURGERY: remove the LAST 45 leaf-padding (any 45: the hist-delta the same-ish!!)
TRIM = 45
dead = set(leaf[:TRIM])
newR = R - len(dead)
log('the trim: %d -> R = %d (the target 389!!)' % (len(dead), newR))
assert newR == 389

# the re-index map (the register-compaction!!)
remap = {}
for r, q in enumerate([x for x in range(nreg) if x not in dead]):
    remap[q] = r
def remap_reg(x):
    return remap[x]

# the gates: filter + remap!!
def fix_gates(gates):
    out = []
    for F, d, ss in gates:
        if remap_reg(d) is None: continue
        ss2 = [remap_reg(s) for s in ss if remap_reg(s) is not None]
        out.append([F, remap_reg(d), ss2])
    return out
# careful: the D-gates: the srcs: remove the dead (the y-balance?!) — the empirical!!
D2 = []
for F, d, ss in W['D']:
    ss2 = [remap_reg(s) for s in ss if s in remap]
    D2.append([F, remap_reg(d), ss2])
A2 = fix_gates(W['A'])
B2 = fix_gates(W['B'])
# the C: the literal reversal: rebuild from the z-gates of A2+B2!!!
zg = [[F, d, s] for F, d, s in A2 + B2 if not (v <= d < 2 * v)]
C2 = [[W['form'] and 1 or 1, d, s] for F, d, s in reversed(zg)]  # placeholder frame — FIX BELOW!!
# hmm: the C's frame: dims == h: the FULL-frame index: find it!!
full_f = None
for i, F in enumerate(W['frames']):
    if len(F) == 8:
        # the rref-dim check: the 8-vectors: the full span?!
        pass
# the honest: the C's frames must be dim-8: reuse the A's frames?!: the ORIGINAL C's frames: same indices as the zg!!
C2 = []
for F, d, s in reversed(zg):
    # find the zg-matching original frame: the C-reversal: the frame = the FULL-frame index: from the original C!!
    pass
# SIMPLEST: the C's original gates filtered+remapped (the H4-preserved (the zg matches automatically!!))
C2 = []
orig_zg = [[F, d, ss] for F, d, ss in W['A'] + W['B'] if not (v <= d < 2 * v)]
# the ORIGINAL C: the [F, d, [s]]?!: the sample!! — check the C-format first!!
log('the C sample: %s' % (W['C'][0],))
log('the original C: %d gates | the zg: %d' % (len(W['C']), len(orig_zg)))
