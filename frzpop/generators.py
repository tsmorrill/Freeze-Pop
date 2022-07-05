from additives import state_machine, water
from math import sin, pi


# base machines and their derivatives


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
def list_reader(list):
    if list:
        length = len(list)
        i = 0
        while True:
            yield list[i]
            i += 1
            i %= length
    yield 0


@state_machine
def logistic(x_0, r=3.56995):
    """Generate the logistic map."""
    x = x_0

    while True:
        yield x
        x = r*x*(1-x)


def sweep(start, end, steps):
    step = (end - start)/steps
    vals = [start + step*i for i in range(steps)]

    return list_reader(vals)


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


def sine(steps, offset=0):
    step = 2*pi/steps
    vals = [sin(step*i + offset) for i in range(steps)]
    return list_reader(vals)


# machines which wrap one other machines, and their derivatives


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


def offset(machine, offset):
    return attenuvert(machine, mult=1, offset=offset)


@state_machine
def skip(machine, batches):
    while True:
        yield machine()
        for _ in range(batches - 1):
            machine()


# machines which wrap multiple other machines


@state_machine
def interleave(*machines):
    """Cycle through the outputs of the given machines."""
    if machines:
        length = len(machines)
        i = 0
        while True:
            yield machines[i]()
            i += 1
            i %= length
    while True:
        yield 0


@state_machine
def mix(*machines):                             # don't colide names with sum()
    length = len(machines)
    if machines:
        while True:
            yield sum(machines[i]() for i in range(length))
    while True:
        yield 0


if __name__ == "__main__":
    water()
