def euclid(i, k, n):
    """Determine whether a pulse occurs on beat i in the (k,n) Euclidean rhythm.
    """
    rollover = (k*i % n) > (k*(i+1) % n)
    return(rollover)


def Bresenham(k, n):
    """Return Euclidean rhythm of k pulses and length n."""
    list = [euclid(i - k, k, n) for i in range(n)]      # shift by -k to ensure
    return(list)                                        # list[0] == True


if __name__ == "__main__":
    print(Bresenham(7, 16))
