#!/usr/bin/python

#= initialize ==================================================================

import random, string, sys
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

#= create stress pattern via midpoint displacement =============================

stress = [random.random(), random.random()]

# smoothing parameter
h = 1.0

for i in range(iter):
    temp_list = []
    for j in range(2**i):
        temp_list.append(stress[j])
        temp_list.append((stress[j]+stress[j+1])/2
                         + random.uniform(-1,1)*2**(-h*i))
    temp_list.append(stress[-1])
    stress = temp_list

m = min(stress)
M = max(stress)
width = M - m

# normalize
for index, value in enumerate(stress):
    stress[index] = (value - m)/width

#= generate threshold pattern for ordered dithering ============================

threshold = []
format_string = '0' + str(iter) + 'b'

for i in range(length)[::-1]:
    threshold.append((int(format(i, format_string)[::-1], 2)+0.5)/length)

#= dither stress pattern =======================================================

rhythm = []

for i in range(length):
    rhythm.append(stress[i] <= threshold[i])

#= write MIDI file =============================================================

output_file = MIDIFile(1)
track = 0
time = 0
channel = 0
pitch = 60
duration = 1/4

track_name = seed + " {} bar".format(length // 16)
if (length // 16) > 1:
    track_name += "s"

output_file.addTrackName(track, time, track_name)

for index, value in enumerate(rhythm):
    if value:
        time = index/4
        volume = int(stress[index]*127 + 0.5)           # no zero velocity notes
        output_file.addNote(track, channel, pitch, time, duration, volume)

filename = track_name + ".mid"

try:
    with open(filename, 'wb') as outf:
        output_file.writeFile(outf)
    print("Created file {}".format(filename))
except:
    print("Write failed.")

#= print to console ============================================================

# print("Using random seed \"{}\"".format(seed))

# output = [int(value) for value in rhythm]
# print(output)
