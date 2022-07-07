from random import Random


def gamut(root: int, intervals: list) -> list:
    """Return a list of all MIDI note values which belong to the chord
    specified by root and intervals."""
    root %= 12
    chromatics = [root]
    for interval in intervals:
        chromatics.append(chromatics[-1] + interval)
    all_octaves = [n for n in range(128) if n % 12 in chromatics]
    return all_octaves


def sip_water():
    """Check that import is working"""
    print("Sipped a glass of water. Refreshing!")


def state_machine(gen):
    """Wrap a parameterized generator in a function call."""

    def wrapper(*args, **kwargs):
        generator = gen(*args, **kwargs)

        def func():
            return next(generator)

        return(func)
    return wrapper


# simple state machines


@state_machine
def bogo(init: list, seed=None) -> list:
    """Generate a random permutation of list."""
    permutation = init.copy()

    rng = Random(seed)
    while True:
        yield permutation
        rng.shuffle(permutation)


@state_machine
def list_reader(list):
    if list:
        length = len(list)
        i = 0
        while True:
            yield list[i]
            i += 1
            i %= length
    yield 0


@state_machine
def rng(seed=None):
    rng = Random(seed)

    while True:
        yield rng.random()


if __name__ == "__main__":
    names = [name for name in dir() if not name.startswith("_")]
    imports = ['Random']
    for name in imports:
        names.remove(name)
    print(", ".join(names))

    test = list(range(5))
    machine = bogo(test)
    for _ in range(5):
        print(machine())
