import random
import numpy as np


def expressive(func):
    # stress pattern of 16th notes in common time
    stresses = [7, -1, 3, -5, 5, -3, 1, -7, 6, -2, 2, -6, 4, -4, 0, -8]

    def wrap(t):
        # add current stress to velocity
        t %= 16
        val = func() + stresses[t]
        val = max(0, min(val, 127))
        return val
    return wrap


@expressive
def ppp(): return(8)                                          # 0 < ppp < 15


@expressive
def pp(): return(24)                                          # 16 < pp < 31


@expressive
def p(): return(40)                                           # 32 < p < 47


@expressive
def mp(): return(56)                                          # 48 < mp < 63


@expressive
def mf(): return(72)                                          # 64 < mf < 79


@expressive
def f(): return(88)                                           # 80 < f < 95


@expressive
def ff(): return(104)                                         # 96 < ff < 111


@expressive
def fff(): return(120)                                        # 112 < fff < 127


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


class Euclid(Sequencer):
    @staticmethod
    def is_trig(t, trig_count, len):
        if trig_count < 0 or trig_count > len:
            raise ValueError("trig_count must be within 0 and len inclusive")
        prod = t * trig_count
        rollover_bool = (prod % len) > ((prod + trig_count) % len)
        return(rollover_bool)

    @staticmethod
    def trigs(trig_count, len):
        return [Euclid.is_trig(t, trig_count, len) for t in range(-1, len-1)]

    def __init__(self, trig_count, len):
        self.values = Euclid.trigs(trig_count, len)
        self.len = len
        self.clock = 0


class Resultant(Sequencer):
    @staticmethod
    def trigs(a, b):
        return [(t % a == 0) or (t % b == 0) for t in range(a*b)]

    def __init__(self, a, b):
        self.values = Resultant.trigs(a, b)
        self.len = a*b
        self.clock = 0


class Fractioning(Sequencer):
    @staticmethod
    def trigs(a, b):
        if a < b:
            raise ValueError("b cannot exceed a")
        trig_list = [0 for t in range(a*a)]
        for i in range(a - b + 1):
            for j in range(a):
                trig_list[i*a + j*b] = True
        return(trig_list)

    def __init__(self, a, b):
        self.values = Fractioning.trigs(a, b)
        self.len = a*a
        self.clock = 0


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
    seq = Fractioning(4, 3)
    list = seq.values
    list = [int(val) for val in list]
    print(list)
