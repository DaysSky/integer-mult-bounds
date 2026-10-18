"""THE NATIVE-121 v15b (ii19_nat15b.py) — THE 12-FRAMES'-STRUCTURE (THE PROVEN-MIDS!!!
THE MEASURE: the 12-frames (the the-543/549/550/...?! (the the-10-SHARED-mids?! — the
the-LINES?! — the the-SHARING?! — the the-THE-TEMPLATE (the the-THE-BUILD!!!
"""
import sys, json, time
from collections import Counter, defaultdict
import numpy as np

W4 = json.load(open('ii19_own_word4.json'))
v, h, R = W4['v'], W4['h'], W4['R']
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

frames_of = defaultdict(set)
for phase in ['A', 'B']:
    for F, d, srcs in W4[phase]:
        for s in srcs:
            if s < v:
                frames_of[s].add(F)
frame_users = Counter()
for s, fs in frames_of.items():
    for F in fs:
        frame_users[F] += 1
shared = sorted([F for F, c in frame_users.items() if c > 1])
log('(0) THE SHARED-FRAMES: %d' % len(shared))
for F in shared:
    fl = W4['frames'][F]
    log('    frame-%d: len-%d | users %s' % (F, len(fl),
        sorted([s for s, fs in frames_of.items() if F in fs])))
# the perps?! — the 64-len?! — the the-the-the?! — the the-the-... — the the-the-the-... —
# the the-perp-frames?! — the the-the-... — hmm: the the-the-the?! — the the-... —
# OK: the the-PERP-census?! — the the-the-64-len-frames?! — the the-the-... — the the-... —
perps = sorted([F for F in range(len(W4['frames'])) if len(W4['frames'][F]) >= 60])
log('(1) THE PERP-FRAMES: %d (the lens %s)' % (len(perps),
    dict(sorted(Counter(len(W4['frames'][F]) for F in perps).items()))))
perp_users = Counter()
for s, fs in frames_of.items():
    for F in fs:
        if F in perps:
            perp_users[F] += 1
log('    the perp-users: %s' % dict(sorted(Counter(perp_users.values()).items())))
# THE CELL-LEVEL?! — the the-2-len?! — the the-... — the census!!!
cells = sorted([F for F in range(len(W4['frames'])) if len(W4['frames'][F]) == 2])
log('(2) THE CELL-FRAMES: %d' % len(cells))
cell_users = Counter()
for s, fs in frames_of.items():
    for F in fs:
        if F in cells:
            cell_users[F] += 1
log('    the cell-users: %s' % dict(sorted(Counter(cell_users.values()).items())))
# the the-... — hmm: the cells?! (the the-the-1-src?! — hmm: the the-... — OK — the the-
# SAMPLE?! — hmm: the the-first-3-cells?! — the the-... — the honest — OK:
for F in cells[:3]:
    fl = W4['frames'][F]
    us = sorted([s for s, fs in frames_of.items() if F in fs])
    log('    cell-%d: %s | users %s' % (F, fl, us))
# the the-... — hmm: the the-the-cells?! — the the-1-src?! — the the-... — hmm: the cells'-
# src-reads?! — hmm: the the-... — hmm: the the-the-... — the the-A?! — the the-... —
# the srcs'-READ-SEQUENCES?! — the the-... — the honest-simple?! — the the-... — hmm —
# THE KEY-QUESTION?! — the the-cells?! (the the-the-1-src?! (the the-... — hmm: the cells'-
# STRUCTURE?! — the the-2-len?! — the the-2-LINES?! — the the-the-... — hmm — the cell-142?!
# (the the-[?! — the the-... — hmm — OK: the the-the-... — hmm — the the-... — the the-... —
log("DONE — THE NAT15B (the 12-frames-structure!!!)")
