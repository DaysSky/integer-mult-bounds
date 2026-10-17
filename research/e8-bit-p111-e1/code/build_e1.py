"""Build E1 from P111-tuned: helper 248 (register 470) becomes an entrance-rank-2 helper.
An early gate `helper 222 += helper 248` is inserted right before A[230] (`helper 248 += x77`), so the dirt of register
470 enters register 444 twice (here and at A[1993], PR #589's hoist) and cancels; 470 leaves D.  The three gates on 470
(the inserted read, A[230] and A[1993]) are placed at frame 186 = span(root 33, root 77) (rank 2, two orthogonal live
roots), the frame x77 climbs to next (A[426]), and 470 starts there.  D is recomputed from the raw word (K = helper part
of every target's raw output), C is rebuilt as the literal reverse of the z-destination gates of A and B at the full
frame."""
import gzip, json, sys, copy, hashlib
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(HERE, '..', '..', 'e8-bit-p111-tuned', 'tune', 'bitE8mut-p111-tuned.json.gz')
out = sys.argv[1] if len(sys.argv) > 1 else 'bitE8mut-p111-e1.json.gz'
w = json.load(gzip.open(src, 'rt'))
v, R = w['v'], w['R']; n = 2 * v + R
FULL = [k for k, f in enumerate(w['frames']) if len(f) == v]; assert len(FULL) == 1; FULL = FULL[0]
ZERO = [k for k, f in enumerate(w['frames']) if len(f) == 0]; assert len(ZERO) == 1; ZERO = ZERO[0]
H, G, E0, E = 470, 444, 79, 186
assert w['A'][230] == [E0, H, [77]] and w['A'][1993] == [E0, G, [H]]
assert sorted(w['frames'][E]) == [33, 77] and sorted(w['frames'][E0]) == [77]
nw = copy.deepcopy(w)
nw['start'][H] = E
nw['A'] = w['A'][:230] + [[E, G, [H]], [E, H, [77]]] + w['A'][231:]
nw['A'][1994] = [E, G, [H]]
is_y = lambda r: v <= r < 2 * v
# raw word values (A, scatter, B)
val = [1 << r for r in range(n)]
def run(gates):
    for f, d, srcs in gates:
        acc = 0
        for s in srcs: acc ^= val[s]
        val[d] ^= acc
run(nw['A'])
copies = [val[q] for q in nw['ret']]
for t, row in enumerate(nw['scatter']):
    for k in row: val[v + t] ^= copies[k]
run(nw['B'])
hmask = ((1 << R) - 1) << (2 * v)
D = []
for t in range(v):
    K = [r for r in range(2 * v, n) if val[v + t] >> r & 1]
    if K: D.append([ZERO, v + t, K])
old = {g[1]: g[2] for g in w['D']}
newd = {g[1]: g[2] for g in D}
diff = sorted(set(old) | set(newd))
changes = [(t, sorted(set(old.get(t, [])) ^ set(newd.get(t, [])))) for t in diff if set(old.get(t, [])) != set(newd.get(t, []))]
print('D gates changed:', len(changes), '; symmetric differences:', sorted({x for _, d in changes for x in d}))
nw['D'] = D
zg = [[FULL, g[1], list(g[2])] for sec in ('A', 'B') for g in nw[sec] if not is_y(g[1])]
nw['C'] = list(reversed(zg))
nw['stats'] = dict(w.get('stats', {}), entrance_helpers={str(H - 2 * v): E})
# canonical, byte-reproducible file (as P111-tuned's tune/wlib.py: sorted keys, compact separators, gzip mtime 0, OS byte 255)
data = gzip.compress(json.dumps(nw, sort_keys=True, separators=(',', ':')).encode(), compresslevel=9, mtime=0)
data = data[:9] + bytes([255]) + data[10:]
open(out, 'wb').write(data)
print('written: A', len(nw['A']), 'B', len(nw['B']), 'C', len(nw['C']), 'D', len(nw['D']), '; file sha256', hashlib.sha256(data).hexdigest()[:16] + '...')
