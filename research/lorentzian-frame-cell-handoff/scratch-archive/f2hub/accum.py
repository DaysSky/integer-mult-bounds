    for s, (F, D, tgt) in acc.items():                              # sources accumulate their X part
        w.gate(F, s, [regs[D][0]])
