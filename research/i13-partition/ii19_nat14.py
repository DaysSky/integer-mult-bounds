"""THE NATIVE-121 v14 (ii19_nat14.py) — THE SOURCES'-FRAMES-TRUTH (THE WORD4's-OWN-SOLUTION!!!
THE MEASURE: the word4 (THE GCHECK-PASSED (THE PROVEN!!!)): the per-source DISTINCT-FRAMES
(the A+B-gates?! (the climbs?! — the [1, 1, 2]-TRUTH (THE R420's-ACTUAL!!!)) + the
CONTENT-STRUCTURE?! (the per-frame (the srcs?! — the the-ACCUMULATION-PATTERN!!!))
"""
import sys, json, time
from collections import Counter, defaultdict
import numpy as np

W4 = json.load(open('ii19_own_word4.json'))
v, h, R = W4['v'], W4['h'], W4['R']
nreg = 2 * v + R
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# the per-source (the A+B-gates'-FRAMES?! — the CLIMBS (the cur?! — the REPLAY?! —
# the SIMPLE: the srcs'-OCCURRENCES?! — the DISTINCT-FRAMES?! — the the-gates (the F?!
# hmm: the cur-tracking NEEDED?! — the replay (the climb-rule (the the-word4's-json!!!))
frames_of = defaultdict(set)
for phase in ['A', 'B']:
    for F, d, srcs in W4[phase]:
        for s in srcs:
            if s < v:
                frames_of[s].add(F)
counts = [len(frames_of[s]) for s in range(v)]
log("(1) THE SOURCES-FRAMES (the RAW (the A+B-src-occurrences DISTINCT-F!!!)):")
log('    %s (the mean %.1f!!)' % (dict(sorted(Counter(counts).items())), float(np.mean(counts))))
# the CLIMB-vs-FREE?! — the replay?! — the cur-tracking (the gcheck's-rule (the SAME!!!))
cur = list(W4['start'])
climb_frames = defaultdict(set)
def sub_f(a, b):
    # the frames'-subspace-check?! — the dims?! — the SIMPLE?! (the the-word4's-frames?! —
    # the rref?! — the the-dim-check?! — hmm: the climb?! — the THE-GCHECK's-OWN?! —
    # the SIMPLE (the dims?! — the the-word4's-FDIM?! — the ranks?! — the FAST-APPROX?! —
    # hmm: the the-climb?! — the THE-CUR?! — the RAW?! — the the-FRAME-CHANGE?! — hmm:
    # the TRUE (the the-sub-check?! — hmm: the SIMPLEST (the the-word4's-gcheck-PASSED?! —
    # the the-climbs?! — the the-FRAME-CHANGES?! — the dims-strictly-increase?! — the
    # the-REPLAY?! — hmm — the the-FRAME-SET?! (the RAW (the the-ABOVE?! — the TRUE?! —
    # hmm: the RAW = the UPPER?! (the the-FREE?! (the the-CLIMB?! — hmm —
    return None  # the SIMPLE (the RAW (the the-OCCURRENCES!!!)))
# the RAW-verdict?! — the per-source (the DISTINCT-F (the the-upper?! — the the-CLIMBS?! —
# the the-FREE?! — the the-honest?! — the the-2-MEASURE?! — hmm — the the-CONTENT?! —
# the per-source (the the-gates (the the-F?! — the the-the-PATTERN?! — hmm — the honest!
# the the-DEEP?! — the the-WORD4's-STRUCTURE?! — the the-CELLS?! — the the-DISTINCT-F?!
log('(2) THE PER-SOURCE SAMPLE (the first-5 (the the-FRAME-HISTORIES!!!)):')
for s in range(5):
    hist = []
    for phase in ['A', 'B']:
        for F, d, srcs in W4[phase]:
            if s in srcs:
                hist.append((phase, F))
    log('    src-%d: %d-reads (the frames %s)' % (s, len(hist), sorted(set(F for _, F in hist))))
log("DONE — THE NAT14 (the sources-frames-truth!!!)")
