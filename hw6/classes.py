# Additional types (classes) that you may want to define.
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

    def __setitem__(self, i, v):
        self.value[i] = v

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

    def __str__(self):
        res = self.value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{res}"'
