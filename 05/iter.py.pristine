# Implement these 4 utilities on iterables:
#
#  • prefix and suffix list
#  • prefix and suffix sum
#
# Examples:
#
#     dump( prefixes( [ 1, 2, 3 ] ) ) # [] [1] [1, 2] [1, 2, 3]
#     dump( suffixes( [ 1, 2, 3 ] ) ) # [] [3] [2, 3] [1, 2, 3]

def prefixes_iter( list_in ):
    pass

def prefixes_gen( list_in ):
    pass

def suffixes( list_in ):
    pass

def prefix_sum( list_in ):
    pass

def suffix_sum( list_in ):
    pass

# Implement the prefix list both using an iterator (an object with
# __iter__) and using a generator. Pick one approach for each of the
# remaining 3, but make sure there's at least one iterator and one
# generator among them.

# Go on to ‹flat.py›.

import types

def test_main():

    res = [ [], [1], [1,2], [1,2,3], [1,2,3,4] ]

    for i in prefixes_iter( [1,2,3,4] ):
        assert i in res
        res.remove( i )

    assert not res # emptied

    res = [ [], [1], [1,2], [1,2,3], [1,2,3,4] ]
    assert isinstance( prefixes_gen( [] ), types.GeneratorType )

    for i in prefixes_gen( [1,2,3,4] ):
        assert i in res
        res.remove( i )

    assert not res


    res = [ [], [7], [8,7], [6,8,7], [5,6,8,7] ]

    for i in suffixes( [5,6,8,7] ):
        assert i in res
        res.remove( i )

    assert not res # emptied


    count = 0
    for item in prefix_sum( [1,2,3,4,5] ):
        count += 1 # is iterable
    assert count == len( [1,2,3,4,5] )

    assert list( prefix_sum( [1,2,3,4,5] ) ) == [1,3,6,10,15]

    count = 0
    for item in suffix_sum( [1,2,3,4,5] ):
        count += 1 # is iterable
    assert count == len( [1,2,3,4,5] )

    assert list( suffix_sum( [1,2,3,4,5] ) ) == [5,9,12,14,15]


if __name__ == "__main__":
    test_main()

