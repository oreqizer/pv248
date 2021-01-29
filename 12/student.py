import pandas as pd

# The t-test is used, among other things, to assess whether two
# «population» means of some attribute are the same, based on a
# «sample» of each of the two populations. The test makes a few
# assumptions, the most important being:
#
#  1. the attribute is normally distributed,
#  2. the variances of the two samples are similar,
#  3. the sample sizes are equal.
#
# The assumptions are not exact: small deviations only lead to small
# inaccuracy in the result. Hence, we can set up some tolerances.
# Implement a predicate ‹t_validate› that takes 2 sets of numbers, and
# tolerance arguments as follows:
#
#  • ‹normality› is the maximum p-value that we are willing to
#    accept for a normality test on the input data (use a
#    Shapiro-Wilk test to obtain the p-value),
#  • ‹variance› is the difference of variances that we are willing
#    to tolerate, and finally
#  • ‹relsize› is the relative size difference that we are willing
#    to accept (i.e. we accept the samples if their size difference
#    divided by their size average is less than ‹relsize›).

def t_validate( s_1, s_2, normality, variance, relsize ):
    pass

# Then implement a function ‹split› that takes:
#
#  • ‹data›, a pandas data frame,
#  • ‹col›, the column to test,
#  • ‹split_col›, the column by which the data is split into two
#    disjoint sets,
#  • ‹split_val› if ‹None›, ‹split_col› must have exactly 2 values,
#    which are taken to be the sample sets to compare, otherwise
#    ‹split_val› is a number and ‹split_col› is numeric: then the
#    two sets are given by ‹data[split_col] < split_val› and
#    ‹data[split_col] >= split_val›.
#
# The result of ‹split› is two sets of numbers (in the form of
# single-column data frames).

def split( data, col, split_col, split_val = None ):
    pass

# Finally implement ‹pvalue› which takes 2 samples (sets of numbers)
# and produces a p-value indicating the likelihood that the means of
# the corresponding populations are equal.

def pvalue( s_1, s_2 ):
    pass


def test_main():
    data = pd.read_csv( 'stats.csv' )
    x, y = split( data, 'bmi', 'sex' )
    assert t_validate( x, y, 0.05, 5, .1 )
    assert 0.08 < pvalue( x, y ) < 0.1

    x, y = split( data, 'bmi', 'smoker' )
    assert not t_validate( x, y, 0.05, 5, .1 )
    assert t_validate( y, y, 0.05, 5, .1 )
    assert not t_validate( x, x, 0.05, 5, .1 )
    assert 0.99 < pvalue( y, y ) <= 1

    x, y = split( data, 'bmi', 'age', 39 )
    assert t_validate( y, y, 0.05, 5, .1 )
    assert 0 < pvalue( x, y ) < 0.001

if __name__ == '__main__':
    test_main()
