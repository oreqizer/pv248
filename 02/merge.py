# Write a function ‹merge_dict› which takes these 3 arguments:
#
#  • a ‹dict› instance, in which some keys are deemed equivalent:
#    the goal of ‹merge_dict› is to create a new dictionary, where
#    all equivalent keys have been merged; keys which are not
#    equivalent to anything else are left alone
#  • a ‹list› of ‹set› instances, where each ‹set› describes one set
#    of equivalent keys (the sets are pairwise disjoint), and
#    finally,
#  • a function ‹combine› which takes a ‹list› of values (not a set,
#    because we may care about duplicates): ‹merge_dict› will pass,
#    for each set of equivalent keys, all the values corresponding to
#    those keys into ‹combine›.
#
# In the output dictionary, create a single key for each equivalent
# set:
#
#  • the key is the «smallest» of the keys from the set which were
#    actually present in the input ‹dict›,
#  • the value is the result of calling ‹combine› on the list of
#    values associated with all the equivalent keys in the input
#    ‹dict›.
#
# Do not modify the input dictionary.

import copy


def merge_dict(dict_in, equiv, combine):
    res = {}

    keys_left = [k for k in dict_in.keys() if k not in [e for eq in equiv for e in eq]]
    for k in keys_left:
        res[k] = dict_in[k]
    
    for eq in equiv:
        vals = []
        key_val = None
        for key in eq:
            if key not in dict_in:
                continue

            # set proper key
            if key_val == None or key < key_val:
                key_val = key

            vals.append(dict_in[key])
        
        res[key_val] = combine(vals)

    return res


def test_main():

    def combine(x): return sum(x)
    dict_in = {1: 1, 2: 2, 3: 3, 4: 4, 5: 1, 6: 2, 7: 3}
    eq = [set([1, 3, 5, 7]), set([2, 4, 6])]

    dict_orig = dict_in.copy()
    assert merge_dict(dict_in, eq, combine) == {1: 8, 2: 8}
    assert dict_in == dict_orig

    # pylint: disable=function-redefined
    def combine(x): return sum([len(s) for s in x])
    dict_in = {2: 'two', 3: 'three', 6: 'two', 1: 'one', 9: 'woo'}
    eq = [set([2]), set([3, 6, 1])]

    dict_orig = dict_in.copy()
    assert merge_dict(dict_in, eq, combine) == {2: 3, 1: 11, 9: 'woo'}
    assert dict_in == dict_orig

    def combine(x): return sum(x)
    dict_in = {1: 9, 8: "eek", "ef": 22}
    eq = []

    dict_orig = dict_in.copy()
    assert merge_dict(dict_in, eq, combine) == dict_orig
    assert dict_in == dict_orig

    dict_in = {"ab": {7: 33, 9: 1, 13: 45}, "abcde": {3: 9, 0: 5, -1: 4},
               "foo": {1: 3, 91: 3, 4: 3, 5: -1, 8: 4}, "val": {6: 7}}
    eq_out = [set(["ab", "abcde", "val"])]
    eq_in = [set([1, 91, 8, 6]), set([3, 7, 9, -1]), set([0])]

    dict_orig = copy.deepcopy(dict_in)

    # list of dictionaries into one dictionary
    def flatten(x):
        d = {}
        for dic in x:
            d.update(dic)
        return d

    def combine(x): return merge_dict(flatten(x), eq_in, lambda y: sum(y))

    res = {"ab": {13: 45, -1: 47, 0: 5, 6: 7},
           "foo": {1: 3, 91: 3, 4: 3, 5: -1, 8: 4}}
    assert merge_dict(dict_in, eq_out, combine) == res
    assert dict_in == dict_orig


if __name__ == "__main__":
    test_main()
