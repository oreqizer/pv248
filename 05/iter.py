# Implement these 4 utilities on iterables:
#
#  • prefix and suffix list
#  • prefix and suffix sum
#
# Examples:
#
#     dump( prefixes( [ 1, 2, 3 ] ) ) # [] [1] [1, 2] [1, 2, 3]
#     dump( suffixes( [ 1, 2, 3 ] ) ) # [] [3] [2, 3] [1, 2, 3]

import types

class PrefixIter:
    def __init__(self, l):
        self.list = l
        self.i = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.i > len(self.list):
            raise StopIteration
        i = self.i
        self.i += 1
        return self.list[0:i]

class PrefixSum:
    def __init__(self, l):
        self.list = l
        self.i = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.list == []:
            raise StopIteration
        self.i += self.list.pop(0)
        return self.i

def prefixes_iter(list_in):
    return PrefixIter(list_in)


def prefixes_gen(list_in):
    l = len(list_in)
    for i in range(0, l+1):
        yield list_in[0:i]


def suffixes(list_in):
    l = len(list_in)
    for i in range(l, -1, -1):
        yield list_in[i:l]


def prefix_sum(list_in):
    return PrefixSum(list_in)


def suffix_sum(list_in):
    l = len(list_in)
    s = 0
    for i in range(l-1, -1, -1):
        s += list_in[i]
        yield s

# Implement the prefix list both using an iterator (an object with
# __iter__) and using a generator. Pick one approach for each of the
# remaining 3, but make sure there's at least one iterator and one
# generator among them.

# Go on to ‹flat.py›.


def test_main():

    res = [[], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4]]

    for i in prefixes_iter([1, 2, 3, 4]):
        assert i in res
        res.remove(i)

    assert not res  # emptied

    res = [[], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4]]
    assert isinstance(prefixes_gen([]), types.GeneratorType)

    for i in prefixes_gen([1, 2, 3, 4]):
        assert i in res
        res.remove(i)

    assert not res

    res = [[], [7], [8, 7], [6, 8, 7], [5, 6, 8, 7]]

    for i in suffixes([5, 6, 8, 7]):
        assert i in res
        res.remove(i)

    assert not res  # emptied

    count = 0
    for item in prefix_sum([1, 2, 3, 4, 5]):
        count += 1  # is iterable
    assert count == len([1, 2, 3, 4, 5])

    assert list(prefix_sum([1, 2, 3, 4, 5])) == [1, 3, 6, 10, 15]

    count = 0
    for item in suffix_sum([1, 2, 3, 4, 5]):
        count += 1  # is iterable
    assert count == len([1, 2, 3, 4, 5])

    assert list(suffix_sum([1, 2, 3, 4, 5])) == [5, 9, 12, 14, 15]


if __name__ == "__main__":
    test_main()
