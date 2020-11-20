# In this exercise, we will look at talking to external programs
# using ‹asyncio›. There are two coroutines in the ‹asyncio› module
# for spawning new processes: for simplicity, we will use
# ‹create_subprocess_shell›.

# However, before you start working, try the following shell
# command:
#
#    $ while read x; do echo x is $x; done
#
# and type a few lines. Use ctrl+d to terminate the loop.

# This is one of the programs we will interact with. Use stdout and
# stdin streaming to talk to this simple shell program from python:
# send a line and read back the reply from the program. Copy it to
# the standard output of the python program. Apart from printing,
# return a list of all outputs from the shell program. There are two
# arguments, the command to run and a list of inputs to serve this
# program one-by-one. Keep the type: if the output is an integer,
# add an integer to the result; otherwise, add a string.

# NOTE: The data that goes into the process and that comes out is
# ‹bytes›, not strings. Make sure to encode and decode the bytes as
# needed.

import asyncio
from asyncio.subprocess import PIPE

async def pipe_cmd( command, inputs ):
    pass


async def run():

    p = "while read x; do echo x is $x; done"
    inputs = [ 'a', 7, "input", 3.6, "`echo 2`" ]
    outputs = [ 'x is a', 'x is 7', 'x is input', 'x is 3.6',
                'x is `echo 2`' ]

    res = await pipe_cmd( p, inputs )
    assert res == outputs

    p = "bc"
    inputs = [ "231-19", "sqrt(2+7)*3", "8^7-5432^2" ]
    outputs = [ 212, 9, -27409472 ]

    res = await pipe_cmd( p, inputs )
    assert res == outputs

    p = "while read var; do echo \"${#var}\"; done"
    inputs = [ 229, 10239, 1343, 1, "06" ]
    outputs = [ 3, 5, 4, 1, 2 ]

    res = await pipe_cmd( p, inputs )
    assert res == outputs

def test_main():
    asyncio.run( run() )

if __name__ == "__main__":
    test_main()

# Continue to ‹aio-multi.py›.
