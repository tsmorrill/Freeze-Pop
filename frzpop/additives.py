from random import Random
from typing import Callable, Generator


def sip_water():
    """Check that import is working"""
    print("Sipped a glass of water. Refreshing!")


def base_2(*args) -> int:
    sum = 0
    power = 0
    for bit in args[::-1]:
        sum += bit * 2**power
        power += 1
    return sum


def try_calling(x):
    if callable(x):
        output = x()
    else:
        output = x
    return output


def gamut(root: int, intervals: list) -> list:
    """Return a list of all MIDI note values which belong to the chord
    specified by root and intervals."""
    root %= 12
    chromatics = [root]
    note = root
    for interval in intervals:
        note += interval
        note %= 12
        chromatics.append(note)
    all_octaves = [n for n in range(128) if n % 12 in chromatics]
    return all_octaves


def pairs_of(list: list) -> list:
    *head, _ = list
    _, *tail = list
    return zip(head, tail)


def state_machine(machine: Callable):
    """Wrap a parameterized generator in a function call."""

    def wrapper(*args, **kwargs):
        instance = machine(*args, **kwargs)

        def func():
            return next(instance)

        return func

    return wrapper


# simple state machines


@state_machine
def bogo(init: list, seed=None) -> Generator:
    """Generate a random permutation of list."""
    permutation = init.copy()

    rng = Random(seed)
    while True:
        yield permutation
        rng.shuffle(permutation)


@state_machine
def choose_from(choices: list, seed=None) -> Generator:
    if not choices:
        raise ValueError("choices must be a non-empty list.")
    rng = Random(seed)

    while True:
        yield rng.choice(choices)


@state_machine
def next_up(queue: list) -> Generator:
    if not queue:
        raise ValueError("queue must be a non-empty list.")
    length = len(queue)
    i = 0
    while True:
        yield queue[i]
        i += 1
        i %= length


@state_machine
def rng(seed=None) -> Generator:
    rng = Random(seed)

    while True:
        yield rng.random()


if __name__ == "__main__":
    names = [name for name in dir() if not name.startswith("_")]
    imports: list = ["Callable", "Generator"]
    for name in imports:
        names.remove(name)
    print("Things to test:")
    print(", ".join(names))
    print()
    print(base_2(1, 1, 1, 0))
