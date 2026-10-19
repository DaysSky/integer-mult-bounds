"""nat163: THE RECOMPOSED WORD'S BUILD FEASIBILITY (the 242-family over the W4's pieces).

The build: the new wires' contents (the nat155 shared-family) built via the W4's
piece-family (the intermediates!) at legal build-frames - the decomposition feasibility.
Gate: each new content = the XOR of pieces available at a common build-frame.
"""
import json
from collections import Counter, defaultdict

W4 = json.load(open('ii19_own_word4.json'))
v = W4['v']
nreg = 2*v + W4['R']
X = (1 << v) - 1

# the W4's frame dims (the line-lists!)
frames = W4['frames']
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(fr)] for fr in frames]
fmask = []
for fr in frames:
    m = 0
    for x in fr:
        pass  # the lines are VECTORS not indices - need the index mapping!
# the W4's frames: lists of LINE-VECTORS: map to indices via the lines list
lines = [tuple(int(c) for c in l) for l in W4['lines']]
lidx = {l: i for i, l in enumerate(lines)}
fmask = []
for fr in frames:
    m = 0
    ok = True
    for x in fr:
        t = tuple(int(c) for c in x)
        if t in lidx:
            m |= 1 << lidx[t]
        elif tuple(-c for c in x) in lidx:
            m |= 1 << lidx[tuple(-c for c in x)]
        else:
            ok = False
    fmask.append(m if ok else -1)
print('the frames: %d | the unmapped: %d' % (len(frames), sum(1 for m in fmask if m == -1)), flush=True)

# the replay: the registers' x-contents at the A-END + the piece-structure
val = [0]*nreg
for s in range(v): val[s] = 1 << s
for F, d, ss in W4['D']:
    for s in ss: val[d] ^= val[s]
for F, d, ss in W4['A']:
    for s in ss: val[d] ^= val[s]
xpart = [val[r] & X for r in range(nreg)]

# the pieces: the intermediates (the A-dests read later) + the wires: the content census
tgt_dests = set(range(v, 2*v))
read_by = defaultdict(set)
for F, d, ss in W4['A']:
    for s in ss:
        read_by[s].add(d)
for F, d, ss in W4['B']:
    for s in ss:
        read_by[s].add(d)
pieces = [r for r in range(2*v, nreg) if r not in set(W4['ret'])]
print('the candidate pieces (the helpers): %d' % len(pieces), flush=True)

# the per-frame piece-pools: the pieces whose content ⊆ the frame
frame_pool = defaultdict(list)
for r in pieces:
    xm = xpart[r]
    if not xm:
        continue
    for fi, m in enumerate(fmask):
        if m >= 0 and (xm & ~m) == 0:
            frame_pool[fi].append(r)
print('the per-frame piece-pools:', dict(sorted(Counter(len(p) for p in frame_pool.values()).items())), flush=True)

# the 242-family
SF = json.load(open('ii19_nat155_shared121.json'))
masks = {int(k, 16): sorted(vals) for k, vals in SF['masks'].items()}
print('the shared-family: %d masks' % len(masks), flush=True)

# THE DECOMPOSITION FEASIBILITY: for each new content: the build-frame candidates
# (the frames ⊇ the content), then the XOR-solve over the frame's piece-pool.
def rref_solve(tm, cands):
    rows, piv = [], {}
    for cm in cands:
        cur, combo = cm, [cm]
        while cur:
            p = cur & -cur
            if p in piv:
                _, bm, bc = rows[piv[p]]
                cur ^= bm
                combo = combo + bc
            else:
                break
        if cur:
            p = cur & -cur
            piv[p] = len(rows)
            rows.append((p, cur, combo))
    cur, combo = tm, []
    while cur:
        p = cur & -cur
        if p not in piv:
            return None
        _, bm, bc = rows[piv[p]]
        cur ^= bm
        combo = combo + bc
    cnt = Counter(combo)
    return [c for c, nn in cnt.items() if nn % 2]

ok, fail, sizes = 0, 0, Counter()
for cm, users in masks.items():
    # the build-frame: the dim-6/8 frames containing the content
    bf = [fi for fi, m in enumerate(fmask) if m >= 0 and (cm & ~m) == 0 and dims[fi] >= 6]
    done = False
    for fi in bf:
        pool = frame_pool.get(fi, [])
        # the piece-masks as the XOR-targets: solve cm = XOR of the pieces' x-parts
        sol = rref_solve(cm, [xpart[r] for r in pool])
        if sol is not None:
            ok += 1
            sizes[len(sol)] += 1
            done = True
            break
    if not done:
        fail += 1
        if fail <= 5:
            print('  FAIL: the content %d lines, the frames tried %d' % (bin(cm).count('1'), len(bf)), flush=True)
print('THE DECOMPOSITION: %d ok, %d FAIL' % (ok, fail))
print('the XOR-sizes (the pieces per build):', dict(sorted(sizes.items())))
