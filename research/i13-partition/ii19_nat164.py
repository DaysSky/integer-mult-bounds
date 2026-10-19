"""nat164: THE A-SIDE RECOMPOSITION CENSUS (the 121's piece-family economy).

The B-side recomposition delivered 242 (the -41). The A-side (~180 intermediates serving
the wires) was never recomposed. The shared piece-family: the wires' contents' pairwise
intersections; the per-wire demands re-solved reuse-first -> the distinct-piece minimum.
"""
import json
from collections import Counter, defaultdict

W4 = json.load(open('ii19_own_word4.json'))
v = W4['v']
nreg = 2*v + W4['R']
X = (1 << v) - 1

# the replay: the registers' x-contents at the A-END
val = [0]*nreg
for s in range(v): val[s] = 1 << s
for F, d, ss in W4['D']:
    for s in ss: val[d] ^= val[s]
for F, d, ss in W4['A']:
    for s in ss: val[d] ^= val[s]
xpart = [val[r] & X for r in range(nreg)]

# the wire-structure: the B-phase's srcs (the wires read by the targets) -> the B-wires;
# the A-phase's dests read by later A/B -> the intermediates.
ret_set = set(W4['ret'])
read_by = defaultdict(set)
for F, d, ss in W4['A']:
    for s in ss:
        read_by[s].add(d)
for F, d, ss in W4['B']:
    for s in ss:
        read_by[s].add(d)

b_wires = set()
for F, d, ss in W4['B']:
    for s in ss:
        if s >= 2*v and s not in ret_set:
            b_wires.add(s)
inters = [r for r in range(2*v, nreg) if r not in ret_set and r not in b_wires]
print('the W4 structure: %d B-wires | %d intermediates | %d rets' % (len(b_wires), len(inters), len(ret_set)), flush=True)

# the intermediates' consumer census
cons = Counter(len(read_by[r]) for r in inters)
print('the intermediates by consumer-count:', dict(sorted(cons.items())), flush=True)
contents = Counter(bin(xpart[r]).count('1') for r in inters)
print('the intermediates by content-size:', dict(sorted(contents.items())), flush=True)

# THE WIRES' DEMANDS: each B-wire's content = the XOR of its build-pieces (the A-srcs!)
# The A-phase: the wire's build-gates: the srcs (the intermediates + the sources!!)
def build_srcs(r):
    srcs = set()
    for F, d, ss in W4['A']:
        if d == r:
            srcs.update(ss)
    return srcs

wire_demand = {}
for w in sorted(b_wires):
    srcs = build_srcs(w)
    # the demand: the wire's content; the pieces available: the srcs' contents + the sources
    # the re-solve: the wire's content = XOR of the pieces' contents (the srcs' x-parts!)
    dm = xpart[w]
    pieces_avail = [xpart[s] for s in srcs if s >= 2*v and s not in ret_set]
    sol_srcs = [s for s in srcs if s < v]  # the direct source-reads
    wire_demand[w] = (dm, pieces_avail, sol_srcs)
pcs = Counter(len(p) for _, p, _ in wire_demand.values())
print('the wires by their build-piece-counts:', dict(sorted(pcs.items())), flush=True)

# THE SHARED PIECE-FAMILY: the wires' contents' pairwise intersections
wc = {w: xpart[w] for w in b_wires}
pool = {}
wl = sorted(b_wires)
for i in range(len(wl)):
    for j in range(i+1, len(wl)):
        S = wc[wl[i]] & wc[wl[j]]
        if bin(S).count('1') >= 8:
            pool[S] = (wl[i], wl[j])
print('the shared piece-pool (the wire-content intersections >= 8 lines): %d' % len(pool), flush=True)

# the reuse-first re-solve: each wire's demand over (the pool + its own pieces + the sources)
def rref_solve(tm, cands):
    rows, piv = [], {}
    for cm in cands:
        cur, combo = cm, [cm]
        while cur:
            p = cur & -cur
            if p in piv:
                _, bm, bc = rows[piv[p]]
                cur ^= bm
                combo = combo + bc
            else:
                break
        if cur:
            p = cur & -cur
            piv[p] = len(rows)
            rows.append((p, cur, combo))
    cur, combo = tm, []
    while cur:
        p = cur & -cur
        if p not in piv:
            return None
        _, bm, bc = rows[piv[p]]
        cur ^= bm
        combo = combo + bc
    cnt = Counter(combo)
    return [c for c, nn in cnt.items() if nn % 2]

used = set()
ok, fail = 0, 0
per_wire = Counter()
for w in wl:
    dm, own, srcs = wire_demand[w]
    cands = [cm for cm in pool if (cm & ~dm) == 0] + own
    sol = rref_solve(dm, cands)
    if sol is None:
        # the own-pieces must always span: fallback
        sol = own
        fail += 1
    else:
        ok += 1
    per_wire[len(sol)] += 1
    used.update(sol)
print('the re-solves: %d ok, %d fallback | the pieces-per-wire:', ok, fail, dict(sorted(per_wire.items())), flush=True)
print('THE DISTINCT PIECES: %d (vs the W4 intermediates: %d)' % (len(used), len(inters)))

# the sources' side: the direct source-reads per wire
sread = Counter(len(s) for _, _, s in wire_demand.values())
print('the direct-source-reads per wire:', dict(sorted(sread.items())))
print('the total source-reads: %d' % sum(len(s) for _, _, s in wire_demand.values()))
