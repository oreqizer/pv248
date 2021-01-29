# Implement the server here.
import asyncio
import time

from classes import State, User, ChannelMessage, Channel, Nick, Join, Message, Part, Replay
from lisp import parse, make_ok, make_error, make_message


PATH = "chatsock"

## Again, really clean code, very readable.
## Only remarks I have here are these:
## 1.)user_write() is used only once but it could've been used like everywhere.
##    Every 'write() + .drain()' should've been user_write() and it seems like
##    this is the case every time you write either in loop or when writing
##    error, so quite often.
## 2.)'if cmd.nickname in state.users:' is here twice with the same body,
##    considering how many methods you write and use only once, this could've
##    been a method too, I guess. But this is really minor and I understand that
##    it's in different, yet similar, context of code where one needs to
##    continue and the second wants to return.
## 3.)It probably is not a real problem, because it's not in the specs, but if
##    one client chose a name and then tries to 'rename' to the same name,
##    server returns error, which in my opinion is a bit weird behaviour.
## 4.)Other thing is that after the server stops, it would be better to delete
##    it from the directory so there is no mess after the program ends.
## Otherwise I really like the readability of your code and I think it will
## inspire me to be more structured in my next project :D.

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
    async def handler(reader, writer):
        user = None
        while True:
            try:
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
