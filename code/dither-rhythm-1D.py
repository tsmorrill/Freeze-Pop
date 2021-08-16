#!/usr/bin/python

import math
import random
import string
import sys

import numpy as np

from midiutil.MidiFile import MIDIFile

from midigen import heightmap
from midigen import dither

if len(sys.argv) > 1:
    seed = str(sys.argv[1])
else:
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    seed = ''.join(random.choice(chars) for i in range(8))

iter = 4
# length of rhythm in sixteenth notes
length = 2**iter
smoothing = 1

init = [1, 0]
stress_list = heightmap.heightmap_1D(iter, smoothing, seed + "stress", init)
threshold = dither.dither_1D(iter)
rhythm = [threshold[i] < stress_list[i] for i in range(length)]

#= write MIDI file =============================================================
output_file = MIDIFile(1)
track = 0
time = 0
channel = 0
pitch = 60
duration = 1/4

track_name = "1D rhythm " + seed + " {} bar".format(length // 16)
if (length // 16) > 1:
    track_name += "s"

output_file.addTrackName(track, time, track_name)

for index, play_note in enumerate(rhythm):
    if play_note:
        time = index/4
        # no zero velocity notes
        volume = math.ceil(stress_list[index]*127)
        volume = max(volume, 1)
        output_file.addNote(track, channel, pitch, time, duration, volume)

filename = track_name + ".mid"

try:
    with open(filename, 'wb') as outf:
        output_file.writeFile(outf)
    print("Created file {}".format(filename))
except:
    print("Write failed.")
