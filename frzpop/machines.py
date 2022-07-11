from frzpop import additives
from math import sin, pi, pow
from typing import Optional

next_up = additives.next_up
state_machine = additives.state_machine
sip_water = additives.sip_water
Random = additives.Random
rng = additives.rng


# undecorated machines and their derivatives


def contour(
    iter: int,
    init: Optional[list] = None,
    smoothing: float = 1,
    seed=None,
    truncate: int = -1,
):
    """Generate a random contour via midpoint displacement."""

    noise = rng(seed=seed)
    if init is None:
        vals = [noise(), noise()]

    for i in range(iter):
        new_vals = []

        *head, _ = vals
        _, *tail = vals
        pairs = zip(head, tail)

        for a, b in pairs:
            new_vals.append(a)
            midpoint = (a + b) / 2
            displacement = (2 * noise() - 1) * pow(2, -smoothing * (i + 1))
            new_vals.append(midpoint + displacement)
        new_vals.append(vals[-1])
        vals = new_vals

    vals = vals[:truncate]

    offset = min(vals)
    vals = [val + offset for val in vals]
    multiplier = 1 / max(vals)
    vals = [multiplier * val for val in vals]

    return next_up(vals)


def euclid(k: int, n: int):
    """Generate pattern of k 1's equally spaced between (n-k) 0's."""

    if k == n:
        trigs = [1 for _ in range(n)]
    else:
        trigs = []
        old_res, new_res = -k % n, 0

        for _ in range(n):
            trigs.append(int(old_res > new_res))
            old_res, new_res = new_res, (new_res + k) % n

    return next_up(trigs)


def fractioning(a: int, b: int):
    """Generate Schillinger's fractioning of a and b."""

    if a < b:
        raise ValueError("b cannot exceed a")
    trigs = [0 for t in range(a * a)]
    for i in range(a - b + 1):
        for j in range(a):
            trigs[i * a + j * b] = 1
    return next_up(trigs)


def guido(lyric: str, gamut: list = None, seed=None):
    """Generate text-to-pitches method of Guido d'Arezzo using weighted random
    choices."""
    vowels = [char for char in lyric.upper() if char in "AEIOU"]

    if gamut is None:
        gamut = [
            55,
            57,
            59,
            60,
            62,
            64,
            65,
            67,
            69,
            71,
            72,
            74,
            76,
            77,
            79,
            81,
        ]

    note_assignment = {
        "A": gamut[0::5],
        "E": gamut[1::5],
        "I": gamut[2::5],
        "O": gamut[3::5],
        "U": gamut[4::5],
    }

    def weigh(potential_notes, prev_note):
        if prev_note is None:
            return [1 for note in potential_notes]
        weights = [
            1 / max(abs(note - prev_note), 1)  # avoid division by 0
            for note in potential_notes
        ]
        return weights

    notes = []
    prev_note = None

    rng = Random(seed)

    for char in vowels:
        potential_notes = note_assignment[char]
        weights = weigh(potential_notes, prev_note)
        new_note = rng.choices(potential_notes, weights, k=1)[0]
        notes.append(new_note)
        prev_note = new_note
    return next_up(notes)


def count_vowels(lyric: str) -> int:
    vowels = [char for char in lyric.upper() if char in "AEIOU"]
    return len(vowels)


def sweep(start: float, end: float, steps: int):
    jump = (end - start) / steps
    vals = [start + jump * i for i in range(steps)]

    return next_up(vals)


def ramp(steps: int):
    return sweep(start=0, end=1, steps=steps)


def saw(steps: int):
    return sweep(start=1, end=0, steps=steps)


def resultant(a: int, b: int):
    """Generate Schillinger's resultant of a and b."""

    trigs = []
    for t in range(a * b):
        trigs.append(int((t % a == 0) or (t % b == 0)))
    return next_up(trigs)


def sine_fixed(length: int, offset: float = 0):
    step = 2 * pi / length
    vals = [sin(step * i + offset) for i in range(length)]
    return next_up(vals)


@state_machine
def sine_free(wavelength: float, offset: float = 0):
    x = offset
    step = 2 * pi / wavelength
    while True:
        return sin(x)
        x += step


# simple decorated machines and their derivatives


@state_machine
def automaton(row_0: list = None, rule: int = 30, seed=None):
    """Generate an elementary cellular automaton with wraparound."""
    if row_0 is None:
        row_0 = [int(i == 0) for i in range(8)]
    row = row_0

    def unpack(rule):
        """Calculate binary representation, but backwards to work with list
        indexing."""
        results = [rule >> i & 1 for i in range(8)]
        return results

    results = unpack(rule)

    def iteration(row: list):
        def look_next_door(index, row):
            left = row[index - 1]
            center = row[index]
            right = row[(index + 1) % len(row)]

            return 4 * left + 2 * center + right

        new_row = []

        for index, _ in enumerate(row):
            bit = results[look_next_door(index, row)]
            new_row.append(bit)

        return new_row

    while True:
        yield row
        row = iteration(row)


@state_machine
def circle_map(x_0: float, omega: float, coupling: float):
    """Generate the standard circle map."""
    tau = 2 * pi
    tau_inv = 1 / tau

    x = float(x_0) % 1

    while True:
        yield x
        x = x + omega + tau_inv * sin(tau * x)
        x %= 1


@state_machine
def duffing(x_0: float, y_0: float, a: float = 2.75, b: float = 0.2):
    """Generate the Duffing map."""
    x, y = x_0, x_0

    while True:
        yield x
        x, y = y, -b * x + a * y - y**3


@state_machine
def gingerbread(x_0: float, y_0: float, a: float = 1, b: float = 1):
    """Generate the Gingerbreadman map."""
    x, y = x_0, y_0

    while True:
        yield x
        x, y = 1 - a * y + b * abs(x), x


@state_machine
def henon(x_0: float, y_0: float, a: float = 1.4, b: float = 0.3):
    """Generate the Henon map."""
    x, y = x_0, y_0

    while True:
        yield x
        x, y = 1 - a * x**2 + y, b * x


@state_machine
def lfsr(n_0: int = 1):
    """Generate a 16-bit linear feedback shift register."""
    modulus = 1 << 16
    n = n_0 % modulus
    n += int(n == 0)  # don't initialize on 0
    while True:
        yield n
        bit = (n ^ (n >> 1) ^ (n >> 3) ^ (n >> 12)) & 1
        n = (n >> 1) | (bit << 15)
        n %= modulus


@state_machine
def logistic(x_0: float, r: float = 3.56995):
    """Generate the logistic map."""
    x = x_0

    while True:
        yield x
        x = r * x * (1 - x)


@state_machine
def muse(
    out_a: int,
    out_b: int,
    out_c: int,
    out_d: int,
    feed_w: int,
    feed_x: int,
    feed_y: int,
    feed_z: int,
    notes: Optional[list] = None,
    seed=None,
):
    """Emulate the Triadex Muse."""
    if (
        min(out_a, out_b, out_c, out_d, feed_w, feed_x, feed_y, feed_z) < 0
        or max(out_a, out_b, out_c, out_d, feed_w, feed_x, feed_y, feed_z) > 39
    ):
        raise ValueError("tap locations must be integers from 0 to 39.")

    noise = rng(seed=seed)
    shift_register = [int(noise() > 0.5) for _ in range(31)]
    t = 0

    if notes is None:
        notes = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 24]

    while True:
        constant_taps = [0, 1]
        bit_taps = [(t >> i) & 1 for i in range(5)]
        tri_taps = [int(t % 6 > 2), int(t % 12 > 5)]
        all_taps = constant_taps + shift_register + bit_taps + tri_taps

        scale_degree = (
            8 * all_taps[out_d]
            + 4 * all_taps[out_c]
            + 2 * all_taps[out_b]
            + all_taps[out_a]
        )
        yield notes[scale_degree % len(notes)]

        bit = all_taps[feed_w] + all_taps[feed_x] + all_taps[feed_y] + all_taps[feed_z]
        bit %= 2

        shift_register.insert(0, bit)
        shift_register.pop()

        t += 1
        t %= 96


@state_machine
def pfsr(n: int = 0b10101010, len: int = 8, prob: float = 0.5, seed=None):
    """Return a generator for a probabalistic feedback shift register."""
    mask = (2 << len) - 1
    n &= mask
    noise = rng(seed=seed)

    while True:
        yield n
        bit = n & 1
        n >>= 1
        if prob == 1 or noise() < prob:
            bit = 1 - bit
        n += bit << (len - 1)


@state_machine
def tent(x_0: float, m: float = 1.5):
    """Generate the tent map."""
    x = x_0

    while True:
        yield x
        x = m * min(x, 1 - x)


@state_machine
def xshift(n_0: int):
    """Generate an xor shift pseudorandom number generator."""
    n = n_0
    len = 16
    modulus = 1 << len
    while True:
        yield n
        n ^= n >> 7
        n ^= n << 9
        n ^= n >> 13
        n %= modulus


# machines which input other machines, and their derivatives


@state_machine
def clip(machine, lower: float, upper: float):
    instance = machine()
    while True:
        yield max(lower, min(instance(), upper))


@state_machine
def is_over(machine, threshold: float):
    instance = machine()
    while True:
        yield int(instance() > threshold)


def pulse(steps: int, duty: float = 0.5):
    instance = sweep(1, 0, steps)
    return is_over(instance, duty)


@state_machine
def attenuvert(machine, mult: float, offset: float = 0):
    instance = machine()
    while True:
        yield mult * instance() + offset


def offset(machine, offset: float):
    return attenuvert(machine, mult=1, offset=offset)


@state_machine
def skip(machine, batches: int):
    instance = machine()
    while True:
        yield instance()
        for _ in range(batches - 1):
            instance()


# machines which input multiple other machines


@state_machine
def interleave(*machines):
    """Cycle through the outputs of the input machines."""
    if not machines:
        raise ValueError("interleave requires a nonempty list of machines.")
    length = len(machines)
    instances = [machine() for machine in machines]
    i = 0
    while True:
        yield instances[i]()
        i += 1
        i %= length


@state_machine
def mix(*machines):  # don't colide names with sum()
    if not machines:
        raise ValueError("mix requires a nonempty list of machines.")
    instances = [machine() for machine in machines]
    while True:
        yield sum(instance() for instance in instances)


if __name__ == "__main__":
    sip_water()

    Schill = resultant(3, 4)
    print(Schill(), Schill())
