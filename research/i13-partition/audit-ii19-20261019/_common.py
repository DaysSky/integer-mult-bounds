"""Shared helpers for the 2026-10-19 II19 audit (repo-relative paths; pricer and gcheck are used unmodified)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
I13 = os.path.join(REPO, 'research', 'i13-partition')
PRICER_DIR = os.path.join(REPO, 'research', 'lorentzian-frame-cell-handoff', 'code', 'price')
GCHECK = os.path.join(REPO, 'research', 'lorentzian-frame-cell-handoff', 'code', 'tword', 'gcheck.py')
sys.path.insert(0, PRICER_DIR)
from pricer import price  # noqa: E402
from mpmath import mp  # noqa: E402
FRONTIER = mp.mpf('0.001744385950814795279853')   # r434, the bit frontier the II19 record compares against

R434 = {1: 1311, 2: 1339, 3: 69, 4: 45, 5: 103, 6: 12, 7: 18}; COPY_R434 = {7: 9}
W4T = {1: 1151, 2: 1719, 3: 252, 4: 83, 5: 18, 6: 43, 7: 10, 8: 18, 9: 2}; COPY_W4T = {8: 8, 9: 1}
R420 = {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}; COPY_R420 = {8: 9}


def transplant(base, base_copies, v, h, R, copies):
    """Keep the base word's climb-shape proportions (by count), rescale the climbs to the mass identity
    h R + 2 v (h - 1), then add the new copy children.  A model, not a word (calibrated in audit_pricer.py)."""
    climb = {r: z - base_copies.get(r, 0) for r, z in base.items()}
    cm = sum(r * z for r, z in climb.items()); target = h * R + 2 * v * (h - 1)
    hist = {r: int(z * target / cm) for r, z in climb.items()}
    hist[1] += target - sum(r * z for r, z in hist.items())
    for r, z in copies.items(): hist[r] = hist.get(r, 0) + z
    return hist


def pct(hist, v, h, R, K=4, ref=FRONTIER):
    c, _, d = price(hist, v, h, R, K=K)
    return (float((c / ref - 1) * 100), c) if c is not None else (None, d.get('error'))
