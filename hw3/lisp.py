# Implement ‹parse› here. You can define helper classes either here
# or in ‹classes.py› (the latter will not be directly imported by
# the tests).
import re

from classes import Atom, Boolean, String, Number, Identifier, Compound


def parse(s):
    try:
        tokens = tokenize(s)

        return parser(tokens)
    except Exception:
        return None


def parse_test(s):
    return parser(tokenize(s))


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
    is_atom = not (len(expr) >= 2 and expr[0] in '([' and expr[-1] in ')]')

    word = ''          # Current word-in-progress
    words = []         # Resulting words of current compound
    stack = [words]    # Resulting stack
    depth = []         # ( ) or [ ] nesting
    escaped = False    # Escaped chars in strings
    is_string = False  # Is the current word a string
    was_string = False # Was a string

    i = 0
    while len(expr) > 0:
        c, expr = expr[0], expr[1:]
        
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

        if c in '([':
            if is_atom:
                raise Exception("invalid atom")

            # Bracket/paren enter
            if len(depth) > 0:
                stack.append([])
                words = stack[-1]
            depth.append(c)
            continue

        if c in ')]':
            if is_atom:
                raise Exception("invalid atom")

            # Paren leave
            if len(depth) == 0:
                raise Exception("paren / bracket mismatch")
            left = depth.pop()
            if c == ")" and left != '(' or c == "]" and left != "[":
                raise Exception("paren / bracket mismatch")
            if len(word) > 0:
                words.append(word)
                word = ''
            if len(depth) == 0:
                break
            if len(depth) > 0:
                n = stack.pop()
                words = stack[-1]
                words.append(n)
                continue
            continue

        if c == ' ':
            if is_atom:
                raise Exception("invalid atom")

            if len(word) > 0:
                words.append(word)
                word = ''
                continue

        if c != ' ':
            word += c

        i += 1
        # Loop end

    if len(expr) > 0:
        raise Exception("invalid input, leftover expression: {expr}")

    if is_string:
        raise Exception("string mismatch")

    if len(depth) > 0:
        raise Exception("paren / bracket mismatch")

    if len(word) > 0:
        # Leftover
        words.append(word)

    res = stack.pop()
    if is_atom:
        return res[0]

    return res


# === UTILS ===


def maybe_number(s):
    try:
        if not s[0].isnumeric() and s[0] not in ('+', '-'):
            return None

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
