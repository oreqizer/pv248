# This exercise is quite hard, but also rather interesting, which is
# why it is marked as a bonus.

# Write a ‘merge server’, which will take 2 string arguments, both
# paths to unix sockets. The first socket is the ‘input’ socket:
# listen on this socket for client connections, until there are
# exactly 2 clients. The clients will send lines, sorted
# lexicographically.

# Connect to the ‘output’ socket (second argument) as a client. Read
# lines as needed from each of the clients and write them out to the
# output socket, again in sorted order. Do not buffer more than 1
# line of input from each of the clients.

# Use ‹readline› on the input sockets' streams to fetch data, and
# relational operators (<, >, ==) to compare the ‹bytes› objects.

import asyncio

# The ‹merge_server› coroutine will simply start the unix server and
# return the server object, just like ‹asyncio.start_unix_server›
# does.


async def read_buffer(reader):
    return await reader.readline()


def handle_in(w, path_in, path_out):
    readers = []

    async def handler(reader, writer):
        nonlocal readers
        readers.append(reader)
        if len(readers) == 2:
            r1, r2 = readers[0], readers[1]
            p1, p2 = b'', b''
            while True:
                await asyncio.sleep(0.2)

                if r1.at_eof() and r2.at_eof():
                    l = [p for p in [p1, p2] if len(p) > 0]
                    if len(l) > 0:
                        w.writelines(l)
                        await w.drain()
                        print(f"{path_in} | {l} >> {path_out} @ EOF")
                    w.close()
                    return

                l1, l2 = b'', b''
                if len(p1) == 0:
                    l1 = await read_buffer(r1) 
                if len(p2) == 0:
                    l2 = await read_buffer(r2)   

                # keep
                if len(l1) > 0 and len(l2) > 0:
                    l = [l1, l2]
                    l.sort()
                    w.writelines(l)
                    await w.drain()
                    print(f"{path_in} | {l} >> {path_out} @ l1, l2")
                    continue


                if len(l1) > 0:
                    # TODO just solve this
                    # if l1 == b"a\n":
                    #     w.write(l1)
                    #     await w.drain()
                    #     print(f"{path_in} | {l1} >> {path_out} @ p1 | {r1.at_eof()} | {r2.at_eof()}")
                    #     continue
                    l = await read_buffer(r1) 
                    lines = [l1, l]
                    lines.sort()
                    w.writelines(lines)
                    print(f"{path_in} | {lines} >> {path_out} @ p1 | {r1.at_eof()} | {r2.at_eof()} AFTERMATH {l}")
                    await w.drain()
                    continue

                p1, p2 = l1, l2


    return handler


async def merge_server(path_in, path_out):
    _, w = await asyncio.open_unix_connection(path=path_out)
    server = await asyncio.start_unix_server(handle_in(w, path_in, path_out), path=path_in)
    await server.start_serving()
    return server


def test_main():
    lines_read = 0
    sem_start, sem_end = None, None

    async def check_line(reader, expect):
        nonlocal lines_read
        expect += b'\n'
        got = await reader.readline()
        assert got == expect, f"{got} == {expect}"
        lines_read += 1

    async def check_complex(reader, writer):
        await sem_start.get()

        _, s111 = await asyncio.open_unix_connection("sock_11")
        _, s112 = await asyncio.open_unix_connection("sock_11")
        _, s121 = await asyncio.open_unix_connection("sock_12")
        _, s122 = await asyncio.open_unix_connection("sock_12")
        _, s21 = await asyncio.open_unix_connection("sock_2")
        _, s22 = await asyncio.open_unix_connection("sock_2")

        s111.write(b'b\n')
        s112.write(b'c\n')

        s121.write(b'd\n')
        s122.write(b'e\n')

        s21.write(b'a\n')
        s22.close()

        await check_line(reader, b'a')

        s121.write(b'f\n')
        s111.close()
        s112.close()
        s121.close()
        s122.close()
        s21.close()

        await check_line(reader, b'b')
        await check_line(reader, b'c')
        await check_line(reader, b'd')
        await check_line(reader, b'e')
        await check_line(reader, b'f')

        await sem_end.put(0)

    async def main_complex():
        nonlocal sem_start, sem_end
        sem_start, sem_end = asyncio.Queue(1), asyncio.Queue(1)
        chk = await asyncio.start_unix_server(check_complex, "sock_o")
        m = await merge_server("socket",  "sock_o")
        m1 = await merge_server("sock_1",  "socket")
        m11 = await merge_server("sock_11", "sock_1")
        m12 = await merge_server("sock_12", "sock_1")
        m2 = await merge_server("sock_2",  "socket")
        await sem_start.put(0)
        await sem_end.get()
        assert lines_read == 6, f"{lines_read} == 6"

    async def check_simple(reader, writer):
        await sem_start.get()
        _, s0 = await asyncio.open_unix_connection("socket")
        _, s1 = await asyncio.open_unix_connection("socket")

        s0.write(b'b\n')
        s1.write(b'c\n')
        await check_line(reader, b'b')

        s0.write(b'f\n')
        s1.write(b'd\n')
        await check_line(reader, b'c')

        s1.close()
        await check_line(reader, b'd')

        s0.close()
        await check_line(reader, b'f')

        await sem_end.put(0)

    async def main_simple():
        nonlocal sem_start, sem_end
        sem_start, sem_end = asyncio.Queue(1), asyncio.Queue(1)
        chk = await asyncio.start_unix_server(check_simple, "sock_o")
        m = await merge_server("socket", "sock_o")
        await sem_start.put(0)
        await sem_end.get()
        assert lines_read == 4, f"{lines_read} == 4"

    # asyncio.run(main_simple())
    lines_read = 0

    asyncio.run(main_complex())


if __name__ == '__main__':
    test_main()
