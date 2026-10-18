"""THE NATIVE-121 v12 (ii19_nat12.py) — THE ~30-LINE PIECES (THE COVERAGE-SCALE!!)
THE word4's-own-30-frame-scale: the pieces (the ~21-34-lines!!) (the users (the ~1-8?! (the
carrier-scale-LEGAL!!!))) -> the per-target (the ~2-3-pieces (the <= 8-steps!!!)) + the sources'
piece-memberships (the ONE-CLIMB!!!) — THE BUDGETS (THE MEASURED (THE HONEST!!!))
"""
import sys, json, time, itertools
from collections import Counter
import numpy as np
from mpmath import mp
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

W4 = json.load(open('ii19_own_word4.json'))
L = [np.array(l, dtype=float) for l in W4['lines']]
V, H, n = 121, 9, 9
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def iph(a, b): return float(np.dot(a, b)) / 2

perps = [[u for u in range(120) if u != t and iph(L[t], L[u]) == 0] for t in range(120)]

log('(1) THE ~30-LINE-PIECES (the top-down (the perp-splits (the carrier-scale!!!))):')
pieces = []
covered = [set() for _ in range(120)]
def users_of(S, t):
    return [u for u in range(120) if u != t and all(iph(L[u], L[x]) == 0 for x in S)]
for t in range(120):
    pool = list(perps[t])
    while pool:
        S = []
        pool.sort(key=lambda u: -len(perps[u]))
        for u in pool:
            if len(S) >= 34: break
            S2 = S + [u]
            us = users_of(S2, t)
            if len(us) <= 8:
                S = S2
        if not S:
            S = [pool[0]]
        us = users_of(S, t)
        key = tuple(sorted(S))
        pieces.append((key, sorted(us)))
        for u2 in us:
            covered[u2].update(S)
        Sset = set(S)
        pool = [u for u in pool if u not in Sset]
pieces = [(S, us) for S, us in pieces if S]
tail_sizes = [len(set(perps[t]) - covered[t]) for t in range(120)]
log('    the pieces: %d (the sizes %s (the mean %.1f!!))' % (
    len(pieces), dict(sorted(Counter(len(S) for S, _ in pieces).items())),
    float(np.mean([len(S) for S, _ in pieces]))))
log('    the users: %s (the mean %.1f!!)' % (
    dict(sorted(Counter(len(us) for _, us in pieces).items())),
    float(np.mean([len(us) for _, us in pieces]))))
log('    the tails: %s (the mean %.1f!!)' % (
    dict(sorted(Counter(tail_sizes).items())), float(np.mean(tail_sizes))))
log('    the per-target-pieces: %s (the mean %.1f!!) | the OVER-8: %d/120' % (
    dict(sorted(Counter(sum(1 for S, us in pieces if t in us) for t in range(120)).items())),
    float(np.mean([sum(1 for S, us in pieces if t in us) for t in range(120)])),
    sum(1 for t in range(120) if sum(1 for S, us in pieces if t in us) > 8)))
src_mem = Counter()
for S, us in pieces:
    for x in S:
        src_mem[x] += 1
log('    the sources-piece-memberships: %s (the mean %.1f!!) | the OVER-8: %d/120' % (
    dict(sorted(Counter(src_mem.values()).items())), float(np.mean(list(src_mem.values()))),
    sum(1 for x in src_mem.values() if x > 8)))
log('DONE — THE NAT12 (the coverage-scale-budgets!!!)')
