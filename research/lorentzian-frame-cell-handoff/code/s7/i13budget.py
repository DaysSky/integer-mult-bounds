from mix import price, pct
from maxh import maxH
h, v = 13, 364
for cst in ([12]*13, [13]*13):
    print('I13 cst', sum(cst), 'budget', 8*v - 9*sum(cst))
    for src in ([12], [1,11], [1,2,9]):
        for tg in ([12], [2,10], [1,2,9]):
            row = []
            for brp in ([1,1,11], [1,1,2,9], [1,1,2,3,6]):
                for mp_ in ([13], [2,11], [2,3,8], [1,2,3,7]):
                    M = maxH(h, v, cst, src, tg, [(2*v, 0, brp)], mp_, ge=0)
                    row.append('%s/%s:%s' % ('-'.join(map(str,brp)), '-'.join(map(str,mp_)), '%.2f' % (M/v) if M is not None else 'X'))
            print('  src', src, 'tgt', tg, ' '.join(row), flush=True)
