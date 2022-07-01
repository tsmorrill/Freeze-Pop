import numpy as np
import random


def p_gen(gen):
    """Wrap a parameterized generator in a function call."""

    def wrapper(*args, **kwargs):
        generator = gen(*args, **kwargs)

        def func(*args):
            return next(generator)
        return(func)
    return wrapper


def make_guido_phrase(lyric_string, scale=None):
    """Return a phrase. Probabilistically assign pitches to text using method
    of Guido d'Arezzo."""
    lyric_string = lyric_string.upper()
    vowels = [char for char in lyric_string if char in "AEIOU"]

    if scale is None:                                    # use d'Arezzo's scale
        scale = [55, 57, 59, 60, 62,         # list indices will be taken mod 5
                 64, 65, 67, 69, 71,
                 72, 74, 76, 77, 79,
                 81]

    note_assignment = {"A": scale[0::5],
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

    phrase = []
    prev_note = None

    for char in vowels:
        potential_notes = note_assignment[char]
        weights = weigh(potential_notes, prev_note)
        new_note = random.choices(potential_notes, weights, k=1)[0]
        phrase.append(new_note)
        prev_note = new_note
    return phrase


def make_midpoint_displace(iter, smoothing, seed, init):
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


@p_gen
def make_pfsr(n, len=8, prob=0.5):
    """Return a generator for a probabalistic feedback shift register."""
    modulus = 1 << len
    n %= modulus

    while True:
        yield n
        bit = n & 1
        n >>= 1
        if random.uniform(0, 1) < prob:
            bit = 1 - bit
        bit <<= len-1
        n += bit
