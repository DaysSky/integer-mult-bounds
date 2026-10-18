"""THE 2-CLASS BUILD STAGE 6 (ii19_nat59.py) — THE EMISSION SKELETON (the word writer!!).

THE WORD JSON (the pub2-format (the gcheck-convention!!)): {v, h, R, lines, form, frames,
start, final, D, A, ret, scatter, B, C}. THE REGISTERS: 240 sources (r < 240!!) + 240
targets (240 <= r < 480!!) + the helpers (the pieces + the carriers + the 18 retained!!).
THE STARTS: the sources at their singletons (dim 1!!); the targets/helpers at 0.
THE FINALS: the sources + the helpers at FULL (frame 1!!); the targets at their perp-spaces
(nat54's TPERP!!). THE PHASES: D (the doubling!!) -> A (the builds!!) -> the scatter (the
W-rows (nat57!!)) -> B (the target-reads!!) -> C (the reversal!!).
THIS SKELETON: the writer parameterized by the assignments (nat58's!!) — the emission
mechanical once the chains land!!
"""
import os, sys, json
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

FR = json.load(open('ii19_nat54_frames.json', 'rt'))
W57 = json.load(open('ii19_nat57_W.json', 'rt'))
log('the inputs: %d lines | the basis %d | the W %dx%d' % (
    len(FR['lines']), len(W57['BASIS_IDX']), len(W57['W']), len(W57['W'][0])))

def emit_word(pieces, piece_roles, carriers, carrier_srcs, A5x, chains, path):
    """THE EMISSION: pieces = [(lines, users)], the roles = the running-sum triples,
    the carriers = the per-target leftover-assemblers, chains = the read-frames!!"""
    V, H = 240, 10
    lines = FR['lines']
    FRAMES = json.load(open('ii19_nat54_frames.json', 'rt'))
    # the frame list: 0 empty, 1 FULL, the singletons, the t-perps (+ the built cells/rungs!!)
    # THE REGISTERS!!
    nsrc = V; ntgt = V
    npiece = len(pieces); ncar = len(carriers); nret = 18
    R = npiece + ncar + nret
    nreg = 2 * V + R
    ret_base = 2 * V + npiece + ncar
    log('  the registers: %d sources + %d targets + %d pieces + %d carriers + %d retained = R %d (nreg %d!!)' % (
        nsrc, ntgt, npiece, ncar, nret, R, nreg))
    # the starts/finals!!
    start = [0] * nreg
    final = [0] * nreg
    for s in range(V):
        start[s] = 2 + s                    # the singletons (frame idx from nat54!!)
    for r in range(nreg):
        if r < V or r >= 2 * V:
            final[r] = 1                   # the sources + the helpers at FULL!!
    for t in range(V):
        final[V + t] = FR['tperps'][t]      # the targets at their perp-spaces!!
    # THE D-GATES (the doubling: the targets' B-srcs + the scatter-rets pre-read!!)
    # (the y-algebra: the D adds the srcs' self-bits so the later reads' self-bits cancel!!)
    D = []
    # THE A-GATES (the pieces' builds (the running-sums (the roles!!)) + the carriers!!)
    A = A5x
    # THE RET (the 18 retained) + THE SCATTER (the W-rows!!)
    ret = list(range(ret_base, ret_base + nret))
    scatter = W57['W']
    # THE B-GATES (the target-reads (the chains!!))
    B = []
    # THE C (the reversal: the literal reverse of the z-gates (the pub2-convention!!))
    C = []
    w = {'v': V, 'h': H, 'R': R,
         'lines': lines,
         'form': {'num': FR['form_num'], 'den': '1'},
         'frames': FRAMES_IF_NEEDED,
         'start': start, 'final': final,
         'D': D, 'A': A, 'ret': ret, 'scatter': scatter, 'B': B, 'C': C}
    json.dump(w, open(path, 'wt'))
    log('  the word skeleton written: %s (the gates: D %d | A %d | B %d | C %d!!)' % (
        path, len(D), len(A), len(B), len(C)))

# (the driver: completed when nat58's chains land!!)
log('THE EMISSION SKELETON READY (the driver pending nat58!!)')
FRAMES_IF_NEEDED = None
