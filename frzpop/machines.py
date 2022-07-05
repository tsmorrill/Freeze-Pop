from additives import list_reader, state_machine, sip_water, rng
from math import sin, pi


# undecorated machines and their derivatives


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
def pfsr(n=0, len=8, prob=0.5, seed=None):
    """Return a generator for a probabalistic feedback shift register."""
    modulus = 1 << len
    n %= modulus
    noise = rng(seed=seed)

    while True:
        yield n
        bit = n & 1
        n >>= 1
        if noise() < prob:
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
    while True:
        yield max(min, min(machine(), max))


@state_machine
def is_over(machine, threshold):
    while True:
        yield int(machine() > threshold)


def pulse(steps, duty=0.5):
    machine = sweep(1, 0, steps)
    return is_over(machine, duty)


@state_machine
def attenuvert(machine, mult, offset=0):
    while True:
        yield mult*machine() + offset


def offset(machine, offset): return attenuvert(machine, mult=1, offset=offset)


@state_machine
def skip(machine, batches):
    while True:
        yield machine()
        for _ in range(batches - 1):
            machine()


# machines which wrap multiple other machines


@state_machine
def interleave(*machines):
    """Cycle through the outputs of the input machines."""
    if not machines:
        raise ValueError("interleave requires a nonempty list of machines.")
    length = len(machines)
    i = 0
    while True:
        yield machines[i]()
        i += 1
        i %= length


@state_machine
def mix(*machines):                             # don't colide names with sum()
    length = len(machines)
    if not machines:
        raise ValueError("mix requires a nonempty list of machines.")
    while True:
        yield sum(machines[i]() for i in range(length))


if __name__ == "__main__":
    sip_water()
    machine = pfsr()
    for _ in range(16):
        print(bin(machine()))
