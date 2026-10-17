"""Break-even R (bank-aware shape model, code/price/bebank.py) for h = 9 systems of v lines and decoder cost cst,
against P111-tuned, with E8/P111 controls at h = 8."""
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import bebank as BE
rows = [('E8 h8', 8, 120, 72), ('P111 h8', 8, 111, 63), ('O- h9 cst72', 9, 136, 72), ('O- h9 cst81', 9, 136, 81),
        ('O- h9 cst64', 9, 136, 64), ('O- 128 cst72', 9, 128, 72), ('h9 119 cst72', 9, 119, 72)]
for name, h, v, cst in rows:
    for ks, kt, kh in ((3, 2, 3), (5, 2, 5), (4, 3, 4)):
        r0 = BE.be(h, v, cst, ks, kt, kh, 0)
        print('%-14s stops %d/%d/%d  break-even R (all frame-0): %s  (%s)' % (name, ks, kt, kh, r0, ('%.2fv' % (r0 / v)) if r0 else '-'), flush=True)
