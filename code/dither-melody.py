#!/usr/bin/python

import math
import random
import string
import sys

import numpy as np

from dither import dither_1D
from heightmap import diamond_square, entrywise_product, trim_and_flatten
from midiutil.MidiFile import MIDIFile

mult_height = 1/4
stress_height = 1.0

pitch_height = 1.0
scale = [60, 62, 65, 67, 70, 72]
# scale = [i for i in range(60, 73)]

offbeat_height = 2/3

if len(sys.argv) > 1:
    seed = str(sys.argv[1])
else:
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    seed = ''.join(random.choice(chars) for i in range(8))

iter = 3

smoothing = 0
mult_init = [[0, 0],
             [0, 0]]
mult_map = diamond_square(iter, smoothing, seed + "mult_map", mult_init)
mult_map *= mult_height
mult_map += 1 - mult_height

smoothing = 0
stress_init = [[1, 0],
               [1, 0]]
stress_map = diamond_square(iter, smoothing, seed + "stress_map", stress_init)
stress_map = entrywise_product(stress_map, mult_map)
stress_map = trim_and_flatten(stress_map)
stress_map *= stress_height

smoothing = 0
pitch_init = [[0, 0.5],
              [0.5, 1]]
pitch_map = diamond_square(iter, smoothing, seed + "pitch_map", pitch_init)
pitch_map = entrywise_product(pitch_map, mult_map)
pitch_map = trim_and_flatten(pitch_map)
pitch_map *= pitch_height

smoothing = 1
offbeat_init = None
offbeat_map = diamond_square(iter, smoothing,
                             seed + "offbeat_map", offbeat_init)
offbeat_map = entrywise_product(offbeat_map, mult_map)
offbeat_map = trim_and_flatten(offbeat_map)
offbeat_map *= offbeat_height

threshold = dither_1D(2*iter)

for (i,), value in np.ndenumerate(offbeat_map):
    if value > 0.5:
        threshold[i] = 1 - threshold[i]

# comma required to denote 1-tuple
rhythm = [threshold[i % len(threshold)] < value
          for (i,), value in np.ndenumerate(stress_map)]

output_file = MIDIFile(1)
track = 0
time = 0
channel = 0
duration = 1/4
track_name = "melody " + seed + " {} bar".format(len(rhythm) // 16)
if (len(rhythm) // 16) > 1:
    track_name += "s"
output_file.addTrackName(track, time, track_name)
for index, play_note in enumerate(rhythm):
    if play_note:
        pitch_index = math.floor(len(scale)*pitch_map[index])
        pitch_index = min(pitch_index, len(scale)-1)
        pitch = scale[pitch_index]
        time = index/4
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
