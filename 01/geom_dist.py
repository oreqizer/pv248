from math import isclose, sqrt
from geom_types import *  # as before
from geom_intersect import intersect_line_line

# In case there are no intersections, it makes sense to ask about
# distances of two objects. In this case, it also makes sense to
# include points, and we will start with those:


def distance_point_point(a, b):
    diff = b - a
    return sqrt(diff.x**2 + diff.y**2)


def distance_point_line(p, a):
    n = a.vec.normal()
    cross = intersect_line_line(a, Line(p, p.translated(n)))[0]
    return distance_point_point(cross, p)

# If we already have the point-line distance, it's easy to also find
# the distance of two parallel lines:


def distance_line_line(p, q):
    return distance_point_line(q.point, p)

# Circles vs points are rather easy, too:


def distance_point_circle(a, c):
    pass

# A similar idea works for circles and lines. Note that if they
# intersect, we set the distance to 0.


def distance_line_circle(p, c):
    pass

# And finally, let's do the friendly dispatch function:


def distance(a, b):
    pass

# Probably time for some testcases. That wraps up the seminar for
# today.


def test_main():
    test_point_point()
    test_point_line()
    test_line_line()
    #test_point_circle()
    #test_line_circle()
    #test_distance()


def test_point_point():
    p1 = Point(9, 7)
    p2 = Point(3, 2)
    assert isclose(distance_point_point(p1, p2), 7.81024967590665)


def test_point_line():
    p = Point(2, -1)
    l = Line(Point(3, 6), Point(-4, -2))
    assert isclose(distance_point_line(p, l), 3.85695556037274)


def test_line_line():
    l1 = Line(Point(-3, -6), Point(3, 1))
    l2 = Line(Point(3, 6), Point(-3, -1))
    assert isclose(distance_line_line(l1, l2), 3.25395686727984)


def test_point_circle():

    # point outside circle
    p = Point(0, -2)
    c = Circle(Point(2, 9), 2)
    assert isclose(distance_point_circle(p, c), 9.18033988749894)

    # point within circle
    p = Point(3, 2)
    c = Circle(Point(2, 5), 4)
    assert isclose(distance_point_circle(p, c), 0.83772233983162)

    # point on circle
    p = Point(0, 1)
    c = Circle(Point(0, 5), 4)
    assert isclose(distance_point_circle(p, c), 0)


def test_line_circle():
    l = Line(Point(1, -3), Point(2, -1))
    c = Circle(Point(2, 7), 2)
    assert isclose(distance_line_circle(l, c), 1.57770876399966)


def test_distance():
    p1 = Point(9, 7)
    p2 = Point(3, 2)
    assert isclose(distance(p1, p2), 7.81024967590665)

    p = Point(3, 2)
    c = Circle(Point(2, 5), 4)
    assert isclose(distance(c, p), 0.83772233983162)


if __name__ == "__main__":
    test_main()
