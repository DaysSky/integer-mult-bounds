"""F2^8 quadratic spaces: O+(8,2) and O-(8,2) nonsingular points, and the orthogonality patterns."""
import itertools, numpy as np
def forms(kind):
    # symplectic basis pairs (e1,f1)...(e4,f4); Q = sum x_i y_i (+ x4^2 + x4 y4 + y4^2 for minus)
    def Q(v):
        x = v[0::2]; y = v[1::2]
        q = sum(int(a)*int(b) for a, b in zip(x, y)) % 2
        if kind == '-':
            q = (q + x[3] + y[3]) % 2   # x4^2+x4y4+y4^2 = x4 + x4y4 + y4 over F2 -> replace pair 4 by anisotropic
            q = (sum(int(a)*int(b) for a, b in zip(x[:3], y[:3])) + x[3] + x[3]*y[3] + y[3]) % 2
        return q
    def B(u, v):
        return sum(int(u[2*i])*int(v[2*i+1]) + int(u[2*i+1])*int(v[2*i]) for i in range(4)) % 2
    return Q, B
def points(kind, which=1):
    Q, B = forms(kind)
    P = [np.array(v) for v in itertools.product((0,1), repeat=8) if any(v) and Q(v) == which]
    return P, Q, B
if __name__ == '__main__':
    for k in '+-':
        P, Q, B = points(k)
        M = np.array([[B(a, b) for b in P] for a in P])
        print(k, len(P), 'nonorth degree', set(M.sum(1).tolist()))
