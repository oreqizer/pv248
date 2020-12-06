# Implement ‹parse› here. You can define helper classes either here
# or in ‹classes.py› (the latter will not be directly imported by
# the tests).
import re

from classes import Atom, Boolean, String, Number, Identifier, Compound


def parse(s):
    try:
        return parser(s)
    except Exception as err:
        print(f"Parse error: {err}")
        return None


def parser(s):
    if s == '':
        raise Exception("something is wrong")

    res = tokenize(s)
    if res == '':
        return Atom('')

    if type(res) == str:
        if len(res) >= 2 and res[0] == '"' and res[-1] == '"':
            return String(res[1:-1])

        if res == '#f':
            return Boolean(False)

        if res == '#t':
            return Boolean(True)

        num = maybe_number(res)
        if num is not None:
            return Number(num)

        if is_identifier(res):
            return Identifier(res)

        raise Exception("invalid token")

    return Compound([parser(x) for x in res])


def tokenize(s):
    expr = s.strip()
    if len(expr) < 2 or expr[0] not in '([' or expr[-1] not in ')]':
        # Atom
        return expr

    words = []         # Resulting words
    word = ''          # Current word-in-progress
    depth = []         # ( ) or [ ] nesting
    escaped = False    # Escaped chars in strings
    is_string = False  # Is the current word a string

    for c in expr:
        # Loop start
        if escaped:
            if c not in '"\\':
                raise Exception("invalid escaped character")
            word += c
            escaped = False
            continue

        if c in '([':
            # Bracket/paren enter
            depth.append(c)
            continue

        if c == ')':
            # Paren leave
            left = depth.pop()
            if left != '(':
                raise Exception("paren/bracket mismatch")
            if len(depth) == 0 and len(word) > 0:
                words.append(word)
                word = ''
            continue

        if c == ']':
            # Bracket leave
            left = depth.pop()
            if left != '[':
                raise Exception("paren/bracket mismatch")
            if len(depth) == 0 and len(word) > 0:
                words.append(word)
                word = ''
            continue

        if is_string:
            if c in '\\':
                escaped = True
                continue

            if c == '"':
                is_string = False
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

    if len(word) > 0:
        # Leftover
        words.append(word)

    return words


# === UTILS ===


def maybe_number(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except:
            return None


id_symbol  = set(['!', '$', '%', '&', '*', '/', ':', '<', '=', '>', '?', '_', '~'])
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
