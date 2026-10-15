"""m_t = |R(t)| - (max lines of R(t) routably covered by <= 3 A2 plane sections + one in-chain cell read inside one of
them).  In any 4-section top at least one section is a 2-line plane (A2-only covers need 5, ltop4a), so >= m_t
incidences of t pass through 2-user sections.  usage: lmt.py SYSTEM.json"""
import sys, os, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, closure, perp, g
from ortools.sat.python import cp_model
pc = lambda m: bin(m).count('1')
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
co = {s: [C for C in cells if C >> s & 1] for s in range(V)}
out = {}
for t in range(V):
    R = HYP[t]
    planes = sorted(set(closure((1 << t) | (1 << e)) for e in range(V) if e != t and g.G[t, e] != 0))
    secs = [perp(Q) for Q in planes]
    rout = []
    for S in secs:
        m = 0
        for u in bits(R & S):
            if any(C & ~S == 0 for C in co[u]): m |= 1 << u
        rout.append(m)
    rc = [C for C in cells if C & ~R == 0]
    M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in secs]; y = {C: M.NewBoolVar('') for C in rc}
    M.Add(sum(x) <= 3); M.Add(sum(y.values()) <= 1)
    for C in rc: M.AddBoolOr([y[C].Not()] + [x[i] for i, S in enumerate(secs) if C & ~S == 0])
    z = {}
    for u in bits(R):
        z[u] = M.NewBoolVar('')
        M.AddBoolOr([z[u].Not()] + [x[i] for i in range(len(secs)) if rout[i] >> u & 1] + [y[C] for C in rc if C >> u & 1])
    M.Maximize(sum(z.values()))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 30; sv.parameters.num_workers = 4
    st = sv.Solve(M)
    ub = int(sv.BestObjectiveBound() + 1e-6)   # proven upper bound on A2 coverage -> lower bound on m_t
    out[t] = pc(R) - ub
    print(t, g.kind[t], '|R|', pc(R), 'max A2 coverage <=', ub, sv.StatusName(st), 'm_t >=', out[t], flush=True)
json.dump(out, open('lmt_%s.json' % os.path.basename(sys.argv[1]).split('.')[0], 'w'))
print('sum m_t >=', sum(out.values()))
