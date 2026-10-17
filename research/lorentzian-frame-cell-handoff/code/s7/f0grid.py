from maxh import maxH
h, v = 11, 220
for cstp in ([11]*11, [10]*11):
    print('frame-0 world, cst', sum(cstp))
    for src in ([1,9], [1,2,7], [1,2,3,4]):
        for tg in ([10], [2,8], [1,2,7]):
            row = []
            for brp in ([1,1,9], [1,1,2,7], [1,1,2,3,4]):
                for mp_ in ([11], [2,9], [2,3,6], [1,2,3,5]):
                    M = maxH(h, v, cstp, src, tg, [(2*v, 0, brp)], mp_, ge=0)
                    row.append('%s/%s:%s' % ('-'.join(map(str,brp)), '-'.join(map(str,mp_)), '%.2f' % (M/v) if M is not None else 'X'))
            print('  src', src, 'tgt', tg, ' '.join(row), flush=True)
