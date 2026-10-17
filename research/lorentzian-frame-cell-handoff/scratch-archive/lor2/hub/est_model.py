"""Helper-adjusted estimate of the achievable saving a for a unit family (MODEL, not a bound).

The #595 ceiling X(s, h, x) is helper-free.  On the realised E8 words the gap to the ceiling is 87-93% helper cost
(#595 A.5).  This model puts the helpers back with the piece statistics of the shipped words and solves the same
pressure root, so that unit families can be compared at the same design maturity:

  per port and replica (v = 1), stage count s = 2K + 1, a = h - 1, m = 1 + s a, D = (s - 1) - s x   (#595 A.1, k = 1)
  data      2 s a mass, cut into pieces with the per-port run histogram of the shipped word
            (bit: #555 x/y runs; complex: #569 four-cold data runs, as replayed by #595 a4_gap.py)
  copies    s x mass in children of rank h - 1 (#555: 9 x 7, #568: 8 x 8)
  helpers   rho = R / v helpers per port, each climbing h per stage, cut with the shipped helper run histogram
            (bit: #555, complex: #568's implied helper histogram, both from #595 a4_gap.py)
  idle      the B_K idle slots (skel.idle_slots, 2 per port), hosting: the helper mass is hosted into the largest idle
            slots first; a hosted slot of rank r leaves a remainder child of rank r / a (the #555 pattern: 42, 28, 14 ->
            6, 4, 2); helper mass beyond the hostable mass stays as extra paid children (#595 step D semantics)
Piece-size scaling to another window h:
  'abs'  pieces keep the shipped absolute ranks (their number grows like h)            -- pessimistic for large h
  'rel'  pieces scale with the window (rank x a/a_ref; same number of stops per register) -- optimistic
Calibration: the model is run on the E8 words themselves (bit h 8, x 63/111, rho 439/111; complex h 9, x 64/112,
rho 496/112) and the ratio to the published value (1.7331e-3 / 1.5987e-3, #595 A.5) is reported; the same factor is
applied to every candidate of that side (a_cal).
Also printed: #634's loss-chain factors 1/m, D/W (W = 2K v, whole hosting), L_ent = ln m - E ln r on the model profile.
"""
import math
import sys
from fractions import Fraction as Fr

REPO = sys.argv[1] if len(sys.argv) > 1 else None
if REPO:
    sys.path.insert(0, REPO + '/research/format-limits/scripts')
sys.dont_write_bytecode = True
from skel import idle_slots             # noqa: E402

# shipped piece statistics (checked by #595 a4_gap.py: A4.runs.#555, A4.data.#568, A4.inputs.#568)
BIT = dict(h=8, v=111, R=439,
           data={1: 10 + 317, 2: 209 + 92, 3: 10, 4: 3, 5: 92, 6: 10, 7: 9},            # x + y runs per stage
           helpers={1: 994, 2: 1041, 3: 70, 4: 44, 5: 10}, published=Fr(17331, 10 ** 7), x=Fr(63, 111), s=9)
CX = dict(h=9, v=112, R=496,
          data={1: 718, 2: 74, 3: 60, 4: 92, 5: 42, 6: 28},                                # per call, v = 112
          helpers={1: 115952, 2: 26320, 3: 28064, 4: 7072, 5: 1008, 6: 2016}, published=Fr(15987, 10 ** 7),
          x=Fr(64, 112), s=9)


def _norm(hist, mass):
    tot = sum(r * z for r, z in hist.items())
    return {Fr(r): Fr(z) * mass / tot for r, z in hist.items()}


def profile(side, h, x, rho, s, mode):
    ref = BIT if side == 'bit' else CX
    a, K = h - 1, (s - 1) // 2
    m = 1 + s * a
    D = (s - 1) - s * Fr(x)
    scale = Fr(a, ref['h'] - 1) if mode == 'rel' else Fr(1)
    prof = {}

    def add(r, n):
        r = Fr(r)
        if n <= 0 or r >= m:
            return
        prof[r] = prof.get(r, 0) + n
    # data: 2 s a mass with the reference run shape
    for r, n in _norm(ref['data'], 2 * s * a).items():
        rr = min(r * scale, a)
        add(rr, n * r / rr)                       # keep the mass of each class
    # copies
    add(a, Fr(s) * Fr(x) / a)
    # helpers
    hmass = Fr(rho) * s * h
    hsc = Fr(h, ref['h']) if mode == 'rel' else Fr(1)
    for r, n in _norm(ref['helpers'], hmass).items():
        rr = min(r * hsc, h)
        add(rr, n * r / rr)
    # idle with hosting
    slots = sorted([r for r in idle_slots(K, a) for _ in range(2)], reverse=True)
    left = hmass
    for r in slots:
        rem = Fr(r, a)                           # remainder piece of a hosted slot
        cap = r - rem
        if left >= cap:
            left -= cap
            add(rem, 1)
        elif left > 0:
            add(r - left, 1)                    # partially hosted slot: one paid child of the rest
            left = 0
        else:
            add(r, 1)
    return prof, m, D


def root(prof, m, D, iters=200):
    m = float(m); D = float(D)
    F = lambda q: sum(float(z) * float(r) * ((m / float(r)) ** q - 1) for r, z in prof.items())
    lo, hi = 0.0, 0.5
    for _ in range(iters):
        mid = (lo + hi) / 2
        if F(mid) >= D:
            hi = mid
        else:
            lo = mid
    return hi


def chain(prof, m, D, s):
    """#634 loss chain on the model profile: a ~ (1/m)(D/W)/L_ent with W = (mass + D)/m data-equivalent wires per port
    (= 2K when every helper is hosted) and L_ent = ln m - E ln r (rank-weighted)."""
    mass = sum(float(r * z) for r, z in prof.items())
    W = (mass + float(D)) / float(m)
    Eln = sum(float(r * z) * math.log(float(r)) for r, z in prof.items()) / mass
    Lent = math.log(float(m)) - Eln
    return dict(inv_m=1 / float(m), W=W, DW=float(D) / W, Lent=Lent, first=float(D) / W / float(m) / Lent)


def estimate(side, h, x, rho, mode, S=range(3, 26, 2)):
    best = None
    for s in S:
        prof, m, D = profile(side, h, x, rho, s, mode)
        if D <= 0:
            continue
        a = root(prof, m, D)
        if best is None or a > best[1]:
            best = (s, a, chain(prof, m, D, s))
    return best


def calibration(side, mode):
    ref = BIT if side == 'bit' else CX
    prof, m, D = profile(side, ref['h'], ref['x'], Fr(ref['R'], ref['v']), ref['s'], mode)
    return float(ref['published']) / root(prof, m, D)


if __name__ == '__main__':
    for side in ('bit', 'complex'):
        for mode in ('abs', 'rel'):
            print(side, mode, 'calibration factor (published / model at s = 9): %.4f' % calibration(side, mode))
