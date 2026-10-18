"""THE WORD3 241-CHANNEL TRACE (the gcheck semantics!!) — resolve the 605/570 leftover
puzzle + the [253]x2 gates before the word4 redesign (ii19_own8!!)."""
import json
W3 = json.load(open('ii19_ext_word3.json', 'rt'))
V, H, R, SP = W3['v'], W3['h'], W3['R'], 120
D, A, B, C = W3['D'], W3['A'], W3['B'], W3['C']
start, final = W3['start'], W3['final']
ret_list, scatter0 = W3['ret'], W3['scatter']
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(fr)] for fr in W3['frames']]
nreg = 2 * V + R
XMASK = (1 << V) - 1

val = [1 << i for i in range(nreg)]
cur = list(start)
def climb(r, F):
    if cur[r] != F:
        assert dims[F] >= dims[cur[r]]
        cur[r] = F
def bits(x, lo=0, hi=None):
    hi = nreg if hi is None else hi
    return [i for i in range(lo, hi) if (x >> i) & 1]

print('A gates with d in {605, 570, 253}:')
for F, d, srcs in A:
    if d in (605, 570, 253):
        print('  A [F=%d (dim %d), d=%d, srcs=%s]' % (F, dims[F], d, srcs))
print('B gates with srcs containing 605 or 570 or 253:')
for F, d, srcs in B:
    if any(s in (605, 570, 253) for s in srcs):
        print('  B [F=%d (dim %d), d=%d, srcs=%s]' % (F, dims[F], d, srcs))
print('A gates with srcs containing 253:')
for F, d, srcs in A:
    if 253 in srcs:
        print('  A [F=%d (dim %d), d=%d, srcs=%s]' % (F, dims[F], d, srcs))

T = V + SP
def show(tag):
    x = val[T]
    print('  %-14s tgt-241: own=%d xbits=%d helperbits=%s dirt241=%d' % (
        tag, (x >> T) & 1, bin(x & XMASK).count('1'),
        bits(x, 2 * V), (x >> T) & 1))

for F, d, srcs in D:
    for r in [d] + srcs: climb(r, F)
    for s in srcs: val[d] ^= val[s]
show('after D')
for F, d, srcs in A:
    for r in [d] + srcs: climb(r, F)
    for s in srcs: val[d] ^= val[s]
show('after A')
for t in range(V):
    for k in scatter0[t]:
        val[V + t] ^= val[ret_list[k]]
show('after scatter')
print('  val[253] helperbits=%s xbits=%d' % (bits(val[253], 2 * V), bin(val[253] & XMASK).count('1')))
for gi, (F, d, srcs) in enumerate(B):
    for r in [d] + srcs: climb(r, F)
    for s in srcs: val[d] ^= val[s]
    if d == T:
        show('after B#%d' % gi)
        print('     gate=[F=%d, d=%d, srcs=%s] | cur[241]=%d (dim %d)' % (F, d, srcs, cur[T], dims[cur[T]]))
for F, d, srcs in C:
    for r in [d] + srcs: climb(r, F)
    for s in srcs: val[d] ^= val[s]
show('after C')
for r in range(nreg): climb(r, final[r])
show('after finals')
want = (1 << T) ^ (1 << SP)
print('want = own ^ e120 | match: %s' % (val[T] == want))
print('final x-part = bits %s' % bits(val[T] & XMASK))
print('final helper-bits = %s' % bits(val[T], 2 * V))
