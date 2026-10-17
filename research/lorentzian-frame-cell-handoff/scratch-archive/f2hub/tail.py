def build(FEED, final):
    w = LWord(); dead = []
    for s in FEED:
        h = w.helper('feeder'); w.gate(1 << s, h, [s]); dead.append(h)
    bcast = collections.defaultdict(list); consume = collections.defaultdict(list)   # demand -> regs / (u, reg)
    for u in range(V):
        chs = lch[u]
        if not chs: continue
        if u in acc:
            AF = acc[u][0]
            ins = [i for i, ch in enumerate(chs) if all(F & ~AF == 0 for F in ch)]
            src_i = max(ins, key=lambda i: len(chs[i])) if ins else None
        else:
            src_i = max(range(len(chs)), key=lambda i: len(chs[i]))
        for i, ch in enumerate(chs):
            if i == src_i: r = u
            else:
                r = w.helper('carrier'); w.gate(1 << u, r, [u])
            pure = (r == u and u in acc)
            for j, F in enumerate(ch):
                Ds = uses_at[u][F]
                last = (j == len(ch) - 1) and not pure
                for k, D in enumerate(Ds):
                    if last and k == len(Ds) - 1: consume[D].append((u, r))
                    else: bcast[D].append(r)
