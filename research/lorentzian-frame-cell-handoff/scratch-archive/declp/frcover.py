"""Minimum-misalignment good-frame partitions, full-perp version (exact CP-SAT).
A frame = 4 mutually orthogonal lines.  Weight w(F) = #{targets t not in F : |F cap t-perp| odd}; with the partition
as the cell graph (disjoint K4), target t needs 1 + #{F != F_t : |F cap t-perp| odd} single-line reads.
Minimise sum w(F) over exact covers of the lines by frames.  E8 control on E8(M) (R420-type partitions have w = 0).
usage: frcover.py SYSTEM(I11|E8) TIME"""
import sys, itertools, collections, time
import numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
from ortools.sat.python import cp_model
G = g.G
sysname, TL = sys.argv[1], float(sys.argv[2])
L = list(range(V)) if sysname == 'I11' else [x for x in range(V) if 9 not in g.supp[x] and 10 not in g.supp[x]]
n = len(L); Ls = set(L)
P = np.array([[1 if (a != b and G[a, b] == 0) else 0 for b in L] for a in L], dtype=np.int64)
idx = {x: i for i, x in enumerate(L)}
nbr = [set(np.nonzero(P[i])[0]) for i in range(n)]
frames = []
for a in range(n):
    for b in nbr[a]:
        if b <= a: continue
        for c in nbr[a] & nbr[b]:
            if c <= b: continue
            for d in nbr[a] & nbr[b] & nbr[c]:
                if d <= c: continue
                frames.append((a, b, c, d))
F = np.array(frames)
cnt = P[:, F].sum(axis=2)                     # cnt[t, f] = |F cap t-perp|
inF = np.zeros((n, len(frames)), dtype=bool)
for j, f in enumerate(frames): inF[list(f), j] = True
w = ((cnt % 2 == 1) & ~inF).sum(axis=0)
print('%s: %d lines, %d frames; weight distribution (min, mean, max) %d %.1f %d; frames of weight 0: %d' % (
    sysname, n, len(frames), w.min(), w.mean(), w.max(), int((w == 0).sum())), flush=True)
m = cp_model.CpModel(); x = [m.NewBoolVar('') for _ in frames]
byline = collections.defaultdict(list)
for j, f in enumerate(frames):
    for a in f: byline[a].append(x[j])
for a in range(n): m.AddExactlyOne(byline[a])
m.Minimize(sum(int(w[j]) * x[j] for j in range(len(frames))))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
t0 = time.time(); st = sv.Solve(m)
print('%s exact cover: %s, total odd (target, frame) incidences %s, bound %s, per target %.2f (+1 own frame)  %.0fs' % (
    sysname, sv.StatusName(st), sv.ObjectiveValue(), sv.BestObjectiveBound(), sv.ObjectiveValue() / n, time.time() - t0), flush=True)
