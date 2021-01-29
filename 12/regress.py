# This is the final exercise for today. In this case, the input data
# will again be (x, y) tuples, but distributed around a straight
# line and we will compute linear regression on the data. This time,
# we will remove outliers iteratively: find the term with the
# greatest squared residual and if the squared residual is larger
# than ‹cutoff›-times the sum of all squared residuals, drop the
# data point and restart the regression. Stop when there are no more
# outliers.

# Feel free to use pandas and/or numpy.

def drop_outliers( data, cutoff ): # feel free to add arguments if you like
    pass # return filtered data

def regress( data, cutoff ):
    pass # remove outliers iteratively
         # return the slope and the intercept of the regression line

# NOTE: In both the previous and in this exercise, we have taken a
# rather cavalier approach to outlier removal. For real statistics
# on real data, you often need to be much more careful and take the
# origin of the data set into account. Always disclose any outliers
# you have removed from further consideration.

import numpy as np
# import matplotlib.pyplot as plt

def test_main():

    rng = np.random.default_rng( 1337 )
    x = np.linspace( 0, 100, 50 ) # generate 50 values between 0 and 100
    np.random.seed( 56 )
    delta = rng.normal( 0, 15, x.size )
    y = -2 * x - 1 + delta

    # add noise
    for _ in range( 4 ):
        x = np.append( x, rng.uniform( 0, 100.0 ) )
        y = np.append( y, rng.uniform( -200, 200.0 ) )

    # you can use the following to plot the data if you like
    # plt.plot( x, y, 'bo' )
    # plt.savefig( "regress.png" )

    data = list( zip( x, y ) )
    a, b = regress( data, 1/3 )
    assert -1.87 < a < -1.85
    assert -10 < b < -8
    a, b = regress( data, 1/4 )
    assert -2.06 < a < -2.05
    assert  2.41 < b < 2.42

if __name__ == "__main__":
    test_main()
