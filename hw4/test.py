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

    await write(w1, '(nick "r0")')
    res = await readline(r1)
    assert res == '(ok)', f"{res} == (ok)"

    await write(w1, '(nick "r1")')
    res = await readline(r1)
    assert res == '(ok)', f"{res} == (ok)"

    await write(w2, '(message "#chan" "kek")')
    res = await readline(r2)
    assert res == '(error "set up session with the \'nick\' command")', f'{res} == (error "set up session with the \'nick\' command")'

    await write(w2, '(nick "r1")')
    res = await readline(r2)
    assert res == '(error "nickname taken")', f'{res} == (error "nickname taken")'

    await write(w2, '(nick "r2")')
    res = await readline(r2)
    assert res == '(ok)', f"{res} == (ok)"

    await write(w1, '(join "#chan")')
    res = await readline(r1)
    assert res == '(ok)', f"{res} == (ok)"

    await write(w1, '(join "#dump")')
    res = await readline(r1)
    assert res == '(ok)', f"{res} == (ok)"

    await write(w2, '(join "#chan")')
    res = await readline(r2)
    assert res == '(ok)', f"{res} == (ok)"

    await write(w1, '  (message "#chan" "kek")\n (message "#chan" "bur")  ')
    res = await readline(r1)
    msg1 = res
    assert res[:16] == '(message "#chan"', f'{res[:16]} == message "#chan"'
    assert res[-11:] == '"r1" "kek")', f'{res[-11:]} == "r1" "kek")'
    res = await readline(r1)
    msg2 = res
    assert res[:16] == '(message "#chan"', f'{res[:16]} == message "#chan"'
    assert res[-11:] == '"r1" "bur")', f'{res[-11:]} == "r1" "bur")'

    res = await readline(r2)
    assert res == msg1, f"{res} == {msg1}"
    assert res[:16] == '(message "#chan"', f'{res[:16]} == message "#chan"'
    assert res[-11:] == '"r1" "kek")', f'{res[-11:]} == "r1" "kek")'
    res = await readline(r2)
    assert res == msg2, f"{res} == {msg2}"
    assert res[:16] == '(message "#chan"', f'{res[:16]} == message "#chan"'
    assert res[-11:] == '"r1" "bur")', f'{res[-11:]} == "r1" "bur")'

    await write(w1, f'(replay "#chan" {time.time()})')
    res = await readline(r1)
    assert res == '(ok)', f"{res} == (ok)"
    res = await readline(r1)
    assert res == msg1, f"{res} == {msg1}"
    assert res[:16] == '(message "#chan"', f'{res[:16]} == message "#chan"'
    assert res[-11:] == '"r1" "kek")', f'{res[-11:]} == "r1" "kek")'
    res = await readline(r1)
    assert res == msg2, f"{res} == {msg2}"
    assert res[:16] == '(message "#chan"', f'{res[:16]} == message "#chan"'
    assert res[-11:] == '"r1" "bur")', f'{res[-11:]} == "r1" "bur")'

    await write(w2, f'(replay "#chan" {time.time()})')
    res = await readline(r2)
    assert res == '(ok)', f"{res} == (ok)"
    res = await readline(r2)
    assert res == msg1, f"{res} == {msg1}"
    assert res[:16] == '(message "#chan"', f'{res[:16]} == message "#chan"'
    assert res[-11:] == '"r1" "kek")', f'{res[-11:]} == "r1" "kek")'

    await write(w1, '(message "#dump" "(kek)")')
    res = await readline(r1)
    msg1 = res
    assert res[:16] == '(message "#dump"', f'{res[:16]} == message "#dump"'
    assert res[-13:] == '"r1" "(kek)")', f'{res[-13:]} == "r1" "(kek)")'

    await write(w1, '(message "#dump" "\\"kek\\"")')
    res = await readline(r1)
    msg1 = res
    assert res[:16] == '(message "#dump"', f'{res[:16]} == message "#dump"'
    assert res[-15:] == '"r1" "\\"kek\\"")', f'{res[-15:]} == "r1" "\\"kek\\"")'

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
