# Write a function that generates 1 second of signal as a sequence
# of amplitude samples, built from a given mix of sinus frequencies.
# The result should contain ‹count› samples, including the initial
# state at t = 0. 1 second is the time of 1 full cycle of a sine
# wave with frequency 1.

# Then write a function ‹logscale›, which takes a histogram
# represented as a list (a sorted list of values) and converts its x
# axis to logscale. That is: the first item is discarded, the second
# item becomes first, the average of 3rd and 4th item comes second,
# the average of 5th through 8th items comes third, and so on.

# Cf. np.ceil( np.log2( range( 1, 32 ) ) )

# Next stop is ‹dft.py›.

import numpy as np

def freq( count, freqs ):
    pass

def logscale( data ):
    pass


def test_main():

    # 8 samples, a single sine wave with freq. 2
    f1 = freq( 8, [ 2 ] )
    f1_res = [ 0, 1, 0, -1, 0, 1, 0, -1 ]

    assert len( f1 ) == 8
    assert all( np.isclose( f1, f1_res ) )

    f2 = freq( 10, [ 0.5, 2, 1, 3, 9 ] )
    f2_res = [ 0, 2.2111300269652543, 0.5877852522924732, -0.3665535102099986,
               0.9510565162951541, 1, 0.9510565162951549, 1.9845874989598953,
               0.5877852522924734, -1.593096038215359 ]

    assert len( f2 ) == 10
    assert all( np.isclose( f2, f2_res ) )

    lg1 = logscale( [ 0, 1, 2, 2, 3, 3, 3, 3 ] )
    lg1_res = [ 1, 2, 3 ]

    assert len( lg1 ) == 3
    assert all( np.isclose( lg1, lg1_res ) )

    lg2 = logscale( [ 0, 9, 9, 13, 14, 14, 14, 14, 16, 16, 17, 19, 20, 22,
                      25, 25, 25, 26, 26, 27, 27, 29, 29, 29, 29, 29, 29, 33 ] )
    lg2_res = [ 9.0, 11.0, 14.0, 20.0, 28.166666666666668 ]

    assert len( lg2 ) == 5
    assert all( np.isclose( lg2, lg2_res ) )

if __name__ == "__main__":
    test_main()
