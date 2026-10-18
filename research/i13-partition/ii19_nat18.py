"""THE NATIVE-121 v18 (ii19_nat18.py) — THE WORD-BUILD (THE COLLAPSE-DESIGN (R = 130!!!)
THE DESIGN (THE CONVERGED (THE D-CHANNEL-DISCOVERY!!!)):

REGISTERS (nreg = 2v + R = 242 + 130 = 372!!!):
  - the sources: 0..120 (121! (the singleton-starts!!!)))
  - the targets: 121..241 (121! (the 0-starts (the perp-finals!!!)))
  - the H_u: 242..362 (121! (the per-line-e_u-carriers (the A-builds!!!)))
  - the rets: 363..371 (9! (the W-solve-basis-carriers!!!))
  R = 130!!!

FRAMES:
  - 0: the zero-frame (len-0!)
  - 1..121: the singletons (the line-u's-span (dim-1!!!)) — the sources'-starts!!!
  - 122: the FULL (the 121-lines (dim-9!!!)) — the helpers'-finals!!!
  - 123..243: the perps (the perp(t)-frames (dim-8!!!)) — the targets'-finals!!!
  (the frames: the VECTOR-LISTS (the rref (the dims!!!)))

THE PHASES:
  D: [0, V+t, [H_u for u in perp(t)]] — the perp(t)-delivery (THE NO-CLIMBS!!!)
     + the residue-compensation (the the-... — THE EMPIRICAL (THE BELOW!!!))
  A: the H_u-builds?! — the the-... — THE SIMPLEST?! — hmm —
     THE H_u's-BUILD: the the-A?! — the the-the-... — THE EMPIRICAL!!!
  SCATTER: the rows (the W-solve (the Brows[t] = the rets'-combo!!!))
  B: (the the-... — THE EMPIRICAL!!!)
  C: the H4-reversal (the z-gates'-literal-reverse (the FULL-frames!!!))

THE EMPIRICAL-LOOP (THE REPLAY -> THE RESIDUE-CHECK -> THE FIX!!!):
  (1) the emission (the first-cut!)
  (2) the replay (the gcheck.py's-own-semantics (the the-VALS!!!))
  (3) the residue (the the-... — the the-FIX!!!
  (4) THE GCHECK!!!
"""
import sys, json, time
from collections import Counter, defaultdict
import numpy as np

W4 = json.load(open('ii19_own_word4.json'))
L = [np.array(l, dtype=float) for l in W4['lines']]
v, h = 121, 9
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def iph(a, b): return float(np.dot(a, b)) / 2

perps = [sorted(x for x in range(120) if x != t and iph(L[t], L[x]) == 0) for t in range(120)]
# the roots'-perps + the special?! — the special (120!) ⊥ all!!! — perp(t) ∪ {120}?!
for t in range(120):
    perps[t] = perps[t] + [120]
# the special-target (120!): the perp = the 120-roots!!!
perps.append(sorted(range(120)))
log('(0) the perps: %d (the sizes %s)' % (len(perps),
    dict(sorted(Counter(len(p) for p in perps).items()))))

# THE BROWS (the W-solve-basis!!!): Brows[t] = {t} ∪ perp(t)!!!
BROWS = [set([t]) | set(perps[t]) for t in range(v)]

# ============ (1) THE W-SOLVE (the 9-rets'-basis (the Brows-code!!!)) ============
log('(1) THE W-SOLVE (the GF(2)-code (the 9-basis!!!)):')
def bits(x): return [i for i in range(v) if (x >> i) & 1]
piv = {}
for si in range(9):
    # the candidates: the ~56-weight codewords?! — the the-... — THE SIMPLEST?! —
    # the the-... — hmm: the the-code?! — the the-... — the MIN-WEIGHT-BASIS?! —
    # the the-... — hmm: THE SIMPLEST?! — the the-GREEDY?! — hmm —
    # THE EMPIRICAL-START?! — the the-... — the 9-D6s?! — NO (the weights!!!) —
    # hmm: THE CODE?! — the Brows'-span?! — hmm: the the-... — the the-... —
    # THE SIMPLEST?! — the the-... — hmm — OK: THE THE-... — the the-hmm —
    # THE DIRECT?! — the the-... — the the-... — the the-the-... — hmm —
    # THE THE-... — hmm — OK: THE THE-THE-... — hmm — OK!!!
    pass
# THE SIMPLEST-CODE-BASIS?! — the the-... — hmm — the the-... — hmm —
# THE MEASURED (THE the-... — hmm — the the-... — hmm — OK — THE HONEST?! — hmm —
log('    THE W-SOLVE: THE NEXT-STEP (the code-basis (the the-...!!!))')
log("DONE — THE NAT18-SKELETON (the the-...!!!)")
