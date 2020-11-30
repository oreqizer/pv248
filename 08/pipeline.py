# In this and the next exercise, we will write coroutines which can
# be connected into a sort of pipeline, like what we did with
# generator-based streams in week 6. Again, there will be sources,
# sinks and processors and the coroutines will pass data to each
# other as it becomes available.

# Native coroutines have an arguably a more intuitive and more
# powerful construct to send data to each other than what is
# available with generators: ‹asyncio.Queue›. The queues are of two
# basic types: bounded and unbounded. The former limits the amount
# of memory taken up by ‘backlogs’ and enforce some level of
# synchronicity into the system.

# In the special case where the size bound is set to 1, the queue
# behaves a lot like ‹send›/‹yield›.  Trying to get an item from a
# queue that is empty naturally blocks the coroutine (making it
# possible for the writer coroutine to run) – this is quite obvious.
# However, if the queue is bounded, the opposite is also true:
# writing into a full queue blocks the «writer» until space becomes
# available. This lets the «reader» make progress at the expense of
# the writer.

# We will use such queues to build up our stream pipelines: sinks
# and sources will accept a single queue as a parameter each (sink
# as its input, source as its output), while a processor will accept
# two (one input and one output). Like before, we will use ‹None› to
# indicate an empty stream, however, we will not repeat it forever
# (i.e. only send it once).

# In this exercise, we will write two simple processors for our
# stream pipelines:
#
#  • a ‹chunker› which accepts ‹str› chunks of arbitrary sizes and
#    produces chunks of a fixed size,
#  • ‹getline› which accepts chunks of arbitrary size and produces
#    chunks that correspond to individual lines.

import asyncio

def chunker( size ):

    async def process( q_in, q_out ):
        pass

    return process

async def main():
    sink_done = False

    async def source( q_out ):
        await q_out.put( 'hello ' )
        await q_out.put( 'world' )
        await q_out.put( None )

    async def check( pipe, expect ):
        x = await pipe.get()
        assert x == expect, f"{x} == {expect}"

    async def sink_4( q_in ):
        nonlocal sink_done
        await check( q_in, 'hell' )
        await check( q_in, 'o wo' )
        await check( q_in, 'rld' )
        await check( q_in, None )
        sink_done = True

    async def sink_2( q_in ):
        nonlocal sink_done
        await check( q_in, 'he' )
        await check( q_in, 'll' )
        await check( q_in, 'o ' )
        await check( q_in, 'wo' )
        await check( q_in, 'rl' )
        await check( q_in, 'd' )
        await check( q_in, None )
        sink_done = True

    def pipeline( *elements ):
        q_out = asyncio.Queue( 1 )
        line = [ elements[ 0 ]( q_out ) ]
        for e in elements[ 1 : -1 ]:
            q_in = q_out
            q_out = asyncio.Queue( 1 )
            line.append( e( q_in, q_out ) )
        line.append( elements[ -1 ]( q_out ) )
        return line

    async def run( *pipe ):
        nonlocal sink_done
        sink_done = False
        await asyncio.gather( *pipeline( *pipe ) )
        assert sink_done

    await run( source, chunker( 4 ), sink_4 )
    await run( source, chunker( 2 ), chunker( 4 ), sink_4 )
    await run( source, chunker( 7 ), chunker( 4 ), sink_4 )
    await run( source, chunker( 7 ), chunker( 2 ), sink_2 )
    await run( source, chunker( 4 ), chunker( 2 ), sink_2 )
    await run( source, chunker( 3 ), chunker( 2 ), sink_2 )

def test_main():
    asyncio.run( main() )

if __name__ == "__main__":
    test_main()
