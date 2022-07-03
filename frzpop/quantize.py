from math import floor


def p_gen(gen):
    """Wrap a parameterized generator in a function call."""

    def wrapper(*args, **kwargs):
        generator = gen(*args, **kwargs)

        def func(*args):
            return next(generator)
        return(func)
    return wrapper


def float_to_CC(x):
    x = max(0, min(x, 127))
    return floor(x)


def quantizer(notes):
    """Make a quantizer function."""
    notes.sort()
    min_note, max_note = min(notes), max(notes)

    def quantize(x):
        if callable(x):
            val = x()
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

    return quantize


if __name__ == "__main__":
    @p_gen
    def spam(*args):
        x = 55
        while True:
            yield x
            x += 1.1

    chord = [60, 64, 67]
    Cmaj = quantizer(chord)

    eggs = spam()

    notes = [Cmaj(eggs) for _ in range(16)]
    print(notes)
