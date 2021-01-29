# Grab the data from the given ‹filename› and compute the average,
# median, first and last quartile and variance of each numeric
# column. Put the data into a dictionary with sub-dictionaries as
# values, e.g.
#
#     {
#         'average': { 'age': 39.207, 'bmi': 30.663, … },
#         'variance': …,
#         'first quartile': { 'age': 27, … },
#         'last quartile': { 'age': 51, … },
#         …
#     }

def stats( filename ):
    pass

def test_main():
    d = stats( 'stats.csv' )
    assert 39.207 < d[ 'average' ][ 'age' ] < 39.208
    assert 37.187 < d[ 'variance' ][ 'bmi' ] < 37.188
    assert d[ 'first quartile' ][ 'children' ] == 0
    assert d[ 'last quartile' ][ 'children' ] == 2
    assert d[ 'median' ][ 'age' ] == 39
    assert d[ 'median' ][ 'bmi' ] == 30.4

if __name__ == '__main__':
    test_main()
