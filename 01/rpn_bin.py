from functools import reduce

# The second exercise is rather simple: take the RPN evaluator from
# the previous exercise, and extend it with the following binary
# operators: ‹+›, ‹-›, ‹*›, ‹/›, ‹**›. On top of that, add two
# ‘greedy’ operators, ‹sum› and ‹prod›, which reduce the entire
# content of the stack to a single number.

# Note that we write the stack with ‘top’ to the right, and
# operators take arguments from left to right in this ordering (i.e.
# the top of the stack is the right argument of binary operators).
# This is important for non-commutative operators.

# This exercise is one of the two which you can submit this week,
# and is worth «0.5 points».

def rpn_eval(rpn):
    stack = []
    for e in rpn:
        if e == "neg":
            stack[-1] *= -1
            continue
        
        if e == "recip":
            stack[-1] = 1/stack[-1]
            continue
        
        if e == "+":
            n2 = stack.pop()
            n1 = stack.pop()
            stack.append(n1 + n2)
            continue
        
        if e == "-":
            n2 = stack.pop()
            n1 = stack.pop()
            stack.append(n1 - n2)
            continue
        
        if e == "*":
            n2 = stack.pop()
            n1 = stack.pop()
            stack.append(n1 * n2)
            continue
        
        if e == "/":
            n2 = stack.pop()
            n1 = stack.pop()
            stack.append(n1 / n2)
            continue
        
        if e == "**":
            n2 = stack.pop()
            n1 = stack.pop()
            stack.append(n1 ** n2)
            continue
        
        if e == "sum":
            stack = [reduce(lambda a, b: a + b, stack)]
            continue
        
        if e == "prod":
            stack = [reduce(lambda a, b: a * b, stack)]
            continue

        stack.append(e)
    return stack

# Some test cases are included below. Write a few more test cases to
# convince yourself that your code works correctly. If you didn't
# see it yet, you should make a short detour to ‹varargs.py› before
# you come back to the last round of RPNs, in ‹rpn_gen.py›.


def test_main():

    rpn = [2, -2, '+']
    assert rpn_eval(rpn) == [0]

    rpn = [3, 7, '*']
    assert rpn_eval(rpn) == [21]

    rpn = [8, 2, "recip", '/']
    assert rpn_eval(rpn) == [16]

    rpn = [-1, 3, '-', 2, '+', 4, "neg", 2, '**']
    assert rpn_eval(rpn) == [-2, 16]

    rpn = [3, -1, 9, '*', 22, 100, "neg", "sum"]
    # [ 3, -9, 22, -100, sum ]
    assert rpn_eval(rpn) == [-84]


if __name__ == "__main__":
    test_main()
