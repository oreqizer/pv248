from math import sqrt, acos
from math import isclose, pi

# The second set of exercises will deal with planar analytic
# geometry. First define classes ‹Point› and ‹Vector› (tests expect
# the attributes to be named ‹x› and ‹y›):


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):  # self - other
        return Point(self.x - other.x, self.y - other.y)

    def translated(self, vec):
        return Point(self.x + vec.x, self.y + vec.y)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def dot(self, other):  # dot product
        return self.x * other.x + self.y * other.y

    def angle(self, other):  # in radians
        pass

# Let us define a line next. Whether you use a point and a vector or
# two points is up to you (the constructor should take two points).
# Whichever you choose, make both representations available using
# methods (‹point_point› and ‹point_vector›, both returning a
# 2-tuple). The points returned should be the same as those passed
# to the constructor, and the vector should be the vector from the
# first point to the second point.

# Apart from the above methods, also implement an equality operator
# for two lines (‹__eq__›), which will be called when two lines are
# compared using ‹==›. In Python 2, you were also expected to
# implement its counterpart, ‹__ne__› (which stands for 'not
# equal'), but Python 3 defines ‹__ne__› automatically, by negating
# the result of ‹__eq__›.


class Line:
    def __eq__(self, other):
        if not isinstance(other, Line):
            return False
        pass  # continue the implementation

    def translated(self, vec):
        pass

    def point_point(self):
        pass

    def point_vector(self):
        pass

# The ‹Segment› class is a finite version of the same.


class Segment:
    def length(self):
        pass

    def translated(self, vec):
        pass

    def point_point(self):
        pass

# And finally a circle, using a center (a ‹Point›) and a radius (a
# ‹float›).


class Circle:
    def __init__(self, c, r):
        pass

    def center(self):
        pass

    def radius(self):
        pass

    def translated(self, vec):
        pass

# As always, write a few test cases to check that your code works.
# Please make sure that your implementation is finished before
# consulting tests; specifically, try to avoid reverse-engineering
# the tests to find out how to write your program.


def test_main():
    test_point()
    test_vector()
    test_line()
    test_segment()
    test_circle()


def point_eq(p1, p2):
    return p1.x == p2.x and p1.y == p2.y


def test_point():
    p1 = Point(1, -1)
    p2 = Point(-7, 2)

    assert point_eq(p2 - p1, Point(-8, 3))
    assert point_eq(p1 - p2, Point(8, -3))

    # check that it did not affect original points
    assert point_eq(p1, Point(1, -1))
    assert point_eq(p2, Point(-7, 2))

    v_0 = Vector(0, 0)
    assert point_eq(p1.translated(v_0), p1)

    v_24 = Vector(2, 4)
    assert point_eq(p1.translated(v_24), Point(3, 3))
    assert point_eq(p1, Point(1, -1))  # remains unaffected


def test_vector():
    v1 = Vector(2, 7)
    v2 = Vector(-5, 0)

    assert isclose(v1.length(), 7.28010988928)
    assert isclose(v2.length(), 5)

    assert v1.dot(v2) == -10
    assert isclose(v1.angle(v2), 1.8490959858)


def test_line():
    p1 = Point(2, -1)
    p2 = Point(3, 4)
    ln = Line(p1, p2)

    ln_t = ln.translated(Vector(-2, -2))
    p1_t, p2_t = ln_t.point_point()
    assert point_eq(p1_t, Point(0, -3))
    assert point_eq(p2_t, Point(1, 2))

    p1_t, v_t = ln_t.point_vector()
    assert point_eq(p1_t, Point(0, -3)) or point_eq(p1_t, Point(1, 2))
    assert isclose(v_t.length(), 5.0990195135927845)
    assert (v_t.x == -1 and v_t.y == -5) or (v_t.x == 1 and v_t.y == 5)

    # Test line equality.
    assert ln == ln

    # Parallel lines.
    l1 = Line(Point(2, 0), Point(3.5, -3))
    l2 = Line(Point(5, 2), Point(7, -2))
    assert l1 != l2

    # l1 represented by different points
    l2 = Line(Point(1.5, 1), Point(-1, 6))
    assert l1 == l2

    # Intersecting lines.
    l2 = Line(Point(-3, 2), Point(1, 9))
    assert l1 != l2


def test_segment():
    p1 = Point(2, -1)
    p2 = Point(3, 4)
    sg = Segment(p1, p2)

    sg_t = sg.translated(Vector(-1, 3))
    assert sg.length() == sg_t.length()
    p1_t, p2_t = sg_t.point_point()
    assert point_eq(p1_t, Point(1, 2))
    assert point_eq(p2_t, Point(2, 7))


def test_circle():
    c = Circle(Point(1, -1), 4)
    assert point_eq(c.center(), Point(1, -1))
    assert c.radius() == 4

    c_t = c.translated(Vector(-11, -3))
    assert point_eq(c_t.center(), Point(-10, -4))
    assert c_t.radius() == 4

    assert point_eq(c.center(), Point(1, -1))
    assert c.radius() == 4

# Since we will want to import this file into the next two
# exercises, we use the ‘current module is the main program’ trick
# below, which prevents the test code from running on import.


if __name__ == "__main__":
    test_main()

# When satisfied, go on to ‹geom_intersect.py›.
