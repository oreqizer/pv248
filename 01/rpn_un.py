# In the first (short) series of exercises, we will implement a
# simple RPN (Reverse Polish Notation) evaluator. The entry point
# will be a single function, with the following prototype:

def rpn_eval( rpn ):
    pass

# The ‹rpn› argument is a list with two kinds of objects in it:
# numbers (of type ‹int›, ‹float› or similar) and operators (for
# simplicity, these will be of type ‹str›).  To evaluate an RPN
# expression, we will need a stack (which can be represented using a
# ‹list›, which has useful ‹append› and ‹pop› methods).

# Implement the following unary operators: ‹neg› (for negation, i.e.
# unary minus) and ‹recip› (for reciprocal, i.e. the multiplicative
# inverse).

# The result of ‹rpn_eval› should be the stack at the end of the
# computation. Below are a few test cases to check the
# implementation works as expected.  You are free to add your own
# test cases. When you are done, you can continue with ‹rpn_bin.py›.

def test_main():
    rpn_num = [ 5 ]
    assert rpn_eval( rpn_num ) == [ 5 ]

    rpn_neg = [ 1, "neg" ]
    assert rpn_eval( rpn_neg ) == [ -1 ]

    rpn_rec = [ 2, "recip" ]
    assert rpn_eval( rpn_rec ) == [ 1/2 ]

    rpn_n = [ -1/7, "recip" ]
    assert rpn_eval( rpn_n ) == [ -7 ]

    rpn_simp = [ 1, "recip", "neg" ]
    assert rpn_eval( rpn_simp ) == [ -1 ]

    rpn = [ 4, "neg", "recip", "neg", "neg", "recip", "neg",
            "recip", "recip" ]
    assert rpn_eval( rpn ) == [ 4 ]

    rpn_nums = [ 5, 1/9, "recip", 2, "neg", "recip", -1, "neg" ]
    assert rpn_eval( rpn_nums ) == [ 5, 9, -1/2, 1 ]

if __name__ == "__main__":
    test_main()
