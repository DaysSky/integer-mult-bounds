"""Stop-entropy budget for I_{11,1} (v=220, h=11) vs P111-tuned.  At fixed R the word beats P111-tuned iff
F(q*) <= 0 at q* = c(P111-tuned), and F is linear in the local histogram: each local jump of size r contributes
w(r) = r (m/r)^q* (times T*L/(mW)).  Baseline = all chains single jumps.  Budget(R) = max extra sum of split costs
Delta(a,b) = w(a) + w(b) - w(a+b) a word may spend.  Printed in units of Delta for common splits."""
from pricer import price, idle_slots, host_greedy, root
from mpmath import mp, mpf
mp.dps = 30
P111t = mpf('0.001733427039589844')
v, h = 220, 11; K, T = 4, 32; L = 2 * K + 1; a = h - 1; m = 1 + L * a; W = 2 * K * v * T
q = P111t
w = lambda r: mpf(r) * (mpf(m) / r) ** q
def F_parts(local, R):
    slots = {}
    for c in idle_slots(K, a): slots[c] = slots.get(c, 0) + 2 * v
    rem = host_greedy(slots, R * L, h, q, m)
    prof = {}
    for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * L
    for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
    tot = sum(prof.values())
    s = sum(mpf(r) * z / (m * W) * (mpf(m) / r) ** q for r, z in prof.items() if r < m)
    s += 32 * m * mpf(tot) / (mpf(10) ** 16 * W) * mpf(m) ** q
    return s - 1
D = lambda a_, b_: w(a_) + w(b_) - w(a_ + b_)
unit = T * L / (m * W)
for R in range(640, 900, 20):
    base = {10: 220 + 220 + 11, 11: R}
    F0 = F_parts(base, R)
    if F0 > 0: print('R', R, 'even single jumps lose'); continue
    budget = -F0 / unit           # allowed sum of Delta over all splits (local units)
    print('R %d budget %.1f  = %.0f x D(1,10) = %.0f x D(2,9) = %.0f x D(1,1) = %.0f x D(5,5)' % (
        R, budget, budget / D(1, 10), budget / D(2, 9), budget / D(1, 1), budget / D(5, 5)), flush=True)
print('Delta values: D(1,10) %.3f D(1,9) %.3f D(2,9) %.3f D(1,1) %.3f D(1,2) %.3f D(5,5) %.3f D(5,6) %.3f D(3,8) %.3f' % tuple(
    float(x) for x in (D(1, 10), D(1, 9), D(2, 9), D(1, 1), D(1, 2), D(5, 5), D(5, 6), D(3, 8))))
def cost(ch):
    return sum(w(b - a_) for a_, b in zip(ch, ch[1:])) - w(ch[-1] - ch[0])
chains = {'src 1-11': [1, 11], 'src 1-2-11': [1, 2, 11], 'src 1-2-3-8-9-11': [1, 2, 3, 8, 9, 11], 'src 1-2-8-9-11': [1, 2, 8, 9, 11],
          'src 1-3-8-11': [1, 3, 8, 11], 'src 1-2-5-11': [1, 2, 5, 11], 'src 1-3-11': [1, 3, 11],
          'car 0-1-2-8-9-10-11': [0, 1, 2, 8, 9, 10, 11], 'car 0-1-2-3-8-9-10-11': [0, 1, 2, 3, 8, 9, 10, 11],
          'car 0-1-3-8-10-11': [0, 1, 3, 8, 10, 11], 'car 0-1-2-11': [0, 1, 2, 11],
          'emp 0-9-10-11': [0, 9, 10, 11], 'emp 0-8-10-11': [0, 8, 10, 11], 'emp 0-3-8-10-11': [0, 3, 8, 10, 11], 'emp 0-9-11': [0, 9, 11],
          'tgt 0-1-10': [0, 1, 10], 'tgt 0-9-10': [0, 9, 10], 'tgt 0-1-9-10': [0, 1, 9, 10], 'tgt 0-2-9-10': [0, 2, 9, 10]}
print('chain split costs in budget units (budget(720) = 23.9 for all 1171 chains):')
for k, ch in chains.items(): print('  %-26s %.4f' % (k, float(cost(ch))))
