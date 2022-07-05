def oct_scale(root, intervals):
    """Return a list of all MIDI note values which belong to the chord
    specified by root and intervals."""
    root %= 12
    chromatics = [root]
    for interval in intervals:
        chromatics.append(chromatics[-1] + interval)
    all_octaves = [n for n in range(128) if n % 12 in chromatics]
    return all_octaves


# interval between penultimate scale degree and root is not necessary, but
# included below for legibility


# diatonic modes in the usual order


def major(root):
    intervals = [2, 2, 1, 2, 2, 2, 1]
    return oct_scale(root, intervals)


def ionian(root):
    return major(root)


def dorian(root):
    intervals = [2, 1, 2, 2, 2, 1, 2]
    return oct_scale(root, intervals)


def phrygian(root):
    intervals = [1, 2, 2, 2, 1, 2, 2]
    return oct_scale(root, intervals)


def lydian(root):
    intervals = [2, 2, 2, 1, 2, 2, 1]
    return oct_scale(root, intervals)


def mixolydian(root):
    intervals = [2, 2, 1, 2, 2, 1, 2]
    return oct_scale(root, intervals)


def minor(root):
    intervals = [2, 1, 2, 2, 1, 2, 2]
    return oct_scale(root, intervals)


def aeolian(root):
    return minor(root)


def locrian(root):
    intervals = [1, 2, 2, 1, 2, 2, 2]
    return oct_scale(root, intervals)


# other scales


def blues(root):
    intervals = [3, 2, 1, 1, 3, 2]
    return oct_scale(root, intervals)


def messiaen(root, mode):
    """Generate one of Messiaen's modes of limited transposition."""
    modes = [[2, 2, 2, 2, 2, 2],
             [1, 2, 1, 2, 1, 2, 1, 2],
             [2, 1, 1, 2, 1, 1, 2, 1, 1],
             [1, 1, 3, 1, 1, 1, 3, 1],
             [1, 4, 1, 1, 4, 1],
             [2, 2, 1, 1, 2, 2, 1, 1],
             [1, 1, 1, 2, 1, 1, 1, 1, 2, 1]]
    intervals = modes[mode - 1]
    return oct_scale(root, intervals)


if __name__ == "__main__":
    C = major(60)
    for i in range(0, len(C), 7):
        print(C[i:i+8])
