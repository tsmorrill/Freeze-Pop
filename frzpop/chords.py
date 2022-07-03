def make_chord(root, degree_list):
    """Return a list of all MIDI note values which belong to the given
    chord."""
    root %= 12
    degree_list = [(root + degree) % 12 for degree in degree_list]
    all_octaves = [n for n in range(128) if n % 12 in degree_list]
    return all_octaves


def major(root):
    degree_list = [0, 4, 7]
    return make_chord(root, degree_list)


def dom7(root):
    degree_list = [0, 4, 7, 10]
    return make_chord(root, degree_list)


def minor(root):
    degree_list = [0, 3, 7]
    return make_chord(root, degree_list)


if __name__ == "__main__":
    chord = minor(11)
    print(chord)
