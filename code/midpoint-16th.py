#!/usr/bin/python

import math
import random
import string
import sys

import numpy as np

from dither import dither_1D
from heightmap import diamond_square
from midiutil.MidiFile import MIDIFile

if len(sys.argv) > 1:
    seed = str(sys.argv[1])
else:
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    seed = ''.join(random.choice(chars) for i in range(8))

iter = 4
smoothing = 0

stress_init = np.array([[1, 0],
                 [1, 0]])
stress_map = diamond_square(iter, smoothing, seed + "stress_map", stress_init)

# delete bottom row
stress_map = np.delete(stress_map, -1, 0)
# delete right column
stress_map = np.delete(stress_map, -1, 1)
stress_map = stress_map.flatten()

# dither
threshold = []
threshold = dither_1D(2*iter)
# comma required to denote 1-tuple
rhythm = [threshold[i % len(threshold)] < value
          for (i,), value in np.ndenumerate(stress_map)]

output_file = MIDIFile(1)
track = 0
time = 0
channel = 0
pitch = 60
duration = 1/4
track_name = "16ths " + seed + " {} bar".format(len(rhythm) // 16)
if (len(rhythm) // 16) > 1:
    track_name += "s"
output_file.addTrackName(track, time, track_name)
for index, play_note in enumerate(rhythm):
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
