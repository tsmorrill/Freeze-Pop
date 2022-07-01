from math import floor, sin, pi


def p_gen(gen):
    """Wrap a parameterized generator in a function call."""

    def wrapper(*args, **kwargs):
        generator = gen(*args, **kwargs)

        def func():
            return next(generator)
        return(func)
    return wrapper


@p_gen
def circle_map(x, omega, coupling):
    """Return a generator for the circle map."""
    tau = 2*pi
    tau_inv = 1/tau

    while True:
        yield x
        x = x + omega + tau_inv*sin(tau*x)
        x %= 1


@p_gen
def duffing(x, y, a=2.75, b=0.2):
    """Return a generator for the Duffing map."""

    while True:
        yield x
        x, y = y, -b*x + a*y - y**3


@p_gen
def gingerbread(x, y, a=1, b=1):
    """Return a generator for the Gingerbreadman map."""

    while True:
        yield x
        x, y = 1 - a*y + b*abs(x), x


@p_gen
def henon(x, y, a=1.4, b=0.3):
    """Return a generator for the Henon map."""

    while True:
        yield x
        x, y = 1 - a*x**2 + y, b*x


@p_gen
def lfsr(n):
    """Return a generator for a linear feedback shift register."""
    n += int(n == 0)                                    # don't initialize on 0
    while True:
        yield n
        bit = (n ^ (n >> 1) ^ (n >> 3) ^ (n >> 12)) & 1
        n = (n >> 1) | (bit << 15)


@p_gen
def logistic(x, r=3.56995):
    """Return a generator for the logistic map."""

    while True:
        yield x
        x = r*x*(1-x)


def make_CC(x):
    x = max(0, min(x, 127))
    return floor(x)


@p_gen
def tent(x, m=1.5):
    """Return a generator for the tent map."""

    while True:
        yield x
        x = m*min(x, 1-x)


@p_gen
def xor_shift(n):
    """Return a generator for an xor shift pseudorandom number generator."""
    len = 16
    modulus = 1 << len
    while True:
        yield n
        n ^= n >> 7
        n ^= n << 9
        n ^= n >> 13
        n %= modulus


if __name__ == "__main__":
    print(make_CC(23.45))
