"""Dead-minimizer v1: LP lower bound + greedy primal for the PG(2,3) 610-demand instance.

Model (7c pool accounting, exact at that level):
- A demand E (at frame S) is served by a DISJOINT set cover {A_1..A_k} of E by candidate flats inside S
  (flat-sum semantics: A_i partition E as line sets).
- Cost: each used candidate flat A with |A| >= 1 lines costs 1 register IF it is a leaf (built at the bottom
  as a sum of line copies: cost 1 like a line copy, already inside the 2v branches when |A| = 1, else +1).
  A formed pool (any used flat fed by >= 2 other used flats) with k inputs costs (k - 1) dead (the merge).
  Total = sum over used flats of (1 if leaf else (inputs - 1)) + (extra for demanded XOR-combinations).
- v1 LP: choose for each demand one cover from a menu (its candidate flats + the demand itself as one piece),
  minimise sum over flats of max(1, uses_in_internal_structure).  Simplify to the honest core:
    dead = sum over non-leaf used flats (k_A - 1), leaf flats free (they are the branch registers),
           + 1 register per used flat that serves as an assembled input (non-single-line flat).
  So the objective = sum over used flats A of (1 if |A| > 1 else 0) + sum over internal pools (k-1).
  v1 counts the first term exactly and approximates the second by pool-sharing (a flat used by c demands
  as a *formed* piece costs 1 + (c >= 2 ? 1 : 0) ... we take the cleaner upper model:
    cost(A) = 1 for every used flat with |A| > 1 (it must exist as a register) — sharing across demands is
    free (one register, many readers), which is the zero-waste ideal; and dead = #used non-leaf flats.
  This is the standard set-cover-with-sharing LP and is a LOWER bound on the true dead only if pools never
  pay merges; we also run a k-bounded variant that adds merge costs for flats whose covers use >= 2 pieces.
"""
import os, pickle, sys, time, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

D = pickle.load(open(os.path.join(HERE, 'deadmin_instance.pkl'), 'rb'))
cand_set = set(D['cand']); dem_cand = D['dem_cand']; part = D['part']; DEM = D['DEM_kind']
log('instance loaded: cands %d demands %d' % (len(cand_set), len(dem_cand)))

sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g13 = Geom(13)
rk_cache = {}
def rkof(A):
    if A not in rk_cache: rk_cache[A] = g13.closure(A)[1] if A else 0
    return rk_cache[A]

# distinct demands with their frames
ddem = sorted(set(E for k, S, E in DEM))
frame_of = {}
for k, S, E in DEM: frame_of.setdefault(E, S)
log('distinct demands', len(ddem))

# candidates restricted per demand; also index: for each demand, which candidates are SINGLE lines (leaf-0-cost)
V = g13.V
single = {1 << i for i in range(V)}

# Build cover menus: for demand E, menu entries are disjoint-set covers of E.  Enumerating all is huge;
# restrict to covers of size <= KMAX built greedily from largest candidates + exact small covers via DP.
KMAX = 4
from functools import lru_cache
def covers_of(E, S_cands, kmax=KMAX, limit=400):
    """DFS disjoint covers of E by candidates (each candidate used once per cover)."""
    out = []
    Ebits = [i for i in range(V) if E >> i & 1]
    # order: candidates sorted by size desc
    cl = sorted(S_cands, key=lambda A: -bin(A).count('1'))
    def rec(rem, chosen, start):
        if len(out) >= limit: return
        if rem == 0:
            out.append(tuple(chosen)); return
        if len(chosen) >= kmax: return
        # first uncovered line must be covered by some candidate containing it
        u = (rem & -rem).bit_length() - 1
        for A in cl:
            if A >> u & 1 and A & ~rem == 0 and A not in chosen:
                rec(rem & ~A, chosen + [A], 0)
                if len(out) >= limit: return
    rec(E, [], 0)
    return out

menus = {}
t1 = time.time()
for n, E in enumerate(ddem):
    S = frame_of[E]
    cands = [A for A in dem_cand[E]]
    # candidates that are single lines of E are always available; ensure E itself excluded (>= 2 pieces)
    cv = covers_of(E, cands)
    # add the trivial 1-piece cover if E itself is a candidate (it is: frames were included)
    if E in cand_set and (rkof(E) <= 10): cv.insert(0, (E,))
    menus[E] = cv
    if n % 100 == 0: log('menu %d/%d entries %d %.0fs' % (n, len(ddem), len(cv), time.time() - t1))
log('menus built: total covers', sum(len(v) for v in menus.values()), 'mean', sum(len(v) for v in menus.values())/len(menus))
pickle.dump(menus, open(os.path.join(HERE, 'deadmin_menus.pkl'), 'wb'))
cnt = collections.Counter(len(v) for v in menus.values())
log('menu size histogram (bottom 12):', sorted(cnt.items())[:12])
zero = [E for E, v in menus.items() if len(v) == 0]
log('demands with NO cover:', len(zero))
if zero[:3]:
    for E in zero[:3]:
        log('  example no-cover demand: size', bin(E).count('1'), 'frame rank', rkof(frame_of[E]))
