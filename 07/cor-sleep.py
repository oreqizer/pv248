# Demonstrate the use of native coroutines and basic ‹asyncio›
# constructs.  Define 2 coroutines, say ‹cor1()› and ‹cor2()›, along
# with an asynchronous ‹main()›. Make the coroutines suspend for a
# different amount of time (say 0.7 seconds and 1 second) and then
# print the name of the function, in an infinite loop.

# Use asyncio.gather to run them in parallel (from your ‹main()›,
# which you should invoke by using ‹asyncio.run()› at the toplevel)
# and observe the result. What happens if you instead ‹await cor1()›
# and then ‹await cor2()›?  Try making the loops in ‹corN› finite
# (tests are meant for 5 iterations, but feel free to play around
# with them).

import asyncio

import sys
from io import StringIO
import time

def test_main():

    old = sys.stdout
    out = StringIO()
    sys.stdout = out

    start = time.time()
    asyncio.run( main() )
    end = time.time()

    sys.stdout = old
    result = out.getvalue().strip().split( '\n' )

    assert result[0] == "cor1"
    assert result[1] == "cor2"
    assert result[2] == "cor1"
    assert result[-1] == "cor2"
    assert result[-2] == "cor2"
    assert result[-3] == "cor1"

    assert end - start >= 5
    assert end - start < 5.2

if __name__ == "__main__":
    test_main()

# When done, go on to ‹cor-semaphore.py›.
