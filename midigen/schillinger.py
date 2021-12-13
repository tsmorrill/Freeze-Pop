def main(a, b):
    bits = [int(item) for item in fractioning(a, b)]
    print(bits)


def resultant(a, b):
    beats = [i % a == 0 or i % b == 0 for i in range(a*b)]
    return(beats)


def fractioning(a, b):
    beats = [i % a == 0 for i in range(a*a)]
    for i in range(a - b + 1):
        for j in range(a):
            beats[i*a + j*b] = True
    return(beats)


if __name__ == '__main__':
    main(6, 5)
