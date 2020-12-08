import asyncio
import time

from chatserv import serve, PATH


async def write(w, msg):
    print(" > ", msg)
    w.write(f'{msg}\n'.encode())
    await w.drain()


async def readline(r):
    res = await r.readline()
    print(" < ", res.decode()[:-1])
    return res.decode()[:-1]


async def test():
    await asyncio.sleep(0.1)

    r1, w1 = await asyncio.open_unix_connection(path=PATH)
    r2, w2 = await asyncio.open_unix_connection(path=PATH)

    await write(w1, '(nick "r1")')
    res = await readline(r1)
    assert res == '(ok)', f"{res} == (ok)"

    await write(w2, '(nick "r2")')
    res = await readline(r2)
    assert res == '(ok)', f"{res} == (ok)"

    await write(w1, '(join "#chan")')
    res = await readline(r1)
    assert res == '(ok)', f"{res} == (ok)"

    await write(w2, '(join "#chan")')
    res = await readline(r2)
    assert res == '(ok)', f"{res} == (ok)"

    await write(w1, '(message "#chan" "kek")')
    res = await readline(r1)
    msg1 = res
    assert res[:16] == '(message "#chan"', f'{res[:16]} == message "#chan"'
    assert res[-11:] == '"r1" "kek")', f'{res[-11:]} == "r1" "kek")'

    res = await readline(r2)
    assert res == msg1, f"{res} == {msg1}"
    assert res[:16] == '(message "#chan"', f'{res[:16]} == message "#chan"'
    assert res[-11:] == '"r1" "kek")', f'{res[-11:]} == "r1" "kek")'

    await write(w1, f'(replay "#chan" {time.time()})')
    res = await readline(r1)
    assert res == '(ok)', f"{res} == (ok)"
    res = await readline(r1)
    assert res == msg1, f"{res} == {msg1}"
    assert res[:16] == '(message "#chan"', f'{res[:16]} == message "#chan"'
    assert res[-11:] == '"r1" "kek")', f'{res[-11:]} == "r1" "kek")'

    await write(w1, '(part "#chan")')
    res = await readline(r1)
    assert res == '(ok)', f"{res} == (ok)"

    await write(w1, '(part "#chan")')
    res = await readline(r1)
    assert res == '(error "user r1 is not in channel #chan")', f'{res} == (error "user r1 is not in channel #chan")'

    print("OK")


async def run():
    return await asyncio.gather(
        serve(),
        test(),
    )


if __name__ == "__main__":
    asyncio.run(run())
