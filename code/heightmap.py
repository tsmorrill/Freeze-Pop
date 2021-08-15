from mpl_toolkits import mplot3d
import random

import numpy as np
import matplotlib.pyplot as plt

def heightmap_1D(iter, smoothing, seed, init):
    """Create 2^iter + 1 linear heightmap via midpoint displacement.
    """
    if init == None:
        random.seed(seed + "init")
        heightmap = np.array([random.random(), random.random()])
    else:
        heightmap = init

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
    if init == None:
        random.seed(seed + "init")
        heightmap = np.array([[random.random(), random.random()],
                              [random.random(), random.random()]])
    else:
        heightmap = np.array(init)

    random.seed(seed + "iterate")
    for n in range(iter):
        rows, cols = heightmap.shape
        temp_map = np.zeros((2*rows - 1, 2*cols - 1))
        jitter_diamond = 2**(-smoothing*(2*n + 1))
        jitter_square  = 2**(-smoothing*(2*n + 2))
        for (i, j), value_ij in np.ndenumerate(heightmap):
            north_exists = i > 0
            south_exists = i < rows - 1
            west_exists  = j > 0
            east_exists  = j < cols - 1

            temp_map[2*i, 2*j] = heightmap[i, j]

            if east_exists and south_exists:
                diamond_center = (heightmap[i, j] + heightmap[i, j+1]
                                  + heightmap[i+1, j] + heightmap[i+1, j+1])
                diamond_center /= 4
                diamond_center += random.uniform(-1,1)*jitter_diamond
                temp_map[2*i + 1, 2*j + 1] = diamond_center

                square_top = (heightmap[i, j] + heightmap[i, j+1]
                             + diamond_center)
                if north_exists:
                    square_top += temp_map[2*i + 1, 2*j - 1]
                    square_top /= 4
                else:
                    square_top /= 3
                square_top += random.uniform(-1,1)*jitter_square
                temp_map[2*i, 2*j + 1] = square_top

                square_left = (heightmap[i, j] + heightmap[i+1, j]
                              + diamond_center)
                if west_exists:
                    square_left += temp_map[2*i + 1, 2*j - 1]
                    square_left /= 4
                else:
                    square_left /= 3
                square_left += random.uniform(-1,1)*jitter_square
                temp_map[2*i + 1, 2*j] = square_left
            elif east_exists and not south_exists:
                square_top = (heightmap[i, j] + heightmap[i, j+1]
                             + temp_map[2*i - 1, 2*j + 1])/3
                square_top += random.uniform(-1,1)*jitter_square
                temp_map[2*i, 2*j + 1] = square_top
            elif not east_exists and south_exists:
                square_left = (heightmap[i, j] + heightmap[i+1, j]
                             + temp_map[2*i + 1, 2*j - 1])/3
                square_left += random.uniform(-1,1)*jitter_square
                temp_map[2*i + 1, 2*j] = square_left
        heightmap = temp_map

        # noise = 2*np.random.random(heightmap.shape) - 1
        # noise /= 2**(n+5)
        # heightmap += noise

        # heightmap_to_png(heightmap, seed + ' ' + str(n))

    # normalize
    heightmap -= heightmap.min()
    heightmap /= heightmap.max()
    return(heightmap)

def trim_and_flatten(heightmap, rows=1, cols=1):
    for i in range(rows):
        heightmap = np.delete(heightmap, -1, 0)
    for j in range(cols):
        heightmap = np.delete(heightmap, -1, 1)
    heightmap = heightmap.flatten()
    return(heightmap)

def entrywise_product(heightmap0, heightmap1, normalize=True):
    output = np.zeros(heightmap0.shape)
    for (i, j), value in np.ndenumerate(heightmap0):
        output[i,j] = heightmap0[i,j]*heightmap1[i,j]
    if normalize:
        output = heightmap_normalize(output)
    return(output)

def heightmap_normalize(heightmap):
    heightmap -= heightmap.min()
    heightmap /= heightmap.max()
    return(heightmap)

def heightmap_radar_list(heightmap, r_step, theta_step,
                         init_angle=0, sweep=np.pi):
    """Read and interpolate a square heightmap radially from the center.
    """
    N = heightmap.shape[0]
    list = []
    for turn in range(theta_step):
        angle = sweep*turn/theta_step
        for length in range(r_step):
            x, y = length*np.cos(angle), length*np.sin(angle)
            # correct for orientation
            i, j = int(np.floor(y + N/2)), int(np.floor(x + N/2))
            u, v = y + N/2 - i, x + N/2 - j
            A, B = heightmap[  i, j], heightmap[  i, j+1]
            C, D = heightmap[i+1, j], heightmap[i+1, j+1]
            interp = (A*(1-v) + B*v)*(1-u) + (C*(1-v) + D*v)*u
            list.append(interp)
    list = np.array(list)
    return(list)

def erode(heightmap, seed, iter):
    rows, cols = heightmap.shape
    random.seed(seed + "rain")

    for n in range(iter):
        i = random.randint(0, rows-1)
        j = random.randint(0, cols-1)
        droplet_volume = 1
        while droplet_volume > 0:
            north_exists = i > 0
            south_exists = i < rows - 1
            west_exists  = j > 0
            east_exists  = j < cols - 1

            current_min = heightmap[i, j]
            choices = [(0, 0)]

            if north_exists:
                new_height = heightmap[i - 1, j]
                if new_height < current_min:
                    min = heightmap
                    choices = [(i - 1, j)]
                elif new_height == current_min:
                    choices.append((i - 1, j))
            if south_exists:
                new_height = heightmap[i + 1, j]
                if new_height < current_min:
                    min = heightmap
                    choices = [(i + 1, j)]
                elif new_height == current_min:
                    choices.append((i + 1, j))
            if west_exists:
                new_height = heightmap[i, j - 1]
                if new_height < current_min:
                    min = heightmap
                    choices = [(i, j - 1)]
                elif new_height == current_min:
                    choices.append((i, j - 1))
            if east_exists:
                new_height = heightmap[i, j + 1]
                if new_height < current_min:
                    min = heightmap
                    choices = [(i, j + 1)]
                elif new_height == current_min:
                    choices.append((i, j + 1))

            if len(choices) == 1:
                new_i, new_j = choices[0]
            else:
                random.seed(seed + "choose")
                new_i, new_j = random.choice(choices)
            if (i, j) == (new_i, new_j):
                droplet_volume = -1
            else:
                average = (heightmap[i, j] + heightmap[new_i, new_j])/2
                heightmap[i, j] = average
                heightmap[new_i, new_j] = average
                droplet_volume -= random.random()/8
                i, j = new_i, new_j

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

    plt.gca().axes.get_xaxis().set_ticks([])
    plt.gca().axes.get_yaxis().set_ticks([])

    plt.xlabel('X')
    plt.ylabel('Y')

    filename += '.png'
    plt.savefig(filename)
    plt.close('all')
