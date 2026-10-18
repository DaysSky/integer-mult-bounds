"""Dead-minimizer v2: rank-weighted primal.  Pieces cost by their frame rank (shallow = fewer climbs = cheaper
in the pricer's fragmentation metric).  Also minimises the dead-piece rank profile directly.
Cost model: piece of rank r costs w(r) >= 1, w calibrated to the pricer's marginal (one dead register with
piece shape (3,4,6) at break-even ~ 1 unit; shallow pieces (2,9) cheaper than deep (4,6,3)...).  We use
w(r) = 1 + alpha * max(0, r - 3) and scan alpha; plus count 0-cost leaves.
Also: a "combination-extra" term - pieces used by >= 2 demands in different XOR-combinations pay 1 extra.
"""
import os, pickle, sys, time, collections
HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()
def log(*a, **kw): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

D = pickle.load(open(os.path.join(HERE, 'deadmin_menus2.pkl'), 'rb'))
menus = D['menus']; piece_of = D['piece_of']; frame_of = D['frame_of']
# piece_of keys saved as tuples but pickle may return lists
piece_of = {tuple(k) if not isinstance(k, tuple) else k: v for k, v in piece_of.items()}
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g13 = Geom(13)
rank_of = {}
def rkof(A):
    if A not in rank_of: rank_of[A] = g13.closure(A)[1] if A else 0
    return rank_of[A]
piece_rank = {pid: rkof(F) for (c, F), pid in piece_of.items()}
piece_size = {pid: bin(c).count('1') for (c, F), pid in piece_of.items()}
leaf = {pid: piece_size[pid] == 1 for pid in piece_of.values()}
log('pieces %d, rank hist %s' % (len(piece_of), dict(sorted(collections.Counter(piece_rank.values()).items()))), flush=True)

demand_covers = {E: sorted(set(tuple(piece_of[item] for item in cv
                                       if not (isinstance(item, tuple) and item and item[0] == 'LEAVES')))
                           for cv in cvs) for E, cvs in menus.items()}
log('covers after dedup: total', sum(len(v) for v in demand_covers.values()), flush=True)

from ortools.sat.python import cp_model
def solve(alpha, tmax):
    m = cp_model.CpModel()
    used = {pid: m.NewBoolVar('') for pid in range(len(piece_of))}
    y = {}
    for E, cvs in demand_covers.items():
        for j in range(len(cvs)): y[(E, j)] = m.NewBoolVar('')
    for E, cvs in demand_covers.items():
        m.AddExactlyOne([y[(E, j)] for j in range(len(cvs))])
        for j, ps in enumerate(cvs):
            for pid in ps: m.AddImplication(y[(E, j)], used[pid])
    def w(pid):
        if leaf[pid]: return 0
        r = piece_rank[pid]
        return 1 + alpha * max(0, r - 3)
    # total climbs term: used pieces contribute their rank cost; ALSO the leaf-fill remainder is free
    m.Minimize(sum(w(pid) * used[pid] for pid in range(len(piece_of))))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tmax
    solver.parameters.num_search_workers = 8
    st = solver.Solve(m)
    ok = st in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    res = None
    if ok:
        chosen = {E: list(cvs[j]) for E, cvs in demand_covers.items() for j in range(len(cvs)) if solver.Value(y[(E, j)])}
        used_p = sorted(pid for pid in range(len(piece_of)) if solver.Value(used[pid]))
        res = {'chosen': chosen, 'used': used_p}
        ndead = sum(1 for p in used_p if not leaf[p])
        rh = collections.Counter(piece_rank[p] for p in used_p if not leaf[p])
        log('alpha %.2f: status %s, non-leaf pieces %d, obj %.1f, rank hist %s' % (
            alpha, solver.StatusName(st), ndead, solver.ObjectiveValue(), dict(sorted(rh.items()))), flush=True)
        pickle.dump(res, open(os.path.join(HERE, 'deadmin_primal_a%s.pkl' % str(alpha).replace('.', '')), 'wb'))
    else:
        log('alpha %.2f: %s' % (alpha, solver.StatusName(st)), flush=True)
    return res

for alpha in (0.0, 0.25, 0.5, 1.0):
    solve(alpha, float(os.environ.get('TMAX', '120')))
log('done', flush=True)
