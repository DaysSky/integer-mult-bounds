"""THE NATIVE-121 v3 (ii19_nat3.py) — THE PARTITION-PIECES + THE READ-ROOMS + THE HONEST HIST!!!
THE SYNTHESIS (the blocks 23+24+29 (the recorded arc's resolution!!!)):
1. THE PARTITION: the 120 roots -> the 30 DISJOINT 4-frames (the E8's D4-partition analog
   (the sources' ONE frame per dim -> THE CHAINS LEGAL BY CONSTRUCTION (the block-23!!!)))
2. THE PIECES: the inside-the-frames subsets (the cells: the ~2-4-line: the ~12-30 users
   (the block-24's greedy (TH_SAVE=4!!!)))
3. THE READ-ROOMS: the co-read groups' SHARED frames (the pieces' registers read at the
   ONE shared frame per (group, dim) — THE FREE SAME-FRAME RE-READS (the block-29!!!!!))
   + THE NESTING (the target's successive read-frames must NEST (the block-21!!!))
4. THE HONEST HIST (the chains' deltas!!!) + THE PRICER (THE VERDICT at the R ~ 219-250!!!)
"""
import sys, json, time
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

# ============ (1) THE PARTITION: the 30 disjoint 4-frames (the 120 roots!!) ============
# the greedy D4-partition: the 4-subsets whose span is dim-4 + pairwise iph != 0 (the D4s!!)
# the construction: the norm-4's D4-analog: the {2e_i, 2e_j, ...}-style?! — the GREEDY:
# pick the maximal cliques of pairwise-NON-orthogonal lines with the dim-4 spans!!
log('(1) THE PARTITION HUNT (the disjoint 4-frames (dim-4 spans!!)):')
# the candidate 4-frames: the spans' dim-4 + the 12+-line contents (the D4-rooms (the block-31!!!))
# the block-31's census: the 3,150 D4-rooms (the norm-4's analog!!) — the LIGHT version:
# the greedy disjoint cover: the seeds' D4-neighborhoods!!
used = set()
frames = []
for seed in range(120):
    if seed in used:
        continue
    # the seed's D4-frame: the lines u with iph(seed, u) != 0 (the non-orthogonal!!) forming the dim-4 span!!
    cand = [u for u in range(120) if u not in used and u != seed and iph(L[seed], L[u]) != 0]
    # the greedy: the 3 more lines: the pairwise non-orthogonal + the dim-4!!
    best = None
    import itertools
    for trio in itertools.combinations(cand, 3):
        lines4 = [seed] + list(trio)
        if any(iph(L[a], L[b]) == 0 for a, b in itertools.combinations(lines4, 2)):
            continue
        M = np.array([L[x] for x in lines4])
        if np.linalg.matrix_rank(M) == 4:
            best = lines4
            break
    if best is None:
        log('    !!! the partition FAILS at the seed %d (the leftover %s!!)' % (
            seed, [u for u in range(120) if u not in used][:6]))
        break
    frames.append(best)
    used.update(best)
log('    the frames: %d | the covered %d/120' % (len(frames), len(used)))

# ============ (2) THE PIECES (the block-24's greedy (TH_SAVE=4!!)) ============
# the piece-candidates: the INSIDE-the-frame subsets (the 2-4-line cells!!) with the >= TH_SAVE users!!
TH_SAVE = 4
pieces = []   # (the content-lines, the users!!)
for fi, fr in enumerate(frames):
    for size in (4, 3, 2):
        for sub in itertools.combinations(fr, size):
            # the users: the targets t with sub ⊆ perp(t) (every line of sub ⊥ t!!)
            users = [t for t in range(120) if all(iph(L[t], L[u]) == 0 for u in sub)]
            if len(users) >= TH_SAVE:
                pieces.append((sub, users))
# the greedy covering (the block-24's: the max-users-first + the coverage-tracking!!)
covered = [set() for _ in range(120)]   # per-target: the covered perp-lines!!
chosen = []
pc = sorted(pieces, key=lambda p: -len(p[1]))
for sub, users in pc:
    useful = [t for t in users if any(u not in covered[t] for u in sub)]
    if not useful:
        continue
    gain = sum(len([u for u in sub if u not in covered[t]]) for t in useful)
    if gain < TH_SAVE * len(sub):
        continue
    for t in useful:
        covered[t].update(sub)
    chosen.append((sub, useful))
log('(2) the pieces: %d chosen (the candidates %d!!) | the users-hist %s' % (
    len(chosen), len(pieces), dict(sorted(Counter(len(u) for _, u in chosen).items()))))
tails = [len(perp_t := [u for u in range(120) if u != t and iph(L[t], L[u]) == 0]) - len([u for u in perp_t if u in covered[t]]) for t in range(120)]
log('    the coverage: the tails %s (the mean %.1f!!)' % (
    dict(sorted(Counter(tails).items())), float(np.mean(tails))))
special_cov = sum(1 for t in range(120) if 120 in covered[t])
log('    THE SPECIAL-covered: %d/120 root-targets!!' % special_cov)

# ============ (3) THE R + THE PRICE (the coarse + the honest-hist!!) ============
R = len(chosen) + 9   # the pieces + the gathers (the leftover-inline (the free singleton-reads (NO tail-registers (the ~2-line leftovers!!!))))
log('(3) THE R: %d (the pieces %d + the gathers 9!!)' % (R, len(chosen)))
# THE HIST (the honest-model!!):
# the sources: [1 (the free singletons!!), the cell-climb (the +1 (the dim-2?! — the pieces' cells?!))]: hmm —
# THE PARTITION-PIECES' ECONOMY (the block-24's hist: the pieces' chains [0, 4 (the frame!!), the read-dims, 9]!!)
# THE MODEL: the pieces: [0 -> the frame (dim 4!!) -> the FULL (9!!)]: {4: n, 5: n}
# the sources: the [1, 1, 2]-style?! — the partition: the sources' ONE 4-frame: [1 (free), the +3 (1->4!!)]
# the targets: [0 -> the read-frames (the dim 4!!) -> the perp (8!!)]: {4, 4}: the coarse!!
for name, tgt_hist in (('coarse', {4: 1, 4: 1}), ('fewbig', {8: 1})):
    hist = Counter()
    hist[3] += 121          # the sources: 1 -> 4 (the partition-frames!!): the +3
    hist[5] += 121          # the sources: 4 -> 9 (the FULL!!): the +5
    hist[4] += len(chosen)  # the pieces: 0 -> 4
    hist[5] += len(chosen)  # the pieces: 4 -> 9
    hist[9] += 9            # the gathers: 0 -> 9
    for k in tgt_hist:
        hist[k] += 121      # the targets: 0 -> the perp (8!!) or the laddered!!
    # the targets' finals: the mass 8 each: the model {8: 121} covers it!!
    if name == 'fewbig':
        pass
    mass = sum(k * v for k, v in hist.items())
    ident = 9 * R + 73 + 2 * V * 8
    # hmm: the targets' mass 8: the hist must include the targets' 8!!
    hist2 = Counter(hist)
    hist2[8] += 121 - sum(tgt_hist.values())
    mass2 = sum(k * v for k, v in hist2.items())
    c = pprice(dict(hist2), v=V, h=H, R=R)
    log('    %s: the hist %s | the mass %d vs %d (%s!!) | c = %s | %+.2f%%' % (
        name, dict(sorted(hist2.items())), mass2, ident,
        'MATCH' if mass2 == ident else 'MISMATCH',
        mp.nstr(c, 12) if not isinstance(c, tuple) else c[0].get('error', c) if isinstance(c[0], dict) else c,
        0 if isinstance(c, tuple) else float((c / FRONTIER - 1) * 100)))
log('DONE — THE NAT3!!')
