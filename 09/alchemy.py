# You are given:
#
#  • a list of «available» substances and their quantities,
#  • a list of «desired» substances and their quantities,
#  • a list of «transmutation rules», where each consists of an input
#    list and an output list (so a list of tuples - each
#    representing a rule - the first element of the tuple being
#    a list of outputs, the second element a list of required
#    inputs), again with substances and quantities on each.
#
# The sum of the quantities on the right hand side of the list is
# strictly less than that on the left side. Decide whether it is
# possible to get from the available substances to the desired,
# using the given rules: return a boolean. It does not matter
# whether there are leftovers. Rules can be used repeatedly.


import math


def to_dict(l):
    d = {}
    for n, q in l:
        d[n] = q
    return d


def alchemy(available, desired, rules):
    a = to_dict(available)

    stack = desired.copy()
    while len(stack) > 0:
        (name, q) = stack.pop()

        # Check available first
        a_has = a.get(name, 0)
        if a_has >= q:
            a[name] -= q
            continue

        # Take at least part
        if a_has > 0:
            a[name] = 0
            stack.append((name, q - a_has))
            continue

        # Transmute what we can
        options = []
        for want, res in rules:
            for rn, rq in res:
                if rn == name:
                    qty = math.ceil(q / rq)
                    options.append((want, (rq, qty)))

        n = q
        for (want, (rq, qty)) in options:
            max = 0
            for i in range(qty):
                if alchemy([(an, aq) for an, aq in a.items()], [(wn, wq * (i + 1)) for wn, wq in want], rules):
                    n -= rq
                    max = i + 1

            if max > 0:
                for wn, wq in want:
                    stack.append((wn, wq * max))

        # Out of options :(
        if n > 0:
            return False

    return True

# The rules from tests in a readable format, for your convenience:
#
# 3 chamomile, 4 water, 1 verbena, 2 valerian root -> relaxing concoction
# 7 ethanol -> elixir of life
# 4 water, 2 mandrake root, 2 valerian root, nightshade -> elixir of life
# 5 tea leaves -> tea tree oil
# 2 primrose oil, 2 water, 1 tea tree oil -> skin cleaning oil
# iron, carbon -> steel
# footprint -> carbon
# 6 ice -> 5 water
# 3 steel -> 1 cable
# 10 lead, philosopher stone, 2 unicorn hair -> 10 gold


def test_main():
    # what follows is the list of rules
    # each rule in the list is a tuple of two lists ( [ingredients], [result] )
    # each of the ingredients and products is again a tuple in the format (name, amount)

    rules = [([('tea leaves', 5)], [('tea tree oil', 1)]),
             ([('primrose oil', 2), ('water', 2), ('tea tree oil', 1)],
              [('skin cleaning oil', 1)]),
             ([('footprint', 1)], [('carbon', 1)]),
             ([('iron', 1), ('carbon', 1)], [('steel', 1)]),
             ([('water', 4), ('mandrake root', 2),
               ('valerian root', 2), ('nightshade', 1)],
              [('elixir of life', 1)]),
             ([('ethanol', 7)], [('elixir of life', 1)]),
             ([('chamomile', 3), ('water', 4), ('verbena', 1), ('valerian root', 1)],
              [('relaxing concoction', 1)]),
             ([('ice', 6)], [('water', 5)]),
             ([('lead', 10), ('philosopher stone', 1), ('unicorn hair', 2)],
              [('gold', 10)]),
             ([('steel', 3)], [('cable', 1)])]

    a = alchemy([('ethanol', 5)], [('ethanol', 4)], [])
    assert a, "avail: 5 ethanol, desired: 4 ethanol"

    a = alchemy([('tea leaves', 6), ('primrose oil', 4), ('zinc', 2), ('water', 10)],
                [('skin cleaning oil', 1)],
                rules)
    assert a, "skin cleaning oil, valid"

    # check that we have enough tea leaves after -> we don't
    a = alchemy([('tea leaves', 6), ('primrose oil', 4), ('zinc', 2), ('water', 10)],
                [('skin cleaning oil', 1), ('tea leaves', 2)],
                rules)
    assert not a, "not enough tea tree leaves"

    # check that we have enough tea leaves after -> we do
    a = alchemy([('tea leaves', 6), ('primrose oil', 4), ('zinc', 2), ('water', 10)],
                [('skin cleaning oil', 1), ('tea leaves', 1)],
                rules)
    assert a, "enough tea tree leaves"

    # check that we have enough tea leaves after -> we do
    a = alchemy([('tea leaves', 6), ('primrose oil', 4), ('zinc', 2), ('water', 10)],
                [('tea leaves', 1), ('skin cleaning oil', 1)],
                rules)
    assert a, "enough tea tree leaves, switch order"

    # don't have enough steel as of now but more can be created
    a = alchemy([('steel', 2), ('iron', 2), ('carbon', 1),
                 ('footprint', 2), ('water', 10)],
                [('steel', 3), ('carbon', 2)],
                rules)
    assert a, "forge steel"

    a = alchemy([('nightshade', 1), ('chamomile', 4),
                 ('ice', 20), ('water', 2),
                 ('verbena', 1), ('valerian root', 3),
                 ('ethanol', 9), ('mandrake root', 2)],
                [('elixir of life', 2), ('relaxing concoction', 1)],
                rules)
    assert a, "elixirs"

    # no rule to create ice
    a = alchemy([('ice', 1), ('water', 5)],
                [('water', 2), ('ice', 3)],
                rules)
    assert not a, "no rule to create ice"

    a = alchemy([('philosopher stone', 2), ('tea leaves', 17),
                 ('unicorn hair', 5), ('lead', 12),
                 ('water', 5)],
                [('tea tree oil', 3), ('gold', 11)],
                rules)
    assert not a, "no ingredients for enough gold"

    a = alchemy([('philosopher stone', 2), ('tea leaves', 17),
                 ('unicorn hair', 5), ('lead', 22),
                 ('water', 5)],
                [('tea tree oil', 3), ('gold', 11)],
                rules)
    assert a, "enough ingredients"

    a = alchemy([('footprint', 4), ('iron', 3), ('water', 5)],
                [('cable', 1)],
                rules)
    assert a, "3rd level of indirection"


if __name__ == "__main__":
    test_main()
