"""Lift the r434 frontier word (P111 lines, h=8) to a Lorentzian h=9 word on P111 + one special line of norm -2
(E8 + <e - f> inside II_{1,9}; signature (8,1)).

Construction (flow level, checked by the unmodified gcheck):
  * the special decodes as an orthogonal singleton total (the audit's E1 decoder: cst 63 + 1 = 64);
  * a set U of r434 frames carries the special direction (F -> F + <sp>); U must contain the full frame and
    every target perp, be closed upward along every register's chain, and exclude the source singletons,
    frame 0 and the totals' frames with everything before them in the totals' chains;
  * every old register then gains +1 rank exactly once, on its first climb into U, matching the mass identity
    9R + cst + 2v(h-1) = 5762;
  * the special source sits at <sp> (its retained total), the special target reads only that total at the
    scatter and ends at sp-perp = E8.
U is chosen greedily to maximize the nine-stage price.  usage: lift_r434.py [--emit OUT.json]"""
import json, os, sys
from fractions import Fraction as Fr
from collections import Counter
from _common import I13, FRONTIER, price
from mpmath import mp

W = json.load(open(os.path.join(I13, 'ii19_pub2_p111-r434.json')))
v, h, R = W['v'], W['h'], W['R']; nreg = 2 * v + R
def rank(vs):
    m = [[Fr(x) for x in r] for r in vs]; rk = 0
    for c in range(len(m[0]) if m else 0):
        p = next((i for i in range(rk, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[rk], m[p] = m[p], m[rk]
        for i in range(len(m)):
            if i != rk and m[i][c] != 0:
                f = m[i][c] / m[rk][c]; m[i] = [a - f * b for a, b in zip(m[i], m[rk])]
        rk += 1
    return rk
DIMS = [rank(F) if F else 0 for F in W['frames']]
FULL = DIMS.index(h)

# per-register frame sequences (the order of visited frames, as gcheck's climbs see them)
cur = list(W['start']); SEQ = [[W['start'][r]] for r in range(nreg)]
def visit(r, F):
    if cur[r] != F: SEQ[r].append(F); cur[r] = F
for ph in ('D', 'A'):
    for F, d, srcs in W[ph]:
        for r in [d] + srcs: visit(r, F)
for F, d, srcs in W['B'] + W['C']:
    for r in [d] + srcs: visit(r, F)
for r in range(nreg): visit(r, W['final'][r])
SUCC = {}
for s in SEQ:
    for i, F in enumerate(s):
        SUCC.setdefault(F, set()).update(s[i + 1:])
def closure(fs):
    out, stack = set(fs), list(fs)
    while stack:
        F = stack.pop()
        for G in SUCC.get(F, ()):
            if G not in out: out.add(G); stack.append(G)
    return out
TOT_FRAMES = set(W['ret_frames'])
FORBID = {0} | {W['start'][s] for s in range(v)} | TOT_FRAMES
for q in W['ret']:                                    # frames before the totals' retained frames
    s = SEQ[q]; k = s.index(W['ret_frames'][W['ret'].index(q)]); FORBID |= set(s[:k + 1])
TARGET_FINALS = {W['final'][v + t] for t in range(v)}

def hist_of(U):
    hist = Counter()
    for r in range(nreg):
        s = SEQ[r]
        for a, b in zip(s, s[1:]):
            hist[(DIMS[b] + (b in U)) - (DIMS[a] + (a in U))] += 1
    for f in W['ret_frames']: hist[DIMS[f]] += 1      # copies (unlifted)
    hist[1] += 1                                       # the special's singleton copy
    hist[8] += 2                                       # special source <sp> -> full, special target 0 -> E8
    return dict(hist)
def value(U):
    hst = hist_of(U); c, _, d = price(hst, v + 1, h + 1, R)
    return (c if c is not None else mp.mpf(0)), hst

def optimize():
    U = closure({FULL} | TARGET_FINALS)
    assert not (U & FORBID)
    best, hst = value(U); log = [('U_min', len(U), best)]
    cands = sorted(set(range(len(W['frames']))) - FORBID - U)
    improved = True
    while improved:
        improved = False; top = None
        for F in cands:
            if F in U: continue
            add = closure({F}) - U
            if add & FORBID: continue
            c, _ = value(U | add)
            if c > best and (top is None or c > top[0]): top = (c, add)
        if top:
            best = top[0]; U = U | top[1]; improved = True; log.append(('add', len(U), best))
            print('  lifted %d frames: c = %s (%+.3f%% vs frontier)' % (len(U), mp.nstr(best, 12),
                  float((best / FRONTIER - 1) * 100)), flush=True)
    return U, best, log

def emit(U, out):
    sp = [0] * 8 + [1]
    frames = [[x + [0] for x in F] + ([sp] if k in U else []) for k, F in enumerate(W['frames'])]
    SPF = len(frames); frames.append([sp])
    E8F = len(frames); frames.append([x + [0] for x in W['frames'][FULL]])
    num = [row + [0] for row in W['form']['num']] + [[0] * 8 + [-2 * W['form']['den']]]   # special norm -2
    rm = lambda r: r if r < v else (r + 1 if r < 2 * v else r + 2)
    V2 = v + 1; SPS, SPT = v, 2 * V2 - 1
    start = [None] * (2 * V2 + R); final = [None] * (2 * V2 + R)
    for r in range(nreg): start[rm(r)] = W['start'][r]; final[rm(r)] = W['final'][r]
    start[SPS], final[SPS] = SPF, FULL
    start[SPT], final[SPT] = 0, E8F
    g = lambda gl: [[F, rm(d), [rm(s) for s in srcs]] for F, d, srcs in gl]
    word = dict(format='bitGen/1+mut', h=h + 1, v=V2, R=R, form=dict(num=num, den=W['form']['den']),
                lines=[l + [0] for l in W['lines']] + [sp], frames=frames, start=start, final=final,
                D=g(W['D']), A=g(W['A']), B=g(W['B']), C=g(W['C']),
                ret=[rm(q) for q in W['ret']] + [SPS], ret_frames=W['ret_frames'] + [SPF],
                scatter=[list(s) for s in W['scatter']] + [[len(W['ret'])]],
                note='r434 lifted to II_{1,9} (E8 + <-2>), special decoded as an orthogonal singleton; lifted frames %d' % len(U))
    json.dump(word, open(out, 'w'))

if __name__ == '__main__':
    U0 = closure({FULL} | TARGET_FINALS)
    c0, h0 = value(U0)
    print('U_min (full + target perps, up-closed): %d frames, hist %s, c = %s (%+.3f%%)' % (
        len(U0), dict(sorted(h0.items())), mp.nstr(c0, 12), float((c0 / FRONTIER - 1) * 100)), flush=True)
    U, best, _ = optimize()
    hb = hist_of(U)
    print('best: %d lifted frames, hist %s, c = %s (%+.3f%% vs frontier)' % (
        len(U), dict(sorted(hb.items())), mp.nstr(best, 16), float((best / FRONTIER - 1) * 100)))
    if '--emit' in sys.argv:
        out = sys.argv[sys.argv.index('--emit') + 1]
        emit(U, out); print('wrote', out)
