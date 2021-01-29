# Given a square matrix, find its ‘null space’ in the form of a list
# of unit-length basis vectors for that space. The null space (or a
# kernel) of a matrix is the space of all vectors which, multiplied
# by the matrix, come out as zero. For instance:
#
#     │ 1 0 0 │   │ x │   │ x │
#     │ 0 1 0 │ × │ y │ = │ y │
#     │ 0 0 0 │   │ z │   │ 0 │
#
# This comes out zero if ⟦x = y = 0⟧, regardless of ⟦z⟧. Hence, the
# null space is spanned by the single vector (0, 0, 1). Indeed:
#
#     │ 1 0 0 │   │ 0 │   │ 0 │
#     │ 0 1 0 │ × │ 0 │ = │ 0 │
#     │ 0 0 0 │   │ 1 │   │ 0 │
#
# If we consider another matrix, we see:
#
#     │ 1 1 0 │   │ x │   │  x +  y │
#     │ 2 2 0 │ × │ y │ = │ 2x + 2y │
#     │ 0 0 0 │   │ z │   │    0    │
#
# The vector is zero whenever ⟦x = -y⟧ (and irrespective of ⟦z⟧).
# Hence, the null space is two-dimensional, spanned by (for
# instance) the vectors (1, -1, 0) and (0, 0, 1).
#
#     │ 1 1 0 │   │  1 │   │ 0 │
#     │ 2 2 0 │ × │ -1 │ = │ 0 │
#     │ 0 0 0 │   │  0 │   │ 0 │
#
#     │ 1 1 0 │   │  0 │   │ 0 │
#     │ 2 2 0 │ × │  0 │ = │ 0 │
#     │ 0 0 0 │   │  1 │   │ 0 │
#
# Notice that we have chosen the basis so that it is orthogonal:
#
#                  │ 0 │
#     │ 1 -1 0 │ × │ 0 │ = 0
#                  │ 1 │
#
# It's easy to make it orthonormal, just divide the first vector by
# a square root of 2. In the exercise, however, orthogonality is not
# required (it just makes it easy to see that the vectors are
# linearly independent).

import numpy as np


def null(m):
    pass


def test_main():
    def norm( x ): return np.sqrt( np.dot( x, x ) )
    def arr( *x ): return np.array( x )
    def isunit( v ): return np.isclose( norm( v ), 1 )
    def isnull( m, v ): return all( np.isclose( m @ v, [ 0, 0, 0 ] ) )

    m = arr( [ 1, 0, 0 ], [ 0, 1, 0 ], [ 0, 0, 0 ] )
    v, = null( m )
    assert isunit( v )
    assert isnull( m, v )

    m = arr( [ 1, 1, 0 ], [ 2, 2, 0 ], [ 0, 0, 0 ] )
    v, w = null( m )
    assert isunit( v )
    assert isunit( w )
    assert isnull( m, v )
    assert isnull( m, w )
    assert np.linalg.matrix_rank( [ v, w ] ) == 2

    m = arr( [ 1, 0, 0 ], [ 0, 1, 0 ], [ 0, 0, 1 ] )
    assert len( null( m ) ) == 0

    m = arr( [ 1, -1, 1 ], [ 1, 0, 1 ], [ 1, 1, 1 ] )
    v, = null( m )
    assert isunit( v )
    assert isnull( m, v )


if __name__ == "__main__":
    test_main()
