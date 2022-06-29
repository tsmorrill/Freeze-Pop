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
