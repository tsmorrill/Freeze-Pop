import random
import numpy as np

C0 = 12
Db0 = 13
D0 = 14
Eb0 = 15
E0 = 16
F0 = 17
Gb0 = 18
G0 = 19
Ab0 = 20
A0 = 21
Bb0 = 22
B0 = 23
C1 = 24
Db1 = 25
D1 = 26
Eb1 = 27
E1 = 28
F1 = 29
Gb1 = 30
G1 = 31
Ab1 = 32
A1 = 33
Bb1 = 34
B1 = 35
C2 = 36
Db2 = 37
D2 = 38
Eb2 = 39
E2 = 40
F2 = 41
Gb2 = 42
G2 = 43
Ab2 = 44
A2 = 45
Bb2 = 46
B2 = 47
C3 = 48
Db3 = 49
D3 = 50
Eb3 = 51
E3 = 52
F3 = 53
Gb3 = 54
G3 = 55
Ab3 = 56
A3 = 57
Bb3 = 58
B3 = 59
C4 = 60
Db4 = 61
D4 = 62
Eb4 = 63
E4 = 64
F4 = 65
Gb4 = 66
G4 = 67
Ab4 = 68
A4 = 69
Bb4 = 70
B4 = 71
C5 = 72
Db5 = 73
D5 = 74
Eb5 = 75
E5 = 76
F5 = 77
Gb5 = 78
G5 = 79
Ab5 = 80
A5 = 81
Bb5 = 82
B5 = 83
C6 = 84
Db6 = 85
D6 = 86
Eb6 = 87
E6 = 88
F6 = 89
Gb6 = 90
G6 = 91
Ab6 = 92
A6 = 93
Bb6 = 94
B6 = 95
C7 = 96
Db7 = 97
D7 = 98
Eb7 = 99
E7 = 100
F7 = 101
Gb7 = 102
G7 = 103
Ab7 = 104
A7 = 105
Bb7 = 106
B7 = 107
C8 = 108
Db8 = 109
D8 = 110
Eb8 = 111
E8 = 112
F8 = 113
Gb8 = 114
G8 = 115
Ab8 = 116
A8 = 117
Bb8 = 118
B8 = 119
C9 = 120
Db9 = 121
D9 = 122
Eb9 = 123
E9 = 124
F9 = 125
Gb9 = 126
G9 = 127


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
        if trig_count > len:
            raise ValueError("trig_count cannot exceed len")
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


def diamond_square(iter, smoothing, seed, init):
    """Create 2^iter + 1 square heightmap via diamond square algorithm.
    """
    if init is None:
        random.seed(seed + "init")
        heightmap = np.array([[random.random(), random.random()],
                              [random.random(), random.random()]])
    else:
        heightmap = np.array(init)

    random.seed(seed + "iterate")
    for n in range(iter):
        rows, cols = heightmap.shape
        temp_map = np.zeros((2*rows - 1, 2*cols - 1))
        jitter_diamond = 2**(-smoothing*(2*n + 1))
        jitter_square = 2**(-smoothing*(2*n + 2))
        for (i, j), value_ij in np.ndenumerate(heightmap):
            north_exists = i > 0
            south_exists = i < rows - 1
            west_exists = j > 0
            east_exists = j < cols - 1

            temp_map[2*i, 2*j] = heightmap[i, j]

            if east_exists and south_exists:
                diamond_center = (heightmap[i, j] + heightmap[i, j+1]
                                  + heightmap[i+1, j] + heightmap[i+1, j+1])
                diamond_center /= 4
                diamond_center += random.uniform(-1, 1)*jitter_diamond
                temp_map[2*i + 1, 2*j + 1] = diamond_center

                square_top = (heightmap[i, j] + heightmap[i, j+1]
                              + diamond_center)
                if north_exists:
                    square_top += temp_map[2*i - 1, 2*j + 1]
                    square_top /= 4
                else:
                    square_top /= 3
                square_top += random.uniform(-1, 1)*jitter_square
                temp_map[2*i, 2*j + 1] = square_top

                square_left = (heightmap[i, j] + heightmap[i+1, j]
                               + diamond_center)
                if west_exists:
                    square_left += temp_map[2*i + 1, 2*j - 1]
                    square_left /= 4
                else:
                    square_left /= 3
                square_left += random.uniform(-1, 1)*jitter_square
                temp_map[2*i + 1, 2*j] = square_left
            elif east_exists and not south_exists:
                square_top = (heightmap[i, j] + heightmap[i, j+1]
                              + temp_map[2*i - 1, 2*j + 1])/3
                square_top += random.uniform(-1, 1)*jitter_square
                temp_map[2*i, 2*j + 1] = square_top
            elif not east_exists and south_exists:
                square_left = (heightmap[i, j] + heightmap[i+1, j]
                               + temp_map[2*i + 1, 2*j - 1])/3
                square_left += random.uniform(-1, 1)*jitter_square
                temp_map[2*i + 1, 2*j] = square_left
        heightmap = temp_map

        # noise = 2*np.random.random(heightmap.shape) - 1
        # noise /= 2**(n+5)
        # heightmap += noise

        # heightmap_to_png(heightmap, seed + ' ' + str(n))

    # normalize
    heightmap -= heightmap.min()
    heightmap /= heightmap.max()
    return(heightmap)


def map_interp(heightmap):
    rows, cols = heightmap.shape
    temp_map = np.zeros((rows - 1, cols - 1))
    for (i, j), value_ij in np.ndenumerate(temp_map):
        average = (heightmap[i, j] + heightmap[i, j+1]
                   + heightmap[i+1, j] + heightmap[i+1, j+1])/4
        temp_map[i, j] = average
    return(temp_map)


def trim_and_flatten(heightmap, rows=1, cols=1):
    for i in range(rows):
        heightmap = np.delete(heightmap, -1, 0)
    for j in range(cols):
        heightmap = np.delete(heightmap, -1, 1)
    heightmap = heightmap.flatten()
    return(heightmap)


def entrywise_product(heightmap0, heightmap1, normalize=True):
    output = np.zeros(heightmap0.shape)
    for (i, j), value in np.ndenumerate(heightmap0):
        output[i, j] = heightmap0[i, j]*heightmap1[i, j]
    if normalize:
        output = heightmap_normalize(output)
    return(output)


def heightmap_normalize(heightmap):
    heightmap -= heightmap.min()
    heightmap /= heightmap.max()
    return(heightmap)


def mean_normalize(heightmap, new_mean):
    size = heightmap.shape
    old_mean = np.sum(heightmap.reshape(1, -1))/size
    heightmap = heightmap*new_mean/old_mean
    return(heightmap)


def heightmap_radar_list(heightmap, r_step, theta_step,
                         init_angle=0, sweep=np.pi):
    """Read and interpolate a square heightmap radially from the center.
    """
    N = heightmap.shape[0]
    list = []
    for turn in range(theta_step):
        angle = sweep*turn/theta_step
        for length in range(r_step):
            x, y = length*np.cos(angle), length*np.sin(angle)
            # correct for orientation
            i, j = int(np.floor(y + N/2)), int(np.floor(x + N/2))
            u, v = y + N/2 - i, x + N/2 - j
            A, B = heightmap[i, j], heightmap[i, j+1]
            C, D = heightmap[i+1, j], heightmap[i+1, j+1]
            interp = (A*(1-v) + B*v)*(1-u) + (C*(1-v) + D*v)*u
            list.append(interp)
    list = np.array(list)
    return(list)


def erode(heightmap, seed, iter):
    rows, cols = heightmap.shape
    random.seed(seed + "rain")

    for n in range(iter):
        i = random.randint(0, rows-1)
        j = random.randint(0, cols-1)
        droplet_volume = 1
        while droplet_volume > 0:
            north_exists = i > 0
            south_exists = i < rows - 1
            west_exists = j > 0
            east_exists = j < cols - 1

            current_min = heightmap[i, j]
            choices = [(0, 0)]

            if north_exists:
                new_height = heightmap[i - 1, j]
                if new_height < current_min:
                    current_min = heightmap
                    choices = [(i - 1, j)]
                elif new_height == current_min:
                    choices.append((i - 1, j))
            if south_exists:
                new_height = heightmap[i + 1, j]
                if new_height < current_min:
                    current_min = heightmap
                    choices = [(i + 1, j)]
                elif new_height == current_min:
                    choices.append((i + 1, j))
            if west_exists:
                new_height = heightmap[i, j - 1]
                if new_height < current_min:
                    current_min = heightmap
                    choices = [(i, j - 1)]
                elif new_height == current_min:
                    choices.append((i, j - 1))
            if east_exists:
                new_height = heightmap[i, j + 1]
                if new_height < current_min:
                    current_min = heightmap
                    choices = [(i, j + 1)]
                elif new_height == current_min:
                    choices.append((i, j + 1))

            if len(choices) == 1:
                new_i, new_j = choices[0]
            else:
                random.seed(seed + "choose")
                new_i, new_j = random.choice(choices)
            if (i, j) == (new_i, new_j):
                droplet_volume = -1
            else:
                average = (heightmap[i, j] + heightmap[new_i, new_j])/2
                heightmap[i, j] = average
                heightmap[new_i, new_j] = average
                droplet_volume -= random.random()/8
                i, j = new_i, new_j

    # normalize
    heightmap -= heightmap.min()
    heightmap /= heightmap.max()
    return(heightmap)

    dithering_xor_0 = [0,  8,  4, 12,  2, 10,  6, 14,
                       1,  9,  5, 13,  3, 11,  7, 15]
    dithering_xor_1 = [1,  9,  5, 13,  3, 11,  7, 15,
                       0,  8,  4, 12,  2, 10,  6, 14]
    dithering_xor_2 = [2, 10,  6, 14,  0,  8,  4, 12,
                       3, 11,  7, 15,  1,  9,  5, 13]
    dithering_xor_3 = [3, 11,  7, 15,  1,  9,  5, 13,
                       2, 10,  6, 14,  0,  8,  4, 12]
    dithering_xor_4 = [4, 12,  0,  8,  6, 14,  2, 10,
                       5, 13,  1,  9,  7, 15,  3, 11]
    dithering_xor_5 = [5, 13,  1,  9,  7, 15,  3, 11,
                       4, 12,  0,  8,  6, 14,  2, 10]
    dithering_xor_6 = [6, 14,  2, 10,  4, 12,  0,  8,
                       7, 15,  3, 11,  5, 13,  1,  9]
    dithering_xor_7 = [7, 15,  3, 11,  5, 13,  1,  9,
                       6, 14,  2, 10,  4, 12,  0,  8]
    dithering_xor_8 = [8,  0, 12,  4, 10,  2, 14,  6,
                       9,  1, 13,  5, 11,  3, 15,  7]
    dithering_xor_9 = [9,  1, 13,  5, 11,  3, 15,  7,
                       8,  0, 12,  4, 10,  2, 14,  6]
    dithering_xor_A = [10,  2, 14,  6,  8,  0, 12,  4,
                       11,  3, 15,  7,  9,  1, 13,  5]
    dithering_xor_B = [11,  3, 15,  7,  9,  1, 13,  5,
                       10,  2, 14,  6,  8,  0, 12,  4]
    dithering_xor_C = [12,  4,  8,  0, 14,  6, 10,  2,
                       13,  5,  9,  1, 15,  7, 11,  3]
    dithering_xor_D = [13,  5,  9,  1, 15,  7, 11,  3,
                       12,  4,  8,  0, 14,  6, 10,  2]
    dithering_xor_E = [14,  6, 10,  2, 12,  4,  8,  0,
                       15,  7, 11,  3, 13,  5,  9,  1]
    dithering_xor_F = [15,  7, 11,  3, 13,  5,  9,  1,
                       14,  6, 10,  2, 12,  4,  8,  0]

    def dithermap_to_threshold(dithermap):
        length = len(dithermap)
        output = [(i + 0.5)/length for i in dithermap]
        return(output)

    def dither_1D(iter):
        """Create 1 x 2^iter dithering map.
        """
        length = 2**iter
        format_string = '0' + str(iter) + 'b'
        list = [1 - int(format(i, format_string)[::-1], 2)
                for i in range(length)[::-1]]
        threshold = np.array(list)
        return(threshold)

    def dither(heightmap, dither_map):
        temp_list = []
        for i, value in enumerate(heightmap):
            threshold = dither_map[i]
            if value >= threshold:
                temp_list.append('X')
            else:
                temp_list.append('-')
        return temp_list


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
