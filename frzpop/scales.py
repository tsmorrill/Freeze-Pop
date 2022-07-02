def make_oct_scale(root, degree_list):
    """Return a list of all MIDI note values which belong to the given
    octave scale."""
    root %= 12
    degree_list = [(root + degree) % 12 for degree in degree_list]
    all_octaves = [n for n in range(128) if n % 12 in degree_list]
    return all_octaves


def major(root):
    degree_list = [0, 2, 4, 5, 7, 9, 11]
    return make_oct_scale(root, degree_list)


def ionian(root):
    return major(root)


def dorian(root):
    degree_list = [0, 2, 3, 5, 7, 9, 10]
    return make_oct_scale(root, degree_list)


def phrygian(root):
    degree_list = [0, 1, 3, 5, 7, 8, 10]
    return make_oct_scale(root, degree_list)


def lydian(root):
    degree_list = [0, 2, 4, 6, 7, 9, 11]
    return make_oct_scale(root, degree_list)


def mixolydian(root):
    degree_list = [0, 2, 4, 5, 7, 9, 10]
    return make_oct_scale(root, degree_list)


def minor(root):
    degree_list = [0, 2, 3, 5, 7, 8, 10]
    return make_oct_scale(root, degree_list)


def aeolian(root):
    return minor(root)


def locrian(root):
    degree_list = [0, 1, 3, 5, 6, 8, 10]
    return make_oct_scale(root, degree_list)


if __name__ == "__main__":
    scale = minor(11)
    for i in range(0, len(scale), 7):
        print(scale[i:i+8])
