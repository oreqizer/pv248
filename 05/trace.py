# Write a decorator that prints a message every time a function is called or it
# returns. The output should be indented when calls are nested, and should
# include arguments and the return value.

# Aim for something like this:

# foo [13]
#   bar [13] -> 20
#   bar [26] -> 33
# returned 53

import sys
from io import StringIO
import traceback

indt = 1

def traced(f):
    name = f.__name__
    
    def decor(*args):
        global indt
        if indt > 1:
            print()
        print("{indt}{name} {args}".format(indt=indt*' ', name=name, args=list(args)), end='')
        indt += 2
        res = f(*args)
        indt -= 2
        if indt == 1:
            print('\n returned {res}'.format(res=res))
        else:
            print(' -> {res}'.format(res=res), end='')
        return res

    decor.__doc__ = f.__doc__
    decor.__name__ = f.__name__

    return decor

@traced
def bar(x):
    return x + 7


@traced
def foo(x):
    return bar(x) + bar(2 * x)


def redirect_out(test, *args):

    stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    test(*args)

    sys.stdout = stdout
    return out.getvalue()


def test_main():

    output = redirect_out(foo, 13)

    print(output)
    assert output == " foo [13]\n" \
                     "   bar [13] -> 20\n" \
                     "   bar [26] -> 33\n" \
                     " returned 53\n"


if __name__ == "__main__":
    test_main()

# Now that we have seen both decorators and exceptions in some detail, we can
# have a look at `noexcept.py`.
