# You are given a graph, in the form of a dictionary, where keys are
# numbers and values are lists of numbers (i.e. it is an oriented
# graph and its vertices are numbered; however, note that the
# numbering does «not» need to be consecutive, or only use small
# numbers).

# Write a function, ‹has_cycle› which decides whether a cycle with
# at least one even-numbered vertex is reachable from vertex 1.

# Hint: look up Nested DFS. Essentially, run DFS from vertex 1 and
# when you backtrack through an even-numbered vertex (i.e. in DFS
# postorder), run another DFS from that vertex to detect any cycles
# that reach the (even-numbered) initial vertex of the inner DFS.
# All the inner searches should share the ‘visited’ marks. Be
# careful to implement the DFS correctly.

def has_cycle( graph ):
    pass

def test_main():

    g = { 1: [3],
          3: [5, 2],
          2: [0],
          0: [5],
          5: [1] }
    assert has_cycle( g )

    g = { 1: [3],
          3: [5, 2],
          5: [1],
          2: [] }
    assert not has_cycle( g )

    g = { 1: [3],
          3: [7],
          7: [2,3,0],
          0: [3],
          2: [7] }
    assert has_cycle( g )

    g = { 1: [3],
          3: [7],
          7: [2,3,0],
          0: [3],
          2: [] }
    assert has_cycle( g )

    g = { 1: [3],
          3: [7],
          7: [2,3,13],
          13: [3],
          2: [] }
    assert not has_cycle( g )

    g = { 1: [3,5],
          3: [1,5],
          71: [5,0],
          5: [1,3,71],
          0: [] }
    assert not has_cycle( g )

    g = { 1: [3,5],
          3: [1,5],
          71: [5,0],
          5: [71],
          0: [5] }
    assert has_cycle( g )

    g = { 1: [3,5],
          3: [1,5],
          71: [5,0],
          5: [],
          0: [5,2],
          2: [0] }
    assert not has_cycle( g )

    g = { 1: [2,30],
          2: [5, 41],
          30: [69,5],
          41: [2, 74],
          69: [30,74],
          74: [5],
          5: [74] }
    assert has_cycle( g )

    g = { 1: [2,4],
          2: [],
          4: [] }
    assert not has_cycle( g )

    g = { 1: [2,4],
          2: [3,5],
          4: [5,7],
          3: [3,5],
          5: [5],
          7: [7,5] }
    assert not has_cycle( g )

    g = { 1: [3],
          3: [5],
          5: [4],
          4: [7],
          7: [3] }
    assert has_cycle( g )

    g = { 1: [3],
          3: [6],
          6: [5],
          5: [7],
          7: [3] }
    assert has_cycle( g )

    g = { 1: [3],
          3: [9],
          9: [5],
          5: [4],
          4: [3] }
    assert has_cycle( g )

if __name__ == "__main__":
    test_main()

