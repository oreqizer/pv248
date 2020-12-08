# You can drop your parser from hw3 into this file, if you want to
# use it.
from classes import Nick, Join, Message, Part, Replay, Atom, Boolean, String, Number, Identifier, Compound

# === PARSER ===


def parse(s):
    root = parser(tokenize(s))
    if type(root) is not Compound:
        raise Exception(
            f"invalid root format. want {Compound}, got {type(root)}")

    iden = root[0]
    if type(iden) is not Identifier:
        raise Exception(
            f"invalid command format. want {Identifier}, got {type(iden)}")

    cmd = str(iden)
    if cmd == "nick":
        return parse_nick(root)
    if cmd == "join":
        return parse_join(root)
    if cmd == "message":
        return parse_message(root)
    if cmd == "part":
        return parse_part(root)
    if cmd == "replay":
        return parse_replay(root)

    raise Exception(f"unknown command: {cmd}")


def parse_nick(root):
    # (nick "{nickname}")
    if len(root) != 2:
        raise Exception(
            f"invalid number of argumetns. want 2, got {len(root)}")

    nickname = root[1]
    if type(nickname) is not String:
        raise Exception(
            f"invalid argument #1. want {String}, got {type(nickname)}")

    nickname_value = repr(nickname)
    if len(nickname_value) > 0 and nickname_value[0] == '#':
        raise Exception(f"invalid argument #1. nickname cannot start with #")

    return Nick(nickname_value)


def parse_join(root):
    # (join "{channel}")
    if len(root) != 2:
        raise Exception(
            f"invalid number of argumetns. want 2, got {len(root)}")

    channel = root[1]
    if type(channel) is not String:
        raise Exception(
            f"invalid argument #1. want {String}, got {type(channel)}")

    channel_value = repr(channel)
    if not is_channel(channel_value):
        raise Exception(
            f"invalid channel format. want #<alphanum>, got {channel_value}")

    return Join(channel_value)


def parse_message(root):
    # (message "{channel}" "{text}")
    if len(root) != 3:
        raise Exception(
            f"invalid number of argumetns. want 3, got {len(root)}")

    channel = root[1]
    if type(channel) is not String:
        raise Exception(
            f"invalid argument #1. want {String}, got {type(channel)}")

    channel_value = repr(channel)
    if not is_channel(channel_value):
        raise Exception(
            f"invalid channel format. want #<alphanum>, got {channel_value}")

    text = root[2]
    if type(text) is not String:
        raise Exception(
            f"invalid argument #2. want {String}, got {type(text)}")

    return Message(channel_value, repr(text))


def parse_part(root):
    # (part "{channel}")
    if len(root) != 2:
        raise Exception(
            f"invalid number of argumetns. want 2, got {len(root)}")

    channel = root[1]
    if type(channel) is not String:
        raise Exception(
            f"invalid argument #1. want {String}, got {type(channel)}")

    channel_value = repr(channel)
    if not is_channel(channel_value):
        raise Exception(
            f"invalid channel format. want #<alphanum>, got {channel_value}")

    return Part(channel_value)


def parse_replay(root):
    # (replay "{channel}" {unix timestamp})
    if len(root) != 3:
        raise Exception(
            f"invalid number of argumetns. want 3, got {len(root)}")

    channel = root[1]
    if type(channel) is not String:
        raise Exception(
            f"invalid argument #1. want {String}, got {type(channel)}")

    channel_value = repr(channel)
    if not is_channel(channel_value):
        raise Exception(
            f"invalid channel format. want #<alphanum>, got {channel_value}")

    timestamp = root[2]
    if type(timestamp) is not Number:
        raise Exception(
            f"invalid argument #2. want {Number}, got {type(timestamp)}")

    return Replay(channel_value, int(timestamp))


# === RESPONSES ===


def make_ok():
    # (ok)
    root = Compound([Identifier("ok")])

    return str(root) + '\n'


def make_error(text):
    # (error "{text}")
    root = Compound([Identifier("error"), String(text)])

    return str(root) + '\n'


def make_message(channel, timestamp, nickname, text):
    # (message "{channel}" {unix timestamp} "{nickname}" "{text}")
    root = Compound([
        Identifier("message"),
        String(channel),
        Number(timestamp),
        String(nickname),
        String(text),
    ])

    return str(root) + '\n'


# === UTILS ===


def is_channel(s):
    if len(s) < 2:
        return False
    hashtag = s[0]
    if hashtag != '#':
        return False
    for c in s[1:]:
        if not c.isalnum():
            return False
    return True


def parser(token):
    if token == '':
        return Atom('')

    if type(token) == list:
        return Compound([parser(x) for x in token])

    if type(token) == str:
        if len(token) >= 2 and token[0] == '"' and token[-1] == '"':
            return String(token[1:-1])

        if token == '#f':
            return Boolean(False)

        if token == '#t':
            return Boolean(True)

        num = maybe_number(token)
        if num is not None:
            return Number(num)

        if is_identifier(token):
            return Identifier(token)

    raise Exception(f"invalid token: {token}")


def tokenize(s):
    expr = s.strip()
    if len(expr) < 2 or expr[0] not in '([' or expr[-1] not in ')]':
        # Atom
        return expr

    word = ''          # Current word-in-progress
    words = []         # Resulting words of current compound
    stack = [words]    # Resulting stack
    depth = []         # ( ) or [ ] nesting
    escaped = False    # Escaped chars in strings
    is_string = False  # Is the current word a string
    was_string = False  # Was a string

    for c in expr:
        # Loop start
        if escaped:
            if c not in '"\\':
                raise Exception(f"invalid escaped character: {c}")
            word += c
            escaped = False
            continue

        if was_string:
            if c not in ' )]':
                raise Exception(f"invalid character after string: {c}")
            was_string = False

        if c in '([':
            # Bracket/paren enter
            if len(depth) > 0:
                stack.append([])
                words = stack[-1]
            depth.append(c)
            continue

        if c in ')]':
            # Paren leave
            if len(depth) == 0:
                raise Exception("paren/bracket mismatch")
            left = depth.pop()
            if c == ")" and left != '(' or c == "]" and left != "[":
                raise Exception("paren/bracket mismatch")
            if len(word) > 0:
                words.append(word)
                word = ''
            if len(depth) > 0:
                n = stack.pop()
                words = stack[-1]
                words.append(n)
            continue

        if is_string:
            if c in '\\':
                escaped = True
                continue

            if c == '"':
                is_string = False
                was_string = True
                word += c
                words.append(word)
                word = ''
                continue

            word += c
            continue

        if c == '"':
            is_string = True
            word += c
            continue

        if len(word) > 0 and c == ' ':
            words.append(word)
            word = ''
            continue

        if c != ' ':
            word += c
        # Loop end

    if is_string:
        raise Exception("string mismatch")

    if len(depth) > 0:
        raise Exception("paren / bracket mismatch")

    if len(word) > 0:
        # Leftover
        words.append(word)

    return stack.pop()


def maybe_number(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except:
            return None


id_symbol = set(['!', '$', '%', '&', '*', '/',
                 ':', '<', '=', '>', '?', '_', '~'])
id_special = set(['+', '-', '.', '@', '#'])


def is_ident_char(char):
    return char.isalpha() or char in id_symbol


def is_identifier(expr):
    first = expr[0]
    if len(expr) == 1 and first in ('+', '-'):
        return True

    if is_ident_char(first):
        return all([is_ident_char(c) or c.isnumeric() or c in id_special for c in expr])

    raise Exception("unknown identifier")
