# This is the first in a series of exercises focused on working with
# «streams». A stream is like a sequence, but it is not held in
# memory all at once: instead, pieces of the stream are extracted
# from the input (e.g. a file), then processed and discarded, before
# another piece is extracted from the input. Some of the concepts
# that we will explore are available in the ‹asyncio› library which
# we will look at next week. However, for now, we will do everything
# by hand, to get a better understanding of the principles.

# A «stream processor» will be a (semi)coroutine (i.e. a generator)
# which takes another (semi)coroutine as an argument. It will
# extract data from the ‘upstream’ (the coroutine that it got as an
# argument) using ‹next› and it'll send it further ‘downstream’
# using ‹yield›.

# We will use the convention that an empty stream yields ‹None›
# forever (i.e. we will not use ‹StopIteration›). A «source» is like
# a stream processor, but does not take another stream processor as
# an argument: instead, it creates a new stream. A «sink» is another
# variation: it takes a stream, but does not yield anything. It
# «consumes» the stream. Obviously, stream processors can be
# chained: the chain starts with a source, followed by some
# processors and ends with a sink. 

# Let us first define a simple source, which yields chunks of text.
# To use it, do something like: ‹stream, cnt = make_test_source()›.
# The ‹cnt› variable will keep track of how many chunks were pulled
# out of the stream – this is useful for testing.

class Box:
    def __init__( self, v ):
        self.value = v

def make_test_source():
    counter = Box( 0 )
    def test_source():
        yield "hello "
        counter.value += 1
        yield "world\ni am\n"
        counter.value += 1
        yield " a"
        counter.value += 1
        yield " strea"
        counter.value += 1
        yield "m\nsour"
        counter.value += 1
        yield "ce\n"
        counter.value += 1
        while True:
            yield None
    return ( test_source(), counter )

# What follows is a very simple sink, which prints the content of
# the stream to ‹stdout›:

def dump_stream( stream ):
    while True:
        x = next( stream )
        if x is None: break
        print( end = x )

# Your first goal is to define a simple stream processor, which
# takes a stream of chunks (like the test source above) and produces
# a stream of «lines». Each line ends with a newline character. To
# keep in line with the stated goal of minimizing memory use, the
# processor should only pull out as many chunks as it needs to, and
# not more.

def stream_getline( stream ):
    pass

def test_main():
    stream, counter = make_test_source()
    assert counter.value == 0
    lines = stream_getline( stream )
    assert counter.value == 0
    assert next( lines ) == "hello world\n"
    assert counter.value == 1
    assert next( lines ) == "i am\n"
    assert counter.value == 1
    assert next( lines ) == " a stream\n"
    assert counter.value == 4
    assert next( lines ) == "source\n"
    assert counter.value == 5
    assert next( lines ) is None
    assert counter.value == 6

if __name__ == '__main__':
    test_main()
