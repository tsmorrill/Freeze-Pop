def oct_scale(root, intervals):
    """Return a list of all MIDI note values which belong to the given
    octave scale."""
    root %= 12
    chromatics = [root]
    for interval in intervals:
        chromatics.append(chromatics[-1] + interval)
    all_octaves = [n for n in range(128) if n % 12 in chromatics]
    return all_octaves


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


if __name__ == "__main__":
    scale = major(60)
    for i in range(0, len(scale), 7):
        print(scale[i:i+8])
