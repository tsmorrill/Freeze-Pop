import numpy as np

def dither_1D(iter):
    """Create 1 x 2^iter dithering matrix.
    """
    length = 2**iter
    format_string = '0' + str(iter) + 'b'
    list = [1 - (int(format(i, format_string)[::-1], 2)+0.5)/length
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
