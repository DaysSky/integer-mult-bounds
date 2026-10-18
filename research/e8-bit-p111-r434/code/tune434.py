"""Run P111-tuned's generic tuner (research/e8-bit-p111-tuned/tune/tune.py, PR #589, imported unchanged) on the R = 434
base word to its fixed point and write the tuned word.  The loop is that of P111-tuned's `apply.py --discover`:
transports, Steinberg 3 -> 2 and frame-only reassignment on A and B, until a pass applies nothing.  D, the scatter,
start and final are never changed; C is rebuilt as the literal reverse of the z-destination gates of A then B.
usage: python -I tune434.py BASE.json.gz OUT.json.gz
Prepared by DaysSky with assistance from Claude; Apache-2.0."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "e8-bit-p111-tuned", "tune"))
import tune  # noqa: E402
import wlib  # noqa: E402

A_FEE = 0.001733        # the fee-table rate P111-tuned's apply.py uses

base = wlib.load(sys.argv[1])
before = wlib.paid(base)
Tn = tune.Tuner(base, a=A_FEE)
total, passes = 0, 0
for _ in range(8):
    n = 0
    for ch in "TSF":
        for sec in "AB":
            V = Tn.view(sec)
            ap = (tune.transport_sweep(V, verbose=False) if ch == "T" else
                  tune.steinberg_sweep(V, verbose=False) if ch == "S" else
                  tune.transport_sweep(V, verbose=False, allow_move=False))
            n += len(ap)
    total += n
    passes += 1
    if not n:
        break
w = Tn.word()
after = wlib.paid(w)        # asserts nested frames and the exact F2 endpoint on all columns
assert sum(k * c for k, c in before.items()) == sum(k * c for k, c in after.items())
sha = wlib.save(w, sys.argv[2])
print("tuner fixed point after %d passes: %d moves; local paid profile %s -> %s; word sha256 %s"
      % (passes, total, before, after, sha))
