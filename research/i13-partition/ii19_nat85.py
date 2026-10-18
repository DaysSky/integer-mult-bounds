"""THE LADDER-WORD AT THE FULL R (ii19_nat85.py) — the mass across the root!!

THE §748's LADDERED PASS (R = 174 (the hist {1: 309, 2: 51, 3: 180, 4: 72, 5: 189,
6: 69, 7: 120} (the mass 3,438!!)) + THE +100 DUPLICATES (the own-class at the RAISED
RUNGS (the [RUNG[l], q', [l]] (the block-3!!)) -> R = 274 | THE PRICE-TRIAL!!!
"""
import os, sys, json
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

w = json.load(open('ii19_ext120_ladder2.json', 'rt'))
V, h = w['v'], w['h']
frames = w['frames']
F_FULL = 1
old_R = w['R']
old_nreg = len(w['start'])
n_extra = 100
# the duplicates' RUNGS = the own-helpers' ret_frames (the raised A-ENDS!!)
ret_frames = w['ret_frames']
new_start = list(w['start']) + [0] * n_extra
new_final = list(w['final']) + [F_FULL] * n_extra
NP = old_R - V            # 54
own_base = 2 * V + NP     # the original own-helpers' base!!
# the A: the block-3 (the own-builds (the dests >= own_base in the last 120 gates!!)
A = list(w['A'])
block3 = A[-V:]
assert all(d >= own_base for _, d, _ in block3), 'the block-3 shape!!'
dup_gates = []
for j in range(n_extra):
    l = j % V
    q = old_nreg + j
    dup_gates.append([ret_frames[l], q, [l]])
A2 = A + dup_gates
C = [[F_FULL, d, srcs] for (_, d, srcs) in reversed(A2)]
w2 = dict(w)
w2['R'] = old_R + n_extra
w2['start'] = new_start
w2['final'] = new_final
w2['A'] = A2
w2['C'] = C
path = 'ii19_ext120_ladder_full.json'
with open(path, 'wt') as f:
    json.dump(w2, f)
log('THE WORD WRITTEN: %s (R = %d!!)' % (path, w2['R']))
from gcheck import main
try:
    out = main(path, do_price=True)
    log('THE GCHECK VERDICT:')
    print(json.dumps(out, indent=1, default=str))
except Exception as e:
    log('REJECT: %s' % e)
    sys.exit(1)
