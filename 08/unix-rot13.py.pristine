# We will do something similar to tcp-echo, but this time we will
# use a UNIX socket. UNIX sockets exist on the filesystem and need
# to be given a (file)name. Additionally, instead of simply echoing
# the text back, we will use Caesar cipher (rotate the characters)
# with right shift (the intuitive one) of 13. We will have to
# explicitly remove the socket once we are done with it, as it will
# stay on the filesystem otherwise. Note that this should only
# require very small changes from your previous solution to
# ‹tcp-echo›.

import asyncio

async def handle_client( reader, writer ):
    # print( "server received", ... )
    # print( "server sending", ... )
    pass

async def client( msg, path ):
    # print( "client sending", ... )
    # print( "client received", ... )
    pass

async def main( path ):
    pass

import sys
from io import StringIO
import os

def test_main():

    stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    path = "./tmp.socket"
    data = asyncio.run( main( path ) )
    print( data )
    assert data == ['uryyb', 'jbeyq']

    sys.stdout = stdout
    output = out.getvalue()
    print( output )
    output = output.split('\n')

    assert 'client sending hello' in output[ 0 : 3 ]
    assert 'client sending world' in output[ 0 : 3 ]
    assert 'server received hello' in output[ 1 : 3 ]
    assert 'server sending uryyb' in output
    assert 'server received world' in output
    assert 'server sending jbeyq' in output

    assert not os.path.exists( path )

if __name__ == "__main__":
    test_main()
