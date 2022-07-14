from random import Random
from typing import Callable, Generator


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


def sip_water():
    """Check that import is working"""
    print("Sipped a glass of water. Refreshing!")


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
    print(gamut(69, [2, 2, 1, 2, 2, 2, 1]))
