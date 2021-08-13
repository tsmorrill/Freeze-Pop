#!/usr/bin/python

import math
import random
import string
import sys

import numpy as np

from dither import dither_1D
from heightmap import diamond_square, erode, heightmap_to_png
from midiutil.MidiFile import MIDIFile

iter = 10
smoothing = 1

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
seed = ''.join(random.choice(chars) for i in range(8))

init = None
heightmap = diamond_square(iter, smoothing, seed, init=init)

heightmap_to_png(heightmap, seed)
