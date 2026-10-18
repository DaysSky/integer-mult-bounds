"""Halves-assembly set cover: demands = 576 maxpairs-partition halves (16/30/64 lines), pieces = closed
nondegenerate flats inside the halves' closure frames.  Same model as deadmin_primal; decides whether the
6h rank-7 block-group blueprint's assembly layer fits its ~650-register budget."""
import os, pickle, itertools, collections, time, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g13 = Geom(13); V = g13.V; HYP = g13.HYP; G = g13.G
bits = g13.bits
def cl(m): return g13.closure(m)[0] if m else 0
def rk(m): return g13.closure(m)[1] if m else 0

halves = [sum(1 << u for u in hl) for hl in pickle.load(open(os.path.join(HERE, 'halves_maxpairs.pkl'), 'rb'))]
print('halves', len(halves), flush=True)
t0 = time.time()
frames = [cl(h) for h in halves]
cand = set()
for S in set(frames):
    for u in bits(S):
        A = cl(S & HYP[u])
        if A != S: cand.add(A)
    cand.add(S)
cand = {A for A in cand if A and 2 <= rk(A) <= 10}
print('candidate flats', len(cand), '%.0fs' % (time.time()-t0), flush=True)
ND = {}
def nondeg(A):
    if A not in ND:
        b = []
        for i in bits(A):
            if np.linalg.matrix_rank(g13.LA[b + [i]]) > len(b): b.append(i)
        Gm = np.array([[G[a, bb] for bb in b] for a in b], dtype=float)
        ND[A] = abs(round(np.linalg.det(Gm))) > 0
    return ND[A]
cand = {A for A in cand if nondeg(A)}
print('nondegenerate candidates', len(cand), '%.0fs' % (time.time()-t0), flush=True)
dem_cand = {}
for h in halves:
    S = cl(h)
    dem_cand[h] = sorted(A for A in cand if A & ~S == 0 and A != S and A & h)
print('options per half: min %d max %d mean %.0f' % (min(len(v) for v in dem_cand.values()),
      max(len(v) for v in dem_cand.values()), sum(len(v) for v in dem_cand.values())/len(dem_cand)), flush=True)
def covers_of(E, cands, kmax=3, limit=60):
    out = []
    cl_ = sorted(cands, key=lambda A: -bin(A).count('1'))
    def rec(rem, chosen):
        if len(out) >= limit: return
        if rem == 0: out.append(tuple(chosen)); return
        if len(chosen) >= kmax:
            out.append(tuple(chosen) + (('L', rem),)); return
        u = (rem & -rem).bit_length() - 1
        for A in cl_:
            if A >> u & 1 and A & ~rem == 0 and A not in chosen:
                rec(rem & ~A, chosen + [A])
                if len(out) >= limit: return
        out.append(tuple(chosen) + (('L', rem),))
    rec(E, [])
    return out
menus = {}
piece_of = {}
t1 = time.time()
for n, h in enumerate(halves):
    cv = covers_of(h, dem_cand[h])
    menus[h] = cv
    for cover in cv:
        for item in cover:
            if isinstance(item, tuple) and item and item[0] == 'L': continue
            if item not in piece_of: piece_of[item] = len(piece_of)
    if n % 150 == 0: print('menu', n, 'covers', len(cv), 'pieces', len(piece_of), '%.0fs' % (time.time()-t1), flush=True)
print('total covers', sum(len(v) for v in menus.values()), 'pieces', len(piece_of), flush=True)
from ortools.sat.python import cp_model
m = cp_model.CpModel()
used = {pid: m.NewBoolVar('') for pid in range(len(piece_of))}
y = {}
for h, cvs in menus.items():
    for j in range(len(cvs)): y[(h, j)] = m.NewBoolVar('')
leaf = {pid: bin(c).count('1') == 1 for (c, F), pid in piece_of.items()}
for h, cvs in menus.items():
    m.AddExactlyOne([y[(h, j)] for j in range(len(cvs))])
    for j, ps in enumerate(cvs):
        for item in ps:
            if isinstance(item, tuple) and item and item[0] == 'L': continue
            m.AddImplication(y[(h, j)], used[piece_of[item]])
m.Minimize(sum((0 if leaf[pid] else 1) * used[pid] for pid in range(len(piece_of))))
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = float(os.environ.get('TMAX', '240'))
solver.parameters.num_search_workers = 8
st = solver.Solve(m)
print('HALVES assembly:', solver.StatusName(st),
      'objective', solver.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else '-',
      'bound', solver.BestObjectiveBound(), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    used_p = [pid for pid in range(len(piece_of)) if solver.Value(used[pid])]
    rh = collections.Counter(rk(F) for (c, F), pid in piece_of.items() if pid in set(used_p))
    print('used pieces', len(used_p), 'non-leaf', sum(1 for p in used_p if not leaf[p]), 'rank hist', dict(sorted(rh.items())))
    pickle.dump({'used': used_p, 'piece_of': piece_of}, open(os.path.join(HERE, 'halves_assembly.pkl'), 'wb'))
