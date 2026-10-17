    w.ret = totals; w.phase = 'B'
    for (t, a, b, c) in FR:                                        # in-chain reads (shared registers)
        for (x, y) in ((t, a), (b, c)):
            for z in (x, y):
                if not INQ:
                    DQ = topQ[(t, a, b, c)]; w.gate(DQ[0], V + z, [regs[DQ][0]])
                DI = topIN[(x, y)]; w.gate(DI[0], V + z, [regs[DI][0]])
    for (t, a, b, c) in FR:
        for z in (t, a, b, c):
            s, DX = deliv[z]
            w.gate(HYP[z], V + z, [s, regs[DX][0]])
    for t in punct:
        w.gate(HYP[t], V + t, [regs[topP[t]][0]])
    for t in range(V): assert w.xpart(V + t) == HYP[t], ('target content', t)
    w.finish()
    return w, [], dict(after_top=nh_top, R=w.nh)
w, missing, _ = build([], False)
log('pass 1: helpers before totals', w.nh, '| feeder lines', len(missing))
if os.environ.get('EVAL') == '1':
    print("EVAL {'R': %d}" % (w.nh + len(missing) + 11)); sys.exit(0)
w, _, stats = build(missing, True)
scatter = [[i for i in range(11) if g.binlabel(t) >> i & 1] for t in range(V)]
w.emit(scatter, [FULL] * 11, OUT)
log('EMITTED', OUT, stats, '| roles', dict(collections.Counter(w.role.values())))
