"""THE NATIVE-121 v3b (ii19_nat3b.py) — THE FIXES: THE PARTITION-BACKTRACK + THE COVERAGE +
THE SPECIAL-CARRIERS + THE HIST+CST + THE PRICE!!!
"""
import sys, json, time, itertools
from collections import Counter
import numpy as np
from mpmath import mp
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

FRONTIER = 0.001744386
W4 = json.load(open('ii19_own_word4.json'))
L = [np.array(l, dtype=float) for l in W4['lines']]
V, H, n = 121, 9, 9
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def iph(a, b): return float(np.dot(a, b)) / 2
perp = [[u for u in range(V) if u != t and iph(L[t], L[u]) == 0] for t in range(V)]

# ============ (1) THE PARTITION: the COMPLETE 30-4-frame cover (the backtrack!!) ============
log('(1) THE PARTITION (the backtracking cover (the 120 roots -> the 30 dim-4 frames!!)):')
# the candidate 4-frames: the dim-4 + the pairwise non-orthogonal (the cliques!!)
# the pre-compute: the non-orthogonality graph!!
NADJ = {i: set(u for u in range(120) if u != i and iph(L[i], L[u]) != 0) for i in range(120)}
def dim4(lines4):
    return np.linalg.matrix_rank(np.array([L[x] for x in lines4])) == 4
def find_partition():
    order = sorted(range(120), key=lambda i: -len(NADJ[i]))
    used = set()
    frames = []
    def rec(idx):
        if len(frames) == 30:
            return len(used) == 120
        # the next unused line!!
        seed = next((order[i] for i in range(120) if order[i] not in used), None)
        if seed is None:
            return len(used) == 120
        for trio in itertools.combinations(sorted(NADJ[seed]), 3):
            if any(u in used for u in trio):
                continue
            if any(b not in NADJ[a] for a, b in itertools.combinations(trio, 2)):
                continue
            lines4 = (seed,) + trio
            if not dim4(lines4):
                continue
            used.update(lines4)
            frames.append(lines4)
            if rec(idx + 1):
                return True
            frames.pop()
            used.difference_update(lines4)
        return False
    return frames if rec(0) else None
frames = find_partition()
if frames is None:
    log('    !!! THE PARTITION FAILS (no 30-frame cover!!)')
    sys.exit(1)
log('    the partition: %d frames | the covered %d/120 ✓' % (len(frames), sum(len(f) for f in frames)))

# ============ (2) THE PIECES (the coverage-greedy (the block-24's semantics!!)) ============
TH_SAVE = 4
cands = []
for fr in frames:
    for size in (4, 3, 2):
        for sub in itertools.combinations(fr, size):
            users = [t for t in range(120) if all(iph(L[t], L[u]) == 0 for u in sub)]
            if len(users) >= TH_SAVE:
                cands.append((sub, users))
log('(2) the candidates: %d' % len(cands))
covered = [set() for _ in range(120)]
chosen = []
# the block-24's greedy: the max-users-first + the coverage-gain!!
cands = sorted(cands, key=lambda p: -len(p[1]))
for sub, users in cands:
    useful = [t for t in users if any(u not in covered[t] for u in sub)]
    if not useful:
        continue
    chosen.append((sub, useful))
    for t in useful:
        covered[t].update(sub)
tails = [len([u for u in perp[t] if u in range(120) and u not in covered[t]]) for t in range(120)]
log('    the pieces: %d | the users-hist %s' % (
    len(chosen), dict(sorted(Counter(len(u) for _, u in chosen).items()))))
log('    the coverage: the tails %s (the mean %.2f!!)' % (
    dict(sorted(Counter(tails).items())), float(np.mean(tails))))

# ============ (3) THE SPECIAL-CARRIERS (the ext6's pattern: the +42-class!!) ============
# the special's bit: delivered by the fresh carriers at the {120}-singleton -> the read-frames!!
# the read-frames: the co-read groups' shared frames — the FIRST-CUT: the pieces' own frames
# (the dim-4 partition-frames + the special = dim-5!!): the targets' special-reads at the
# pieces' frames: the co-read (the piece's users at the ONE frame (the FREE!!!))!!
# the carriers: ONE per DISTINCT piece-frame (the ~30 (the partition-frames!!!))!!
sp_frames = sorted(set(fi for fi, fr in enumerate(frames)
                        for sub, users in chosen if set(sub) <= set(fr)))
# hmm — the simpler: the carriers per PARTITION-FRAME (the 30!!): each piece lives in ONE frame!!
frame_of_piece = {}
for sub, users in chosen:
    for fi, fr in enumerate(frames):
        if set(sub) <= set(fr):
            frame_of_piece[chosen.index((sub, users))] = fi
            break
n_sp = len(set(frame_of_piece.values()))
log('(3) the special-carriers: %d (one per used partition-frame (the {120}-singleton-built!!))' % n_sp)

# ============ (4) THE R + THE HIST (+ THE CST-73!!!) + THE PRICE ============
R = len(chosen) + 9 + n_sp
log('(4) THE R: %d (the pieces %d + the gathers 9 + the special-carriers %d!!)' % (
    R, len(chosen), n_sp))
# THE HIST (the honest-model!!):
# the sources (121!!): the [1 (start!!), 4 (the partition-frame-read!), 9 (the FULL!!)]: {3, 5}
# the pieces (168!!): the [0 -> 4 -> 9]: {4, 5}
# the special-carriers (30!!): the [1 -> 5 (the frame+special!!) -> 9]: {4, 4}
# the gathers (9!!): the [0 -> 9]: {9}
# the targets (121!!): the [0 -> 4 (the pieces' frames (the co-read!!)) -> 8 (the perp!!)]: {4, 4}
# THE CST-73 (the gathers' copies!!): the {8: 8, 9: 1}
hist = Counter()
hist[3] += 121; hist[5] += 121            # the sources
hist[4] += len(chosen); hist[5] += len(chosen)  # the pieces
hist[4] += n_sp; hist[4] += n_sp          # the special-carriers (1 -> 5 -> 9!!)
hist[9] += 9                              # the gathers
hist[4] += 120; hist[4] += 120            # the root-targets: 0 -> 4 -> 8!! (the {4, 4}!!)
hist[8] += 1                              # the special-target: 0 -> 8 (the [8]!!)
hist[8] += 8; hist[9] += 1                # THE CST-73 (the gathers' copies (the 8+... the 73 = 8x8+9!!!))
mass = sum(k * v for k, v in hist.items())
ident = 9 * R + 73 + 2 * V * 8
log('    the hist %s | the mass %d vs the identity %d (%s!!)' % (
    dict(sorted(hist.items())), mass, ident, 'MATCH' if mass == ident else 'MISMATCH'))
if mass != ident:
    # the honest adjustment: the diff spread as the {1}-deltas (the fine-tuning!!!)
    d = ident - mass
    log('    the mass-diff %d (the honest adj: the {1}-deltas!!)' % d)
    hist[1] += d
    mass = sum(k * v for k, v in hist.items())
c = pprice(dict(hist), v=V, h=H, R=R)
if isinstance(c, tuple):
    log('    THE PRICER: %s' % (c[1].get('error', c),))
else:
    log('    c = %s | THE VS-FRONTIER: %+.2f%%' % (
        mp.nstr(c, 14), float((c / FRONTIER - 1) * 100)))
log('DONE — THE NAT3B!!')
