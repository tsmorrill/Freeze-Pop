from midigen import heightmap, dither, strings
import string
import random

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
seed = ''.join(random.choice(chars) for i in range(8))
print(seed)

map = heightmap.diamond_square(2, 1, seed, None)
map = heightmap.map_interp(map)
map = map.flatten()

threshold = dither.dither_1D(4)
beat_list = dither.dither(map, threshold)
string = strings.list_to_print_str(beat_list)

print(string)
