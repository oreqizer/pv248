# Write an evaluator for a very small lisp-like language (cf. hw3,
# ‹08/minilisp.py›). Let there only be compound expressions which
# always have an integer arithmetic operator in the first position
# (‹+›, ‹-›, ‹*›, ‹/›) and the remainder of the compound are either
# non-negative integer constants or other compounds.

def minieval(expr):
    pass


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
