"""My own transcription of the 3x2 'merged' two-hub XOR network (33 vertices, 91 edges, capacity 149, 30 messages).
Builds the edge table with capacities and the message list; checks totals and hop distances."""
import itertools, collections, pickle
R, K = 3, 2
rows, cols = range(1, R + 1), range(1, K + 1)
cells = [(a, b) for a in rows for b in cols]; N = len(cells); A = K * R * (R - 1); B = R * K * (K - 1)
cap = {}
def edge(u, v, c):
    k = frozenset((u, v)); assert len(k) == 2 and k not in cap; cap[k] = c
s = lambda a, b: 's%d%d' % (a, b); p = lambda a, b: 'p%d%d' % (a, b); q = lambda a, b: 'q%d%d' % (a, b); t = lambda a, b: 't%d%d' % (a, b)
C = lambda b: 'C%d' % b; D = lambda a: 'D%d' % a
for (a, b) in cells:
    edge('O', s(a, b), R - 1); edge(s(a, b), C(b), 1); edge(C(b), q(a, b), 1)
    edge('H', p(a, b), 1 + (K - 1)); edge(p(a, b), D(a), 1); edge(D(a), t(a, b), 1)
    edge(q(a, b), 'G', 1 + (R - 1)); edge(t(a, b), 'Z', K)
for b in cols:
    edge(C(b), 'H', 1)
    for i in rows:
        for j in rows:
            if j != i: edge(s(j, b), p(i, b), 1); edge(p(i, b), q(j, b), 1)
for a in rows:
    edge(D(a), 'G', 1)
    for i in cols:
        for j in cols:
            if j != i: edge(p(a, j), q(a, i), 1); edge(q(a, i), t(a, j), 1)
edge('O', 'H', N + B); edge('G', 'Z', N + A)
msgs = []
for (a, b) in cells: msgs.append((s(a, b), t(a, b))); msgs.append(('O', 'Z'))
msgs += [('O', 'Z')] * (A + B)
V = sorted({v for k in cap for v in k}); adj = collections.defaultdict(list)
for k in cap:
    u, v = tuple(k); adj[u].append(v); adj[v].append(u)
def bfs(sv):
    d = {sv: 0}; dq = collections.deque([sv])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if y not in d: d[y] = d[x] + 1; dq.append(y)
    return d
need = sum(bfs(a)[b] for a, b in msgs)
print('vertices', len(V), 'edges', len(cap), 'capacity', sum(cap.values()), 'messages', len(msgs), 'routing need', need)
pickle.dump(dict(V=V, cap={tuple(sorted(k)): c for k, c in cap.items()}, msgs=msgs), open('net33.pkl', 'wb'))
