"""THE WORD4 t*-DIAGNOSIS: which target's old scatter row differs from the unique Wp rep,
and what the residue is (the fix = a B-gate read of the old rets in the delta!!)."""
import json
from collections import Counter
W3 = json.load(open('ii19_ext_word3.json', 'rt'))
V, H, R, SP = W3['v'], W3['h'], W3['R'], 120
lines = W3['lines']; frames = W3['frames']
ret_list, scatter0 = W3['ret'], W3['scatter']
D, A, B = W3['D'], W3['A'], W3['B']
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(fr)] for fr in frames]
nreg0 = 2 * V + R
XMASK = (1 << V) - 1

# replay the A-phase (the rets' values)
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
xp = [val[r] & XMASK for r in ret_list]

# the unique solve over the 10 (the own8's Wp machinery, compact)
rows = list(xp); aug = [[1 if i == j else 0 for j in range(10)] for i in range(10)]
rr = 0; pivots = []; T = []
for col in range(V):
    piv_i = next((i for i in range(rr, 10) if (rows[i] >> col) & 1), None)
    if piv_i is None: continue
    rows[rr], rows[piv_i] = rows[piv_i], rows[rr]
    aug[rr], aug[piv_i] = aug[piv_i], aug[rr]
    for i in range(10):
        if i != rr and (rows[i] >> col) & 1:
            rows[i] ^= rows[rr]; aug[i] = [a ^ b for a, b in zip(aug[i], aug[rr])]
    pivots.append((col, rows[rr])); T.append(list(aug[rr])); rr += 1
assert rr == 10
def solve10(row):
    coords = [0] * 10; x = row
    for k, (col, rw) in enumerate(pivots):
        if (x >> col) & 1:
            coords[k] = 1; x ^= rw
    assert x == 0
    return coords
def ip121(a, b): return sum(a[i] * b[i] for i in range(8)) + 2 * a[8] * b[8]
Brows = []
for t in range(V):
    m = 1 << t
    for u in range(V):
        if u != t and ip121(lines[t], lines[u]) == 0:
            m |= 1 << u
    Brows.append(m)

print('t | old-row (10) | Wp[t] (10) | delta | old-x==Brows[t]?')
bad = []
for t in range(V):
    Wp_t = solve10(Brows[t])
    old = sorted(scatter0[t])
    wp = sorted(k for k in range(10) if Wp_t[k])
    if old != wp:
        delta = sorted(set(old) ^ set(wp))
        oldx = 0
        for k in old: oldx ^= xp[k]
        print('t=%d: old=%s | Wp=%s | delta=%s | old-x==Brows: %s | old-x popcount %d' % (
            t, old, wp, delta, oldx == Brows[t], bin(oldx).count('1')))
        bad.append((t, old, wp, delta))
print('the mismatching targets: %d' % len(bad))

# the t* channel: the B gates + the final frame + the old rets' frames
for (t, old, wp, delta) in bad:
    print('--- t* = %d (the target reg %d) ---' % (t, V + t))
    print('  final frame: %d (dim %d)' % (W3['final'][V + t], dims[W3['final'][V + t]]))
    print('  the D gates:')
    for F, d, srcs in W3['D']:
        if d == V + t:
            print('    [F=%d, d=%d, srcs=%s]' % (F, d, srcs))
    print('  the B gates:')
    for F, d, srcs in W3['B']:
        if d == V + t:
            print('    [F=%d (dim %d), d=%d, srcs=%s]' % (F, dims[F], d, srcs))
    print('  the delta rets (registers %s, frames:' % [ret_list[k] for k in delta])
    for k in delta:
        r = ret_list[k]
        print('    ret %d = reg %d: B-time frame %d (dim %d)' % (k, r, cur[r], dims[cur[r]]))
    # the residue check: XOR of the delta rets' values = the residue?
    resx = 0; resd = 0
    for k in delta:
        v = val[ret_list[k]]
        resx ^= v & XMASK
        resd ^= v >> V
    print('  the delta-XOR: x-popcount %d, dirt-popcount %d' % (
        bin(resx).count('1'), bin(resd).count('1')))
