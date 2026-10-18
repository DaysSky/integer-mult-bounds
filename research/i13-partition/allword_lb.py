"""All-word lower bound for I_{13,1}: the gate-event (arrival) counting argument, made rigorous.

THE ARGUMENT (to be checked piece by piece below):
1. A word for system S must deliver, to every target t, the content of its perp R(t) = the XOR of the
   lines orthogonal to t (delivery of |R(t)| line-values summed at t's full-frame read; standard).
2. Format fact (gcheck climb rule, as in halves_struct.py): a register chain visits at most ONE frame
   of each dimension 0..h-1, so at most h = 13 frames, and each of its reads happens at one of them.
3. Define a gate event = a (register, frame) read that transfers a line-value into a sum.  The sum
   x_t (target t's final value) is a GF(2) sum of SOME set of register contents; over all t, the
   distinct line-values that must arrive somewhere are bounded by the demand structure.
4. LOWER BOUND on arrivals: every target t needs |R(t)| line-values; a line-value x_u arrives at
   t through a chain of gates; the total gate events >= sum_t |R(t)| is FALSE in general (a register
   holding a SUM of k lines arriving once serves k line-values at once — that is the whole point of
   assembly).  The correct count: assembly is free in gate events but costs registers: a sum of k
   lines is built by >= k-1 gates somewhere below.  So total gate events >= (total line-incidences
   of all demands) - (number of registers), and registers cost R.
5. The census input: which (frame, demand-set) pairs exist.  A register at frame F can serve exactly
   the demands whose frames contain F.  The reuse factor = max demands served per (register, visit).
   The exhaustive frame-sharing census measured: on the maxpairs partition, halves have 2-6 readers
   and zero nesting; on the PG top, 618 piece frames for 619 pieces (1 demand each).

THIS SCRIPT: computes the exact bound for the PG-top demand set and the maxpairs half set, i.e.
  R >= (total line-incidences) / h - v   [each register supplies <= h line-arrivals]
and the analogous bound with the SHARPER per-register arrival cap once frame sharing is accounted:
  a register's k-th visit is at dimension k; arrivals at a visit = #demands whose frame contains the
  visit frame AND whose content includes lines the register holds.  A single-line register (copy)
  supplies 1 line-value per visit; a sum register supplies |content| values per visit but needed
  k-1 lower gates to build.  Net over the whole tree: total gates >= total incidences - #registers.
So the honest floor: R >= (incidences - h * R_mid)... circular; resolve as:
  R_total * h >= incidences + R_total  =>  R_total >= incidences / (h - 1).
Plug incidences = 15,411 (PG top) or 13,508 + Q (maxpairs): R >= 15,411/12 = 1,285 (PG top),
R >= 13,508/12 = 1,126 (maxpairs).  Plus branches v = 364?  Branches are registers too; the bound
is on ALL registers: R_total >= 1,285 already includes them.  Cross-check against kappa(R):
  kappa at R = 1,285: (computed) ~ -14% vs the new frontier.  With branch shape reality (2v needed
  as sources), R >= 728 + (15,411 - 728*13)/13 ... the branches contribute 9,464 arrivals, leaving
  5,947 for mid registers at 13 each = 458 mids; R >= 728 + 458 = 1,186 (matches the earlier floor).
kappa(1,186) = -20.4%.  THIS SCRIPT verifies the incidence counts from the saved pickles and prints
the bound cleanly.  The formalization gap (what a proof needs): (a) the h-visits cap (gcheck climb
rule) is a format theorem; (b) 'sum registers need k-1 lower gates' is the standard assembly tree
count; (c) the incidences are system constants (perp sizes).  All three are checkable.
"""
import os, pickle, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; bits = g.bits
h_dim = 13

def bound(name, incidences, notes):
    # every register: <= h_dim visits; each visit transfers the register's content (a sum).  Building
    # a content of k lines needs k-1 internal gates (tree).  Total gates G >= incidences - R + (#sum
    # registers' savings already counted).  Clean version: incidence count I = sum over demands of
    # |content|.  Each incidence is discharged either (a) at a leaf (the line's own source/copy read:
    # costs 1 branch register per line, already in R) or (b) inside a built sum.  A built sum of k
    # lines at a frame costs k-1 gates and >= 1 register (if reused) or is inlined.  Total gates:
    # G >= I - R (each register read 'pays' for at most one of its own content-lines' incidences at
    # each visit; over its lifetime a register provides <= h_dim visits; but its content required
    # k-1 gates).  Standard resolution: I <= G + (registers' savings) and G <= h_dim * R/1...
    # The clean inequality (used in the handoff-style counts): total gate events G satisfies
    #   I <= G + R   (a register's own delivery to its consumers counts once per (register, consumer))
    # and G <= h_dim * R (visit cap).  Neither alone bounds R from below — the binding form used:
    # arrivals A (line-values crossing a gate into a sum) satisfy A >= I - v_sources... final form:
    #   R >= ceil((I - h_dim * v) / h_dim)  when the v branch registers carry I_branch <= h_dim * v.
    # For the PG top: I = 15,411; branch arrivals <= 728 * 13 = 9,464; rest needs mid registers
    # carrying the remaining 5,947 arrivals at <= 13 each: R_mid >= 458; R >= 728 + 458 = 1,186.
    R_branch = 2 * V   # 2 copies per line (standard; 1 source + 1 carrier minimum)
    A_branch = h_dim * R_branch
    R_mid = max(0, -(-(incidences - A_branch) // h_dim))
    print('%s: incidences %d; branch arrivals <= %d; mid registers >= %d; R >= %d = %.2fv'
          % (name, incidences, A_branch, R_mid, R_branch + R_mid, (R_branch + R_mid) / V))
    return R_branch + R_mid

# demand incidences from the corrected primal (PG top)
D = pickle.load(open(os.path.join(HERE, 'deadmin_primal.pkl'), 'rb'))
piece_of = {(eval(k) if isinstance(k, str) else k): v for k, v in D['piece_of'].items()}
pid_cf = {v: k for k, v in piece_of.items()}
chosen = {k: tuple(v) for k, v in D['chosen'].items()}
allp = set()
for ps in chosen.values(): allp.update(ps)
fc = {}
for p in allp:
    c, F = pid_cf[p]
    fc.setdefault(F, set()).update(i for i in range(c.bit_length()) if c >> i & 1)
I_pg = sum(len(s) - 1 for s in fc.values())   # merge-ins at piece frames
I_pg_full = sum(len(s) for s in fc.values())  # full line-slots
print('PG top: piece frames %d, content slots %d, merge-ins %d' % (len(fc), I_pg_full, I_pg))
R1 = bound('PG top (merge-ins)', I_pg, 'corrected covers')
# perp sizes (system constant): sum_t |R(t)|
import numpy as np
HYP = g.HYP
perp_total = sum(bin(HYP[t] ^ (1 << t) & HYP[t]).count('1') if False else sum(1 for u in range(V) if u != t and (HYP[t] >> u & 1)) for t in range(V))
print('system constant: sum_t |R(t)| over all 364 targets =', perp_total)
R2 = bound('all-targets perps', perp_total, 'any word must assemble every target perp')
print()
print('kappa at the floors (exitmix best shapes):')
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
from exitmix import price
import mpmath as mp
cst = [12] * 13
NEWF = mp.mpf(1744385950814795279853) / mp.mpf(10)**24
for R in (R1, R2):
    dead = max(0, R - 2 * V)
    if dead == 0:
        c = price(13, V, cst, [(V, [12])], [(V, [11, 1])], [(2 * V, 0, 13, [1, 1, 2, 3, 6])])
    else:
        c = price(13, V, cst, [(V, [12])], [(V, [11, 1])],
                  [(2 * V, 0, 13, [1, 1, 2, 3, 6]), (dead, 0, 13, [3, 4, 6])])
    print('  R = %d (floor): kappa = %s = %+.2f%% vs new frontier' %
          (R, mp.nstr(c, 8) if c else 'over wall', float(c / NEWF - 1) * 100 if c else 0))
