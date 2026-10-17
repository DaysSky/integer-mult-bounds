"""I_{11,1} cell bottleneck screen.  Frame graphs: each line a picks a good 4-frame F_a ∋ a, symmetric adjacency
(b ∈ F_a <=> a ∈ F_b), invariant under the group (env GRP=55 H55, GRP=11 Z11).  MODE part: F_b = F_a for all b ∈ F_a
(partition into 55 frames); MODE nonpart: no line whose 3 neighbours all share its frame (MAXSAME=0).
Per cell C={s,a}: doubly forced targets T_C (free top: t ⊥ s,a and no other cell of s or of a inside t-perp; frame
top additionally: C inside one of t's own frame sections); a node N = closure(C+x) (nondegenerate) serves t iff
N ⊂ t-perp (free) / N inside a C-containing own-frame section of t (frame).  k_C = |T_C| - max served.
Bound: cells keeping 2 registers need k_C distinct cell readers (<= 220) -> sum j_C >= 330 - max coverable;
R >= 440 + sum j_C."""
import sys, json, random, collections, pickle
from lbase import *
from ortools.sat.python import cp_model
MODE = sys.argv[1]; seed = int(sys.argv[2]); n = int(sys.argv[3]); random.seed(seed)
fr = goodframes()
fr_of = {a: [F for F in fr if F >> a & 1] for a in range(V)}
frset = set(fr)
M = cp_model.CpModel()
Y = {(a, F): M.NewBoolVar('') for a in range(V) for F in fr_of[a]}
for a in range(V):
    M.AddExactlyOne([Y[(a, F)] for F in fr_of[a]])
for p in PERMS:
    for (a, F), y in Y.items():
        M.Add(y == Y[(p[a], act(F, p))])
for a in range(V):
    for b in orth[a]:
        if a < b:
            M.Add(sum(Y[(a, F)] for F in fr_of[a] if F >> b & 1) == sum(Y[(b, F)] for F in fr_of[b] if F >> a & 1))
if MODE == 'part':
    for a in range(V):
        for F in fr_of[a]:
            for b in bits(F):
                if b != a: M.AddImplication(Y[(a, F)], Y[(b, F)])
else:
    for a in range(V):
        for F in fr_of[a]:
            M.AddBoolOr([Y[(a, F)].Not()] + [Y[(b, F)].Not() for b in bits(F) if b != a])
def screen(Fa):
    adj = {a: [b for b in bits(Fa[a]) if b != a] for a in range(V)}
    cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in adj[a]))
    cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
    own = {t: [perp((1 << t) | (1 << f)) for f in adj[t]] for t in range(V)}
    res = {'free': [], 'frame': []}
    for C in cells:
        s, a = list(bits(C))
        Tf = [t for t in range(V) if C & ~HYP[t] == 0 and not any(c != C and c & ~HYP[t] == 0 for c in cells_of[s] + cells_of[a])]
        Nodes = []
        for x in range(V):
            if C >> x & 1: continue
            N = closure(C | (1 << x))
            if nondeg_span(N): Nodes.append(N)
        Nodes = set(Nodes)
        best = max([sum(1 for t in Tf if N & ~HYP[t] == 0) for N in Nodes] + [0])
        res['free'].append((len(Tf), len(Tf) - best))
        # frame top: t's routes only via own-frame sections
        Tr = []
        for t in range(V):
            if C & ~HYP[t]: continue
            Ds = own[t]
            rs = [(D, c) for D in Ds for c in cells_of[s] if c & ~D == 0]
            ra = [(D, c) for D in Ds for c in cells_of[a] if c & ~D == 0]
            if rs and ra and all(c == C for _, c in rs) and all(c == C for _, c in ra): Tr.append([D for D, _ in rs])
        bestr = max([sum(1 for Ds in Tr if any(N & ~D == 0 for D in Ds)) for N in Nodes] + [0])
        res['frame'].append((len(Tr), len(Tr) - bestr))
    out = {}
    for k, v in res.items():
        free0 = sum(1 for x, y in v if y == 0)
        ks = sorted(y for x, y in v if y > 0); pool = V; cnt = 0
        for kk in ks:
            if pool >= kk: pool -= kk; cnt += 1
        out[k] = (dict(collections.Counter(x for x, y in v)), dict(collections.Counter(y for x, y in v)), len(cells) - free0 - cnt)
    return len(cells), out
for k in range(n):
    M.Maximize(sum(random.randint(0, 100) * v for v in Y.values()))
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = 300; sol.parameters.num_workers = 2
    sol.parameters.random_seed = seed * 100 + k
    r = sol.Solve(M)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): print(MODE, 'no graph', sol.StatusName(r), flush=True); break
    Fa = {a: next(F for F in fr_of[a] if sol.Value(Y[(a, F)])) for a in range(V)}
    ncell, out = screen(Fa)
    print(MODE, 'graph', k, 'cells', ncell, flush=True)
    for top, (hT, hk, bound) in out.items():
        print('   %s top: |T_C| %s  k_C %s  => sum j_C >= %d  => R >= %d' % (top, hT, hk, bound, 440 + bound), flush=True)
    json.dump({str(a): Fa[a] for a in range(V)}, open('lfg_%s_%d_%d.json' % (MODE, seed, k), 'w'))
