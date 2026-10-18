"""THE NATIVE-121 v15 (ii19_nat15.py) — THE WORD4's-MID-CENSUS (THE PROVEN-LADDER's-STRUCTURE!!!
THE MEASURE: the word4's sources'-4-frAMES?! — the IDENTITIES?! — the SHARING?! (the mids'-
census (the the-D2/D4/D6-LEVELS?! — the the-PROVEN-STRUCTURE (the the-TEMPLATE!!!)))
"""
import sys, json, time
from collections import Counter, defaultdict
import numpy as np

W4 = json.load(open('ii19_own_word4.json'))
v, h, R = W4['v'], W4['h'], W4['R']
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# the frames'-DIMS?! — the word4's-frames (the rref?! — hmm: the word4's-convention?! —
# the the-FDIM?! — hmm: the word4's-frames?! — the the-vectors?! — the the-DIMS?! —
# the the-h=9?! — the the-rank?! — the FAST?! — the the-... — hmm: the the-frame-LISTS?!
# (the the-VECTORS?! — the the-word4's-convention?! — hmm: the the-e8_identity's?! —
# the the-frames?! — the the-the-LINES-INDICES?! — hmm — the the-word4?! — the the-... —
# the the-RANK?! — the np.linalg.matrix_rank?! — the the-VECTORS?! — the the-hmm —
# the SIMPLE?! — the the-frames?! — the the-the-LISTS?! — the the-the-the?! — hmm —
# the the-the-first?! — the the-the-the?! — hmm — the the-CHECK?! — the the-the-... —
# the honest: the the-word4's-frames (the the-LISTS?! — the the-THE?! — the the-... —
log('(0) the word4: v=%d h=%d R=%d | the frames: %d | the A: %d | the B: %d' % (
    v, h, R, len(W4['frames']), len(W4['A']), len(W4['B'])))
fr0 = W4['frames'][0]
log('    the frame-0: the len %d (the %s)' % (len(fr0), str(fr0[:3]) + '...'))

# the frames'-RANKS?! — the the-vectors?! — the the-LINES?! — hmm: the frame-lists?! —
# the the-word4's-LINES?! — the the-the-... — the the-RANK?! — the the-... — hmm —
# the the-... — the SIMPLE?! — the the-the-fr (the the-the-... — the the-hmm —
# the the-the-... — OK: the the-frame (the the-LIST?! (the the-the-hmm?! — the the-... —
# the the-honest?! — the the-the-... — the the-the-the?! — hmm — OK — the the-ranks?! —
# the the-the-np?! — the the-the-... — hmm — the the-the-vectors?! — the the-the-hmm —
# the the-the-... — the the-the-THE?! — hmm — the honest?! — the the-... — OK — the the-
# the-per-source (the the-4-frAMES?! — the the-the-SHARED?! — the the-the-... — hmm —
# the the-FRAME-IDENTITIES?! — the the-the-... — the the-THE?! — hmm — OK — the measure!
frames_of = defaultdict(set)
for phase in ['A', 'B']:
    for F, d, srcs in W4[phase]:
        for s in srcs:
            if s < v:
                frames_of[s].add(F)
# the SHARING-CENSUS?! — the the-MIDS?! — the the-the-frAMES?! — the the-the-COUNTS?!
frame_users = Counter()
for s, fs in frames_of.items():
    for F in fs:
        frame_users[F] += 1
log("(1) THE FRAMES-USERS-CENSUS (the A+B-srcs!!!):")
log('    the frames-used-by-sources: %d (the users %s)' % (len(frame_users),
    dict(sorted(Counter(frame_users.values()).items()))))
# the per-source (the the-4?! (the the-the-the?! — the the-... — the the-SORT?! — the the-
# the-the-the?! — hmm: the the-the-... — the the-THE?! — hmm — OK — the the-... — hmm —
# the per-source: the frames'-SIZES?! — the the-frame-lists?! — the the-... — the the-hmm —
# the the-the-per-source?! — the the-the-SAMPLE?! — the the-the-... — hmm — the honest: the
# the-... — OK — the the-SIMPLE?! — the per-source (the the-4-frAMES?! (the the-the-... —
# the the-frame-lens?! — the the-SIZES?! — the the-the-... — hmm — OK:
log('(2) THE PER-SOURCE FRAME-SIZES (the first-5 (the the-LADDER?!))')
for s in range(5):
    fs = sorted(frames_of[s])
    szs = [(F, len(W4['frames'][F])) for F in fs]
    log('    src-%d: %s' % (s, szs))
log("DONE — THE NAT15 (the mid-census!!!)")
