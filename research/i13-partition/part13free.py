"""No-symmetry partition of I_{13,1} lines into good 4-frames: exact cover, 70,785 frames / 364 lines."""
import os, pickle, collections, sys
from ortools.sat.python import cp_model
import base13 as B

g, V = B.g, B.V
HERE = os.path.dirname(os.path.abspath(__file__))
fr = pickle.load(open(os.path.join(HERE, 'goodframes13.pkl'), 'rb'))

# rows: line -> list of (frame, its 3 orthogonal mates) is implicit; model each frame as a set of 4 lines
model = cp_model.CpModel()
x = [model.NewBoolVar(f'f{i}') for i in range(len(fr))]
# per line: exactly 1 frame
line_frames = [[] for _ in range(V)]
for i, F in enumerate(fr):
    for s in g.bits(F): line_frames[s].append(i)
print('max frames per line', max(len(lf) for lf in line_frames), 'min', min(len(lf) for lf in line_frames))
for s in range(V):
    model.AddExactlyOne([x[i] for i in line_frames[s]])
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = float(os.environ.get('TMAX', '900'))
solver.parameters.num_search_workers = 8
st = solver.Solve(model)
print('no-symmetry partition:', solver.StatusName(st), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    chosen = [F for i, F in enumerate(fr) if solver.Value(x[i])]
    cover = collections.Counter()
    for F in chosen:
        for s in g.bits(F): cover[s] += 1
    print('frames', len(chosen), 'cover counts', dict(collections.Counter(cover.values())))
    kinds = collections.Counter()
    for F in chosen:
        kinds[sum(1 for s in g.bits(F) if g.kind[s] == 'P')] += 1
    print('P-count census of chosen frames', dict(kinds))
    pickle.dump(sorted(chosen), open(os.path.join(HERE, 'partition13.json' if False else 'partition13.pkl'), 'wb'))
