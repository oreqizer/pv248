# This file should implement evaluate().
import numpy as np

import lisp
from classes import Compound, Identifier, Number, String


# === PARSE ===


def evaluate(s):
    try:
        return eval_root(lisp.parse(s))
    except Exception as err:
        return Error(str(err))


def eval_root(root):
    # root: Compound
    # returns Number | Vector | Matrix
    if type(root) is Number:
        return root

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
    args = [a if type(a) is Number else eval_root(a) for a in root[1:]]
    for a in args:
        if type(a) is not Number:
            raise Exception(
                f"invalid Vector argument, want float, got {type(a)}")

    return Vector([float(a) for a in args])


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
        return Number(a1.dot(a2))

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

    arg = root[1] if type(root[1]) == Matrix else eval_root(root[1])
    return Number(arg.det())


def eval_solve(root):
    # • ‹(solve <matrix>)›          # → ‹vector› -- linear equation solver
    if len(root) != 2:
        raise Exception(
            f"invalid number of arguments. want 2, got {len(root)}")

    arg = root[1] if type(root[1]) == Matrix else eval_root(root[1])
    return arg.solve()


# === CLASSES ===


class Vector:
    def __init__(self, values):
        self.values = values

    def is_real(self):
        return False

    def is_vector(self):
        return True

    def is_matrix(self):
        return False

    def is_error(self):
        return False

    def __eq__(self, o):
        return self.values == o.values

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        self.number = 0
        return self

    def __next__(self):
        if self.number == len(self.values):
            raise StopIteration

        res = self.values[self.number]
        self.number += 1

        return Number(res)

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

    def is_real(self):
        return False

    def is_vector(self):
        return False

    def is_matrix(self):
        return True

    def is_error(self):
        return False

    def __eq__(self, o):
        return self.values == o.values

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        self.number = 0
        return self

    def __next__(self):
        if self.number == len(self.values):
            raise StopIteration

        res = self.values[self.number]
        self.number += 1

        return res

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
        return Matrix([Vector(list(r)) for r in np.add(self.rows(), o.rows())])

    def __mul__(self, o):
        # • ‹(* <matrix> <matrix>)›     # → ‹matrix› -- matrix multiplication
        if self.x != o.y:
            raise Exception(
                f'multiplication of incompatbile matrices, {self} and {o}')
        return Matrix([Vector(list(r)) for r in np.matmul(self.rows(), o.rows())])

    def det(self):
        # • ‹(det <matrix>)›            # → ‹real›   -- determinant of the matrix
        if self.x != self.y:
            raise Exception(
                f'determinant of a non-square matrix, {self}')
        return float(np.linalg.det(self.rows()))

    def solve(self):
        # • ‹(solve <matrix>)›          # → ‹vector› -- linear equation solver
        if self.x != self.y:
            raise Exception(
                f'solving a non-square matrix, {self}')
        _, s, vh = np.linalg.svd(np.matrix(self.rows()))
        null_mask = (s < 1e-15)
        null_space = np.compress(null_mask, vh, axis=0)
        res = np.transpose(null_space)
        if res.size == 0:
            res = np.array([0 for x in range(self.y)])
        else:
            res_vect = []
            for var in res.tolist():
                for val in var:
                    res_vect.append(val)
                    break
            res = np.array(res_vect)
        return Vector(list(res.flat))

    def rows(self):
        return [v.values for v in self.values]


class Error:
    def __init__(self, msg):
        self.message = msg

    def is_real(self):
        return False

    def is_vector(self):
        return False

    def is_matrix(self):
        return False

    def is_error(self):
        return True

    def __str__(self):
        exp = Compound([
            Identifier("error"),
            String(self.message),
        ])
        return str(exp)
