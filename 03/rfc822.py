# In this exercise, we will parse a format that is based on rfc 822
# headers, though our implementation will only handle the simplest
# cases. The format looks like this:

# From: Petr Ročkai <xrockai@fi.muni.cz>
# To: Random X. Student <xstudent@fi.muni.cz>
# Subject: PV248

# and so on and so forth (for your convenience, the above example
# can be also found in the file `rfc822.txt`). In real e-mail (and
# in HTTP), each header entry may span multiple lines, but we will
# not deal with that.

# Our goal is to create a ‹dict› where the keys are the individual
# header fields and the corresponding values are the strings coming
# after the colon. In this iteration, assume that each header is
# unique.

def parse_rfc822( filename ):
    pass

# When done, go on to ‹multi822.py›.

# ----%<----

def test_main():

    res = parse_rfc822( "rfc822.txt" )
    assert len( res ) == 3
    for k in [ "From", "To", "Subject" ]:
        assert k in res

    assert res[ "From" ] == "Petr Ročkai <xrockai@fi.muni.cz>"
    assert res[ "To" ] == "Random X. Student <xstudent@fi.muni.cz>"
    assert res[ "Subject" ] == "PV248"

if __name__ == "__main__":
    test_main()

