"""THE ROLE-SOLVER (ii19_nat73.py) — the chains' global consistency!!

THE CONFLICTS (nat71!!): 64 orientation-conflicts (the b's ONE-cell rule!!) + 16 heavy
c-homes (the dim > 4!!). THE SOLVER: the per-piece role-assignments (the orientation
freedom (the pair's either-element as the cell!!) + the role-splits (the heavy c's
re-roled as the 1st (FREE!!))) with the GLOBAL consistency (the b's one cell + the c's
one dim-4 home!!). THE OUTPUT: the clean chain-spec (the pieces' 3-gate grammar!!).
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
lines = [tuple(int(x) for x in l) for l in SPEC['lines']]
V = len(lines)
PERP = [set(p) for p in SPEC['PERP']]
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
pool = [(sorted(p), sorted(u)) for p, u in P70['pool']]
log('the pieces: %d' % len(pool))

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
def span(lines_idx):
    return len(rref([list(lines[x]) for x in sorted(lines_idx)], 8))

# ============ THE SOLVER ============
# the roles per piece: (a, b, c): a = the 1st (the singleton-read (FREE!!)), b = the 2nd
# (the cell-read (ONE cell per b!!)), c = the 3rd (the home-read (ONE dim-4 home per c!!))
partner = {}                 # b -> a (the ONE cell!!)
c_home = {}                  # c -> the piece-set (the ONE home (the span <= 4!!))
kept = []
dropped = []
order = sorted(range(len(pool)), key=lambda i: -len(pool[i][1]))
for i in order:
    ps, users = pool[i]
    x, y, z = ps
    found = None
    # the orientations + the role-assignments: try all 6 permutations!!
    for a, b, c in itertools.permutations(ps):
        if b in partner and partner[b] != a:
            continue
        # the c's home: the span (the c's ALL pieces (the existing + this one!!)) <= 4!!
        newhome = {c} | set(ps)
        if c in c_home:
            newhome = c_home[c]['span'] | set(ps)
        if span(newhome) > 4:
            continue
        # the a: FREE (no constraints!!); the c: its home-span ✓!!
        found = (a, b, c, newhome)
        break
    if found is None:
        dropped.append(i)
        continue
    a, b, c, newhome = found
    partner[b] = a
    if c in c_home:
        c_home[c]['span'] = newhome
        c_home[c]['pieces'].append(i)
    else:
        c_home[c] = {'span': set(newhome), 'pieces': [i]}
    kept.append((i, a, b, c))
log('THE SOLVER: kept %d | dropped %d (-> the carriers!!)' % (len(kept), len(dropped)))
# the coverage after the drops!!
covered = [set() for _ in range(V)]
for i, a, b, c in kept:
    for t in pool[i][1]:
        covered[t] |= set(pool[i][0])
left = [PERP[t] - covered[t] for t in range(V)]
nleft = sum(1 for lo in left if lo)
loads = Counter()
for t in range(V):
    for l in left[t]: loads[l] += 1
log('    the leftovers: %d lines | the per-line loads %s' % (
    sum(len(lo) for lo in left), dict(sorted(Counter(loads.values()).items()))))
# the c-homes' spans!!
hd = Counter(span(v['span']) for v in c_home.values())
log('    the c-homes: %d | the span-dims %s' % (len(c_home), dict(sorted(hd.items()))))
# the homes' FRAMES (the dim-4 (the nondegenerate Grams!!)) — the honest: the span's basis
# extended to dim 4 (the ⊥-extensions (the {0,+-2}-class!!))!!
def gram_det(basis):
    n = len(basis)
    A = [[sum(basis[i][k] * basis[j][k] for k in range(8)) for j in range(n)] for i in range(n)]
    A = [[Fraction(x) for x in row] for row in A]
    det = Fraction(1)
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None: return Fraction(0)
        if p != c:
            A[c], A[p] = A[p], A[c]; det = -det
        det *= A[c][c]
        for i in range(c + 1, n):
            if A[i][c] != 0:
                f = A[i][c] / A[c][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    return det
ndeg = 0
for c, v in c_home.items():
    b = rref([list(lines[x]) for x in sorted(v['span'])], 8)
    if gram_det(b) == 0:
        ndeg += 1
log('    the homes Grams: the degenerate %d (the extension-fix at the emission!!)' % ndeg)
R = len(kept) + nleft + 9
log('THE ECONOMY: %d pieces + %d carriers + 9 = R %d' % (len(kept), nleft, R))
json.dump({'kept': [(i, a, b, c) for i, a, b, c in kept], 'dropped': dropped,
           'c_home': {str(k): {'span': sorted(v['span']), 'pieces': v['pieces']}
                      for k, v in c_home.items()},
           'partner': partner, 'left': [sorted(lo) for lo in left], 'R': R},
          open('ii19_nat73_chains.json', 'w'))
log('saved ii19_nat73_chains.json (the chain-spec!!)')
