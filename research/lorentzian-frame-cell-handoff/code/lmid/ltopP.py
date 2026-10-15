"""Paired top for a frame-cell system.  Each target t picks plane sections (planes Q containing t, S = perp(Q)):
 - at most one IN-CHAIN section, read for free from the delivery register of a co-user e of Q (another line of Q)
   whose part on S is the FULL routable set rt(S); t's own part on it is then rt(S) as well;
 - DELIVERED sections, each one register; 'full' (part = rt(S)) if some co-user reads it in-chain, else partial.
Constraints per t: full sections (in-chain + delivered-full) have pairwise disjoint rt(S); every u in R(t) is covered.
Minimise total deliveries.  Output: list of (t, S, part, mode) with mode in {'in', 'full', 'part'} and the reader map.
usage: ltopP.py SYSTEM.json OUT.json [time]"""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lw import V, g, bits, closure, FULL
from ortools.sat.python import cp_model
HYP = g.HYP
pc = lambda m: bin(m).count('1')
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
TL = float(sys.argv[3]) if len(sys.argv) > 3 else 600
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
def pm(m):
    r = FULL
    for s in bits(m): r &= HYP[s]
    return r
RT = {}
def rt(S):
    r = RT.get(S)
    if r is None:
        r = 0
        for u in bits(S):
            if any(C & ~S == 0 for C in cells_of[u]): r |= 1 << u
        RT[S] = r
    return r
planes = set()
for t in range(V):
    for e in range(V):
        if e != t: planes.add(closure((1 << t) | (1 << e)))
planes = sorted(planes)
sec = {Q: pm(Q) for Q in planes}
print('planes', len(planes), flush=True)
M = cp_model.CpModel()
IN, DF, DP = {}, {}, {}
for Q in planes:
    for t in bits(Q):
        IN[t, Q] = M.NewBoolVar(''); DF[t, Q] = M.NewBoolVar(''); DP[t, Q] = M.NewBoolVar('')
        M.AddAtMostOne([IN[t, Q], DF[t, Q], DP[t, Q]])
byt = collections.defaultdict(list)
for Q in planes:
    for t in bits(Q): byt[t].append(Q)
for t in range(V):
    M.Add(sum(IN[t, Q] for Q in byt[t]) <= 1)
    R = HYP[t]
    for u in bits(R):
        full_terms = [IN[t, Q] for Q in byt[t] if rt(sec[Q]) >> u & 1] + [DF[t, Q] for Q in byt[t] if rt(sec[Q]) >> u & 1]
        if len(full_terms) > 1: M.Add(sum(full_terms) <= 1)
        M.AddBoolOr(full_terms + [DP[t, Q] for Q in byt[t] if rt(sec[Q]) >> u & 1])
# pairing: t in-chain on Q => some co-user e of Q delivers Q in full mode; DF only if someone reads it
for Q in planes:
    ls = bits(Q)
    for t in ls:
        M.AddBoolOr([IN[t, Q].Not()] + [DF[e, Q] for e in ls if e != t])
        M.AddBoolOr([DF[t, Q].Not()] + [IN[e, Q] for e in ls if e != t])
deliveries = sum(DF.values()) + sum(DP.values())
M.Minimize(deliveries)
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M)
print('status', sv.StatusName(st), 'deliveries', sv.ObjectiveValue(), 'bound', sv.BestObjectiveBound(), flush=True)
out = []
for t in range(V):
    R = HYP[t]; fulls = []; partials = []
    for Q in byt[t]:
        S = sec[Q]
        if sv.Value(IN[t, Q]): out.append([t, hex(S), hex(rt(S)), 'in', hex(Q)]); fulls.append(S)
        elif sv.Value(DF[t, Q]): out.append([t, hex(S), hex(rt(S)), 'full', hex(Q)]); fulls.append(S)
        elif sv.Value(DP[t, Q]): partials.append(S)
    rest = R
    for S in fulls: rest &= ~rt(S)
    asg = collections.defaultdict(int)
    for u in bits(rest):
        S = max([S for S in partials if rt(S) >> u & 1], key=lambda S: pc(rt(S) & rest))
        asg[S] |= 1 << u
    for S, m in asg.items(): out.append([t, hex(S), hex(m), 'part', None])
json.dump(out, open(sys.argv[2], 'w'))
modes = collections.Counter(o[3] for o in out)
print('modes', dict(modes), 'deliveries', modes['full'] + modes['part'])
