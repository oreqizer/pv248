# Write an evaluator for a very small lisp-like language (cf. hw3,
# ‹08/minilisp.py›). Let there only be compound expressions which
# always have an integer arithmetic operator in the first position
# (‹+›, ‹-›, ‹*›, ‹/›) and the remainder of the compound are either
# non-negative integer constants or other compounds.


from functools import reduce


def minieval(expr):
    return parse(tokenize(expr))


def parse(exp):
    if type(exp) == str and exp.isnumeric():
        return int(exp)

    if type(exp) == list:
        if len(exp) < 2:
            raise Exception(f"invalid list, got {exp}")

        op = exp[0]
        args = [a if type(a) is int else parse(a) for a in exp[1:]]
        if op == "+":
            return reduce(lambda a, b: a + b, args)
        if op == "-":
            return reduce(lambda a, b: a - b, args)
        if op == "*":
            return reduce(lambda a, b: a * b, args)
        if op == "/":
            return reduce(lambda a, b: a / b, args)
        raise Exception(f"invalid oparator, got {op}")

    raise Exception(f"invalid parse input, got {exp}")


def tokenize(s):
    expr = s.strip()

    is_atom = True     # Is an atom?
    word = ''          # Current word-in-progress
    words = []         # Resulting words of current compound
    stack = [words]    # Resulting stack
    depth = []         # ( ) or [ ] nesting
    escaped = False    # Escaped chars in strings
    is_string = False  # Is the current word a string
    was_string = False # Was a string

    for i, c in enumerate(expr):
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

        if c in '([':
            # Bracket/paren enter
            is_atom = False
            if len(depth) > 0:
                stack.append([])
                words = stack[-1]
            if len(depth) == 0 and i != 0:
                raise Exception("invalid brackets")
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

        if c == '"':
            is_string = True
            word += c
            continue

        if c == ' ':
            if len(depth) == 0:
                raise Exception("invalid atom, cannot contain spaces")
            if len(word) > 0:
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

    res = stack.pop()
    if is_atom:
        return res[0]

    return res


# ===============


def test_main():
    assert minieval("4") == 4
    assert minieval("(+ 4 4)") == 8
    assert minieval("(* 2 2)") == 4
    assert minieval("(+ (* 2 2) 4)") == 8
    assert minieval("(/ (* 2 2) 2)") == 2
    assert minieval("(/ (+ 2 2) (* 2 2))") == 1
    assert minieval("(- (+ 2 (- 2 1)) (* 2 2))") == -1
    assert minieval("(+ 1 2 3)") == 6
    assert minieval("(+ 10 5)") == 15


if __name__ == "__main__":
    test_main()
