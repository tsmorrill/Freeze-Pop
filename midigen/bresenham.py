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
    list = [euclid(i - 1, k, n) for i in range(n)]      # shift by -k to ensure
    return(list)                                        # list[0] == True


if __name__ == "__main__":
    list = Bresenham(2, 16)
    list = [int(item) for item in list]
    print(list)
