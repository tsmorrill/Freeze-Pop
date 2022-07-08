from frzpop import additives
from math import floor


next_in = additives.next_in
rng = additives.rng
state_machine = additives.state_machine
sip_water = additives.sip_water


def emphasize_16ths(center_vel: int):
    # curiously, identical to ordered dithering numerators
    stress_16ths = [7, -1, 3, -5, 5, -3, 1, -7, 6, -2, 2, -6, 4, -4, 0, -8]
    vels = [center_vel + stress for stress in stress_16ths]
    return next_in(vels)


def ppp():
    return emphasize_16ths(8)  # 0 <= ppp <=  15


def pp():
    return emphasize_16ths(24)  # 16 <= pp  <=  31


def p():
    return emphasize_16ths(40)  # 32 <= p   <=  47


def mp():
    return emphasize_16ths(56)  # 48 <= mp  <=  63


def mf():
    return emphasize_16ths(72)  # 64 <= mf  <=  79


def f():
    return emphasize_16ths(88)  # 80 <= f   <=  95


def ff():
    return emphasize_16ths(104)  # 96 <= ff  <= 111


def fff():
    return emphasize_16ths(120)  # 112 <= fff <= 127


@state_machine
def random_vel(min: int, max: int, seed=None):
    noise = rng(seed)
    while True:
        yield floor(min + (max - min + 1) * noise())


if __name__ == "__main__":
    sip_water()
    machine = emphasize_16ths(40)
    for _ in range(16):
        print(machine())
