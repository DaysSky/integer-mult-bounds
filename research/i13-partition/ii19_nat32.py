"""THE MOVE+RAISE FAMILY (ii19_nat32.py) — the reordering lever: the last in-place concentration
family on the word4 (the record start: ii19_word4_skip.json, c = 0.001342540624871021312984).

nat28 (raises at fixed order): 0/101,719 — every raise blocked by a co-operand's later
lower-frame need.  HERE: the compound proposal MOVE+RAISE — a gate g whose raise to G fails at a
later gate gj (the blocking register x lifted above a frame it needs there) gets gj MOVED
EARLIER (just before g), if the move is VALUE-SAFE:
  - gj's srcs: no writes to any src in the interval (i, j) -> their values stable;
  - gj's dest: no reads of the dest in (i, j) -> no reader sees the earlier write;
  - the same phase only (A within A, B within B); the ret/scatter boundary untouched.
Then the raise retries; the full replay + the exact price judge; accept iff replay passes and
the price does not fall.  Fixpoint over passes.
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

argv = sys.argv[1:]
sys.argv = ['ii19_nat20.py', argv[0] if argv else 'ii19_word4_skip.json']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
SRC = sys.argv[1]
OUT = argv[1] if len(argv) > 1 else 'ii19_word4_move.json'
FRONT = mp.mpf('0.001744385950814795279853')
R = w['R']
def pc(hist): return price(dict(hist), V, H, R)[0]
PH = ('D', 'A', 'B')

# the write maps: which registers get written where (A and B), for the value-safety checks
writes = {ph: defaultdict(list) for ph in ('A', 'B')}
for ph in ('A', 'B'):
    for gi, (F, d, srcs) in enumerate(w[ph]):
        writes[ph][d].append(gi)
srcwrites = Counter(ph for ph in ('A', 'B') for F, d, srcs in w[ph] if d < V)
log('(0b) source-writing gates: %s (the sources EVOLVE in A/B — the value-safety checks handle them generically!!)' % dict(srcwrites))
assert all(not (V <= d < 2 * V) for F, d, srcs in w['A']), 'H3: no target dests in A'

def word_full(order, re):
    """order: {ph: [gate,...]} the permuted gate lists; re: {(ph,gi-original): frame}."""
    out = {}
    for ph in ('A', 'B'):
        out[ph] = [[re.get((ph, gi), F), d, list(s)] for gi, (F, d, s) in enumerate(w[ph])]
        # apply the permutation: out[ph] as a LIST of gates, reordered
        out[ph] = [out[ph][i] for i in order[ph]]
    out['D'] = w['D']
    return out

def replay_full(order, re):
    saved = {ph: w[ph] for ph in PH}
    G = word_full(order, re)
    w['A'] = G['A']; w['B'] = G['B']
    try:
        return replay(w['A'])
    finally:
        w.update(saved)

def value_safe_move(ph, i, j):
    """move gate j to just after position i (i < j) in phase ph; value-safety checks.
    Returns True if safe (the srcs stable, the dest unread in the interval)."""
    cur = [w[ph][k] for k in order[ph]]
    moved = cur[j]
    Fj, dj, Sj = moved
    interval = cur[i + 1:j]
    for F, d, srcs in interval:
        if d in Sj:
            return False                    # a write to a src inside the interval
        for s in srcs:
            if s == dj:
                return False                # a reader of the dest inside the interval
    return True

def permute(ph, i, j):
    """the order permutation moving j to just after i (i < j)."""
    order = list(range(len(w[ph])))
    val = order.pop(j)
    order.insert(i + 1, val)
    return order

order = {'A': list(range(len(w['A']))), 'B': list(range(len(w['B'])))}
re = {}

def apply_move(ph, i, j):
    """mutate the current order: move j to just after i."""
    val = order[ph].pop(j)
    order[ph].insert(i + 1, val)

# the containers (as nat28)
gframes = sorted(set(F for ph in ('A', 'B') for F, d, s in w[ph]))
conts = {}
for F in gframes:
    conts[F] = sorted((G for G in range(len(fr)) if dims[G] > dims[F] and sub(F, G)),
                      key=lambda G: -dims[G])
log('containers per gate-frame: %d..%d | base c %s' % (
    min(len(conts[F]) for F in gframes), max(len(conts[F]) for F in gframes), mp.nstr(pc(hist0), 22)))
e, hist, _ = replay_full(order, re)
assert e is None
c0 = pc(hist)
log('(0) the record start: %s (%+.4f%% vs the frontier)' % (mp.nstr(c0, 22), float((c0 / FRONT - 1) * 100)))

def cur_gate(ph, pos):
    """the ORIGINAL gate index at position pos in phase ph under the current order."""
    return order[ph][pos]

for pas in range(6):
    e, hist, _ = replay_full(order, re)
    assert e is None
    curbest = pc(hist)
    adm, tried = 0, 0
    for ph in ('A', 'B'):
        n = len(w[ph])
        for pos in range(n):
            gi = cur_gate(ph, pos)
            F, d, srcs = w[ph][gi]
            for G in conts.get(F, ()):
                re2 = dict(re); re2[(ph, gi)] = G
                e2, hist2, _ = replay_full(order, re2)
                tried += 1
                if e2 is None:
                    c2 = pc(hist2)
                    if c2 >= curbest:
                        re, curbest, adm = re2, c2, adm + 1
                        break
                if e2 is not None and e2[0] == 'climb' and e2[1][0] == ph and len(e2[1]) == 2:
                    # the MOVE-REPAIR: the blocking gate position j in the same phase, after pos
                    jpos = e2[1][1]
                    if not (pos < jpos < n):
                        continue
                    if value_safe_move(ph, pos, jpos):
                        order2 = dict(order)
                        saved = list(order2[ph])
                        val = saved.pop(jpos)
                        saved.insert(pos + 1, val)
                        order2[ph] = saved
                        e3, hist3, _ = replay_full(order2, re2)
                        tried += 1
                        if e3 is None:
                            c3 = pc(hist3)
                            if c3 >= curbest:
                                order, re, curbest, adm = order2, re2, c3, adm + 1
                                break
    e, hist, C2 = replay_full(order, re)
    assert e is None
    log('pass %d: admitted %d (trials %d) | c %s (%+.4f%% vs the frontier) | hist %s' % (
        pas, adm, tried, mp.nstr(curbest, 22), float((curbest / FRONT - 1) * 100), dict(sorted(hist.items()))))
    if adm == 0:
        break

e, hist, C2 = replay_full(order, re)
assert e is None
G = word_full(order, re)
word = dict(w); word['A'] = G['A']; word['B'] = G['B']; word['C'] = C2
word['stats'] = dict(w.get('stats', {}), move_raise_reframes=len(re))
json.dump(word, open(OUT, 'w'))
log('emitted %s (c %s, %+.4f%% vs the frontier)' % (OUT, mp.nstr(pc(hist), 22), float((pc(hist) / FRONT - 1) * 100)))
