def euclid(i, k, n):
    """Determine whether a pulse occurs on beat i in the (k,n) Euclidean rhythm.
    """
    if k > n:
        raise Exception("k cannot exceed n.")
    prod = i*k
    rollover = (prod % n) > ((prod+k) % n)
    return(rollover)


def Bresenham(k, n):
    """Return Euclidean rhythm of k pulses and length n."""
    list = [euclid(i, k, n) for i in range(-1, n-1)]    # shift by -1 to ensure
    return(list)                                        # list[0] == True


if __name__ == "__main__":
    list = [int(item) for item in Bresenham(7, 16)]
    print(list)
