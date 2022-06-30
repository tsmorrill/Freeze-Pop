import random
import numpy as np


class Sequencer:
    def __init__(self, list):
        self.values = list
        self.len = len(list)
        self.clock = 0

    def trig(self):
        value = self.values[self.clock]
        self.clock = (self.clock + 1) % self.len
        return value

    def reset(self):
        value = self.values[0]
        self.clock = 1
        return value

    def reverse(self):
        value = self.values[self.clock - 1]
        self.values = self.values[::-1]
        self.clock = (1 - self.clock) % self.len
        return value


def Euclid(k, n):
    """Return Euclidean rhythm of k True bools equally spaced
    in a list of n bools."""

    trigs = []
    old_res = -k % n
    new_res = 0

    if k == n:
        return [True for _ in range(n)]

    for _ in range(n):
        trigs.append(old_res > new_res)
        old_res, new_res = new_res, (new_res + k) % n

    return trigs


def fractioning(a, b):
    """Return fractioning of a and b according to the Schillinger system."""
    if a < b:
        raise ValueError("b cannot exceed a")
    trigs = [False for t in range(a*a)]
    for i in range(a - b + 1):
        for j in range(a):
            trigs[i*a + j*b] = True
    return(trigs)


def resultant(a, b):
    """Return resultant of a and b according to the Schillinger system."""

    return [(t % a == 0) or (t % b == 0) for t in range(a*b)]


def heightmap_1D(iter, smoothing, seed, init):
    """Create 2^iter + 1 linear heightmap via midpoint displacement.
    """
    if init is None:
        random.seed(seed + "init")
        heightmap = np.array([random.random(), random.random()])
    else:
        heightmap = init

    random.seed(seed + "iterate")
    for i in range(iter):
        temp_list = []
        for j in range(2**i):
            temp_list.append(heightmap[j])
            temp_list.append((heightmap[j]+heightmap[j+1])/2
                             + random.uniform(-1, 1)*2**(-smoothing*(i+1)))
        temp_list.append(heightmap[-1])
        heightmap = np.array(temp_list)

    # normalize
    heightmap += heightmap.min()
    heightmap /= heightmap.max()
    return(heightmap)


guido_scale = [55, 57, 59, 60, 62,           # list indices will be taken mod 5
               64, 65, 67, 69, 71,
               72, 74, 76, 77, 79,
               81]


def guido(lyric, scale=guido_scale):
    """Probabilistically assign pitches to text using method of Guido d'Arezzo.
    """
    lyric = lyric.upper()
    vowels = [char for char in lyric if char in "AEIOU"]

    dict = {"A": scale[0::5],
            "E": scale[1::5],
            "I": scale[2::5],
            "O": scale[3::5],
            "U": scale[4::5]}

    def weigh(potential_notes, prev_note):
        if prev_note is None:
            return [1 for note in potential_notes]
        weights = [1/max(abs(note - prev_note), 1/2)      # avoid division by 0
                   for note in potential_notes]
        return weights

    note_list = []
    prev_note = None

    for char in vowels:
        potential_notes = dict[char]
        weights = weigh(potential_notes, prev_note)
        new_note = random.choices(potential_notes, weights, k=1)[0]
        note_list.append(new_note)
        prev_note = new_note
    return note_list


if __name__ == "__main__":
    trigs = resultant(3, 7)
    ints = [int(trig) for trig in trigs]
    print(ints)
