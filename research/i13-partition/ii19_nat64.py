"""THE P111-SYSTEM IDENTITY (ii19_nat64.py) — the frontier word's own geometry!!

THE PROGRAM-DEFINING QUESTION: the frontier (ii19_pub2_p111-r434.json!!) IS the II19-family
published word — WHAT IS ITS LINE-SYSTEM?! (1) the 111 lines' norms/ip-structure/perps;
(2) THE IDENTITY: a pure E8-subset?! a Lorentzian section?! the (alpha, a)-class?!;
(3) THE EXTENSION MAP: if the P111 C= a bigger family system (the 120/125/130-line
SUPERSETS (the v-sweep's +13-20% targets!!!)) — the ON-PROGRAM verdict!!!
"""
import json, itertools, sys
from collections import Counter
from fractions import Fraction
import numpy as np
log = lambda *a: print(*a, file=sys.stderr, flush=True)

w = json.load(open('ii19_pub2_p111-r434.json', 'rt'))
V, H = w['v'], w['h']
L = [[Fraction(x) for x in l] for l in w['lines']]
log('THE PUBLISHED P111-R434: v %d | h %d | the ambient %d | R %d' % (V, H, len(L[0]), w['R']))
log('  the form: %s' % w.get('form', 'NONE?!'))
norms = Counter(sum(x * x for x in l) for l in L)
log('  THE NORMS: %s' % {str(k): v for k, v in sorted(norms.items(), key=lambda kv: str(kv[0]))})
ips = Counter()
for s in range(V):
    for t in range(s + 1, V):
        ips[sum(L[s][i] * L[t][i] for i in range(H))] += 1
log('  THE IP-STRUCTURE: %s' % {str(k): v for k, v in sorted(ips.items(), key=lambda kv: str(kv[0]))})
PERP = [set(s for s in range(V) if s != t and sum(L[s][i] * L[t][i] for i in range(H)) == 0) for t in range(V)]
log('  THE PERPS: %s' % dict(sorted(Counter(len(p) for p in PERP).items())))
# the form-field (if present!!): the signature?!
if 'form' in w:
    Fm = w['form']
    log('  the form field: %s' % str(Fm)[:200])
# the span/rank!!
A = np.array([[float(x) for x in l] for l in L])
log('  THE SPAN RANK: %d (h %d!!)' % (np.linalg.matrix_rank(A), H))
# the E8-subset test: the P111's lines vs the E8-roots (mod scale/sign!!)!!
roots = set()
for i, j in itertools.combinations(range(8), 2):
    for si, sj in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        v = [0] * 8
        v[i] = si; v[j] = sj
        roots.add(tuple(v))
for s in itertools.product([1, -1], repeat=8):
    if sum(s) % 4 == 0:
        roots.add(tuple(Fraction(x, 2) for x in s))

def canon(v):
    v = list(v)
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)

rset = {canon(r) for r in roots}
log('  THE E8-240: %d canonical roots' % len(rset))
# the P111's lines: 8-dim?! (h=8!!) — project to 8 + the match!!
match = 0; nomatch = []
for l in L:
    c = canon(tuple(l[:8]))
    if c in rset:
        match += 1
    else:
        nomatch.append(l)
log('  THE E8-MATCH: %d/%d lines are canonical E8-roots (the first 8 coords!!)' % (match, V))
if nomatch:
    log('    the non-matching (the first 5): %s' % [list(map(str, l)) for l in nomatch[:5]])
