import numpy as np, pickle
elems = np.load('eis_elems.npy').astype(np.int64)
n = 40
key = lambda g: g.tobytes()
idx = {key(g): i for i, g in enumerate(elems)}
gens = [np.array(g) for g in pickle.load(open('eis_gens.pkl', 'rb'))]
inv = lambda g: np.argsort(g)
seen = np.zeros(len(elems), dtype=bool); classes = []
for i, g in enumerate(elems):
    if seen[i]: continue
    orb = {i}; front = [g]
    while front:
        new = []
        for x in front:
            for s in gens:
                y = s[x[inv(s)]]   # s x s^-1
                k = idx[key(y)]
                if k not in orb: orb.add(k); new.append(y)
        front = new
    for k in orb: seen[k] = True
    o = 1; x = g.copy()
    while not np.array_equal(x, np.arange(n)): x = g[x]; o += 1
    fixed = int(np.sum(g == np.arange(n)))
    classes.append((o, len(orb), i, fixed))
classes.sort()
for c in classes: print('order', c[0], 'class size', c[1], 'rep', c[2], 'fixed lines', c[3])
pickle.dump(classes, open('classes.pkl', 'wb'))
