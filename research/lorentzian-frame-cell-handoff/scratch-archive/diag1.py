import sys, json
sys.argv = ['x']
sys.path.insert(0, '.')
import lr8z11 as Z
from ortools.sat.python import cp_model
d = json.load(open('lr8poolmip2_opt.json')); sel = [d[str(r)][0] for r in Z.reps]
for ri in range(Z.NR):
    M, hosted, cin, A = Z.solve(sel, force=ri, only=True)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 20; st = sv.Solve(M)
    r = Z.reps[ri]
    print(ri, r, Z.KIND[r], Z.SUPP[r], 'alone-hostable:', sv.StatusName(st), flush=True)
