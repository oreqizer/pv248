# Helper classes, as you see fit.
import time

# === SERVER ===


class State:
    def __init__(self):
        self.users = {}
        self.channels = {}

    def join(self, user, channel_name):
        if channel_name not in self.channels:
            ch = Channel(channel_name)
            self.channels[ch.name] = ch

        ch = self.channels[channel_name]
        ch.join(user)
        user.join(ch)

    def part(self, user, channel_name):
        ch = self.get_channel(channel_name)
        ch.part(user)
        user.part(ch)

    def get_channel(self, name):
        if name not in self.channels:
            raise Exception(f"no channel named {name}")
        return self.channels[name]

    def get_user_channel(self, user, channel_name):
        ch = self.get_channel(channel_name)
        if user.nickname not in self.users:
            raise Exception(f"user {user.nickname} does not exist")
        if not ch.has(user) or not user.joined(ch):
            raise Exception(f"user {user.nickname} not in channel {channel_name}")
        return ch


class User:
    def __init__(self, nickname, writer):
        self.nickname = nickname
        self.writer = writer
        self.channels = set()

    def join(self, channel):
        if channel in self.channels:
            raise Exception(
                f"user {self.nickname} is already in channel {channel.name}")
        self.channels.add(channel)

    def part(self, channel):
        if channel not in self.channels:
            raise Exception(
                f"user {self.nickname} is not in channel {channel.name}")
        self.channels.remove(channel)

    def joined(self, channel):
        return channel in self.channels


class ChannelMessage:
    def __init__(self, user, text):
        self.user = user
        self.text = text
        self.timestamp = time.time()


class Channel:
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.users = set()

    def join(self, user):
        if user in self.users:
            raise Exception(
                f"user {user.nickname} is already in channel {self.name}")
        self.users.add(user)

    def part(self, user):
        if user not in self.users:
            raise Exception(
                f"user {user.nickname} is not in channel {self.name}")
        self.users.remove(user)

    def send(self, msg):
        self.messages.append(msg)

    def has(self, user):
        return user in self.users

    def replay(self, timestamp):
        if timestamp > time.time():
            raise Exception(f"cannot replay from the future")
        return [m for m in self.messages if m.timestamp >= timestamp]


# === COMMANDS ===


class Nick:
    def __init__(self, nickname):
        self.nickname = nickname

    def __eq__(self, o):
        return self.nickname == o.nickname

    def __str__(self):
        return f"Nick({self.nickname})"


class Join:
    def __init__(self, channel):
        self.channel = channel

    def __eq__(self, o):
        return self.channel == o.channel

    def __str__(self):
        return f"Join({self.channel})"


class Message:
    def __init__(self, channel, text):
        self.channel = channel
        self.text = text

    def __eq__(self, o):
        return self.channel == o.channel and self.text == o.text

    def __str__(self):
        return f"Message({self.channel}, {self.text})"


class Part:
    def __init__(self, channel):
        self.channel = channel

    def __eq__(self, o):
        return self.channel == o.channel

    def __str__(self):
        return f"Join({self.channel})"


class Replay:
    def __init__(self, channel, timestamp):
        self.channel = channel
        self.timestamp = timestamp

    def __eq__(self, o):
        return self.channel == o.channel and self.timestamp == o.timestamp

    def __str__(self):
        return f"Replay({self.channel}, {self.timestamp})"


# === LISP ===


class Atom:
    def __init__(self, value):
        self.value = value

    def __eq__(self, o):
        return self.value == o.value

    def __str__(self):
        return str(self.value)

    def is_atom(self):
        return True

    def is_bool(self):
        return isinstance(self, Boolean)

    def is_compound(self):
        return isinstance(self, Compound)

    def is_identifier(self):
        return isinstance(self, Identifier)

    def is_literal(self):
        return isinstance(self, Literal)

    def is_number(self):
        return isinstance(self, Number)

    def is_string(self):
        return isinstance(self, String)


class Literal(Atom):
    def __init__(self, value):
        super().__init__(value)


class Boolean(Literal):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return '#t' if self.value else '#f'

    def __bool__(self):
        return self.value


class Compound(Atom):
    def __init__(self, values: list):
        super().__init__(values)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, i):
        return self.value[i]

    def __eq__(self, o):
        return str(self) == str(o)

    def __iter__(self):
        self.number = 0
        return self

    def __next__(self):
        if self.number == len(self.value):
            raise StopIteration

        res = self.value[self.number]
        self.number += 1

        return res

    def __str__(self):
        return f'({" ".join([str(x) for x in self.value])})'

    def is_atom(self):
        return False


class Identifier(Atom):
    def __init__(self, value):
        super().__init__(value)


class Number(Literal):
    def __init__(self, value):
        super().__init__(value)

    def do(self, o, fn):
        return fn(self.value, o.value if isinstance(o, Number) else o)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __eq__(self, o):
        return self.do(o, lambda a, b: a == b)

    def __lt__(self, o):
        return self.do(o, lambda a, b: a < b)

    def __gt__(self, o):
        return self.do(o, lambda a, b: a > b)

    def __add__(self, o):
        return self.do(o, lambda a, b: a + b)

    def __radd__(self, o):
        return self.do(o, lambda a, b: b + a)

    def __sub__(self, o):
        return self.do(o, lambda a, b: a - b)

    def __rsub__(self, o):
        return self.do(o, lambda a, b: b - a)

    def __mul__(self, o):
        return self.do(o, lambda a, b: a * b)

    def __rmul__(self, o):
        return self.do(o, lambda a, b: b * a)

    def __floordiv__(self, o):
        return self.do(o, lambda a, b: a // b)

    def __rfloordiv__(self, o):
        return self.do(o, lambda a, b: b // a)

    def __truediv__(self, o):
        return self.do(o, lambda a, b: a / b)

    def __rtruediv__(self, o):
        return self.do(o, lambda a, b: b / a)


class String(Literal):
    def __init__(self, value):
        super().__init__(value)

    def __repr__(self):
        return self.value.replace("\\", "\\\\").replace('"', '\\"')

    def __str__(self):
        return f'"{repr(self)}"'
