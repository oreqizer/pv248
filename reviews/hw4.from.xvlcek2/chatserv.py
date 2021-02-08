##
## Hi, I tested your solution, works fine.
##
## Your code is quite easy to understand as a whole and your asyncio part
## is very simple. You haven't even used a single asyncio.queue, which is
## great (some people used 3 queues per client).
##
## You heavily used Exceptions, which makes code more readable (but may slow
## execution down on the other hand).
##
## Shorter lines would be cool, at most ~80 chars, they gets wrapped often.
##
## I hope you'll like/appriciate my review, took me a lot of time.
##

# Implement the server here.
import asyncio
import time

from classes import State, User, ChannelMessage, Channel, Nick, Join, Message, Part, Replay
from lisp import parse, make_ok, make_error, make_message


PATH = "chatsock"


# === HANDLERS ===


async def user_write(user, s):
    user.writer.write(s.encode())
    await user.writer.drain()


async def handle_cmd(state, user, cmd):
    w = user.writer

    try:
        if type(cmd) == Nick:
            if cmd.nickname in state.users:
                w.write(make_error("nickname taken").encode())
                await w.drain()
                return

            state.users.pop(user.nickname)
            user.nickname = cmd.nickname
            state.users[user.nickname] = user
            w.write(make_ok().encode())
            return

        if type(cmd) == Join:
            state.join(user, cmd.channel)
            w.write(make_ok().encode())
            return

        if type(cmd) == Message:
            ch = state.get_user_channel(user, cmd.channel)
            msg = ChannelMessage(user, cmd.text)
            ch.send(msg)
            await asyncio.gather(*[user_write(u, make_message(ch.name, msg.timestamp, user.nickname, msg.text)) for u in ch.users])
            return

        if type(cmd) == Part:
            state.part(user, cmd.channel)
            w.write(make_ok().encode())
            return

        if type(cmd) == Replay:
            ch = state.get_user_channel(user, cmd.channel)
            msgs = ch.replay(cmd.timestamp)
            w.write(make_ok().encode())
            for m in msgs:
                w.write(make_message(ch.name, m.timestamp,
                                     m.user.nickname, m.text).encode())
            return

        w.write(make_error(f"unknown channel command: {cmd}").encode())
    except Exception as err:
        w.write(make_error(str(err)).encode())


# === SERVER ===


def make_handler(state):
    ## Returning a handler is definitely interesting.
    async def handler(reader, writer):
        user = None
        while True:
            try:
                ## Documentation says `feed_eof()` needs to be called
                ## prior at_eof(), but if it works, who knows :0.
                ## https://docs.python.org/3/library/asyncio-stream.html
                if reader.at_eof():
                    # Closed connection
                    state.users.pop(user.nickname)
                    writer.close()
                    await writer.wait_closed()
                    return

                cmd = await parse(reader)
                if user is None:
                    # New connection
                    if type(cmd) != Nick:
                        writer.write(make_error("set up session with the 'nick' command").encode())
                        await writer.drain()
                        continue

                    if cmd.nickname in state.users:
                        writer.write(make_error("nickname taken").encode())
                        await writer.drain()
                        continue

                    user = User(cmd.nickname, writer)
                    state.users[cmd.nickname] = user

                    writer.write(make_ok().encode())
                    await writer.drain()
                    continue

                await handle_cmd(state, user, cmd)
                await writer.drain()

            except Exception as err:
                writer.write(make_error(str(err)).encode())
                await writer.drain()

    return handler


async def serve():
    state = State()
    server = await asyncio.start_unix_server(make_handler(state), path=PATH)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(serve())
