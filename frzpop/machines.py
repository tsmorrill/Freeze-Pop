from additives import list_reader, state_machine, sip_water, rng
from math import sin, pi, pow


# undecorated machines and their derivatives


def contour(iter, init=None, smoothing=1, seed=None, truncate=-1):
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
            midpoint = (a + b)/2
            displacement = (2*noise() - 1) * pow(2, -smoothing*(i + 1))
            new_vals.append(midpoint + displacement)
        new_vals.append(vals[-1])
        vals = new_vals

    vals = vals[:truncate]

    offset = min(vals)
    vals = [val + offset for val in vals]
    multiplier = 1/max(vals)
    vals = [multiplier * val for val in vals]

    return list_reader(vals)


def euclid(k, n):
    """Generate pattern of k 1's equally spaced between (n-k) 0's."""

    if k == n:
        trigs = [1 for _ in range(n)]
    else:
        trigs = []
        old_res, new_res = -k % n, 0

        for _ in range(n):
            trigs.append(int(old_res > new_res))
            old_res, new_res = new_res, (new_res + k) % n

    return list_reader(trigs)


def fractioning(a, b):
    """Generate Schillinger's fractioning of a and b."""

    if a < b:
        raise ValueError("b cannot exceed a")
    trigs = [0 for t in range(a*a)]
    for i in range(a - b + 1):
        for j in range(a):
            trigs[i*a + j*b] = 1
    return list_reader(trigs)


def sweep(start, end, steps):
    jump = (end - start)/steps
    vals = [start + jump*i for i in range(steps)]

    return list_reader(vals)


def ramp(steps): return sweep(start=0, end=1, steps=steps)


def saw(steps): return sweep(start=1, end=0, steps=steps)


def resultant(a, b):
    """Generate Schillinger's resultant of a and b."""

    trigs = [(t % a == 0) or (t % b == 0) for t in range(a*b)]
    return list_reader(trigs)


def sine(steps, offset=0):
    step = 2*pi/steps
    vals = [sin(step*i + offset) for i in range(steps)]
    return list_reader(vals)


# simple decorated machines and their derivatives


@state_machine
def automaton(row_0=None, rule=30, seed=None):
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

    def iteration(row):
        def look_next_door(index, row):
            left = row[index - 1]
            center = row[index]
            right = row[(index + 1) % len(row)]

            return 4*left + 2*center + right

        new_row = []

        for index, _ in enumerate(row):
            bit = results[look_next_door(index, row)]
            new_row.append(bit)

        return new_row

    while True:
        yield row
        row = iteration(row)


@state_machine
def circle_map(x_0, omega, coupling):
    """Generate the standard circle map."""
    tau = 2*pi
    tau_inv = 1/tau

    x = float(x_0) % 1

    while True:
        yield x
        x = x + omega + tau_inv*sin(tau*x)
        x %= 1


@state_machine
def duffing(x_0, y_0, a=2.75, b=0.2):
    """Generate the Duffing map."""
    x, y = x_0, x_0

    while True:
        yield x
        x, y = y, -b*x + a*y - y**3


@state_machine
def gingerbread(x_0, y_0, a=1, b=1):
    """Generate the Gingerbreadman map."""
    x, y = x_0, y_0

    while True:
        yield x
        x, y = 1 - a*y + b*abs(x), x


@state_machine
def henon(x_0, y_0, a=1.4, b=0.3):
    """Generate the Henon map."""
    x, y = x_0, y_0

    while True:
        yield x
        x, y = 1 - a*x**2 + y, b*x


@state_machine
def lfsr(n_0=1):
    """Generate a 16-bit linear feedback shift register."""
    modulus = 1 << 16
    n = n_0 % modulus
    n += int(n == 0)                                    # don't initialize on 0
    while True:
        yield n
        bit = (n ^ (n >> 1) ^ (n >> 3) ^ (n >> 12)) & 1
        n = (n >> 1) | (bit << 15)
        n %= modulus


@state_machine
def logistic(x_0, r=3.56995):
    """Generate the logistic map."""
    x = x_0

    while True:
        yield x
        x = r*x*(1-x)


@state_machine
def pfsr(n=0b10101010, len=8, prob=0.5, seed=None):
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
        n += bit << (len-1)


@state_machine
def tent(x_0, m=1.5):
    """Generate the tent map."""
    x = x_0

    while True:
        yield x
        x = m*min(x, 1-x)


@state_machine
def xshift(n_0):
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
def clip(machine, min, max):
    instance = machine()
    while True:
        yield max(min, min(instance(), max))


@state_machine
def is_over(machine, threshold):
    instance = machine()
    while True:
        yield int(instance() > threshold)


def pulse(steps, duty=0.5):
    instance = sweep(1, 0, steps)
    return is_over(instance, duty)


@state_machine
def attenuvert(machine, mult, offset=0):
    instance = machine()
    while True:
        yield mult*instance() + offset


def offset(machine, offset): return attenuvert(machine, mult=1, offset=offset)


@state_machine
def skip(machine, batches):
    instance = machine()
    while True:
        yield instance()
        for _ in range(batches - 1):
            instance()


# machines which wrap multiple other machines


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
def mix(*machines):                             # don't colide names with sum()
    if not machines:
        raise ValueError("mix requires a nonempty list of machines.")
    instances = [machine() for machine in machines]
    while True:
        yield sum(instance() for instance in instances)


if __name__ == "__main__":
    sip_water()
    machine = automaton()
    for _ in range(16):
        print(machine())
