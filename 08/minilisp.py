# Write an asynchronous parser for a very limited subset of the hw3
# lisp grammar. Specifically, only consider compound expressions and
# atoms. Represent atoms using ‹str› and compound expressions using
# lists (note: it might be hard to find a reasonable mypy type, so
# if you normally use annotations, it's quite okay to skip them in
# this exercise). The argument to the parser is an
# ‹asyncio.StreamReader› instance. Your best bet is reading the data
# using ‹readexactly( 1 )›. The parser should immediately return
# after reading the closing bracket of the initial expression.

# Note: This exercise is designed to help you in adapting your hw3
# parser for use with hw4 (i.e. in making it asynchronous). Writing
# a predictive (LL) parser for the hw3 grammar is easy and worth a
# shot even if you originally wrote something else.

import asyncio

async def minilisp( reader ):
    pass

import os

async def main():
    loop = asyncio.get_running_loop()
    r_fd, w_fd = os.pipe()
    w_file = os.fdopen( w_fd, 'w' )
    r_stream = asyncio.StreamReader()
    await loop.connect_read_pipe( lambda:
            asyncio.StreamReaderProtocol( r_stream ),
            os.fdopen( r_fd ) )

    def send( data ):
        w_file.write( data )
        w_file.flush()

    async def check( *expect ):
        expect = list( expect )
        got = await minilisp( r_stream ) 
        assert got == expect, f"{got} == {expect}"

    send( '(hello)' )
    await check( 'hello' )
    send( '(hello world)' )
    await check( 'hello', 'world' )
    send( '(hello (world))' )
    await check( 'hello', [ 'world' ] )
    send( '((hello) (cruel (or not) world))' )
    await check( [ 'hello' ],
                 [ 'cruel', [ 'or', 'not' ], 'world' ] )

def test_main():
    asyncio.run( main() )

if __name__ == '__main__':
    test_main()
