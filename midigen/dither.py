import numpy as np

dithering_xor_0 = [0,  8,  4, 12,  2, 10,  6, 14,  1,  9,  5, 13,  3, 11,  7, 15]
dithering_xor_1 = [1,  9,  5, 13,  3, 11,  7, 15,  0,  8,  4, 12,  2, 10,  6, 14]
dithering_xor_2 = [2, 10,  6, 14,  0,  8,  4, 12,  3, 11,  7, 15,  1,  9,  5, 13]
dithering_xor_3 = [3, 11,  7, 15,  1,  9,  5, 13,  2, 10,  6, 14,  0,  8,  4, 12]
dithering_xor_4 = [4, 12,  0,  8,  6, 14,  2, 10,  5, 13,  1,  9,  7, 15,  3, 11]
dithering_xor_5 = [5, 13,  1,  9,  7, 15,  3, 11,  4, 12,  0,  8,  6, 14,  2, 10]
dithering_xor_6 = [6, 14,  2, 10,  4, 12,  0,  8,  7, 15,  3, 11,  5, 13,  1,  9]
dithering_xor_7 = [7, 15,  3, 11,  5, 13,  1,  9,  6, 14,  2, 10,  4, 12,  0,  8]
dithering_xor_8 = [8,  0, 12,  4, 10,  2, 14,  6,  9,  1, 13,  5, 11,  3, 15,  7]
dithering_xor_9 = [9,  1, 13,  5, 11,  3, 15,  7,  8,  0, 12,  4, 10,  2, 14,  6]
dithering_xor_A = [10,  2, 14,  6,  8,  0, 12,  4, 11,  3, 15,  7,  9,  1, 13,  5]
dithering_xor_B = [11,  3, 15,  7,  9,  1, 13,  5, 10,  2, 14,  6,  8,  0, 12,  4]
dithering_xor_C = [12,  4,  8,  0, 14,  6, 10,  2, 13,  5,  9,  1, 15,  7, 11,  3]
dithering_xor_D = [13,  5,  9,  1, 15,  7, 11,  3, 12,  4,  8,  0, 14,  6, 10,  2]
dithering_xor_E = [14,  6, 10,  2, 12,  4,  8,  0, 15,  7, 11,  3, 13,  5,  9,  1]
dithering_xor_F = [15,  7, 11,  3, 13,  5,  9,  1, 14,  6, 10,  2, 12,  4,  8,  0]


def dithermap_to_threshold(dithermap):
    length = len(dithermap)
    output = [(i + 0.5)/length for i in dithermap]
    return(output)


def dither_1D(iter):
    """Create 1 x 2^iter dithering map.
    """
    length = 2**iter
    format_string = '0' + str(iter) + 'b'
    list = [1 - int(format(i, format_string)[::-1], 2)
            for i in range(length)[::-1]]
    threshold = np.array(list)
    return(threshold)


def dither(heightmap, dither_map):
    temp_list = []
    for i, value in enumerate(heightmap):
        threshold = dither_map[i]
        if value >= threshold:
            temp_list.append('X')
        else:
            temp_list.append('-')
    return temp_list
