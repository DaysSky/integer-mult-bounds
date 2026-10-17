"""E8 roots (lines), Gram, orthogonality."""
import itertools, numpy as np
def e8_roots():
    R = []
    for i, j in itertools.combinations(range(8), 2):
        for si in (1, -1):
            for sj in (1, -1):
                v = [0]*8; v[i] = si; v[j] = sj; R.append(tuple(2*x for x in v))
    for signs in itertools.product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0: R.append(tuple(signs))
    # doubled coordinates; norm 8 -> root norm 2 after /2
    lines = []
    seen = set()
    for r in R:
        key = r if r > tuple(-x for x in r) else tuple(-x for x in r)
        if key not in seen: seen.add(key); lines.append(key)
    return np.array(lines)   # 120 x 8, doubled coords
if __name__ == '__main__':
    L = e8_roots(); G = L @ L.T // 4
    print(L.shape, set(np.diag(G)), np.unique(G))
