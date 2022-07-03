from math import floor


def float_to_CC(x):
    x = max(0, min(x, 127))
    return floor(x)


def make_quantizer(notes):
    """Return a quantizer function."""
    notes.sort()
    min_note, max_note = min(notes), max(notes)

    def quantizer(x):
        x = max(x, min_note)

        *head, _ = notes
        _, *tail = notes
        pairs = zip(head, tail)
        for a, b in pairs:
            if a <= x < b:
                midpoint = (a + b)/2
                x = a + (b - a)*int(x > midpoint)
                return x

        return max_note
    return quantizer


if __name__ == "__main__":
    chord = [60, 64, 67]
    quantizer = make_quantizer(chord)
    for x in range(59, 69):
        x += 0.1
        print(x, quantizer(x))
