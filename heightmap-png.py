from midigen import heightmap

map = heightmap.diamond_square(8, 0.5, "Math Center", None)
map = heightmap.heightmap_normalize(map)
print("Map in memory")
heightmap.heightmap_to_png(map, "mathcenter")
