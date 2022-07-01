from math import floor


def float_to_CC(x):
    x = max(0, min(x, 127))
    return floor(x)


def make_quantizer(note_list):
    """Return a quantizer function."""
    note_list.sort()
    min_note, max_note = min(note_list), max(note_list)

    def quantizer(x):
        x = max(x, min_note)

        pairs = zip(note_list[:-1], note_list[1:])
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
