intervals = {"major": [0, 4, 7],
             "minor": [0, 3, 7]}


def make_chord(root, type):
    root %= 12
    degrees = intervals[type]
    degrees = [(root + degree) % 12 for degree in degrees]
    all_octaves = [n for n in range(128) if n % 12 in degrees]
    return all_octaves


def major(root):
    return make_chord(root, "major")


def minor(root):
    return make_chord(root, "minor")


if __name__ == "__main__":
    chord = minor(11)
    for i in range(0, len(chord), 3):
        print(chord[i:i+3])
