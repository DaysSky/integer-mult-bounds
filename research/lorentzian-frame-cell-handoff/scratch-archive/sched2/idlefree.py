"""Rigorous upper bound for any schedule with K pairs (s = 2K + 1 locals, P111-tuned local word): drop every idle
remainder (idle children free, every helper residual hosted at no cost).  The root only decreases when paid children
are added, so this bounds every layout, every hosting and every bank choice."""
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
from mpmath import mpf
ref = mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
T = 32; v = 111
for K in range(2, 11):
    s = 2 * K + 1; m = 1 + 7 * s; W = 2 * K * v * T
    prof = {r: z * T * s for r, z in tuned.items()}
    # mass identity: idle mass and residuals are dropped, so the true deficit D = mW - (full mass) is used directly:
    D = T * (2 * K * v - s * 63)
    # root of sum z_r g_q(r) = D with only local children
    lo, hi = mpf(0), mpf('0.05')
    def F(q): return sum(z * r * ((mpf(m) / r) ** q - 1) for r, z in prof.items()) - D
    for _ in range(200):
        mid = (lo + hi) / 2
        if F(mid) > 0: hi = mid
        else: lo = mid
    print('K', K, 's', s, 'idle-free upper bound', float(lo), '%+.2f%% vs P111-tuned' % float((lo / ref - 1) * 100))
