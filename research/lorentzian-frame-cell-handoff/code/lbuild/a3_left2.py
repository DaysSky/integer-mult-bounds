"""Re-select the leftover targets' defect-1 triples for the all-A3 builder (build_a3g.py, ALLA3=1).
Complete A3 blocks of CHOICE are kept.  For every other target, each candidate triple (a3_triples.pkl) is costed by
the top demands it creates: A3-type triples (two triangles + the pair through t, defect inside the A3) create
B-perp, E_Q1, E_Q2, E_P keyed by their A3 (shared with any other user of that A3); other triples create full plane
sections.  CP-SAT minimises the total content (lines) of distinct new demands + KW per keeper (defect source not
provided).  usage: a3_left2.py CHOICE.pkl OUT.pkl [TL] [KW]"""
import sys, os, pickle, collections, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lmid'))
import lw
from lw import V, g, bits
from fastcl import fclosure
from ortools.sat.python import cp_model
HYP = g.HYP; pc = lambda m: bin(m).count('1')
CH, OUT = sys.argv[1], sys.argv[2]
TL = float(sys.argv[3]) if len(sys.argv) > 3 else 120
KW = int(sys.argv[4]) if len(sys.argv) > 4 else 30
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = (1 << V) - 1
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
def a3type(tr):
    a, b, c, d = tr
    tris = [Q for Q in (a, b, c) if pc(Q) == 3]; pairs = [Q for Q in (a, b, c) if pc(Q) == 2]
    if len(tris) == 2 and len(pairs) == 1 and d >= 0 and pairs[0] >> d & 1:
        A3 = fclosure(tris[0] | tris[1])
        if pc(A3) == 6 and A3 >> d & 1: return (A3, tris[0], tris[1], pairs[0], d)
    return None
def demands_of(tr):
    v = a3type(tr)
    if v is None: return [(pm(Q), pm(Q)) for Q in tr[:3]]
    A3, Q1, Q2, P, d = v; Bp = pm(A3)
    return [(Bp, Bp), (pm(Q1), pm(Q1) & ~Bp), (pm(Q2), pm(Q2) & ~Bp), (pm(P), pm(P) & ~Bp)]
choice = pickle.load(open(CH, 'rb'))
TR = pickle.load(open('a3_triples.pkl', 'rb'))
blk = {t: a3type(tr) for t, tr in choice.items()}
mem = collections.defaultdict(list)
for t, v in blk.items():
    if v: mem[v[0]].append(t)
fixed = {t for t, v in blk.items() if v and len(mem[v[0]]) == 6}
free = set()
for t in fixed: free.update(demands_of(choice[t]))
srcused = {blk[t][4] for t in fixed}            # opposites' sources read inside complete blocks
others = [t for t in range(V) if t not in fixed]
log('complete-block targets', len(fixed), '| to select', len(others))
M = cp_model.CpModel(); X = {}; dv = {}; kv = []
def dvar(K):
    if K not in dv: dv[K] = M.NewBoolVar('')
    return dv[K]
srcv = collections.defaultdict(list)
for t in others:
    xs = []
    for k, tr in enumerate(TR[t]):
        x = M.NewBoolVar(''); X[(t, k)] = x; xs.append(x)
        for K in demands_of(tr):
            if K not in free: M.AddImplication(x, dvar(K))
        d = tr[3]
        if d >= 0:
            if d in srcused: kv.append(x)                      # defect source taken -> keeper
            else: srcv[d].append(x)
    M.AddExactlyOne(xs)
# a free defect source can serve one target pure; extra users need keepers
for d, xs in srcv.items():
    e = M.NewIntVar(0, len(xs), '')
    M.Add(e >= sum(xs) - 1); kv.append(e)
M.Minimize(sum(pc(K[1]) * v for K, v in dv.items()) + KW * sum(kv))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M)
new = dict(choice)
for t in others:
    k = next(k for k in range(len(TR[t])) if sv.Value(X[(t, k)]))
    new[t] = TR[t][k]
na3 = sum(1 for t in others if a3type(new[t]))
log('status', sv.StatusName(st), '| objective', sv.ObjectiveValue(), '| A3-type among selected', na3, '/', len(others),
    '| new demands', sum(1 for v in dv.values() if sv.Value(v)))
pickle.dump(new, open(OUT, 'wb'))
