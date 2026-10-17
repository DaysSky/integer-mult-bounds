"""I_{13,1}: all rank-3 frames F through a target t (closures of {t,a,b}); keeps only NONDEGENERATE frames (Gram
matrix of a basis of F nonsingular -- legal frames), reports section sizes |F-perp| (inside R(t)), lines per frame,
and the EXACT minimum number of nondegenerate sections covering R(t) (CP-SAT set cover).
usage: python3 i13_frames.py  -> i13_frames_<kind>.pkl (t, frames, perps, degenerate-count)"""
import itertools, collections, pickle, time
import numpy as np
from lgeo13 import *
from ortools.sat.python import cp_model
eta = np.diag([1.0] * n + [-1.0])
def basis(m):
    M = np.zeros((0, n + 1))
    for s in bits(m):
        M2 = np.vstack([M, g.LA[s]])
        if np.linalg.matrix_rank(M2) > M.shape[0]: M = M2
    return M
def nondeg(m):
    B = basis(m); return abs(np.linalg.det(B @ eta @ B.T)) > 1e-6
for kind, t in (('T', IDX[('T', (0, 1, 2))]), ('P', IDX[('P', (0, 1))])):
    t0 = time.time(); R = HYP[t]
    frames = {}; deg = collections.Counter()
    for a, b in itertools.combinations([s for s in range(V) if s != t], 2):
        m = (1 << t) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        F = pp(m)
        if F in frames or F in deg: continue
        if nondeg(F): frames[F] = pm(F)
        else: deg[F] = pc(pm(F))
    print(kind, '|R(t)|', pc(R), '| nondegenerate frames through t:', len(frames), '| degenerate:', len(deg),
          'with perp sizes', dict(collections.Counter(deg.values())), '| %.0fs' % (time.time() - t0), flush=True)
    print('  section sizes:', dict(sorted(collections.Counter(pc(P) for P in frames.values()).items())), flush=True)
    print('  lines per frame:', dict(sorted(collections.Counter(pc(F) for F in frames).items())), flush=True)
    FL = list(frames); PL = [frames[F] for F in FL]
    pickle.dump((t, FL, PL), open('i13_frames_%s.pkl' % kind, 'wb'))
    for K in (3, 4):
        M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in FL]
        M.Add(sum(x) <= K)
        for s in bits(R): M.AddBoolOr([x[i] for i in range(len(FL)) if PL[i] >> s & 1])
        sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 900; sv.parameters.num_workers = 4
        st = sv.Solve(M)
        print('  cover of R(t) by <=', K, 'nondegenerate sections:', sv.StatusName(st), flush=True)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            sel = [i for i in range(len(FL)) if sv.Value(x[i])]
            print('   example: sizes', [pc(PL[i]) for i in sel], 'frame lines', [[KIND[s] + ''.join(map(str, SUPP[s])) for s in bits(FL[i])] for i in sel], flush=True)
            break
