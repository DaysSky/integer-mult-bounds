"""Can ANY TTTT frame appear in a star-structured (apex 12) aligned partition of I_{13,1}?
All TTTT frames on points 0..11 are equivalent under S_12 = Stab(12).  For t0: star frames compatible with t0; exact
cover of the 66 P lines on 0..11 by them (CP-SAT).  Also: maximum number of P lines coverable (with P punctures)."""
import sys, pickle, numpy as np
from ortools.sat.python import cp_model
frames, comp_lists, kinds = pickle.load(open('compat13.pkl', 'rb'))
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; F = np.array(frames); nf = len(F)
def is_comp(a, b):
    arr = comp_lists[a]; k = np.searchsorted(arr, b); return k < len(arr) and arr[k] == b
supp = lambda l: g.supp[l]
star = [j for j in range(nf) if kinds[j] == 'PPTT' and all(12 in supp(l) for l in F[j] if g.kind[l] == 'T')]
tts = [j for j in range(nf) if kinds[j] == 'TTTT' and all(12 not in supp(l) for l in F[j])]
t0 = tts[0]
cs = [j for j in star if is_comp(t0, j)]
print('t0', [supp(l) for l in F[t0]], ': star frames compatible with t0:', len(cs), 'of', len(star))
Plines = [l for l in range(V) if g.kind[l] == 'P' and 12 not in supp(l)]
cov = {l: sum(1 for j in cs if l in F[j]) for l in Plines}
print('P lines with no compatible star frame:', sum(1 for l in Plines if cov[l] == 0))
m = cp_model.CpModel(); x = {j: m.NewBoolVar('s%d' % j) for j in cs}; p = {l: m.NewBoolVar('p%d' % l) for l in Plines}
for l in Plines: m.Add(sum(x[j] for j in cs if l in F[j]) + p[l] == 1)
m.Minimize(sum(p.values()))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 2
st = s.Solve(m)
print('min extra P punctures with t0 present (star apex 12):', s.ObjectiveValue(), s.StatusName(st))
# how many star frames does a random TTTT frame on 0..11 kill? distribution over a few
import random
random.seed(0)
for t in random.sample(tts, 5):
    print('  TTTT', [supp(l) for l in F[t]], 'compatible star frames', sum(1 for j in star if is_comp(t, j)))
