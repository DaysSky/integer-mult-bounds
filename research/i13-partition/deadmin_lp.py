"""Dead-minimizer master: set cover with shared pieces (the v2 content-piece menus).
Objective: minimise (number of distinct non-leaf pieces used) + (merge penalties).
A merge penalty applies when a piece's content is used in >= 2 different cover *combinations* at the same
consuming pool; v1 approximation: penalty = (users_of_piece - 1) * W_MERGE with W_MERGE configurable
(0 = optimistic zero-waste sharing, 1 = one extra register per extra user).
Also solves the LP relaxation for a dual certificate (GLOP via ortools linear solver).
"""
import os, pickle, sys, time, collections
HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()
def log(*a, **kw): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

D = pickle.load(open(os.path.join(HERE, 'deadmin_menus2.pkl'), 'rb'))
menus = D['menus']; piece_of = D['piece_of']; frame_of = D['frame_of']
log('menus %d pieces %d' % (len(menus), len(piece_of)))
# piece metadata: cost 0 if any content is a single line (leaf), else 1
leaf = {pid: (bin(c).count('1') == 1) for (c, F), pid in piece_of.items()}
# covers as tuples of piece ids + optional leaf-fill marker
def cover_pieces(cover):
    return [piece_of[item] for item in cover if not (isinstance(item, tuple) and item and item[0] == 'LEAVES')]
demand_covers = {E: [cover_pieces(cv) for cv in cvs] for E, cvs in menus.items()}
log('demand covers: total', sum(len(v) for v in demand_covers.values()), flush=True)

from ortools.linear_solver import pywraplp
def solve_lp(w_merge):
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None: raise SystemExit('no GLOP')
    y = {}
    for E, cvs in demand_covers.items():
        for j in range(len(cvs)): y[(E, j)] = solver.NumVar(0, 1, '')
    p = {}
    for pid in range(len(piece_of)): p[pid] = solver.NumVar(0, 1, '')
    for E, cvs in demand_covers.items():
        solver.Add(sum(y[(E, j)] for j in range(len(cvs))) == 1)
        for j, ps in enumerate(cvs):
            for pid in ps: solver.Add(y[(E, j)] <= p[pid])
    # merge penalties: for each piece, users = sum of covers using it; penalty linearised as extra var
    obj = sum((1 - leaf[pid]) * p[pid] for pid in range(len(piece_of)))
    if w_merge > 0:
        u = {}
        for pid in range(len(piece_of)):
            us = [y[(E, j)] for E, cvs in demand_covers.items() for j, ps in enumerate(cvs) if pid in ps]
            if len(us) >= 2:
                u[pid] = solver.NumVar(0, solver.infinity(), '')
                solver.Add(u[pid] >= sum(us) - 1)
                obj = obj + w_merge * u[pid]
    solver.Minimize(obj)
    st = solver.Solve()
    log('LP status', st, 'objective %.2f' % solver.Objective().Value() if st == pywraplp.Solver.OPTIMAL else st)
    return solver.Objective().Value() if st == pywraplp.Solver.OPTIMAL else None

for wm in (0.0, 0.5, 1.0):
    v = solve_lp(wm)
    log('LP objective at w_merge = %.1f : %s' % (wm, v), flush=True)
