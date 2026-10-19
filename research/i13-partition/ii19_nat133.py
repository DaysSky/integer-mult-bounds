"""nat133: THE A-DAG INTERMEDIATES CENSUS (the retirement-feasibility map).

Per intermediate (the 200 A-built, never-B-read registers): its content-lines, its
consumers (the A-gates' dests reading it, and at which frames), its own build-gates,
and the retirement cost: if retired, each consumer's gate reads the intermediate's
srcs directly instead (the src-content law + the one-climb consequences).
Reports the sharing structure (the consumer-counts) and the retirement classes.
"""
import json, gzip
from collections import Counter

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
v = W['v']; R = W['R']; nreg = 2 * v + R
A = W['A']; B = W['B']; D = W['D']
RET = set(W['ret'])

# the replay: the vals + the per-gate frames
val = [0] * nreg
for s in range(v):
    val[s] = 1 << s
for F, d, ss in D:
    for s in ss:
        val[d] ^= val[s]
for F, d, ss in A:
    for s in ss:
        val[d] ^= val[s]

mask_of = lambda x: x & ((1 << v) - 1)
b_read = set()
for F, d, ss in B:
    for s in ss:
        if s >= 2 * v:
            b_read.add(s)

inter = [q for q in range(2 * v, nreg) if q not in b_read and q not in RET]
print('the intermediates: %d' % len(inter))

# per intermediate: content, consumers (the dests reading it + the frames), build-gates
cons = {}
builds = {}
for gi, (F, d, ss) in enumerate(A):
    for s in ss:
        if s >= 2 * v and s not in RET:
            cons.setdefault(s, []).append((d, F))
    builds.setdefault(d, []).append((gi, F, tuple(ss)))
print('the consumer-counts:', dict(sorted(Counter(len(cons.get(q, [])) for q in inter).items())))
# the content-sizes
print('the content-sizes:', dict(sorted(Counter(len(bin(mask_of(val[q]))[2:].replace('0', '')) for q in inter).items())))
# hmm - bitcount properly:
csz = Counter()
for q in inter:
    m = mask_of(val[q])
    csz[bin(m).count('1')] += 1
print('the content-sizes (proper):', dict(sorted(csz.items())))
# the consumers' frames (where the intermediates are read)
fr = Counter()
for q in inter:
    for d, F in cons.get(q, []):
        fr[F] += 1
print('the read-frames of the intermediates: %d distinct' % len(fr))
# the multi-frame intermediates (read at SEVERAL frames - the chain-pins!!)
multi = 0
for q in inter:
    fs = set(F for d, F in cons.get(q, []))
    if len(fs) > 1:
        multi += 1
print('the intermediates read at >1 distinct frame: %d' % multi)
# the build-depth (the srcs: the sources vs the other intermediates)
dep = Counter()
for q in inter:
    srcs = set()
    for gi, F, ss in builds.get(q, []):
        srcs.update(ss)
    dep[(sum(1 for s in srcs if s < v), sum(1 for s in srcs if s >= 2 * v and s not in RET))] += 1
print('the build-src classes (sources, intermediates):')
for k, c in sorted(dep.items()):
    print('   %-12s x %d' % (str(k), c))
# the retirement classes: the consumers' frame-alignment (if all the consumers read at the
# same frame class, the retirement is a clean swap)
ret_clean = 0
for q in inter:
    fs = set(F for d, F in cons.get(q, []))
    if len(fs) <= 1:
        ret_clean += 1
print('the clean-retirement intermediates (single read-frame): %d' % ret_clean)
