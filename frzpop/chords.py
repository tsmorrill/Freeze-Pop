def chord(root, intervals):
    """Return a list of all MIDI note values which belong to the chord
    specified by root and intervals."""
    root %= 12
    chromatics = [root]
    for interval in intervals:
        chromatics.append(chromatics[-1] + interval)
    all_octaves = [n for n in range(128) if n % 12 in chromatics]
    return all_octaves


def major(root):
    intervals = [0, 4, 3]
    return chord(root,  intervals)


def minor(root):
    intervals = [0, 3, 4]
    return chord(root,  intervals)


def dim(root):
    intervals = [0, 3, 3]
    return chord(root,  intervals)


def aug(root):
    intervals = [0, 5, 2]
    return chord(root, intervals)


def maj7(root):
    intervals = [0, 4, 3, 4]
    return chord(root,  intervals)


def dom7(root):
    intervals = [0, 4, 3, 3]
    return chord(root,  intervals)


def min7(root):
    intervals = [0, 3, 4, 3]
    return chord(root,  intervals)


if __name__ == "__main__":
    c7 = min7(60)
    for i in range(0, len(c7), 4):
        print(c7[i:i+4])
