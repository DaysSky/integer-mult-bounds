def build(FEED, final):
    w = LWord(); dead = []
    kneed = sorted({choice[t][3] for t in left if choice[t][3] >= 0 and srcdef.get(t) != choice[t][3]})
    keeper = {}
    for d in kneed:
        h = w.helper('keeper'); w.gate(1 << d, h, [d]); keeper[d] = h
    bkeeper = {}
    for t, v in block_of.items():
        if srcdef.get(t) != v[4]:
            h = w.helper('keeper'); w.gate(1 << v[4], h, [v[4]]); bkeeper[t] = h
    for s in FEED:
        h = w.helper('feeder'); w.gate(1 << s, h, [s]); dead.append(h)
    bcast = collections.defaultdict(list); consume = collections.defaultdict(list)   # demand -> regs / (u, reg)
    for u in range(V):
        chs = lch[u]
        if not chs: continue
        src_i = None
        if u in provider:
            t = provider[u]
            ins = [i for i, ch in enumerate(chs) if all(F & ~HYP[t] == 0 for F in ch)]
            src_i = max(ins, key=lambda i: len(chs[i])) if ins else None
        else:
            src_i = max(range(len(chs)), key=lambda i: len(chs[i]))
        for i, ch in enumerate(chs):
            if i == src_i: r = u
            else:
                r = w.helper('carrier'); w.gate(1 << u, r, [u])
            pure = (r == u and u in provider)
            for j, F in enumerate(ch):
                Ds = uses_at[u][F]
                last = (j == len(ch) - 1) and not pure
                for k, D in enumerate(Ds):
                    if last and k == len(Ds) - 1: consume[D].append((u, r))
                    else: bcast[D].append(r)
    regs = {}; take = collections.Counter(); asm = {}
    LAZY = os.environ.get('LAZY', '1') == '1'
    pool = collections.defaultdict(list); master = {}; reused = set()
    uses_left = collections.Counter()
    for D in dlist:
        for C in children[D]:
            if C not in set(hops.get(D, [])): uses_left[C] += 1
    qout = {}
    creg = {}
    def chain_reg(P, C, F):
        k, first, last = prole[(P, C)]
        if first:
            if k == pmaster[C]: r = master[C]
            else:
                r = None; lst = pool.get(content[C], [])
                for k2, x in enumerate(lst):
                    if w.cur[x] & ~F == 0 and w.xpart(x) == content[C]:
                        r = x; del lst[k2]; reused.add(x); break
                if r is None:
                    r = w.helper('copy'); w.gate(GFR[C], r, [master[C]])
            creg[(C, k)] = r
        return creg[(C, k)], last
    for D in dlist:
        if D in QFR:
            i = D[1]; F = QFR[D]; X, inp, inl, outs = quads[i]
            ins = [r for (u, r) in consume[D]]
            bpc = {}
            for C in children[D]:
                if PCH:
                    r, last = chain_reg(D, C, F)
                    if last: ins.append(r)
                    else: bpc[C] = r
                    continue
                r = None; lst = pool.get(content[C], [])
                for k2, x in enumerate(lst):
                    if w.cur[x] & ~F == 0 and w.xpart(x) == content[C]:
                        r = x; del lst[k2]; reused.add(x); break
                uses_left[C] -= 1
                if r is None:
                    if uses_left[C] == 0: r = master[C]
                    else:
                        r = w.helper('copy'); w.gate(GFR[C], r, [master[C]])
                elif uses_left[C] == 0:
                    dead.append(master[C]); pool[content[C]].append(master[C])
                ins.append(r)
            bl = {u: r for (u, r) in [(w.xpart(r).bit_length() - 1, r) for r in bcast[D]]}
            targets = []
            for (Dt, v, tt) in outs:
                bpart = 0
                for t in tt:
                    if t[0] == 'L' and t[1] in bl: bpart |= 1 << t[1]
                    if t[0] == 'P' and t[1] in bpc: bpart ^= content[t[1]]
                targets.append(v ^ bpart)
            res, dd = frame_alg(w, F, ins, targets, 'quad')
