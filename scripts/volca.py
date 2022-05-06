import midigen
import string
import random

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
seed = ''.join(random.choice(chars) for i in range(8))
print(seed)

map = midigen.heightmap.diamond_square(2, 1, seed, None)
map = midigen.map_interp(map)
map = map.flatten()
map = midigen.mean_normalize(map, 3/16)
print(map)

threshold = midigen.dithermap_to_threshold(midigen.dithering_xor_8)

beat_list = midigen.dither(map, threshold)
row_list = midigen.list_to_print_str(beat_list)

for row in row_list:
    print(row)
