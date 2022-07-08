from frzpop import additives

gamut = additives.gamut


def major(root: int) -> list:
    intervals = [0, 4, 3]
    return gamut(root, intervals)


def minor(root: int) -> list:
    intervals = [0, 3, 4]
    return gamut(root, intervals)


def dim(root: int) -> list:
    intervals = [0, 3, 3]
    return gamut(root, intervals)


def aug(root: int) -> list:
    intervals = [0, 5, 2]
    return gamut(root, intervals)


def maj7(root: int) -> list:
    intervals = [0, 4, 3, 4]
    return gamut(root, intervals)


def dom7(root: int) -> list:
    intervals = [0, 4, 3, 3]
    return gamut(root, intervals)


def min7(root: int) -> list:
    intervals = [0, 3, 4, 3]
    return gamut(root, intervals)


if __name__ == "__main__":
    c7 = min7(60)
    for i in range(0, len(c7), 4):
        print(c7[i: i + 4])
