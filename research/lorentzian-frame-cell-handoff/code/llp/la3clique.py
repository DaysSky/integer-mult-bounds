"""Exact DFS for a COMPATIBLE A3 packing: pairwise disjoint, pairwise compatible A3 blocks covering as many lines as
possible (partition if all).  Dynamic ordering: branch on the uncovered line with fewest candidate blocks; a line with
no candidate is left uncovered only if the remaining budget of uncovered lines allows (target = max uncovered).
usage: la3clique.py n maxuncovered timelimit  (reads a3compat_n.pkl)  -> a3cpart_n.json"""
import sys, pickle, time, json
n = int(sys.argv[1]); MAXU = int(sys.argv[2]); TL = float(sys.argv[3])
d = pickle.load(open('a3compat_%d.pkl' % n, 'rb'))
A3 = d['A3']; nb = d['nb']; N = len(A3)
V = max(max(x) for x in A3) + 1
lm = [sum(1 << s for s in X) for X in A3]
nbm = []
for i in range(N):
    m = 0
    for j in nb[i]: m |= 1 << j
    nbm.append(m)
by_line = [0] * V
for i, X in enumerate(A3):
    for s in X: by_line[s] |= 1 << i
ALLC = (1 << N) - 1
t0 = time.time(); best = [None, -1]; nodes = [0]
def bits(m):
    out = []
    while m:
        b = m & -m; out.append(b.bit_length() - 1); m ^= b
    return out
def dfs(chosen, cand, covered, skipped):
    nodes[0] += 1
    if time.time() - t0 > TL: raise TimeoutError
    ncov = bin(covered).count('1')
    if ncov > best[1]:
        best[1] = ncov; best[0] = list(chosen)
        print('[%5.0fs] covered %d blocks %d skipped %d nodes %d' % (time.time() - t0, ncov, len(chosen), len(skipped), nodes[0]), flush=True)
        json.dump([A3[i] for i in chosen], open('a3cpart_%d.json' % n, 'w'))
    if ncov == V: return True
    # choose uncovered, unskipped line with fewest candidates
    bl = None; bc = None
    for s in range(V):
        if covered >> s & 1 or s in skipped: continue
        c = cand & by_line[s]
        k = bin(c).count('1')
        if bl is None or k < bc[0]:
            bl = s; bc = (k, c)
            if k == 0: break
    if bl is None: return False
    k, c = bc
    # upper bound: lines still coverable
    for i in bits(c):
        if dfs(chosen + [i], cand & nbm[i] & ~sum(by_line[s] for s in A3[i]) if False else (cand & nbm[i]), covered | lm[i], skipped):
            return True
    if len(skipped) < MAXU:
        return dfs(chosen, cand & ~by_line[bl], covered, skipped | {bl})
    return False
# candidates must be disjoint from covered lines: maintain by removing blocks meeting newly covered lines
def dfs2(chosen, cand, covered, skipped):
    return dfs(chosen, cand, covered, skipped)
# patch: when choosing block i, remove all blocks meeting its lines
_dfs = dfs
def dfs(chosen, cand, covered, skipped):
    nodes[0] += 1
    if time.time() - t0 > TL: raise TimeoutError
    ncov = bin(covered).count('1')
    if ncov > best[1]:
        best[1] = ncov; best[0] = list(chosen)
        print('[%5.0fs] covered %d blocks %d skipped %d nodes %d' % (time.time() - t0, ncov, len(chosen), len(skipped), nodes[0]), flush=True)
        json.dump([A3[i] for i in chosen], open('a3cpart_%d.json' % n, 'w'))
    if ncov == V: return True
    bl = None; bc = None
    for s in range(V):
        if covered >> s & 1 or s in skipped: continue
        c = cand & by_line[s]
        k = bin(c).count('1')
        if bl is None or k < bc[0]:
            bl = s; bc = (k, c)
            if k == 0: break
    if bl is None: return False
    # bound: uncovered lines with no candidate at all must be skipped
    dead = sum(1 for s in range(V) if not (covered >> s & 1) and s not in skipped and not (cand & by_line[s]))
    if len(skipped) + dead > MAXU: return False
    k, c = bc
    for i in bits(c):
        rm = 0
        for s in A3[i]: rm |= by_line[s]
        if dfs(chosen + [i], cand & nbm[i] & ~rm, covered | lm[i], skipped): return True
    if len(skipped) < MAXU:
        return dfs(chosen, cand & ~by_line[bl], covered, skipped | {bl})
    return False
try:
    r = dfs([], ALLC, 0, frozenset())
    print('search complete:', 'FOUND' if r else 'NONE within maxuncovered', 'best covered', best[1], 'nodes', nodes[0], '%.0fs' % (time.time() - t0))
except TimeoutError:
    print('TIMEOUT best covered', best[1], 'nodes', nodes[0])
