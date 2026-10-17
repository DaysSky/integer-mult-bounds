import numpy as np
def rank2(M):
    M = (np.array(M, dtype=np.uint8) & 1).copy()
    r = 0; rows, cols = M.shape
    for c in range(cols):
        piv = np.nonzero(M[r:, c])[0]
        if len(piv) == 0: continue
        p = r + piv[0]
        M[[r, p]] = M[[p, r]]
        nz = np.nonzero(M[:, c])[0]
        nz = nz[nz != r]
        M[nz] ^= M[r]
        r += 1
        if r == rows: break
    return r
