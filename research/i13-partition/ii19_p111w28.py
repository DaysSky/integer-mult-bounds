"""THE V4-COMPATIBILITY COUNT (ii19_p111w28.py) — scratch: the final scope number.

A v4 build of helper h (pair s1, s2; cell F2 = span) at a dim-6 rung R needs, within the current
duty structure: R ⊇ F2 (content), and both srcs' dim-6 duty frames equal to R (their later duties
must be reachable from R — no sideways at dim 6).  Sources are singly-homed at dim 6 (w27), so
the condition is: dim6frame(s1) == dim6frame(s2) == a frame containing F2 (and h's later duties
nest above it).  Count those pairs; also count under the weaker relaxations.
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))

sys.argv = ['ii19_p111w21.py']
exec(open('ii19_p111w21.py').read().split('# (1) the T155 helpers')[0])
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
dim6 = {}
for r in range(nreg):
    six = sorted(set(f for f in chainF[r] if dims[f] == 6))
    dim6[r] = six[0] if len(six) == 1 else None

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

strict = sum(1 for h, b, s, F2, s1, s2 in pairs
             if s2 in dim6 and dim6[s2] is not None and dim6.get(s1) == dim6[s2] and sub(F2, dim6[s2]))
at6 = sum(1 for h, b, s, F2, s1, s2 in pairs if dim6.get(s1) == h6[h])
h_later = defaultdict(list)
for h in T155:
    h_later[h] = [f for f in chainF[h] if f not in chainDA[h]]
full = sum(1 for h, b, s, F2, s1, s2 in pairs
           if s1 in dim6 and dim6.get(s1) is not None and dim6.get(s1) == h6[h]
           and sub(F2, h6[h]) and all(sub(h6[h], f) for f in h_later[h] if dims[f] >= 6))
log('pairs %d' % len(pairs))
log('  dim6(s1) == dim6(s2) ⊇ F2 (the v4-buildable pairs, current duties): %d' % strict)
log('  dim6(s1) == h own rung: %d' % at6)
log('  full (s1 rung == h rung ⊇ F2, h later duties nest): %d' % full)
log('  h later-duty frame dims (sample): %s' % dict(sorted(Counter(tuple(sorted(dims[f] for f in h_later[h])) for h in T155).items())))
