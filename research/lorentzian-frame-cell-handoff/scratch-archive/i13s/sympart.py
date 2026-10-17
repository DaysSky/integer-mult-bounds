"""Exhaustive enumeration of G-invariant good-frame partitions of I_{13,1} for a permutation group G on 13 points.
Frame orbits that are 'free' (orbit size * 4 = lines covered) are the candidate pieces; exact cover of line orbits
(DLX-style recursion).  Each partition is scored by compatible frame pairs and greedy per-line cover (diag13 metric)."""
import sys, pickle, itertools, collections, numpy as np, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V; G = g.G
frames, comp_lists, kinds = pickle.load(open('../i13a/compat13.pkl', 'rb'))
fidx = {tuple(sorted(q)): i for i, q in enumerate(frames)}
orth = (G == 0); np.fill_diagonal(orth, False)
OM = [sum(1 << j for j in range(V) if orth[i, j]) for i in range(V)]
def act(p, l):
    k, s = g.kind[l], g.supp[l]
    return g.idx[(k, tuple(sorted(p[i] for i in s)))]
def group(gens):
    I = tuple(range(13)); els = {I}; fr = [I]
    while fr:
        nf = []
        for a in fr:
            for b in gens:
                c = tuple(b[a[i]] for i in range(13))
                if c not in els: els.add(c); nf.append(c)
        fr = nf
    return list(els)
def comp(a, b):
    arr = comp_lists[a]; k = np.searchsorted(arr, b); return k < len(arr) and arr[k] == b
def evaluate(part):
    cp = sum(comp(fidx[tuple(sorted(a))], fidx[tuple(sorted(b))]) for a, b in itertools.combinations(part, 2))
    frame_of = {u: f for f in part for u in f}
    dem = []
    for f in part:
        dem.append(OM[f[0]] & OM[f[1]] & OM[f[2]] & OM[f[3]])
        for a, b in itertools.combinations(range(4), 2):
            o = [z for z in range(4) if z not in (a, b)]
            dem.append(OM[f[a]] & OM[f[b]] & ~OM[f[o[0]]] & ~OM[f[o[1]]])
    fr = []; gr = []
    for u in range(V):
        mates = [x for x in frame_of[u] if x != u]
        Du = [d for d in dem if d >> u & 1]
        fr.append(sum(1 for d in Du if any(d >> m & 1 for m in mates)) / len(Du))
        unc = list(Du); cnt = 0
        while unc:
            cnts = collections.Counter()
            for d in unc:
                for v in Geom.bits(d & ~(1 << u)): cnts[v] += 1
            v, c = cnts.most_common(1)[0]
            unc = [d for d in unc if not d >> v & 1]; cnt += 1
        gr.append(cnt)
    return cp, float(np.mean(fr)), float(np.mean(gr)), max(gr)
def run(name, gens, limit=10**6, evalmax=200):
    Gp = group(gens)
    lorb = {}; lorbs = []
    for l in range(V):
        if l in lorb: continue
        o = sorted({act(p, l) for p in Gp}); 
        for x in o: lorb[x] = len(lorbs)
        lorbs.append(o)
    forbs = []; seen = set()
    for i, q in enumerate(frames):
        if i in seen: continue
        o = {tuple(sorted(act(p, l) for l in q)) for p in Gp}
        for x in o: seen.add(fidx[x])
        cov = collections.Counter(l for x in o for l in x)
        if max(cov.values()) > 1: continue
        lo = collections.Counter(lorb[l] for l in cov)
        if any(lo[k] != len(lorbs[k]) for k in lo): continue
        forbs.append((sorted(o), sorted(lo)))
    print('%s: |G| %d, line orbits %d, free frame orbits %d' % (name, len(Gp), len(lorbs), len(forbs)), flush=True)
    by = collections.defaultdict(list)
    for j, (o, lo) in enumerate(forbs):
        for k in lo: by[k].append(j)
    sols = []; t0 = time.time()
    def rec(unc, chosen):
        if len(sols) >= limit: return
        if not unc: sols.append(list(chosen)); return
        k = min(unc, key=lambda k: sum(1 for j in by[k] if set(forbs[j][1]) <= unc))
        for j in by[k]:
            s = set(forbs[j][1])
            if s <= unc:
                chosen.append(j); rec(unc - s, chosen); chosen.pop()
    rec(set(range(len(lorbs))), [])
    print('  partitions found %d (%.1fs)%s' % (len(sols), time.time() - t0, ' [LIMIT]' if len(sols) >= limit else ''), flush=True)
    res = []
    import random; random.seed(1)
    sample = sols if len(sols) <= evalmax else random.sample(sols, evalmax)
    for s in sample:
        part = [f for j in s for f in forbs[j][0]]
        assert sorted(l for f in part for l in f) == list(range(V))
        res.append((evaluate(part), part))
    res.sort(key=lambda r: r[0][2])
    for (cp, fr, gm, gx), part in res[:5]:
        print('  compat %d  matefrac %.3f  greedy mean %.2f max %d' % (cp, fr, gm, gx), flush=True)
    if res:
        print('  best compat %d, best matefrac %.3f' % (max(r[0][0] for r in res), max(r[0][1] for r in res)), flush=True)
    return res
if __name__ == "__main__":
    out = {}
    cyc = lambda n, off=0: tuple(list(range(off)) + [off + (i + 1) % n for i in range(n)] + list(range(off + n, 13)))
    groups = {
        'Z13': [tuple((i + 1) % 13 for i in range(13))],
        'Z13:Z3': [tuple((i + 1) % 13 for i in range(13)), tuple((3 * i) % 13 for i in range(13))],
    }
    sel = sys.argv[1:] or list(groups)
    for nm in sel:
        out[nm] = run(nm, groups[nm])
    pickle.dump(out, open('sympart_%s.pkl' % '_'.join(sel), 'wb'))
