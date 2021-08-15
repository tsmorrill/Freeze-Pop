#!/usr/bin/python



mult_height = 1/8
stress_height = 1

pitch_height = 1
scale = [60, 62, 65, 67, 70, 72]
# scale = [i for i in range(60, 73)]

offbeat_height = 2/3

if len(sys.argv) > 1:
    seed = str(sys.argv[1])
else:
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    seed = ''.join(random.choice(chars) for i in range(8))

iter = 4

smoothing = 0.6
mult_init = [[0, 0],
             [0, 0]]
mult_map = diamond_square(iter, smoothing, seed + "mult_map", mult_init)
mult_map *= mult_height
mult_map += 1 - mult_height

heightmap_to_png(mult_map, "uniform")
