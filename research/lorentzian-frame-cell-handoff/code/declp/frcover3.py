"""Minimum total full-perp misalignment of a partition of the 220 I_{11,1} lines into orthogonal 4-frames.
Uses i11frames.npz (F = frames, w = number of targets outside the frame meeting it in an odd number of lines).
Good frames have w = 0 (20,790); every other frame has w >= 90, and a good frame contains an even number of P lines, so
any partition needs a non-good frame; the exact cover below minimises the total weight over frames of weight <= WMAX.
usage: frcover3.py WMAX TIME"""
import sys, collections, time
import numpy as np
from ortools.sat.python import cp_model
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
WMAX, TL = int(sys.argv[1]), float(sys.argv[2])
z = np.load(D + 'i11frames.npz'); F, w = z['F'], z['w']
sel = np.nonzero(w <= WMAX)[0]
print('frames with weight <= %d: %d' % (WMAX, len(sel)), flush=True)
m = cp_model.CpModel(); x = [m.NewBoolVar('') for _ in sel]
byline = collections.defaultdict(list)
for j, f in enumerate(sel):
    for a in F[f]: byline[int(a)].append(x[j])
for a in range(220): m.AddExactlyOne(byline[a])
m.Minimize(sum(int(w[f]) * x[j] for j, f in enumerate(sel)))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 3
sv.parameters.log_search_progress = False
t0 = time.time(); st = sv.Solve(m)
print('status', sv.StatusName(st), 'objective', sv.ObjectiveValue() if st in (2, 4) else None, 'bound', sv.BestObjectiveBound(), '%.0fs' % (time.time() - t0), flush=True)
if st in (2, 4):
    chosen = [tuple(int(a) for a in F[f]) for j, f in enumerate(sel) if sv.Value(x[j])]
    ws = collections.Counter(int(w[f]) for j, f in enumerate(sel) if sv.Value(x[j]))
    print('frames', len(chosen), 'weight histogram', dict(ws), flush=True)
    print('non-good frames:', [c for c, f in zip(chosen, [f for j, f in enumerate(sel) if sv.Value(x[j])]) if w[f] > 0], flush=True)
