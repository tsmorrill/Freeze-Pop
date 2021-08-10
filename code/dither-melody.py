#!/usr/bin/python

import math
import random
import string
import sys

from heightmap import diamond_square
from midiutil.MidiFile import MIDIFile

scale = [60, 62, 64, 66, 67, 69, 71,
         72, 74, 76, 78, 79, 81, 83,
         84]

if len(sys.argv) > 1:
    seed = str(sys.argv[1])
else:
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    seed = ''.join(random.choice(chars) for i in range(8))

iter = 4
length = 2**iter
smoothing = 1.2

stress_map = diamond_square(iter, smoothing, seed + "stress_map")
# trim to 2^iter square and flatten
stress_list = []
for i in range(length // 2):
    stress_list.extend(stress_map[i][:length])
    stress_list.extend(stress_map[i + length//2][:length])

smoothing = 1.4

pitch_map = diamond_square(iter, smoothing, seed + "pitch_map")
# trim to 2^iter square and flatten
pitch_list = []
for i in range(length // 2):
    pitch_list.extend(pitch_map[i][:length])
    pitch_list.extend(pitch_map[i +  length//2][:length])

# dither
threshold = []
format_string = '0' + str(iter) + 'b'
for i in range(length)[::-1]:
    threshold.append((int(format(i, format_string)[::-1], 2)+0.5)/length)
rhythm = []
for i in range(length**2):
    rhythm.append(stress_list[i] <= threshold[i % length])

output_file = MIDIFile(1)
track = 0
time = 0
channel = 0
duration = 1/4
track_name = "melody " + seed + " {} bar".format(len(stress_list) // 16)
if (len(stress_list) // 16) > 1:
    track_name += "s"
output_file.addTrackName(track, time, track_name)
for index, value in enumerate(rhythm):
    if value:
        pitch_index = math.floor(len(scale)*pitch_list[index])
        pitch_index = min(pitch_index, len(scale)-1)
        pitch = scale[pitch_index]
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
