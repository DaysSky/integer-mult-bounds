"""THE R420-EXTENSION BUILD — STAGE 2a: THE FORMAT-DUMP (ii19_ext2.py).

THE STAGE 1 (ii19_ext.py; SS1914!!) verified the re-base's geometry perfectly (the dims
{0: 1, 1: 120, 2: 180, 4: 70, 6: 180, 8: 120, 9: 1} — THE EXPECTED EXACTLY!!).

THE STAGE 2 needs the EXACT semantics for the gates' re-base + the special's extension:
(a) THE FORMAT-DUMP (this script!): the 'form' field's convention + the 'coords' + the
    'start'/'final' + the gates' structure (the A/B/C/D samples!!) — the re-base's semantics!
"""
import gzip, json, time
from collections import Counter
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

W = json.load(gzip.open('research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
log('(1) the scalars: v=%d h=%d R=%d' % (W['v'], W['h'], W['R']))
log('    format: %r' % (W.get('format'),))
log('    form:   %r' % (W.get('form'),))

# ============ (2) THE COORDS ============
C = W.get('coords')
log('(2) the coords: type %s' % type(C).__name__)
if isinstance(C, list) and C:
    log('    len %d | the entry type %s' % (len(C), type(C[0]).__name__))
    if isinstance(C[0], (list, tuple)):
        log('    the sizes %s' % dict(sorted(Counter(len(c) for c in C).items())))
    for i in (0, 1, 120, 600):
        if i < len(C):
            log('    coords[%d]: %s' % (i, C[i] if len(str(C[i])) < 300 else str(C[i])[:300] + '...'))
elif isinstance(C, dict):
    log('    the keys (%d): %s' % (len(C), list(C.keys())[:20]))
    for k in list(C.keys())[:3]:
        log('    coords[%r]: %s' % (k, str(C[k])[:300]))

# ============ (3) THE START / FINAL ============
S = W.get('start'); F = W.get('final')
log('(3) the start: type %s' % type(S).__name__)
if isinstance(S, list):
    log('    len %d | the samples %s' % (len(S), S[:6]))
elif isinstance(S, dict):
    log('    the keys (%d): %s' % (len(S), list(S.keys())[:20]))
log('    the final: type %s' % type(F).__name__)
if isinstance(F, list):
    log('    len %d | the samples %s' % (len(F), F[:6]))
elif isinstance(F, dict):
    log('    the keys (%d): %s' % (len(F), list(F.keys())[:20]))

# ============ (4) THE GATES (A/B/C/D) ============
for ph in ('A', 'B', 'C', 'D'):
    G = W[ph]
    log('(4) the %s-gates: type %s len %s' % (ph, type(G).__name__, len(G) if G is not None else None))
    if isinstance(G, list) and G:
        for i in (0, 1, 2):
            if i < len(G):
                s = str(G[i])
                log('    %s[%d]: %s' % (ph, i, s if len(s) < 300 else s[:300] + '...'))
        # the gate-size histogram
        if isinstance(G[0], (list, tuple)):
            log('    the gate arities: %s' % dict(sorted(Counter(len(g) for g in G).items())))

# ============ (5) THE RET / SCATTER ============
log('(5) the ret: %s' % (W.get('ret'),))
sc = W.get('scatter')
log('    the scatter: type %s len %s' % (type(sc).__name__, len(sc) if sc is not None else None))
if isinstance(sc, list) and sc:
    for i in range(min(4, len(sc))):
        log('    scatter[%d]: %s' % (i, sc[i]))

# ============ (6) THE FRAMES vs THE START/FINAL RELATION ============
frames = W['frames']
log('(6) the frames: %d | the dims (line-counts!) %s' % (
    len(frames), dict(sorted(Counter(len(f) for f in frames).items()))))
log('DONE — STAGE 2a')
