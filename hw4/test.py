import asyncio

from chatserv import serve, PATH


async def write(w, msg):
    w.write(f'{msg}\n'.encode())
    await w.drain()


async def readline(r):
    res = await r.readline()
    return res.decode()[:-1]


async def test():
    await asyncio.sleep(0.1)

    r1, w1 = await asyncio.open_unix_connection(path=PATH)
    r2, w2 = await asyncio.open_unix_connection(path=PATH)

    await write(w1, '(nick "r1")')
    res = await readline(r1)
    assert res == '(ok)', f"{res} == (ok)"
    print("r1 connected")

    await write(w2, '(nick "r2")')
    res = await readline(r2)
    assert res == '(ok)', f"{res} == (ok)"
    print("r2 connected")

    print("OK")


async def run():
    return await asyncio.gather(
        serve(),
        test(),
    )


if __name__ == "__main__":
    asyncio.run(run())
