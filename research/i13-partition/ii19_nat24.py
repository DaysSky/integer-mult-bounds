"""THE WORD4 LADDER-MERGE ANATOMY (ii19_nat24.py) — why are the 137 (1,2,4,6)-helpers' build->2nd
merges blocked?  The r434 wall: s1's own cell != F2 (its own cell is another helper's F2, and the
cells are single-helper).  The word4's cells serve 3 helpers each (420 helpers at 180 cells) and
120 sources sit at 120 of them.  Measure: the 137 pairs' (s1, s2, F2), s1's own cell vs F2, and
s1's line inside F2 (the pair-span hypothesis).
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))

sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
PH = ('D', 'A', 'B')

chainF = defaultdict(list)
cur = list(w['start'])
for ph in PH + ('C',):
    for F, d, srcs in w[ph]:
        for r in [d] + srcs:
            if cur[r] != F and dims[F] >= dims[cur[r]]:
                cur[r] = F; chainF[r].append(F)
for r in range(nreg):
    if cur[r] != w['final'][r] and dims[w['final'][r]] >= dims[cur[r]]:
        chainF[r].append(w['final'][r])
own_cell = {}
for r in range(nreg):
    cells = [f for f in chainF[r] if dims[f] == 2]
    own_cell[r] = cells[0] if len(cells) == 1 else (None if not cells else cells)

chainDA = defaultdict(list)
cur = list(w['start'])
for F, d, srcs in w['D'] + w['A']:
    for r in [d] + srcs:
        if cur[r] != F and dims[F] >= dims[cur[r]]:
            cur[r] = F; chainDA[r].append(F)
T = sorted(h for h in range(2 * V, nreg) if tuple(dims[f] for f in chainDA[h]) == (1, 2, 4, 6))
touch = defaultdict(list)
for gi, (F, d, srcs) in enumerate(w['A']):
    for r in [d] + srcs: touch[r].append(gi)
pairs = []
for h in T:
    b, s = touch[h][0], touch[h][1]
    Fb, db, sb = w['A'][b]; Fs, ds, ss = w['A'][s]
    if db == h and dims[Fb] == 1 and len(sb) == 1 and sb[0] < V and ds == h and dims[Fs] == 2 and len(ss) == 1:
        pairs.append((h, b, s, Fs, sb[0], ss[0]))
log('T(1,2,4,6) %d | standard build->2nd pairs %d | 2nd-src: source %d / helper %d' % (
    len(T), len(pairs), sum(1 for p in pairs if p[5] < V), sum(1 for p in pairs if p[5] >= V)))
same = sum(1 for h, b, s, F2, s1, s2 in pairs if own_cell[s1] is not None and not isinstance(own_cell[s1], list) and own_cell[s1] == F2)
inF2 = sum(1 for h, b, s, F2, s1, s2 in pairs if cont(F2, s1))
ok2 = sum(1 for h, b, s, F2, s1, s2 in pairs if own_cell[s2] == F2)
log('  s1 own cell == F2: %d/%d | s1 line inside F2: %d/%d | s2 own cell == F2: %d' % (
    same, len(pairs), inF2, len(pairs), ok2))
f2c = Counter(F2 for h, b, s, F2, s1, s2 in pairs)
log('  distinct F2s: %d | pairs-per-F2 hist: %s' % (len(f2c), dict(sorted(Counter(f2c.values()).items()))))
cellhelp = Counter(own_cell[x] for x in range(2 * V, nreg) if own_cell[x] is not None and not isinstance(own_cell[x], list))
log('  helper own-cells: %d distinct | helpers-per-cell hist: %s' % (len(cellhelp), dict(sorted(Counter(cellhelp.values()).items()))))
# s1's own cell vs F2 as frames: both dim 2 — nested only if equal; count equal-subspace (different index)?
eqsub = sum(1 for h, b, s, F2, s1, s2 in pairs
            if own_cell[s1] is not None and not isinstance(own_cell[s1], list)
            and own_cell[s1] != F2 and sub(own_cell[s1], F2) )
log('  C1 ⊆ F2 (equal subspaces, distinct indices): %d' % eqsub)
