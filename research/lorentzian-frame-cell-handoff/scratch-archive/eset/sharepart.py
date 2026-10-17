"""Partition of I_{11,1} into disjoint good 4-frames (<= PUN punctured lines) minimising the number of distinct E-set
sign halves used (i.e. maximising E8-style half sharing; E8 R420: 360 half slots, 120 distinct, every half 3-fold).
usage: sharepart.py PUN TIME [seed]"""
import sys, collections, itertools, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
PUN = int(sys.argv[1]); TL = float(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
g = Geom(11); V = g.V; G = g.G
OM = [0] * V
for i in range(V):
    for j in range(V):
        if i != j and G[i, j] == 0: OM[i] |= 1 << j
d = pickle.load(open('halfglobal.pkl', 'rb')) if __import__('os').path.exists('halfglobal.pkl') else pickle.load(open('halfglobal_11.pkl', 'rb'))
frames = d['frames']
halves = collections.defaultdict(set)     # H -> frames
fh = collections.defaultdict(list)        # frame -> its 12 halves
for fi, f in enumerate(frames):
    for t, e in itertools.combinations(f, 2):
        k, l = [x for x in f if x not in (t, e)]
        E = OM[t] & OM[e] & ~OM[k] & ~OM[l] & ~(1 << k) & ~(1 << l)
        Ep = 0; Em = 0; m = E
        while m:
            x = m & -m; u = x.bit_length() - 1; m ^= x
            if G[u, k] == G[u, l]: Ep |= x
            else: Em |= x
        for H in (Ep, Em): halves[H].add(fi); fh[fi].append(H)
Hl = list(halves); hid = {H: i for i, H in enumerate(Hl)}
m = cp_model.CpModel()
x = [m.NewBoolVar('') for _ in frames]
z = [m.NewBoolVar('') for _ in Hl]
for fi in range(len(frames)):
    for H in fh[fi]: m.AddImplication(x[fi], z[hid[H]])
cov = []
for u in range(V):
    fs = [fi for fi, f in enumerate(frames) if u in f]
    c = m.NewBoolVar(''); m.Add(sum(x[fi] for fi in fs) == c); cov.append(c)
m.Add(sum(cov) >= V - PUN)
m.Minimize(sum(z))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = 8; s.parameters.random_seed = seed
s.parameters.log_search_progress = False
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(self): super().__init__(); self.best = None
    def on_solution_callback(self):
        print('  solution: distinct halves', int(self.ObjectiveValue()), 'bound', int(self.BestObjectiveBound()), 'time %.0f' % self.WallTime(), flush=True)
st = s.Solve(m, CB())
print('status', s.StatusName(st), 'obj', s.ObjectiveValue(), 'bound', s.BestObjectiveBound(), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    chosen = [frames[fi] for fi in range(len(frames)) if s.Value(x[fi])]
    pun = [u for u in range(V) if not s.Value(cov[u])]
    used = [H for H in Hl if s.Value(z[hid[H]])]
    mult = collections.Counter(sum(1 for fi in halves[H] if s.Value(x[fi])) for H in used)
    print('frames', len(chosen), 'punctured', pun, 'half sharing multiplicity:', sorted(mult.items()))
    pickle.dump((chosen, pun), open('sharepart_p%d_s%d.pkl' % (PUN, seed), 'wb'))
