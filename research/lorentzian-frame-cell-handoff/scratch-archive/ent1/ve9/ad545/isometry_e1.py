"""[E1 VARIANT of PR #443's bank_routes.validate_isometries (vendored unchanged in PR #510 as
e8-r740-replica32/code/bank_routes.py); one listed change.]

The vendored function accepts only coordinate permutations as the Gaussian reduction of a residual isometry ("This
selected family needs coordinate permutations only"), because every entrance frame of R715/R740 is spanned by
coordinate roots 2e_i.  E1's entrance frame 186 is spanned by roots 33 = (1,1,0,0,-1,-1,0,0) and 77 = (0,1,0,-1,1,0,1,0),
which are not coordinate roots, so its isometry has genuine route factors.  The change: the listed reduction may also contain the elementary
factors of the nine-stage port routes (GEOMETRY.json `elementary_inverse_replay`): ['scale', i, None, s] (row i *= s,
s != 0) and ['add', i, j, s] (row i += s * row j, i != j), with exact rational s whose denominators are powers of two.
They are replayed exactly (Fractions) and must reduce the orthogonal matrix (rows / 2) to the identity, as before.  The
number of factors is bounded by MAX_FACTORS = 77, the nine-stage geometry's max_route_factors for the port routes, so
the finite selector bill of assemble9.py (which charges max_route_factors per residual route) still covers it.
Every other assertion is the vendored one, unchanged.  Prepared with Anthropic Claude assistance; Apache-2.0."""
from fractions import Fraction

MAX_FACTORS = 77


def _dyadic(s):
    q = Fraction(s)
    d = q.denominator
    assert q != 0 and d & (d - 1) == 0
    return q


def validate_isometries(rows, frames, roots, dimensions):
    seen = set()
    dot = lambda a, b: sum(x*y for x, y in zip(a, b))
    for record in rows:
        f = record['frame']
        assert f not in seen
        seen.add(f)
        e = record['entrance_rank']
        assert e == dimensions[f] and record['denominator'] == 2
        basis = record['entrance_basis'] + record['residual_basis']
        matrix = record['orthogonal_rows_numerator']
        assert len(basis) == len(matrix) == 8
        assert matrix == [roots[i] for i in basis]
        assert all(len(r) == 8 and all(type(x) is int for x in r) for r in matrix)
        assert all(dot(a,b) == 4*(i==j) for i,a in enumerate(matrix) for j,b in enumerate(matrix))
        # The first e rows span precisely the frame, not only its dimension.
        for i in frames[f]:
            assert sum(dot(roots[i], q)**2 for q in matrix[:e]) == 4*dot(roots[i], roots[i])
        assert len(record['entrance_basis']) == e
        # E1 change: exact replay of swaps and dyadic scale/add factors (vendored: swaps only, at most 7).
        reduced = [[Fraction(x, 2) for x in row] for row in matrix]
        operations = record['gaussian_reduction']
        assert len(operations) <= MAX_FACTORS
        for kind, i, j, scalar in operations:
            assert 0 <= i < 8
            if kind == 'swap':
                assert scalar is None and 0 <= j < 8
                reduced[i], reduced[j] = reduced[j], reduced[i]
            elif kind == 'scale':
                assert j is None
                s = _dyadic(scalar)
                reduced[i] = [s * x for x in reduced[i]]
            else:
                assert kind == 'add' and 0 <= j < 8 and i != j
                s = _dyadic(scalar)
                reduced[i] = [x + s * y for x, y in zip(reduced[i], reduced[j])]
        assert reduced == [[int(i == j) for j in range(8)] for i in range(8)]
    return seen
