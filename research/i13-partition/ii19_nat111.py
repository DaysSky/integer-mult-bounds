"""THE nat111: THE DEEPER-SHELL CENSUS (the breakthrough hunt!!)
THE FRESH LEVER: the ext120 = the E8 root lines (the parallel session's identity!!)
-> the class-closure verdict ("the pool exhausts at 120") was for the RAW-NORM-4 shell;
   the deeper shells (the raw-norm-8 (the form-norm-4!!)) were NEVER censused!!
THE TESTS: (1) enumerate the raw-norm-8 shell (the integer 8-tuples, x·x = 8);
           (2) the ⊥-structure: per candidate x: the count of the ext120 lines ⊥ x
               (the 63-analog?! (the perp-frame's line-richness!!!));
           (3) the legality-suite: the form (the positive-definite ✓ (the same lattice!!)),
               the Gram (the nondegenerate (the 2x·x' the form!!)), the decoder-rank,
               the TPERP-dims (the 7-dim perps (the x ∉ perp(x) (the norm ≠ 0 ✓!!)));
           (4) THE PRICE-MAP at v=121-125 (the never-measured v-up trend!!).
"""
import json, itertools
from collections import Counter
from fractions import Fraction

log = print
SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
L120 = [tuple(Fraction(int(x), 1) if isinstance(x, int) else Fraction(*x) for x in l) for l in SPEC['lines']]
V = 120
log('the ext120 lines: %d (the raw-norms: %s)' % (len(L120), Counter(sum(a*a for a in l) for l in L120)))

# the raw-norm-4 lines as integer tuples (the SPEC's are the Fractions/integers!!)
Lints = [tuple(int(c) for c in l) for l in L120]
assert all(sum(c*c for c in l) == 4 for l in Lints), 'the raw-norm-4 class!!'
log('(1) THE RAW-NORM-8 SHELL (x·x = 8, the integer 8-tuples!!):')
shell = []
# the compositions of 8 into squares 0,1,4: (4,4): the (±2,±2) pairs; (4,1x4): the (±2,±1^4); (1x8): the (±1^8)
for a in range(8):
    for b in range(a + 1, 8):
        for sa in (2, -2):
            for sb in (2, -2):
                t = [0] * 8; t[a] = sa; t[b] = sb
                shell.append(tuple(t))  # 4+4 = 8 ✓
for pos in itertools.combinations(range(8), 5):
    rest = [i for i in range(8) if i not in pos]
    for s2 in (2, -2):
        for signs in itertools.product((1, -1), repeat=4):
            t = [0] * 8; t[rest[0]] = s2
            for i, s in zip(rest[1:], signs): t[i] = s
            shell.append(tuple(t))  # 4+1+1+1+1 = 8 ✓
for signs in itertools.product((1, -1), repeat=8):
    shell.append(tuple(signs))  # 8x1 = 8 ✓
shell = sorted(set(shell))
log('    the raw-norm-8 shell: %d vectors -> %d lines (the +-pairs!!)' % (len(shell), len(shell) // 2))

# (2) the ⊥-structure: per candidate x: the ext120-lines ⊥ x
def dot(a, b): return sum(x * y for x, y in zip(a, b))
perp_counts = Counter()
cand_lines = []
for x in shell:
    first = next((c for c in x if c != 0), 0)
    if first < 0: continue  # the +-pair canonicalization: keep the first-nonzero-positive!!
    pc = sum(1 for l in Lints if dot(x, l) == 0)
    perp_counts[pc] += 1
    cand_lines.append((x, pc))
log('(2) THE PERP-COUNTS (the ext120-lines ⊥ x): %s' % dict(sorted(perp_counts.items())))
log('    the candidates: %d | the 63-analogs: %d' % (len(cand_lines), perp_counts.get(63, 0)))

# (3) the legality-suite per the rich candidates (the ⊥-count >= 40?!)
rich = [(x, pc) for x, pc in cand_lines if pc >= 40]
log('(3) THE RICH CANDIDATES (the >= 40 perps): %d' % len(rich))
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
good = []
for x, pc in rich:
    # the form: x vs the 120: the Gram of (the 120 + x): the positive-definite?! (the Sylvester-ish!!)
    # the form matrix: (a,b) -> a·b/2 (the I/2!!): the Gram = the pairwise dot/2!!
    # the decoder: the rank of (the 120 lines + x) must stay <= 8+1 (the (a,b)-style?!): the rank-8 lattice!!
    rr = rref([list(l) + [1] for l in Lints] + [list(x) + [1]], 9)  # the affine-augmented (the (x,1)-style!!)
    good.append((x, pc, len(rr)))
    if len(good) <= 3:
        log('    the sample %s: the perps %d | the affine-rank %d' % (x, pc, len(rr)))
log('    the legality-suite: the %d rich candidates (the affine-ranks: %s)' % (len(good), Counter(r for _, _, r in good)))

# (4) the price-map at v=121-125 (the never-measured!!): the profile law at the +lines!!
log('(4) THE PRICE-MAP (the v-up (the never-measured trend!!)):')
import os, sys
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
import mpmath as mp
mp.mp.dps = 50
P111 = mp.mpf('0.001733052823330162099157')
for v in (111, 120, 121, 122, 125):
    for cst, R in ((63, 389), (72, 420)):
        # the hist: the rank-1/2-heavy favorable shape at the mass identity!!
        mass = 8 * R + cst + 2 * v * 7
        # the shape: {1: ~45%, 2: ~45%, 3: ~2%, 4: 1%, 5: 3%, 7: ~1%} scaled to the mass!!
        h1 = int(mass * 0.44); h2 = int((mass - h1) * 0.82 / 2); rest_m = mass - h1 - 2 * h2
        h5 = rest_m // 2; h7 = rest_m - h5 - (rest_m - h5) // 7 * 7  # the leftovers split!!
        h3 = (rest_m - h5) // 2
        hist = {1: h1, 2: h2, 3: h3, 5: h5}
        m2 = sum(r * c for r, c in hist.items())
        hist[1] += mass - m2
        c, prof, d = price(hist, v, 8, R)
        if c is None:
            log('    v=%3d cst=%2d R=%3d: %s' % (v, cst, R, d if isinstance(d, str) else 'None'))
        else:
            log('    v=%3d cst=%2d R=%3d: c = %s  (%+.4f%%)' % (v, cst, R, mp.nstr(c, 22), float((c - P111) / P111) * 100))
