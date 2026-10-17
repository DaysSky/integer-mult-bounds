"""E8 rank-5 frame-section top design (no symmetry).  Choose rank-3 frames (types: A3 = 6 lines, perp D5 20; A2A1 = 4,
perp 15; A1^3 = 3, perp 13; select with TYPES) so that every line lies in exactly K chosen frames and every orthogonal
pair (t,u) has a chosen frame X containing t with u _|_ X.  usage: e8r5design.py K timelimit TYPES(6|46|346)
-> e8r5design_K_TYPES.json (list of frame masks hex)"""
import sys, itertools, collections, json, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from ortools.sat.python import cp_model
K = int(sys.argv[1]); TL = float(sys.argv[2]); TYPES = set(int(c) for c in sys.argv[3])
V = e8.V; HYP = e8.HYP; bits = e8.bits
pc = lambda m: bin(m).count('1')
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def pm(m):
    r = e8.FULL
    for s in bits(m): r &= HYP[s]
    return r
frames = set()
for t in range(V):
    for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
        F, r = e8.closure((1 << t) | (1 << a) | (1 << b))
        if r == 3 and pc(F) in TYPES: frames.add(F)
frames = sorted(frames)
log('frames', len(frames), collections.Counter(pc(F) for F in frames))
P = [pm(F) for F in frames]
M = cp_model.CpModel(); y = [M.NewBoolVar('') for _ in frames]
inF = collections.defaultdict(list)
for i, F in enumerate(frames):
    for s in bits(F): inF[s].append(i)
for s in range(V): M.Add(sum(y[i] for i in inF[s]) == K)
ncl = 0
for t in range(V):
    R = HYP[t] & ~(1 << t)
    for u in bits(R):
        M.AddBoolOr([y[i] for i in inF[t] if P[i] >> u & 1]); ncl += 1
log('coverage clauses', ncl)
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 2
st = sv.Solve(M)
log('status', sv.StatusName(st))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    used = [frames[i] for i in range(len(frames)) if sv.Value(y[i])]
    log('used frames', len(used), collections.Counter(pc(F) for F in used))
    json.dump([hex(F) for F in used], open('e8r5design_%d_%s.json' % (K, sys.argv[3]), 'w'))
