"""THE FRAME-CLASS CENSUS (ii19_nat41.py) — the word4's frames as the class-candidates.

THE CORE MACHINERY: per dim d, the CLASSES = the sets of targets sharing a dim-d frame
(the frame C= every member's perp!!). THE WORD4's OWN FRAMES (716, the Grams proven!!) are
the class-candidates: their ⊥-target-sets (the frames C= perp(t)!!) measured here.
THE ASSIGNMENT: the pieces'/singletons' user-sets must fit the classes (the users C= the
class's target-set!!); the target's chain: its classes' frames one-per-dim nested (the class
frames at the increasing dims!!); the gathers read the pieces at the class frames too!!
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
V, H = V, H
log = lambda *a: print(*a, file=sys.stderr, flush=True)

# the word4's frames + their ⊥-target-sets (the frames C= perp(t)!!)
fr_targets = defaultdict(set)     # F -> the targets whose perp contains F
for F in range(len(w['frames'])):
    d = dims[F]
    if d < 2 or d > 8: continue
    for t in range(V):
        # F C= perp(t): every frame-vector ⊥ the line t
        okk = True
        for vec in w['frames'][F]:
            if sum(vec[i] * w['lines'][t][j] * w['form']['num'][i][j]
                   for i in range(H) for j in range(H) if w['form']['num'][i][j]) != 0:
                okk = False; break
        if okk: fr_targets[F].add(t)
sizes = Counter()
for F, ts in fr_targets.items():
    if ts: sizes[(dims[F], len(ts))] += 1
log('the frame-classes (dim, the ⊥-target-set size): the counts')
for (d, n), c in sorted(sizes.items()):
    log('  dim %d | %d targets: %d frames' % (d, n, c))

# the class-candidates: per (dim, the target-set) — the frames with >= 2 targets
cand = defaultdict(list)           # (dim, frozenset(targets)) -> [F]
for F, ts in fr_targets.items():
    if len(ts) >= 2:
        cand[(dims[F], frozenset(ts))].append(F)
log('the distinct class-candidates: %d' % len(cand))
by_dim = Counter(d for (d, ts) in cand)
log('by dim: %s' % dict(sorted(by_dim.items())))

# THE ASSIGNMENT FEASIBILITY: the singleton-pieces' user-sets (the loads!!) vs the classes
A39 = json.load(open('ii19_nat39_assign.json'))
left2 = [set(l) for l in A39['left2']]
sing_users = defaultdict(set)
for t in range(V):
    for l in left2[t]:
        sing_users[l].add(t)
# per singleton-piece: can its user-set be COVERED by the classes (the user-sets ⊆ the classes'
# target-sets, the pieces read at the class frames (the value ⊆ the frame!!))?
def class_cover(us):
    """the greedy: cover the user-set by the classes (the frames ⊇ the value!!)."""
    rem = set(us)
    chosen = []
    for (d, ts), Fs in sorted(cand.items(), key=lambda kv: -len(kv[0][1] & rem or ())):
        pass  # (the real assignment in the emitter!!)
    return None

# the simpler census: per (dim, class-size): the coverage capacity for the singleton-loads
sload = Counter(len(u) for u in sing_users.values())
log('the singleton-loads: %s' % dict(sorted(sload.items())))
# the per-line check: the line's users ⊆ some class at some dim? (the value {l} ⊆ the frame:
# the frame ⊆ perp(t) C> l automatically (l C= perp(t)!!) — so ANY class with the users ⊆ ts!!)
ok_lines = 0; part_lines = 0
for l, us in sing_users.items():
    best = max((len(ts & set(us)) for (d, ts) in cand), default=0)
    if best >= len(us): ok_lines += 1
    elif best >= len(us) / 2: part_lines += 1
log('THE LINE-CLASS FIT: full %d | half+ %d | the lines total %d' % (
    ok_lines, part_lines, len(sing_users)))
json.dump({'fr_targets': {str(F): sorted(ts) for F, ts in fr_targets.items() if ts},
           'dims': {str(F): dims[F] for F in fr_targets if fr_targets[F]}},
          open('ii19_nat41_classes.json', 'w'))
log('saved ii19_nat41_classes.json')
