# Use ‹aiohttp› to fetch a given URL and stream the HTML into
# ‹tidy›. Specifically, use ‹tidy 2>&1› as the command that you
# start with ‹asyncio.create_subprocess_shell›. Capture the ‹stdout›
# and return the second line that ‹tidy› prints (should say there
# were no errors).

import aiohttp
import asyncio
from asyncio.subprocess import PIPE

async def tidy( url ):
    pass

async def main():
    out = await tidy( 'http://example.com' )
    assert out == b'No warnings or errors were found.\n'
    out = await tidy( 'http://www.fi.muni.cz' )
    assert out == b'line 125 column 81 - Warning: replacing unexpected button with </button>\n';

def test_main():
    asyncio.run( main() )

if __name__ == '__main__':
    test_main()
