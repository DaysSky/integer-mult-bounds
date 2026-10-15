"""Exact Z11 parts layer for a design: sel.json {rep: cover index or [index, ...]} -> det.json (sel + assignment,
in-chain choice, hosted flags) for lr8nodecost.py / lr8midlb.py.  Honours env POOL, FAITH, XOR, MID of lr8z11.py.
usage: lr8mkdet.py sel.json det.json"""
import sys, json
inp, out = sys.argv[1], sys.argv[2]
sys.argv = ['x']; sys.path.insert(0, '.')
import lr8z11 as Z
d = json.load(open(inp)); sel = [d[str(r)][0] if isinstance(d[str(r)], list) else d[str(r)] for r in Z.reps]
val, det = Z.solve(sel, TL=60, workers=2, want=True)
print('cost orbits', val, det['status'])
json.dump({'sel': {str(r): sel[ri] for ri, r in enumerate(Z.reps)}, 'det': det}, open(out, 'w'))
