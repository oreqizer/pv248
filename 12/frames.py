import pandas as pd
import math

# The data for this exercise is in ‹frames.csv›. The data represents
# grading of this very subject (with made-up names and numbers, of
# course). The columns are names, number of points from weekly
# exercises, from assignments and from reviews. Implement the
# following functions:

# Return a DataFrame which only contains rows of students, which
# achieved the best result among their peers in one of the
# categories (weekly, assignments, reviews). If there are multiple
# such students for a given category, include all of them.
def best( data ):
    pass

# Return a DataFrame which contains the name and the total score (as
# the only 2 columns). Don't forget that the weekly exercises
# contribute at most 9 points to the total.
def compute_total( data ):
    pass

# Return a dictionary with 4 keys ('weekly', 'assignments', 'reviews'
# and 'total') where each value is the average number of points in
# the given category. Consider factoring out a helper function from
# compute_total to get a DataFrame with 5 columns.
def compute_averages( data ):
    pass

# Test utilities and tests follow.

def eq( data, student, col, val ):
    matches = data[ data[ 'student' ] == student ][ col ]
    return ( matches == val ).all()

def test_main():
    df = pd.read_csv( 'frames.csv' )
    assert len( best( df ) ) == 5

    tot = compute_total( df )
    assert eq( tot, 'Věra Hrbáčková', 'total', 18 )
    assert eq( tot, 'Blanka Pichrtová', 'total', 17.4 )

    avg = compute_averages( df )
    assert math.isclose( avg['weekly'], 61/9 )
    assert math.isclose( avg['assignments'], 245/36 )
    assert math.isclose( avg['reviews'], 87/90 )

if __name__ == '__main__':
    test_main()
