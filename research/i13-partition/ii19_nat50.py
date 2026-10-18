"""THE P111 vs E8 GEOMETRY (ii19_nat50.py) — is the frontier's system an E8-subset?!

THE PATH (the +20.12% target (the nat49!!)): the frontier word (the r434 (the concentrated
shape!!)) EXTENDED from v=111 to the E8-120 (the +9 lines (the own8/ext4 channel class!!!)).
HERE: (1) the pub word's lines (the 111!!); (2) the comparison with the E8-240/120; (3) the
subset verdict + the missing-lines identification (the +9!!); (4) the junk/perp-structure
preview of the extension (the new targets' perps vs the old!!).
"""
import json, itertools
from collections import Counter
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

# (1) the published P111's lines
w = json.load(open('ii19_pub2_p111-r434.json', 'rt'))
V, H = w['v'], w['h']
L = [[Fraction(x) for x in l] for l in w['lines']]
log('THE PUBLISHED P111-R434: v %d | h %d | the lines %d-dim' % (V, H, len(L[0])))
norms = Counter(sum(x * x for x in l) for l in L)
log('  the norms: %s' % {str(k): v for k, v in sorted(norms.items(), key=lambda kv: str(kv[0]))})
# the scale: the E8-roots norm 2; the P111's norms?? (the scaling freedom!!)
# (2) the E8-240 (the standard!!) + the match-test (mod scaling/sign!!)
roots = set()
for i, j in itertools.combinations(range(8), 2):
    for si, sj in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        v = [0] * 8
        v[i] = si; v[j] = sj
        roots.add(tuple(v))
for s in itertools.product([1, -1], repeat=8):
    if sum(s) % 4 == 0:
        roots.add(tuple(Fraction(x, 2) for x in s))
roots = sorted(roots)
log('  the E8-240: %d roots' % len(roots))

def canon(v):
    v = list(v)
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)

# the P111's lines vs the E8: the ip-structure preservation (the scaling-invariant test!!):
# the P111's pairwise ips vs the E8's: the pattern-match (the norm/ip-ratios!!)
ips = Counter()
for s in range(V):
    for t in range(s + 1, V):
        ip = sum(L[s][i] * L[t][i] for i in range(H))
        ips[ip] += 1
log('  the P111 ip-structure: %s' % {str(k): v for k, v in sorted(ips.items(), key=lambda kv: str(kv[0]))})
# the perps
PERP = [set(s for s in range(V) if s != t and sum(L[s][i] * L[t][i] for i in range(H)) == 0) for t in range(V)]
log('  the P111 perps: %s' % dict(sorted(Counter(len(p) for p in PERP).items())))
# (3) the embedding test: try to match each P111 line to an E8-root (mod scale + sign + basis!!)
# the simplest: the norm/ip ratio structure: the E8's subset would show ips in {0, +-1/2-norm...}
n0 = norms.most_common(1)[0][0]
log('  the dominant norm: %s | the ip/norm ratios: %s' % (str(n0), {str(k): v for k, v in sorted(Counter(ips).items(), key=lambda kv: str(kv[0]))}))
