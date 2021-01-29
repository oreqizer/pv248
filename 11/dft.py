# Write a function which reconstructs the frequencies which were
# given to ‹freq› in ‹sig.py›, as an ascending list of integers.

# Note that the FFT algorithm used in NumPy will give you non-zero
# amplitudes for every frequency – use ‹isclose› to check if the
# amplitude is almost zero.

# You can assume that the input only contains integer frequencies.
# When testing, be careful to avoid aliasing (i.e. make sure the
# highest frequency passed to ‹freq› from ‹sig.py› is less than half
# the number of samples).

def dft( amp ):
    pass

def test_main():
    sig_1 = [ 0, 1, 0, -1, 0, 1, 0, -1 ]
    assert dft( sig_1 ) == [ 2 ]

    sig_2 = [ 0.00000000e+00,  1.63098631e+00,
              1.70710678e+00,  3.24423349e-01,
             -1.00000000e+00, -1.08979021e+00,
             -2.92893219e-01,  2.16772751e-01,
              0.00000000e+00, -2.16772751e-01,
              2.92893219e-01,  1.08979021e+00,
              1.00000000e+00, -3.24423349e-01,
             -1.70710678e+00, -1.63098631e+00 ]

    assert dft( sig_2 ) == [ 2, 3 ]

    sig_3 = [ 0.00000000e+00,  3.39635318e+00,
              1.70710678e+00,  1.17218241e+00,
             -1.00000000e+00,  1.75796885e+00,
             -2.92893219e-01, -1.78603839e-02,
              6.12323400e-16,  1.78603839e-02,
              2.92893219e-01, -1.75796885e+00,
              1.00000000e+00, -1.17218241e+00,
             -1.70710678e+00, -3.39635318e+00 ]

    assert dft( sig_3 ) == [ 1, 2, 3, 4, 7 ]
