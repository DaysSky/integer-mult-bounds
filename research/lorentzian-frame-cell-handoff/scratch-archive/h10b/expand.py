import json, sys, itertools, numpy as np, glob
def expand(d):
    blocks = d['blocks']; vecs = set()
    for parts, y in d['orbits']:
        perms = [set(itertools.permutations(p)) for p in parts]
        for combo in itertools.product(*perms):
            x = [c for blk in combo for c in blk]
            v = tuple(x + [y]); nv = tuple(-a for a in v)
            vecs.add(max(v, nv))
    return np.array(sorted(vecs))
for f in sorted(glob.glob('../lor3/best_n10_t3_*.json')):
    d = json.load(open(f))
    if d['lines'] != 165: continue
    V = expand(d); n = d['n']
    eta = np.array([1]*n + [-1]); G = (V*eta) @ V.T
    ok = (np.diag(G) == 2).all() and set(np.unique(G[~np.eye(len(V), dtype=bool)])) <= {-1, 0, 1}
    name = f.split('best_')[1].replace('.json', '')
    np.save('sys_%s.npy' % name, V)
    print(name, len(V), 'root-like' if ok else 'NOT root-like', flush=True)
