# Write a decorator that prints a message every time a function is called or it
# returns. The output should be indented when calls are nested, and should
# include arguments and the return value.

# Aim for something like this:

# foo [13]
#   bar [13] -> 20
#   bar [26] -> 33
# returned 53

def traced( f ):
    pass

@traced
def bar( x ):
    return x + 7

@traced
def foo( x ):
    return bar( x ) + bar( 2 * x )

import sys
from io import StringIO

def redirect_out( test, *args ):

    stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    test( *args )

    sys.stdout = stdout
    return out.getvalue()


def test_main():

    output = redirect_out( foo, 13 )

    assert output == " foo [13]\n" \
                     "   bar [13] -> 20\n" \
                     "   bar [26] -> 33\n" \
                     " returned 53\n"

if __name__ == "__main__":
    test_main()

# Now that we have seen both decorators and exceptions in some detail, we can
# have a look at `noexcept.py`.
