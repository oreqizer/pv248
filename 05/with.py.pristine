# Write a simple context manager to be used in a `with` block. The goal is to
# enrich stack traces with additional context, like this:

def context( *args ):
    pass

def foo( x, y ):
    with context( "asserting equality", x, '=', y ):
        assert x == y

# foo( (), () )
# foo( 7, [] )
# should print something like this (the first call should print nothing):

# asserting equality 7 = []
# Traceback (most recent call last):
#   File "with.py", line 20, in <module>
#     foo( 7, [] )
#   File "with.py", line 17, in foo
#     assert x == y
# AssertionError

import sys
import traceback
from io import StringIO

def redirect_err( f ):

    stderr = sys.stderr
    out = StringIO()
    sys.stderr = out

    try:
        f()
    except:
        traceback.print_exc()

    sys.stderr = stderr
    return out.getvalue()


def test_main():

    def test():
        foo( (), () )
        foo( 7, [] )

    output = redirect_err( test )

    res = output.split( '\n' )
    assert res[0] == "asserting equality 7 = []"
    assert res[1] == "Traceback (most recent call last):"
    assert res[2].strip().startswith( "File" )
    assert res[2].endswith( "in redirect_err" )
    assert res[3] == "    f()"
    assert res[-2] == "AssertionError"

if __name__ == "__main__":
    test_main()

# After you are done here, go on to `trace.py`.
