"""THE TWO-PASS SOLVER (ii19_nat77.py) — the partner/home co-constraint!!

THE CURRENT FRONT (§614!!): the source's chain SINGLE -> cell -> home -> FULL must nest:
THE CELL's partner-line INSIDE the source's home-span!! THE TWO-PASS: (1) the homes (the
c-role choices (the spans!!)); (2) the partners (the b-roles: the partner a chosen FROM
the b's home-members (a ∈ the home-span!!!)). OUTPUT: the clean chain-spec v2!!
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
def in_span(basis_rows, vec):
    return len(rref([list(x) for x in basis_rows] + [list(vec)], 8)) == len(basis_rows)
def span_of(idx_set):
    return rref([list(lines[x]) for x in sorted(set(idx_set))], 8)

# ============ THE PASS-1: THE HOMES (the c-role choices (the spans!!)) ============
# per piece: the c-role: the third source; the home-span: {c} ∪ ALL its c-pieces' lines!!
# THE CHOICE-FREEDOM: WHICH of the 3 is the c (the other two: the a/b-pair!!)!!
# THE ORDER: the pool-order (the greedy's savings!!); the c's homes: the span <= 4!!
c_home = {}          # c -> {'span': set, 'pieces': []}
kept = []
dropped = []
order = sorted(range(len(pool)), key=lambda i: -len(pool[i][1]))
for i in order:
    ps, users = pool[i]
    x, y, z = ps
    # try each as the c (the home-candidates!!): the span with the existing + this piece!!
    found = None
    for c in (x, y, z):
        ab = [s for s in ps if s != c]
        if c in c_home:
            newsp = c_home[c]['span'] | set(ps)
        else:
            newsp = {c} | set(ps)
        if len(span_of(newsp)) > 4:
            continue
        found = (c, ab, newsp)
        break
    if found is None:
        dropped.append(i)
        continue
    c, ab, newsp = found
    if c in c_home:
        c_home[c]['span'] = newsp
        c_home[c]['pieces'].append(i)
    else:
        c_home[c] = {'span': set(newsp), 'pieces': [i]}
    kept.append((i, ab, c))
log('PASS-1 (the homes!!): kept %d | dropped %d' % (len(kept), len(dropped)))
hd = Counter(len(span_of(v['span'])) for v in c_home.values())
log('  the c-homes: %d | the span-dims %s' % (len(c_home), dict(sorted(hd.items()))))

# ============ THE PASS-2: THE PARTNERS (the b-roles from the home-members!!) ============
# per piece (i, [a', b'], c): the pair-orientation: WHICH of the two is the b (the
# cell-owner!!): the b's partner = the other (a!!); THE CONSTRAINT: the partner a's LINE
# INSIDE the b's home-span (the b's chain: SINGLE -> cell(a, b) -> home(b)!!!!!
# — WAIT: the source's OWN home: the b's home (its c-role-home?! — the b: ANOTHER piece's
# c?! — the b's home = ITS c_home (if it serves as a c elsewhere!!!) — THE SOURCE's chain:
# its cell (its b-role!) + its home (its c-role!!): the b's partner ∈ THE B's HOME-SPAN
# (its c-home!!!) — IF the b has NO c-role: its home = ... hmm — the b's chain: SINGLE ->
# cell -> (its OTHER duties!!) -> FULL: the cell (dim 2!!) then the next duty: ANY frame
# ⊇ the cell (the partner-line's span!!) — the constraint: the LATER frames ⊇ the cell!!
partner = {}
conflicts = 0
for i, ab, c in kept:
    a_cand, b_cand = ab
    # the orientation: the b's cell must nest into the b's LATER duties (its c-home!!)!
    # try both orientations: prefer the b WITH a c-home containing the partner!!!
    for a, b in ((a_cand, b_cand), (b_cand, a_cand)):
        if b in partner and partner[b] != a:
            continue
        if b in c_home:
            # the b's c-home must contain the partner-line (the cell ⊆ the home!!)
            if not in_span(span_of(c_home[b]['span']), lines[a]):
                continue
        partner[b] = a
        break
    else:
        conflicts += 1
log('PASS-2 (the partners!!): matched %d | the b-conflicts %d' % (len(partner), conflicts))

# the coverage after the drops!!
covered = [set() for _ in range(V)]
for i, ab, c in kept:
    for t in pool[i][1]:
        covered[t] |= set(pool[i][0])
left = [PERP[t] - covered[t] for t in range(V)]
nleft = sum(1 for lo in left if lo)
R = len(kept) + nleft + 9
log('THE ECONOMY: %d pieces + %d carriers + 9 = R %d' % (len(kept), nleft, R))
json.dump({'kept': [(i, ab, c) for i, ab, c in kept], 'dropped': dropped,
           'c_home': {str(k): {'span': sorted(v['span']), 'pieces': v['pieces']}
                      for k, v in c_home.items()},
           'partner': partner, 'left': [sorted(lo) for lo in left], 'R': R},
          open('ii19_nat77_chains.json', 'w'))
log('saved ii19_nat77_chains.json (the chain-spec v2!!)')
