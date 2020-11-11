# Write a decorator @noexcept(), which turns a function which might throw an
# exception into one that will instead return ‹None›. If used with arguments,
# those arguments indicate which exception types should be suppressed.

def noexcept( *ignore ):
    def decorate( f ):
        return f
    return decorate


def test_main():

    @noexcept( TypeError, AssertionError )
    def foo():
        assert 1 == 2

    @noexcept()
    def bar():
        assert 2 == 3

    assert foo() == None
    assert bar() == None

    @noexcept( TypeError )
    def baz():
        raise AssertionError

    try:
        baz()
        assert False
    except AssertionError:
        pass

    @noexcept( TypeError, AssertionError, RuntimeError )
    def bazz( a1, a2, a3 ):
        assert 1 == 1
        return a1 + a2 + 7 + a3

    assert bazz( 3, -4, a3 = -1 ) == 5

if __name__ == "__main__":
    test_main()

