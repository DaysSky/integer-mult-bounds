"""THE IDENTITY-WORD EXPERIMENT — the decisive cheap test of the format's true legality floor.
B = I (the trivial decoder): each target receives its own line's value via one retained
register; NO phase-B reads; the D-phase pre-reads cancel the scattered dirt by doubling.
Manual gcheck tracing says every check passes (D/A/scatter/B/C, H1-H5, content-frame,
mass identity 8x120 + 120 + 2x120x7 = 2760).  If gcheck PASSES this, the frontier is
trivially beatable (R = v helpers!) and the whole economics re-opens; if it REJECTS,
the rejection reason pins the true constraint that governs every sparse decoder.
Usage: builds word JSON then calls gcheck.main() directly."""
import sys, json, itertools
import numpy as np

sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/tword')

roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
d8 = {}
for r in list(roots) + half: d8[canon(r)] = np.array(r)
L = np.array(list(d8.values()))
V = len(L)
h = 8
print('E8 system: %d lines' % V)

# frames: 0 = empty; 1..V = the singletons; V+1 = FULL; V+2.. = the t-perps
frames = [[]]
start = [0] * (2 * V + V)          # placeholders; sources set below
for s in range(V):
    frames.append([[float(x) for x in L[s]]])
FULL = [[1.0 if i == j else 0.0 for j in range(h)] for i in range(h)]
frames.append(FULL)
fidx_full = len(frames) - 1
tperp = []
for t in range(V):
    perp = [s for s in range(V) if s != t and abs(float(L[s] @ L[t])) < 1e-9]
    basis = []
    for s in perp:
        vec = L[s]
        if any(abs(float(np.array(b) @ vec)) > 1e-9 for b in basis):
            continue
        basis.append(vec)
        if len(basis) == h - 1: break
    assert len(basis) == h - 1, (t, len(basis))
    frames.append([[float(x) for x in b] for b in basis])
    tperp.append(len(frames) - 1)

nreg = 2 * V + V   # sources, targets, helpers (the retained = the helpers)
start = [0] * nreg
final = [0] * nreg
for s in range(V):
    start[s] = 1 + s                 # the source s at its singleton frame
    final[s] = fidx_full
for t in range(V):
    start[V + t] = 0                # targets at the empty frame
    final[V + t] = tperp[t]
for q in range(2 * V, nreg):
    start[q] = 0
    final[q] = fidx_full

# gates
D = []
for t in range(V):
    q = 2 * V + t
    D.append([0, V + t, [q]])       # frame 0, write target t, read helper q (the dirt pre-read)
A = []
for s in range(V):
    q = 2 * V + s
    A.append([1 + s, q, [s]])       # at the singleton frame {s}: helper q ^= source s
ret = [2 * V + s for s in range(V)]
ret_frames = [1 + s for s in range(V)]
scatter = [[t] for t in range(V)]   # target t scatters ret[t] (its own helper)
B = []
C = [[fidx_full, d, [s]] for (_, d, [s]) in reversed(A)]  # the literal reverse at FULL

w = dict(
    h=h, v=V, R=V,
    form=dict(num=[[1 if i == j else 0 for j in range(h)] for i in range(h)], den=1),
    lines=[[float(x) for x in L[s]] for s in range(V)],
    frames=frames, start=start, final=final,
    D=D, A=A, B=B, C=C,
    ret=ret, ret_frames=ret_frames, scatter=scatter,
)
path = '/private/var/folders/cg/9jd0z3791rv0t784bs323m7m0000gn/T/opencode/e8_identity_word.json'
import os
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'wt') as f:
    json.dump(w, f)
print('word written: %s (R = %d helpers)' % (path, V))

from gcheck import main
try:
    out = main(path, do_price=True)
    print('GCHECK VERDICT:')
    print(json.dumps(out, indent=1, default=str))
except Exception as e:
    print('REJECT:', e)
    sys.exit(1)