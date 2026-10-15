"""Frame-by-frame span structure of the E8 R420 word (z-gates of phases A and B; helpers start empty; targets
ignored as destinations except to record reads).  For each frame: registers touched, dim of their contents before
the first and after the last gate there, frame rank, content sizes.  usage: align.py word.json.gz"""
import sys, gzip, json, collections
import numpy as np
w = json.load(gzip.open(sys.argv[1]))
V = w['v']; L = np.array(w['lines'], dtype=float); frames = w['frames']
NS = V; NT = V   # registers: 0..119 sources, 120..239 targets, 240.. helpers (assumed)
nreg = len(w['start'])
content = [0] * nreg
for u in range(NS): content[u] = 1 << u
def frank(f):
    ls = frames[f]
    return int(np.linalg.matrix_rank(L[ls])) if ls else 0
gates = [('A', g) for g in w['A']] + [('B', g) for g in w['B']]
istarget = lambda r: NS <= r < NS + NT
first = {}; last = {}; touched = collections.defaultdict(set)
before = {}; after = {}
for idx, (ph, (f, d, srcs)) in enumerate(gates):
    regs = [d] + list(srcs)
    for r in regs:
        if (f, r) not in before: before[(f, r)] = content[r]
        touched[f].add(r)
    if not istarget(d):
        v = content[d]
        for s in srcs: v ^= content[s]
        content[d] = v
    else:
        v = content[d]
        for s in srcs: v ^= content[s]
        content[d] = v
    for r in regs: after[(f, r)] = content[r]
def rk(vs):
    basis = []
    for v in vs:
        for b in basis:
            if v ^ b < v: v ^= b
        if v: basis.append(v); basis.sort(reverse=True)
    return len(basis)
stat = collections.defaultdict(list)
for f, regs in touched.items():
    zr = [r for r in regs if not istarget(r)]
    if not zr: continue
    b = [before[(f, r)] for r in zr]; a = [after[(f, r)] for r in zr]
    nz_b = sum(1 for v in b if v); nz_a = sum(1 for v in a if v)
    stat[frank(f)].append((len(frames[f]), len(zr), rk(b), rk(a), nz_b, nz_a,
                           np.mean([bin(v).count('1') for v in b]), np.mean([bin(v).count('1') for v in a]), sum(1 for r in regs if istarget(r))))
print('frame rank: #frames | lines | regs | dim before | dim after | nonzero before/after | mean |content| before/after | target touches')
for r in sorted(stat):
    S = np.array(stat[r], dtype=float)
    print('rank %d: %4d frames | lines %.1f | regs %.2f | dim %.2f -> %.2f | nz %.2f -> %.2f | size %.1f -> %.1f | tgt %.2f' % (
        r, len(S), *S[:, 0:1].mean(0), S[:, 1].mean(), S[:, 2].mean(), S[:, 3].mean(), S[:, 4].mean(), S[:, 5].mean(), S[:, 6].mean(), S[:, 7].mean(), S[:, 8].mean()))
