import random

def diamond_square(iter, smoothing, seed):
    """Create 2^iter + 1 square heightmap via diamond square algorithm.
    """
    random.seed(seed)
    height_map = [[random.random(), random.random()],
                  [random.random(), random.random()]]
    for n in range(iter):
        in_rows = len(height_map)
        in_cols = len(height_map[0])
        out_rows = 2*in_rows - 1
        out_cols = 2*in_cols - 1
        temp_map = [[None for j in range(out_cols)] for i in range(out_rows)]
        # top row
        i = 0
        row = height_map[0]
        # left column
        j = 0
        center = (random.uniform(-1,1)*2**(-smoothing*n)
                  + (  height_map[i  ][j] + height_map[i  ][j+1]
                     + height_map[i+1][j] + height_map[i+1][j+1])/4)
        top = (random.uniform(-1,1)*2**(-smoothing*n)
               + (height_map[i][j] + height_map[i][j+1] + center)/3)
        left = (random.uniform(-1,1)*2**(-smoothing*n)
                + (height_map[i][j] + height_map[i+1][j] + center)/3)
        temp_map[2*i  ][2*j], temp_map[2*i  ][2*j+1] = row[j], top
        temp_map[2*i+1][2*j], temp_map[2*i+1][2*j+1] = left,   center

        # interior columns
        for j, value in enumerate(row[1:-1]):
            j += 1
            center = (random.uniform(-1,1)*2**(-smoothing*n)
                      + (  height_map[i  ][j] + height_map[i  ][j+1]
                         + height_map[i+1][j] + height_map[i+1][j+1])/4)
            top = (random.uniform(-1,1)*2**(-smoothing*n)
                   + (height_map[i][j] + height_map[i][j+1] + center)/3)
            left = (random.uniform(-1,1)*2**(-smoothing*n)
                    + (height_map[i][j] + height_map[i+1][j]
                       + temp_map[2*i+1][2*j-1] + center)/4)
            temp_map[2*i  ][2*j], temp_map[2*i  ][2*j+1] = row[j], top
            temp_map[2*i+1][2*j], temp_map[2*i+1][2*j+1] = left,   center
        # right column
        j = in_cols - 1
        left = (random.uniform(-1,1)*2**(-smoothing*n)
                + (height_map[i][j] + height_map[i+1][j]
                   + temp_map[2*i+1][2*j-1])/3)
        temp_map[2*i  ][2*j] = row[j]
        temp_map[2*i+1][2*j] = left
        # interior rows
        for i, row in enumerate(height_map[1:-1]):
            i += 1
            # left column
            j = 0
            center = (random.uniform(-1,1)*2**(-smoothing*n)
                      + (  height_map[i  ][j] + height_map[i  ][j+1]
                         + height_map[i+1][j] + height_map[i+1][j+1])/4)
            top = (random.uniform(-1,1)*2**(-smoothing*n)
                   + (height_map[i][j] + height_map[i][j+1]
                      + temp_map[2*i-1][2*j+1] + center)/4)
            left = (random.uniform(-1,1)*2**(-smoothing*n)
                    + (height_map[i][j] + height_map[i+1][j] + center)/3)
            temp_map[2*i  ][2*j], temp_map[2*i  ][2*j+1] = row[j], top
            temp_map[2*i+1][2*j], temp_map[2*i+1][2*j+1] = left,   center
            # interior columns
            for j, value in enumerate(row[1:-1]):
                j += 1
                center = (random.uniform(-1,1)*2**(-smoothing*n)
                          + (  height_map[i  ][j] + height_map[i  ][j+1]
                             + height_map[i+1][j] + height_map[i+1][j+1])/4)
                top = (random.uniform(-1,1)*2**(-smoothing*n)
                       + (height_map[i][j] + height_map[i][j+1]
                          + temp_map[2*i-1][2*j+1] + center)/4)
                left = (random.uniform(-1,1)*2**(-smoothing*n)
                        + (height_map[i][j] + height_map[i+1][j]
                           + temp_map[2*i+1][2*j-1] + center)/4)
                temp_map[2*i  ][2*j], temp_map[2*i  ][2*j+1] = row[j], top
                temp_map[2*i+1][2*j], temp_map[2*i+1][2*j+1] = left,   center
            # right column
            j = in_cols - 1
            left = (random.uniform(-1,1)*2**(-smoothing*n)
                    + (height_map[i][j] + height_map[i+1][j]
                       + temp_map[2*i+1][2*j-1])/3)
            temp_map[2*i  ][2*j] = row[j]
            temp_map[2*i+1][2*j] = left
        # bottom row
        i = in_rows - 1
        row = height_map[i]
        # left column
        j = 0
        top = (random.uniform(-1,1)*2**(-smoothing*n)
               + (height_map[i][j] + height_map[i][j+1] + center)/3)
        temp_map[2*i  ][2*j], temp_map[2*i  ][2*j+1] = row[j], top
        # interior columns
        for j, value in enumerate(row[1:-1]):
            j += 1
            top = (random.uniform(-1,1)*2**(-smoothing*n)
                   + (height_map[i][j] + height_map[i][j+1] + center)/3)

            temp_map[2*i  ][2*j], temp_map[2*i  ][2*j+1] = row[j], top
        # right column
        j = in_cols - 1
        temp_map[2*i][2*j] = row[j]
        height_map = temp_map
    # normalize
    m = min(min(height_map[i]) for i in range(len(height_map)))
    M = max(max(height_map[i]) for i in range(len(height_map)))
    width = M - m
    for i, row in enumerate(height_map):
        for j, value in enumerate(row):
            height_map[i][j] = (value - m)/width
    return(height_map)
