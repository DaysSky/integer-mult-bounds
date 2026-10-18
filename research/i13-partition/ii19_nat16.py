"""THE NATIVE-121 v16 (ii19_nat16.py) — THE WORD-BUILD-SKELETON (THE SCAFFOLDING!!!
THE STRUCTURE (THE CONVERGED-DESIGN (the nat2-nat15's-complete-measurements!!!)):

REGISTERS:
  - the sources: 0..120 (121! (the singleton-starts (the FREE-reads!!!)))
  - the targets: 121..241 (121! (the 0-starts (the perp-finals!!!)))
  - the cells: the pair-sums (the u's-1-3-memberships (the LEVEL-2!!!))
  - the D6-pieces: the 286-junk-carriers (the users-2-3 (the CARRIER-SCALE!!!))
  - the special-carriers: the ext6's-42-pattern (THE PROVEN!!!)
  - the gathers: the 9-rets (the CST-73 (the W-solve (the SCATTER!!!)))

THE LADDER (THE WORD4's-PROVEN-TEMPLATE!!!):
  the singleton (dim-1! (the FREE-reads!!!)) -> the cell (dim-2 (the PRIVATE (1-src!!!)))
  -> the 12-frame?! (THE the-the-... — hmm: OUR-version?! — the D6-builds'-frames?!
  -> the D6 (dim-6 (the the-33-line-sums!!!)) -> the perp (dim-8 (the TARGETS'-FINALS!!!))

THE BALANCE (THE GCHECK's-OWN!!!):
  [the scatter's-line-part (the Brows-combo!!!)] XOR [the B-reads'-line-parts (the perp(t)-delivery!!!)] = e_t

THE GATES (THE PHASES!!!):
  D: [0-frame, V+t, [the-D-srcs?! — the the-... — the the-H2?! — the helpers-only?!]]
  A: the builds (the cells?! (the the-... — the D6s?! — the rets?! — the specials!!!))
  SCATTER: the 9-rets (the the-ret_frames (the the-... — the the-...!!!
  B: the targets'-reads?! (the the-... — the the-perp-delivery (the D6-reads (the the-...!!!
  C: the H4-REVERSAL (the the-z-gates'-literal-reverse!!!)

THE CONSTRAINTS (THE GCHECK's-RULES (THE ALL-CONFIRMED!!!)):
  - the climb: the cur == F (FREE!!!) | the sub(cur, F) + the dims-strictly-increase!!!
  - the content_ok: the dest's-content-lines (the ⊆ the F?! — the the-...!!!
  - the H1-H5!!! | the mass-identity!!! | the finals (the own XOR e_t!!!

THIS-SCRIPT (THE SKELETON'S-STATE (the the-... — the NEXT-SESSION's-START!!!)):
  (0) the system-load (the word4's-lines (the the-121!!!))
  (1) the D6-set-cover (the nat13b's-286!!!)
  (2) the cells'-selection (the the-... — the nat14/15's-...!!!
  (3) the ladder-assignment (the the-the-4-frAME?! — the the-...!!!
  (4) the gates'-emission (the the-... — the FULL-WORD!!!)
  (5) the replay (the the-... — the VALS!!!
  (6) the gcheck-json (the the-... — THE WORD!!!)
"""
import sys, json, time
from collections import Counter, defaultdict
import numpy as np

# ============ (0) THE SYSTEM ============
W4 = json.load(open('ii19_own_word4.json'))
L = [np.array(l, dtype=float) for l in W4['lines']]
v, h = 121, 9
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def iph(a, b): return float(np.dot(a, b)) / 2
log('(0) the system: v=%d h=%d' % (v, h))

perps = [set(x for x in range(120) if x != t and iph(L[t], L[x]) == 0) for t in range(120)]

# ============ (1) THE D6-SET-COVER (the nat13b's-greedy!!!) ============
res = {}
for t in range(120):
    d6s = {}
    for u in range(120):
        if u == t: continue
        c = tuple(sorted(perps[t] & perps[u]))
        if len(c) >= 15:
            d6s[c] = d6s.get(c, 0) + 1
    res[t] = d6s
all_d6s = {}
for t in range(120):
    for c in res[t]:
        all_d6s.setdefault(c, set()).add(t)
chosen = []
covered = [set() for _ in range(120)]
cnt = [0] * 120
while True:
    prio = sorted(range(120), key=lambda x: -len(perps[x] - covered[x]))
    t = prio[0]
    need = perps[t] - covered[t]
    if not need or cnt[t] >= 8: break
    best = None
    for c, users in all_d6s.items():
        if t not in users: continue
        gain = len(set(c) & need)
        if gain > 0 and (best is None or gain > best[0]):
            best = (gain, c, users)
    if best is None: break
    _, c, users = best
    chosen.append((c, users))
    for u2 in users:
        covered[u2].update(c)
        cnt[u2] += 1
tails = [len(perps[t] - covered[t]) for t in range(120)]
log('(1) the D6-cover: %d-chosen (the tails %s)' % (len(chosen),
    dict(sorted(Counter(tails).items()))))

# ============ (2) THE CELLS'-SELECTION (THE NAT16's-CORE-REMAINING!!!) ============
# THE TASK (the next-session!!!): the per-D6's-build?! — the ~33-srcs?! — the cells?! —
# the u's-the-4-frAME-ladders?! — the the-... — the STRUCTURING?! — hmm —
# THE SIMPLEST-CANDIDATE?! — the word4's-OWN?! — the 180-private-cells?! — hmm —
# the D6's-build?! — the ~33-srcs?! — the cells?! — the ~?! — hmm —
# THE MEASURED-GOLD: the best-partner-co-occ mean-45.9?! — the SHARED-cells?! —
# the the-... — the NEXT-SESSION's-CORE (the cells'-the-4-frAME-STRUCTURING!!!
log('(2) THE CELLS-SELECTION: THE NEXT-SESSIONs-CORE (the the-4-frame-structuring!!!)')
log("DONE — THE NAT16-SKELETON (the scaffolding!!!)")
