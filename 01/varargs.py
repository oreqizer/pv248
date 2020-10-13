# Argument passing in python is rather flexible. It's possible to
# take an arbitrary number of arguments (which becomes a tuple in
# the function body), like this:

def f(*args):
    for a in args:
        print(a, end=" ")

# Side-note: we will use Python's ‹end› argument in ‹print()› to
# avoid a newline at the end (‹end› defaults to newline, so
# specifying the text we want to print as ‹end› will result in just
# the text being printed).


print(end="f( 1, 2, 3 ): ")
f(1, 2, 3)
print()

print(end="f( 7 ): ")
f(7)
print()

print(end="f(): ")
f()
print()

# This is fairly standard. However, there is another interesting
# option, and that is dynamic construction of argument lists. This
# is essentially the dual to variadic functions:


def g(a, b, c):
    print(a, c, b)


print(end="g( 1, 3, 2 ): ")
g(1, 3, 2)

x = [5, 7, 6]
print(end="g( *x ): ")
g(*x)

# Of course, it's okay if both things are used with the same
# function, too:

print(end="f( *x ): ")
f(*x)
print()
