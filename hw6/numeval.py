# This file should implement evaluate().
import numpy as np

import lisp
from classes import Compound, Identifier, Number


# === PARSE ===


def evaluate(s):
    try:
        return eval_root(lisp.parse(s))
    except Exception as err:
        return err


def eval_root(root):
    # root: Compound
    # returns Number | Vector | Matrix
    if type(root) is not Compound:
        raise Exception(
            f"invalid root format. want {Compound}, got {type(root)}")

    if len(root) < 2:
        raise Exception(
            f"invalid number of arguments. want 2+, got {len(root)}")

    iden = root[0]
    if type(iden) is not Identifier:
        raise Exception(
            f"invalid command format. want {Identifier}, got {type(iden)}")

    t = str(iden)
    if t == "vector":
        return eval_vector(root)
    if t == "matrix":
        return eval_matrix(root)
    if t == "+":
        return eval_add(root)
    if t == "dot":
        return eval_dot(root)
    if t == "cross":
        return eval_cross(root)
    if t == "*":
        return eval_mul(root)
    if t == "det":
        return eval_det(root)
    if t == "solve":
        return eval_solve(root)

    raise Exception(f"unknown type: {t}")


def eval_vector(root):
    # • ‹(vector <real>+)›    # <real>+ means 1 or more objects of type ‹real›
    args = [float(a) if type(a) is Number else eval_root(a) for a in root[1:]]
    for a in args:
        if type(a) is not float:
            raise Exception(
                f"invalid Vector argument, want float, got {type(a)}")

    return Vector(args)


def eval_matrix(root):
    # • ‹(matrix <vector>+)›  # each vector is one row, starting from the top
    args = [a if type(a) is Vector else eval_root(a) for a in root[1:]]
    dim = len(args[0])
    for a in args:
        if type(a) is not Vector:
            raise Exception(
                f"invalid Matrix argument, want Vector, got {type(a)}")
        if len(a) != dim:
            raise Exception(
                f"invalid Matrix argument, inconsistent vector lengths, got {len(a)}, want {dim}")

    return Matrix(args)


def eval_add(root):
    # • ‹(+ <vector> <vector>)›     # → ‹vector› -- vector addition
    # • ‹(+ <matrix> <matrix>)›     # → ‹matrix› -- matrix addition
    if len(root) != 3:
        raise Exception(
            f"invalid number of arguments. want 3, got {len(root)}")

    args = [a if type(a) in [Vector, Matrix] else eval_root(a)
            for a in root[1:]]
    a1, a2 = args[0], args[1]
    if type(a1) is type(a2):
        return a1 + a2

    raise Exception(
        f"invalid argument types, want Vector/Matrix, got {type(a1)} and {type(a2)}")


def eval_dot(root):
    # • ‹(dot <vector> <vector>)›   # → ‹real›   -- dot product
    if len(root) != 3:
        raise Exception(
            f"invalid number of arguments. want 3, got {len(root)}")

    args = [a if type(a) is Vector else eval_root(a) for a in root[1:]]
    a1, a2 = args[0], args[1]
    if type(a1) is Vector and type(a2) is Vector:
        return a1.dot(a2)

    raise Exception(
        f"invalid argument types, want Vector, got {type(a1)} and {type(a2)}")


def eval_cross(root):
    # • ‹(cross <vector> <vector>)› # → ‹vector› -- cross product
    if len(root) != 3:
        raise Exception(
            f"invalid number of arguments. want 3, got {len(root)}")

    args = [a if type(a) is Vector else eval_root(a) for a in root[1:]]
    a1, a2 = args[0], args[1]
    if type(a1) is Vector and type(a2) is Vector:
        return a1.cross(a2)

    raise Exception(
        f"invalid argument types, want Vector, got {type(a1)} and {type(a2)}")


def eval_mul(root):
    # • ‹(* <matrix> <matrix>)›     # → ‹matrix› -- matrix multiplication
    if len(root) != 3:
        raise Exception(
            f"invalid number of arguments. want 3, got {len(root)}")

    args = [a if type(a) is Matrix else eval_root(a) for a in root[1:]]
    a1, a2 = args[0], args[1]
    if type(a1) is Matrix and type(a2) is Matrix:
        return a1 * a2

    raise Exception(
        f"invalid argument types, want Matrix, got {type(a1)} and {type(a2)}")


def eval_det(root):
    # • ‹(det <matrix>)›            # → ‹real›   -- determinant of the matrix
    if len(root) != 2:
        raise Exception(
            f"invalid number of arguments. want 2, got {len(root)}")
    pass  # TODO


def eval_solve(root):
    # • ‹(solve <matrix>)›          # → ‹vector› -- linear equation solver
    if len(root) != 2:
        raise Exception(
            f"invalid number of arguments. want 2, got {len(root)}")
    pass  # TODO


# === CLASSES ===


class Vector:
    def __init__(self, values):
        self.values = values

    def __eq__(self, o):
        return self.values == o.values

    def __len__(self):
        return len(self.values)

    def __str__(self):
        exp = Compound([
            Identifier("vector"),
            *[Number(v) for v in self.values]
        ])
        return str(exp)

    def __add__(self, o):
        #  • ‹(+ <vector> <vector>)›     # → ‹vector› -- vector addition
        self.check_len(o)
        return Vector(list(np.add(self.values, o.values)))

    def dot(self, o):
        #  • ‹(dot <vector> <vector>)›   # → ‹real›   -- dot product
        self.check_len(o)
        return float(np.dot(self.values, o.values))

    def cross(self, o):
        #  • ‹(cross <vector> <vector>)› # → ‹vector› -- cross product
        if len(self) != 3 or len(o) != 3:
            raise Exception(
                f"cross product vectors must be of len(3), got {self} and {o}")
        return Vector(list(np.cross(self.values, o.values)))

    def check_len(self, o):
        if len(self) != len(o):
            raise Exception(f"vector length mismatch, got {self} and {o}")


class Matrix:
    def __init__(self, values):
        # values: [Vector]
        self.values = values
        self.x = len(values[0])
        self.y = len(values)

    def __eq__(self, o):
        return self.values == o.values

    def __len__(self):
        return len(self.values)

    def __str__(self):
        exp = Compound([
            Identifier("matrix"),
            *self.values,
        ])
        return str(exp)

    def __add__(self, o):
        # • ‹(+ <matrix> <matrix>)›     # → ‹matrix› -- matrix addition
        if self.x != o.x or self.y != o.y:
            raise Exception(
                f'addition of incompatbile matrices, {self} and {o}')
        return Matrix([Vector(list(r)) for r in np.add(self.lists(), o.lists())])

    def __mul__(self, o):
        # • ‹(* <matrix> <matrix>)›     # → ‹matrix› -- matrix multiplication
        if self.x != o.y:
            raise Exception(
                f'multiplication of incompatbile matrices, {self} and {o}')
        return Matrix([Vector(list(r)) for r in np.matmul(self.lists(), o.lists())])

    def lists(self):
        return [v.values for v in self.values]
