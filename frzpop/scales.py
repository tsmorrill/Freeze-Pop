notes = {"C":   0,
         "Cs":  1, "Db":  1,
         "D":   2,
         "Ds":  3, "Eb":  3,
         "E":   4,
         "F":   5,
         "Fs":  6, "Gb":  6,
         "G":   7,
         "Gs":  8, "Ab":  8,
         "A":   9,
         "As": 10, "Bb": 10,
         "B":  11}

intervals = {"major":      [0, 2, 4, 5, 7, 9, 11],
             "ionian":     [0, 2, 4, 5, 7, 9, 11],
             "dorian":     [0, 2, 3, 5, 7, 9, 10],
             "phrygian":   [0, 1, 3, 5, 7, 8, 10],
             "lydian":     [0, 2, 4, 6, 7, 9, 11],
             "mixolydian": [0, 2, 4, 5, 7, 9, 10],
             "aeolian":    [0, 2, 3, 5, 7, 8, 10],
             "minor":      [0, 2, 3, 5, 7, 8, 10],
             "locrian":    [0, 1, 3, 5, 6, 8, 10]}


def make_oct_scale(root, type):
    root %= 12
    degrees = intervals[type]
    degrees = [(root + degree) % 12 for degree in degrees]
    all_octaves = [n for n in range(128) if n % 12 in degrees]
    return all_octaves


def major(root):
    return make_oct_scale(root, "major")


def ionian(root):
    return major(root)


def dorian(root):
    return make_oct_scale(root, "dorian")


def phrygian(root):
    return make_oct_scale(root, "phrygian")


def lydian(root):
    return make_oct_scale(root, "lydian")


def mixolydian(root):
    return make_oct_scale(root, "mixolydian")


def minor(root):
    return make_oct_scale(root, "minor")


def aeolian(root):
    return minor(root)


def locrian(root):
    return make_oct_scale(root, "locrian")


if __name__ == "__main__":
    scale = minor(11)
    for i in range(0, len(scale), 7):
        print(scale[i:i+8])
