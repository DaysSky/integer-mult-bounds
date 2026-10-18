"""THE P111-CLASS WORD BUILD — STAGE 1: THE SYSTEM + THE MAP + THE PROJECTION CHECK!!
(ii19_p111w1.py) — THE FRONTIER-WORD (the crossing at R=420!!).
THE DESIGN: the R420-word PROJECTED to the 111-line puncture (rm = [21,23,24,29,53,71,80,89,103]
(the CST-63 puncture: 9 independent span-7s!!)) + THE SPAN-7 SCATTER-SWAP + THE D-EXTENSION.
THIS STAGE: (0) the loads + the kept-map; (1) the lines/form check (the puncture transfer!!);
(2) the frames re-based; (3) the registers/gates re-map + the prune; (4) THE PROJECTION
IDENTITY CHECK (the R420's balance projected to the 111!!) — the scatter/reads/dirt over
the 111 bits!!
"""
import gzip, json, time
from collections import Counter
W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
W3 = json.load(open('ii19_ext_word3.json', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = [21, 23, 24, 29, 53, 71, 80, 89, 103]          # THE CST-63 PUNCTURE (our hunt!!)
v0, h0, R0 = W['v'], W['h'], W['R']
log('(0) THE R420: v=%d h=%d R=%d | the puncture %s -> v=111!!' % (v0, h0, R0, RM))

# (1) THE LINE-CONVENTION CHECK: the R420's lines vs the word3's lines[0..119]!!
same = all(W['lines'][i] == W3['lines'][i][:8] for i in range(120))
log('(1) the line-order match (the R420 == the word3 roots!!): %s' % same)
# the form: the R420 <x,y>/2 = the word3's ip/2?!
def ip_half(a, b): return sum(x * y for x, y in zip(a, b)) / 2
def ip_full(a, b): return sum(x * y for x, y in zip(a, b))
norms = Counter(ip_half(l, l) for l in W['lines'])
log('    the norms (<x,x>/2!!): %s | the perps (the ip_half == 0!!): %s' % (
    dict(norms),
    dict(sorted(Counter(sum(1 for u in range(120) if u != t and ip_half(W['lines'][t], W['lines'][u]) == 0)
                    for t in range(120)).items()))))

# (2) THE KEPT-MAP: the old line-index -> the new!!
kept = [i for i in range(120) if i not in RM]
old2new = {o: n for n, o in enumerate(kept)}
n = len(kept)
assert n == 111
log('(2) the kept-lines: %d | the map: the line %d -> %d .. the line %d -> %d' % (
    n, kept[0], old2new[kept[0]], kept[-1], old2new[kept[-1]]))

# (3) THE REGISTERS' MAP: the sources (0..119 -> the kept!!), the targets (120..239!!),
#     the helpers (240..659 -> the shift!!): the new: sources 0..110, targets 111..221,
#     the helpers 222..!!  (the old helpers: h -> h - 18!!)
def reg_map(r):
    if r < 120:
        return old2new.get(r, None)                 # the source (None = dropped!!)
    if r < 240:
        t = r - 120
        return old2new.get(t, None) + 111 if t in old2new else None   # the target!!
    return r - 18                                   # the helper (the shift!!)
log('(3) the register-map: the helpers: 240 -> %d | 659 -> %d | the targets: 120 -> %s | the dropped: %s' % (
    reg_map(240), reg_map(659), reg_map(120), RM))

# (4) THE FRAMES re-based: the vectors' lists minus the dropped LINES' vectors!!
frames0 = W['frames']
log('(4) the frames: %d | the lens-census: %s' % (len(frames0),
    dict(sorted(Counter(len(f) for f in frames0).items()))))
dropped_set = {tuple(W['lines'][i]) for i in RM}
def rebase(fr):
    out = []
    for vec in fr:
        tv = tuple(vec)
        if tv in dropped_set: continue
        out.append(list(vec))
    return out
frames = [rebase(f) for f in frames0]
log('    the re-based lens-census: %s' % dict(sorted(Counter(len(f) for f in frames).items())))
# the frames that became empty!!
empt = [i for i, f in enumerate(frames) if not f]
log('    the emptied frames: %d: %s' % (len(empt), empt))

# (5) THE GATES' RE-MAP + THE PRUNE (a quick census!!): the gates touching the dropped!!
def gate_census(gates, nm):
    tot = 0; dropd = 0; dropsrc = 0
    for F, d, srcs in gates:
        tot += 1
        if reg_map(d) is None: dropd += 1
        if any(reg_map(s) is None for s in srcs): dropsrc += 1
    log('    %s: %d gates | the dropped-dest: %d | the dropped-src: %d -> the kept: %d' % (
        nm, tot, dropd, dropsrc, tot - dropd))
gate_census(W['D'], 'D')
gate_census(W['A'], 'A')
gate_census(W['B'], 'B')
gate_census(W['C'], 'C')
log('(5) NOTE: the dropped-src gates: the srcs-LISTS PRUNE (not the whole gates!!)!!')
log('DONE — THE STAGE-1 (the map + the frames + the census!!)')
