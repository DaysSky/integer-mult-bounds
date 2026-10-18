"""THE P111-R434 SHAVE-HUNT (ii19_p111w15.py) — THE FRONTIER-WORD's-OWN-REGISTERS!!!

THE SENSITIVITY (the true-shape (§1895!!)): the ~0.157%/register (the r434: +0.654%!!) ->
THE EVERY-REGISTER = THE +0.157%!!! THE TARGETS: R = 434 -> 428 (+0.94%!!) -> 420 (+2.2%!!!)

THE MECHANISM-THEORY (the W4's-lessons (§1996: the root-fails (the 121's-own!!!))):
  - THE P111 (the pure-E8 (the no-special!!)): the DIFFERENT-structure (the untried!!)
  - THE CANDIDATES: (a) THE SINGLE-READ-HELPERS (the val-consumed-ONCE (the mergeable into
    the consumer's-gate (the srcs'-direct!!!))); (b) THE SINGLE-WRITE-HELPERS (the pure
    accumulators (the never-read?! (the DEAD?!))); (c) THE IDENTITY-CHAINS (the h1 -> h2
    with-the-same-content (the COLLAPSIBLE!!!))

THE MEASURE: the per-helper: the #writes (the A-dest!!) | the #reads (the A/B/C/D-srcs + the
scatter!!) | the climb-frames (the chain!!) | the content (the x-part!!) -> THE CENSUS!!!
"""
import json, time
from collections import Counter
from fractions import Fraction

w = json.load(open('ii19_pub2_p111-r434.json', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

V, H, R = w['v'], w['h'], w['R']
nreg = len(w['start'])
ret = w['ret']
log('(0) the r434: v=%d h=%d R=%d nreg=%d (the rets %s)' % (V, H, R, nreg, ret))

# the usage-census!!
writes = Counter()   # the A-dest-hits!!
reads = Counter()    # the any-src-hits!!
D_srcs = Counter()
A_srcs = Counter()
B_srcs = Counter()
C_srcs = Counter()
for F, d, srcs in w['D']:
    writes[d] += 1
    for s in srcs:
        reads[s] += 1; D_srcs[s] += 1
for F, d, srcs in w['A']:
    writes[d] += 1
    for s in srcs:
        reads[s] += 1; A_srcs[s] += 1
for F, d, srcs in w['B']:
    writes[d] += 1
    for s in srcs:
        reads[s] += 1; B_srcs[s] += 1
for F, d, srcs in w['C']:
    writes[d] += 1
    for s in srcs:
        reads[s] += 1; C_srcs[s] += 1
scat_reads = Counter()
for row in w['scatter']:
    for k in row:
        scat_reads[ret[k]] += 1
helpers = [r for r in range(2 * V, nreg)]
log('(1) THE HELPERS: %d' % len(helpers))
census = {}
for h in helpers:
    census[h] = (writes[h], reads[h] - scat_reads[h], scat_reads[h])
wc = Counter((c[0], c[1], c[2]) for c in census.values())
log('    the (writes, reads, scatter-reads)-census: %s' % dict(sorted(wc.items())))
# the special-classes!!
dead = [h for h in helpers if census[h][0] == 0 and census[h][1] == 0 and census[h][2] == 0]
log('    THE DEAD (never-touched!!): %d %s' % (len(dead), dead[:10]))
unwritten = [h for h in helpers if census[h][0] == 0]
log('    THE UNWRITTEN: %d (the reads %s!!)' % (len(unwritten),
    dict(sorted(Counter(census[h][1] for h in unwritten).items()))))
single_read = [h for h in helpers if census[h][1] == 1 and census[h][2] == 0]
log('    THE SINGLE-READ (the merge-candidates!!): %d (the writes %s!!)' % (
    len(single_read), dict(sorted(Counter(census[h][0] for h in single_read).items()))))
never_read = [h for h in helpers if census[h][1] == 0 and census[h][2] == 0 and census[h][0] > 0]
log('    THE WRITE-ONLY (the DEAD-WEIGHT?!): %d' % len(never_read))
# the single-read-single-write (the pure-relays (the 1->1-chains!!))
pure = [h for h in helpers if census[h][0] == 1 and census[h][1] == 1 and census[h][2] == 0]
log('    THE PURE-RELAYS (1-write-1-read!!): %d' % len(pure))
# the rets'-details!!
for q in ret:
    log('    THE RET %d: the writes %d | the reads %d | the scatter %d' % (
        q, writes[q], reads[q] - scat_reads[q], scat_reads[q]))

# (2) THE CLIMB-CHAINS (the per-helper: the frames-sequence (the replay!!)!!)
def rref(rows, n):
    m = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]
fr = [rref(F, H) for F in w['frames']]
dims = [len(F) for F in fr]
cur = list(w['start'])
chain = {r: [cur[r]] for r in range(nreg)}
val = [1 << r for r in range(nreg)]
X = (1 << V) - 1
for F, d, srcs in w['D']:
    for r in [d] + srcs:
        if cur[r] != F:
            cur[r] = F; chain[r].append(F)
    for s in srcs: val[d] ^= val[s]
for F, d, srcs in w['A']:
    for r in [d] + srcs:
        if cur[r] != F:
            cur[r] = F; chain[r].append(F)
    for s in srcs: val[d] ^= val[s]
log('(2) THE CLIMB-CHAINS (the A-end!!): the per-helper-dims-sequence-census:')
seq_c = Counter()
for h in helpers:
    seq_c[tuple(dims[f] for f in chain[h])] += 1
for k in sorted(seq_c):
    log('    %s: %d' % (k, seq_c[k]))
# the contents (the x-parts (the A-end!!))
CONT = {h: bin(val[h] & X).count('1') for h in helpers}
log('    the x-weights-census: %s' % dict(sorted(Counter(CONT.values()).items())))
log('DONE — THE SHAVE-HUNT-CENSUS!!!')
