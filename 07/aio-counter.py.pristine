# Spawn a given number of instances of the following shell program:
#
#    while true; do echo .; sleep {n}; done
#
# Where the values for `{n}` are given in the argument ‹sleeps›.
# Run all these programs in parallel and monitor their output
# (asserting that each line they print is exactly a single dot).

# Once a second, use ‹queue.put› to send a list of numbers, each of
# which gives the number of dots received from the i'th subprocess.
# For instance, the first list should be approximately ‹[ 1, 2, 10
# ]› if ‹sleeps› were given as ‹[ 1, 0.5, 0.1 ]›. The last
# parameter, ‹iterations› tells you how many one-second intervals to
# run for (and hence, how many items to put into the queue).  After
# the given number of iterations, kill all the subprocesses.

import asyncio

async def counters( queue, sleeps, iterations ):
    pass

def fuzzy( a, b ):
    for i, j in zip( a, b ):
        if abs( i - j ) > 1:
            return False
    return True

async def check( q ):
    assert fuzzy( await q.get(), [ 1, 2, 10 ] )
    assert fuzzy( await q.get(), [ 2, 4, 20 ] )
    assert fuzzy( await q.get(), [ 3, 6, 30 ] )

async def main():
    q = asyncio.Queue()
    await asyncio.gather( check( q ), counters( q, [ 1, 0.5, 0.1 ], 3 ) )

def test_main():
    asyncio.run( main() )

if __name__ == '__main__':
    test_main()

# Go on to ‹http-client.py›.
