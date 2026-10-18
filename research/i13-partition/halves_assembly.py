"""Halves-assembly set cover v2 (fixed): demands = 576 maxpairs-partition halves (16/30/64 lines).
Pieces are CONTENT pieces (c, F): c a nonempty subset of the half's lines, F = cl(c) a closed
nondegenerate flat of rank <= 10 (the deadmin_menus2 semantics; the v1 bug required whole flats A <=
cl(h) with A & h lines, which for these halves are almost always disjoint from h, so every menu
degenerated to leaf-fill only).  Covers = disjoint content partitions of the half into <= KMAX pieces
+ free leaf fill.  Objective = non-leaf pieces used (leaf fill = 0).  This answers: how many registers
does the maxpairs partition's half layer cost at the top-assembly level (the analogue of the 610-demand
PG-top run that gave 573)?
NOTE (budget caveat): the "~650 assembly budget" figures quoted earlier were I_{11,1} numbers (450
movers; 6i prices); an I_{13,1} blueprint needs ~886 movers plus §3h feeders, so compare the result to
a recomputed I13 budget, not to 650.
"""
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
print('halves', len(halves), 'sizes', sorted(collections.Counter(bin(h).count('1') for h in halves).items()), flush=True)
t0 = time.time()
# candidate CONTENT sets: contents from candidate flats intersected with the half (like deadmin_menus2's
# piece_options): for each closed flat F of rank <= 10 reachable from the half's closure, c = F & h.
# Build candidate flats from the closure frames of the halves (line-normal hyperplanes + the frame).
frames = [cl(h) for h in halves]
flat_cand = set()
for S in set(frames):
    flat_cand.add(S)
    for u in bits(S):
        A = cl(S & HYP[u])
        if A != S: flat_cand.add(A)
flat_cand = {A for A in flat_cand if A and 2 <= rk(A) <= 10}
print('candidate flats', len(flat_cand), '%.0fs' % (time.time()-t0), flush=True)
ND = {}
def nondeg(A):
    if A not in ND:
        b = []
        for i in bits(A):
            if np.linalg.matrix_rank(g13.LA[b + [i]]) > len(b): b.append(i)
        Gm = np.array([[G[a, bb] for bb in b] for a in b], dtype=float)
        ND[A] = abs(round(np.linalg.det(Gm))) > 0
    return ND[A]
flat_cand = {A for A in flat_cand if nondeg(A)}
print('nondegenerate candidate flats', len(flat_cand), '%.0fs' % (time.time()-t0), flush=True)
# contents per half: (F & h) for flats F <= cl(h), F != cl(h); keep distinct
dem_cand = {}
for h in halves:
    S = cl(h)
    cs = set()
    for F in flat_cand:
        if F & ~S == 0:
            c = F & h
            if c and c != h: cs.add(c)
    dem_cand[h] = sorted(cs, key=lambda c: -bin(c).count('1'))
print('content options per half: min %d max %d mean %.0f' % (min(len(v) for v in dem_cand.values()),
      max(len(v) for v in dem_cand.values()), sum(len(v) for v in dem_cand.values())/len(dem_cand)), flush=True)
KMAX = 4
def covers_of(E, contents, kmax=KMAX, limit=200):
    out = []
    def rec(rem, chosen):
        if len(out) >= limit: return
        if rem == 0: out.append(tuple(chosen)); return
        if len(chosen) >= kmax:
            out.append(tuple(chosen) + (('L', rem),)); return
        u = (rem & -rem).bit_length() - 1
        for c in contents:
            if c >> u & 1 and c & ~rem == 0 and c not in chosen:
                rec(rem & ~c, chosen + [c])
                if len(out) >= limit: return
        out.append(tuple(chosen) + (('L', rem),))
    rec(E, [])
    return out
menus = {}
piece_of = {}   # (c, F=cl(c)) -> pid
t1 = time.time()
for n, h in enumerate(halves):
    cv = covers_of(h, dem_cand[h])
    menus[h] = cv
    for cover in cv:
        for item in cover:
            if isinstance(item, tuple) and item and item[0] == 'L': continue
            key = (item, cl(item))
            if key not in piece_of: piece_of[key] = len(piece_of)
    if n % 150 == 0: print('menu', n, 'covers', len(cv), 'pieces', len(piece_of), '%.0fs' % (time.time()-t1), flush=True)
print('total covers', sum(len(v) for v in menus.values()), 'distinct pieces', len(piece_of), '%.0fs' % (time.time()-t1), flush=True)
pickle.dump({'menus': {h: [(list(cv)) for cv in cvs] for h, cvs in menus.items()},
             'piece_of': {str(k): v for k, v in piece_of.items()}},
            open(os.path.join(HERE, 'halves_menus.pkl'), 'wb'))
from ortools.sat.python import cp_model
m = cp_model.CpModel()
used = {pid: m.NewBoolVar('') for pid in range(len(piece_of))}
y = {}
for h, cvs in menus.items():
    for j in range(len(cvs)): y[(h, j)] = m.NewBoolVar('')
piece_key = {v: k for k, v in piece_of.items()}
leaf = {pid: bin(piece_key[pid][0]).count('1') == 1 for pid in range(len(piece_of))}
for h, cvs in menus.items():
    m.AddExactlyOne([y[(h, j)] for j in range(len(cvs))])
    for j, ps in enumerate(cvs):
        for item in ps:
            if isinstance(item, tuple) and item and item[0] == 'L': continue
            m.AddImplication(y[(h, j)], used[piece_of[(item, cl(item))]])
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
    rh = collections.Counter(rk(piece_key[pid][1]) for pid in used_p if not leaf[pid])
    sh = collections.Counter()
    use = collections.Counter()
    for h, cvs in menus.items():
        for j, ps in enumerate(cvs):
            if solver.Value(y[(h, j)]):
                for item in ps:
                    if isinstance(item, tuple) and item and item[0] == 'L': continue
                    use[piece_of[(item, cl(item))]] += 1
    print('used pieces', len(used_p), 'non-leaf', sum(1 for p in used_p if not leaf[p]),
          'rank hist', dict(sorted(rh.items())), flush=True)
    print('piece use histogram (>=2):', dict(sorted(collections.Counter(use.values()).items())))
    fr = {piece_key[pid][1] for pid in used_p if not leaf[pid]}
    print('distinct piece frames', len(fr), flush=True)
    pickle.dump({'used': used_p, 'piece_of': {str(k): v for k, v in piece_of.items()}},
                open(os.path.join(HERE, 'halves_assembly.pkl'), 'wb'))
