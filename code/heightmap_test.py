#!/usr/bin/python

import math
import random
import string
import sys

import numpy as np

from dither import dither_1D
from heightmap import diamond_square, heightmap_to_png
from midiutil.MidiFile import MIDIFile

iter = 8
smoothing = 1

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
seed = ''.join(random.choice(chars) for i in range(8))

init = [[1,2],[3, 4]]

# heightmap_to_png(init, seed + ' 0')

heightmap = diamond_square(iter, smoothing, seed, init=init)
