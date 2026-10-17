import itertools, collections
# combinatorial check of T-triangle covers: for A = {0,1,2}, D = {3..10}; a node = (B, C) disjoint triples in D, E = rest pair.
D = list(range(3, 11))
pairs = list(itertools.combinations(D, 2))
nodes = []
for B in itertools.combinations(D, 3):
    rest = [x for x in D if x not in B]
    for C in itertools.combinations(rest, 3):
        if C < B: continue
        E = tuple(x for x in rest if x not in C)
        within = set(itertools.combinations(B, 2)) | set(itertools.combinations(C, 2)) | {E}
        cross = set(tuple(sorted((b, c))) for b in B for c in C)
        nodes.append((B, C, E, within, cross))
print('triangle nodes through A:', len(nodes))
cnt = 0; ex = None
allp = set(pairs)
for q in itertools.combinations(range(len(nodes)), 4):
    W = set(); X = set()
    for i in q: W |= nodes[i][3]; X |= nodes[i][4]
    if W == allp and X == allp:
        cnt += 1
        if ex is None: ex = [nodes[i][:3] for i in q]
print('4-node T-triangle covers of R(T(012)):', cnt, 'example', ex)
