from mpl_toolkits import mplot3d
import random

import numpy as np
import matplotlib.pyplot as plt


def heightmap_1D(iter, smoothing, seed, init):
    """Create 2^iter + 1 linear heightmap via midpoint displacement.
    """
    if type(init) == "<class 'numpy.ndarray'>":
        heightmap = init
    else:
        random.seed(seed + "init")
        heightmap = np.array([random.random(), random.random()])

    random.seed(seed + "iterate")
    for i in range(iter):
        temp_list = []
        for j in range(2**i):
            temp_list.append(heightmap[j])
            temp_list.append((heightmap[j]+heightmap[j+1])/2
                             + random.uniform(-1,1)*2**(-smoothing*(i+1)))
        temp_list.append(heightmap[-1])
        heightmap = np.array(temp_list)

    # normalize
    heightmap += heightmap.min()
    heightmap /= heightmap.max()
    return(heightmap)

def diamond_square(iter, smoothing, seed, init):
    """Create 2^iter + 1 square heightmap via diamond square algorithm.
    """
    if type(init) == "<class 'numpy.ndarray'>":
        heightmap = init
    else:
        random.seed(seed + "init")
        heightmap = np.array([[random.random(), random.random()],
                              [random.random(), random.random()]])

    random.seed(seed + "iterate")
    for n in range(iter):
        rows, columns = heightmap.shape
        temp_map = np.zeros((2*rows - 1, 2*columns - 1))
        for (i, j), value_ij in np.ndenumerate(heightmap):
            north_exists = i > 0
            south_exists = i < rows - 1
            west_exists  = j > 0
            east_exists  = j < columns - 1

            temp_map[2*i, 2*j] = value_ij

            if east_exists and south_exists:
                diamond_center = (heightmap[i, j] + heightmap[i, j+1]
                                  + heightmap[i+1, j] + heightmap[i+1, j+1])/4
                diamond_center += random.uniform(-1,1)*2**(-smoothing*(i+1))
                temp_map[2*i + 1, 2*j + 1] = diamond_center

                square_top = (heightmap[i, j] + heightmap[i, j+1]
                             + temp_map[i-1, j+1] + temp_map[i+1, j+1])/4
                square_top += random.uniform(-1,1)*2**(-smoothing*(i+1))
                temp_map[2*i, 2*j + 1] = square_top

                square_left = (heightmap[i, j] + heightmap[i+1, j]
                             + temp_map[i+1, j-1] + temp_map[i+1, j+1])/4
                square_left += random.uniform(-1,1)*2**(-smoothing*(i+1))
                temp_map[2*i + 1, 2*j] = square_left
            elif east_exists and not south_exists:
                square_top = (heightmap[i, j] + heightmap[i, j+1]
                             + temp_map[i-1, j+1])/3
                square_top += random.uniform(-1,1)*2**(-smoothing*(i+1))
                temp_map[2*i, 2*j + 1] = square_top
            elif not east_exists and south_exists:
                square_left = (heightmap[i, j] + heightmap[i+1, j]
                             + temp_map[i+1, j-1])/3
                square_left += random.uniform(-1,1)*2**(-smoothing*(i+1))
                temp_map[2*i + 1, 2*j] = square_left
        heightmap = temp_map

        heightmap_to_png(heightmap, seed + ' ' + str(n))

    # normalize
    heightmap -= heightmap.min()
    heightmap /= heightmap.max()
    return(heightmap)

def heightmap_to_png(heightmap, filename):
    rows, cols = heightmap.shape

    x = [i for i in range(cols)]
    # correct for orientation
    y = [-i for i in range(rows)]
    # prepare for plot_surface
    x, y = np.meshgrid(x, y)
    z = heightmap

    px = 1/plt.rcParams['figure.dpi']  # pixel in inches
    fig = plt.figure(figsize = (800*px, 800*px))
    ax = plt.axes(projection = '3d')

    my_cmap = plt.get_cmap('cool')

    stride = 1
    surf = ax.plot_surface(x, y, z, cmap = my_cmap, rstride=stride, cstride=stride, antialiased=False)

    ax.view_init(elev=45, azim=-100)
    ax.set_title(filename)

    # plt.gca().axes.get_xaxis().set_ticks([])
    # plt.gca().axes.get_yaxis().set_ticks([])

    plt.xlabel('X')
    plt.ylabel('Y')

    filename += '.png'
    plt.savefig(filename)
    plt.close('all')
