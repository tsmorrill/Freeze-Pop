#!/usr/bin/python

#= initialize ==================================================================

import math
import random
import string
import sys

from heightmap import heightmap_1D
from midiutil.MidiFile import MIDIFile

if len(sys.argv) > 1:
    seed = str(sys.argv[1])
else:
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    seed = ''.join(random.choice(chars) for i in range(8))

random.seed(seed)

iter = 4
# length of rhythm in sixteenth notes
length = 2**iter

smoothing = 1

stress_list = heightmap_1D(iter, smoothing, seed + "stress")

# dither
threshold = []
format_string = '0' + str(iter) + 'b'

for i in range(length)[::-1]:
    threshold.append((int(format(i, format_string)[::-1], 2)+0.5)/length)

rhythm = []
for i in range(length):
    rhythm.append(stress_list[i] <= threshold[i])

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
