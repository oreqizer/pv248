# Write a function, ‹reduce›, which takes, as input, a dictionary
# ‹funs› with types as keys and functions as values; each of the
# functions will accept 2 arguments of the type given by its key in
# ‹funs›, and return one value, not necessarily of the same type.
# The second input is ‹val›, a value to be reduced.
#
# Depending on the type of ‹val›:
#
#  • if it is a ‹dict›, reduce each value (not the keys though) and
#    check that the results are all of the same type; if not, use
#    the function under the 'default' key to reduce the values; if
#    they are of the same type, look up the type of the reduction
#    result in ‹funs› and use the corresponding function to reduce
#    all the values into a single element and return it; assume that
#    the function is associative,
#  • if it is iterable, do the same process as on the values of the
#    ‹dict›: reduce each value, check they are of the same type and
#    combine them using the appropriate functions from ‹funs›,
#  • otherwise, do nothing and return ‹val› unchanged.
#
# Always pass the same ‹funs› dictionary down to sub-reductions.
# Hint: you can use ‹hasattr(val, '__iter__')› to check whether a
# value is iterable.
#
# Warning: do not feed ‹str› values into ‹reduce› – this will give
# you infinite recursion, because iterating ‹str› yields ‹str›
# yields ‹str› and so on.

def reduce( funs, val ):
    pass

def test_main():

    class A():
        def __init__( self, foo ):
            self.foo = foo
    def a_foo( x, y ):
        return A( x.foo + y.foo )

    def default( x, y ):
        if type( x ) == A:
            x = x.foo
        if type( y ) == A:
            y = y.foo
        return str( x ) + str( y )


    d = { int: lambda x,y: x * y,
          str: lambda x,y: x + y,
          A: a_foo,
          'default': default  }
    assert reduce( d, [ { 'a': { 'b': 2 } }, 3, 4 ] ) == 24

    res = reduce( d, [ A( 7 ), A( 3 ) ] )
    assert type( res ) == A
    assert res.foo == 10

    res = reduce( d, { 'a': 50, 'b': 6, 'c': [ -1, 2, 9 ],
                       'd': { 'a': A('abc'), 'b': A('de'), 'c': 3 } } )
    assert res == "506-18abcde3"

    funs = { float: lambda x, y: int( x ) + int( y ),
             int: lambda x, y: x + y }
    assert reduce( funs, [ 1, 2, [ 3, { 2.0, -1.0 } ],
                           { 'x': 1, 'y': 2 },
                           { 3, 4 } ] ) == 17

if __name__ == "__main__":
    test_main()
