"""Faster exact model for maximal half sharing in I_{11,1}: every PPTT frame lies in exactly one star-D4 block (3
frames sharing all 12 halves and the Q-part) and every TTTT frame in exactly one Pasch pair (2 frames sharing all 12
halves).  Distinct halves = 12 x (#blocks touched + #pairs touched).  Minimise that over partitions with <= PUN
punctured lines.  usage: sharepart2.py PUN TIME [workers]"""
import sys, collections, itertools, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
PUN = int(sys.argv[1]); TL = float(sys.argv[2]); NW = int(sys.argv[3]) if len(sys.argv) > 3 else 4
g = Geom(11); V = g.V; G = g.G
frames = pickle.load(open('halfglobal_11.pkl', 'rb'))['frames']
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
grp = collections.defaultdict(list)          # half-set signature -> frames
for fi, f in enumerate(frames): grp[halves(f)].append(fi)
groups = list(grp.values())
print('groups', len(groups), 'sizes', sorted(collections.Counter(len(x) for x in groups).items()), flush=True)
gof = {}
for gi, fs in enumerate(groups):
    for fi in fs: gof[fi] = gi
m = cp_model.CpModel()
x = [m.NewBoolVar('') for _ in frames]; z = [m.NewBoolVar('') for _ in groups]
for fi in range(len(frames)): m.AddImplication(x[fi], z[gof[fi]])
byline = collections.defaultdict(list)
for fi, f in enumerate(frames):
    for u in f: byline[u].append(fi)
cov = []
for u in range(V):
    c = m.NewBoolVar(''); m.Add(sum(x[fi] for fi in byline[u]) == c); cov.append(c)
m.Add(sum(cov) >= V - PUN)
m.Minimize(sum(z))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = NW
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(self):
        print('  touched groups', int(self.ObjectiveValue()), '(distinct halves %d)' % (12 * int(self.ObjectiveValue())), 'bound', int(self.BestObjectiveBound()), 'time %.0f' % self.WallTime(), flush=True)
st = s.Solve(m, CB())
print('status', s.StatusName(st), 'obj', s.ObjectiveValue(), 'bound', s.BestObjectiveBound(), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    chosen = [frames[fi] for fi in range(len(frames)) if s.Value(x[fi])]
    pun = [u for u in range(V) if not s.Value(cov[u])]
    full = collections.Counter(sum(s.Value(x[fi]) for fi in groups[gi]) for gi in range(len(groups)) if s.Value(z[gi]))
    print('frames', len(chosen), 'punctured', [(g.kind[u], g.supp[u]) for u in pun], 'frames per touched group:', sorted(full.items()))
    pickle.dump((chosen, pun), open('sharepart2_p%d.pkl' % PUN, 'wb'))
