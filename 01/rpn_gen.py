# Let's generalize the code. Until now, we had a fixed set of
# operators hard-coded in the evaluator. Let's instead turn our
# evaluator into an object which can be extended by the user with
# additional operators. The class should have an ‹evaluate› method
# which takes a list like before.

# On top of that, it should also have an ‹add_op(name, arity, f)›
# method, where ‹name› is the string that describes / names the
# operator, ‹arity› is the number of operands it expects and ‹f› is
# a function which implements it. The function ‹f› should take as
# many arguments as ‹arity› specifies.

from operator import add
from functools import reduce


class Evaluator:
    def __init__(self):
        self.operators = {}

    def add_op(self, name, arity, fn):
        self.operators[name] = (arity, fn)

    def evaluate(self, rpn):
        stack = []
        for e in rpn:
            if isinstance(e, (int, float)):
                stack.append(e)
                continue

            arity, fn = self.operators[e]
            if arity == 0:
                stack = [fn(*stack)]
                continue

            nums = []
            for _ in range(arity):
                nums.insert(0, stack.pop())
            stack.append(fn(*nums))
        return stack


def example():
    e = Evaluator()
    e.add_op('*', 2, lambda x, y: x * y)
    e.add_op('+', 2, lambda x, y: x + y)
    print(e.evaluate([1, 2, '+', 7, '*']))  # expect [21]

# «Bonus 1»: Allow ‹arity = 0› to mean ‘greedy’. The function passed
# to ‹add_op› in this case must accept any number of arguments.


bonus_1 = True   # enable / disable tests for bonus 1

# «Bonus 2»: Can you implement ‹Evaluator› in such a way that it
# does not require the ‹arity› argument in ‹add_op()›? How portable
# among different Python implementations do you think this is?

# As usual, write a few test cases to convince yourself that your
# code works (in addition to the ones already provided). Be sure to
# check that operators with arities 1 and 3 work, for instance.

# Then, you can continue to ‹geom_types.py›.


def test_main():
    e = Evaluator()
    e.add_op('*', 2, lambda x, y: x * y)
    e.add_op('+', 2, lambda x, y: x + y)
    assert e.evaluate([1, 2, '+', 7, '*']) == [21]

    e.add_op('neg', 1, lambda x: -x)
    assert e.evaluate([3, 'neg']) == [-3]

    e.add_op('four', 4, lambda a, b, c, d: a - b * c + d)
    e.add_op('second', 5, lambda a, b, c, d, e: b)

    # The following test case should evaluate as follows: ‹[ 2, 4,
    # 7, 'neg', 8, 'four' ]› → ‹[ 2, 4, -7, 8, 'four' ]› → ‹2 - 4 *
    # -7 + 8›.

    assert e.evaluate([1, 2, 3, 4, 5, 'second', 4, 7, 'neg',
                       8, 'four']) == [38]


def test_bonus_1():
    e = Evaluator()
    e.add_op('sum', 0, lambda *x: reduce(add, x))
    assert e.evaluate([2, -3, 4, 9, 'sum']) == [12]


if __name__ == "__main__":
    test_main()
    if bonus_1:
        test_bonus_1()
