"""THE REGISTER-REUSE SCAN: could an EXISTING word3 helper BE one of the 8 even-rets or
the O0-carrier? (val[h] ^ 1<<h == the combo!!) -> the R-reduction (R 472 -> 472 - k!!)."""
import json
from collections import Counter
W3 = json.load(open('ii19_ext_word3.json', 'rt'))
V, H, R, SP = W3['v'], W3['h'], W3['R'], 120
lines = W3['lines']
ret_list, scatter0 = W3['ret'], W3['scatter']
D, A = W3['D'], W3['A']
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(fr)] for fr in W3['frames']]
nreg0 = 2 * V + R
XMASK = (1 << V) - 1

# the A-END (= scatter-time!!) values: replay D + A
val = [1 << i for i in range(nreg0)]
cur = list(W3['start'])
def climb(r, F):
    if cur[r] != F:
        assert dims[F] >= dims[cur[r]]
        cur[r] = F
for F, d, srcs in D:
    for r in [d] + srcs: climb(r, F)
    for s in srcs: val[d] ^= val[s]
for F, d, srcs in A:
    for r in [d] + srcs: climb(r, F)
    for s in srcs: val[d] ^= val[s]

# the targets: the 8 even-combos (the repB!!) + the O0-carrier
# repB[j] = Wp[0] ^ Wp[sel[j]] over the 10 old rets (the diag3 table!!):
reps = [[0,1,1,0,0,0,0,0,0,0], [0,1,0,1,0,0,0,0,0,0], [0,1,0,0,1,0,0,0,0,0],
        [0,1,0,0,0,1,0,0,0,0], [0,1,1,1,1,1,0,0,0,0], [0,1,0,0,0,0,1,0,0,0],
        [0,1,0,0,0,0,0,1,0,0], [0,1,0,0,0,0,0,0,1,0]]
combos = []
for j in range(8):
    acc = 0
    for q in range(10):
        if reps[j][q]: acc ^= val[ret_list[q]]
    combos.append((j, acc, 'even-%d (the repB %s!!)' % (j, [q for q in range(10) if reps[j][q]])))
combos.append((8, val[ret_list[0]], 'THE O0-CARRIER (= val[605]!!)'))

print('THE SCAN: the %d helpers vs %d target-combos (the FULL values!!)' % (R, len(combos)))
hits = []
for h in range(2 * V, nreg0):
    c_h = val[h] ^ (1 << h)              # the build-value (the non-self part!!)
    for (j, acc, tag) in combos:
        if c_h == acc:
            hits.append((h, j, cur[h], dims[cur[h]], tag))
for (h, j, f, d, tag) in hits:
    print('  HIT: the helper %d (at the frame %d, dim %d) == %s' % (h, f, d, tag))
print('the hits: %d' % len(hits))
if not hits:
    print('NO REUSE — the fresh registers FORCED (the R 472 honest!!)')

# ALSO: the nearest-miss census (the x-part-only matches!!) — the info for a future lever!!
xhits = []
targets_x = [(j, acc & XMASK, tag) for (j, acc, tag) in combos]
for h in range(2 * V, nreg0):
    xh = val[h] & XMASK
    if not xh: continue
    for (j, ax, tag) in targets_x:
        if xh == ax:
            xhits.append((h, j, cur[h], dims[cur[h]], tag, bin(val[h] >> V).count('1')))
print('the X-PART-ONLY matches (the dirt off!!): %d' % len(xhits))
for (h, j, f, d, tag, dn) in xhits[:20]:
    print('  xHIT: the helper %d (frame %d, dim %d) == %s (the dirt-popcount %d!!)' % (
        h, f, d, tag, dn))
