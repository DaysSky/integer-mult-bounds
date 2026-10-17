import itertools, sys, json, time
from feasp2 import feasible_p2
K = int(sys.argv[1]); p = int(sys.argv[2]); s = 2 * K + 1
t = time.time(); feas = []; n = 0
for sq in itertools.product(range(K), repeat=s):
    firsts = []
    for x in sq:
        if x not in firsts: firsts.append(x)
    if firsts != list(range(K)): continue
    n += 1
    if feasible_p2(list(sq), p): feas.append(sq)
print('K', K, 'p', p, 'canonical sequences', n, 'feasible', len(feas), '%.0fs' % (time.time() - t), flush=True)
json.dump([list(x) for x in feas], open('feas_K%d_p%d.json' % (K, p), 'w'))
for x in feas[:50]: print(x)
