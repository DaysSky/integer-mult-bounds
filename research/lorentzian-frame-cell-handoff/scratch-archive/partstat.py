import sys, json, collections, pickle, itertools
sys.path.insert(0, '.')
from lgeo import *
from ortools.sat.python import cp_model
D = json.load(open('lr8det_f0.json'))
sel = {int(k): v for k, v in D['sel'].items()}; det = D['det']
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
cov = pickle.load(open('r8covers.pkl', 'rb'))
asg = collections.defaultdict(int)
for key, v in det['assign'].items():
    ri, i, u = map(int, key.split(','))
    if v: asg[(ri, i)] |= 1 << u
# all rank-3 frames (closed sets of rank 3) as line masks
F3 = set()
for a, b, c in itertools.combinations(range(V), 3):
    m = (1 << a) | (1 << b) | (1 << c)
    if G[a][b] == 0 and G[a][c] == 0 and G[b][c] == 0 or True:
        pass
print('enumerating rank-3 closed sets ...', flush=True)
# closed rank-3 sets: pp of rank-3 triples is too many combos (220C3 = 1.7M) -> use pairs + third
seen = set()
for a in range(V):
    for b in range(a + 1, V):
        m2 = pp((1 << a) | (1 << b))
        for c in range(b + 1, V):
            if m2 >> c & 1: continue
            m = (1 << a) | (1 << b) | (1 << c)
            F = pp(m)
            if F in seen: continue
            if rank(F) == 3: seen.add(F)
    if a % 40 == 0: print(a, len(seen), flush=True)
F3 = sorted(seen)
print('rank-3 closed sets', len(F3), collections.Counter(pc(F) for F in F3), flush=True)
pickle.dump(F3, open('rank3frames.pkl', 'wb'))
def kappa3(X, tl=10):
    cand = [F for F in F3 if F & X]
    # keep maximal intersections
    inter = {}
    for F in cand:
        I = F & X
        inter[I] = F
    keys = sorted(inter, key=pc, reverse=True); maxi = []
    for I in keys:
        if not any(I & ~J == 0 for J in maxi): maxi.append(I)
    M = cp_model.CpModel(); xs = [M.NewBoolVar('') for _ in maxi]
    for u in bits(X): M.AddBoolOr([xs[i] for i, I in enumerate(maxi) if I >> u & 1])
    M.Minimize(sum(xs)); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = 1
    st = sv.Solve(M); return int(sv.ObjectiveValue()), int(sv.BestObjectiveBound())
st = collections.Counter()
for ri in range(0, 20, 4):
    for i in range(4):
        P = asg[(ri, i)]
        k, lb = kappa3(P)
        st[(KIND[reps[ri]], pc(P), rank(P), k, lb)] += 1
        print(KIND[reps[ri]], 'part size', pc(P), 'rank', rank(P), 'kappa3', k, 'lb', lb, flush=True)
