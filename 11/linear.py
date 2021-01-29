# The goal of this exercise is to learn about numpy arrays. Write a
# function which takes a list of numbers, interprets it as a square
# matrix and computes the inverse, second power, the determinant.
# The function should return those values as a 3-tuple, with
# matrices represented the same way as input: as a flat list of
# numbers. Return None in place of inverse if the matrix is
# singular, i.e. has no inverse.

# The next exercise is ‹volume.py›.

import numpy as np

def linalg( matrix ):
    pass


from math import isclose

def test_main():

    m = [ 1, 0, 0,
          0, 1, 0,
          0, 0, 1 ]

    minv, mpow, mdet =  linalg( m )

    for i in range( len( minv ) ):
        assert isclose( minv[i], m[i] )
        assert isclose( mpow[i], m[i] )

    assert isclose( mdet, 1 )

    minv, mpow, mdet = linalg( [  1, -1,
                                 -1,  1 ] )
    assert minv is None
    mpow_r = [ 2, -2, -2, 2 ]

    for x, y in zip( mpow, mpow_r ):
        assert isclose( x, y )
    assert isclose( mdet, 0 )

if __name__ == "__main__":
    test_main()
