"""THE V4-GRAMMAR CONSOLIDATION CENSUS (ii19_p111w27.py) — the structural scope's last gate.

The v4-class reshape (each (1,2,4,6)-ladder helper built directly at its dim-6 frame: one rank-6
climb, its srcs climbing singleton->dim-6) has ceiling +6.28% over r434.  Geometric feasibility:
the cell/12-frame rungs vanish, so every duty of a source that currently sits BELOW dim 6 must
ride at a dim-6 frame CONTAINING it, and a source serving several dim-6 frames would face the
sideways wall.  Measures:
  (1) the helpers' dim-6 frames (the '6' rung): distinct count, helpers per frame;
  (2) per source: distinct dim-6 frames in its full chain (the sideways exposure);
  (3) per standard pair (s1, s2, F2): is s1's own cell inside the helper's dim-6 frame?
      (s2's cell = F2 is, by the flag);
  (4) per source: the duties below dim 6 (its cell reads) — could they all ride at ONE dim-6
      frame (a common 30-frame containing its cell and the helper frames)?
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from mpmath import mp

sys.argv = ['ii19_p111w21.py']
exec(open('ii19_p111w21.py').read().split('# (1) the T155 helpers')[0])
PH = ('D', 'A', 'B')

# full climb chains
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

# D+A chains for the T155 identification (w21 convention)
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
h6 = {}
for h in T155:
    b, s = touch[h][0], touch[h][1]
    Fb, db, sb = w['A'][b]; Fs, ds, ss = w['A'][s]
    if not (db == h and dims[Fb] == 1 and len(sb) == 1 and sb[0] < V and ds == h and dims[Fs] == 2 and len(ss) == 1):
        continue
    pairs.append((h, b, s, Fs, sb[0], ss[0]))
    h6[h] = next(f for f in chainDA[h] if dims[f] == 6)

f6 = Counter(h6.values())
log('(1) standard pairs %d | distinct dim-6 rungs %d | helpers-per-rung hist %s' % (
    len(pairs), len(f6), dict(sorted(Counter(f6.values()).items()))))

# (2) per source: distinct dim-6 frames in the FULL chain
multi6, per = 0, {}
for s in range(V):
    six = sorted(set(f for f in chainF[s] if dims[f] == 6))
    per[s] = six
log('(2) sources by #distinct dim-6 frames in chain: %s' % dict(sorted(Counter(len(v) for v in per.values()).items())))

# (3) per pair: s1's own cell inside the helper's dim-6 rung?  s2's (== F2) too?
ok1 = sum(1 for h, b, s, F2, s1, s2 in pairs
          if own_cell[s1] is not None and not isinstance(own_cell[s1], list) and sub(own_cell[s1], h6[h]))
ok2 = sum(1 for h, b, s, F2, s1, s2 in pairs if sub(F2, h6[h]))
log('(3) s1 own cell ⊆ h dim-6 rung: %d/%d | F2 ⊆ h dim-6 rung: %d/%d' % (ok1, len(pairs), ok2, len(pairs)))

# (4) per source: a single dim-6 frame containing its cell AND all its sub-6 duty frames?
duty = defaultdict(set)
for ph in PH + ('C',):
    for gi, (F, d, srcs) in enumerate(w[ph]):
        for r in srcs:
            if r < V and dims[F] < 6:
                duty[r].add(F)
cover = 0
for s in range(V):
    frames = set(duty[s])
    if own_cell[s] is not None and not isinstance(own_cell[s], list):
        frames.add(own_cell[s])
    if not frames: continue
    if any(all(sub(f, g) for f in frames) for g in per[s]):
        cover += 1
log('(4) sources whose sub-6 duties + cell fit ONE of their dim-6 frames: %d/%d (of %d with duties)' % (
    cover, V, sum(1 for s in range(V) if duty[s] or (own_cell[s] is not None and not isinstance(own_cell[s], list)))))

# (5) the pairs' joint view: for each pair, one dim-6 frame containing BOTH srcs' cells + duties?
joint = 0
for h, b, s, F2, s1, s2 in pairs:
    fr1 = set(duty[s1]) | ({own_cell[s1]} if own_cell[s1] is not None and not isinstance(own_cell[s1], list) else set())
    fr2 = set(duty[s2]) | ({own_cell[s2]} if own_cell[s2] is not None and not isinstance(own_cell[s2], list) else set())
    cand = [g for g in per.get(s1, []) if all(sub(f, g) for f in fr1)]
    cand += [g for g in per.get(s2, []) if all(sub(f, g) for f in fr2)]
    if any(g == h6[h] for g in cand): joint += 1
log('(5) pairs whose srcs could both ride at the helper\'s OWN dim-6 rung: %d/%d' % (joint, len(pairs)))
