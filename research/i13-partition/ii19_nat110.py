"""THE nat110: THE r434's PER-REGISTER ROLE CENSUS (the bound-tight trim list!!)
THE TARGET: the r434 (R=434, cst=63, +0.65%) sits ~45 over the v=111 copy bound (~389);
the trim's mass must come off the RANK-1s (the dying-wire ladders!!) -> +8.06% at the bound!!
THE METHOD: (1) load the r434 word; (2) classify each helper by its role
  (the A-dest gates (its build!!), the B-src counts (its readers!!), the frames visited!!);
  (3) the nat108b/c cell overlay: the 315 hyperplane-section covers (the D4 4-frame triples!!)
  -> which helpers serve which cells; (4) the over-counted cells (> 3 registers!!) -> THE TRIM LIST.
"""
import json
from collections import Counter, defaultdict

log = print
W = json.load(open('ii19_pub2_p111-r434.json', 'rt'))
V = W['v']; R = W['R']
log('the word: v=%d R=%d' % (V, R))
A = W['A']; B = W['B']; D = W['D']; C = W['C']
ret = W['ret']; scatter = W['scatter']
frames = W['frames']

# (1) THE HELPER ROLE CENSUS
NH = R  # the helpers [2V, 2V+R)
base = 2 * V
helpers = list(range(base, base + R))
adest = defaultdict(list)   # q -> the A-gates building it
bsrc = defaultdict(list)    # q -> the B-gates reading it
dsrc = defaultdict(int)     # q -> the D-reads
bdest = defaultdict(list)
zdest = defaultdict(list)
for gi, (F, d, ss) in enumerate(A):
    if d >= base: adest[d].append((gi, F, len(ss)))
for gi, (F, d, ss) in enumerate(B):
    if d >= base and d < base + 0: pass
    for s in ss:
        if s >= base: bsrc[s].append((gi, F, d))
    if d >= base: bdest[d].append((gi, F, len(ss)))
for gi, (F, d, ss) in enumerate(D):
    for s in ss:
        if s >= base: dsrc[s] += 1

role = Counter()
for q in helpers:
    na = len(adest[q]); nb = len(bsrc[q]); nd = dsrc[q]
    is_ret = q in ret
    if is_ret: role['ret (the decoder totals!!)'] += 1
    elif na > 0 and nb > 0: role['built+read (the shared nodes!!)'] += 1
    elif na > 0 and nb == 0 and nd == 0: role['built-only (the mass/z-wires!!)'] += 1
    elif na == 0 and nb > 0: role['read-only?!'] += 1
    elif nd > 0 and na == 0 and nb == 0: role['d-only (the pre-cancel sinks!!)'] += 1
    else: role['other'] += 1
log('(1) THE HELPER ROLES: %s' % dict(role))
log('    the ret: %d | the A-gates %d | the B-gates %d | the D-gates %d' % (len(ret), len(A), len(B), len(D)))

# (2) THE BUILD GATES CENSUS (the A-frame dims (the rank-1-heavy builds!!))
fdim = Counter()
for gi, (F, d, ss) in enumerate(A):
    if d >= base:
        fdim[len(frames[F])] += 1
log('(2) THE HELPER-BUILD FRAME DIMS: %s' % dict(sorted(fdim.items())))
sizes = Counter(len(ss) for gi, (F, d, ss) in enumerate(A) if d >= base)
log('    the build src-counts: %s' % dict(sorted(sizes.items())))

# (3) THE READER-LOAD CENSUS (the B-sides!!)
load = Counter()
for q in helpers:
    if q in ret: continue
    load[len(bsrc[q])] += 1
log('(3) THE READER LOADS (the non-ret helpers): %s' % dict(sorted(load.items())))

# (4) THE DYING-READ CENSUS (the B-gates at dim-7 (the perp-frames!!))
dim7 = 0; dimx = Counter()
for gi, (F, d, ss) in enumerate(B):
    if len(frames[F]) == 7: dim7 += 1
    dimx[len(frames[F])] += 1
log('(4) THE B-GATE FRAMES: %s | the dim-7 (the dying reads!!): %d' % (dict(sorted(dimx.items())), dim7))

# (5) THE GATE-SIZE CENSUS (the multi-src usage!!)
bsz = Counter(len(ss) for F, d, ss in B)
log('(5) THE B-GATE SRC-COUNTS: %s' % dict(sorted(bsz.items())))
asz = Counter(len(ss) for F, d, ss in A)
log('    the A-GATE SRC-COUNTS: %s' % dict(sorted(asz.items())))

# (6) THE TRIM CANDIDATES: the built-only helpers (the mass/z-wires!!)
zlist = [q for q in helpers if len(adest[q]) > 0 and len(bsrc[q]) == 0 and dsrc[q] == 0 and q not in ret]
log('(6) THE TRIM CANDIDATES (the built-only!!): %d' % len(zlist))
log('    their A-gates: %d | their build-mass (the rank-1 share!!): TBD-by-frame-dims')
zmass = Counter()
for q in zlist:
    for gi, F, ns in adest[q]:
        zmass[len(frames[F])] += 1
log('    their build-frame dims: %s' % dict(sorted(zmass.items())))
