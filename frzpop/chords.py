from additives import gamut


def major(root):
    intervals = [0, 4, 3]
    return gamut(root,  intervals)


def minor(root):
    intervals = [0, 3, 4]
    return gamut(root,  intervals)


def dim(root):
    intervals = [0, 3, 3]
    return gamut(root,  intervals)


def aug(root):
    intervals = [0, 5, 2]
    return gamut(root, intervals)


def maj7(root):
    intervals = [0, 4, 3, 4]
    return gamut(root,  intervals)


def dom7(root):
    intervals = [0, 4, 3, 3]
    return gamut(root,  intervals)


def min7(root):
    intervals = [0, 3, 4, 3]
    return gamut(root,  intervals)


if __name__ == "__main__":
    c7 = min7(60)
    for i in range(0, len(c7), 4):
        print(c7[i:i+4])
