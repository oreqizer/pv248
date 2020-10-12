# We first import all the classes from the previous exercise, since
# we will want to use them.

from math import isclose
from geom_types import Point, Vector, Line, Segment, Circle

# We will want to compute intersection points of a few object type
# combinations. We will start with lines, which are the simplest.
# You can find closed-form general solutions for all the problems in
# this exercise on the internet. Use them.

# This exercise is the second that you can submit. You will need to
# include ‹geom_types.py› as well, but the points are all attached
# to this exercise (i.e. submitting ‹geom_types.py› alone will not
# earn you any points).

# Line-line intersect either returns a list of points, or a Line, if
# the two lines are coincident.

def det(a, b):
    a_x, a_y = a
    b_x, b_y = b
    return a_x * b_y - a_y * b_x

def intersect_line_line(p, q):
    if p == q:
        return p

    p_p1, p_p2 = p.point_point()
    q_p1, q_p2 = q.point_point()

    x_diff = (p_p1.x - p_p2.x, q_p1.x - q_p2.x)
    y_diff = (p_p1.y - p_p2.y, q_p1.y - q_p2.y)

    div = det(x_diff, y_diff)
    if div == 0:
        return []

    d = (det((p_p1.x, p_p1.y), (p_p2.x, p_p2.y)), det((q_p1.x, q_p1.y), (q_p2.x, q_p2.y)))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div
    return [Point(x, y)]


# A variation. Re-use the line-line case.


def intersect_line_segment(p, s):
    pass

# Intersecting lines with circles is a little more tricky. Checking
# e.g. MathWorld sounds like a good idea. It might be helpful to
# translate both objects so that the circle is centered at the
# origin. The function returns a list of points.


def intersect_line_circle(p, c):
    pass

# It's probably quite obvious that users won't like the above API.
# Let's make a single ‹intersect()› that will work on anything (that
# we know how to intersect, anyway). You can use ‹type( a )› to find
# the type of object ‹a›. You can compare types for equality, too:
# ‹type( a ) == Circle› will do what you think it should.


def intersect(a, b):
    pass

# Test cases follow. Note that the tests use line equality which you
# implemented in ‹geom_types›. The last exercise for this week can
# be found in ‹geom_dist.py›.


def test_main():
    test_line_line()
    #test_line_segment()
    #test_line_circle()
    #test_intersect()


def test_line_line():

    l1 = Line(Point(2, 1), Point(-3, 7))
    l_i = intersect_line_line(l1, l1)
    assert type(l_i) == Line
    assert l_i == l1

    # Same as ‹l1›, but represented using different points.

    l2 = Line(Point(-0.5, 4), Point(7, -5))
    l_i = intersect_line_line(l1, l2)
    assert type(l_i) == Line
    assert l_i == l1
    assert l_i == l2

    l3 = Line(Point(2, 2), Point(-1, 4))
    for line in [l1, l2]:
        points = intersect_line_line(line, l3)
        assert len(points) == 1
        p = points[0]
        assert isclose(p.x, 0.125)
        assert isclose(p.y, 3.25)

    # Parallel lines.

    l1 = Line(Point(1, 1), Point(3, 5))
    l2 = Line(Point(6, 4), Point(7, 6))
    assert intersect_line_line(l1, l2) == []


def test_line_segment():

    # Segment which lies on a line.

    l = Line(Point(-2, -3), Point(-1, -2))
    s = Segment(Point(3, 2), Point(5, 4))
    assert intersect_line_segment(l, s) == s

    # Line which crosses a segment.

    s = Segment(Point(-1, -5), Point(-4, -2))
    points = intersect_line_segment(l, s)
    assert len(points) == 1
    p = points[0]
    assert isclose(p.x, -2.5)
    assert isclose(p.y, -3.5)

    # Line crosses the line in which a segment lies, but not the
    # segment itself.

    s = Segment(Point(-5, -1), Point(-4, -2))
    assert intersect_line_segment(l, s) == []

    # A line parallel to a segment.

    s = Segment(Point(1, -2), Point(2, -1))
    assert intersect_line_segment(l, s) == []


def test_line_circle():

    # A tangent line.

    l = Line(Point(0, 5), Point(3, 5))
    c = Circle(Point(3, 3), 2)
    res = intersect_line_circle(l, c)
    assert len(res) == 1
    assert isclose(res[0].x, 3)
    assert isclose(res[0].y, 5)

    # Line which crosses a circle.

    l = Line(Point(0, 3), Point(7, 3))
    res = intersect_line_circle(l, c)
    assert len(res) == 2
    p1, p2 = res[0], res[1]
    assert (isclose(p1.x, 1) and isclose(p2.x, 5)) or \
           (isclose(p2.x, 1) and isclose(p1.x, 5))
    assert isclose(p1.y, 3)
    assert isclose(p2.y, 3)

    # No intersection.

    l = Line(Point(6, -1), Point(8, 3))
    assert intersect_line_circle(l, c) == []


def test_intersect():

    # Circle with a line, swapped order.

    l = Line(Point(1, 3), Point(-1, -3))
    c = Circle(Point(2, 0), 3)
    res = sorted(intersect(c, l), key=lambda point: point.x)
    p1_exp = Point(-0.5348469228349533, -1.6045407685048603)
    p2_exp = Point(0.9348469228349539, 2.80454076850486)

    assert isclose(res[0].x, p1_exp.x) and isclose(res[0].y, p1_exp.y)
    assert isclose(res[1].x, p2_exp.x) and isclose(res[1].y, p2_exp.y)


if __name__ == "__main__":
    test_main()

# «Bonus 1»: What would happen if we had ‹intersect_line_ellipse(p,
# e)› and ‹Circle› was a subclass of ‹Ellipse›? And what should
# happen? Any ideas how to do that?

# «Bonus 2»: If you are still bored, you can do segment-segment
# and/or circle-circle intersections. Or you can implement ‹Ellipse›
# and ‹intersect_line_ellipse›.
