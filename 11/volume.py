# Compute the volume of an n-dimensional simplex, given as a list of
# n + 1 points. A 2D simplex is a triangle, given by 3 points, a 3D
# simplex is a 3-sided pyramid given by 4 points and so on.

# Go on to ‹histogram.py›.

def volume( pts ):
    pass

from math import isclose

def test_main():
    assert isclose( volume( [ [ 0, 0 ], [ 0, 3 ], [ 4, 0 ] ] ), 6 )
    assert isclose( volume( [ [ 0, 0 ], [ 4, 0 ], [ 3, 0 ] ] ), 0 )
    assert isclose( volume( [ [ 3, 3, 2 ], [ 0, 7, -1 ], [ 3, 1, 4 ], [ 0, -2, 3 ]  ] ), 5 )

if __name__ == "__main__":
    test_main()
