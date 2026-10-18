"""THE B-READ STRUCTURE CENSUS (ii19_nat79.py) — the co-read frames (the r434's 5-helper pattern!!).

THE CURRENT WORD (nat78!!): the climbs/content/scatter/C ALL PASS ✓✓✓ — THE VALUE-FRONT
(the delivery!!). THE TARGETS' READS: the ~16 pieces/target (the 54-piece economy!!) at
the pieces' PF-frames (dims 2-3!!) — THE ONE-FRAME-PER-DIM WALL -> THE r434's OWN
PATTERN: THE CARRIERS (the per-target perp-local assemblers!!). THE CENSUS: the pieces'
PF-dims + the per-target co-read structures (the dim-collisions (the carrier-load!!)
+ THE CARRIER-DESIGN SPEC (the z-class (the perp-local!!!)).
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
lines = [tuple(int(x) for x in l) for l in SPEC['lines']]
V = len(lines)
PERP = [set(p) for p in SPEC['PERP']]
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool = [(sorted(p), sorted(u)) for p, u in P70['pool']]

# the nat78's matching (reproduced!!)
bc_used = set()
kept = []
order = sorted(range(len(pool)), key=lambda i: -len(pool[i][1]))
for i in order:
    ps, users = pool[i]
    found = None
    for a in ps:
        bc = [s for s in ps if s != a]
        if bc[0] in bc_used or bc[1] in bc_used:
            continue
        found = (a, bc)
        break
    if found is None:
        continue
    a, bc = found
    bc_used |= set(bc)
    kept.append((i, a, bc))
log('the kept pieces: %d' % len(kept))

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
def span_dim(idx):
    return len(rref([list(lines[x]) for x in sorted(set(idx))], 8))

# the per-target piece-loads + the PF-dims!!
pfdim = {}
for k, (i, a, bc) in enumerate(kept):
    pfdim[k] = span_dim([a] + bc)
log('the PF-dims: %s' % dict(sorted(Counter(pfdim.values()).items())))
tloads = Counter()
tdims = defaultdict(Counter)
for k, (i, a, bc) in enumerate(kept):
    for t in pool[i][1]:
        tloads[t] += 1
        tdims[t][pfdim[k]] += 1
log('the per-target piece-loads: %s' % dict(sorted(Counter(tloads.values()).items())))
# the dim-collisions (the co-read structure: the pieces at the same dim for one target!!)
coll = Counter()
for t in range(V):
    for d, cnt in tdims[t].items():
        if cnt > 1:
            coll[t] += cnt - 1
log('the dim-collisions: %d targets hit (the total collisions %d!!)' % (
    len(coll), sum(coll.values())))
log('  the collisions per target: %s' % dict(sorted(Counter(coll.values()).items())))
# the co-read CLASSES: the pieces whose PFs SHARE... hmm the PFs are distinct frames —
# the target's dim-d classes: the pieces at the same dim MUST be read at ONE frame ->
# THE CARRIER: the per-target per-dim assemblers (the z-class!!)!!
log('THE CARRIER-SPEC: the per-target dim-d carriers (the co-read assemblers!!):')
carrier_count = sum(max(0, cnt - 1) for t in range(V) for d, cnt in tdims[t].items())
log('  the ~%d extra carriers (the co-read assemblies!!)' % carrier_count)
# the honest alternative: THE TARGET's SINGLE CARRIER (ONE per target!!): the reads of
# ALL its pieces at the SHARED... the pieces' PFs (incomparable!!): the CARRIER visits
# them?! — the same wall... THE CARRIER AT THE PERP (dim 7!!): reads the pieces AT
# THE PIECES' POSITIONS?! — the carrier's chain: 0 -> ... (the multi-PF wall!!)
# THE RESOLUTION (THE r434's): the pieces CLIMB (the read-frames shared (the z-class!!))
log('saved the census (the B-read spec!!)')
json.dump({'pfdim': pfdim, 'tloads': dict(tloads),
           'tdims': {str(t): dict(c) for t, c in tdims.items()}},
          open('ii19_nat79_bread.json', 'w'))
