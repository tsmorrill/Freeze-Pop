from frzpop import additives

gamut = additives.gamut


# interval between penultimate scale degree and root is not necessary using
# gamut, but included below for legibility


# diatonic modes in the usual order


def major(root: int) -> list:
    intervals = [2, 2, 1, 2, 2, 2, 1]
    return gamut(root, intervals)


def ionian(root: int) -> list:
    return major(root)


def dorian(root: int) -> list:
    intervals = [2, 1, 2, 2, 2, 1, 2]
    return gamut(root, intervals)


def phrygian(root: int) -> list:
    intervals = [1, 2, 2, 2, 1, 2, 2]
    return gamut(root, intervals)


def lydian(root: int) -> list:
    intervals = [2, 2, 2, 1, 2, 2, 1]
    return gamut(root, intervals)


def mixolydian(root: int) -> list:
    intervals = [2, 2, 1, 2, 2, 1, 2]
    return gamut(root, intervals)


def minor(root: int) -> list:
    intervals = [2, 1, 2, 2, 1, 2, 2]
    return gamut(root, intervals)


def aeolian(root: int) -> list:
    return minor(root)


def locrian(root: int) -> list:
    intervals = [1, 2, 2, 1, 2, 2, 2]
    return gamut(root, intervals)


# other scales


def blues(root: int) -> list:
    intervals = [3, 2, 1, 1, 3, 2]
    return gamut(root, intervals)


def messiaen(root: int, mode: int) -> list:
    """Generate one of Messiaen's modes of limited transposition."""
    modes = [
        [2, 2, 2, 2, 2, 2],
        [1, 2, 1, 2, 1, 2, 1, 2],
        [2, 1, 1, 2, 1, 1, 2, 1, 1],
        [1, 1, 3, 1, 1, 1, 3, 1],
        [1, 4, 1, 1, 4, 1],
        [2, 2, 1, 1, 2, 2, 1, 1],
        [1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    ]
    intervals = modes[mode - 1]
    return gamut(root, intervals)


if __name__ == "__main__":
    C = major(60)
    for i in range(0, len(C), 7):
        print(C[i : i + 8])
