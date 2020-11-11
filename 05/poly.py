# Implement polynomials which can be added and printed. Do not print
# terms with coefficient 0, unless it is in place of ones and the
# only term.

# Examples:
#
#     x = Poly( 2, 7, 0, 5 )
#     y = Poly( 2, 4 )
#
#     print( x )     # prints: 2x^3 + 7x^2 + 5
#     print( y )     # prints 2x + 4
#     print( x + y ) # prints 2x^3 + 7x^2 + 2x + 9

class Poly:
    pass

# We will do one more exercise with operators, ‹mod.py›, before
# moving on to exceptions.

def test_main():

    x = Poly( 2, 7, 3, 5 )
    y = Poly( 2, 4 )
    z = Poly( 0, 4, 1, -3, 0 )
    a = Poly( 0 )

    assert str( x ) == "2x^3 + 7x^2 + 3x + 5"
    assert str( y ) == "2x + 4"
    assert str( z ) == "4x^3 + x^2 - 3x"
    assert str( a ) == "0"

    assert str( x + a ) == "2x^3 + 7x^2 + 3x + 5"
    assert str( a + a ) == "0"

    assert str( x + y ) == "2x^3 + 7x^2 + 5x + 9"
    assert str( y + x ) == str( x + y )

    assert str( x + z ) == "6x^3 + 8x^2 + 5"
    assert str( z + x ) == str( x + z )

    assert str( y + z ) == "4x^3 + x^2 - x + 4"
    assert str( z + y ) == str( y + z )

    z_inv = Poly( 0, -4, -1, 3, 0 )
    assert str( z_inv + z ) == "0"

if __name__ == "__main__":
    test_main()
