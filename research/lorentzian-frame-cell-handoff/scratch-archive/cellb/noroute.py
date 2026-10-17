import sys, random
sys.argv = ['x']
exec(open('forced2.py').read().split("print('identity:'")[0])
def noroute(src_cells, top_cells):
    cells_of = {s: [C for C in src_cells if C >> s & 1] for s in range(V)}
    D6s_of = {t: [perp(C) for C in top_cells if C >> t & 1] for t in range(V)}
    return sum(1 for t in range(V) for u in e8.bits(e8.HYP[t]) if not any(c & ~D == 0 for D in D6s_of[t] for c in cells_of[u]))
random.seed(1)
print('identity no-route pairs', noroute(cells1, cells1))
for trial in range(8):
    p = list(range(V))
    for _ in range(random.randint(1, 40)):
        q = RP[random.randrange(V)]; p = [q[i] for i in p]
    cells2 = [maskperm(C, p) for C in cells1]
    print('trial', trial, 'no-route (t,u) pairs:', noroute(cells1, cells2), 'of', V * 63)
