# Implement ‹parse› here. You can define helper classes either here
# or in ‹classes.py› (the latter will not be directly imported by
# the tests).
import re

from classes import Atom, Boolean, String, Number, Identifier, Compound


def parse(s):
    if not check_pairing(s) or s == '':
        raise Exception

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
            space = s.find(' ')
            return Identifier(s[:space] if space > 0 else s)

        raise Exception

    return Compound([parse(x) for x in res])


def tokenize(s):
    pure = s.strip()
    if len(pure) < 2 or pure[0] != '(' or pure[-1] != ')':
        # Atom
        return pure

    expr = pure[1:-1].strip()  # Expression without ( )
    words = []                 # Resulting words
    word = ''                  # Current word-in-progress
    depth = 0                  # ( ) nesting
    escaped = False            # Escaped chars in strings
    is_string = False          # Is the current word a string

    for i, c in enumerate(expr):
        word += c

        if depth > 0:
            if c == '(':
                # Bracket enter
                depth += 1

            if c == ')':
                # Bracket leave
                depth -= 1
                
            if depth == 0:
                words.append(word)
                word = ''

        elif is_string:
            if escaped:
                # Ignore next string char
                escaped = False
                continue

            if c in '"':
                # String end
                is_string = False
                words.append(word)
                word = ''

            escaped = c == '\\'

        else:
            if i - 1 >= 0 and expr[i - 1] == '"' and not c.isspace():
                # Not beginning, not inside string and not space
                raise Exception

            if c == '(':
                # Bracket enter
                depth += 1

            elif c == '"':
                # String enter
                is_string = True

            elif len(word.strip()) > 0 and c in ' ':
                # Whitespace, word end
                words.append(word)
                word = ''

        if i == len(expr) - 1 and len(word) > 0:
            # Last char and words exist
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


def check_pairing(s):
    depth = 0         # ( ) nesting
    string_apos = 0   # Number of "
    escaped = False   # Escaped chars in strings

    for c in s:
        if escaped:
            if c not in '"\\':
                raise Exception

            escaped = False
            continue

        if c == '(':
            depth += 1
            continue

        if c == ')':
            depth -= 1
            continue

        if c == '"':
            string_apos += 1
            continue

        escaped = c == '\\'

    return depth == 0 and string_apos % 2 == 0


def is_ident_char(char):
    return char.isalpha() or char in set(['!', '$', '%', '&', '*', '/', ':', '<', '=', '>', '?', '^', '_', '~'])


def is_identifier(expr):
    first = expr[0]
    if len(expr) == 1 and first in ('+', '-'):
        return True

    if is_ident_char(first):
        return all([is_ident_char(c) or c.isnumeric() or c in set(['+', '-', '.', '@', '#']) for c in expr])

    raise Exception
