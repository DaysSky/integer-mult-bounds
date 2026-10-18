"""THE WORD3 SP-CHANNEL INSPECTION — the inputs for the word4 redesign (ii19_own8!!)."""
import json
W3 = json.load(open('ii19_ext_word3.json', 'rt'))
V, H, R, SP = W3['v'], W3['h'], W3['R'], 120
D, A, B, C = W3['D'], W3['A'], W3['B'], W3['C']
lines, frames, start, final = W3['lines'], W3['frames'], W3['start'], W3['final']
ret_list, ret_frames0, scatter0 = W3['ret'], W3['ret_frames'], W3['scatter']
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(fr)] for fr in frames]
nreg0 = 2 * V + R

print('frames (ix, dim, len, has-special?):')
for i, fr in enumerate(frames):
    print('  ix=%d dim=%d len=%d special-in=%s' % (i, dims[i], len(fr), SP in fr))

print('start[0..7] =', start[:8])
print('start[SP] =', start[SP], '(frame %d dim %d)' % (start[SP], dims[start[SP]]) if start[SP] < len(frames) else start[SP])
print('final[SP] =', final[SP])
print('final[V+SP] =', final[V + SP])
print('ret_list =', ret_list)
print('ret_frames0 =', ret_frames0)
print('scatter0[SP] =', scatter0[SP], '(size %d)' % len(scatter0[SP]))
print('scatter0 sizes:', sorted(set(len(s) for s in scatter0)))

print('D gates with dest in [V+SP] or srcs containing SP:')
for F, d, srcs in D:
    if d == V + SP or SP in srcs:
        print('  D [F=%d (dim %d), d=%d, srcs=%s]' % (F, dims[F], d, srcs))

print('A gates with SP in srcs or d==SP:')
for F, d, srcs in A:
    if d == SP or SP in srcs:
        print('  A [F=%d (dim %d), d=%d, srcs=%s]' % (F, dims[F], d, srcs))

print('B gates with dest V+SP (the SP-read gates!!):')
for F, d, srcs in B:
    if d == V + SP:
        print('  B [F=%d (dim %d), d=%d, srcs=%s]' % (F, dims[F], d, srcs))

print('B gates with SP in srcs (any dest):')
for F, d, srcs in B:
    if SP in srcs:
        print('  B [F=%d (dim %d), d=%d, srcs=%s]' % (F, dims[F], d, srcs))

print('C gates with dest V+SP or SP in srcs:')
for F, d, srcs in C:
    if d == V + SP or SP in srcs:
        print('  C [F=%d (dim %d), d=%d, srcs=%s]' % (F, dims[F], d, srcs))

print('B-gate dest-classes:', sorted(set(d for F, d, s in B)))
print('number of B gates with target dests:', sum(1 for F, d, s in B if V <= d < 2 * V))
print('the zregs: which registers have x-part with SP bit? (the replay)')
XMASK = (1 << V) - 1
val = [1 << i for i in range(nreg0)]
cur = list(start)
def climb(r, F):
    global cur
    if cur[r] != F:
        assert dims[F] >= dims[cur[r]]
        cur[r] = F
for F, d, srcs in D:
    for r in [d] + srcs: climb(r, F)
    for s in srcs: val[d] ^= val[s]
for F, d, srcs in A:
    for r in [d] + srcs: climb(r, F)
    for s in srcs: val[d] ^= val[s]
for k, r in enumerate(ret_list):
    print('  ret %d (reg %d): x-popcount %d, phi(SP)=%d, start=%d final=%d' % (
        k, r, bin(val[r] & XMASK).count('1'), (val[r] >> SP) & 1, start[r], final[r]))
print('cur[SP] at end of A =', cur[SP], '(dim %d)' % dims[cur[SP]])
