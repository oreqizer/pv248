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
    s = '(vector 1.0 3.0 7.0)'
    res = eval_root(parse(s))
    assert type(res) == Vector, f'{type(res)} == Vector'
    assert str(res) == s, f'{str(res)} == {s}'
    assert res.values == [1, 3, 7], f'{res.values} == [1, 3, 7]'

    assert_throw(lambda: eval_root(parse('(vector 1 "kek" 7)')))

    res = eval_root(parse('(vector 1 (dot (vector 1 0) (vector 3 2)) 7)'))
    want = Vector([1, 3, 7])
    assert res == want, f'{res} == {want}'

    print("test_eval_vector OK")


def test_eval_matrix():
    # • ‹(matrix <vector>+)›  # each vector is one row, starting from the top
    s = '(matrix (vector 1.0 3.0) (vector 3.0 7.0))'
    res = eval_root(parse(s))
    assert type(res) == Matrix, f'{type(res)} == Matrix'
    assert str(res) == s, f'{str(res)} == {s}'
    assert res.values == [Vector([1, 3]), Vector([3, 7])], f'{res.values} == [Vector([1. 3]), Vector([3, 7])]'

    assert_throw(lambda: eval_root(parse('(matrix (vector 1 3) (vector 3 7 5))')))
    assert_throw(lambda: eval_root(parse('(matrix (vector 1 3) "kek")')))

    res = eval_root(parse('(matrix (+ (vector 1 2) (vector 0 1)) (vector 3 7))'))
    want = Matrix([Vector([1, 3]), Vector([3, 7])])
    assert res == want, f'{res} == {want}'

    print("test_eval_matrix OK")


def test_eval_add():
    # • ‹(+ <vector> <vector>)›     # → ‹vector› -- vector addition
    res = eval_root(parse('(+ (vector 0 2 1 6) (vector 1 1 2 1))'))
    want = Vector([1, 3, 3, 7])
    assert res == want, f'{res} == {want}'

    assert_throw(lambda: eval_root(parse('(+ (vector 0 1) (vector 1 2 3))')))

    res = eval_root(parse('(+ (+ (vector 0 1 1 2) (vector 0 1 0 4)) (vector 1 1 2 1))'))
    want = Vector([1, 3, 3, 7])
    assert res == want, f'{res} == {want}'

    # • ‹(+ <matrix> <matrix>)›     # → ‹matrix› -- matrix addition
    res = eval_root(parse('(+ (matrix (vector 1 2 0) (vector 2 3 1)) (matrix (vector 3 1 4) (vector 0 1 0)))'))
    want = Matrix([Vector([4, 3, 4]), Vector([2, 4, 1])])
    assert res == want, f'{res} == {want}'

    assert_throw(lambda: eval_root(parse('(+ (matrix (vector 1 2)) (matrix (vector 3 1) (vector 0 1)))')))
    assert_throw(lambda: eval_root(parse('(+ (matrix (vector 1 2 3) (vector 2 3 1)) (matrix (vector 3 1) (vector 0 1)))')))

    res = eval_root(parse('(+ (matrix (+ (vector 0 1) (vector 1 1)) (vector 2 3)) (matrix (vector 3 1) (vector 0 1)))'))
    want = Matrix([Vector([4, 3]), Vector([2, 4])])
    assert res == want, f'{res} == {want}'

    print("test_eval_add OK")


def test_eval_dot():
    # • ‹(dot <vector> <vector>)›   # → ‹real›   -- dot product
    res = eval_root(parse('(dot (vector 2 1 6) (vector 1 2 1))'))
    assert res == 10.0, f'{res} == 10.0'

    assert_throw(lambda: eval_root(parse('(dot (vector 0 1) (vector 1 2 3))')))

    res = eval_root(parse('(dot (+ (vector 1 1 2) (vector 1 0 4)) (vector 1 2 1))'))
    assert res == 10.0, f'{res} == 10.0'

    print("test_eval_dot OK")


def test_eval_cross():
    # • ‹(cross <vector> <vector>)› # → ‹vector› -- cross product
    res = eval_root(parse('(cross (vector 2 1 6) (vector 1 2 1))'))
    want = Vector([-11, 4, 3])
    assert res == want, f'{res} == {want}'

    assert_throw(lambda: eval_root(parse('(cross (vector 0 1) (vector 1 2 3))')))
    assert_throw(lambda: eval_root(parse('(cross (vector 0 1) (vector 2 3))')))
    assert_throw(lambda: eval_root(parse('(cross (vector 0 1 1 3) (vector 2 3 3 7))')))

    res = eval_root(parse('(cross (+ (vector 1 1 2) (vector 1 0 4)) (vector 1 2 1))'))
    want = Vector([-11, 4, 3])
    assert res == want, f'{res} == {want}'

    print("test_eval_cross OK")


def test_eval_mul():
    # • ‹(* <matrix> <matrix>)›     # → ‹matrix› -- matrix multiplication
    res = eval_root(parse('(* (matrix (vector 1 2 0) (vector 2 3 1)) (matrix (vector 3) (vector 0) (vector 1)))'))
    want = Matrix([Vector([3]), Vector([7])])
    assert res == want, f'{res} == {want}'

    assert_throw(lambda: eval_root(parse('(* (matrix (vector 1 2 3)) (matrix (vector 3 1) (vector 0 1)))')))

    res = eval_root(parse('(* (matrix (+ (vector 0 1) (vector 1 1)) (vector 2 3)) (matrix (vector 3 1) (vector 0 1)))'))
    want = Matrix([Vector([3, 3]), Vector([6, 5])])
    assert res == want, f'{res} == {want}'

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
