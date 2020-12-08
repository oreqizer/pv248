# Implement the server here.
import asyncio
import time

from classes import State, User, ChannelMessage, Channel, Nick, Join, Message, Part, Replay
from lisp import parse, make_ok, make_error, make_message


PATH = "chatsock"


# === HANDLERS ===


async def user_write(user, s):
    user.writer.write(s)
    await user.writer.drain()


async def handle_cmd(state, user, cmd):
    w = user.writer

    try:
        if type(cmd) == Join:
            state.join(user, cmd.channel)
            w.write(make_ok())
            return

        if type(cmd) == Message:
            ch = state.get_user_channel(user, cmd.channel)
            msg = ChannelMessage(user, cmd.text)
            ch.send(msg)
            await asyncio.gather(*[await user_write(u, msg) for u in ch.users])
            return

        if type(cmd) == Part:
            state.part(user, cmd.channel)
            w.write(make_ok())
            return

        if type(cmd) == Replay:
            ch = state.get_user_channel(user, cmd.channel)
            msgs = ch.replay(cmd.timestamp)
            w.write(make_ok())
            await w.drain()
            for m in msgs:
                w.write(make_message(ch.name, m.timestamp, user.nickname, m.text))
            return

        w.write(make_error(f"unknown channel command: {cmd}"))
    except Exception as err:
        w.write(make_error(str(err)))


# === SERVER ===


def make_handler(state):
    async def handler(reader, writer):
        user = None
        while True:
            if reader.at_eof():
                # Closed connection
                state.users.pop(user.nickname)
                writer.close()
                await writer.wait_closed()
                return

            s = await reader.readline()
            cmd = parse(s.decode())
            if user is None:
                # New connection
                if type(cmd) != Nick:
                    return make_error("set up session with the 'nick' command")
                
                if cmd.nickname in state.users:
                    return make_error("nickname taken")

                user = User(cmd.nickname, writer)
                state.users[cmd.nickname] = user

                writer.write(make_ok())
                await writer.drain()
                continue

            if type(cmd) == Nick:
                writer.write(make_error("session already set up"))
                await writer.drain()
                continue

            await handle_cmd(state, user, cmd)
            await writer.drain()

    return handler


async def serve():
    state = State()
    server = await asyncio.start_unix_server(make_handler(state), path=PATH)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(serve())
