from lisp import parse

from classes import Number
from numeval import eval_root, eval_vector, eval_matrix, eval_add, eval_dot, eval_cross, eval_mul, eval_det, eval_solve, Vector, Matrix


def assert_throw(cb):
    res = None
    try:
        res = cb()
    except:
        return
    assert False, f"no throw happened, got {res}"


def test_eval_root():
    # root: Compound
    # returns Matrix | Vector | Number
    assert_throw(lambda: eval_root(parse('(kek)')))
    assert_throw(lambda: eval_root(parse('(oopa 1 3 3 7)')))

    print("test_eval_root OK")


def test_eval_vector():
    # • ‹(vector <real>+)›    # <real>+ means 1 or more objects of type ‹real›
    res = eval_root(parse('(vector 1 3 7)'))
    assert type(res) == Vector, f'{type(res)} == Vector'
    assert res.values == [1, 3, 7], f'{res.values} == [1, 3, 7]'

    # TODO add compounds

    print("test_eval_vector OK")


def test_eval_matrix():
    # • ‹(matrix <vector>+)›  # each vector is one row, starting from the top

    # TODO

    print("test_eval_matrix OK")


def test_eval_add():
    # • ‹(+ <vector> <vector>)›     # → ‹vector› -- vector addition
    res = eval_root(parse('(+ (vector 0 2 1 6) (vector 1 1 2 1))'))
    assert res == Vector([1, 3, 3, 7]), f'{res} == Vector([1, 3, 3, 7])'

    assert_throw(lambda: eval_root(parse('(+ (vector 0 1) (vector 1 2 3))')))

    res = eval_root(parse('(+ (+ (vector 0 1 1 2) (vector 0 1 0 4)) (vector 1 1 2 1))'))
    assert type(res) == Vector, f'{type(res)} == Vector'
    assert res == Vector([1, 3, 3, 7]), f'{res} == Vector([1, 3, 3, 7])'

    # • ‹(+ <matrix> <matrix>)›     # → ‹matrix› -- matrix addition

    # TODO matrix

    print("test_eval_add OK")


def test_eval_dot():
    # • ‹(dot <vector> <vector>)›   # → ‹real›   -- dot product
    
    # TODO

    print("test_eval_dot OK")


def test_eval_cross():
    # • ‹(cross <vector> <vector>)› # → ‹vector› -- cross product
    
    # TODO

    print("test_eval_cross OK")


def test_eval_mul():
    # • ‹(* <matrix> <matrix>)›     # → ‹matrix› -- matrix multiplication
    
    # TODO

    print("test_eval_mul OK")


def test_eval_det():
    # • ‹(det <matrix>)›            # → ‹real›   -- determinant of the matrix
    
    # TODO

    print("test_eval_det OK")


def test_eval_solve():
    # • ‹(solve <matrix>)›          # → ‹vector› -- linear equation solver
    
    # TODO

    print("test_eval_solve OK")


if __name__ == "__main__":
    test_eval_root()
    test_eval_vector()
    test_eval_matrix()
    test_eval_add()
    test_eval_dot()
    test_eval_cross()
    test_eval_mul()
    test_eval_det()
    test_eval_solve()
