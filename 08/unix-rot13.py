# We will do something similar to tcp-echo, but this time we will
# use a UNIX socket. UNIX sockets exist on the filesystem and need
# to be given a (file)name. Additionally, instead of simply echoing
# the text back, we will use Caesar cipher (rotate the characters)
# with right shift (the intuitive one) of 13. We will have to
# explicitly remove the socket once we are done with it, as it will
# stay on the filesystem otherwise. Note that this should only
# require very small changes from your previous solution to
# ‹tcp-echo›.

import os
from io import StringIO
import sys
import asyncio


def encrypt(text, s = 13):
    result = ""
    # transverse the plain text
    for i in range(len(text)):
        char = text[i]
        # Encrypt uppercase characters in plain text

        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)
        # Encrypt lowercase characters in plain text
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
    return result


async def handle_client(reader, writer):
    r = await reader.read(100)
    txt = r.decode()
    print(f"server received {txt}")
    enc = encrypt(txt)
    print(f"server sending {enc}")
    writer.write(enc.encode())
    writer.close()


async def client(msg, path):
    reader, writer = await asyncio.open_unix_connection(path=path)
    print(f"client sending {msg}")
    if msg == "world":
        await asyncio.sleep(1)
    writer.write(msg.encode())
    data = await reader.read()
    txt = data.decode()
    print(f"client received {txt}")
    writer.close()
    return txt


async def main(path):
    server = await asyncio.start_unix_server(handle_client, path=path)
    await server.start_serving()
    res = await asyncio.gather(
        client("hello", path),
        client("world", path),
    )
    server.close()
    os.remove(path)
    return res


def test_main():

    stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    path = "./tmp.socket"
    data = asyncio.run(main(path))
    print(data)
    assert data == ['uryyb', 'jbeyq']

    sys.stdout = stdout
    output = out.getvalue()
    print(output)
    output = output.split('\n')

    assert 'client sending hello' in output[0: 3]
    assert 'client sending world' in output[0: 3]
    assert 'server received hello' in output[1: 3]
    assert 'server sending uryyb' in output
    assert 'server received world' in output
    assert 'server sending jbeyq' in output

    assert not os.path.exists(path)


if __name__ == "__main__":
    test_main()
