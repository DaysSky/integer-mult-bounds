"""THE cst-SEARCH (ii19_nat89.py) — the dim-7-supported gather families!!!

THE nat88's VERDICT: the row-space's nonzero elements ALL span dim 8 (the 511!!) — the
naive 9-gather basis sits at FULL (cst = 72 (the R420's own!!)). BUT the gathers' vals
need NOT be row-space elements: ANY family whose GF(2) span contains all B0[t] works —
and the natural dim-7-supported candidates are THE PERP-PATTERNS perp(t) (the 63-line
sets (each inside its OWN dim-7 perp-frame!!!))!! THE SEARCH:
(1) the perp-pattern family's span vs the B0-span (the rank + the containment!!);
(2) the minimal dim-7-supported families (the perp-patterns + their XORs-INSIDE-frames...)
    spanning all B0[t] — the cst = Σ dims (the 9-dim-7 = 63!!! / 10-dim-7 = 70 / mixed!!);
(3) the FALLBACK ladder: k dim-7 + (9−k) FULL gathers — the cst menu (63+8j!!).
"""
import os, sys, json, itertools
from collections import Counter
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
lines = [tuple(int(x) for x in l) for l in SPEC['lines']]
V = len(lines)
PERP = [set(p) for p in SPEC['PERP']]
B0 = [sum(1 << s for s in ({t} | PERP[t])) for t in range(V)]
def bits(x): return [s for s in range(V) if (x >> s) & 1]

def gf2_rank_rows(rows):
    M = list(rows); rr = 0
    for c in range(V):
        p = next((i for i in range(rr, len(M)) if (M[i] >> c) & 1), None)
        if p is None: continue
        M[rr], M[p] = M[p], M[rr]
        for i in range(len(M)):
            if i != rr and ((M[i] >> c) & 1): M[i] ^= M[rr]
        rr += 1
    return rr, M[:rr]

# (1) THE PERP-PATTERNS' SPAN
Pp = [sum(1 << s for s in PERP[t]) for t in range(V)]
rP, rrefP = gf2_rank_rows(Pp)
rB, rrefB = gf2_rank_rows(B0)
log('(1) THE SPANS: rank{perp-patterns} = %d | rank{B0} = %d' % (rP, rB))
# containment: every B0 in span{P}?
def in_span(v, rref_rows):
    for r in rref_rows:
        if (v >> (r.bit_length() - 1)) & 1 if False else False: pass
    # reduce v by the rref
    w = v
    for r in rref_rows:
        pb = r.bit_length() - 1
        if (w >> pb) & 1: w ^= r
    return w == 0
cont = all(in_span(B0[t], rrefP) for t in range(V))
contP = all(in_span(Pp[t], rrefB) for t in range(V))
log('    B0 ⊆ span{perp-patterns}: %s | perp ⊆ span{B0}: %s' % (cont, contP))

# (2) THE DIM-7-SUPPORTED FAMILY SEARCH (the perp-patterns themselves!!)
if cont:
    log('\n(2) THE 9-DIM-7 FAMILY (cst = 63!!!): a basis of span{P} ∩ (dim-7-supported!!):')
    # basis from the perp-patterns directly (they are dim-7-supported by construction!!)
    sel = []
    for t in range(V):
        if len(sel) == rB: break
        if in_span(Pp[t], [x for x in sel]) and False: pass
        # greedy independent extension
        cand = sel + [Pp[t]]
        rr, _ = gf2_rank_rows(cand)
        if rr == len(cand): sel.append(Pp[t])
    rr, _ = gf2_rank_rows(sel)
    log('    the greedy perp-basis: %d elements (rank %d)' % (len(sel), rr))
    # the W-solve: each B0[t] = XOR of which sel-elements?
    # reduce B0[t] against the sel in ORDER (the sel is a basis; solve by reduction)
    def solve(v, basis):
        combo = []
        w = v
        for b in basis:
            pb = b.bit_length() - 1
            if (w >> pb) & 1:
                w ^= b; combo.append(b)
        return combo if w == 0 else None
    okall = True
    Wt = []
    for t in range(V):
        c = solve(B0[t], sorted(sel, key=lambda x: -x.bit_length()))
        if c is None: okall = False; break
        Wt.append([sel.index(x) for x in c])
    log('    the W-solve over the perp-basis: %s | the W-weights: %s'
        % (okall, dict(sorted(Counter(len(w) for w in Wt).items())) if okall else '-'))
    if okall:
        json.dump({'basis': sel, 'W': Wt}, open('ii19_nat89_cst63.json', 'wt'))
        log('    SAVED ii19_nat89_cst63.json — THE cst=63 FAMILY (9 dim-7 perp-frames!!!)')
else:
    log('\n(2) THE PERP-FAMILY FAILS (B0 ⊄ span{perp-patterns}) — the mixed search:')
    # the mixed families: perp-patterns + B0-elements... and the XORs perp(t)^perp(u)?
    # candidate pool: all perp-patterns + all B0 + pairwise XORs that stay dim-7-supported?
    # (the XOR of two perp-patterns: perp(t) Δ perp(u) — supported on perp(t) ∪ perp(u) — dim-8-ish!!)
    # the honest fallback menu:
    log('    THE FALLBACK: k dim-7 + (9-k) FULL: cst = 7k + 8(9-k) = 72 - k')

# (3) THE FALLBACK MENU + the price map at each cst
from pricer import price
from mpmath import mp
from collections import Counter as Ctr
TARGET = {1: 1010, 2: 1038, 3: 53, 4: 34, 5: 79, 6: 9, 7: 15}
def synth(R, cst, tmpl):
    mass = 8 * R + cst + 2 * V * 7
    d = Ctr(tmpl); d[1] += mass - sum(r * z for r, z in d.items())
    return dict(d)
log('\n(3) THE cst-MENU PRICE MAP (R=174 and R=200 and R=250!!):')
for cst in (63, 70, 71, 72):
    row = []
    for R in (174, 200, 250):
        c, prof, d = price(synth(R, cst, TARGET), V, 8, R)
        row.append('R=%d: %s' % (R, mp.nstr(c, 8) if c is not None else 'NO-ROOT'))
    log('  cst=%2d  %s' % (cst, ' | '.join(row)))
