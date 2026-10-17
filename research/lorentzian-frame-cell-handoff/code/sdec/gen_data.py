import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
n = int(sys.argv[1]); out = sys.argv[2]
g = Geom(n); V = g.V
with open(out, 'w') as f:
    f.write('%d %d\n' % (V, n))
    for t in range(V): f.write('%d\n' % g.binlabel(t))
    for t in range(V):
        N = [u for u in range(V) if u != t and g.G[t, u] != 0]
        R = [u for u in range(V) if u != t and g.G[t, u] == 0]
        f.write('%d %s\n' % (len(N), ' '.join(map(str, N))))
        f.write('%d %s\n' % (len(R), ' '.join(map(str, R))))
print('V', V)
