# Write a function that takes a list of numbers and draws an ASCII
# histogram.  Normalize the height to 25 characters. You can compare
# your output with example output which uses the ‹*› character to
# represent value frequency.

def histogram( bins ):
    pass

# Let's move on to ‹sig.py›.

def test_main():

    h1 = histogram( [2,2,5,6,8,9,2,1,6,3,5,2] + [4]*12 )

    print( "\nreference:" )

    h1_out = '''
    *     
    *     
    *     
    *     
    *     
    *     
    *     
    *     
    *     
    *     
    *     
    *     
    *     
    *     
    *     
    *     
    *     
  * *     
  * *     
  * *     
  * *     
  * ***   
  * ***   
 ****** **
 ****** **
    '''

    print( h1_out )

    h2 = histogram( [5,19,3,19] + [13]*7 + [11]*3 + [19]*27 + [5,11,19,3,19,3,4,4,3] )


    h2_out = '''
                   *
                   *
                   *
                   *
                   *
                   *
                   *
                   *
                   *
                   *
                   *
                   *
                   *
                   *
                   *
                   *
                   *
                   *
                   *
             *     *
             *     *
             *     *
   *       * *     *
   ***     * *     *
   ***     * *     *
    '''

    print( "\nreference:" )
    print( h2_out )


if __name__ == "__main__":
    test_main()
