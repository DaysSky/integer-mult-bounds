"""THE CO-GROUP CHAIN-SOLVER (ii19_nat105.py) — the forest via the rich-4 rungs!!

THE nat104's LESSON: the blind ⊥-extension chains fail (154/154 overflow!!) — the
shared rungs must come from THE RICH-4 POOL (the nat94 cache (the T-sets (the
co-groups!!!))). THE PROTOCOL (per wire (the piece {a,b,c} or the source u!!)):
(1) THE CANDIDATE RUNGS: the rich-4s with inF ⊇ the wire's span (the frames
    containing the wire's lines!!): T(G) ∩ the readers = the cluster!!!
(2) THE CHAIN: home -> G_1 (the biggest cluster!!) -> G_2 (⊇ G_1?? — the level-
    nesting (the dim-5/6 extensions (the ⊥-structure!!!))) -> ... -> FULL;
(3) THE READER-SLOTS: the reader at the FIRST chain-frame ⊆ perp(t);
(4) THE DUP-FILLS at the leftovers (the census!!!) + THE R-VERDICT!!!
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
PERP = [set(p) for p in SPEC['PERP']]
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
R0 = DES['R']
log('the design: the pieces %d | the R0 %d' % (len(kept), R0))

# the rich-4 cache (the rung candidates!!)
import numpy as np
Z = np.load('ii19_nat94_richpool.npz')
RKEYS = [tuple(int(x) for x in k) for k in Z['keys']]
RMASK = [int(''.join(str(int(b)) for b in m[::-1]), 2) for m in Z['masks']]
RT = [int(''.join(str(int(b)) for b in t[::-1]), 2) for t in Z['Tmat']]
log('the rich-4 cache: %d' % len(RKEYS))

# the readers!!
readers = defaultdict(list)
for t in range(V):
    for p in T_BASE[t]: readers[('P', p)].append(t)
    for s in T_FILL[t]: readers[('S', s)].append(t)
log('the wires: %d | the loads %s' % (len(readers), dict(sorted(Counter(len(v) for v in readers.values()).items()))))

# the frame machinery!!
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

# per wire: the candidate rich-4s (inF ⊇ the wire's lines!!)
def wire_lines(w):
    return list(w[1]) if w[0] == 'P' else [w[1]]
WIRE_CAND = {}
for w in readers:
    wl = wire_lines(w)
    wmask = sum(1 << s for s in wl)
    cand = [i for i in range(len(RKEYS)) if (RMASK[i] & wmask) == wmask]
    WIRE_CAND[w] = cand
log('the wire-candidates: %s' % dict(sorted(Counter(len(c) for c in WIRE_CAND.values()).items())))

# the chain-solver: the biggest-cluster-first + the level-nesting!!!
def chain_for(w):
    rs = set(readers[w])
    rmask = 0
    for t in rs: rmask |= (1 << t)
    home = fidx(spf(wire_lines(w))) if w[0] == 'P' else SINGLE[w[1]]
    chain = [home]
    slots = defaultdict(list)
    served = set()
    cur = home; curdim = fdim(home)
    while len(rs - served) > 0 and curdim < 8:
        rem = rs - served
        # the best rung: the rich-4 (or the current's extension) maximizing the new coverage!!
        best_i, best_cov = None, 0
        for i in WIRE_CAND[w]:
            cov = len([t for t in rem if (RT[i] >> t) & 1])
            if cov > best_cov: best_cov = cov; best_i = i
        # the extension of cur ⊇ (cur + the rich-4's span?!): the nesting cur ⊂ G!!
        if best_i is not None and best_cov > 0:
            G = fidx(spf(sorted(RKEYS[best_i])))
            if fdim(cur) < 4 and (fmask(G) & fmask(cur)) != fmask(cur):
                # cur ⊄ G: the bridge: cur's lines + the rich-4's keys!!
                bl = sorted(set([s for s in range(V) if (fmask(cur) >> s) & 1]) | set(RKEYS[best_i]))
                G = fidx(spf(bl))
            if fdim(G) > 8 - 1: G = FULL
            # the readers: G ⊆ perp(t)?!
            gm = fmask(G)
            group = [t for t in rem if (gm & ~PM[t]) == 0]
            if not group:
                served |= rem; break
            for t in group: slots[len(chain)].append(t)
            served |= set(group)
            chain.append(G); cur = G; curdim = fdim(G)
            continue
        served |= rem
    return chain, slots

WCHAIN = {}
dupneed = Counter()
for w in readers:
    ch, sl = chain_for(w)
    WCHAIN[w] = (ch, sl)
    # the unserved!!
log('the chains: %d | the chain-lengths: %s' % (len(WCHAIN), dict(sorted(Counter(len(v[0]) for v in WCHAIN.values()).items()))))

# the census: the per-target read-frames (the nesting?!?!)
tframes = defaultdict(list)
for w, (ch, sl) in WCHAIN.items():
    for j, ts in sl.items():
        for t in ts:
            tframes[t].append((ch[j], w))
log('the per-target read-frames: %s' % dict(sorted(Counter(len(v) for v in tframes.values()).items())))
# THE DUP-CENSUS: the target's frames sorted by dim: the violations (the non-nesting!!)
viol = 0
for t in range(V):
    fs = sorted(tframes[t], key=lambda x: fdim(x[0]))
    cur = EMPTY
    for f, w in fs:
        if (fmask(f) & fmask(cur)) != fmask(cur):
            viol += 1          # the dup-fill needed!!!
        else:
            cur = f
log('THE DUP-CENSUS: the violations %d (the dup-fills (the +1 registers each!!))' % viol)
log('THE R-VERDICT: %d (R0 %d) + the dups %d -> R = %d vs THE CEILING 480' % (
    R0, R0, viol, R0 + viol))
json.dump({'chains': {repr(list(wire_lines(k))): [list(v[0]), {str(j): v[1][j] for j in v[1]}] for k, v in WCHAIN.items()},
           'R0': R0, 'viol': viol},
          open('ii19_nat105_census.json', 'wt'))
log('SAVED ii19_nat105_census.json')
