"""S11 orbits of the 9-line sub-cliques Q - q of the 10-cliques (each still forces >= 9 pieces), merged with the
maximal-clique orbits into corbits2.pkl."""
import sys, pickle, collections, time
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp')
import flats
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
orb = pickle.load(open(D + 'corbits.pkl', 'rb'))
t = time.time()
subs = set()
for k, v in orb.items():
    if len(v[0]) != 10: continue
    for c in v:
        for i in range(10): subs.add(c[:i] + c[i + 1:])
known = {}
for k, v in orb.items():
    for c in v: known[c] = k
new = collections.defaultdict(list)
for c in subs:
    if c in known: continue          # a maximal 9-clique (cannot happen for a proper subset, kept for safety)
    new[('sub',) + flats.canon(c)].append(c)
out = dict(orb); out.update(new)
print('sub-cliques', len(subs), 'new orbits', len(new), '%.0fs' % (time.time() - t), flush=True)
pickle.dump(out, open(D + 'corbits2.pkl', 'wb'))
