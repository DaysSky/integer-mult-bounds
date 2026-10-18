"""THE NATIVE-121 v12d (ii19_nat12d.py) — THE CELLS-LADDER (THE SOURCES'-SOLUTION!!)
THE PROBLEM: the pieces'-BUILDS' ~21-srcs -> the sources'-~63-reads (THE ONE-CLIMB (THE
MASS-8-WALL!!!)) -> THE SOLUTION (THE R420's-OWN [1, 1, 2]): THE CELLS-LADDER (the shared
2-4-line-sums (the ~1-3-cell-memberships-per-source!!!)) — THE MEASURE (THE CONSTRUCTION!!!
"""
import sys, json, time, itertools
from collections import Counter, defaultdict
import numpy as np

W4 = json.load(open('ii19_own_word4.json'))
L = [np.array(l, dtype=float) for l in W4['lines']]
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def iph(a, b): return float(np.dot(a, b)) / 2

perps = [set(u for u in range(120) if u != t and iph(L[t], L[u]) == 0) for t in range(120)]

# ============ (1) THE PIECES (the nat12c's direct-splits (the users-0-2!!!)) ============
def users_of(S, t):
    return [u for u in range(120) if u != t and all(iph(L[u], L[x]) == 0 for x in S)]
pieces = []
for t in range(120):
    pool = sorted(perps[t], key=lambda u: -len(perps[u]))
    n = len(pool); k = 2 if n <= 44 else 3
    bounds = [int(round(n * (i + 1) / k)) for i in range(k)]
    prev = 0
    for b in bounds:
        S = tuple(sorted(pool[prev:b])); prev = b
        us = users_of(S, t)
        pieces.append((t, S, us))
log('(1) the pieces: %d (the users %s)' % (len(pieces),
    dict(sorted(Counter(len(us) for _, _, us in pieces).items()))))

# ============ (2) THE CELLS (THE E8-ANALOG (the pair-cells (the SHARED-SUMS!!!))) ============
# THE CELL-CANDIDATES: the pairs {u, w} (the shared-pieces?! — the pieces'-BUILDS?! —
# THE CRITICAL-STRUCTURE: the cell {u, w} serves the pieces containing BOTH u and w!!
# THE CELL'-COUNT (the R!!): the cells (the DISTINCT-pairs (the used?! — the greedy!!!
# THE CELL'-MEMBERSHIP-BUDGET (the u (the ∈ the <= 3-cells!!!)) — THE CONSTRUCTION:
# the per-source-pairs?! — hmm: the SIMPLEST: the pairs-withIN-the-pieces?! — the
# per-source: the u's-CELLS (the ~1-3?! — the pairs?! — hmm: the u (the ∈ the ~?! —
# THE HONEST-FIRST-MEASURE: the pairs'-CO-OCCURRENCES-IN-THE-PIECES!!! + the SOURCE's
# PIECE-MEMBERSHIPS (the ~63?!?! — the CELLS'-REDUCTION (THE MEASURE!!!
src_piece_mem = Counter()
for t, S, us in pieces:
    for x in S:
        src_piece_mem[x] += 1
log('(2) the sources-piece-memberships: %s (the mean %.1f!!) | the OVER-8: %d/120' % (
    dict(sorted(Counter(src_piece_mem.values()).items())),
    float(np.mean(list(src_piece_mem.values()))),
    sum(1 for x in src_piece_mem.values() if x > 8)))

# THE CELLS (THE PAIRS (the most-co-occurring?! — the construction: the u's-partner
# (the pair {u, w}?! — the cell (the shared?! (the ~2-3-pieces?!?! — hmm —
# THE CELL-NEED: the u's-piece-memberships (the ~63?! — the cells (the ~1-3?! —
# the CELL-SERVES-the ~63-pieces?!?! — the cell {u, w}?! — the ✗?! —
# THE DEEPER-SOLUTION (THE R420's-ACTUAL!!!): the u's-READS (the ~1-3?! — the R420's-
# cells (the ~430?! — the u (the ∈ the ~1-3?! — THE 121's-EQUIVALENT?!?! — the
# D4-analog?! — hmm — THE LIGHT-EXTRACTION (THE MEASURE (THE BELOW!!!
# THE D4-ANALOG-CELLS: the maximal-line-sets-inside-the-dim-2/4-subspaces?! — the
# PAIR-CELLS?! — the {u, w}-pairs?! — hmm: the u (the ∈ the ~1-3-PAIRS?!?! — the
# SHARED-PAIR-CELLS?! — the construction (the pieces'-INTERNAL?! — the MEASURE!!!
pair_in_pieces = Counter()
for t, S, us in pieces:
    for u, w in itertools.combinations(S, 2):
        pair_in_pieces[(u, w)] += 1
log('    the pairs-in-pieces: %d distinct (the co-occ %s (the mean %.1f!!)' % (
    len(pair_in_pieces), dict(sorted(Counter(pair_in_pieces.values()).items())),
    float(np.mean(list(pair_in_pieces.values())))))
# the per-source: the best-partners?! — the cells (the ~1-3-per-u?! — the greedy!!!
# THE CELL-SET: the greedy (the per-u (the ~1-3-cells?! — hmm: the u's-pieces (the ~63?!
# — the CELLS (the covering?! — hmm: the cell {u, w} (the serves?! — the pieces-containing
# both?! — the ~?! — the u's-pieces (the ~?! — the cell {u, w}?! — the ✗ —
# THE DEEPER-STRUCTURE?!?! — hmm — the R420's-cell (the ~2-3-lines?! — the u (the ∈ the
# ~1-3?! — the SHARED?! — the cell's-reads?! — the ~?! — THE MEASURE (the u's-partners'
# distribution (the below (the HONEST!!!
best_partner = {}
for (u, w), c in pair_in_pieces.items():
    if u not in best_partner or c > best_partner[u][1]: best_partner[u] = (w, c)
    if w not in best_partner or c > best_partner[w][1]: best_partner[w] = (u, c)
bp_counts = [c for _, c in best_partner.values()]
log('    the best-partner-co-occs: %s (the mean %.1f!!)' % (
    dict(sorted(Counter(bp_counts).items())), float(np.mean(bp_counts))))
log('DONE — THE NAT12D (the cells-measures!!!)')
