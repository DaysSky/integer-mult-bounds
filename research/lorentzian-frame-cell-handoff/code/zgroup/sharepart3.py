"""Sharing partition, decomposed: fix complete star-D4 blocks (from blocks8.py), then cover the remaining lines with
good frames minimising touched groups (blocks / Pasch pairs), <= PUN punctures.  usage: sharepart3.py PUN TIME"""
import sys, collections, itertools, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
PUN = int(sys.argv[1]); TL = float(sys.argv[2])
g = Geom(11); V = g.V; G = g.G
idx = {(g.kind[i], g.supp[i]): i for i in range(V)}
P = lambda a, b: idx[('P', tuple(sorted((a, b))))]; T = lambda a, b, c: idx[('T', tuple(sorted((a, b, c))))]
blocks = [(0, (1, 3, 8, 10)), (2, (0, 4, 9, 10)), (3, (2, 4, 5, 8)), (5, (0, 1, 2, 6)), (9, (0, 3, 5, 7)), (10, (6, 7, 8, 9))]
fixed = []
for h, S in blocks:
    a, b, c, d = S
    for (p, q), (r, s) in (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))):
        fixed.append(tuple(sorted((P(p, q), P(r, s), T(p, q, h), T(r, s, h)))))
used = set(u for f in fixed for u in f); assert len(used) == 72
frames = pickle.load(open('halfglobal_11.pkl', 'rb'))['frames']
cand = [f for f in frames if not (set(f) & used)]
print('candidate frames', len(cand), flush=True)
OM = [0] * V
for i in range(V):
    for j in range(V):
        if i != j and G[i, j] == 0: OM[i] |= 1 << j
def halves(f):
    out = []
    for t, e in itertools.combinations(f, 2):
        k, l = [x for x in f if x not in (t, e)]
        E = OM[t] & OM[e] & ~OM[k] & ~OM[l] & ~(1 << k) & ~(1 << l); Ep = Em = 0; m = E
        while m:
            x = m & -m; u = x.bit_length() - 1; m ^= x
            if G[u, k] == G[u, l]: Ep |= x
            else: Em |= x
        out += [Ep, Em]
    return frozenset(out)
grp = collections.defaultdict(list)
for fi, f in enumerate(cand): grp[halves(f)].append(fi)
groups = list(grp.values()); gof = {fi: gi for gi, fs in enumerate(groups) for fi in fs}
m = cp_model.CpModel(); x = [m.NewBoolVar('') for _ in cand]; z = [m.NewBoolVar('') for _ in groups]
for fi in range(len(cand)): m.AddImplication(x[fi], z[gof[fi]])
byline = collections.defaultdict(list)
for fi, f in enumerate(cand):
    for u in f: byline[u].append(fi)
cov = []
for u in range(V):
    if u in used: continue
    c = m.NewBoolVar(''); m.Add(sum(x[fi] for fi in byline[u]) == c); cov.append((u, c))
m.Add(sum(c for _, c in cov) >= V - 72 - PUN)
m.Minimize(sum(z))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = 3
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(self): print('  touched', int(self.ObjectiveValue()), '+6 blocks; bound', int(self.BestObjectiveBound()), 'time %.0f' % self.WallTime(), flush=True)
st = s.Solve(m, CB()); print('status', s.StatusName(st), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    chosen = fixed + [cand[fi] for fi in range(len(cand)) if s.Value(x[fi])]
    pun = [u for u, c in cov if not s.Value(c)]
    pickle.dump((chosen, pun), open('sharepart3_p%d.pkl' % PUN, 'wb'))
    print('frames', len(chosen), 'punctured', [(g.kind[u], g.supp[u]) for u in pun])
