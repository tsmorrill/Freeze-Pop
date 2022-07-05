from random import Random


def water():
    print("Refreshing!")


def state_machine(gen):
    """Wrap a parameterized generator in a function call."""

    def wrapper(*args, **kwargs):
        generator = gen(*args, **kwargs)

        def func(*args):
            return next(generator)
        return(func)
    return wrapper


@state_machine
def rng(seed=None):
    rng = Random(seed)

    while True:
        yield rng.random()


if __name__ == "__main__":
    rng1 = rng(1019)
    rng2 = rng(1019)

    print(rng1(), rng1(), rng1(), rng1())
    print(rng2(), rng2(), rng2(), rng2())
