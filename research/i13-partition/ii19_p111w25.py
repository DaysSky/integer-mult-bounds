"""THE LADDER CENSUS (ii19_p111w25.py, v2) — the structural route's SCOPE measurement (scratch).

Facts to measure (after w21/w23/w24: the v2 build->2nd merge is illegal because each build-src's
OWN dim-2 cell C1 != F2, and raising the build forces s1 sideways C1 -> F2):
  (1) every source's own dim-2 cell (full chain) + the single-source group fact;
  (2) the T155 standard pairs (s1, s2, F2) with w21's D+A chain convention;
  (3) for each pair: is s1's LINE inside the F2 subspace (the span(s1,s2) hypothesis)?  Which
      gates need s1 at C1 (the duties that pin it), and could those duties ride at F2?
  (4) the payoff ceiling: the exact price of the hypothetical v2-reshape hist.
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

argv = sys.argv[1:]
sys.argv = ['ii19_p111w21.py']
exec(open('ii19_p111w21.py').read().split('# (1) the T155 helpers')[0])
P111 = mp.mpf('0.001733052823330162099157')
R = w['R']
def pc(hist): return price(dict(hist), V, H, R)[0]
PH = ('D', 'A', 'B')

# (1) full climb chain (D/A/B/C/final) -> every source's own dim-2 cell
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
cell_srcs = defaultdict(list)
for s in range(V):
    if own_cell[s] is not None and not isinstance(own_cell[s], list):
        cell_srcs[own_cell[s]].append(s)
log('(1) unique-own-cell sources %d/%d | multi %d | none %d | distinct cells %d | group sizes %s' % (
    sum(1 for s in range(V) if not isinstance(own_cell[s], list) and own_cell[s] is not None), V,
    sum(1 for s in range(V) if isinstance(own_cell[s], list)), sum(1 for s in range(V) if own_cell[s] is None),
    len(cell_srcs), dict(sorted(Counter(len(v) for v in cell_srcs.values()).items()))))

# (2) the T155 standard pairs (w21's convention: chain over D+A)
chainDA = defaultdict(list)
cur = list(w['start'])
for F, d, srcs in w['D'] + w['A']:
    for r in [d] + srcs:
        if cur[r] != F and dims[F] >= dims[cur[r]]:
            cur[r] = F; chainDA[r].append(F)
T155 = sorted(h for h in range(2 * V, nreg) if tuple(dims[f] for f in chainDA[h]) == (1, 2, 4, 6))
touch = defaultdict(list)
for gi, (F, d, srcs) in enumerate(w['A']):
    for r in [d] + srcs: touch[r].append(gi)
pairs = []
for h in T155:
    b, s = touch[h][0], touch[h][1]
    Fb, db, sb = w['A'][b]; Fs, ds, ss = w['A'][s]
    if db == h and dims[Fb] == 1 and len(sb) == 1 and sb[0] < V and ds == h and dims[Fs] == 2 and len(ss) == 1:
        pairs.append((h, b, s, Fs, sb[0], ss[0]))
log('(2) T155 %d | standard pairs %d | 2nd-src: source %d / helper %d' % (len(T155), len(pairs),
    sum(1 for h, b, s, F2, s1, s2 in pairs if s2 < V), sum(1 for h, b, s, F2, s1, s2 in pairs if s2 >= V)))
ok2 = sum(1 for h, b, s, F2, s1, s2 in pairs if own_cell[s2] == F2)
ok1 = sum(1 for h, b, s, F2, s1, s2 in pairs if own_cell[s1] == F2)
log('    s2 own cell == F2: %d/%d | s1 own cell == F2: %d' % (ok2, len(pairs), ok1))

# (3) the pair anatomy: s1's line in the F2 subspace?  s1's C1-duties?
inF2 = sum(1 for h, b, s, F2, s1, s2 in pairs if cont(F2, s1))
log('(3) s1 line inside F2 subspace: %d/%d | source-s2 line inside: %d/%d' % (
    inF2, len(pairs), sum(1 for h, b, s, F2, s1, s2 in pairs if s2 < V and cont(F2, s2)),
    sum(1 for h, b, s, F2, s1, s2 in pairs if s2 < V)))
duty = defaultdict(list)          # src -> [(phase, pos, frame)] gates reading it at its own cell
for ph in PH + ('C',):
    for gi, (F, d, srcs) in enumerate(w[ph]):
        for r in srcs:
            if r < V and own_cell[r] is not None and not isinstance(own_cell[r], list) and F == own_cell[r]:
                duty[r].append((ph, gi, F))
s1s = set(s1 for h, b, s, F2, s1, s2 in pairs)
duty_counts = Counter(len(duty[s]) for s in s1s if s in duty)
log('    s1-srcs with C1-duties: %d/%d | duty-count hist %s' % (
    sum(1 for s in s1s if s in duty), len(s1s), dict(sorted(duty_counts.items()))))
# could the C1-duties ride at F2?  need F2 == C1 (same dim) or the duty gates' frames ⊇ F2 with all operands climbable
sameCF = sum(1 for h, b, s, F2, s1, s2 in pairs if own_cell[s1] is not None and not isinstance(own_cell[s1], list) and own_cell[s1] == F2)
log('    s1 own cell == F2 (identical frame): %d (the shared-cell geometry)' % sameCF)
# how many distinct F2s and how many pairs share an F2 (multi-helper cells)?
f2c = Counter(F2 for h, b, s, F2, s1, s2 in pairs)
log('    distinct F2 cells: %d | pairs-per-F2 hist %s' % (len(f2c), dict(sorted(Counter(f2c.values()).items()))))
# per-pair: s1's own cell C1 vs F2 nested?  (equal is the only same-dim nesting)
nested = sum(1 for h, b, s, F2, s1, s2 in pairs
             if own_cell[s1] is not None and not isinstance(own_cell[s1], list) and sub(own_cell[s1], F2))
log('    C1 ⊆ F2 (nested): %d' % nested)

# (4) the payoff ceiling
if pairs:
    h2 = Counter(hist0)
    h2[1] -= 2 * len(pairs); h2[2] += len(pairs)
    c_hyp, c0 = pc(h2), pc(hist0)
    log('(4) hypothetical v2-reshape: hist %s | mass %d (base %d)' % (
        dict(sorted(h2.items())), sum(k * c for k, c in h2.items()), sum(k * c for k, c in hist0.items())))
    log('    ceiling: %s (%+.5f%% vs the r434 base, %+.5f%% vs P111)' % (mp.nstr(c_hyp, 22),
        float((c_hyp / c0 - 1) * 100), float((c_hyp / P111 - 1) * 100)))
