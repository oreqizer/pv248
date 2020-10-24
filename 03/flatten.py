# In this exercise, your task is to write a function that flattens
# json data. Flattening works as follows:
# 
# The result is a single-level (flat) json with key-value pairs, the
# keys representing the former structure of data. We could use any
# (unique) separator to indicate the nested structure, which would
# allow unflattening without loss of information.  We will use the
# dollar sign '$'. If you do encounter '$' in the original data,
# replace it with two dollars '$$'.  Assume that there are no keys
# composed entirely of numbers.
#
# Example:
#     { 'student': { 'Joe': { 'full name': 'Joe Peppy',
#                             'address': 'Clinical Street 7',
#                             'aliases': ['Joey', 'MataMata'] } } }
#
# Flattened:
#     { 'student$Joe$full name': 'Joe Peppy',
#       'student$Joe$address': 'Clinical Street 7',
#       'student$Joe$aliases$0': 'Joey',
#       'student$Joe$aliases$1': 'MataMata' }
#
# The simplest way to go about it is to use recursion.

def flatten( data ):
    pass

# ----%<----

def test_main():
    js =  { 'student': { 'Joe': { 'full name': 'Joe Peppy',
                                  'address': 'Clinical Street 7',
                                  'aliases': ['Joey', 'MataMata'] } } }
    flat_js = { 'student$Joe$full name': 'Joe Peppy', 'student$Joe$address': 'Clinical Street 7',
                'student$Joe$aliases$0': 'Joey', 'student$Joe$aliases$1': 'MataMata' }

    assert flatten( js ) == flat_js


    js = { 'product': [ { 'id': [ 2327, 7824 ],
                          'info': { 'description': 'lcd monitor',
                                    'price in $': 22 } },
                        { 'id': [ 33 ],
                          'info': { 'description': 'mouse',
                                    'price in $': 4 } } ] }
    flat_js = { 'product$1$info$description': 'mouse', 'product$0$info$price in $$': 22,
                'product$0$id$1': 7824, 'product$0$info$description': 'lcd monitor',
                'product$0$id$0': 2327, 'product$1$info$price in $$': 4,
                'product$1$id$0': 33 }

    assert flatten( js ) == flat_js


if __name__ == "__main__":
    test_main()


# Bonus: If you are bored, you can write the reverse function,
# to unflatten the data back.
