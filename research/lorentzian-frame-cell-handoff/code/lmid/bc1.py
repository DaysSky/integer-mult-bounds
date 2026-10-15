"""Broadcaster/collector prototype (support level, exact frame nesting).
Broadcasters: every system cell C sends its two branch registers (x_s, x_a) up a nested chain of frames
   C = Y0 < Y1 < ... (each Y_{k+1} = pp(Y_k u D) for a system cell D, nondegenerate); a broadcaster is never modified,
   so line u is AVAILABLE at every frame on any of its broadcasters' chains.
Readers: each target t owns K chains of nested frames inside t-perp (its own in-chain chain + K-1 collector registers
   delivered at t-perp); a chain reads every needed line available at its frames.  Lines of R(t) must be covered.
Here: broadcaster chains chosen greedily (frames shared by many targets' perps first), then per target a greedy set of
nested chains over the frames where t's lines are available.  Reports collectors needed per target.
usage: bc1.py SYSTEM.json [depth]"""
import sys, os, json, collections, itertools, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lw import V, g, bits, dim, nondegenerate, FULL
HYP = g.HYP
pc = lambda m: bin(m).count('1')
random.seed(1)
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
DEPTH = int(sys.argv[2]) if len(sys.argv) > 2 else 4
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = FULL
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
def pp(m): return pm(pm(m))
ND = {}
def ok(N):
    r = ND.get(N)
    if r is None: r = nondegenerate(N); ND[N] = r
    return r
# ---- broadcaster chains: grow each cell's chain by adding the cell whose pp-closure keeps the largest perp
avail = collections.defaultdict(int)        # frame -> mask of lines available there
chains_b = {}
for C in cells:
    for s in bits(C):
        Y = C; ch = [C]; avail[C] |= 1 << s
        for d in range(DEPTH):
            best = None
            for D in random.sample(cells, 60):
                if D & ~Y == 0: continue
                Y2 = pp(Y | D)
                if Y2 == FULL or not ok(Y2): continue
                b = pc(pm(Y2))
                if b < 8: continue
                sc = b * pc(Y2 & ~Y) ** 0.5
                if best is None or sc > best[0]: best = (sc, Y2)
            if best is None: break
            Y = best[1]; ch.append(Y); avail[Y] |= 1 << s
        chains_b[(C, s)] = ch
frames = list(avail)
print('broadcaster chains built; frames', len(frames), 'avg lines available per frame',
      sum(pc(a) for a in avail.values()) / len(frames), flush=True)
# subset relation among frames (for nested reader chains)
fr_by_t = {}
need_coll = collections.Counter(); uncovered_total = 0
for t in range(V):
    R = HYP[t]
    F = [X for X in frames if X & ~R == 0 and avail[X] & R]
    left = R; nch = 0
    while left and nch < 12:
        # greedy nested chain: start from best frame, then extend up/down by inclusion picking max new coverage
        best_chain = None
        for X0 in F:
            cur = [X0]; got = avail[X0] & left
            # extend upward greedily
            top = X0
            while True:
                ups = [X for X in F if top & ~X == 0 and X != top]
                if not ups: break
                X1 = max(ups, key=lambda X: pc(avail[X] & left & ~got))
                if not (avail[X1] & left & ~got): break
                cur.append(X1); got |= avail[X1] & left; top = X1
            if best_chain is None or pc(got) > pc(best_chain[1]): best_chain = (cur, got)
        if best_chain is None or not best_chain[1]: break
        left &= ~best_chain[1]; nch += 1
    need_coll[nch] += 1; uncovered_total += pc(left)
    if t % 20 == 0: print(t, g.kind[t], '|R|', pc(R), 'chains used', nch, 'uncovered', pc(left), flush=True)
print('chains per target (own + collectors):', sorted(need_coll.items()), 'uncovered lines total', uncovered_total)
