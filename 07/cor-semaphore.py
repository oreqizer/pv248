# Use ‹gather()› to spawn 10 tasks, each running an infinite loop.
# Create a global semaphore that is shared by all those tasks and
# set its initial value to 3. In each iteration, each task should
# queue on the semaphore and when it is allowed to proceed, sleep 2
# seconds before calling ‹notify›, and relinquishing the semaphore
# again.

# ‹notify› adds a tuple -- containing the task id ( 1 - 10 ) and the
# time when the task reached the semaphore -- to the global list
# ‹reached›.

# Observe the behaviour of the program. Add a short sleep «outside»
# of the critical section of the task. Compare the difference in
# behaviour.

# After your program works as expected, i.e. only 3 tasks are active
# at any given moment and the tasks alternate fairly, switch the
# infinite loop for a bounded loop: each task running twice, to be
# consistent with the tests.

# NOTE: Most asyncio objects, semaphores included, are tied to an
# event loop.  You need to create the semaphore from within the same
# event loop in which your tasks will run. (Alternatively, you can
# create the loop explicitly and pass it to the semaphore.)

import asyncio
import time

reached = []
begin = time.time()


def notify(i):
    t = time.time() - begin
    print("task {} reached semaphore at {}".format(i, t))
    reached.append((i, t))


class Semaphore:
    def __init__(self):
        self.i = 3
        self.tasks = set()

    async def go(self, task):
        if task in self.tasks:
            if len(self.tasks) == 10:
                self.tasks = set()
            return
        self.i -= 1
        await asyncio.sleep(2)
        notify(task)
        self.i += 1
        self.tasks.add(task)


async def task(sem, n):
    ran = 0
    while ran < 2:
        if sem.i > 0:
            await sem.go(n)
            ran += 1
        else:
            await asyncio.sleep(0.05)


async def main():
    sem = Semaphore()
    await asyncio.gather(
        task(sem, 1),
        task(sem, 2),
        task(sem, 3),
        task(sem, 4),
        task(sem, 5),
        task(sem, 6),
        task(sem, 7),
        task(sem, 8),
        task(sem, 9),
        task(sem, 10),
    )


asyncio.run(main())


def test_main():
    asyncio.run(main())
    for i in [1, 2, 3]:
        assert i in [t[0] for t in reached[0:3]]
    for i in [4, 5, 6]:
        assert i in [t[0] for t in reached[3:6]]

    for i in range(1, 11):
        assert i in [t[0] for t in reached]
    assert len(reached) == 20

    # time difference at least 2 seconds from last 3-batch
    for i in range(3, len(reached)):
        assert reached[i][1] - reached[i - 3][1] > 2


if __name__ == "__main__":
    test_main()

# Proceed to ‹aio-process.py›.
