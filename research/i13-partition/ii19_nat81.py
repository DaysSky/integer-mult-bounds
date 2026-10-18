"""THE R-INFLATION TRIAL (ii19_nat81.py) — the mass across the root threshold!!

THE §657's PASS (R = 174 (the mass 3,192 (the no-root!!!))) + THE +100 DUPLICATE
OWN-HELPERS (the [SINGLE[l], q', [l]] (the A+C self-only class ✓✓✓ (the proven!!)))
-> R ~ 274 | the mass ~ 3,992 (THE ROOT-REGIME?!?! (THE VERIFIED C!!!)).
"""
import os, sys, json
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

w = json.load(open('ii19_ext120_interim.json', 'rt'))
V, h = w['v'], w['h']
frames = w['frames']
SINGLE_F = {}   # the singleton-frame per source (from the ret_frames (the own-helpers!!))
ret_frames = w['ret_frames']
for t, rf in enumerate(ret_frames):
    SINGLE_F[t] = rf
n_extra = 100
old_R = w['R']
old_nreg = len(w['start'])
# the new helpers: the duplicates at [old_nreg, old_nreg + n_extra)
new_start = list(w['start']) + [0] * n_extra
new_final = list(w['final']) + [0] * n_extra
F_FULL = 1
for q in range(old_nreg, old_nreg + n_extra):
    new_final[q] = F_FULL
# the A: the block-1 (the singleton-reads): the duplicates' builds ([SINGLE[l], q', [l]])
# — l = q - old_nreg (the line-index!!!) — the block-2 (the PF-climbs!!) stays AFTER!!
block1 = []
block2 = []
seen_pf = False
for gi, (F, d, srcs) in enumerate(w['A']):
    # the interim's A: the block-1 (the singleton-frames (dim 1!!)) then the block-2 (PFs)
    # — distinguish by the srcs' count + the dest (the own-helpers (the pieces...)))
    block1.append([F, d, srcs])
# the honest split: the interim's A-order: the first (NP + V) gates = the block-1
# (the §657's (the 174 singleton-reads!!)) — recompute: the pieces (54!!) + the own (120!!)
NP = old_R - V    # 54
b1_count = NP + V  # 174
new_block1 = list(w['A'])[:b1_count] + \
    [[SINGLE_F[q - old_nreg], q, [q - old_nreg]] for q in range(old_nreg, old_nreg + n_extra)]
new_block2 = list(w['A'])[b1_count:]
newA = new_block1 + new_block2
newC = [[F_FULL, d, srcs] for (_, d, srcs) in reversed(newA)]
w2 = dict(w)
w2['R'] = old_R + n_extra
w2['start'] = new_start
w2['final'] = new_final
w2['A'] = newA
w2['C'] = newC
path = 'ii19_ext120_rinf.json'
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
