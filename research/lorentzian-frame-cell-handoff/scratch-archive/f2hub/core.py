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
            for k2, (Dt, v, tt) in enumerate(outs):
                r = res[k2]
                need = [bl[t[1]] for t in tt if t[0] == 'L' and t[1] in bl] + [bpc[t[1]] for t in tt if t[0] == 'P' and t[1] in bpc]
                if need: w.gate(F, r, need)
                assert w.xpart(r) == v
                qout[(i, Dt)] = r
            dead += dd
            for x in dd: pool[w.xpart(x)].append(x)
            continue
        F, Y = GFR[D], D[1]
        ins = [r for (u, r) in consume[D]]
        for (i, v) in qparts.get(D, []): ins.append(qout[(i, D)])
        hset = set(hops.get(D, []))
        bpc = []; bvec = 0
        for C in children[D]:
            if C in hset: continue
            if PCH and C not in TOPSET:
                r, last = chain_reg(D, C, F)
                if last: ins.append(r)
                else: bpc.append(r); bvec ^= content[C]
                continue
            if LAZY and C not in TOPSET:
                r = None; lst = pool.get(content[C], [])
                for i, x in enumerate(lst):
                    if w.cur[x] & ~F == 0 and w.xpart(x) == content[C]:
                        r = x; del lst[i]; reused.add(x); break
                uses_left[C] -= 1
                if r is None:
                    if uses_left[C] == 0: r = master[C]
                    else:
                        r = w.helper('copy'); w.gate(GFR[C], r, [master[C]])
                elif uses_left[C] == 0:
                    dead.append(master[C]); pool[content[C]].append(master[C])
                ins.append(r)
            else:
                ins.append(regs[C][take[C]]); take[C] += 1
        if D in asm: ins.append(asm[D])
        tv = covered[D]
        for (u, r) in consume[D]: tv ^= 1 << u
        tv ^= bvec
        nout = 1 if (LAZY and D not in TOPSET) else demand[D]
        if ins:
            res, dd = frame_alg(w, F, ins, [tv] * nout, 'flat')
        else:
            assert tv == 0
            res = {k: w.helper('empty@flat') for k in range(nout)}; dd = []
        regs[D] = [res[k] for k in range(nout)]; dead += dd
        if bpc:
            for r in regs[D]: w.gate(F, r, list(bpc))
        if LAZY and D not in TOPSET: master[D] = res[0]
        for x in dd: pool[w.xpart(x)].append(x)
        if bcast[D]:
            for r in regs[D]: w.gate(F, r, list(bcast[D]))
        # hop receptions: parents' assemblers read this piece at its own frame, before any copy of it climbs
        for P in hopparents.get(D, []):
            if P not in asm: asm[P] = w.helper('assembler')
            w.gate(F, asm[P], [regs[D][-1]])
