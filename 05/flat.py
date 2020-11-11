# Write a generator that completely flattens iterable structures
# (i.e. given arbitrarily nested iterables, it will generate a
# stream of scalars). Note: while strings are iterable, there are
# no ‘scalar’ characters, so you do not need to consider strings.

def flatten( g ):
    pass

# Let's move on to ‹poly.py›.

def test_main():

    f = flatten( [ 7, [ 2, 2 ], map( lambda x : x - 8, [ 0, 9 ] ) ] )
    assert list( f ) == [ 7, 2, 2, -8, 1 ]

    f = flatten( [ map( lambda x: x * x, range( 3 ) ),
                 [ range( i + 1 ) for i in range( 3 ) ] ] )

    assert list( f )  ==  [ 0, 1, 4, 0, 0, 1, 0, 1, 2 ]

    f = flatten( [ 0, ( 1, 7, 3 ), 9, [ [ [ 3 ] ], [ -2, [ 0 ] ] ], reversed( [ 22, 9 ] ) ] )
    res = [ 0, 1, 7, 3, 9, 3, -2, 0, 9, 22 ]

    f_len = 0

    for item, item_r in zip( f, res ):
        f_len += 1
        assert item == item_r

    assert f_len == len( res )

if __name__ == "__main__":
    test_main()

