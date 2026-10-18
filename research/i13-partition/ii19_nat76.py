"""THE SPAN DUMP (ii19_nat76.py) — the cell-251 vs the home-365 (the definitive!!)."""
import json, sys
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

w = json.load(open('ii19_ext120_pieces.json', 'rt'))
h = w['h']
CH = json.load(open('ii19_nat73_chains.json', 'rt'))
kept = CH['kept']
v = w['v']
pieces_base = 2 * v
log('the kept[9] (the reg %d!!): %s' % (pieces_base + 9, kept[9]))
i, a, b, c = kept[9]
P70 = json.load(open('ii19_nat70_pool.json', 'rt'))
ps = P70['pool'][i][0]
log('  the pool-piece %d: %s (the users %s!!)' % (i, ps, len(P70['pool'][i][1])))
log('  the roles: a %d b %d c %d' % (a, b, c))
c_home = {int(k): v2 for k, v2 in CH['c_home'].items()}
log('  the c_home[%d]: the span %s (the pieces %s!!)' % (
    c, c_home[c]['span'], c_home[c]['pieces']))
def rref(rows, n):
    m = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c2 in range(n):
        p = next((i2 for i2 in range(r, len(m)) if m[i2][c2] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c2]; m[r] = [x * iv for x in m[r]]
        for i2 in range(len(m)):
            if i2 != r and m[i2][c2] != 0:
                f = m[i2][c2]; m[i2] = [x - f * y for x, y in zip(m[i2], m[r])]
        r += 1
    return m[:r]
L = [[Fraction(x) for x in l] for l in w['lines']]
cellB = w['frames'][251]
homeB = w['frames'][365]
log('  the cell-251 basis: %s' % [[str(x) for x in row] for row in cellB])
log('  the home-365 basis: %s' % [[str(x) for x in row] for row in homeB])
# the check: the cell's rows in the home's span?!
for row in cellB:
    r = len(rref([list(x) for x in homeB] + [row], h))
    log('    the cell-row in the home-span: %s (the home dim %d!!)' % (r == len(homeB), len(homeB)))
# the roles' lines in the home's span?!
for s in (a, b, c):
    r = len(rref([list(x) for x in homeB] + [list(L[s])], h))
    log('    the line %d in the home-span: %s' % (s, r == len(homeB)))
