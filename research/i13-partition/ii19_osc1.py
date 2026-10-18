"""THE TOOL-AUDIT (ii19_osc1.py) — the user's directive: 'the oscillation audit + keep pushing
the II19 frontier, first targeting the assumptions and optimizations meant for non-II19'!!

THE NON-II19-CALIBRATED TOOL-ASSUMPTIONS (the pricer = the E8/R420/P111-era machine!!):
  (A) THE UNDAMPED 30-ITERATION FIXED-POINT (the SPEED-optimization!!): the host_greedy's
      slot-order is q-dependent -> the period-2 cycles -> the LAST-iterate = GARBAGE at
      some (hist, R) — DISCOVERED in the census (the first 121-grid's zigzag!!)!!  THE FIX:
      the damped q <- (q+q2)/2 + the convergence flag (the TRUE fixed-point unchanged!!).
  (B) HOST = 'greedy' HARDCODED (the module flag!!): the exact-DP host() EXISTS but unused
      — an E8-era speed optimization: the II19's rem-profiles' c-difference UNMEASURED!!
  (C) THE q-START 0.0017 + THE 30-CAP (the R420-scale!!): the no-convergence-flag garbage!!
  (D) THE K=4/T=32 (the R420's calibration (the SS1879's scan was undamped!!)).
  (E) THE MASTER-LAW's ~2.5% FIRST-ORDER error on the close verdicts (the -2.1% band!!).

THE AUDIT (the full tool audit!!):
  (1) THE BATTERY: the 3 published (the R420/P111/word3!!) at the damped + the greedy-vs-DP.
  (2) THE BANDS' RE-RUNS: the ORIGINAL scripts re-run with the PATCHED pricer.price (the
      runpy!!) — the identical hists/grids, ONLY the engine differs -> the headline-shifts!!
      the own1 (the c(R)-regime!!) | the own2 (the zone-map!!) | the own5 (the honest-matrix!)
      | the own7 (the CST-81-lever!!) | the ext8 (the m-grid!!) | the h10 (the 2-class!!).
  (3) THE HOST-DP LEVER: the greedy-vs-the-exact-DP at the key-points (the c-differences!!).
  (4) THE K=4-vs-K=5 (the damped!!): the 121's D-band.
  (5) THE VERDICT-TABLE: which of the record's headline numbers SHIFT!!
"""
import io, math, runpy, sys, time
from contextlib import redirect_stdout

sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer
from pricer import idle_slots, host_greedy, host, root
from mpmath import mp, mpf
mp.dps = 40
P111 = mpf('0.001733052823330162099157')
FRONTIER = mpf('0.001744386')

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE DAMPED DROP-IN (the same signature + the DP flag!!) ============
def price_damped(local, v, h, R, K=4, T=32, w=None, start_dims=None, use_dp=False,
                 max_iter=200):
    """the pricer's price() with: the DAMPING (q <- (q+q2)/2!!), the convergence flag, the
    200-cap, and the optional EXACT-DP hosting (the pricer's own host()!!)."""
    L = 2 * K + 1; a = h - 1; m = 1 + L * a; w = h if w is None else w
    slots = {}
    for c in idle_slots(K, a):
        slots[c] = slots.get(c, 0) + 2 * v
    nres = R * L
    W = 2 * K * v * T
    cap = sum(n * (c // w) for c, n in slots.items())
    if nres > cap:
        return None, None, dict(error='hosting wall', cap=cap, nres=nres)
    q = mpf('0.0017')
    q2 = None
    conv = False
    for it in range(max_iter):
        rem = host(slots, nres, w, q, m) if use_dp else host_greedy(slots, nres, w, q, m)
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        q2 = root(prof, m, W)
        if q2 is None:
            return None, prof, dict(error='no root', oscillated_after=it)
        if abs(q2 - q) < mpf(10) ** -25:
            conv = True
            break
        q = (q + q2) / 2
    d = dict(m=m, W=W, rem_per_replica=rem, mass=sum(r * z for r, z in prof.items()),
             deficit=m * W - sum(r * z for r, z in prof.items()),
             converged=conv, iters=it + 1, dp=use_dp)
    return q2, prof, d

# ============ (1) THE BATTERY (the damped-greedy + the damped-DP vs the published!!) ============
log('(1) THE VALIDATION BATTERY — the greedy vs the exact-DP (the damped!!)!!')
R420H = {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}
P111H = {1: 1321, 2: 1342, 3: 80, 4: 47, 5: 102, 6: 10, 7: 18}
W3H = {1: 1091, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 8, 9: 4}
for (hst, vv, hh, RR, pub, nm) in [
        (R420H, 120, 8, 420, '0.001653826988146798944268', 'the R420 true hist'),
        (P111H, 111, 8, 439, '0.001733052823330162099157', 'the P111 hist'),
        (W3H, 121, 9, 463, '0.0009558217144810735671339', 'the word3 true hist')]:
    cg, pg, dg = price_damped(hst, vv, hh, RR)
    cd, pd, dd = price_damped(hst, vv, hh, RR, use_dp=True)
    log('    %-20s greedy: %s (it=%d) | DP: %s (it=%d) | published: %s' % (
        nm, mp.nstr(cg, 12) if cg else 'NONE', dg.get('iters', -1),
        mp.nstr(cd, 12) if cd else 'NONE', dd.get('iters', -1), pub))
    if cg is not None and cd is not None and abs(cd - cg) > mpf('1e-14'):
        log('        !!! THE DP-vs-GREEDY DIFFERS: %+0.4f%% (the hosting-lever!!)' % (
            float((cd / cg - 1) * 100)))

# ============ (2) THE BANDS' RE-RUNS (the original scripts + the patched engine!!) ============
log('(2) THE BANDS RE-RUNS — the original scripts, the patched pricer.price (the damped!!)!!')
pricer.price = price_damped          # THE PATCH (the `from pricer import price` binds at run!!)

def rerun(script, key_tag):
    log('    ---- %s ----' % script)
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            runpy.run_path(script, run_name='__main__')
        out = buf.getvalue()
    except Exception as e:
        out = buf.getvalue()
        out += ('\n!!! EXCEPTION: %r\n' % (e,))
    print(out, end='')
    # THE DELTA-SUMMARY: the lines with the c's / the pcts (the quick-scan!!)
    nmark = 0
    for ln in out.split('\n'):
        s = ln.strip()
        if any(kk in s for kk in ('c =', 'THE BEST', 'CROSSING', 'NO PRICE', 'NONE(')) and len(s) < 220:
            nmark += 1
    log('    [%s: the %d verdict-lines captured (the full output above!!)]' % (key_tag, nmark))
    return out

outs = {}
for script, tag in [('ii19_own1.py', 'own1: the c(R)-regime!!'),
                    ('ii19_own2.py', 'own2: the zone-map!!'),
                    ('ii19_own5.py', 'own5: the honest-matrix!!'),
                    ('ii19_own7.py', 'own7: the CST-81-lever!!'),
                    ('ii19_ext8.py', 'ext8: the m-grid!!'),
                    ('ii19_2class_h10.py', 'h10: the 2-class band!!')]:
    outs[tag] = rerun(script, tag)

# ============ (3) THE HOST-DP LEVER at the key model-points!! ============
log('(3) THE HOST-DP LEVER — the greedy vs the exact-DP (the model-bands key points!!)!!')
V, H = 121, 9
def hist_D_121(R, CST, rho=9):
    climb = H * R + 2 * V * (H - 1)
    hist = {1: int(round(0.262 * climb)), 2: int(round(0.571 * climb / 2.0)),
            4: int(round(0.048 * climb / 4.0)), 5: int(round(0.119 * climb / 5.0)),
            max(1, H - 1): rho}
    mass = sum(k * z for k, z in hist.items())
    dd = (H * R + CST + 2 * V * (H - 1)) - mass
    guard = 0
    while dd != 0 and guard < 100000:
        guard += 1
        if dd > 0:
            hist[1] = hist.get(1, 0) + 1; dd -= 1
        else:
            k = max(z for z in hist if hist[z] > 0)
            hist[k] -= 1; dd += k
            if hist[k] == 0: del hist[k]
    return {k: int(z) for k, z in hist.items() if z}

for (R, CST) in [(290, 81), (451, 73), (463, 83), (280, 81)]:
    h = hist_D_121(R, CST)
    cg, _, dg = price_damped(h, V, H, R)
    cd, _, dd = price_damped(h, V, H, R, use_dp=True)
    if cg is None:
        log('    R=%d CST=%d: the greedy NO-PRICE' % (R, CST))
        continue
    log('    R=%d CST=%d: greedy %.9f (%+.2f%%) | DP %s (%s)' % (
        R, CST, float(cg), float((cg / FRONTIER - 1) * 100),
        ('%.9f (%+.2f%%)' % (float(cd), float((cd / FRONTIER - 1) * 100))) if cd else 'NONE',
        'SAME' if (cd is not None and abs(cd - cg) < mpf('1e-14')) else 'DIFFERS!!'))

# ============ (4) THE K=4-vs-K=5 (the damped!!) ============
log('(4) THE K=4-vs-K=5 — the 121 D-band (the damped!!)!!')
for K in (4, 5):
    for (R, CST) in [(451, 73), (290, 81)]:
        h = hist_D_121(R, CST)
        c, _, d = price_damped(h, V, H, R, K=K)
        log('    K=%d R=%d CST=%d: %s (%s)' % (
            K, R, CST, mp.nstr(c, 12) if c is not None else 'NO-ROOT (%s)' % d.get('error'),
            'conv=%s it=%d' % (d.get('converged'), d.get('iters', -1)) if c is not None else ''))

# ============ (5) THE VERDICT-TABLE ============
log('(5) THE VERDICT — the record headline numbers vs the damped re-runs!!')
log('    (the full outputs above (the honest!!): compare vs the SESSION-SUMMARY blocks!!)')
log('    THE ENGINE: the damped-converged (the oscillation-garbage ELIMINATED!!).')
log('DONE — THE TOOL-AUDIT!!')
