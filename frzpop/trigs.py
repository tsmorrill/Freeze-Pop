def euclid(k, n):
    """Return Euclidean rhythm of k True bools equally spaced
    in a list of n bools."""

    trigs = []
    old_res = -k % n
    new_res = 0

    if k == n:
        return [True for _ in range(n)]

    for _ in range(n):
        trigs.append(old_res > new_res)
        old_res, new_res = new_res, (new_res + k) % n

    return trigs


def fractioning(a, b):
    """Return fractioning of a and b according to the Schillinger system."""
    if a < b:
        raise ValueError("b cannot exceed a")
    trigs = [False for t in range(a*a)]
    for i in range(a - b + 1):
        for j in range(a):
            trigs[i*a + j*b] = True
    return(trigs)


def resultant(a, b):
    """Return resultant of a and b according to the Schillinger system."""

    return [(t % a == 0) or (t % b == 0) for t in range(a*b)]


if __name__ == "__main__":
    trigs = resultant(3, 7)
    ints = [int(trig) for trig in trigs]
    print(ints)
