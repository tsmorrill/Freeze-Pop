from math import floor
from typing import Callable


def float_to_CC(x: float) -> int:
    x = max(0, min(x, 127))
    return floor(x)


def quantizer(gamut: list) -> Callable:
    """Make a quantizer function."""
    min_note, max_note = min(gamut), max(gamut)

    def quantize(x):
        val = x() if callable(x) else x
        val = max(val, min_note)

        *head, _ = gamut
        _, *tail = gamut
        pairs = zip(head, tail)
        for a, b in pairs:
            if a <= val < b:
                midpoint = (a + b) / 2
                val = a + (b - a) * int(val > midpoint)
                return val

        return max_note

    return quantize


if __name__ == "__main__":
    ...
