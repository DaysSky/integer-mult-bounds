"""THE NATIVE-121 v11 (ii19_nat11.py) — THE WORD4's-USAGE-CENSUS (THE BACKWARD-REACHABILITY!!)
THE PRACTICAL-PATH (THE GCHECK (THE NOW!!!)): the word4 (THE GCHECK-PASSED (THE R=471!!!))
-> THE BACKWARD-CLOSURE (the targets'-finals (the transitively-load-bearing-registers!!!))
-> THE DEAD-REGISTERS (the unused (the shave (THE R-DOWN (THE PRICE (THE GCHECK-REPLAY!!!))))
"""
import sys, json, time
from collections import Counter
import numpy as np
from mpmath import mp
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

FRONTIER = 0.001744386
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

W4 = json.load(open('ii19_own_word4.json'))
V, H = W4['v'], W4['h']
nreg = len(W4['start'])
R4 = W4['R']
log('the word4: v=%d h=%d R=%d nreg=%d' % (V, H, R4, nreg))
log('    the gates: D=%d A=%d B=%d C=%d' % (
    len(W4['D']), len(W4['A']), len(W4['B']), len(W4['C'])))

# ============ (1) THE BACKWARD-REACHABILITY (the load-bearing-registers!!) ============
# THE SEEDS: the targets (V..2V-1: the finals'-holders!!) + the rets (the scatter!!!)
# + the sources (the finals'-holders (the own-bits!!!))
seeds = set(range(V, 2 * V)) | set(W4['ret']) | set(range(V))
# THE BACKWARD-CLOSURE: the gates (the D/A/B (the dests'-reached => the srcs'-reached!!!))
# + the scatter (the targets (the rets!!!)) + the C (the Z-RESTORES (the srcs'-reached!!!
# (the H4 (the zg-reversal (the SAME-srcs!!!))))
reached = set(seeds)
changed = True
while changed:
    changed = False
    # the A/B-gates: the dest-reached -> the srcs-reached!!
    for F, d, srcs in W4['A'] + W4['B']:
        if d in reached:
            for s in srcs:
                if s not in reached:
                    reached.add(s); changed = True
    # the D-gates: the dest-reached -> the srcs (the srcs' SELF-BITS (the D-delivery!!!))
    for F, d, srcs in W4['D']:
        if d in reached:
            for s in srcs:
                if s not in reached:
                    reached.add(s); changed = True
    # the C-gates: the dest-reached -> the srcs (the restores!!!
    for F, d, srcs in W4['C']:
        if d in reached:
            for s in srcs:
                if s not in reached:
                    reached.add(s); changed = True
dead = [r for r in range(nreg) if r not in reached]
log('(1) THE LOAD-BEARING: %d/%d | THE DEAD: %d (the %s..)' % (
    len(reached), nreg, len(dead), dead[:20]))
# the dead'-composition: the helpers?! (the >= 2V?!)
dead_helpers = [r for r in dead if r >= 2 * V]
dead_targets = [r for r in dead if V <= r < 2 * V]
dead_sources = [r for r in dead if r < V]
log('    the dead: the helpers %d | the targets %d | the sources %d' % (
    len(dead_helpers), len(dead_targets), len(dead_sources)))

# ============ (2) THE FORWARD-DEAD-CHECK (the never-written-and-never-read?! ) ============
# the honest-dead: the not-reached (the backward) — the second-check: the forward-usage
# (the gates'-appearances (the dests-or-the-srcs!!!))
appears = set()
for F, d, srcs in W4['D'] + W4['A'] + W4['B'] + W4['C']:
    appears.add(d)
    appears.update(srcs)
never = [r for r in range(nreg) if r not in appears and r not in set(W4['ret'])]
log('(2) THE NEVER-APPEARING: %d (the %s..)' % (len(never), never[:20]))
log('DONE — THE NAT11 (the usage-census!!!)')
