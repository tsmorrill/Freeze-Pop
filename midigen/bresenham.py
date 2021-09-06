def Bresenham(k,n):
    """Compute Euclidean rhythm of k pulses and length n."""
    list = []
    cumDiff = -k

    for x in range(n):
        if cumDiff < 0:
            cumDiff += n
            list.append(True)
        else:
            list.append(False)
        cumDiff -= k
    return(list)
