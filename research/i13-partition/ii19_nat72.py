"""THE FIRST GCHECK RUN (ii19_nat72.py) — the extension-system trivial word!!

THE TEMPLATE (e8_identity_word.py (the gcheck-PASSING format!!)): the trivial decoder
(B = I!!): each target receives its own line's value via ONE retained; the D pre-reads
cancel the scattered dirt; NO B-reads; the C reversal at FULL.  ADAPTED: the v=120
EXTENSION system (the {0,+-2}-class (the P111's own form (num I, den 2!!!)) + the nat69
frames (the singletons + FULL + the t-perps (ALL NONDEGENERATE ✓✓!!))).
THE VERDICT: GCHECK RUNS (the format's floor at the extension!!!).
"""
import os, sys, json, itertools
from collections import Counter
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
lines = [tuple(int(x) for x in l) for l in SPEC['lines']]
V = len(lines)
h = 8
log('THE EXTENSION SYSTEM: v %d | the norms %s' % (
    V, dict(sorted(Counter(sum(x * x for x in l) for l in lines).items()))))

# the frames (nat69's!!): 0 = empty; 1 = FULL; the singletons; the t-perps!!
frames = [[]]
frames.append([[1 if i == j else 0 for j in range(h)] for i in range(h)])   # 1 = FULL
fidx_full = 1
SINGLE = []
for s in range(V):
    frames.append([[x for x in lines[s]]])
    SINGLE.append(len(frames) - 1)
TPERP = SPEC['TPERP']
for t in range(V):
    frames.append(SPEC['frames'][TPERP[t]])

nreg = 3 * V
start = [0] * nreg
final = [0] * nreg
for s in range(V):
    start[s] = SINGLE[s]
    final[s] = fidx_full
for t in range(V):
    start[V + t] = 0
    final[V + t] = TPERP[t]
for q in range(2 * V, nreg):
    start[q] = 0
    final[q] = fidx_full

D = []
for t in range(V):
    q = 2 * V + t
    D.append([0, V + t, [q]])
A = []
for s in range(V):
    q = 2 * V + s
    A.append([SINGLE[s], q, [s]])
ret = [2 * V + s for s in range(V)]
ret_frames = [SINGLE[s] for s in range(V)]
scatter = [[t] for t in range(V)]
B = []
C = [[fidx_full, d, [s]] for (_, d, [s]) in reversed(A)]

w = dict(
    h=h, v=V, R=V,
    form=dict(num=[[1 if i == j else 0 for j in range(h)] for i in range(h)], den=2),
    lines=[[float(x) for x in lines[s]] for s in range(V)],
    frames=frames, start=start, final=final,
    D=D, A=A, B=B, C=C,
    ret=ret, ret_frames=ret_frames, scatter=scatter,
)
path = 'ii19_ext120_trivial.json'
with open(path, 'wt') as f:
    json.dump(w, f)
log('THE WORD WRITTEN: %s (R = %d helpers!!)' % (path, V))

from gcheck import main
try:
    out = main(path, do_price=True)
    log('THE GCHECK VERDICT:')
    print(json.dumps(out, indent=1, default=str))
except Exception as e:
    log('REJECT: %s' % e)
    sys.exit(1)
