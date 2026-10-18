"""THE NATIVE-121 EXTRACTION (ii19_nat1.py) — THE FRONTIER-WORD BUILD's STEP 1!!

THE GOAL (the user's BUILD THE FRONTIER WORD!!): the native 121-assembly at the R ~ 260-300
(the crossing!!) — NOT the R420-transplant (the 421-base!!).

THE EXTRACTION:
(1) the actual perp-structure (the lines' ⊥-sets — NOT the memory!!);
(2) THE INTERSECTION-LATTICE (the natural shared cells!!): the closure of the 121 perps
    under the intersection -> the distinct sets + sizes (the sharing structure!!);
(3) THE FRAME-LATTICE: the 716 frames' dims/line-sets + which lattice-cells fit which
    frames (S's lines ⊆ F's lines!!);
(4) THE FIRST R-ESTIMATES: the greedy coverings (the cells + the readers!!).
"""
import json, sys, time
from collections import Counter
W4 = json.load(open('ii19_own_word4.json', 'rt'))
V, H, R = W4['v'], W4['h'], W4['R']
lines = W4['lines']
frames = W4['frames']
SP = 120
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# (0) the form: the ip121 (the diag(1^8, 2)!!) — verify against the word4's Gram-legal lines!!
def ip121(a, b):
    return sum(a[i] * b[i] for i in range(8)) + 2 * a[8] * b[8]
log('(0) the lines: %d | the norms: %s' % (
    V, dict(sorted(Counter(ip121(l, l) for l in lines).items()))))

# (1) the perps (the actual!!)
PERP = [set() for _ in range(V)]
for t in range(V):
    for u in range(V):
        if u != t and ip121(lines[t], lines[u]) == 0:
            PERP[t].add(u)
log('(1) the perp sizes: %s (the special %d)' % (
    dict(sorted(Counter(len(p) for p in PERP).items())), len(PERP[SP])))
# the 9th-coordinates (the a-coefficients!!):
a9 = Counter(tuple(l[8:9]) for l in lines)
log('    the 9th-coordinates: %s' % {str(k): v for k, v in a9.items()})
# the perps' composition: the roots vs the special!!
comp = Counter()
for t in range(V):
    n_root = len([u for u in PERP[t] if u != SP])
    comp[(n_root, SP in PERP[t])] += 1
log('    the perps (the roots-count, the-special-in): %s' % {str(k): v for k, v in comp.items()})

# (2) THE INTERSECTION-LATTICE (the closure!!): the meet-semilattice of the perps!!
lat = {}                                  # frozenset -> the reader-set (the Ts that generate it!!)
def add(s, readers):
    key = frozenset(s)
    if key in lat:
        lat[key] |= readers
    else:
        lat[key] = set(readers)
frontier = [frozenset(PERP[t]) for t in range(V)]
for t in range(V):
    add(PERP[t], {t})
changed = True
iters = 0
while changed and iters < 12:
    iters += 1
    changed = False
    cur = list(lat.keys())
    for i in range(len(cur)):
        for j in range(i + 1, len(cur)):
            s = cur[i] & cur[j]
            if s and s not in lat:
                add(s, lat[cur[i]] | lat[cur[j]])
                changed = True
log('(2) THE INTERSECTION-LATTICE: %d distinct sets (the closure in %d passes!!)' % (len(lat), iters))
sizes = Counter(len(s) for s in lat)
log('    the sizes: %s' % dict(sorted(sizes.items())))
# the maximal shared cells (the biggest sets read by >= 2 targets!!):
shared = [(s, len(rd)) for s, rd in lat.items() if len(rd) >= 2]
shared.sort(key=lambda z: (-len(z[1]), -len(z[0])))
log('    the shared sets (>=2 generators): %d | the TOP (by readers): %s' % (
    len(shared), [(len(s), len(rd)) for s, rd in shared[:12]]))

# (3) THE FRAME-LATTICE: the dims + the line-sets!!
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM.get(len(fr), None) for fr in frames]
unk = [i for i, d in enumerate(dims) if d is None]
log('(3) THE FRAMES: %d | the unknown-len frames: %s' % (len(frames), unk[:20]))
for i in unk[:20]:
    log('    the frame %d: len %d' % (i, len(frames[i])))
dims = [LCDIM.get(len(fr), len(fr)) for fr in frames]
log('    the dim-census: %s' % dict(sorted(Counter(dims).items())))
# the frames' line-sets (the content-capacity!!): the frames as the line-index sets!!
# NOTE: the frames = the coordinate VECTOR lists (the rref-basis or the line-lists?!!)
#       -> the len-keys: {1: dim1, 2: dim2, 3: dim3, 12: dim4, 13: dim5, 30: dim6, 64: dim8, 120: dim8, 121: dim9}
#       the len-120/121 frames = the LINE-LISTS; the others = the BASES (the rref!!)!!
big = [i for i, fr in enumerate(frames) if len(fr) in (64, 120, 121)]
log('    the BIG frames (the line-lists!!): %d: %s' % (len(big), big[:20]))
# extract the line-sets of the big frames!!
def frame_lines(fi):
    fr = frames[fi]
    out = set()
    for vec in fr:
        for u in range(V):
            if all(abs(lines[u][k] - vec[k]) < 1e-12 for k in range(9)):
                out.add(u); break
    return out
FL = {}
for fi in big[:400]:
    FL[fi] = frame_lines(fi)
log('    the big-frames line-sets extracted: %d (the sizes %s)' % (
    len(FL), dict(sorted(Counter(len(s) for s in FL.values()).items()))))
# which perps fit which big-frames?!
fits = Counter()
for t in range(V):
    p = frozenset(PERP[t])
    for fi, s in FL.items():
        if p <= s:
            fits[t] += 1
            break
log('    the perps with a >=1 fitting big-frame: %d/121' % len(fits))
log('DONE — THE NATIVE EXTRACTION (STEP 1!!)')
