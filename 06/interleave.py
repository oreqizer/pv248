# Write two generators, one which simply yields numbers 1-5 and another which
# implements a counter: sending a number to the generator will adjust its value
# by the amount sent. Then write a driver loop that sends the output of gen1()
# into gen2(). Add print statements to both to make it clear in which order the
# code executes.

# After you are done, implement the same thing with plain objects: Numbers with
# a get() method and Counter with a `get()` and `put(n)`.

def numbers():  # generate numbers 1-5
    for i in range(0, 5):
        yield i+1


def counter():
    i = 1
    for _ in range(0, 5):
        i += yield i
    yield i

# Write one more generator, the driver loop.


def driver():
    num = numbers()
    cnt = counter()

    yield next(cnt)
    for i in num:
        yield cnt.send(i)

class Numbers:
    pass


class Counter:
    pass

# The driver loop again, now with objects.


def driver_obj():
    pass


def test_main():

    for dr in [driver, driver_obj]:
        nums = iter([1, 2, 4, 7, 11, 16])
        d = dr()
        for n in d:
            num = next(nums)
            assert n == num, "{} != {} in {}".format(n, num, d.__name__)
        # check we exhausted nums
        try:
            next(nums)
            assert False
        except StopIteration:
            pass


if __name__ == "__main__":
    test_main()
