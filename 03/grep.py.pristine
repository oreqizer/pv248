# The goal of this exercise is to write a simple program that works
# like UNIX ‹grep›. We will start by writing a procedure which takes
# 2 arguments, a string representation of a regex and a filename. It
# will print the lines of the file that match the regular expression
# (in the same order as they appear in the file).  Prefix the line
# with its line number like so:

#     43: This line matched a regex,

# Hint: check out the ‹enumerate› built-in.

def grep( regex, filename ):
    pass

# ----%<----

import sys
from io import StringIO

def test_1():
    grep( "empty", "grep1.txt" )

def test_2():
    grep( "p[p|t]", "grep1.txt" )

def redirect_out( test ):

    stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    test()

    sys.stdout = stdout
    return out.getvalue()

def test_main():

    output = redirect_out( test_1 )
    assert output == "4: be nonempty.\n" \
                     "6: Has some empty lines, too.\n"

    output = redirect_out( test_2 )
    assert output == "3: is not very long and appears to\n" \
                     "4: be nonempty.\n" \
                     "6: Has some empty lines, too.\n"


# Change the code below to only run ‹test_main› if an argument
# ‹--test› is given. Otherwise, expect 2 command-line arguments: a
# regular expression and a file name, and pass those to the ‹grep›
# procedure above.

if __name__ == "__main__":
    test_main()

# The next exercise is ‹rfc822.py›.
