from math import floor


def float_to_CC(x):
    x = max(0, min(x, 127))
    return floor(x)


def quantizer(notes):
    """Make a quantizer function."""
    notes.sort()
    min_note, max_note = min(notes), max(notes)

    def func(x):
        if callable(x):
            val = next(x())
        else:
            val = x

        val = max(val, min_note)

        *head, _ = notes
        _, *tail = notes
        pairs = zip(head, tail)
        for a, b in pairs:
            if a <= val < b:
                midpoint = (a + b)/2
                val = a + (b - a)*int(val > midpoint)
                return val

        return max_note
    return func


if __name__ == "__main__":
    def foo(*args):
        x = 40
        while True:
            yield x
            x *= 2
    print(type(foo))
    print(foo)
    print(foo())
    chord = [60, 64, 67]
    Cmaj = quantizer(chord)
    for _ in range(8):
        print(Cmaj(foo))
