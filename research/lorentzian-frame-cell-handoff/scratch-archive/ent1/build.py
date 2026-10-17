"""Build the entrance-rank-1 variant of P111-tuned: helper 248 (register 470) starts at its line frame 79 (line 77);
an early gate `helper 222 += helper 248` at frame 79 is inserted right before A[230] (`helper 248 += x77`), so the
dirt of register 470 enters register 444 twice (here and at A[1993]) and cancels.  D is recomputed from the raw word
(K = helper part of every target's raw output), C is rebuilt as the literal reverse of the z-destination gates of A
and B at the full frame."""
import gzip, json, sys, copy
src = '/home/user/integer-mult-bounds/research/e8-bit-p111-tuned/tune/bitE8mut-p111-tuned.json.gz'
w = json.load(gzip.open(src, 'rt'))
v, R = w['v'], w['R']; n = 2 * v + R
FULL = [k for k, f in enumerate(w['frames']) if len(f) == v]; assert len(FULL) == 1; FULL = FULL[0]
ZERO = [k for k, f in enumerate(w['frames']) if len(f) == 0]; assert len(ZERO) == 1; ZERO = ZERO[0]
H, G, E = 470, 444, 79
assert w['A'][230] == [E, H, [77]] and w['A'][1993] == [E, G, [H]]
nw = copy.deepcopy(w)
nw['start'][H] = E
nw['A'] = w['A'][:230] + [[E, G, [H]]] + w['A'][230:]
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
nw['stats'] = dict(w.get('stats', {}), entrance_rank1_helpers=[H - 2 * v])
json.dump(nw, gzip.open('bitE8mut-p111-e1.json.gz', 'wt'))
print('written: A', len(nw['A']), 'B', len(nw['B']), 'C', len(nw['C']), 'D', len(nw['D']))
