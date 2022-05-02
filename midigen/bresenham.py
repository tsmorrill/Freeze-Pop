def euclid(i, k, n):
    """Determine whether a pulse occurs on beat i in the (k,n) Euclidean rhythm.
    """
    if k > n:
        raise Exception("k cannot exceed n.")
    prod = i*k
    bool_rollover = (prod % n) > ((prod+k) % n)
    return(bool_rollover)


def Bresenham(k, n):
    """Return Euclidean rhythm of k pulses and length n."""
    bool_list = [euclid(i, k, n) for i in range(-1, n-1)]     # shift to ensure
    return(bool_list)                                         # list[0] == True


if __name__ == "__main__":
    list = [int(item) for item in Bresenham(7, 16)]
    print(list)
