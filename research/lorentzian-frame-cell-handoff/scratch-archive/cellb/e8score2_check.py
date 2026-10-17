"""Validation of the refined per-cell screen logic (lcell/lscore2) on E8 R420 cells (free top): must be >= the
doubly-forced counting bound (150 extras) and <= R420's realised 180."""
import sys, json
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
V = e8.V
def perp(m):
    r = (1 << V) - 1
    for s in e8.bits(m): r &= e8.HYP[s]
    return r
pc_ = lambda m: bin(m).count('1')
cells = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
rs = []
for C in cells:
    s, a = e8.bits(C)
    os_ = 0; oa_ = 0
    for c in cells_of[s]:
        if c != C: os_ |= perp(c)
    for c in cells_of[a]:
        if c != C: oa_ |= perp(c)
    PC = perp(C); Fs = PC & ~os_; Fa = PC & ~oa_
    D = Fs & Fa; S = Fs & ~Fa; A = Fa & ~Fs
    nps = list(set(perp(e8.closure(C | (1 << x))[0]) for x in range(V) if not C >> x & 1))
    best = None
    for q1 in nps:
        for q2 in nps:
            u = min(pc_(D & ~q1) + pc_(S & ~(q1 | q2)) + pc_(A & ~q1), pc_(D & ~q1) + pc_(S & ~q1) + pc_(A & ~(q1 | q2)),
                    pc_(D & ~(q1 & q2)) + pc_(S & ~q1) + pc_(A & ~q2))
            if best is None or u < best: best = u
    rs.append(best)
free0 = sum(1 for r in rs if r == 0); pool = V; cnt = 0
for r in sorted(r for r in rs if r > 0):
    if pool >= r: pool -= r; cnt += 1
print('E8 R420 cells, refined free-top screen: r_C histogram', {k: rs.count(k) for k in set(rs)}, ' sum j >=', len(cells) - free0 - cnt)
