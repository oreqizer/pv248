# Write a function that removes outliers from an otherwise normally
# distributed data set, given as a list of 2-tuples (x, y). You can
# create random inputs for testing with ‹numpy.random.normal( mean,
# stddev, count )› and then add a few outliers manually.

import numpy as np

# What exactly constitutes an outlier is somewhat domain- and
# dataset-specific, but using some small integer multiple (3-5) of
# ⟦σ⟧ (the standard deviation) as the cutoff is quite common.

# You can use pandas data frames in the implementation if you like,
# or even construct them outside and pass them to the function
# directly. Remove all outliers strictly outside the range given by
# the ‹nsigmas› argument. Return the filtered list.

def drop_outliers( data, nsigmas ):
    pass

# Now that we have a function to remove outliers, let's look at what
# effect it has. The following function should call ‹f› on both the
# original data, and the outlier-culled variant. Return a 2-tuple of
# (original data, outliers removed) where each is itself a 2-tuple
# (x, y).

def cmp_outliers( data, nsigmas, f ):
    pass

# Try computing mean, median, quartiles and standard deviation of a
# few data sets with a more or less severe outlier problem. Then
# move on to ‹regress.py›.

def test_main():
    # x from np.random.normal( 10, 2, 20 )
    # y from np.random.normal( 16, 4, 20 )
    # df = list( zip( x, y ) )

    df = [ (11.54374531728097, 17.033772004561364),
           (11.290028460704368, 19.681696486385874),
           (7.1643136735932975, 10.870688470455766),
           (13.971510465448336, 25.84382951213484),
           (10.235362487870768, 13.335019695487416),
           (11.570182527561014, 25.942666592712968),
           (10.04348229223319, 16.647844406377086),
           (10.860219629924522, 16.32999469177061),
           (6.6509301946328065, 21.91010945935638),
           (7.180572899557317, 11.46870838514586),
           (11.825633778267322, 17.767212925501756),
           (9.00854587508819, 10.411313403825243),
           (11.126065121853257, 9.824750824415826),
           (11.495888803926471, 16.642366166951682),
           (7.623291697323285, 14.716767839462358),
           (9.903271374302527, 15.567414333088639),
           (9.814000405042467, 10.170996444018712),
           (6.495340904669167, 16.60891860720696),
           (9.27817477485331, 17.891234152688135),
           (11.150900697249186, 16.678742256710567) ]

    # note that values within 1 or 2 ⟦σ⟧ are not typically considered
    # outliers yet this is to ensure correct functionality of your
    # implementation
    df_out = drop_outliers( df, 1 )
    assert len( df_out ) == 10
    assert all( [ 7.8 <= x <= 12 for x,_ in df_out ] )
    assert all( [ 11.5 <= y <= 21 for _,y in df_out ] )

    df_out = drop_outliers( df, 2 )
    assert len( df_out ) == 18
    assert all( [ x <= 13.9 for x,_ in df_out ] )
    assert all( [ y <= 25.8 for _,y in df_out ] )

    # we do not have any actual outliers yet (a value further than 3
    # ⟦σ⟧ from the mean), as all values were generated from a normal
    # distribution
    df_out = drop_outliers( df, 3 )
    assert len( df_out ) == 20

    # We manually add some outliers. Notice how the mean gets skewed
    # as a result, so some values might not be considered outliers
    # anymore if extreme values are present. Here, -1 gets us over 3
    # ⟦σ⟧ and 97 even over 4 ⟦σ⟧. Value 39, however, will be treated
    # as a non-outlier. If we repeated the process, 39 would get
    # over 3 ⟦σ⟧ and would be considered an outlier. Repeated
    # removal of outliers is of course data-specific and needs to be
    # justified. In our case the problem is too few data points. You
    # can play around with outliers on both extremes of the scale,
    # and with what this means for the mean and, consequently,
    # ⟦σ⟧.

    df.append( ( -1, 17 ) )
    df.append( ( 9, 39 ) )
    df.append( ( 2, 97 ) )
    df_out = drop_outliers( df, 3 )
    assert len( df_out ) == 21
    assert len( df ) == 23

    normal, out = cmp_outliers( df, 3, np.mean )
    x,y = normal
    assert 9 <= x <= 9.1
    assert 20.7 <= y <= 20.9

    x,y = out
    assert 9.8 <= x <= 10
    assert 17.3 <= y <= 17.5

    # Let us generate a bigger dataset with the same initial properties, to make the
    # outliers more visible. Run the program multiple times and compare the output.
    # Make sure you understand what is happening.

    x_ = iter( np.random.normal( 10, 2, 100 ) )
    y_ = iter( np.random.normal( 16, 4, 100 ) )
    df = list( zip( x_, y_ ) )

    df.append( ( -1, 17 ) )
    df.append( ( 9, 39 ) )
    df.append( ( 2, 97 ) )
    df.append( ( 10, 2 ) )
    df.append( ( -3, 84 ) )
    df.append( ( 12, 76 ) )
    df.append( ( -4, 100 ) )
    df.append( ( 1, 1 ) )
    df.append( ( -10, 98 ) )

    def quart( data ):
        return np.percentile( data, [ 0.25, 0.75 ] )

    normal, out = cmp_outliers( df, 3, np.mean )
    print( 'mean (sigma 3):', normal, out )
    normal, out = cmp_outliers( df, 3, np.median )
    print( 'median:', normal, out )
    normal, out = cmp_outliers( df, 3, quart )
    print( '1st,3rd quartiles (sigma 3):', normal, out )
    normal, out = cmp_outliers( df, 2, quart )
    print( '1st,3rd quartiles (sigma 2):', normal, out )
    normal, out = cmp_outliers( df, 3, np.std )
    print( 'std dev (sigma 3):', normal, out )


if __name__ == "__main__":
    test_main()
