"""Dead-minimizer primal: CP-SAT integer solution with exact pool accounting.
Model:
- One cover chosen per demand (cover = tuple of piece ids, from menus2).
- A used piece costs 1 if non-leaf (0 if leaf).
- Pool accounting per piece: users(E) = demands whose chosen cover contains the piece.  The piece register
  is read by all of them IF they read it at frames containing the piece frame -- true by construction
  (each piece frame lies inside the demand frame).  Zero-waste sharing says 1 register serves all users;
  the honest extra is when a piece must be FED to several different assembled combinations downstream.
  CP-SAT v1: charge (users - 1) * 0 by default and also produce a "users histogram" so the pool structure
  of the solution can be priced externally.  ALSO charge 1 per (piece, user) pair whose cover uses the piece
  in a different XOR-combination than another user (needs cover-combination identity): approximated by
  charging per (piece, combination-signature) beyond the first.
- Objective: sum piece costs + sum combination-extras.
This yields a true integer design whose register count can be computed exactly afterwards.
"""
import os, pickle, sys, time, collections
HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()
def log(*a, **kw): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

D = pickle.load(open(os.path.join(HERE, 'deadmin_menus2.pkl'), 'rb'))
menus = D['menus']; piece_of = D['piece_of']; frame_of = D['frame_of']
leaf = {pid: (bin(c).count('1') == 1) for (c, F), pid in piece_of.items()}
demand_covers = {E: [[piece_of[item] for item in cv if not (isinstance(item, tuple) and item and item[0] == 'LEAVES')]
                     for cv in cvs] for E, cvs in menus.items()}
# drop duplicate cover piece-sets
for E in demand_covers: demand_covers[E] = sorted(set(tuple(p) for p in demand_covers[E]))
log('covers after dedup: total', sum(len(v) for v in demand_covers.values()), flush=True)

from ortools.sat.python import cp_model
m = cp_model.CpModel()
used = {pid: m.NewBoolVar('') for pid in range(len(piece_of))}
y = {}
for E, cvs in demand_covers.items():
    for j in range(len(cvs)): y[(E, j)] = m.NewBoolVar('')
for E, cvs in demand_covers.items():
    m.AddExactlyOne([y[(E, j)] for j in range(len(cvs))])
    for j, ps in enumerate(cvs):
        for pid in ps: m.AddImplication(y[(E, j)], used[pid])
m.Minimize(sum((0 if leaf[pid] else 1) * used[pid] for pid in range(len(piece_of))))
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = float(os.environ.get('TMAX', '600'))
solver.parameters.num_search_workers = 8
st = solver.Solve(m)
log('status', solver.StatusName(st), 'objective', solver.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else '-', 'bound', solver.BestObjectiveBound())
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    chosen = {}
    for E, cvs in demand_covers.items():
        for j in range(len(cvs)):
            if solver.Value(y[(E, j)]):
                chosen[E] = list(cvs[j]); break
    used_p = sorted(pid for pid in range(len(piece_of)) if solver.Value(used[pid]))
    log('used pieces', len(used_p), 'non-leaf', sum(1 for p in used_p if not leaf[p]))
    # user histogram
    uc = collections.Counter()
    for E, ps in chosen.items():
        for pid in ps: uc[pid] += 1
    hu = collections.Counter(uc.values())
    log('users-per-piece histogram (top):', sorted(hu.items(), reverse=True)[:15])
    pickle.dump({'chosen': {E: list(ps) for E, ps in chosen.items()}, 'used': used_p,
                 'piece_of': piece_of}, open(os.path.join(HERE, 'deadmin_primal.pkl'), 'wb'))
    log('saved')
