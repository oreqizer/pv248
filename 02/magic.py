# Write function ‹identify› which takes ‹rules›, a list of rules,
# and ‹data›, a ‹bytes› object to be identified. It then tries to
# apply each rule and return the identifier associated with the
# first matching rule, or ‹None› if no rules match. Each rule is
# a tuple with 2 components:
#
#  • name, a string to be returned if the rule matches,
#  • a list of patterns, where each pattern is a tuple with:
#    a. offset, an integer,
#    b. bits, a ‹bytes› object,
#    c. mask, another ‹bytes› object,
#    d. positivity, a ‹bool›.

# The mask and the pattern must have the same length. A rule matches
# the ‹data› if all of its patterns match.
#
# A pattern match is decided by comparing the slice of ‹data› at the
# given offset to the ‘bits’ field of the pattern, after both the
# slice and the bits have been bitwise-anded with the mask. The
# pattern matches iff:
#
#  • the bits and slice compare equal and positivity is ‹True›, or
#  • they compare inequal and positivity is ‹False›.

def identify(rules, data):
    pass

# ----%<----


def test_main():
    def bits(*n): return bytes(n)
    def mask(*n): return bytes([255 for _ in n])

    def eq(o, *b): return (o, bits(*b), mask(*b), True)
    def ne(o, *b): return (o, bits(*b), mask(*b), False)

    eq0_0 = ('eq0_0',  [eq(0, 0)])
    eq0_1 = ('eq0_1',  [eq(0, 1)])
    eq0_00 = ('eq0_00', [eq(0, 0, 0)])
    eq0_10 = ('eq0_10', [eq(0, 1, 0)])
    eq1_0 = ('eq1_0',  [eq(1, 0)])

    odd0 = ('odd0',   [(0, bits(1), bits(1), True)])
    even0A = ('even0A', [(0, bits(1), bits(1), False)])
    even0B = ('even0B', [(0, bits(0), bits(1), True)])

    assert identify([eq0_0, eq1_0], bits(0)) == 'eq0_0'
    assert identify([eq0_0, eq1_0], bits(1)) is None
    assert identify([eq0_0, eq1_0], bits(1, 0)) == 'eq1_0'
    assert identify([eq0_00, eq0_1], bits(1)) == 'eq0_1'
    assert identify([eq0_10, eq1_0], bits(1, 0)) == 'eq0_10'
    assert identify([eq1_0, eq0_10], bits(1, 0)) == 'eq1_0'
    assert identify([eq0_1, odd0], bits(1)) == 'eq0_1'
    assert identify([eq0_1, odd0], bits(3)) == 'odd0'
    assert identify([odd0, even0A, even0B], bits(2)) == 'even0A'
    assert identify([odd0, even0B, even0A], bits(2)) == 'even0B'
    assert identify([even0B, even0A], bits(42)) == 'even0B'
    assert identify([odd0, even0A], bits(42)) == 'even0A'
    assert identify([odd0, even0A], bits(43)) == 'odd0'


if __name__ == '__main__':
    test_main()
