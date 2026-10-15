"""Top coverage screen for a frame-cell system (necessary condition for ANY middle with plane-section tops).
For target t, a plane Q = closure(t, e) gives the section S_Q = perp(Q) (inside t-perp).  Line u in R(t) is ROUTABLE
into S_Q iff some system cell C of u lies inside S_Q (content of x_u can only enter a frame through a frame holding u
and its first mixing partner).  Per target: minimum number of sections covering R(t) by routable lines, optionally
with the in-chain cell read C_t (covers its own lines; must lie inside one chosen section = the in-chain section).
Also reports per target the lines of R(t) routable into NO plane section at all.
usage: ltop4.py SYSTEM.json [ntargets]"""
import sys, os, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, closure, perp, g
from ortools.sat.python import cp_model
pc = lambda m: bin(m).count('1')
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
NT = int(sys.argv[2]) if len(sys.argv) > 2 else V
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
co = {s: [C for C in cells if C >> s & 1] for s in range(V)}
kind = g.kind
res = collections.Counter(); unr_tot = 0; detail = []
for t in range(NT):
    R = HYP[t]
    planes = sorted(set(closure((1 << t) | (1 << e)) for e in range(V) if e != t and (os.environ.get("A2") != "1" or g.G[t, e] != 0)))
    secs = [perp(Q) for Q in planes]
    rout = []  # rout[i] = mask of u in R(t) routable into secs[i]
    for S in secs:
        m = 0
        for u in bits(R & S):
            if any(C & ~S == 0 for C in co[u]): m |= 1 << u
        rout.append(m)
    allr = 0
    for m in rout: allr |= m
    unr = R & ~allr
    # cells usable as in-chain read: C inside t-perp
    rc = [C for C in cells if C & ~R == 0]
    M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in secs]; y = {C: M.NewBoolVar('') for C in rc}
    M.Add(sum(y.values()) <= 1)
    for C in rc:   # the read cell must lie in a chosen section
        M.AddBoolOr([y[C].Not()] + [x[i] for i, S in enumerate(secs) if C & ~S == 0])
    for u in bits(R & allr):
        M.AddBoolOr([x[i] for i in range(len(secs)) if rout[i] >> u & 1] + [y[C] for C in rc if C >> u & 1])
    M.Minimize(sum(x))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 20; sv.parameters.num_workers = 4
    st = sv.Solve(M)
    k = int(sv.ObjectiveValue()); res[(kind[t], k, pc(unr))] += 1; unr_tot += pc(unr)
    detail.append((t, kind[t], pc(R), k, pc(unr), sv.StatusName(st)))
    print(t, kind[t], '|R|', pc(R), 'min sections', k, sv.StatusName(st), 'unroutable lines', pc(unr), flush=True)
print('summary (kind, min sections over routable lines, #unroutable):', sorted(res.items()))
print('total unroutable (t,u) pairs', unr_tot)
