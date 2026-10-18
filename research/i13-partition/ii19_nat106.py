"""THE FOREST-V2 EMITTER (ii19_nat106.py) — THE SHARED-PATH PROTOCOL!!!

THE LAST PIECE: the targets CLUSTERED by perp-overlap (the co-groups!!) -> per
cluster ONE shared rung-ladder (the rich-4s inside the common-perp (the ⊥-
chains!!!)) -> every (target, wire)-read at the cluster's LOWEST rung ⊇ home_w ->
THE WIRES' CHAINS through the shared nodes (nested (the cluster-tree!!!)) ->
the dup-fills ONLY at the cross-cluster stragglers -> THE EMIT -> GCHECK!!!
"""
import os, sys, json
from collections import Counter, defaultdict
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
V = len(SPEC['lines'])
LINES = [tuple(int(x) for x in l) for l in SPEC['lines']]
W_SC = [list(map(int, w)) for w in SPEC['W']]
PERP = [set(p) for p in SPEC['PERP']]
B0 = [sum(1 << s for s in ({t} | PERP[t])) for t in range(V)]
PM = [sum(1 << s for s in PERP[t]) for t in range(V)]
pc = lambda x: x.bit_count()

def rref(rows, n=8):
    m = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]
def spans(vs): return len(rref([list(x) for x in vs]))

DES = json.load(open('ii19_nat104_design.json', 'rt'))
kept = [tuple(p) for p in DES['pieces']]
T_BASE = [[tuple(x) for x in b] for b in DES['bases']]
T_FILL = [set(f) for f in DES['fills']]
PMASK = {p: sum(1 << s for s in p) for p in kept}

fmap = {}; flist = []
def fidx(basis):
    key = tuple(tuple(r) for r in basis)
    if key not in fmap:
        fmap[key] = len(flist); flist.append(key)
    return fmap[key]
def spf(idx): return rref([list(LINES[i]) for i in idx])
EMPTY = fidx([]); FULL = fidx(rref([list(x) for x in LINES]))
SINGLE = [fidx(spf([s])) for s in range(V)]
TPERP = [fidx(spf(sorted(PERP[t]))) for t in range(V)]
_fmask = {}
def fmask(bi):
    if bi in _fmask: return _fmask[bi]
    B = flist[bi]; m = 0
    for s in range(V):
        if spans(list(B) + [list(LINES[s])]) == len(B): m |= (1 << s)
    _fmask[bi] = m
    return m
def fdim(bi): return len(flist[bi])

# ---------------- the readers ----------------
readers = defaultdict(list)
for t in range(V):
    for p in T_BASE[t]: readers[('P', p)].append(t)
    for s in T_FILL[t]: readers[('S', s)].append(t)

# ---------------- (1) THE TARGET CLUSTERS (the perp-overlap co-groups!!) ----------------
# the canonical targets: the perps' structure: cluster by the mutual ⊥ (t ⊥ t'?!)
CL = []          # the clusters (the lists of targets!!)
unassigned = set(range(V))
while unassigned:
    seed = min(unassigned)
    # the cluster: the targets sharing a big perp-overlap with the seed!!
    cl = [seed]
    for t in sorted(unassigned):
        if t == seed: continue
        ov = pc(PM[seed] & PM[t])
        if ov >= 40:                    # the strong overlap (the co-⊥!!
            cl.append(t)
    for t in cl: unassigned.discard(t)
    CL.append(cl)
log('the clusters: %d (the sizes %s)' % (len(CL), dict(sorted(Counter(len(c) for c in CL).items()))))

# ---------------- (2) THE SHARED RUNG-LADDERS (per cluster!!) ----------------
# the cluster's ladder: the shared rungs R_1 ⊂ R_2 ⊂ ... ⊆ ∩perp(cluster)!!
# the rungs: the ⊥-extensions inside the cluster's common perp (the dims 2,3,4,5!!)
CL_LADDER = []
for cl in CL:
    common = None
    for t in cl:
        common = PM[t] if common is None else (common & PM[t])
    cdim = 8 - len(rref([list(LINES[t]) for t in cl])) if len(cl) <= 8 else 0
    # the ladder: the frames ⊆ the common-perp-span, the dims 2..min(6, 8-rank-1)
    cspan = fidx(spf(sorted([s for s in range(V) if (common >> s) & 1][:8])))
    # the rungs: the sub-spaces of the common perp!!
    lad = []
    the_lines = [s for s in range(V) if (common >> s) & 1]
    acc = []
    for target_d in range(2, min(7, 8 - (8 - len(spf(the_lines[:6])) if len(the_lines) >= 6 else 3)) + 1):
        pass
    # (the simple ladder: the prefixes of the common lines' span!!)
    for k in range(2, min(6, len(the_lines)) + 1, 2):
        F = fidx(spf(sorted(the_lines[:k])))
        if fdim(F) != len(spf(sorted(the_lines[:k]))): continue
        lad.append(F)
    CL_LADDER.append(lad)
log('the ladders: the lengths %s' % [len(l) for l in CL_LADDER])

# ---------------- (3) THE READ-ASSIGNMENT (the (t, w) -> the cluster-rung!!) ----------------
# per (t, w): the rung = the LOWEST cluster-rung (t's cluster!!) ⊇ home_w; the
# fallback: the per-target private rung (the ⊥-extension (the dup-territory!!))
wire_home = {}
for w in readers:
    wire_home[w] = fidx(spf(list(w[1]))) if w[0] == 'P' else SINGLE[w[1]]
READNODE = {}      # (t, w) -> the frame!!
PRIVATE = []       # the per-target private rungs (the dup-territory!!)
for t in range(V):
    lad = CL_LADDER[t and next(i for i, c in enumerate(CL) if t in c)]
    for w in [x for x in readers if t in readers[x]]:
        home = wire_home[w]
        node = None
        for R in lad:
            if (fmask(R) & fmask(home)) == fmask(home):
                node = R; break
        if node is None:
            # the private rung: the ⊥-extension of home inside perp(t)!!
            hl = [s for s in range(V) if (fmask(home) >> s) & 1]
            need = sorted(set(hl) | {s for s in PERP[t] if len(spf(sorted(set(hl + [s])))) > fdim(home)})
            F = fidx(spf(need[:fdim(home) + 3]))
            node = F
            PRIVATE.append((t, w))
        READNODE[(t, w)] = node
log('the read-assignment: %d reads | the private (the dup-territory!!) %d' % (len(READNODE), len(PRIVATE)))

# ---------------- (4) THE WIRES' CHAINS (the nodes nested?!? the audit!!) ----------------
WCHAIN = defaultdict(list)
for (t, w), R in READNODE.items():
    WCHAIN[w].append((R, t))
viol = 0; dupreg = {}
dupq = 2 * V + len(kept) + 9 + 150        # (the R0's layout!!)
for w, lst in WCHAIN.items():
    lst.sort(key=lambda x: fdim(x[0]))
    cur = wire_home[w]
    ok = []
    for R, t in lst:
        if (fmask(R) & fmask(cur)) == fmask(cur):
            ok.append((R, t)); cur = R
        else:
            viol += 1                      # the dup-fill (a fresh copy for t!!)
            dupreg[(t, w)] = dupq; dupq += 1
            ok.append((('DUP', (t, w)), t))
log('THE WIRES-CHAIN AUDIT: the violations %d (the dup-fills!!)' % viol)
log('THE R: %d (433 + %d dups!!)' % (433 + viol, viol))
json.dump({'clusters': [[int(x) for x in c] for c in CL],
           'ladders': [[[int(x) for x in r] for r in l] for l in CL_LADDER],
           'viol': viol},
          open('ii19_nat106_census.json', 'wt'))
log('SAVED ii19_nat106_census.json')
