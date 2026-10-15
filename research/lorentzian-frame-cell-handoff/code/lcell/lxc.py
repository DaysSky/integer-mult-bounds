"""Independent (no CP-SAT) check of the j=0 read-assignment test: plain backtracking over cells (fewest live options
first), options pairwise disjoint, pruning by sum of remaining minimum sizes <= free targets.
usage: lxc.py SYSTEM.json"""
import sys, os, json
os.environ['GRP'] = '11'
from lbase import *
pc_ = lambda m: bin(m).count('1')
P = {}
def pm(m):
    if m not in P: P[m] = perp(m)
    return P[m]
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
co = {s: [C for C in cells if C >> s & 1] for s in range(V)}
opts = {}
for C in cells:
    s, a = list(bits(C)); os_ = 0; oa_ = 0
    for c in co[s]:
        if c != C: os_ |= pm(c)
    for c in co[a]:
        if c != C: oa_ |= pm(c)
    PC = pm(C); Fs = PC & ~os_; Fa = PC & ~oa_; D = Fs & Fa; S = Fs & ~Fa; A = Fa & ~Fs
    if not (D | S | A): continue
    nps = sorted(set(pm(closure(C | (1 << x))) for x in range(V) if not C >> x & 1))
    ms = set()
    for q1 in nps:
        for q2 in nps:
            ms.add((D & ~q1) | (S & ~(q1 | q2)) | (A & ~q1))
            ms.add((D & ~q1) | (S & ~q1) | (A & ~(q1 | q2)))
            ms.add((D & ~(q1 & q2)) | (S & ~q1) | (A & ~q2))
    if 0 in ms: continue
    ms = sorted(ms, key=pc_); keep = []
    for m in ms:
        if not any(k & m == k for k in keep): keep.append(m)
    opts[C] = keep
rmin = {C: pc_(o[0]) for C, o in opts.items()}
slack = V - sum(rmin.values())
opts = {C: [m for m in o if pc_(m) <= rmin[C] + slack] for C, o in opts.items()}
print(sys.argv[1], 'cells', len(opts), 'slack', slack, 'options', sum(map(len, opts.values())), flush=True)
nodes = [0]
VERB = os.environ.get('VERB') == '1'
def solve(rem, used, d=0):
    nodes[0] += 1
    if not rem: return True
    if sum(rmin[C] for C in rem) > V - pc_(used):
        if VERB: print('  ' * d + 'prune: remaining min reads', sum(rmin[C] for C in rem), '> free targets', V - pc_(used))
        return False
    best = None
    for C in rem:
        live = [m for m in opts[C] if not m & used]
        if not live:
            if VERB: print('  ' * d + 'dead: cell', sorted(bits(C)), 'all', len(opts[C]), 'options hit used targets')
            return False
        if best is None or len(live) < len(best[1]): best = (C, live)
    C, live = best; rest = [c for c in rem if c != C]
    if VERB: print('  ' * d + 'branch on cell', sorted(bits(C)), 'live options', [sorted(bits(m)) for m in live])
    for m in live:
        if VERB: print('  ' * d + ' try', sorted(bits(m)))
        if solve(rest, used | m, d + 1): return True
    return False
r = solve(list(opts), 0)
print('j=0 read assignment', 'EXISTS' if r else 'DOES NOT EXIST', 'search nodes', nodes[0], flush=True)
