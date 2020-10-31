# Building on the previous exercise, extend the parser in the
# following way: if the given field is unique, keep its associated
# value as a string. However, if a certain field appears multiple
# times, turn the value into a list. The right-hand-side strings
# should be listed in the order of appearance.

def parse_multirfc822( filename ):
    pass


# ----%<----

def test_main():

    res = parse_multirfc822( "multi822.txt" )
    assert len( res ) == 4
    for k in [ "From", "To", "Subject", "Cc" ]:
        assert k in res

    assert res[ "From" ] == "Petr Ročkai <xrockai@fi.muni.cz>"
    assert res[ "To" ] == [ "Random X. Student <xstudent@fi.muni.cz>",
                            "Random Y. <y@fi.muni.cz>",
                            "Random Z. <z@fi.muni.cz>" ]
    assert res[ "Cc" ] == [ "Non-Random Z. Student <nz@fi.muni.cz>",
                            "Non-Random W. Teacher <w@fi.muni.cz>" ]
    assert res[ "Subject" ] == "PV248"

if __name__ == "__main__":
    test_main()

# That is all for text processing. We will now look at some JSON:
# start with ‹report.py›.
