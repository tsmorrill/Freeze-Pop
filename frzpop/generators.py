from additives import state_machine, water
from math import sin, pi


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
def lfsr(n_0):
    """Generate a linear feedback shift register."""
    n = n_0
    n += int(n == 0)                                    # don't initialize on 0
    while True:
        yield n
        bit = (n ^ (n >> 1) ^ (n >> 3) ^ (n >> 12)) & 1
        n = (n >> 1) | (bit << 15)


@state_machine
def logistic(x_0, r=3.56995):
    """Generate the logistic map."""
    x = x_0

    while True:
        yield x
        x = r*x*(1-x)


def sweep(start, end, steps):
    """Generate a linear sweep."""
    step = (end - start)/steps
    vals = [start + step*i for i in range(steps)]

    return from_list(vals)


def ramp(steps):
    return sweep(start=0, end=1, steps=steps)


def saw(steps):
    return sweep(start=1, end=0, steps=steps)


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


@state_machine
def list_reader(list):
    if list:
        length = len(list)
        i = 0
        while True:
            yield list[i]
            i += 1
            i %= length
    yield None


def sine(steps, offset=0):
    step = 2*pi/steps
    vals = [sin(step*i + offset) for i in range(steps)]
    return from_list(vals)


@state_machine
def clip(generator, min, max):
    while True:
        yield max(min, min(generator(), max))


@state_machine
def interleave(*generators):
    """Cycle through the outputs of the given generators."""
    if generators:
        length = len(generators)
        i = 0
        while True:
            yield generators[i]()
            i += 1
            i %= length
    while True:
        yield None


@state_machine
def mix(*generators):                            # don't override sum() builtin
    length = len(generators)
    if generators:
        while True:
            yield sum(generators[i]() for i in range(length))
    while True:
        yield None


@state_machine
def is_over(generator, threshold):
    while True:
        yield int(generator() > threshold)


def pulse(steps, duty=0.5):
    generator = sweep(1, 0, steps)
    return is_over(generator, duty)


@state_machine
def attenuvert(generator, mult, offset=0):
    while True:
        yield mult*generator() + offset


def offset(generator, offset):
    return attenuvert(generator, mult=1, offset=offset)


@state_machine
def skip(generator, batches):
    while True:
        yield generator()
        for _ in range(batches - 1):
            generator()


if __name__ == "__main__":
    water()
