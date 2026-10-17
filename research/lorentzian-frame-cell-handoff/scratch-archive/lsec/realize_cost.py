"""Register cost of realising a section-level solution with a depth-2 middle (lines/cells -> node -> section).
Per support node X: required vectors = arrivals assigned to X (by support) + in-chain reads at X.  V_X = their span.
Inputs needed: a set of raw unit vectors e_s and design-cell vectors (any vector of F2^P for a design cell P ⊂ X) whose
span contains V_X; minimum count computed greedily (exact for raw-only = |supp V_X| restricted to lines needed...).
Outputs of X = #arrivals from X.  Waste(X) = max(0, inputs - outputs).  Registers N = #arrival registers (incl. empty)
+ sum waste.  NOTE: arrivals with the same support set are pooled into one node (optimistic: assumes one node per
distinct support flat)."""
import sys, json, itertools
from lcommon import *
DES = sys.argv[1]; SOL = sys.argv[2]
planes = [int(h, 16) for h in json.load(open(DES))['planes']]
sol = json.load(open(SOL))
# expand H55 orbit reps to all images
def images(Q, a):
    return set((act(Q, p), act(a, p)) for p in PERMS)
node_req = collections.defaultdict(list); node_out = collections.Counter(); n_arr = 0; n_empty = 0
for e in sol['arrivals']:
    Q = int(e['Q'], 16); a = int(e['a'], 16); X = int(e['support'], 16)
    for p in PERMS:
        Qi, ai, Xi = act(Q, p), act(a, p), act(X, p)
        if ai == 0: n_empty += 1; continue
        node_req[Xi].append(ai); node_out[Xi] += 1; n_arr += 1
# dedupe orbit double counting (orbits of size < 55 would repeat): use set of (Q, j, image)
seen = set(); node_req2 = collections.defaultdict(list); node_out2 = collections.Counter(); n_arr2 = 0
for e in sol['arrivals']:
    Q = int(e['Q'], 16); a = int(e['a'], 16); X = int(e['support'], 16); j = e['j']
    for p in PERMS:
        key = (act(Q, p), j)
        if key in seen: continue
        seen.add(key)
        ai, Xi = act(a, p), act(X, p)
        if ai == 0: continue
        node_req2[Xi].append(ai); node_out2[Xi] += 1; n_arr2 += 1
inch_req = collections.defaultdict(list)
seen_t = set()
for e in sol['inchain']:
    t = e['t']
    if not e['node']: continue
    X = int(e['node'][0], 16); rv = int(e['read'], 16)
    for p in PERMS:
        ti = p[t]
        if ti in seen_t and False: continue
        inch_req[act(X, p)].append(act(rv, p))
def rank(vs):
    b = []
    for v in vs:
        for x in b:
            if v ^ x < v: v ^= x
        if v: b.append(v); b.sort(reverse=True)
    return len(b), b
tot_waste = 0; stats = collections.Counter()
for X in set(node_req2) | set(inch_req):
    req = node_req2.get(X, []) + inch_req.get(X, [])
    d, basis = rank(req)
    supp = 0
    for v in req: supp |= v
    n_out = node_out2.get(X, 0)
    n_in_raw = pc(supp)                       # raw unit vectors on the support
    n_in = max(d, min(n_in_raw, n_in_raw))    # optimistic lower: dim; raw realisation: |supp|
    waste_lo = max(0, d - n_out); waste_raw = max(0, n_in_raw - n_out)
    stats['nodes'] += 1; stats['dim_sum'] += d; stats['supp_sum'] += n_in_raw; stats['out_sum'] += n_out
    stats['waste_lo'] += waste_lo; stats['waste_raw'] += waste_raw
# section-level registers: per section max(#delivered users, #nonzero arrivals)
secinfo = collections.defaultdict(lambda: {'deliv': set(), 'nz': 0, 'users': set()})
seen3 = set()
for e in sol['arrivals']:
    Q = int(e['Q'], 16); a = int(e['a'], 16); j = e['j']
    for p in PERMS:
        Qi = act(Q, p)
        key = (Qi, j)
        if key in seen3: continue
        seen3.add(key)
        si = secinfo[Qi]
        if act(a, p): si['nz'] += 1
        for t, z in e['z'].items():
            ti = p[int(t)]
            si['users'].add(ti)
            if not z: si['deliv'].add(ti)
sec_regs = sum(max(len(si['deliv']), si['nz']) for si in secinfo.values())
sec_waste = sum(max(0, si['nz'] - len(si['deliv'])) for si in secinfo.values())
print('sections', len(secinfo), ' delivered users', sum(len(si['deliv']) for si in secinfo.values()), ' nonzero arrivals', n_arr2,
      ' section registers', sec_regs, ' (dead content arrivals', sec_waste, ')')
print(dict(stats))
v = V
print('N (lower) = section registers + node waste(dim) =', sec_regs + stats['waste_lo'], ' -> R =', sec_regs + stats['waste_lo'] - v)
print('N (raw-unit) = section registers + node waste(|supp|) =', sec_regs + stats['waste_raw'], ' -> R =', sec_regs + stats['waste_raw'] - v)
