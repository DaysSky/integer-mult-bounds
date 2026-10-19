"""The II19 (E8 + special) decoder ladder priced at the record word's own middle shape (W4 tuned), with the
hosting wall R <= 4v.  The 112-line row uses the verified cst-64 decoder (audit_decoder112.py); the 103-line
row needs the double-star copy read at the cut <p'_j>, which bitE8/1 does not provide (in-format cost 7 per copy)."""
from _common import W4T, COPY_W4T, transplant, pct
rows = (('121 = E8 + special (record, cst 73)', 121, {8: 8, 9: 1}),
        ('112 = P111 lines + special (cst 64, in format)', 112, {7: 8, 8: 1}),
        ('103 = double star + special (cst 55, needs a cut format)', 103, {6: 9, 1: 1}))
for nm, v, cop in rows:
    cells = []
    for rho in (3.90, 3.70, 3.50):
        R = min(int(round(rho * v)), 4 * v)
        cells.append('R/v %.2f %+6.2f%%' % (rho, pct(transplant(W4T, COPY_W4T, v, 9, R, cop), v, 9, R)[0]))
    R = 4 * v
    cells.append('wall R=%d %+6.2f%%' % (R, pct(transplant(W4T, COPY_W4T, v, 9, R, cop), v, 9, R)[0]))
    print('%-58s %s' % (nm, '  '.join(cells)))
