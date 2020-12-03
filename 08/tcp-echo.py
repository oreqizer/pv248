# Start a server, on localhost, on the given port (using asyncio.start_server)
# and have two clients connect to it.
# The server takes care of the underlying sockets, so we will not be creating
# them manually. Data is, again, transferred as `bytes` object.

# The server should return whatever data was sent to it. Clients should send
# 'hello' and 'world', respectively, then wait for the answer from the server
# and return this answer.
# Add print statements to make sure your server and clients behave as expected;
# print data received by the server, sent to the clients and sent and received
# by the clients on the client side.
# Make sure to close the writing side of sockets once data is exhausted.

from io import StringIO
import random
import sys
import asyncio

# Server-side, handler for connecting clients. Read the message from
# the client and echo it back to the client.


async def handle_client(reader, writer):
    r = await reader.read(100)
    txt = r.decode()
    print(f"server received & sending {txt}")
    writer.write(r)
    writer.close()


# Client, connect to the server, send a message, wait for the answer
# and return this answer. Assert that the answer matches the message
# sent. Sleep for 1 second before sending 'world', to ensure message order.


async def client(port, msg):
    reader, writer = await asyncio.open_connection(port=port)
    print(f"client sending {msg}")
    if msg == "world":
        await asyncio.sleep(1)
    writer.write(msg.encode())
    data = await reader.read()
    txt = data.decode()
    print(f"client received {txt}")
    writer.close()
    return txt

# Start the server and the two clients, gather the data back from the
# two clients into a list, return this list; starting with the 'hello'
# client. Use the provided port.


async def main(port):
    server = await asyncio.start_server(handle_client, port=port)
    await server.start_serving()
    res = await asyncio.gather(
        client(port, "hello"),
        client(port, "world"),
    )
    server.close()
    return res


def test_main():

    stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    data = asyncio.run(main(random.randint(9000, 13000)))
    print(data)
    assert data == ['hello', 'world']

    sys.stdout = stdout
    output = out.getvalue()
    print(output)
    output = output.split('\n')

    assert 'client sending hello' in output[0: 3]
    assert 'client sending world' in output[0: 3]
    assert 'server received & sending hello' in output[1: 3]
    assert 'server received & sending world' in output[2:]


if __name__ == "__main__":
    test_main()
