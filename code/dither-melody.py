#!/usr/bin/python

import math
import random
import string
import sys

import numpy as np

from dither import dither_1D
from heightmap import diamond_square, entrywise_product, heightmap_radar_list
from midiutil.MidiFile import MIDIFile

mult_height = 1/8
stress_height = 1
phrase_length = 1
resolution = 16
oversampling = 1
iter = int(np.log2(phrase_length*resolution)) + 1
takes = 16

pitch_height = 1.0
scale = [60, 62, 65, 67, 70, 72]
# scale = [i for i in range(60, 73)]

offbeat_height = 1
map_size = 2**(iter - 1) + 1

if len(sys.argv) > 1:
    seed = str(sys.argv[1])
else:
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    seed = ''.join(random.choice(chars) for i in range(8))

smoothing = 0
mult_init = None
mult_map = diamond_square(iter + oversampling, smoothing, seed + "mult_map", mult_init)
mult_map *= mult_height
mult_map += 1 - mult_height

smoothing = 0
stress_init = None
stress_map = diamond_square(iter + oversampling, smoothing, seed + "stress_map", stress_init)
stress_map = entrywise_product(stress_map, mult_map)
stress_map = heightmap_radar_list(stress_map, phrase_length*resolution, takes)
stress_map *= stress_height

smoothing = 0
pitch_init = None
pitch_map = diamond_square(iter + oversampling, smoothing, seed + "pitch_map", pitch_init)
pitch_map = entrywise_product(pitch_map, mult_map)
pitch_map = heightmap_radar_list(pitch_map, phrase_length*resolution, takes)
pitch_map *= pitch_height

smoothing = 0
offbeat_init = None
offbeat_map = diamond_square(iter + oversampling, smoothing,
                             seed + "offbeat_map", offbeat_init)
offbeat_map = entrywise_product(offbeat_map, mult_map)
offbeat_map = heightmap_radar_list(offbeat_map, phrase_length*resolution, takes)
offbeat_map *= offbeat_height

threshold_map = dither_1D(2*iter)
for (i,), value in np.ndenumerate(offbeat_map):
    if value > 0.5:
        threshold_map[i] = 1 - threshold_map[i]

# comma required to denote 1-tuple
rhythm = [threshold_map[i % len(threshold_map)] <= value
          for (i,), value in np.ndenumerate(stress_map)]

output_file = MIDIFile(1)
track = 0
time = 0
channel = 0
duration = 4/resolution
length_in_bars = len(rhythm) // resolution
track_name = "melody " + seed + " {} bar".format(length_in_bars)
if (length_in_bars) > 1:
    track_name += "s"
output_file.addTrackName(track, time, track_name)
for index, play_note in enumerate(rhythm):
    if play_note:
        pitch_index = math.floor(len(scale)*pitch_map[index])
        pitch_index = min(pitch_index, len(scale)-1)
        pitch = scale[pitch_index]
        time = index*duration
        # no zero velocity notes
        volume = math.ceil(stress_map[index]*127)
        volume = max(volume, 1)
        output_file.addNote(track, channel, pitch, time, duration, volume)

filename = track_name + ".mid"
try:
    with open(filename, 'wb') as outf:
        output_file.writeFile(outf)
    print("Created file {}".format(filename))
except:
    print("Write failed.")
