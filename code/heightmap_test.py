#!/usr/bin/python

import math
import random
import string
import sys

import numpy as np

from dither import dither_1D
from heightmap import diamond_square, erode, heightmap_to_png
from midiutil.MidiFile import MIDIFile

smoothing = 1

seed = 'test'

init = [[0, 0],
        [0, 0]]
for iter in range(1, 10):
    heightmap = diamond_square(iter, smoothing, seed, init=init)

    heightmap_to_png(heightmap, seed + ' ' + str(iter))
