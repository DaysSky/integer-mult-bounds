"""T-TRIANGLE DESIGN (pure combinatorics on 11 points).  A triangle node = 3 pairwise disjoint triples {A,B,C}
(frame {T(A),T(B),T(C)}, rank 3, perp 37 = A2(A)+A2(B)+A2(C)+P(E)+27 transversal T lines, E = the 2 leftover
points; all three T lines can use it).  For a T line T(A) a 4-cover of R(T(A)) by triangle nodes through A is exactly:
every pair of D = [11]-A lies inside a block (B, C or E) of some node [P lines] and across B x C of some node
[T lines (a,d,d')].  Find 220 nodes with every triple in exactly 4 of them, each triple's 4 nodes forming such a
cover: then every T line has a 4-cover by nodes used by ALL their users (perfect T sharing, 220 nodes for 660 uses).
usage: lttri_design.py timelimit [Z11]"""
import sys, itertools, json, time
from ortools.sat.python import cp_model
TL = float(sys.argv[1]); Z = len(sys.argv) > 2; t0 = time.time()
P11 = range(11)
triples = list(itertools.combinations(P11, 3))
cands = set()
for A in triples:
    rest = [x for x in P11 if x not in A]
    for B in itertools.combinations(rest, 3):
        r2 = [x for x in rest if x not in B]
        for C in itertools.combinations(r2, 3):
            cands.add(tuple(sorted((A, B, C))))
cands = sorted(cands); print('candidate triangle nodes', len(cands), flush=True)
M = cp_model.CpModel(); z = [M.NewBoolVar('') for _ in cands]
if Z:   # Z11 symmetry: node and its rotations share a variable
    def rot(node, k): return tuple(sorted(tuple(sorted((x + k) % 11 for x in T)) for T in node))
    idx = {c: i for i, c in enumerate(cands)}
    for i, c in enumerate(cands):
        j = idx[rot(c, 1)]
        if j != i: M.Add(z[i] == z[j])
by_triple = {A: [] for A in triples}
for i, c in enumerate(cands):
    for T in c: by_triple[T].append(i)
for A in triples:
    M.Add(sum(z[i] for i in by_triple[A]) == 4)
    D = [x for x in P11 if x not in A]
    for p in itertools.combinations(D, 2):
        within = []; cross = []
        for i in by_triple[A]:
            B, C = [T for T in cands[i] if T != A]
            E = tuple(x for x in D if x not in B and x not in C)
            if (p[0] in B and p[1] in B) or (p[0] in C and p[1] in C) or p == E: within.append(z[i])
            elif (p[0] in B and p[1] in C) or (p[0] in C and p[1] in B): cross.append(z[i])
        M.Add(sum(within) >= 1); M.Add(sum(cross) >= 1)
print('model built %.0fs' % (time.time() - t0), flush=True)
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M); print('status', sv.StatusName(st), '%.0fs' % (time.time() - t0), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = [cands[i] for i in range(len(cands)) if sv.Value(z[i])]
    print('nodes', len(sol)); json.dump(sol, open('lttri_design%s.json' % ('_z11' if Z else ''), 'w'))
